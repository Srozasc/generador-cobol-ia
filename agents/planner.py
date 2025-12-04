"""
Agente Planificador para el Generador COBOL IA.

Este módulo contiene la lógica del agente planificador que convierte
solicitudes en lenguaje natural a planes técnicos estructurados en JSON.

El agente opera en tres modos:
1. Modo Creación: Convierte solicitudes nuevas en planes de desarrollo
2. Modo Corrección: Genera planes de corrección basados en errores
3. Modo Modificación: Genera planes para cambiar lógica en código existente

Autor: Generador COBOL IA Team
Fecha: 2025
"""

import json
import os
from typing import Any, Dict

from dotenv import load_dotenv
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI

# Cargar variables de entorno
load_dotenv()


def _resolve_gemini_model() -> str:
    """Resuelve el modelo Gemini asegurando un valor soportado.
    Si LLM_MODEL no apunta a un modelo 'gemini-*', usa 'gemini-2.5-flash'.
    """
    val = os.getenv("LLM_MODEL", "gemini-2.5-flash")
    if not str(val).lower().startswith("gemini-"):
        return "gemini-2.5-flash"
    return val


def get_planner_chain():
    """
    Crea y retorna una cadena de LangChain para generar planes técnicos.

    Esta función encapsula:
    - El prompt especializado para planificación técnica
    - La configuración del modelo LLM (ChatGoogleGenerativeAI)
    - El parser de salida (JsonOutputParser)
    - La cadena secuencial que los conecta
    - La lógica de detección de modos (creación vs corrección)

    Returns:
        RunnableSequence: Cadena de LangChain lista para invocar
    """

    # Configuración del modelo LLM desde variables de entorno
    llm = ChatGoogleGenerativeAI(
        model=_resolve_gemini_model(),
        temperature=float(os.getenv("LLM_TEMPERATURE", "0.1")),
        max_output_tokens=int(os.getenv("LLM_MAX_OUTPUT_TOKENS", "64000")),
        max_retries=int(os.getenv("LLM_RETRIES", "3")),
        google_api_key=os.getenv("GOOGLE_API_KEY"),
    )

    # Prompt especializado para planificación técnica
    prompt_template = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                """Eres un analista técnico senior especializado en COBOL.

INSTRUCCIONES CRÍTICAS:
1. Responde ÚNICAMENTE con JSON válido
2. NO agregues texto antes o después del JSON
3. NO uses markdown o formateo adicional
4. Máximo 5 pasos por plan para mantener simplicidad

DETECCIÓN DE MODO AUTOMÁTICA:
- Si el input contiene "MODO: CORRECCIÓN": usa mode "correction"
- Si el input contiene "MODO: CREACIÓN": usa mode "creation"
- Si el input contiene "MODO: MODIFICACIÓN": usa mode "modification"
- Si el input contiene "ERROR REPORTADO": SIEMPRE usa mode "correction"
- Si el input contiene "CÓDIGO ACTUAL" y NO hay error: SIEMPRE usa mode "modification"

FORMATO JSON OBLIGATORIO:

Para CREACIÓN (cuando el input dice "MODO: CREACIÓN"):
{{
    "plan": "Descripción breve del plan",
    "mode": "creation",
    "steps": [
        "Paso 1: Descripción concisa",
        "Paso 2: Descripción concisa",
        "Paso 3: Descripción concisa"
    ]
}}

Para CORRECCIÓN (cuando el input dice "MODO: CORRECCIÓN"):
{{
    "plan": "Plan de corrección del error",
    "mode": "correction",
    "correction_type": "Tipo de error",
    "original_error": "Error reportado",
    "steps": [
        "Paso 1: Análisis del error",
        "Paso 2: Corrección específica",
        "Paso 3: Validación"
    ]
}}

Para MODIFICACIÓN (cuando el input dice "MODO: MODIFICACIÓN"):
{{
    "plan": "Plan de modificación de reglas de negocio",
    "mode": "modification",
    "analysis": "Análisis de impacto (qué variables y párrafos cambian)",
    "steps": [
        "Paso 1: Identificación de variables (existentes o nuevas)",
        "Paso 2: Punto de inserción en PROCEDURE DIVISION",
        "Paso 3: Lógica específica a insertar/modificar"
    ]
}}

IMPORTANTE: Lee cuidadosamente el input para determinar el modo correcto.""",
            ),
            ("human", "{input}"),
        ]
    )

    # Parser de salida JSON (se maneja con safe_json_parser)
    json_parser = JsonOutputParser()

    # Función para procesar la entrada y detectar el modo
    def process_input(data: Dict[str, Any]) -> str:
        """
        Procesa la entrada y formatea el prompt según el modo detectado.

        Args:
            data: Diccionario con la solicitud y datos opcionales

        Returns:
            str: Prompt formateado para el LLM
        """
        request = data.get("request", "")
        code = data.get("code", "")
        original_code = data.get("original_code", "")
        error_message = data.get("error_message", "")

        # Usar original_code si code está vacío (para modo modificación)
        effective_code = code if code else original_code

        # Detección de modo
        if effective_code and error_message:
            # Modo corrección
            return f"""
MODO: CORRECCIÓN
SOLICITUD: {request}
CÓDIGO ACTUAL:
{effective_code}
ERROR REPORTADO: {error_message}

Genera un plan de corrección en formato JSON para resolver este error específico.
"""
        elif effective_code and not error_message:
            # Modo modificación (Nuevo)
            return f"""
MODO: MODIFICACIÓN
SOLICITUD DE CAMBIO: {request}
CÓDIGO ACTUAL:
{effective_code}

TAREA DE ANÁLISIS:
1. **Identificación de Variables**: Busca en DATA DIVISION las variables afectadas.
2. **Punto de Inserción**: Identifica en PROCEDURE DIVISION dónde aplicar la regla.
3. **Lógica de Cambio**: Define la estructura lógica (IF, PERFORM, CALL).

Genera un plan de modificación en formato JSON detallando el análisis y los pasos.
"""
        else:
            # Modo creación
            return f"""
MODO: CREACIÓN
SOLICITUD: {request}

Genera un plan de desarrollo en formato JSON para esta nueva funcionalidad.
"""

    # Crear la cadena secuencial con manejo de errores
    def safe_json_parser(message) -> Dict[str, Any]:
        """Parser JSON con manejo de errores y fallback."""
        try:
            # Extraer el contenido del mensaje de IA
            if hasattr(message, "content"):
                text = message.content
            else:
                text = str(message)

            # Intentar parsear directamente
            return json_parser.parse(text)
        except Exception:
            # Si falla, intentar extraer JSON del texto
            try:
                # Buscar JSON en el texto
                import re

                json_match = re.search(r"\{.*\}", text, re.DOTALL)
                if json_match:
                    json_str = json_match.group()
                    return json.loads(json_str)
                else:
                    # Fallback: crear plan básico
                    return {
                        "plan": "Plan generado con fallback debido a error de parsing",
                        "mode": "creation",
                        "steps": [
                            "Analizar requisitos",
                            "Diseñar solución",
                            "Implementar código",
                            "Realizar pruebas",
                        ],
                    }
            except Exception:
                # Último fallback
                return {
                    "plan": "Plan de emergencia - error en parsing JSON",
                    "mode": "creation",
                    "steps": ["Revisar solicitud", "Generar plan manualmente"],
                }

    from langchain_core.runnables import RunnableLambda

    chain = (
        RunnableLambda(process_input)
        | RunnableLambda(lambda text: {"input": text})
        | prompt_template
        | llm
        | RunnableLambda(safe_json_parser)
    )

    return chain


def generate_plan(
    request: str,
    code: str | None = None,
    error_message: str | None = None,
    original_code: str | None = None,  # Alias para code en modo modificación
) -> Dict[str, Any]:
    """
    Función de conveniencia para generar planes técnicos.

    Args:
        request: Solicitud en lenguaje natural
        code: Código COBOL existente (para corrección o modificación)
        error_message: Mensaje de error (opcional, para modo corrección)
        original_code: Alias para code (para compatibilidad con tests de modificación)

    Returns:
        Dict: Plan técnico estructurado en JSON

    Raises:
        ValueError: Si la solicitud está vacía
        json.JSONDecodeError: Si el LLM no retorna JSON válido
    """
    if not request or not request.strip():
        return {
            "error": "Solicitud vacía",
            "plan": "No se puede generar un plan sin una solicitud específica",
            "mode": "error",
            "steps": ["Proporcionar una solicitud clara y específica"],
        }

    # Preparar datos de entrada
    input_data = {"request": request}

    # Manejar alias original_code
    effective_code = code if code else original_code

    if effective_code:
        input_data["code"] = effective_code
    if error_message:
        input_data["error_message"] = error_message

    # Generar plan usando la cadena
    chain = get_planner_chain()
    try:
        result = chain.invoke(input_data)

        # Validar que el resultado sea un diccionario
        if not isinstance(result, dict):
            raise ValueError("El LLM no retornó un diccionario válido")

        # Asegurar campos obligatorios
        if "plan" not in result:
            result["plan"] = "Plan generado automáticamente"
        if "mode" not in result:
            if effective_code and error_message:
                result["mode"] = "correction"
            elif effective_code:
                result["mode"] = "modification"
            else:
                result["mode"] = "creation"
        if "steps" not in result:
            result["steps"] = ["Revisar y refinar el plan"]

        return result

    except Exception as e:
        # Manejo de errores con respuesta estructurada
        return {
            "error": f"Error al generar plan: {str(e)}",
            "plan": "Plan de fallback debido a error en generación",
            "mode": "error",
            "steps": [
                "Revisar la configuración del LLM",
                "Verificar la conectividad de la API",
                "Intentar nuevamente con una solicitud más específica",
            ],
        }


def _validate_plan_structure(plan: Dict[str, Any]) -> bool:
    """
    Valida que un plan tenga la estructura correcta.

    Args:
        plan: Diccionario con el plan a validar

    Returns:
        bool: True si la estructura es válida
    """
    required_fields = ["plan", "mode", "steps"]

    # Verificar campos obligatorios
    if not all(field in plan for field in required_fields):
        return False

    # Verificar tipos
    if not isinstance(plan["plan"], str):
        return False
    if not isinstance(plan["mode"], str):
        return False
    if not isinstance(plan["steps"], list):
        return False

    # Verificar que los pasos no estén vacíos
    if len(plan["steps"]) == 0:
        return False

    # Verificar modo válido
    valid_modes = ["creation", "correction", "modification", "error"]
    if plan["mode"] not in valid_modes:
        return False

    # Validaciones específicas por modo
    if plan["mode"] == "correction":
        correction_fields = ["correction_type", "original_error"]
        if not all(field in plan for field in correction_fields):
            return False

    return True


def _generate_fallback_plan(request: str, mode: str = "creation") -> Dict[str, Any]:
    """
    Genera un plan de fallback cuando el LLM falla.

    Args:
        request: Solicitud original
        mode: Modo de operación

    Returns:
        Dict: Plan de fallback estructurado
    """
    if mode == "correction":
        return {
            "plan": f"Plan de corrección de fallback para: {request}",
            "mode": "correction",
            "correction_type": "Corrección general",
            "original_error": "Error no especificado",
            "steps": [
                "Analizar el código existente",
                "Identificar la causa del error",
                "Aplicar la corrección necesaria",
                "Validar la solución",
            ],
        }
    else:
        return {
            "plan": f"Plan de desarrollo de fallback para: {request}",
            "mode": "creation",
            "steps": [
                "Analizar los requisitos",
                "Diseñar la estructura del programa",
                "Implementar la lógica principal",
                "Realizar pruebas y validación",
            ],
        }


# Constantes para configuración
DEFAULT_STEPS_CREATION = [
    "Analizar requisitos funcionales",
    "Diseñar estructura de datos",
    "Implementar lógica de negocio",
    "Agregar validaciones y controles de error",
    "Realizar pruebas unitarias",
]

DEFAULT_STEPS_CORRECTION = [
    "Analizar el error reportado",
    "Identificar la causa raíz",
    "Diseñar la corrección",
    "Implementar la solución",
    "Validar que el error se resuelve",
]


# Información de configuración para debugging
def get_planner_info() -> Dict[str, Any]:
    """
    Retorna información sobre la configuración del planificador.

    Returns:
        Dict: Información de configuración
    """
    return {
        "provider": "google-ai-studio",
        "model": os.getenv("LLM_MODEL", "gemini-2.5-flash"),
        "temperature": float(os.getenv("LLM_TEMPERATURE", "0.1")),
        "max_output_tokens": int(os.getenv("LLM_MAX_OUTPUT_TOKENS", "64000")),
        "max_retries": int(os.getenv("LLM_RETRIES", "3")),
        "supported_modes": ["creation", "correction", "modification"],
        "output_format": "JSON",
        "parser_type": "JsonOutputParser",
    }
