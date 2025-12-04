"""
Agente Codificador - Generador de Código COBOL.

Este módulo contiene la lógica del Agente Codificador que convierte
un plan técnico estructurado en código COBOL funcional.
"""

import os
from datetime import datetime
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


def get_coder_chain():
    """
    Crea y retorna una cadena de LangChain para generar código COBOL.

    Esta función encapsula:
    - El prompt especializado para generación de código COBOL
    - La configuración del modelo LLM (ChatGoogleGenerativeAI)
    - El parser de salida (StrOutputParser)
    - La cadena secuencial que los conecta
    - Lógica dinámica para generar cabeceras empresariales

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

    # Función para enriquecer el contexto con información dinámica
    def enrich_context(inputs: Dict[str, Any]) -> Dict[str, Any]:
        """
        Enriquece el contexto del plan con información dinámica para cabeceras.
        Detecta si es modo modificación (original_code presente) o creación.

        Args:
            inputs: Diccionario con el plan original y opcionalmente original_code

        Returns:
            Dict con plan enriquecido e información dinámica
        """
        plan = inputs.get("plan", "")
        original_code = inputs.get("original_code", "")

        # Convertir plan a string si es un diccionario
        if isinstance(plan, dict):
            plan_text = str(plan)
        else:
            plan_text = str(plan)

        # Detectar modo modificación
        is_modification_mode = bool(original_code)

        if is_modification_mode:
            # Modo Modificación: Retornar plan y código original
            return {
                "plan": plan_text,
                "original_code": original_code,
                "mode": "modification"
            }
        else:
            # Modo Creación: Lógica original
            # Extraer nombre del programa del plan (buscar patrones comunes)
            program_name = "PROG001"  # Default

            # Buscar patrones como "programa XXXX" o "PROGRAM-ID XXXX"
            import re

            program_patterns = [
                r"programa\s+([A-Z0-9]{4,8})",
                r"program-id\s+([A-Z0-9]{4,8})",
                r"llamado\s+([A-Z0-9]{4,8})",
                r"nombre\s+([A-Z0-9]{4,8})",
            ]

            for pattern in program_patterns:
                match = re.search(pattern, plan_text.lower())
                if match:
                    program_name = match.group(1).upper()
                    break

            # Generar información dinámica
            current_date = _get_current_date_formatted()
            system_desc = _infer_system_from_request(plan_text)
            subsystem = _infer_subsystem_from_program(program_name)
            objectives = _extract_objectives_from_request(plan_text)

            # Enriquecer el plan con información dinámica
            enriched_plan = f"""
INFORMACIÓN DINÁMICA PARA CABECERA:
- PROGRAM-ID: {program_name}
- DATE-WRITTEN: {current_date}
- SISTEMA: {system_desc}
- SUBSISTEMA: {subsystem}
- OBJETIVOS: {objectives}

PLAN TÉCNICO ORIGINAL:
{plan}
"""

            return {
                "plan": enriched_plan,
                "program_name": program_name,
                "current_date": current_date,
                "system_desc": system_desc,
                "subsystem": subsystem,
                "objectives": objectives,
                "mode": "creation"
            }

    # Prompt especializado para generación de código COBOL IBM z/OS/390 con Datacom
    # Basado en análisis de código real del cliente bancario
    prompt_template = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                """Eres un programador COBOL senior especializado en IBM z/OS/390
con más de 20 años de experiencia en mainframes bancarios.

REGLA FUNDAMENTAL: TODO programa COBOL DEBE comenzar OBLIGATORIAMENTE
con una cabecera empresarial completa.

EJEMPLO DE CABECERA EMPRESARIAL OBLIGATORIA:
       IDENTIFICATION DIVISION.
      *************************
       PROGRAM-ID.    PROG001.
       AUTHOR.        SISTEMA GENERADOR COBOL IA.
       DATE-WRITTEN.  15/12/2024.
      *****************************************************************
      * SISTEMA   : PROCESAMIENTO BANCARIO EMPRESARIAL               *
      * SUBSISTEMA: BANCARIO                                          *
      * OBJETIVOS : PROCESAR TRANSACCIONES BANCARIAS                 *
      *****************************************************************
      *                  M A N T E N C I O N E S                      *
      * FECHA      RESPONSABLE MOTIVO                                 *
      * 15/12/2024 COBOL-IA    GENERACION INICIAL DEL PROGRAMA       *
      *****************************************************************

INSTRUCCIONES CRÍTICAS PARA CABECERAS:
1. SIEMPRE comenzar el código con la cabecera empresarial completa
2. Usar la información dinámica proporcionada en el prompt humano
3. Mantener el formato exacto con asteriscos y espaciado
4. Incluir todas las secciones: PROGRAM-ID, AUTHOR, DATE-WRITTEN,
SISTEMA, SUBSISTEMA, OBJETIVOS, MANTENCIONES

ESPECIALIZACIONES IBM z/OS/390 BANCARIAS:
1. Genera código para IBM Enterprise COBOL for z/OS
2. Usa convenciones de nomenclatura bancaria empresarial
3. Implementa acceso a Datacom usando DML nativo (NO SQL)
4. Incluye manejo de errores SQL estándar empresarial
5. Usa tipos de datos compatibles con z/OS y sistemas bancarios
6. Implementa múltiples archivos con FILE STATUS
7. Genera estructuras WORKING-STORAGE complejas y jerárquicas
8. Incluye campos bancarios específicos del dominio

REGLAS DE CÓDIGO COBOL EMPRESARIAL:
1. Genera ÚNICAMENTE código COBOL puro, sin explicaciones adicionales
2. Usa MAYÚSCULAS para todo el código COBOL
3. Respeta el formato de columnas COBOL (1-6 números, 7 indicador, 8-72 código)
4. Incluye siempre las 4 divisiones obligatorias:
   - IDENTIFICATION DIVISION (CON CABECERA EMPRESARIAL COMPLETA)
   - ENVIRONMENT DIVISION (con SPECIAL-NAMES y FILE-CONTROL)
   - DATA DIVISION (con FILE SECTION y WORKING-STORAGE SECTION)
   - PROCEDURE DIVISION (con secciones modulares)
5. Usa indentación de 4 espacios para niveles de datos
6. Usa indentación de 8 espacios para procedimientos
7. Termina siempre con STOP RUN
8. Usa nombres descriptivos para variables (formato WS-NOMBRE-VARIABLE)
9. Usa DISPLAY para mostrar mensajes en pantalla

CONFIGURACIÓN z/OS ESTÁNDAR:
SPECIAL-NAMES.
    DECIMAL-POINT IS COMMA.

MANEJO DE MÚLTIPLES ARCHIVOS:
1. Define archivos en FILE-CONTROL con FILE STATUS:
   SELECT ARCHIVO1 ASSIGN TO ARCHIVO1
          FILE STATUS IS WS-STATUS-ARCHIVO1.
   SELECT ARCHIVO2 ASSIGN TO ARCHIVO2
          FILE STATUS IS WS-STATUS-ARCHIVO2.

2. Incluye variables de FILE STATUS en WORKING-STORAGE:
   01  WS-STATUS-ARCHIVO1    PIC X(02).
   01  WS-STATUS-ARCHIVO2    PIC X(02).

3. Maneja errores de archivo:
   IF WS-STATUS-ARCHIVO1 > '00'
       DISPLAY 'ERROR OPEN ARCHIVO1: ' WS-STATUS-ARCHIVO1
       PERFORM ERROR-HANDLING
   END-IF.

ESTRUCTURAS WORKING-STORAGE COMPLEJAS:
1. Usa niveles jerárquicos (01, 05, 10, 15, etc.)
2. Implementa tablas con OCCURS:
   01  TABLA-DATOS.
       05  REGISTRO-DATOS OCCURS 100 TIMES.
           10  CAMPO-ID      PIC X(10).
           10  CAMPO-NOMBRE  PIC X(50).
3. Usa 88-level conditions para validaciones:
   01  WS-ESTADO-PROCESO    PIC X(01).
       88  PROCESO-OK       VALUE 'S'.
       88  PROCESO-ERROR    VALUE 'N'.

CAMPOS BANCARIOS ESPECÍFICOS:
1. RUT Chileno: NUM-RUTD PIC X(09)
2. Código Banco: COD-TBAN PIC X(03)
3. Código SBIF: COD-SBIF PIC X(02)
4. Fecha Proceso: FEC-FPRO PIC X(08) (YYYYMMDD)
5. Código Cliente: COD-CLIE PIC X(10)
6. Montos: IMP-MONTO PIC S9(15)V99 COMP-3
7. Códigos de Segmentación: COD-SEGM PIC X(05)
8. Separadores de Campo: GLS-01 PIC X(01) VALUE '|'

CONVENCIONES DE NOMENCLATURA BANCARIA:
- Programas: máximo 8 caracteres (ej: SUPPGPR1, SUPPGNF6)
- Variables Working Storage: WS-NOMBRE-CAMPO
- Variables de Registro: REG-NOMBRE-CAMPO
- Variables COBOL: COB-NOMBRE-CAMPO
- Contadores: WS-CONT-NOMBRE
- Fechas: WS-FECHA-NOMBRE (formato YYYYMMDD)
- Estados: WS-ESTADO-NOMBRE
- Secciones: NOMBRE-PROCESO SECTION, LEE-ARCHIVO SECTION, ESTADISTICA SECTION

SECCIONES MODULARES OBLIGATORIAS:
1. Sección principal de proceso
2. Secciones de lectura de archivos
3. Sección de manejo de errores
4. Sección de estadísticas (opcional)

ESPECIFICACIONES DATACOM DML NATIVO:
1. Usa DML nativo de Datacom vía llamada al servicio DBNTRY (SIN SQL)
2. Define las áreas estándar para interacción con Datacom:
   - RQST-AREA: área de solicitud/comando
     (ej.: 'FIND', 'READ', 'ADD', 'MODIFY', 'DELETE')
   - KEY-AREA: área de clave para búsquedas/lecturas
   - DATA-AREA: área de datos del registro
   - DB-STATUS: área/campo de estado y código de retorno
3. Ejemplo de definición de áreas:
   01  RQST-AREA.
       05  RDCMND           PIC X(04) VALUE SPACES.
       05  RDNR             PIC X(08) VALUE SPACES.
   01  KEY-AREA.
       05  WS-NUM-RUTD      PIC X(09).
   01  DATA-AREA.
       05  WS-COD-TBAN      PIC X(03).
       05  WS-COD-SBIF      PIC X(02).
       05  WS-FEC-FPRO      PIC X(08).
       05  WS-IMP-SALDO     PIC S9(15)V99 COMP-3.
   01  DB-STATUS.
       05  DB-RETURN-CODE   PIC S9(9) COMP VALUE ZERO.
4. Invocación estándar:
   CALL 'DBNTRY' USING RQST-AREA, DATA-AREA, KEY-AREA, DB-STATUS.
5. Manejo de errores DML:
   - Verificar DB-RETURN-CODE después de cada llamada a DBNTRY
   - Si DB-RETURN-CODE NOT = 0, realizar manejo centralizado de error
   - Registrar códigos y mensajes descriptivos

TIPOS DE DATOS z/OS BANCARIOS:
- PIC X(n) para campos de texto y códigos
- PIC S9(n) COMP-3 para números decimales empaquetados (montos)
- PIC S9(n) COMP para enteros binarios (contadores)
- PIC X(08) para fechas (YYYYMMDD)
- PIC X(06) para horas (HHMMSS)
- PIC X(01) para separadores y flags
- PIC S9(15)V99 COMP-3 para montos grandes
- PIC X(09) para RUT chileno
- PIC X(03) para códigos de banco

MANEJO DE ERRORES ESTÁNDAR EMPRESARIAL:
1. Sección ERROR-HANDLING para manejo centralizado
2. Verificar FILE STATUS después de cada operación de archivo
3. Verificar DB-RETURN-CODE después de cada operación DML Datacom
4. Registrar detalle del error DML (código/condición) para análisis
5. Mostrar mensajes descriptivos con códigos de error
6. Implementar rutinas de abort (PERFORM GNS-PRO-ABT)

ESTRUCTURA DE PROGRAMA ESTÁNDAR CON CABECERA EMPRESARIAL:
       IDENTIFICATION DIVISION.
      *************************
       PROGRAM-ID.    [NOMBRE-PROGRAMA].
       AUTHOR.        SISTEMA GENERADOR COBOL IA.
       DATE-WRITTEN.  [MES-AÑO ACTUAL].
      *****************************************************************
      * SISTEMA   : [DESCRIPCIÓN DEL SISTEMA BASADA EN CONTEXTO]     *
      * SUBSISTEMA: [SUBSISTEMA INFERIDO DEL TIPO DE PROGRAMA]       *
      * OBJETIVOS : [OBJETIVOS EXTRAÍDOS DEL REQUEST DEL USUARIO]    *
      *****************************************************************
      *                  M A N T E N C I O N E S                      *
      * FECHA      RESPONSABLE MOTIVO                                 *
      * [MES-AÑO]  COBOL-IA    GENERACION INICIAL DEL PROGRAMA       *
      *****************************************************************

       ENVIRONMENT DIVISION.
       CONFIGURATION SECTION.
       SPECIAL-NAMES.
           DECIMAL-POINT IS COMMA.
       INPUT-OUTPUT SECTION.
       FILE-CONTROL.
           [Definiciones de archivos con FILE STATUS]

       DATA DIVISION.
       FILE SECTION.
           [Definiciones de registros de archivo]
       WORKING-STORAGE SECTION.
           [Variables de FILE STATUS]
           [Estructuras complejas con niveles jerárquicos]
           [Campos bancarios específicos]
           [Áreas y variables Datacom DML (RQST-AREA, KEY-AREA,
            DATA-AREA, DB-STATUS) si es necesario]

       PROCEDURE DIVISION.
       MAIN-PROCESS SECTION.
           [Lógica principal]
           PERFORM ESTADISTICA
           STOP RUN.

       [OTRAS-SECCIONES] SECTION.
           [Lógica modular]

       ERROR-HANDLING SECTION.
           DISPLAY 'ERROR EN PROCESO'
           STOP RUN.

       ESTADISTICA SECTION.
           DISPLAY 'PROCESO COMPLETADO'.

ADHIÉRETE ESTRICTAMENTE AL PLAN PROPORCIONADO

EJEMPLOS DE CÓDIGO EMPRESARIAL BANCARIO CON CABECERAS:

EJEMPLO 1 - Programa con múltiples archivos y estructuras complejas:
       IDENTIFICATION DIVISION.
      *************************
       PROGRAM-ID.    SUPPGPR1.
       AUTHOR.        SISTEMA GENERADOR COBOL IA.
       DATE-WRITTEN.  ENE-2025.
      *****************************************************************
      * SISTEMA   : SISTEMA DE PROVISIONES Y SEGMENTACION           *
      * SUBSISTEMA: SUP                                              *
      * OBJETIVOS : REGISTROS COMERCIALES CON INTERES CTG           *
      *****************************************************************
      *                  M A N T E N C I O N E S                      *
      * FECHA      RESPONSABLE MOTIVO                                 *
      * ENE-2025   COBOL-IA    GENERACION INICIAL DEL PROGRAMA       *
      *****************************************************************

       ENVIRONMENT DIVISION.
       CONFIGURATION SECTION.
       SPECIAL-NAMES.
           DECIMAL-POINT IS COMMA.
       INPUT-OUTPUT SECTION.
       FILE-CONTROL.
           SELECT CTACTG ASSIGN TO CTACTG
                  FILE STATUS IS WS-STATUS-CTACTG.
           SELECT SUPD00 ASSIGN TO SUPD00
                  FILE STATUS IS WS-STATUS-SUPD00.

       DATA DIVISION.
       FILE SECTION.
       FD  CTACTG
           LABEL RECORD IS STANDARD.
       01  REG-CTACTG.
           05  NUM-RUTD         PIC X(09).
           05  COD-TBAN         PIC X(03).
           05  FEC-FPRO         PIC X(08).
           05  IMP-MONTO        PIC S9(15)V99 COMP-3.

       FD  SUPD00
           LABEL RECORD IS STANDARD.
       01  REG-SUPD00.
           05  COD-CLIE         PIC X(10).
           05  COD-SEGM         PIC X(05).
           05  GLS-01           PIC X(01) VALUE '|'.

       WORKING-STORAGE SECTION.
       01  WS-STATUS-CTACTG     PIC X(02).
       01  WS-STATUS-SUPD00     PIC X(02).
       01  WS-CONT-REGISTROS    PIC S9(07) COMP-3 VALUE ZERO.
       01  WS-ESTADO-PROCESO    PIC X(01).
           88  PROCESO-OK       VALUE 'S'.
           88  PROCESO-ERROR    VALUE 'N'.

       01  TABLA-CTG.
           05  TABLA-MOV-VISA OCCURS 100 TIMES.
               10  VCTG-CTA-CTG    PIC X(04).
               10  VCTG-MONTO      PIC S9(13)V99 COMP-3.

       PROCEDURE DIVISION.
MAIN-PROCESS SECTION.
    OPEN INPUT CTACTG
    IF WS-STATUS-CTACTG > '00'
        DISPLAY 'ERROR OPEN CTACTG: ' WS-STATUS-CTACTG
        PERFORM ERROR-HANDLING
    END-IF
    OPEN OUTPUT SUPD00
    IF WS-STATUS-SUPD00 > '00'
        DISPLAY 'ERROR OPEN SUPD00: ' WS-STATUS-SUPD00
        PERFORM ERROR-HANDLING
    END-IF
    PERFORM LEE-CTA-CTG
    PERFORM ESTADISTICA
    STOP RUN.

LEE-CTA-CTG SECTION.
    READ CTACTG
    PERFORM UNTIL WS-STATUS-CTACTG = '10'
        ADD 1 TO WS-CONT-REGISTROS
        PERFORM PROC-REGISTRO
        READ CTACTG
    END-PERFORM.

PROC-REGISTRO SECTION.
    MOVE NUM-RUTD TO COD-CLIE
    MOVE 'SEG01' TO COD-SEGM
    WRITE REG-SUPD00.

ERROR-HANDLING SECTION.
    DISPLAY 'ERROR EN PROCESO'
    STOP RUN.

ESTADISTICA SECTION.
    DISPLAY 'REGISTROS PROCESADOS: ' WS-CONT-REGISTROS.

EJEMPLO 2 - Consulta DML DATACOM con campos bancarios (SIN SQL):
IDENTIFICATION DIVISION.
PROGRAM-ID. CONSULBCO.
*
* CONSULTA DE DATOS BANCARIOS CON DML NATIVO DATACOM
*
ENVIRONMENT DIVISION.
CONFIGURATION SECTION.
SPECIAL-NAMES.
    DECIMAL-POINT IS COMMA.

DATA DIVISION.
WORKING-STORAGE SECTION.
    01  RQST-AREA.
        05  RDCMND           PIC X(04) VALUE SPACES.
        05  RDNR             PIC X(08) VALUE 'CLIENTE'.
    01  KEY-AREA.
        05  WS-NUM-RUTD      PIC X(09).
    01  DATA-AREA.
        05  WS-COD-TBAN      PIC X(03).
        05  WS-COD-SBIF      PIC X(02).
        05  WS-FEC-FPRO      PIC X(08).
        05  WS-IMP-SALDO     PIC S9(15)V99 COMP-3.
    01  DB-STATUS.
        05  DB-RETURN-CODE   PIC S9(9) COMP VALUE ZERO.
    01  WS-CONT-CONSULTAS    PIC S9(07) COMP-3 VALUE ZERO.

PROCEDURE DIVISION.
MAIN-PROCESS SECTION.
    MOVE '123456789' TO WS-NUM-RUTD
    PERFORM CONSULTA-CLIENTE
    PERFORM ESTADISTICA
    STOP RUN.

CONSULTA-CLIENTE SECTION.
    MOVE 'FIND' TO RDCMND
    CALL 'DBNTRY' USING RQST-AREA, DATA-AREA, KEY-AREA, DB-STATUS
    IF DB-RETURN-CODE = 0
        ADD 1 TO WS-CONT-CONSULTAS
        DISPLAY 'CLIENTE: ' WS-NUM-RUTD
        DISPLAY 'BANCO: ' WS-COD-TBAN
        DISPLAY 'SALDO: ' WS-IMP-SALDO
    ELSE
        DISPLAY 'ERROR DATACOM DML: ' DB-RETURN-CODE
        PERFORM ERROR-HANDLING
    END-IF.

ERROR-HANDLING SECTION.
    DISPLAY 'ERROR EN CONSULTA BANCARIA'
    STOP RUN.

ESTADISTICA SECTION.
    DISPLAY 'CONSULTAS REALIZADAS: ' WS-CONT-CONSULTAS.

FORMATO DE SALIDA:
- Solo código COBOL
- Sin comentarios explicativos
- Sin texto adicional antes o después del código""",
            ),
            (
                "human",
                """Plan técnico a implementar:
{plan}

INFORMACIÓN DINÁMICA PARA CABECERA EMPRESARIAL:
- PROGRAM-ID: {program_name}
- DATE-WRITTEN: {current_date}
- SISTEMA: {system_desc}
- SUBSISTEMA: {subsystem}
- OBJETIVOS: {objectives}

INSTRUCCIONES ESPECÍFICAS:
1. OBLIGATORIO: Usar la información dinámica proporcionada arriba
   para generar la cabecera empresarial
2. Reemplazar los placeholders [NOMBRE-PROGRAMA], [MES-AÑO ACTUAL], etc.
   con los valores específicos proporcionados
3. Generar código COBOL completo que implemente el plan técnico
4. Incluir todas las divisiones obligatorias de COBOL
5. Usar las convenciones empresariales especificadas en el prompt del sistema

Genera ÚNICAMENTE código COBOL puro, sin explicaciones adicionales.""",
            ),
        ]
    )

    # Prompt especializado para MODIFICACIÓN de código COBOL existente
    modification_prompt_template = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                """Eres un Desarrollador COBOL experto en mantenimiento de sistemas mainframe.
Tu especialidad es modificar código COBOL existente sin romper la funcionalidad actual.

REGLAS CRÍTICAS PARA MODIFICACIÓN:
1. **Preservación**: NO elimines ni modifiques lógica existente a menos que el plan lo pida explícitamente
2. **Integración**: Inserta la nueva lógica (IF/PERFORM/CALL) en el punto exacto indicado
3. **Completitud**: Si el plan pide llamar a una rutina que no existe, crea un párrafo stub (esqueleto)
4. **Formato**: Respeta las márgenes COBOL (Área A/B) estrictamente
5. **Estructura**: Mantén todas las divisiones y secciones del código original

CAPACIDADES REQUERIDAS:
- Insertar bloques IF/EVALUATE complejos con múltiples condiciones (AND/OR)
- Agregar llamadas PERFORM o CALL a rutinas nuevas o existentes
- Crear párrafos stub si se necesitan rutinas nuevas
- Preservar comentarios y estructura del código original
- Mantener el estilo de codificación del programa original

FORMATO DE SALIDA:
- Genera el CÓDIGO COBOL COMPLETO modificado
- Sin explicaciones, solo código
- Código compilable y funcional""",
            ),
            (
                "human",
                """CÓDIGO ORIGINAL:
{original_code}

PLAN DE CAMBIOS:
{plan}

INSTRUCCIONES:
1. Analiza el código original cuidadosamente
2. Identifica dónde aplicar los cambios según el plan
3. Implementa los cambios preservando el resto del código
4. Si se necesitan rutinas nuevas (PERFORM/CALL), créalas como stubs al final

Genera ÚNICAMENTE el código COBOL completo modificado.""",
            ),
        ]
    )

    # Parser de salida para obtener string limpio
    output_parser = StrOutputParser()

    # Función para seleccionar el prompt apropiado basado en el modo
    def select_prompt_and_invoke(enriched_data: Dict[str, Any]):
        """Selecciona el prompt template apropiado según el modo e invoca el LLM."""
        mode = enriched_data.get("mode", "creation")
        
        if mode == "modification":
            # Modo modificación: usar prompt de mantenimiento
            messages = modification_prompt_template.invoke(enriched_data)
        else:
            # Modo creación: usar prompt original
            messages = prompt_template.invoke(enriched_data)
        
        # Invocar el LLM con los mensajes generados
        response = llm.invoke(messages)
        
        # Extraer el contenido del mensaje de respuesta
        if hasattr(response, "content"):
            return response.content
        else:
            return str(response)

    from langchain_core.runnables import RunnableLambda

    # Crear la cadena secuencial con enriquecimiento dinámico y selección de prompt
    chain = (
        RunnableLambda(enrich_context)
        | RunnableLambda(select_prompt_and_invoke)
        | output_parser
    )

    return chain


def generate_cobol_code(plan: str) -> str:
    """
    Función de conveniencia para generar código COBOL desde un plan.

    Args:
        plan: Descripción técnica del programa a generar

    Returns:
        str: Código COBOL generado

    Raises:
        ValueError: Si el plan está vacío o es inválido
        Exception: Si hay errores en la generación
    """
    if not plan or not plan.strip():
        raise ValueError("El plan no puede estar vacío")

    try:
        coder_chain = get_coder_chain()
        result = coder_chain.invoke({"plan": plan})

        if not result or not result.strip():
            raise Exception("El LLM no generó código válido")

        return result.strip()

    except Exception as e:
        raise Exception(f"Error al generar código COBOL: {str(e)}")


# Función auxiliar para validar estructura básica de COBOL
def _validate_cobol_structure(code: str) -> bool:
    """
    Valida que el código generado tenga estructura COBOL básica.

    Args:
        code: Código COBOL a validar

    Returns:
        bool: True si tiene estructura válida
    """
    required_elements = [
        "IDENTIFICATION DIVISION.",
        "PROGRAM-ID.",
        "PROCEDURE DIVISION.",
    ]

    return all(element in code for element in required_elements)


# Funciones auxiliares para generar cabeceras empresariales dinámicas
def _get_current_date_formatted() -> str:
    """
    Obtiene la fecha actual en formato DD/MM/YYYY para DATE-WRITTEN.

    Returns:
        str: Fecha en formato DD/MM/YYYY (ej: 15/12/2024)
    """
    now = datetime.now()
    return now.strftime("%d/%m/%Y")


def _infer_system_from_request(request: str) -> str:
    """
    Infiere la descripción del sistema basada en el contexto del request.

    Args:
        request: Texto del request del usuario

    Returns:
        str: Descripción del sistema inferida
    """
    request_lower = request.lower()

    if any(
        keyword in request_lower
        for keyword in ["bancario", "banco", "transacciones", "transaccion"]
    ):
        return "BANCARIO"
    elif any(keyword in request_lower for keyword in ["cliente", "clientes"]):
        return "CLIENTES"
    elif any(
        keyword in request_lower
        for keyword in ["financiero", "finanzas", "reportes financieros"]
    ):
        return "FINANCIERO"
    elif any(keyword in request_lower for keyword in ["cuenta", "cuentas"]):
        return "CUENTAS"
    elif any(keyword in request_lower for keyword in ["nomina", "nómina", "salario"]):
        return "NOMINA"
    else:
        return "GENERAL"


def _infer_subsystem_from_program(program_name: str) -> str:
    """
    Infiere el subsistema basado en el nombre del programa.

    Args:
        program_name: Nombre del programa COBOL

    Returns:
        str: Subsistema inferido
    """
    program_upper = program_name.upper()

    if program_upper.startswith("SUPP"):
        return "SUPP"
    elif program_upper.startswith("BANC"):
        return "BANC"
    elif program_upper.startswith("CLNT"):
        return "CLNT"
    elif program_upper.startswith("FIN"):
        return "FIN"
    elif program_upper.startswith("NOM"):
        return "NOM"
    else:
        # Tomar los primeros 4 caracteres como subsistema
        return program_upper[:4]


def _extract_objectives_from_request(request: str) -> str:
    """
    Extrae los objetivos del programa basado en el request del usuario.

    Args:
        request: Texto del request del usuario

    Returns:
        str: Objetivos extraídos (máximo 50 caracteres)
    """
    request_clean = request.strip().upper()

    # Mapear patrones comunes a objetivos específicos
    if "HOLA MUNDO" in request_clean:
        return "MOSTRAR MENSAJE HOLA MUNDO"
    elif "ARCHIVOS DE CLIENTES" in request_clean:
        return "PROCESAR ARCHIVOS CLIENTES BANCARIOS"
    elif "REPORTES DE SEGMENTACION" in request_clean or "SEGMENTACIÓN" in request_clean:
        return "GENERAR REPORTES SEGMENTACION"
    elif "VALIDAR DATOS" in request_clean:
        return "VALIDAR DATOS ENTRADA"
    elif "PROCESAR" in request_clean and "ARCHIVO" in request_clean:
        return "PROCESAR ARCHIVOS CLIENTES BANCARIOS"
    else:
        # Tomar las primeras palabras significativas
        words = request_clean.split()
        significant_words = [
            w
            for w in words
            if len(w) > 3 and w not in ["CREAR", "PROGRAMA", "COBOL", "QUE"]
        ]
        objective = " ".join(significant_words[:6])  # Máximo 6 palabras
        return objective[:50]  # Máximo 50 caracteres


def _generate_enterprise_header(
    program_name: str, current_date: str, system: str, subsystem: str, objectives: str
) -> str:
    """
    Genera la cabecera empresarial completa para un programa COBOL.

    Args:
        program_name: Nombre del programa COBOL
        current_date: Fecha actual en formato DD/MM/YYYY
        system: Descripción del sistema
        subsystem: Subsistema
        objectives: Objetivos del programa

    Returns:
        str: Cabecera empresarial formateada
    """
    header = f"""       IDENTIFICATION DIVISION.
      *************************
       PROGRAM-ID.    {program_name}.
       AUTHOR.        SISTEMA GENERADOR COBOL IA.
       DATE-WRITTEN.  {current_date}.
      *****************************************************************
      * SISTEMA   : {system:<49} *
      * SUBSISTEMA: {subsystem:<49} *
      * OBJETIVOS : {objectives:<49} *
      *****************************************************************
      *                  M A N T E N C I O N E S                      *
      * FECHA      RESPONSABLE MOTIVO                                 *
      * {current_date:<10} COBOL-IA    GENERACION INICIAL DEL PROGRAMA       *
      *****************************************************************"""

    return header
