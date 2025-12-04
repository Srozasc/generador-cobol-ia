"""
Tests para el Agente de Documentación.

Este módulo contiene las pruebas unitarias para el agente de documentación
que analiza código COBOL y genera documentación técnica en formato Markdown.

Siguiendo TDD, estos tests se escriben ANTES de implementar el agente.
"""

import pytest

# Importación del módulo a implementar
from agents.documenter import generate_documentation, get_documenter_chain


class TestDocumenterAgent:
    """
    Tests principales para el Agente de Documentación.
    """

    def test_creates_chain_successfully(self):
        """
        Test que verifica la creación exitosa de la cadena de documentación.
        """
        # Act: Obtener la cadena
        chain = get_documenter_chain()

        # Assert: Debe retornar una cadena válida
        assert chain is not None
        assert hasattr(chain, "invoke")
        assert callable(getattr(chain, "invoke", None))

    def test_generates_documentation_from_simple_cobol(self):
        """
        Test que verifica la generación de documentación desde código COBOL simple.
        """
        # Arrange: Código COBOL simple
        simple_cobol = """
       IDENTIFICATION DIVISION.
       PROGRAM-ID.    PROG001.
       AUTHOR.        SISTEMA GENERADOR COBOL IA.
       
       ENVIRONMENT DIVISION.
       
       DATA DIVISION.
       WORKING-STORAGE SECTION.
       01  WS-MESSAGE    PIC X(20) VALUE 'HOLA MUNDO'.
       
       PROCEDURE DIVISION.
       MAIN-PROCESS SECTION.
           DISPLAY WS-MESSAGE
           STOP RUN.
        """

        # Act: Generar documentación
        result = generate_documentation(simple_cobol)

        # Assert: Debe retornar documentación válida
        assert result is not None
        assert isinstance(result, str)
        assert len(result) > 0
        # Verificar que contiene elementos clave de Markdown
        assert "#" in result  # Headers de Markdown
        assert "PROG001" in result  # Debe mencionar el program ID

    def test_extracts_program_metadata(self):
        """
        Test que verifica la extracción de metadatos del programa.
        """
        # Arrange: Código con metadatos completos
        cobol_with_metadata = """
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
       
       PROCEDURE DIVISION.
           STOP RUN.
        """

        # Act: Generar documentación
        result = generate_documentation(cobol_with_metadata)

        # Assert: Debe extraer metadatos clave
        assert "SUPPGPR1" in result
        assert "PROVISIONES" in result or "SUP" in result

    def test_identifies_file_operations(self):
        """
        Test que verifica la identificación de operaciones con archivos.
        """
        # Arrange: Código con archivos
        cobol_with_files = """
       IDENTIFICATION DIVISION.
       PROGRAM-ID. FILETEST.
       
       ENVIRONMENT DIVISION.
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
       
       FD  SUPD00
           LABEL RECORD IS STANDARD.
       01  REG-SUPD00.
           05  COD-CLIE         PIC X(10).
       
       PROCEDURE DIVISION.
           STOP RUN.
        """

        # Act: Generar documentación
        result = generate_documentation(cobol_with_files)

        # Assert: Debe identificar archivos
        assert "CTACTG" in result or "archivo" in result.lower()
        assert "SUPD00" in result or "archivo" in result.lower()

    def test_summarizes_procedure_logic(self):
        """
        Test que verifica el resumen de la lógica del procedimiento.
        """
        # Arrange: Código con lógica de negocio
        cobol_with_logic = """
       IDENTIFICATION DIVISION.
       PROGRAM-ID. LOGICTEST.
       
       DATA DIVISION.
       WORKING-STORAGE SECTION.
       01  WS-CONTADOR    PIC 9(03) VALUE ZERO.
       
       PROCEDURE DIVISION.
       MAIN-PROCESS SECTION.
           PERFORM INICIALIZAR
           PERFORM PROCESAR-DATOS
           PERFORM FINALIZAR
           STOP RUN.
       
       INICIALIZAR SECTION.
           MOVE ZERO TO WS-CONTADOR
           DISPLAY 'INICIANDO PROCESO'.
       
       PROCESAR-DATOS SECTION.
           ADD 1 TO WS-CONTADOR
           DISPLAY 'PROCESANDO: ' WS-CONTADOR.
       
       FINALIZAR SECTION.
           DISPLAY 'PROCESO COMPLETADO'.
        """

        # Act: Generar documentación
        result = generate_documentation(cobol_with_logic)

        # Assert: Debe resumir la lógica
        assert "INICIALIZAR" in result or "inicializ" in result.lower()
        assert "PROCESAR" in result or "proces" in result.lower()
        assert "FINALIZAR" in result or "finaliz" in result.lower()

    def test_output_is_valid_markdown(self):
        """
        Test que verifica que la salida sea Markdown válido.
        """
        # Arrange: Código COBOL básico
        basic_cobol = """
       IDENTIFICATION DIVISION.
       PROGRAM-ID. MDTEST.
       PROCEDURE DIVISION.
           STOP RUN.
        """

        # Act: Generar documentación
        result = generate_documentation(basic_cobol)

        # Assert: Debe ser Markdown válido
        assert isinstance(result, str)
        # Verificar elementos de Markdown
        assert "#" in result  # Headers
        assert "**" in result or "*" in result  # Bold o Italic
        # No debe contener código COBOL crudo sin formatear
        assert "```" in result or result.count("\n") > 3  # Code blocks o estructura


class TestDocumenterEdgeCases:
    """
    Tests para casos extremos del documentador.
    """

    def test_handles_empty_code(self):
        """
        Test que verifica el manejo de código vacío.
        """
        # Arrange: Código vacío
        empty_code = ""

        # Act & Assert: Debe manejar graciosamente
        with pytest.raises(ValueError):
            generate_documentation(empty_code)

    def test_handles_invalid_cobol(self):
        """
        Test que verifica el manejo de código COBOL inválido.
        """
        # Arrange: Código que no es COBOL
        invalid_code = "This is not COBOL code at all!"

        # Act: Generar documentación
        result = generate_documentation(invalid_code)

        # Assert: Debe generar algo, aunque sea un mensaje de advertencia
        assert result is not None
        assert isinstance(result, str)

    def test_handles_very_large_cobol_program(self):
        """
        Test que verifica el manejo de programas COBOL muy grandes.
        """
        # Arrange: Programa grande (simulado con repeticiones)
        large_cobol = """
       IDENTIFICATION DIVISION.
       PROGRAM-ID. LARGEPROG.
       
       DATA DIVISION.
       WORKING-STORAGE SECTION.
        """
        # Agregar muchas variables
        for i in range(100):
            large_cobol += f"       01  WS-VAR-{i:03d}    PIC X(10).\n"

        large_cobol += """
       PROCEDURE DIVISION.
           STOP RUN.
        """

        # Act: Generar documentación
        result = generate_documentation(large_cobol)

        # Assert: Debe manejar programas grandes
        assert result is not None
        assert isinstance(result, str)
        assert "LARGEPROG" in result


class TestDocumenterConfiguration:
    """
    Tests para la configuración del documentador.
    """

    def test_uses_correct_llm_configuration(self):
        """
        Test que verifica la configuración correcta del LLM.
        """
        # Act: Obtener la cadena
        chain = get_documenter_chain()

        # Assert: Verificar que la cadena existe
        assert chain is not None
        assert hasattr(chain, "invoke")

    def test_chain_returns_string_output(self):
        """
        Test que verifica que la cadena retorna string.
        """
        # Arrange: Código simple
        simple_code = """
       IDENTIFICATION DIVISION.
       PROGRAM-ID. STRTEST.
       PROCEDURE DIVISION.
           STOP RUN.
        """

        # Act: Invocar cadena directamente
        chain = get_documenter_chain()
        result = chain.invoke({"cobol_code": simple_code})

        # Assert: Debe retornar string
        assert isinstance(result, str)
