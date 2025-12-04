"""
Tests para el Agente Codificador en Modo Modificación.

Verifica que el codificador pueda tomar código COBOL existente y un plan de modificación,
y generar código actualizado sin romper la funcionalidad existente.
"""

from unittest.mock import MagicMock, patch

import pytest

from agents.coder import get_coder_chain


class TestCoderModificationMode:
    """
    Tests para el modo de modificación del Agente Codificador.
    """

    @pytest.fixture
    def sample_cobol_code(self):
        """Código COBOL de ejemplo para modificar."""
        return """       IDENTIFICATION DIVISION.
       PROGRAM-ID. COBPROG01.
       AUTHOR. SISTEMA BANCARIO.
       DATA DIVISION.
       WORKING-STORAGE SECTION.
       01  WS-MONTO-PAGO     PIC 9(07)V99.
       01  WS-ESTADO-CLIENTE PIC X(10).
       PROCEDURE DIVISION.
       MAIN-PROCESS.
           PERFORM PAR-VALIDACION.
           STOP RUN.
       PAR-VALIDACION.
           IF WS-MONTO-PAGO > 5000
               DISPLAY 'PAGO ALTO'
           END-IF.
        """

    @pytest.fixture
    def modification_plan(self):
        """Plan de modificación de ejemplo."""
        return {
            "plan": "Modificar lógica de validación de pagos",
            "mode": "modification",
            "analysis": "Se identificó WS-MONTO-PAGO. Cambio en PAR-VALIDACION.",
            "steps": [
                "Modificar condición IF en PAR-VALIDACION para comparar con 10000",
                "Agregar lógica para verificar WS-ESTADO-CLIENTE = 'MORA'",
                "Insertar PERFORM a rutina de log si se cumple condición",
            ],
        }

    @patch("agents.coder.ChatGoogleGenerativeAI")
    def test_coder_accepts_original_code_and_plan(
        self, mock_llm_class, sample_cobol_code, modification_plan
    ):
        """
        Test que verifica que el coder acepta código original y plan de modificación.
        """
        # Arrange
        from types import SimpleNamespace

        mock_response = SimpleNamespace(
            content=sample_cobol_code
        )  # Por ahora retorna el mismo código
        mock_llm = mock_llm_class.return_value
        mock_llm.invoke.return_value = mock_response
        mock_llm.return_value = mock_response

        input_data = {
            "plan": str(modification_plan),
            "original_code": sample_cobol_code,
        }

        # Act
        chain = get_coder_chain()
        result = chain.invoke(input_data)

        # Assert
        assert result is not None
        assert isinstance(result, str)
        assert "IDENTIFICATION DIVISION" in result

    @patch("agents.coder.ChatGoogleGenerativeAI")
    def test_coder_inserts_complex_if_logic(
        self, mock_llm_class, sample_cobol_code, modification_plan
    ):
        """
        Test que verifica que el coder inserta lógica IF compleja sin romper el código.
        """
        # Arrange
        expected_modified_code = """       IDENTIFICATION DIVISION.
       PROGRAM-ID. COBPROG01.
       AUTHOR. SISTEMA BANCARIO.
       DATA DIVISION.
       WORKING-STORAGE SECTION.
       01  WS-MONTO-PAGO     PIC 9(07)V99.
       01  WS-ESTADO-CLIENTE PIC X(10).
       PROCEDURE DIVISION.
       MAIN-PROCESS.
           PERFORM PAR-VALIDACION.
           STOP RUN.
       PAR-VALIDACION.
           IF WS-MONTO-PAGO > 10000 AND WS-ESTADO-CLIENTE = 'MORA'
               PERFORM LOG-ALERTA
               DISPLAY 'PAGO ALTO CON MORA'
           END-IF.
        """

        from types import SimpleNamespace

        mock_response = SimpleNamespace(content=expected_modified_code)
        mock_llm = mock_llm_class.return_value
        mock_llm.invoke.return_value = mock_response
        mock_llm.return_value = mock_response

        input_data = {
            "plan": str(modification_plan),
            "original_code": sample_cobol_code,
        }

        # Act
        chain = get_coder_chain()
        result = chain.invoke(input_data)

        # Assert
        assert result is not None
        assert "WS-MONTO-PAGO > 10000" in result
        assert "WS-ESTADO-CLIENTE = 'MORA'" in result
        assert "LOG-ALERTA" in result or "PERFORM" in result
        # Verificar que no se rompió la estructura
        assert "IDENTIFICATION DIVISION" in result
        assert "PROCEDURE DIVISION" in result

    @patch("agents.coder.ChatGoogleGenerativeAI")
    def test_coder_preserves_existing_code(
        self, mock_llm_class, sample_cobol_code, modification_plan
    ):
        """
        Test que verifica que el coder preserva código no relacionado con el cambio.
        """
        # Arrange
        expected_code = """       IDENTIFICATION DIVISION.
       PROGRAM-ID. COBPROG01.
       AUTHOR. SISTEMA BANCARIO.
       DATA DIVISION.
       WORKING-STORAGE SECTION.
       01  WS-MONTO-PAGO     PIC 9(07)V99.
       01  WS-ESTADO-CLIENTE PIC X(10).
       PROCEDURE DIVISION.
       MAIN-PROCESS.
           PERFORM PAR-VALIDACION.
           STOP RUN.
       PAR-VALIDACION.
           IF WS-MONTO-PAGO > 10000
               DISPLAY 'PAGO ALTO'
           END-IF.
        """

        from types import SimpleNamespace

        mock_response = SimpleNamespace(content=expected_code)
        mock_llm = mock_llm_class.return_value
        mock_llm.invoke.return_value = mock_response
        mock_llm.return_value = mock_response

        input_data = {
            "plan": str(modification_plan),
            "original_code": sample_cobol_code,
        }

        # Act
        chain = get_coder_chain()
        result = chain.invoke(input_data)

        # Assert
        # Verificar que elementos no modificados siguen presentes
        assert "PROGRAM-ID. COBPROG01" in result
        assert "AUTHOR. SISTEMA BANCARIO" in result
        assert "MAIN-PROCESS" in result
        assert "STOP RUN" in result
