"""
Tests de integración para el flujo completo del generador COBOL IA.

Este módulo contiene pruebas que verifican la integración entre todos los componentes
del sistema: Agente Planificador, Agente Codificador, Validador y Orquestador.
"""

import pytest
from unittest.mock import Mock, patch
from typing import Dict, Any


class TestIntegrationFlow:
    """Pruebas de integración para el flujo completo del sistema."""

    def test_graph_completes_correction_loop(self, mocker):
        """
        Test que verifica el ciclo completo de corrección del sistema.
        
        Escenario:
        1. Usuario solicita generar código COBOL
        2. Planificador genera plan inicial
        3. Codificador genera código con error
        4. Validador detecta error (primera iteración)
        5. Planificador genera plan de corrección
        6. Codificador genera código corregido
        7. Validador aprueba código (segunda iteración)
        8. Sistema termina con éxito
        """
        # Importar el grafo (fallará hasta que se implemente)
        from core.graph import get_compiled_graph
        
        # Configurar mocks directamente en los nodos del grafo
        mock_planner_node = mocker.patch('core.graph.planner_node')
        mock_coder_node = mocker.patch('core.graph.coder_node')
        mock_validator_node = mocker.patch('core.graph.validator_node')
        
        # Configurar respuestas del planificador
        # Primera llamada: plan inicial
        plan_inicial = {
            "plan": "Generar programa HOLA MUNDO en COBOL",
            "mode": "creation",
            "steps": [
                "Crear IDENTIFICATION DIVISION",
                "Crear PROCEDURE DIVISION",
                "Implementar DISPLAY"
            ]
        }
        
        # Segunda llamada: plan de corrección
        plan_correccion = {
            "plan": "Corregir error de sintaxis en programa COBOL",
            "mode": "correction",
            "correction_type": "Error de sintaxis",
            "original_error": "SYNTAX ERROR",
            "steps": [
                "Revisar sintaxis COBOL",
                "Corregir estructura del programa",
                "Validar formato"
            ]
        }
        
        # Configurar respuestas del codificador
        codigo_con_error = """IDENTIFICATION DIVISION.
PROGRAM-ID. HOLA.
PROCEDURE DIVISION.
DISPLAY 'HOLA MUNDO'
STOP RUN."""
        
        codigo_corregido = """IDENTIFICATION DIVISION.
PROGRAM-ID. HOLA.
PROCEDURE DIVISION.
DISPLAY 'HOLA MUNDO'.
STOP RUN."""
        
        # Configurar respuestas secuenciales de los nodos
        mock_planner_node.side_effect = [
            {"plan": plan_inicial},      # Primera llamada: plan inicial
            {"plan": plan_correccion}    # Segunda llamada: plan de corrección
        ]
        
        mock_coder_node.side_effect = [
            {"code": codigo_con_error},  # Primera llamada: código con error
            {"code": codigo_corregido}   # Segunda llamada: código corregido
        ]
        
        mock_validator_node.side_effect = [
            {"error_message": "SYNTAX ERROR: Missing period after DISPLAY", "retry_count": 1},  # Error
            {"error_message": None, "retry_count": 1}  # Éxito
        ]
        
        # Ejecutar el grafo
        graph = get_compiled_graph()
        
        # Estado inicial
        initial_state = {
            "request": "Crear un programa que muestre 'HOLA MUNDO'",
            "plan": None,
            "code": None,
            "error_message": None,
            "retry_count": 0
        }
        
        # Invocar el grafo
        result = graph.invoke(initial_state)
        
        # Verificaciones
        assert result["code"] == codigo_corregido
        assert result["retry_count"] == 1  # Una corrección
        assert "error_message" not in result or result["error_message"] is None
        
        # Verificar que los componentes fueron llamados el número correcto de veces
        assert mock_planner_node.call_count == 2  # Plan inicial + corrección
        assert mock_coder_node.call_count == 2    # Código inicial + corregido
        assert mock_validator_node.call_count == 2                # Validación inicial + final

    def test_graph_handles_successful_first_attempt(self, mocker):
        """
        Test que verifica el flujo cuando el código es correcto en el primer intento.
        """
        from core.graph import get_compiled_graph
        
        # Configurar mocks directamente en los nodos del grafo
        mock_planner_node = mocker.patch('core.graph.planner_node')
        mock_coder_node = mocker.patch('core.graph.coder_node')
        mock_validator_node = mocker.patch('core.graph.validator_node')
        
        # Plan inicial
        plan = {
            "plan": "Generar programa HOLA MUNDO simple",
            "mode": "creation",
            "steps": ["Crear estructura básica", "Implementar lógica"]
        }
        
        # Código correcto desde el inicio
        codigo_correcto = """IDENTIFICATION DIVISION.
PROGRAM-ID. HOLA.
PROCEDURE DIVISION.
DISPLAY 'HOLA MUNDO'.
STOP RUN."""
        
        # Configurar respuestas de los nodos
        mock_planner_node.return_value = {"plan": plan}
        mock_coder_node.return_value = {"code": codigo_correcto}
        mock_validator_node.return_value = {"error_message": None, "retry_count": 0}
        
        # Ejecutar
        graph = get_compiled_graph()
        initial_state = {
            "request": "Crear programa HOLA MUNDO",
            "plan": None,
            "code": None,
            "error_message": None,
            "retry_count": 0
        }
        
        result = graph.invoke(initial_state)
        
        # Verificaciones
        assert result["code"] == codigo_correcto
        assert result["retry_count"] == 0  # Sin correcciones
        assert mock_planner_node.call_count == 1  # Solo plan inicial
        assert mock_coder_node.call_count == 1    # Solo código inicial
        assert mock_validator_node.call_count == 1                # Solo una validación

    def test_graph_handles_max_retries(self, mocker):
        """
        Test que verifica el comportamiento cuando se alcanza el máximo de reintentos.
        """
        from core.graph import get_compiled_graph
        
        # Configurar mocks directamente en los nodos del grafo
        mock_planner_node = mocker.patch('core.graph.planner_node')
        mock_coder_node = mocker.patch('core.graph.coder_node')
        mock_validator_node = mocker.patch('core.graph.validator_node')
        
        # Plan que siempre se genera
        plan = {
            "plan": "Intentar corregir código",
            "mode": "correction",
            "steps": ["Analizar error", "Corregir"]
        }
        
        # Código que siempre tiene error
        codigo_con_error = "INVALID COBOL CODE"
        
        # Configurar respuestas de los nodos
        mock_planner_node.return_value = {"plan": plan}
        mock_coder_node.return_value = {"code": codigo_con_error}
        # Validador que siempre falla, incrementando retry_count
        mock_validator_node.side_effect = [
            {"error_message": "Código COBOL inválido", "retry_count": 1},
            {"error_message": "Código COBOL inválido", "retry_count": 2},
            {"error_message": "Código COBOL inválido", "retry_count": 3}
        ]
        
        # Ejecutar
        graph = get_compiled_graph()
        initial_state = {
            "request": "Crear código COBOL",
            "plan": None,
            "code": None,
            "error_message": None,
            "retry_count": 0
        }
        
        result = graph.invoke(initial_state)
        
        # Verificaciones - debe detenerse después del máximo de reintentos
        assert result["retry_count"] >= 2  # Al menos 2 reintentos
        assert result["code"] == codigo_con_error  # Último código generado
        # El sistema debe terminar aunque haya errores


class TestIntegrationFlowEdgeCases:
    """Pruebas de casos extremos en la integración."""

    def test_graph_handles_empty_request(self, mocker):
        """Test que verifica el manejo de solicitudes vacías."""
        from core.graph import get_compiled_graph
        
        # Configurar mocks directamente en los nodos del grafo
        mock_planner_node = mocker.patch('core.graph.planner_node')
        mock_coder_node = mocker.patch('core.graph.coder_node')
        mock_validator_node = mocker.patch('core.graph.validator_node')
        
        # Plan para solicitud vacía
        plan_vacio = {
            "plan": "Generar programa COBOL básico por defecto",
            "mode": "creation",
            "steps": ["Crear estructura mínima"]
        }
        
        # Configurar respuestas de los nodos
        mock_planner_node.return_value = {"plan": plan_vacio}
        mock_coder_node.return_value = {"code": "BASIC COBOL CODE"}
        mock_validator_node.return_value = {"error_message": None, "retry_count": 0}
        
        graph = get_compiled_graph()
        initial_state = {
            "request": "",
            "plan": None,
            "code": None,
            "error_message": None,
            "retry_count": 0
        }
        
        # No debe fallar con solicitud vacía
        result = graph.invoke(initial_state)
        assert result is not None
        assert mock_planner_node.call_count >= 1

    def test_graph_state_consistency(self, mocker):
        """Test que verifica la consistencia del estado a través del flujo."""
        from core.graph import get_compiled_graph
        
        # Configurar mocks directamente en los nodos del grafo
        mock_planner_node = mocker.patch('core.graph.planner_node')
        mock_coder_node = mocker.patch('core.graph.coder_node')
        mock_validator_node = mocker.patch('core.graph.validator_node')
        
        plan = {"plan": "Test plan", "mode": "creation", "steps": ["Step 1"]}
        codigo = "TEST CODE"
        
        # Configurar respuestas de los nodos
        mock_planner_node.return_value = {"plan": plan}
        mock_coder_node.return_value = {"code": codigo}
        mock_validator_node.return_value = {"error_message": None, "retry_count": 0}
        
        graph = get_compiled_graph()
        initial_state = {
            "request": "Test request",
            "plan": None,
            "code": None,
            "error_message": None,
            "retry_count": 0
        }
        
        result = graph.invoke(initial_state)
        
        # Verificar que el estado mantiene consistencia
        assert result["request"] == "Test request"  # Request original preservado
        assert result["plan"] == plan               # Plan asignado
        assert result["code"] == codigo             # Código asignado
        assert isinstance(result["retry_count"], int)  # Contador es entero