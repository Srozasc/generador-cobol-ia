"""
Tests para la integración del Modo Modificación en el CLI.

Verifica las funciones del CLI relacionadas con la modificación de programas COBOL.
"""

import sys
from io import StringIO
from unittest.mock import MagicMock, mock_open, patch

import pytest

from run_prototype import main, run_modification_process, select_mode


class TestCLIModification:
    """Tests para las funciones del CLI de modificación."""

    def test_select_mode_includes_modification_option(self):
        """Verifica que select_mode incluye la opción 3."""
        with (
            patch("builtins.input", return_value="3"),
            patch("sys.stdout", new=StringIO()) as fake_out,
        ):

            mode = select_mode()

            output = fake_out.getvalue()
            assert "3. Modificar programa existente" in output
            assert mode == "3"

    @patch("core.graph.get_compiled_graph")
    def test_run_modification_process_success(self, mock_get_graph):
        """Verifica la ejecución exitosa del proceso de modificación."""
        # Arrange
        mock_graph = MagicMock()
        mock_get_graph.return_value = mock_graph

        mock_result = {
            "plan": {"mode": "modification", "steps": ["step1"]},
            "code": "MODIFIED COBOL CODE",
            "mode": "modification",
        }
        mock_graph.invoke.return_value = mock_result

        original_code = "ORIGINAL COBOL CODE"
        request = "Change something"

        # Act
        with patch("sys.stdout", new=StringIO()) as fake_out:
            result = run_modification_process(original_code, request)

        # Assert
        assert result == mock_result
        mock_graph.invoke.assert_called_once()
        call_args = mock_graph.invoke.call_args[0][0]
        assert call_args["request"] == request
        assert call_args["code"] == original_code
        assert call_args["mode"] == "modification"

    @patch("run_prototype.validate_environment", return_value=True)
    @patch("run_prototype.select_mode", return_value="3")
    @patch("run_prototype.get_file_path", return_value="test.cbl")
    @patch("run_prototype.load_cobol_file", return_value="COBOL CODE")
    @patch("run_prototype.get_user_request", return_value="Modify logic")
    @patch("run_prototype.run_modification_process")
    @patch("run_prototype.display_results")
    def test_main_flow_modification(
        self,
        mock_display,
        mock_run,
        mock_request,
        mock_load,
        mock_path,
        mock_select,
        mock_validate,
    ):
        """Verifica el flujo principal para la opción de modificación."""
        # Arrange
        mock_run.return_value = {"code": "NEW CODE"}

        # Act
        with patch("sys.stdout", new=StringIO()):
            main()

        # Assert
        mock_select.assert_called_once()
        mock_path.assert_called_once()
        mock_load.assert_called_once_with("test.cbl")
        mock_request.assert_called_once()
        mock_run.assert_called_once_with("COBOL CODE", "Modify logic")
        mock_display.assert_called_once()
