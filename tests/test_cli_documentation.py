"""
Tests para la interfaz CLI del Agente de Documentación.

Este módulo contiene las pruebas para las funciones de interfaz de usuario
que permiten al usuario seleccionar el modo de operación y cargar archivos COBOL.

Siguiendo TDD, estos tests se escriben ANTES de implementar las funciones.
"""

import os
import tempfile
from unittest.mock import MagicMock, patch

import pytest

from run_prototype import (
    display_documentation,
    get_file_path,
    load_cobol_file,
    run_documentation_process,
    select_mode,
)


class TestSelectMode:
    """
    Tests para la función select_mode().
    """

    @patch("builtins.input", return_value="1")
    def test_select_mode_returns_1_for_generation(self, mock_input):
        """
        Test que verifica que select_mode retorna '1' para generación.
        """
        # Act
        result = select_mode()

        # Assert
        assert result == "1"

    @patch("builtins.input", return_value="2")
    def test_select_mode_returns_2_for_documentation(self, mock_input):
        """
        Test que verifica que select_mode retorna '2' para documentación.
        """
        # Act
        result = select_mode()

        # Assert
        assert result == "2"

    @patch("builtins.input", side_effect=["invalid", "4", "1"])
    def test_select_mode_validates_input(self, mock_input):
        """
        Test que verifica que select_mode valida la entrada del usuario.
        """
        # Act
        result = select_mode()

        # Assert: Debe haber solicitado input 3 veces
        assert mock_input.call_count == 3
        assert result == "1"

    @patch("builtins.input", return_value="1")
    def test_select_mode_is_callable(self, mock_input):
        """
        Test que verifica que select_mode es una función callable.
        """
        # Assert
        assert callable(select_mode)


class TestGetFilePath:
    """
    Tests para la función get_file_path().
    """

    def test_get_file_path_accepts_existing_file(self):
        """
        Test que verifica que get_file_path acepta archivos existentes.
        """
        # Arrange: Crear archivo temporal
        with tempfile.NamedTemporaryFile(mode="w", suffix=".cbl", delete=False) as f:
            temp_path = f.name
            f.write("PROGRAM-ID. TEST.")

        try:
            # Act: Simular input del usuario
            with patch("builtins.input", return_value=temp_path):
                result = get_file_path()

            # Assert
            assert result == temp_path
        finally:
            # Cleanup
            os.unlink(temp_path)

    def test_get_file_path_rejects_nonexistent_file(self):
        """
        Test que verifica que get_file_path rechaza archivos inexistentes.
        """
        # Arrange: Ruta que no existe
        nonexistent_path = "C:\\nonexistent\\file.cbl"

        # Act & Assert: Simular input del usuario que rechaza reintentar
        with patch("builtins.input", side_effect=[nonexistent_path, "n"]):
            with pytest.raises(SystemExit):
                get_file_path()

    def test_get_file_path_allows_retry(self):
        """
        Test que verifica que get_file_path permite reintentar.
        """
        # Arrange: Crear archivo temporal
        with tempfile.NamedTemporaryFile(mode="w", suffix=".cbl", delete=False) as f:
            temp_path = f.name
            f.write("TEST")

        try:
            # Act: Simular input con reintento
            with patch(
                "builtins.input",
                side_effect=["nonexistent.cbl", "s", temp_path],
            ):
                result = get_file_path()

            # Assert
            assert result == temp_path
        finally:
            # Cleanup
            os.unlink(temp_path)

    def test_get_file_path_is_callable(self):
        """
        Test que verifica que get_file_path es callable.
        """
        # Assert
        assert callable(get_file_path)


class TestLoadCobolFile:
    """
    Tests para la función load_cobol_file().
    """

    def test_load_cobol_file_reads_file_content(self):
        """
        Test que verifica que load_cobol_file lee el contenido del archivo.
        """
        # Arrange: Crear archivo temporal con contenido COBOL
        cobol_content = """
       IDENTIFICATION DIVISION.
       PROGRAM-ID. TESTPROG.
       PROCEDURE DIVISION.
           STOP RUN.
        """
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".cbl", delete=False, encoding="latin-1"
        ) as f:
            temp_path = f.name
            f.write(cobol_content)

        try:
            # Act
            result = load_cobol_file(temp_path)

            # Assert
            assert result is not None
            assert "TESTPROG" in result
            assert "IDENTIFICATION DIVISION" in result
        finally:
            # Cleanup
            os.unlink(temp_path)

    def test_load_cobol_file_handles_latin1_encoding(self):
        """
        Test que verifica que load_cobol_file maneja encoding latin-1.
        """
        # Arrange: Crear archivo con caracteres especiales
        cobol_content = (
            "IDENTIFICATION DIVISION.\nPROGRAM-ID. TËST."  # Caracteres con tilde
        )
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".cbl", delete=False, encoding="latin-1"
        ) as f:
            temp_path = f.name
            f.write(cobol_content)

        try:
            # Act
            result = load_cobol_file(temp_path)

            # Assert
            assert result is not None
            assert "TËST" in result or "TEST" in result  # Puede normalizar
        finally:
            # Cleanup
            os.unlink(temp_path)

    def test_load_cobol_file_validates_cobol_structure(self):
        """
        Test que verifica que load_cobol_file valida estructura COBOL básica.
        """
        # Arrange: Crear archivo sin IDENTIFICATION DIVISION
        invalid_content = "This is not COBOL"
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".cbl", delete=False, encoding="latin-1"
        ) as f:
            temp_path = f.name
            f.write(invalid_content)

        try:
            # Act & Assert: Debe lanzar excepción o advertencia
            with pytest.raises(ValueError):
                load_cobol_file(temp_path)
        finally:
            # Cleanup
            os.unlink(temp_path)

    def test_load_cobol_file_handles_nonexistent_file(self):
        """
        Test que verifica que load_cobol_file maneja archivos inexistentes.
        """
        # Arrange: Ruta que no existe
        nonexistent_path = "C:\\nonexistent\\file.cbl"

        # Act & Assert
        with pytest.raises(FileNotFoundError):
            load_cobol_file(nonexistent_path)

    def test_load_cobol_file_is_callable(self):
        """
        Test que verifica que load_cobol_file es callable.
        """
        # Assert
        assert callable(load_cobol_file)


class TestDisplayDocumentation:
    """
    Tests para la función display_documentation().
    """

    @patch("builtins.input", return_value="n")
    @patch("builtins.print")
    def test_display_documentation_shows_markdown(self, mock_print, mock_input):
        """
        Test que verifica que display_documentation muestra Markdown.
        """
        # Arrange: Resultado con documentación
        result = {
            "documentation": "# Test Documentation\n\n## Section 1\n\nContent here.",
            "mode": "documentation",
            "error_message": "",
        }

        # Act
        display_documentation(result)

        # Assert: Debe haber llamado a print
        assert mock_print.called
        # Verificar que se imprimió el contenido
        calls = [str(call) for call in mock_print.call_args_list]
        assert any("Test Documentation" in str(call) for call in calls)

    @patch("builtins.print")
    def test_display_documentation_handles_errors(self, mock_print):
        """
        Test que verifica que display_documentation maneja errores.
        """
        # Arrange: Resultado con error
        result = {
            "documentation": "",
            "mode": "documentation",
            "error_message": "Error al generar documentación",
        }

        # Act
        display_documentation(result)

        # Assert: Debe mostrar el error
        assert mock_print.called
        calls = [str(call) for call in mock_print.call_args_list]
        assert any("error" in str(call).lower() for call in calls)

    @patch("builtins.input", return_value="n")
    @patch("builtins.print")
    def test_display_documentation_offers_save_option(self, mock_print, mock_input):
        """
        Test que verifica que display_documentation ofrece guardar.
        """
        # Arrange
        result = {
            "documentation": "# Test\n\nContent",
            "mode": "documentation",
            "error_message": "",
        }

        # Act
        display_documentation(result)

        # Assert: Debe haber preguntado si guardar
        assert mock_input.called

    def test_display_documentation_is_callable(self):
        """
        Test que verifica que display_documentation es callable.
        """
        # Assert
        assert callable(display_documentation)


class TestRunDocumentationProcess:
    """
    Tests para verificar que run_documentation_process está disponible.
    """

    def test_run_documentation_process_is_imported(self):
        """
        Test que verifica que run_documentation_process está importado.
        """
        # Assert
        assert run_documentation_process is not None
        assert callable(run_documentation_process)


class TestCLIIntegration:
    """
    Tests de integración para el flujo CLI completo.
    """

    @patch("builtins.input", return_value="2")
    @patch("builtins.print")
    def test_mode_selection_flow(self, mock_print, mock_input):
        """
        Test de integración para selección de modo.
        """
        # Act
        mode = select_mode()

        # Assert
        assert mode == "2"
        assert mock_print.called  # Debe mostrar el menú

    def test_file_loading_and_documentation_flow(self):
        """
        Test de integración para carga de archivo y documentación.
        """
        # Arrange: Crear archivo COBOL temporal
        cobol_content = """
       IDENTIFICATION DIVISION.
       PROGRAM-ID. INTEGTEST.
       PROCEDURE DIVISION.
           STOP RUN.
        """
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".cbl", delete=False, encoding="latin-1"
        ) as f:
            temp_path = f.name
            f.write(cobol_content)

        try:
            # Act: Cargar archivo
            code = load_cobol_file(temp_path)

            # Assert: Código cargado correctamente
            assert "INTEGTEST" in code

            # Act: Generar documentación
            result = run_documentation_process(code)

            # Assert: Documentación generada
            assert "documentation" in result
            assert "INTEGTEST" in result["documentation"]
        finally:
            # Cleanup
            os.unlink(temp_path)
