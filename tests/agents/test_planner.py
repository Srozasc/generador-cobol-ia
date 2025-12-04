"""
Tests para el Agente Planificador.

Este módulo contiene las pruebas unitarias para el agente planificador
que convierte solicitudes en lenguaje natural a planes técnicos estructurados.

Siguiendo TDD, estos tests se escriben ANTES de implementar el agente.
"""

import json

# Importación del módulo implementado
from agents.planner import get_planner_chain


class TestPlannerAgent:
    """
    Tests principales para el Agente Planificador.
    """

    def test_creates_plan_from_simple_request(self):
        """
        Test que verifica la creación de un plan desde una solicitud simple.
        """
        # Arrange: Solicitud simple
        request_data = {"request": "Crear un programa COBOL que muestre 'HOLA MUNDO'"}

        # Act: Generar plan
        chain = get_planner_chain()
        result = chain.invoke(request_data)

        # Assert: Debe retornar un plan válido
        assert result is not None
        assert isinstance(result, dict)
        assert "plan" in result
        assert "steps" in result
        assert isinstance(result["steps"], list)
        assert len(result["steps"]) > 0

    def test_creates_correction_plan_from_error(self):
        """
        Test que verifica la creación de un plan de corrección desde un error.
        """
        # Arrange: Datos de corrección
        correction_data = {
            "request": "Corregir error de sintaxis",
            "code": (
                "IDENTIFICATION DIVISION.\n"
                "PROGRAM-ID. TEST.\n"
                "PROCEDURE DIVISION.\n"
                "DISPLAY 'ERROR'.\n"
                "STOP RUN"
            ),
            "error_message": "Missing DATA DIVISION",
        }

        # Act: Generar plan de corrección
        chain = get_planner_chain()
        result = chain.invoke(correction_data)

        # Assert: Debe retornar un plan de corrección válido
        assert result is not None
        assert isinstance(result, dict)
        assert "plan" in result
        assert "steps" in result
        assert "mode" in result
        assert result["mode"] == "correction"

    def test_handles_complex_request(self):
        """
        Test que verifica el manejo de solicitudes complejas.
        """
        # Arrange: Solicitud compleja
        complex_request = {
            "request": (
                "Crear un programa COBOL para procesar archivos de empleados "
                "con validaciones de datos, cálculos de nómina y reportes"
            )
        }

        # Act: Generar plan
        chain = get_planner_chain()
        result = chain.invoke(complex_request)

        # Assert: Debe manejar la complejidad
        assert result is not None
        assert isinstance(result, dict)
        assert "plan" in result
        assert "steps" in result
        assert (
            len(result["steps"]) >= 3
        )  # Solicitud compleja debe tener múltiples pasos

    def test_validates_json_output_format(self):
        """
        Test que verifica que la salida sea JSON válido.
        """
        # Arrange: Solicitud estándar
        request_data = {"request": "Crear programa de validación de datos"}

        # Act: Generar plan
        chain = get_planner_chain()
        result = chain.invoke(request_data)

        # Assert: Debe ser JSON válido
        assert result is not None
        assert isinstance(result, dict)
        # Verificar que se puede serializar a JSON
        json_str = json.dumps(result)
        assert json_str is not None
        # Verificar que se puede deserializar
        parsed = json.loads(json_str)
        assert parsed == result

    def test_handles_empty_request(self):
        """
        Test que verifica el manejo de solicitudes vacías.
        """
        # Arrange: Solicitud vacía
        empty_request = {"request": ""}

        # Act: Generar plan
        chain = get_planner_chain()
        result = chain.invoke(empty_request)

        # Assert: Debe manejar graciosamente
        assert result is not None
        assert isinstance(result, dict)
        assert "plan" in result or "error" in result


class TestPlannerModes:
    """
    Tests para los diferentes modos del planificador.
    """

    def test_creation_mode_structure(self):
        """
        Test que verifica la estructura del modo creación.
        """
        # Arrange: Solicitud de creación
        creation_request = {"request": "Crear programa de cálculo de intereses"}

        # Act: Generar plan
        chain = get_planner_chain()
        result = chain.invoke(creation_request)

        # Assert: Estructura de modo creación
        assert result is not None
        assert result["mode"] == "creation"
        assert "plan" in result
        assert "steps" in result
        assert isinstance(result["steps"], list)

    def test_correction_mode_structure(self):
        """
        Test que verifica la estructura del modo corrección.
        """
        # Arrange: Datos de corrección
        correction_data = {
            "request": "Corregir programa",
            "code": "PROGRAM-ID. TEST.",
            "error_message": "Syntax error",
        }

        # Act: Generar plan
        chain = get_planner_chain()
        result = chain.invoke(correction_data)

        # Assert: Estructura de modo corrección
        assert result is not None
        assert result["mode"] == "correction"
        assert "plan" in result
        assert "steps" in result
        assert "correction_type" in result
        assert "original_error" in result

    def test_mode_detection_logic(self):
        """
        Test que verifica la lógica de detección de modos.
        """
        # Arrange & Act: Probar ambos modos
        chain = get_planner_chain()

        # Modo creación (solo request)
        creation_result = chain.invoke({"request": "Crear programa nuevo"})

        # Modo corrección (request + code + error)
        correction_result = chain.invoke(
            {
                "request": "Corregir error",
                "code": "PROGRAM-ID. TEST.",
                "error_message": "Error de sintaxis",
            }
        )

        # Assert: Detección correcta de modos
        assert creation_result["mode"] == "creation"
        assert correction_result["mode"] == "correction"


class TestPlannerConfiguration:
    """
    Tests para la configuración del planificador.
    """

    def test_uses_correct_llm_configuration(self):
        """
        Test que verifica la configuración correcta del LLM.
        """
        # Act: Obtener la cadena
        chain = get_planner_chain()

        # Assert: Verificar que la cadena existe y es del tipo correcto
        assert chain is not None
        assert hasattr(chain, "invoke")

    def test_uses_json_output_parser(self):
        """
        Test que verifica el uso del JsonOutputParser.
        """
        # Act: Generar plan y verificar formato
        chain = get_planner_chain()
        result = chain.invoke({"request": "Test parser"})

        # Assert: Debe ser JSON válido (dict)
        assert isinstance(result, dict)

    def test_chain_structure(self):
        """
        Test que verifica la estructura de la cadena de LangChain.
        """
        # Act: Obtener cadena
        chain = get_planner_chain()

        # Assert: Verificar que es una cadena ejecutable
        assert chain is not None
        assert callable(getattr(chain, "invoke", None))


class TestPlannerEdgeCases:
    """
    Tests para casos extremos del planificador.
    """

    def test_handles_very_long_request(self):
        """
        Test que verifica el manejo de solicitudes muy largas.
        """
        # Arrange: Solicitud muy larga
        long_request = {
            "request": (
                "Crear un sistema complejo de gestión empresarial en COBOL que incluya "
                "módulos de contabilidad, recursos humanos, inventario, "
                "ventas, compras, reportes financieros, auditoría, "
                "control de acceso, integración externa, validación de datos "
                "en tiempo real, procesamiento por lotes, UI, logs, "
                "manejo de errores, optimización de performance, escalabilidad, "
                "compatibilidad con mainframes "
                "legacy, migración de datos, testing automatizado, "
                "CI/CD, monitoreo de sistema "
                "y alertas automáticas"
            )
        }

        # Act: Generar plan
        chain = get_planner_chain()
        result = chain.invoke(long_request)

        # Assert: Debe manejar solicitudes largas
        assert result is not None
        assert isinstance(result, dict)
        assert "plan" in result or "error" in result

    def test_handles_special_characters_in_request(self):
        """
        Test que verifica el manejo de caracteres especiales.
        """
        # Arrange: Solicitud con caracteres especiales
        special_request = {
            "request": (
                "Crear programa con símbolos: "
                "@#$%^&*()[]{}|\\:;\"'<>"
                ",.?/~`±§¿¡€£¥₹₽₩₪₫₱₡₵₦₨"
                "₹₽₩₪₫₱₡₵₦₨"
            )
        }

        # Act: Generar plan
        chain = get_planner_chain()
        result = chain.invoke(special_request)

        # Assert: Debe manejar caracteres especiales
        assert result is not None
        assert isinstance(result, dict)
        assert "plan" in result or "error" in result

    def test_consistent_output_format(self):
        """
        Test que verifica la consistencia del formato de salida.
        """
        # Arrange: Múltiples solicitudes
        requests = [
            {"request": "Programa simple"},
            {"request": "Programa complejo con múltiples módulos"},
            {
                "request": "Corrección de errores",
                "code": "TEST",
                "error_message": "Error",
            },
        ]

        # Act & Assert: Verificar consistencia
        chain = get_planner_chain()
        for req in requests:
            result = chain.invoke(req)
            assert result is not None
            assert isinstance(result, dict)
            assert "plan" in result or "error" in result
            if "plan" in result:
                assert "mode" in result
                assert "steps" in result
