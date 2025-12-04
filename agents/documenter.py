"""
Agente de Documentación - Generador de Documentación Técnica COBOL.

Este módulo contiene la lógica del Agente de Documentación que analiza
código fuente COBOL existente y genera documentación técnica estructurada
en formato Markdown.
"""

import os
from typing import Any, Dict

from dotenv import load_dotenv
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI

# Cargar variables de entorno
load_dotenv()


def _resolve_gemini_model() -> str:
    """Resuelve el modelo Gemini asegurando un valor válido.
    Si LLM_MODEL no corresponde a 'gemini-*', usa 'gemini-2.5-flash'.
    """
    val = os.getenv("LLM_MODEL", "gemini-2.5-flash")
    if not str(val).lower().startswith("gemini-"):
        return "gemini-2.5-flash"
    return val


def get_documenter_chain():
    """
    Crea y retorna una cadena de LangChain para generar documentación técnica.

    Esta función encapsula:
    - El prompt especializado para análisis de código COBOL
    - La configuración del modelo LLM (ChatGoogleGenerativeAI)
    - El parser de salida (StrOutputParser)
    - La cadena secuencial que los conecta

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

    # Prompt especializado para documentación de código COBOL
    prompt_template = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                """Eres un Analista Funcional Senior especializado en mainframes IBM z/OS
con más de 20 años de experiencia documentando sistemas COBOL bancarios.

TU MISIÓN: Analizar código fuente COBOL y generar documentación técnica
clara, estructurada y profesional en formato Markdown.

ESTRUCTURA DE ANÁLISIS:

1. **IDENTIFICACIÓN DEL PROGRAMA**
   - Extraer PROGRAM-ID
   - Identificar AUTHOR y DATE-WRITTEN
   - Leer comentarios de cabecera para SISTEMA, SUBSISTEMA, OBJETIVOS
   - Buscar información en sección de MANTENCIONES

2. **ARCHIVOS Y DATOS**
   - Identificar archivos en FILE-CONTROL (SELECT statements)
   - Analizar FILE SECTION para estructuras de registros
   - Detectar variables principales en WORKING-STORAGE SECTION
   - Identificar tablas (OCCURS) y estructuras jerárquicas

3. **LÓGICA DE NEGOCIO**
   - Resumir el flujo principal en PROCEDURE DIVISION
   - Explicar qué hace cada SECTION o PARAGRAPH principal
   - Identificar validaciones y controles de error
   - Detectar llamadas a otros programas o servicios

4. **DEPENDENCIAS**
   - Identificar COPY statements (copybooks)
   - Detectar llamadas CALL a otros programas
   - Identificar acceso a bases de datos (Datacom DML, DB2 SQL)

FORMATO DE SALIDA MARKDOWN:

```markdown
# Documentación Técnica: [PROGRAM-ID]

## Información General
- **Program ID**: [ID]
- **Sistema**: [Sistema extraído de comentarios]
- **Subsistema**: [Subsistema]
- **Autor**: [Autor]
- **Fecha**: [Fecha]
- **Descripción**: [Objetivos del programa]

## Archivos y Datos

### Archivos de Entrada
- **[Nombre Archivo]**: [Descripción y estructura]

### Archivos de Salida
- **[Nombre Archivo]**: [Descripción y estructura]

### Variables Principales
- **[Variable]**: [Tipo y propósito]

## Lógica Principal

### Flujo de Ejecución
1. **[Sección/Párrafo]**: [Descripción de qué hace]
2. **[Sección/Párrafo]**: [Descripción de qué hace]

### Validaciones y Controles
- [Listar validaciones importantes]

## Dependencias
- **Copybooks**: [Lista de COPY]
- **Programas Llamados**: [Lista de CALL]
- **Acceso a Datos**: [DB2, Datacom, etc.]

## Notas Técnicas
[Cualquier observación relevante sobre el código]
```

REGLAS IMPORTANTES:
1. Genera ÚNICAMENTE Markdown, sin texto adicional antes o después
2. Sé conciso pero completo
3. Usa lenguaje técnico pero claro
4. Si no encuentras información, indica "No especificado"
5. Prioriza la claridad sobre la extensión
6. Usa español para las descripciones
""",
            ),
            (
                "human",
                """Analiza el siguiente código COBOL y genera su documentación técnica:

{cobol_code}

Genera la documentación en formato Markdown siguiendo la estructura especificada.""",
            ),
        ]
    )

    # Parser de salida para obtener string limpio
    output_parser = StrOutputParser()

    # Crear la cadena secuencial
    chain = prompt_template | llm | output_parser

    return chain


def generate_documentation(cobol_code: str) -> str:
    """
    Función de conveniencia para generar documentación desde código COBOL.

    Args:
        cobol_code: Código fuente COBOL a documentar

    Returns:
        str: Documentación técnica en formato Markdown

    Raises:
        ValueError: Si el código está vacío o es inválido
        Exception: Si hay errores en la generación
    """
    if not cobol_code or not cobol_code.strip():
        raise ValueError("El código COBOL no puede estar vacío")

    try:
        documenter_chain = get_documenter_chain()
        result = documenter_chain.invoke({"cobol_code": cobol_code})

        if not result or not result.strip():
            raise Exception("El LLM no generó documentación válida")

        return result.strip()

    except Exception as e:
        if isinstance(e, ValueError):
            raise
        raise Exception(f"Error al generar documentación: {str(e)}")


def _validate_markdown_structure(markdown: str) -> bool:
    """
    Valida que el markdown generado tenga estructura básica.

    Args:
        markdown: Texto Markdown a validar

    Returns:
        bool: True si tiene estructura válida
    """
    required_elements = [
        "#",  # Al menos un header
        "**",  # Al menos un elemento en negrita
    ]

    return all(element in markdown for element in required_elements)
