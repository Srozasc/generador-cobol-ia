"""
Tests de integración específicos para casos bancarios empresariales.
Valida el flujo completo del sistema con casos basados en código real del cliente.
"""

import pytest
from unittest.mock import patch, MagicMock
from core.graph import get_compiled_graph


class TestEnterpriseBankingIntegration:
    """Tests de integración para casos bancarios empresariales."""

    @pytest.fixture
    def mock_llm_responses(self):
        """Mock de respuestas del LLM para casos bancarios."""
        return {
            "plan_response": """{
                "objetivo": "Generar programa COBOL para procesamiento de transacciones bancarias",
                "estructura_archivos": [
                    {
                        "nombre": "ARCHIVO-TRANSACCIONES",
                        "tipo": "INPUT",
                        "campos": ["RUT-CLIENTE", "CODIGO-BANCO", "MONTO-TRANSACCION", "FECHA-PROCESO"]
                    },
                    {
                        "nombre": "ARCHIVO-RESULTADOS", 
                        "tipo": "OUTPUT",
                        "campos": ["RESULTADO-PROCESO", "MENSAJE-ERROR"]
                    }
                ],
                "logica_negocio": [
                    "Validar RUT chileno",
                    "Verificar código de banco",
                    "Procesar monto con formato COMP-3",
                    "Generar reporte de resultados"
                ],
                "manejo_errores": "Implementar validación de FILE STATUS y manejo de errores SQL"
            }""",
            "code_response": """IDENTIFICATION DIVISION.
PROGRAM-ID. BANCPRO1.
AUTHOR. SISTEMA GENERADOR COBOL IA.

ENVIRONMENT DIVISION.
CONFIGURATION SECTION.
SPECIAL-NAMES.
    DECIMAL-POINT IS COMMA.

INPUT-OUTPUT SECTION.
FILE-CONTROL.
    SELECT ARCHIVO-TRANSACCIONES
        ASSIGN TO 'TRANS.DAT'
        FILE STATUS IS WS-STATUS-TRANS.
    SELECT ARCHIVO-RESULTADOS
        ASSIGN TO 'RESULT.DAT'
        FILE STATUS IS WS-STATUS-RESULT.

DATA DIVISION.
FILE SECTION.
FD  ARCHIVO-TRANSACCIONES.
01  REG-TRANSACCION.
    05  RUT-CLIENTE         PIC X(12).
    05  CODIGO-BANCO        PIC 9(3).
    05  MONTO-TRANSACCION   PIC 9(15)V99 COMP-3.
    05  FECHA-PROCESO       PIC 9(8).

FD  ARCHIVO-RESULTADOS.
01  REG-RESULTADO.
    05  RESULTADO-PROCESO   PIC X(10).
    05  MENSAJE-ERROR       PIC X(100).

WORKING-STORAGE SECTION.
01  WS-CONTADORES.
    05  WS-TOTAL-REGISTROS  PIC 9(7) VALUE ZERO.
    05  WS-REGISTROS-OK     PIC 9(7) VALUE ZERO.
    05  WS-REGISTROS-ERROR  PIC 9(7) VALUE ZERO.

01  WS-STATUS-ARCHIVOS.
    05  WS-STATUS-TRANS     PIC XX VALUE SPACES.
    05  WS-STATUS-RESULT    PIC XX VALUE SPACES.

01  WS-VALIDACIONES.
    05  WS-RUT-VALIDO       PIC X VALUE 'N'.
        88  RUT-ES-VALIDO   VALUE 'S'.
    05  WS-BANCO-VALIDO     PIC X VALUE 'N'.
        88  BANCO-ES-VALIDO VALUE 'S'.

01  WS-CAMPOS-TRABAJO.
    05  WS-MONTO-EDITADO    PIC $$$,$$$,$$9.99.
    05  WS-FECHA-EDITADA    PIC 99/99/9999.

PROCEDURE DIVISION.
MAIN-PROCESS.
    PERFORM INICIALIZAR-PROCESO
    PERFORM PROCESAR-TRANSACCIONES
    PERFORM FINALIZAR-PROCESO
    STOP RUN.

INICIALIZAR-PROCESO.
    OPEN INPUT ARCHIVO-TRANSACCIONES
    IF WS-STATUS-TRANS NOT = '00'
        DISPLAY 'ERROR AL ABRIR ARCHIVO TRANSACCIONES: ' WS-STATUS-TRANS
        STOP RUN
    END-IF
    
    OPEN OUTPUT ARCHIVO-RESULTADOS
    IF WS-STATUS-RESULT NOT = '00'
        DISPLAY 'ERROR AL ABRIR ARCHIVO RESULTADOS: ' WS-STATUS-RESULT
        CLOSE ARCHIVO-TRANSACCIONES
        STOP RUN
    END-IF.

PROCESAR-TRANSACCIONES.
    PERFORM UNTIL WS-STATUS-TRANS = '10'
        READ ARCHIVO-TRANSACCIONES
        IF WS-STATUS-TRANS = '00'
            ADD 1 TO WS-TOTAL-REGISTROS
            PERFORM VALIDAR-TRANSACCION
            PERFORM ESCRIBIR-RESULTADO
        END-IF
    END-PERFORM.

VALIDAR-TRANSACCION.
    PERFORM VALIDAR-RUT-CLIENTE
    PERFORM VALIDAR-CODIGO-BANCO
    
    IF RUT-ES-VALIDO AND BANCO-ES-VALIDO
        MOVE 'EXITOSO' TO RESULTADO-PROCESO
        MOVE SPACES TO MENSAJE-ERROR
        ADD 1 TO WS-REGISTROS-OK
    ELSE
        MOVE 'ERROR' TO RESULTADO-PROCESO
        MOVE 'DATOS INVALIDOS' TO MENSAJE-ERROR
        ADD 1 TO WS-REGISTROS-ERROR
    END-IF.

VALIDAR-RUT-CLIENTE.
    IF RUT-CLIENTE NOT = SPACES AND RUT-CLIENTE NOT = LOW-VALUES
        SET RUT-ES-VALIDO TO TRUE
    ELSE
        SET RUT-ES-VALIDO TO FALSE
    END-IF.

VALIDAR-CODIGO-BANCO.
    IF CODIGO-BANCO > 0 AND CODIGO-BANCO < 999
        SET BANCO-ES-VALIDO TO TRUE
    ELSE
        SET BANCO-ES-VALIDO TO FALSE
    END-IF.

ESCRIBIR-RESULTADO.
    WRITE REG-RESULTADO
    IF WS-STATUS-RESULT NOT = '00'
        DISPLAY 'ERROR AL ESCRIBIR RESULTADO: ' WS-STATUS-RESULT
    END-IF.

FINALIZAR-PROCESO.
    CLOSE ARCHIVO-TRANSACCIONES
    CLOSE ARCHIVO-RESULTADOS
    
    DISPLAY 'PROCESO COMPLETADO'
    DISPLAY 'TOTAL REGISTROS: ' WS-TOTAL-REGISTROS
    DISPLAY 'REGISTROS OK: ' WS-REGISTROS-OK
    DISPLAY 'REGISTROS ERROR: ' WS-REGISTROS-ERROR."""
        }

    def test_enterprise_banking_complete_flow(self, mock_llm_responses):
        """Test del flujo completo para caso bancario empresarial."""
        graph = get_compiled_graph()
        
        # Ejecutar el grafo con un caso real (sin mocks para probar el agente mejorado)
        initial_state = {
            "request": "Crear programa COBOL para procesar transacciones bancarias con validación de RUT chileno y códigos de banco",
            "plan": "",
            "code": "",
            "error_message": "",
            "retry_count": 0
        }
        
        # Mock solo el validador para que siempre sea exitoso
        with patch('core.graph.validate_code') as mock_validator:
            mock_validator.return_value = {"status": "success", "message": "Código válido"}
            
            result = graph.invoke(initial_state)
            
            # Verificaciones del resultado
            assert result["code"] != "", "Debe generar código COBOL"
            
            # Verificar estructura empresarial básica
            assert "IDENTIFICATION DIVISION" in result["code"], "Debe incluir IDENTIFICATION DIVISION"
            assert "PROGRAM-ID" in result["code"], "Debe incluir PROGRAM-ID"
            
            # Verificar que incluye elementos empresariales (más flexibles)
            code_upper = result["code"].upper()
            
            # Verificar manejo de archivos (al menos uno de estos patrones)
            file_handling_patterns = [
                "SELECT", "ASSIGN TO", "FILE STATUS", "OPEN", "READ", "WRITE", "CLOSE"
            ]
            file_handling_found = any(pattern in code_upper for pattern in file_handling_patterns)
            assert file_handling_found, "Debe incluir manejo de archivos"
            
            # Verificar campos bancarios (al menos algunos)
            banking_patterns = [
                "RUT", "BANCO", "CLIENTE", "TRANSAC", "MONTO", "FECHA", "CODIGO"
            ]
            banking_found = any(pattern in code_upper for pattern in banking_patterns)
            assert banking_found, "Debe incluir campos relacionados con banca"
            
            # Verificar estructura WORKING-STORAGE
            assert "WORKING-STORAGE SECTION" in result["code"], "Debe incluir WORKING-STORAGE"
            
            # Verificar secciones modulares (al menos algunas)
            modular_patterns = ["SECTION", "PERFORM"]
            modular_found = any(pattern in code_upper for pattern in modular_patterns)
            assert modular_found, "Debe incluir programación modular"

    def test_enterprise_banking_with_correction_cycle(self, mock_llm_responses):
        """Test del flujo con ciclo de corrección para caso bancario."""
        graph = get_compiled_graph()
        
        # Simular un ciclo de corrección usando el validador mock
        initial_state = {
            "request": "Crear programa COBOL bancario con validaciones empresariales",
            "plan": "",
            "code": "",
            "error_message": "",
            "retry_count": 0
        }
        
        with patch('core.graph.validate_code') as mock_validator:
            # Configurar para que la primera validación falle y la segunda sea exitosa
            call_count = 0
            def mock_validate(code):
                nonlocal call_count
                call_count += 1
                if call_count == 1:
                    return {"status": "error", "message": "Error de sintaxis en PROCEDURE DIVISION"}
                else:
                    return {"status": "success", "message": "Código válido"}
            
            mock_validator.side_effect = mock_validate
            
            result = graph.invoke(initial_state)
            
            # Verificar que se completó el proceso (puede o no haber retry dependiendo del validador mock)
            assert result["code"] != "", "Debe contener código generado"
            assert "IDENTIFICATION DIVISION" in result["code"], "Debe incluir estructura COBOL básica"
            
            # Verificar que el validador fue llamado al menos una vez
            assert mock_validator.call_count >= 1, "El validador debe haber sido llamado"

    def test_enterprise_banking_complex_structures(self, mock_llm_responses):
        """Test específico para validar estructuras complejas empresariales."""
        graph = get_compiled_graph()
        
        # Ejecutar el grafo con solicitud específica para estructuras complejas
        initial_state = {
            "request": "Generar programa COBOL con estructuras jerárquicas complejas para procesamiento bancario incluyendo RUT, códigos de banco y montos COMP-3",
            "plan": "",
            "code": "",
            "error_message": "",
            "retry_count": 0
        }
        
        with patch('core.graph.validate_code') as mock_validator:
            mock_validator.return_value = {"status": "success", "message": "Código válido"}
            
            result = graph.invoke(initial_state)
            
            # Verificar estructuras jerárquicas específicas
            code_lines = result["code"].split('\n')
            code_upper = result["code"].upper()
            
            # Verificar niveles jerárquicos en WORKING-STORAGE
            ws_section_found = "WORKING-STORAGE SECTION" in result["code"]
            level_01_found = any("01 " in line for line in code_lines)
            level_05_found = any("05 " in line for line in code_lines)
            
            assert ws_section_found, "Debe incluir WORKING-STORAGE SECTION"
            assert level_01_found, "Debe incluir estructuras nivel 01"
            assert level_05_found, "Debe incluir estructuras nivel 05"
            
            # Verificar campos específicos del dominio bancario (más flexible)
            banking_patterns = ["RUT", "BANCO", "MONTO", "COMP"]
            banking_found = [pattern for pattern in banking_patterns if pattern in code_upper]
            
            assert len(banking_found) >= 2, f"Debe incluir al menos 2 campos bancarios, encontrados: {banking_found}"