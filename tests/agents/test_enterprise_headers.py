"""
Tests específicos para validar cabeceras empresariales COBOL.

Este módulo contiene tests dedicados a verificar que el agente codificador
genera cabeceras empresariales correctas según los estándares del cliente.
"""

from datetime import datetime

import pytest

from agents.coder import (
    _extract_objectives_from_request,
    _generate_enterprise_header,
    _get_current_date_formatted,
    _infer_subsystem_from_program,
    _infer_system_from_request,
    get_coder_chain,
)


class TestEnterpriseHeaders:
    """Tests para validar cabeceras empresariales COBOL."""

    def test_current_date_formatting(self):
        """Test que verifica el formato correcto de fecha actual."""
        # Act
        formatted_date = _get_current_date_formatted()

        # Assert
        assert formatted_date is not None, "La fecha no debe ser None"
        assert isinstance(formatted_date, str), "La fecha debe ser un string"
        assert len(formatted_date) == 10, "La fecha debe tener formato DD/MM/YYYY"
        assert formatted_date.count("/") == 2, "La fecha debe contener dos barras"

        # Verificar que es una fecha válida
        try:
            datetime.strptime(formatted_date, "%d/%m/%Y")
        except ValueError:
            pytest.fail(f"Formato de fecha inválido: {formatted_date}")

    def test_system_inference_from_request(self):
        """Test que verifica la inferencia de sistema desde la solicitud."""
        # Test cases
        test_cases = [
            ("programa bancario", "BANCARIO"),
            ("sistema de clientes", "CLIENTES"),
            ("reportes financieros", "FINANCIERO"),
            ("gestión de cuentas", "CUENTAS"),
            ("programa de nómina", "NOMINA"),
            ("sistema general", "GENERAL"),
        ]

        for request, expected_system in test_cases:
            # Act
            result = _infer_system_from_request(request)

            # Assert
            assert result == expected_system, "Sistema inferido incorrecto"

    def test_subsystem_inference_from_program(self):
        """Verifica inferencia de subsistema desde nombre de programa."""
        # Test cases
        test_cases = [
            ("SUPPGPR1", "SUPP"),
            ("BANCPGR2", "BANC"),
            ("CLNTPGR3", "CLNT"),
            ("FINPGR01", "FIN"),
            ("PROG001", "PROG"),
        ]

        for program_name, expected_subsystem in test_cases:
            # Act
            result = _infer_subsystem_from_program(program_name)

            # Assert
            assert result == expected_subsystem, "Subsistema inferido incorrecto"

    def test_objectives_extraction_from_request(self):
        """Test que verifica la extracción de objetivos desde la solicitud."""
        # Test cases
        test_cases = [
            ("Crear programa que muestre HOLA MUNDO", "MOSTRAR MENSAJE HOLA MUNDO"),
            (
                "Procesar archivos de clientes bancarios",
                "PROCESAR ARCHIVOS CLIENTES BANCARIOS",
            ),
            ("Generar reportes de segmentación", "GENERAR REPORTES SEGMENTACION"),
            ("Validar datos de entrada", "VALIDAR DATOS ENTRADA"),
        ]

        for request, expected_objective in test_cases:
            # Act
            result = _extract_objectives_from_request(request)

            # Assert
            assert (
                expected_objective in result
            ), f"Para '{request}' esperaba que contuviera '{expected_objective}'"
            assert len(result) <= 50, "Los objetivos no deben exceder 50 caracteres"

    def test_enterprise_header_generation(self):
        """Test que verifica la generación completa de cabeceras empresariales."""
        # Arrange
        test_data = {
            "program_name": "SUPPGPR1",
            "current_date": "15/12/2024",
            "system": "BANCARIO",
            "subsystem": "SUPP",
            "objectives": "PROCESAR ARCHIVOS CLIENTES",
        }

        # Act
        header = _generate_enterprise_header(**test_data)

        # Assert
        assert header is not None, "La cabecera no debe ser None"
        assert isinstance(header, str), "La cabecera debe ser un string"

        # Verificar elementos obligatorios
        assert "IDENTIFICATION DIVISION." in header
        assert "PROGRAM-ID.    SUPPGPR1." in header
        assert "AUTHOR.        SISTEMA GENERADOR COBOL IA." in header
        assert "DATE-WRITTEN.  15/12/2024." in header
        assert "SISTEMA   : BANCARIO" in header
        assert "SUBSISTEMA: SUPP" in header
        assert "OBJETIVOS : PROCESAR ARCHIVOS CLIENTES" in header
        assert "M A N T E N C I O N E S" in header
        assert "COBOL-IA" in header

    def test_enterprise_header_in_generated_code(self):
        """Test de integración: valida cabeceras en código generado."""
        # Arrange
        test_plan = {
            "plan": (
                "Crear un programa COBOL bancario llamado SUPPGPR1 "
                "que procese archivos de clientes"
            )
        }

        # Act
        coder_chain = get_coder_chain()
        result = coder_chain.invoke(test_plan)

        # Assert
        assert result is not None, "El código generado no debe ser None"

        # Verificar estructura de cabecera empresarial
        assert "IDENTIFICATION DIVISION." in result
        assert "PROGRAM-ID." in result
        assert "AUTHOR.        SISTEMA GENERADOR COBOL IA." in result
        assert "DATE-WRITTEN." in result

        # Verificar información del sistema
        assert "SISTEMA   :" in result
        assert "SUBSISTEMA:" in result
        assert "OBJETIVOS :" in result

        # Verificar sección de mantenciones
        assert "M A N T E N C I O N E S" in result
        assert "COBOL-IA" in result

        # Verificar que la fecha es actual
        current_date = _get_current_date_formatted()
        assert current_date in result, "Debe contener la fecha actual"

    def test_different_program_types_generate_appropriate_headers(self):
        """Verifica que distintos programas generan cabeceras apropiadas."""
        test_cases = [
            {
                "plan": "Crear programa de nómina NOMPGR01",
                "expected_system": "NOMINA",
                "expected_subsystem": "NOM",
            },
            {
                "plan": "Crear programa financiero FINPGR02",
                "expected_system": "FINANCIERO",
                "expected_subsystem": "FIN",
            },
            {
                "plan": "Crear programa de clientes CLNTPGR1",
                "expected_system": "CLIENTES",
                "expected_subsystem": "CLNT",
            },
        ]

        coder_chain = get_coder_chain()

        for test_case in test_cases:
            # Act
            result = coder_chain.invoke({"plan": test_case["plan"]})

            # Assert
            assert test_case["expected_system"] in result, "Debe contener sistema"
            assert test_case["expected_subsystem"] in result, "Debe contener subsistema"

    def test_header_format_compliance(self):
        """Verifica cumplimiento del formato de cabeceras del cliente."""
        # Arrange
        test_plan = {"plan": "Crear programa COBOL de ejemplo TESTPGR1"}

        # Act
        coder_chain = get_coder_chain()
        result = coder_chain.invoke(test_plan)

        # Assert - Verificar formato específico del cliente
        lines = result.split("\n")

        # Buscar líneas específicas del formato
        identification_found = False
        author_found = False
        date_written_found = False
        system_info_found = False
        maintenance_section_found = False

        for line in lines:
            if "IDENTIFICATION DIVISION." in line:
                identification_found = True
            elif "AUTHOR.        SISTEMA GENERADOR COBOL IA." in line:
                author_found = True
            elif "DATE-WRITTEN." in line and "/" in line:
                date_written_found = True
            elif "SISTEMA   :" in line:
                system_info_found = True
            elif "M A N T E N C I O N E S" in line:
                maintenance_section_found = True

        assert identification_found, "Debe contener IDENTIFICATION DIVISION"
        assert author_found, "Debe contener AUTHOR con formato correcto"
        assert date_written_found, "Debe contener DATE-WRITTEN con fecha"
        assert system_info_found, "Debe contener información del sistema"
        assert maintenance_section_found, "Debe contener sección de mantenciones"
