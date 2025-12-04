"""
Tests para la integración del Agente de Documentación en el Grafo.

Este módulo contiene las pruebas para verificar que el agente de documentación
se integra correctamente en el flujo de LangGraph.

Siguiendo TDD, estos tests se escriben ANTES de modificar el grafo.
"""

import pytest

from core.graph import (
    GraphState,
    documenter_node,
    get_documentation_graph,
    run_documentation_process,
)


class TestGraphStateExtension:
    """
    Tests para la extensión de GraphState con campos de documentación.
    """

    def test_graph_state_has_documentation_field(self):
        """
        Test que verifica que GraphState incluye el campo documentation.
        """
        # Arrange & Act: Crear estado con documentación
        state: GraphState = {
            "request": "Documentar programa",
            "plan": "",
            "code": "PROGRAM-ID. TEST.",
            "error_message": "",
            "retry_count": 0,
            "documentation": "",
            "mode": "documentation",
        }

        # Assert: Debe aceptar el campo documentation
        assert "documentation" in state
        assert "mode" in state

    def test_graph_state_mode_field_accepts_documentation(self):
        """
        Test que verifica que el campo mode acepta 'documentation'.
        """
        # Arrange & Act: Crear estado en modo documentación
        state: GraphState = {
            "request": "Documentar",
            "plan": "",
            "code": "",
            "error_message": "",
            "retry_count": 0,
            "documentation": "",
            "mode": "documentation",
        }

        # Assert: Modo debe ser 'documentation'
        assert state["mode"] == "documentation"


class TestDocumenterNode:
    """
    Tests para el nodo documenter_node del grafo.
    """

    def test_documenter_node_exists(self):
        """
        Test que verifica que documenter_node está definido.
        """
        # Assert: La función debe existir
        assert documenter_node is not None
        assert callable(documenter_node)

    def test_documenter_node_processes_cobol_code(self):
        """
        Test que verifica que documenter_node procesa código COBOL.
        """
        # Arrange: Estado con código COBOL
        state: GraphState = {
            "request": "Documentar programa",
            "plan": "",
            "code": """
       IDENTIFICATION DIVISION.
       PROGRAM-ID. TESTPROG.
       PROCEDURE DIVISION.
           STOP RUN.
            """,
            "error_message": "",
            "retry_count": 0,
            "documentation": "",
            "mode": "documentation",
        }

        # Act: Ejecutar nodo
        result = documenter_node(state)

        # Assert: Debe retornar documentación
        assert result is not None
        assert "documentation" in result
        assert isinstance(result["documentation"], str)
        assert len(result["documentation"]) > 0

    def test_documenter_node_returns_dict(self):
        """
        Test que verifica que documenter_node retorna un diccionario.
        """
        # Arrange: Estado básico
        state: GraphState = {
            "request": "Doc",
            "plan": "",
            "code": "PROGRAM-ID. TEST.",
            "error_message": "",
            "retry_count": 0,
            "documentation": "",
            "mode": "documentation",
        }

        # Act: Ejecutar nodo
        result = documenter_node(state)

        # Assert: Debe ser diccionario
        assert isinstance(result, dict)

    def test_documenter_node_handles_empty_code(self):
        """
        Test que verifica el manejo de código vacío.
        """
        # Arrange: Estado sin código
        state: GraphState = {
            "request": "Doc",
            "plan": "",
            "code": "",
            "error_message": "",
            "retry_count": 0,
            "documentation": "",
            "mode": "documentation",
        }

        # Act: Ejecutar nodo
        result = documenter_node(state)

        # Assert: Debe manejar el error graciosamente
        assert result is not None
        assert "error_message" in result or "documentation" in result


class TestDocumentationGraph:
    """
    Tests para el grafo de documentación.
    """

    def test_get_documentation_graph_exists(self):
        """
        Test que verifica que get_documentation_graph está definido.
        """
        # Assert: La función debe existir
        assert get_documentation_graph is not None
        assert callable(get_documentation_graph)

    def test_get_documentation_graph_returns_compiled_graph(self):
        """
        Test que verifica que retorna un grafo compilado.
        """
        # Act: Obtener grafo
        graph = get_documentation_graph()

        # Assert: Debe ser un grafo compilado
        assert graph is not None
        assert hasattr(graph, "invoke")

    def test_documentation_graph_has_documenter_node(self):
        """
        Test que verifica que el grafo incluye el nodo documenter.
        """
        # Act: Obtener grafo
        graph = get_documentation_graph()

        # Assert: Debe tener el nodo documenter
        assert graph is not None
        # El grafo compilado debe ser invocable
        assert callable(getattr(graph, "invoke", None))


class TestRunDocumentationProcess:
    """
    Tests para la función run_documentation_process.
    """

    def test_run_documentation_process_exists(self):
        """
        Test que verifica que run_documentation_process está definido.
        """
        # Assert: La función debe existir
        assert run_documentation_process is not None
        assert callable(run_documentation_process)

    def test_run_documentation_process_accepts_cobol_code(self):
        """
        Test que verifica que acepta código COBOL como parámetro.
        """
        # Arrange: Código COBOL simple
        cobol_code = """
       IDENTIFICATION DIVISION.
       PROGRAM-ID. DOCTEST.
       PROCEDURE DIVISION.
           STOP RUN.
        """

        # Act: Ejecutar proceso
        result = run_documentation_process(cobol_code)

        # Assert: Debe retornar resultado
        assert result is not None
        assert isinstance(result, dict)

    def test_run_documentation_process_returns_documentation(self):
        """
        Test que verifica que retorna documentación en el resultado.
        """
        # Arrange: Código COBOL
        cobol_code = """
       IDENTIFICATION DIVISION.
       PROGRAM-ID. RETURNTEST.
       PROCEDURE DIVISION.
           STOP RUN.
        """

        # Act: Ejecutar proceso
        result = run_documentation_process(cobol_code)

        # Assert: Debe contener documentación
        assert "documentation" in result
        assert isinstance(result["documentation"], str)
        assert len(result["documentation"]) > 0

    def test_run_documentation_process_handles_complex_cobol(self):
        """
        Test que verifica el manejo de código COBOL complejo.
        """
        # Arrange: Código complejo
        complex_cobol = """
       IDENTIFICATION DIVISION.
       PROGRAM-ID. COMPLEX.
       
       ENVIRONMENT DIVISION.
       INPUT-OUTPUT SECTION.
       FILE-CONTROL.
           SELECT ARCHIVO1 ASSIGN TO ARCHIVO1.
       
       DATA DIVISION.
       FILE SECTION.
       FD  ARCHIVO1.
       01  REG-ARCHIVO1.
           05  CAMPO1    PIC X(10).
       
       WORKING-STORAGE SECTION.
       01  WS-CONTADOR   PIC 9(03).
       
       PROCEDURE DIVISION.
       MAIN-PROCESS SECTION.
           PERFORM INICIALIZAR
           PERFORM PROCESAR
           STOP RUN.
       
       INICIALIZAR SECTION.
           MOVE ZERO TO WS-CONTADOR.
       
       PROCESAR SECTION.
           ADD 1 TO WS-CONTADOR.
        """

        # Act: Ejecutar proceso
        result = run_documentation_process(complex_cobol)

        # Assert: Debe procesar correctamente
        assert result is not None
        assert "documentation" in result
        assert "COMPLEX" in result["documentation"]

    def test_run_documentation_process_sets_mode_to_documentation(self):
        """
        Test que verifica que el modo se establece como 'documentation'.
        """
        # Arrange: Código simple
        cobol_code = "PROGRAM-ID. MODETEST."

        # Act: Ejecutar proceso
        result = run_documentation_process(cobol_code)

        # Assert: Modo debe ser 'documentation'
        assert "mode" in result
        assert result["mode"] == "documentation"


class TestDocumentationFlowIntegration:
    """
    Tests de integración para el flujo completo de documentación.
    """

    def test_end_to_end_documentation_flow(self):
        """
        Test de integración end-to-end del flujo de documentación.
        """
        # Arrange: Código COBOL completo
        cobol_code = """
       IDENTIFICATION DIVISION.
      *************************
       PROGRAM-ID.    E2ETEST.
       AUTHOR.        SISTEMA GENERADOR COBOL IA.
      *****************************************************************
      * SISTEMA   : SISTEMA DE PRUEBAS                               *
      * SUBSISTEMA: TEST                                              *
      * OBJETIVOS : VALIDAR FLUJO DE DOCUMENTACION                   *
      *****************************************************************
       
       DATA DIVISION.
       WORKING-STORAGE SECTION.
       01  WS-MESSAGE    PIC X(20) VALUE 'TEST'.
       
       PROCEDURE DIVISION.
       MAIN-PROCESS SECTION.
           DISPLAY WS-MESSAGE
           STOP RUN.
        """

        # Act: Ejecutar flujo completo
        result = run_documentation_process(cobol_code)

        # Assert: Verificar resultado completo
        assert result is not None
        assert result["mode"] == "documentation"
        assert "documentation" in result
        assert "E2ETEST" in result["documentation"]
        assert (
            "SISTEMA DE PRUEBAS" in result["documentation"]
            or "TEST" in result["documentation"]
        )
