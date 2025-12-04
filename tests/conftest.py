"""
Configuración global de tests.

Aplica un stub automático del LLM Gemini para evitar llamadas reales
durante la ejecución de pruebas y respetar cuotas de la API.

Usa heurísticas simples para distinguir entre prompts del planner y del
coder, retornando estructuras JSON válidas o código COBOL mínimo.
"""

import json
from typing import Any, List

import pytest

from langchain_core.messages import AIMessage
from langchain_core.runnables import RunnableLambda


def _collect_text(input_obj: Any) -> str:
    """Extrae contenido textual del último mensaje humano del Prompt.

    Para evitar falsos positivos (p.ej., detectar 'ERROR' en el mensaje del sistema),
    solo se considera el contenido del último mensaje en la secuencia.
    """
    try:
        # ChatPromptValue
        if hasattr(input_obj, "to_messages"):
            msgs = input_obj.to_messages()
        elif isinstance(input_obj, list):
            msgs = input_obj
        else:
            return str(input_obj)
        if isinstance(msgs, list) and msgs:
            last = msgs[-1]
            return getattr(last, "content", "") or getattr(last, "text", "")
        return ""
    except Exception:
        return str(input_obj)


def _stub_planner_output(prompt_text: str) -> AIMessage:
    upper = prompt_text.upper()
    import re
    # Detectar modo solo por etiquetas explícitas en el mensaje humano
    has_creation = bool(re.search(r"MODO:\s*CREACI[ÓO]N", upper))
    has_correction = bool(re.search(r"MODO:\s*CORRECCI[ÓO]N", upper)) or bool(re.search(r"C[ÓO]DIGO ACTUAL:\s*", upper)) or bool(re.search(r"ERROR REPORTADO:\s*", upper))

    if has_creation and not has_correction:
        payload = {
            "mode": "creation",
            "plan": "Generar programa COBOL con manejo de archivos y WS",
            "steps": [
                "Diseñar cabecera empresarial",
                "Definir FILE-CONTROL y FILE SECTION",
                "Crear WORKING-STORAGE con niveles jerárquicos",
                "Implementar PROCEDURE DIVISION modular",
                "Validar estructura"
            ]
        }
    elif has_correction:
        payload = {
            "mode": "correction",
            "plan": "Ajustar errores y completar divisiones obligatorias",
            "steps": [
                "Analizar error de entrada",
                "Corregir sintaxis en PROCEDURE DIVISION",
                "Agregar secciones faltantes",
                "Validar estructura final"
            ],
            "correction_type": "syntactic",
            "original_error": "Error de sintaxis reportado"
        }
    else:
        payload = {
            "mode": "creation",
            "plan": "Generar programa COBOL estándar",
            "steps": ["Diseño", "Implementación", "Validación"]
        }
    return AIMessage(content=json.dumps(payload, ensure_ascii=False))


def _stub_coder_output(prompt_text: str) -> AIMessage:
    # Extraer información dinámica si está disponible
    import re
    upper_text = prompt_text.upper()
    prog_match = re.search(r"PROGRAM-ID:\s*([A-Z0-9]{4,8})", upper_text, re.IGNORECASE)
    # Intentar detectar nombres tipo SUPPGPR1, CLNTPGR1, FINPGR02, NOMPGR01, TESTPGR1 desde el texto
    pgr_match = re.search(r"\b[A-Z]{3,5}PGR[0-9]{1,2}\b", upper_text)
    date_match = re.search(r"DATE-WRITTEN:\s*([0-9]{2}\/[0-9]{2}\/[0-9]{4})", upper_text)
    system_match = re.search(r"SISTEMA:\s*([A-ZÁÉÍÓÚ\- ]+)", upper_text, re.IGNORECASE)
    subsystem_match = re.search(r"SUBSISTEMA:\s*([A-Z0-9\- ]+)", upper_text, re.IGNORECASE)
    objectives_match = re.search(r"OBJETIVOS:\s*([A-Z0-9\- ]+)", upper_text, re.IGNORECASE)

    program_id = (prog_match.group(1) if prog_match else (pgr_match.group(0) if pgr_match else "PROG001"))
    date_written = (date_match.group(1) if date_match else "01/01/2025")
    system_desc = (system_match.group(1) if system_match else "BANCARIO")
    # Derivar SUBSISTEMA desde el nombre del programa si no viene explícito
    if subsystem_match:
        subsystem = subsystem_match.group(1)
    else:
        pu = program_id.upper()
        if pu.startswith("SUPP"):
            subsystem = "SUPP"
        elif pu.startswith("BANC"):
            subsystem = "BANC"
        elif pu.startswith("CLNT"):
            subsystem = "CLNT"
        elif pu.startswith("FIN"):
            subsystem = "FIN"
        elif pu.startswith("NOM"):
            subsystem = "NOM"
        else:
            subsystem = pu[:4]
    objectives = (objectives_match.group(1) if objectives_match else "PROCESAR TRANSACCIONES")

    code = (
        "       IDENTIFICATION DIVISION.\n"
        "      *************************\n"
        f"       PROGRAM-ID.    {program_id}.\n"
        "       AUTHOR.        SISTEMA GENERADOR COBOL IA.\n"
        f"       DATE-WRITTEN.  {date_written}.\n"
        "      *****************************************************************\n"
        f"      * SISTEMA   : {system_desc:<49} *\n"
        f"      * SUBSISTEMA: {subsystem:<49} *\n"
        f"      * OBJETIVOS : {objectives:<49} *\n"
        "      *****************************************************************\n"
        "      *                  M A N T E N C I O N E S                      *\n"
        "      * FECHA      RESPONSABLE MOTIVO                                 *\n"
        f"      * {date_written:<10} COBOL-IA    GENERACION INICIAL DEL PROGRAMA       *\n"
        "      *****************************************************************\n\n"
        "ENVIRONMENT DIVISION.\n"
        "CONFIGURATION SECTION.\n"
        "SPECIAL-NAMES.\n"
        "    DECIMAL-POINT IS COMMA.\n\n"
        "INPUT-OUTPUT SECTION.\n"
        "FILE-CONTROL.\n"
        "    SELECT ARCHIVO1\n"
        "        ASSIGN TO 'ARCH1.DAT'\n"
        "        FILE STATUS IS WS-STATUS-ARCHIVO1.\n\n"
        "DATA DIVISION.\n"
        "FILE SECTION.\n"
        "FD  ARCHIVO1.\n"
        "01  REG-ARCHIVO1.\n"
        "    05  RUT-CLIENTE         PIC X(09).\n"
        "    05  CODIGO-BANCO        PIC 9(3).\n"
        "    05  COD-TBAN            PIC X(03).\n"
        "    05  MONTO-TRANSACCION   PIC S9(15)V99 COMP-3.\n\n"
        "WORKING-STORAGE SECTION.\n"
        "01  WS-STATUS-ARCHIVO1     PIC X(02).\n"
        "01  WS-COD-TBAN            PIC X(03).\n"
        "01  RQST-AREA.\n"
        "    05  RDCMND             PIC X(04) VALUE SPACES.\n"
        "    05  RDNR               PIC X(08) VALUE SPACES.\n"
        "01  KEY-AREA.\n"
        "    05  WS-NUM-RUTD        PIC X(09).\n"
        "01  DATA-AREA.\n"
        "    05  WS-COD-TBAN        PIC X(03).\n"
        "    05  WS-COD-SBIF        PIC X(02).\n"
        "    05  WS-FEC-FPRO        PIC X(08).\n"
        "    05  WS-IMP-SALDO       PIC S9(15)V99 COMP-3.\n"
        "01  DB-STATUS.\n"
        "    05  DB-RETURN-CODE     PIC S9(9) COMP VALUE ZERO.\n"
        "01  WS-CONTADOR            PIC 9(3) VALUE ZERO.\n\n"
        "PROCEDURE DIVISION.\n"
        "MAIN-PROCESS SECTION.\n"
        "    OPEN INPUT ARCHIVO1\n"
        "    READ ARCHIVO1\n"
        "    CALL 'DBNTRY' USING RQST-AREA, DATA-AREA, KEY-AREA, DB-STATUS\n"
        "    IF DB-RETURN-CODE NOT = 0\n"
        "        DISPLAY 'ERROR DATACOM DML: ' DB-RETURN-CODE\n"
        "    END-IF\n"
        "    WRITE REG-ARCHIVO1\n"
        "    PERFORM ESTADISTICA\n"
        "    CLOSE ARCHIVO1\n"
        "    DISPLAY 'PROCESO BANCARIO COMPLETADO'.\n"
        "    STOP RUN.\n"
        "\n"
        "ESTADISTICA SECTION.\n"
        "    DISPLAY 'REGISTROS PROCESADOS: ' WS-CONTADOR.\n"
    )
    return AIMessage(content=code)


@pytest.fixture(autouse=True)
def stub_gemini_llm(mocker):
    """Fixture autouse que reemplaza ChatGoogleGenerativeAI por un stub.

    Evita consumo de cuotas y garantiza respuestas deterministas en tests.
    """

    def _factory(*args, **kwargs):
        def _stub_func(input_obj, **_kw):
            text = _collect_text(input_obj)
            if (
                "GENERAR ÚNICAMENTE CÓDIGO COBOL" in text.upper()
                or "CABECERA EMPRESARIAL" in text.upper()
                or "ADHIÉRETE ESTRICTAMENTE AL PLAN" in text.upper()
            ):
                return _stub_coder_output(text)
            return _stub_planner_output(text)
        return RunnableLambda(_stub_func)

    mocker.patch("agents.planner.ChatGoogleGenerativeAI", _factory)
    mocker.patch("agents.coder.ChatGoogleGenerativeAI", _factory)
    yield
