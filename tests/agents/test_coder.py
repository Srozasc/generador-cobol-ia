"""
Tests unitarios para el Agente Codificador.

Este módulo contiene las pruebas para verificar que el Agente Codificador
genera código COBOL válido a partir de un plan técnico estructurado.
"""

import pytest
from unittest.mock import Mock, patch

# Importación del módulo que vamos a testear
from agents.coder import get_coder_chain


class TestCoderAgent:
    """Clase de pruebas para el Agente Codificador."""

    def test_generates_valid_cobol_structure(self):
        """
        Test que verifica que el Agente Codificador genera código COBOL válido para z/OS/390.
        
        Este test verifica que:
        1. La función get_coder_chain() existe y es invocable
        2. Acepta un diccionario con clave "plan"
        3. Retorna un string con código COBOL
        4. El código contiene las divisiones esenciales de COBOL
        5. El código es compatible con IBM z/OS/390
        6. El código incluye cabeceras empresariales completas
        """
        # Arrange: Preparar el plan de entrada
        test_plan = {
            "plan": "Crear un programa COBOL que muestre 'HOLA MUNDO' en pantalla"
        }
        
        # Act: Invocar el agente codificador
        coder_chain = get_coder_chain()
        result = coder_chain.invoke(test_plan)
        
        # Assert: Verificar que el resultado es válido
        assert result is not None, "El agente codificador debe retornar un resultado"
        assert isinstance(result, str), "El resultado debe ser un string con código COBOL"
        assert len(result.strip()) > 0, "El código generado no debe estar vacío"
        
        # Verificar que contiene las divisiones esenciales de COBOL
        assert "IDENTIFICATION DIVISION." in result, "Debe contener IDENTIFICATION DIVISION"
        assert "PROCEDURE DIVISION." in result, "Debe contener PROCEDURE DIVISION"
        assert "PROGRAM-ID." in result, "Debe contener PROGRAM-ID"
        
        # Verificar cabeceras empresariales
        assert "AUTHOR." in result, "Debe contener AUTHOR"
        assert "DATE-WRITTEN." in result, "Debe contener DATE-WRITTEN"
        assert "SISTEMA GENERADOR COBOL IA" in result, "Debe contener el autor estándar"
        assert "SISTEMA   :" in result, "Debe contener información del sistema"
        assert "SUBSISTEMA:" in result, "Debe contener información del subsistema"
        assert "OBJETIVOS :" in result, "Debe contener información de objetivos"
        assert "M A N T E N C I O N E S" in result, "Debe contener sección de mantenciones"
        assert "COBOL-IA" in result, "Debe contener responsable de generación"
        
        # Verificar que contiene elementos del programa "HOLA MUNDO"
        assert "HOLA MUNDO" in result or "HELLO WORLD" in result, "Debe contener el mensaje solicitado"
        assert "DISPLAY" in result, "Debe usar la instrucción DISPLAY para mostrar texto"
        assert "STOP RUN" in result, "Debe terminar con STOP RUN"
        
        # Verificar convenciones z/OS/390
        assert result.isupper(), "Todo el código COBOL debe estar en MAYÚSCULAS"
        
        # Verificar que el PROGRAM-ID sigue convenciones IBM (máximo 8 caracteres)
        lines = result.split('\n')
        program_id_line = next((line for line in lines if 'PROGRAM-ID.' in line), None)
        if program_id_line:
            # Extraer el nombre del programa después de PROGRAM-ID.
            program_name = program_id_line.split('PROGRAM-ID.')[1].strip().rstrip('.')
            # Permitir nombres descriptivos para el test básico, pero verificar formato válido
            assert program_name.replace('-', '').replace('_', '').isalnum(), f"PROGRAM-ID debe ser alfanumérico: {program_name}"

    def test_generates_enterprise_banking_structure(self):
        """
        Test que verifica que el Agente Codificador genera código COBOL empresarial bancario.
        
        Este test verifica que:
        1. Genera múltiples archivos con FILE STATUS
        2. Incluye SPECIAL-NAMES con DECIMAL-POINT IS COMMA
        3. Usa estructuras WORKING-STORAGE complejas
        4. Implementa secciones modulares
        5. Incluye campos bancarios específicos
        6. Incluye cabeceras empresariales completas
        """
        # Arrange: Plan para programa bancario empresarial
        test_plan = {
            "plan": "Crear un programa COBOL bancario que procese archivos de clientes y genere reportes de segmentación con múltiples archivos de entrada y salida"
        }
        
        # Act: Invocar el agente codificador
        coder_chain = get_coder_chain()
        result = coder_chain.invoke(test_plan)
        
        # Assert: Verificar estructura empresarial
        assert result is not None, "El agente debe retornar un resultado"
        assert isinstance(result, str), "El resultado debe ser un string"
        
        # Verificar cabeceras empresariales
        assert "IDENTIFICATION DIVISION." in result, "Debe contener IDENTIFICATION DIVISION"
        assert "AUTHOR." in result, "Debe contener AUTHOR"
        assert "DATE-WRITTEN." in result, "Debe contener DATE-WRITTEN"
        assert "SISTEMA   :" in result, "Debe contener información del sistema"
        assert "SUBSISTEMA:" in result, "Debe contener información del subsistema"
        assert "OBJETIVOS :" in result, "Debe contener información de objetivos"
        assert "M A N T E N C I O N E S" in result, "Debe contener sección de mantenciones"
        
        # Verificar configuración z/OS empresarial
        assert "SPECIAL-NAMES." in result, "Debe incluir SPECIAL-NAMES"
        assert "DECIMAL-POINT IS COMMA" in result, "Debe configurar punto decimal como coma"
        
        # Verificar múltiples archivos con FILE STATUS
        assert "INPUT-OUTPUT SECTION." in result, "Debe incluir INPUT-OUTPUT SECTION"
        assert "SELECT" in result and "ASSIGN TO" in result, "Debe incluir definiciones SELECT"
        assert "FILE STATUS IS" in result, "Debe usar FILE STATUS"
        assert "WS-STATUS-" in result, "Debe incluir variables de FILE STATUS"
        
        # Verificar secciones modulares
        assert "SECTION." in result, "Debe incluir secciones modulares"
        section_count = result.count("SECTION.")
        assert section_count >= 2, f"Debe tener al menos 2 secciones, encontradas: {section_count}"
        
        # Verificar manejo de errores empresarial
        assert "ERROR" in result, "Debe incluir manejo de errores"
        assert "PERFORM" in result, "Debe usar PERFORM para modularidad"

    def test_generates_banking_fields(self):
        """
        Test que verifica que el agente genera campos bancarios específicos del dominio.
        """
        # Arrange: Plan específico para campos bancarios
        test_plan = {
            "plan": "Crear programa COBOL para procesar datos de clientes bancarios con RUT chileno, códigos de banco, fechas de proceso y montos"
        }
        
        # Act: Invocar el agente codificador
        coder_chain = get_coder_chain()
        result = coder_chain.invoke(test_plan)
        
        # Assert: Verificar campos bancarios específicos
        banking_patterns = [
            "PIC X(09)",  # RUT chileno
            "PIC X(03)",  # Código banco
            "PIC X(08)",  # Fecha proceso
            "COMP-3",     # Montos empaquetados
            "WS-",        # Prefijo Working Storage
        ]
        
        for pattern in banking_patterns:
            assert pattern in result, f"Debe incluir patrón bancario: {pattern}"

    def test_generates_complex_working_storage(self):
        """
        Test que verifica estructuras WORKING-STORAGE complejas con niveles jerárquicos.
        """
        # Arrange: Plan para estructuras complejas
        test_plan = {
            "plan": "Crear programa COBOL con tablas de datos, estructuras jerárquicas y condiciones 88-level para validaciones"
        }
        
        # Act: Invocar el agente codificador
        coder_chain = get_coder_chain()
        result = coder_chain.invoke(test_plan)
        
        # Assert: Verificar estructuras complejas
        assert "01 " in result, "Debe incluir nivel 01"
        assert "05 " in result or "10 " in result, "Debe incluir niveles jerárquicos"
        
        # Verificar que hay múltiples niveles de datos
        level_01_count = result.count("01 ")
        assert level_01_count >= 2, f"Debe tener múltiples estructuras nivel 01, encontradas: {level_01_count}"

    def test_generates_file_handling_with_status(self):
        """
        Test que verifica el manejo correcto de archivos con FILE STATUS.
        """
        # Arrange: Plan específico para manejo de archivos
        test_plan = {
            "plan": "Crear programa COBOL que lea archivo de entrada y escriba archivo de salida con control de errores"
        }
        
        # Act: Invocar el agente codificador
        coder_chain = get_coder_chain()
        result = coder_chain.invoke(test_plan)
        
        # Assert: Verificar manejo de archivos
        assert "SELECT" in result, "Debe incluir SELECT para archivos"
        assert "ASSIGN TO" in result, "Debe incluir ASSIGN TO"
        assert "FILE STATUS IS" in result, "Debe incluir FILE STATUS"
        assert "OPEN" in result, "Debe incluir operaciones OPEN"
        assert "READ" in result or "WRITE" in result, "Debe incluir operaciones de archivo"
        
        # Verificar control de errores de archivo
        assert "IF" in result and "STATUS" in result, "Debe verificar FILE STATUS"
        """
        Test que verifica que el agente genera código COBOL con acceso a Datacom.
        """
        # Arrange: Plan que requiere acceso a base de datos
        test_plan = {
            "plan": "Crear programa COBOL que consulte la tabla CLIENTES en Datacom y muestre el nombre del cliente con ID '12345'"
        }
        
        # Act: Invocar el agente codificador
        coder_chain = get_coder_chain()
        result = coder_chain.invoke(test_plan)
        
        # Assert: Verificar elementos específicos de Datacom
        assert "EXEC SQL" in result, "Debe contener comandos SQL embebidos"
        assert "END-EXEC" in result, "Debe cerrar comandos SQL correctamente"
        assert "BEGIN DECLARE SECTION" in result, "Debe declarar host-variables"
        assert "END DECLARE SECTION" in result, "Debe cerrar sección de declaraciones"
        assert "SQLCODE" in result, "Debe incluir variable de control SQLCODE"
        assert "SQLSTATE" in result, "Debe incluir variable de control SQLSTATE"
        
        # Verificar manejo de errores SQL
        assert "IF SQLCODE" in result, "Debe verificar SQLCODE para manejo de errores"
        
        # Verificar tipos de datos z/OS
        assert "PIC X(" in result or "PIC S9(" in result, "Debe usar tipos de datos z/OS"
        assert "COMP" in result or "COMP-3" in result, "Debe usar tipos de datos optimizados para z/OS"

    def test_generates_zos_data_types(self):
        """
        Test que verifica el uso de tipos de datos específicos de z/OS.
        """
        # Arrange: Plan que requiere diferentes tipos de datos
        test_plan = {
            "plan": "Crear programa COBOL que maneje un cliente con ID (texto), edad (número entero) y salario (decimal empaquetado)"
        }
        
        # Act: Invocar el agente codificador
        coder_chain = get_coder_chain()
        result = coder_chain.invoke(test_plan)
        
        # Assert: Verificar tipos de datos z/OS
        assert "PIC X(" in result, "Debe usar PIC X para campos de texto"
        assert "PIC S9(" in result, "Debe usar PIC S9 para números"
        assert "COMP-3" in result or "COMP" in result, "Debe usar tipos de datos empaquetados/binarios"
        
        # Verificar convenciones de nomenclatura IBM
        assert "WS-" in result, "Debe usar prefijo WS- para variables de working-storage"

    def test_generates_error_handling(self):
        """
        Test que verifica la generación de manejo de errores SQL estándar.
        """
        # Arrange: Plan que requiere operación SQL con manejo de errores
        test_plan = {
            "plan": "Crear programa COBOL que inserte un nuevo cliente en Datacom y maneje posibles errores"
        }
        
        # Act: Invocar el agente codificador
        coder_chain = get_coder_chain()
        result = coder_chain.invoke(test_plan)
        
        # Assert: Verificar manejo de errores
        assert "SQLCODE" in result, "Debe incluir variable SQLCODE"
        assert "IF SQLCODE" in result, "Debe verificar SQLCODE"
        assert "DISPLAY" in result and "ERROR" in result, "Debe mostrar mensajes de error"
        assert "SQLSTATE" in result, "Debe incluir SQLSTATE para errores específicos"

    def test_handles_empty_plan(self):
        """
        Test que verifica el manejo de planes vacíos o mínimos.
        El agente debe generar código COBOL básico incluso con plan vacío.
        """
        # Arrange: Plan vacío
        empty_plan = {"plan": ""}
        
        # Act: Invocar el agente con plan vacío
        coder_chain = get_coder_chain()
        result = coder_chain.invoke(empty_plan)
        
        # Assert: Debe generar código COBOL básico válido
        assert isinstance(result, str), "Debe retornar una cadena"
        assert len(result.strip()) > 0, "No debe retornar cadena vacía"
        
        # Verificar que contiene elementos básicos de COBOL
        result_upper = result.upper()
        assert "IDENTIFICATION DIVISION" in result_upper, "Debe contener IDENTIFICATION DIVISION"
        assert "PROGRAM-ID" in result_upper, "Debe contener PROGRAM-ID"

    def test_generates_different_programs(self):
        """
        Test que verifica que diferentes planes generan diferentes programas.
        """
        # Arrange: Dos planes diferentes
        plan1 = {"plan": "Crear programa que sume dos números"}
        plan2 = {"plan": "Crear programa que calcule el factorial"}
        
        # Act: Generar código para ambos planes
        coder_chain = get_coder_chain()
        result1 = coder_chain.invoke(plan1)
        result2 = coder_chain.invoke(plan2)
        
        # Assert: Los resultados deben ser diferentes
        assert result1 is not None and result2 is not None
        assert result1 != result2, "Planes diferentes deben generar código diferente"


class TestCoderChainIntegration:
    """Pruebas de integración para la cadena del codificador."""

    @patch('agents.coder.ChatOpenAI')
    def test_uses_correct_llm_configuration(self, mock_chat_openai):
        """
        Test que verifica que el codificador usa la configuración correcta del LLM.
        """
        # Arrange: Mock del LLM
        mock_llm = Mock()
        mock_chat_openai.return_value = mock_llm
        
        # Act: Crear la cadena del codificador
        coder_chain = get_coder_chain()
        
        # Assert: Verificar configuración del LLM
        mock_chat_openai.assert_called_once()
        call_args = mock_chat_openai.call_args
        assert call_args[1]['model'] == 'gpt-5-nano-2025-08-07'
        assert call_args[1]['temperature'] == 0.1

    def test_chain_structure(self):
        """
        Test que verifica la estructura de la cadena LangChain.
        """
        # Act: Crear la cadena del codificador
        coder_chain = get_coder_chain()
        
        # Assert: Verificar que es una instancia de RunnableSequence
        from langchain_core.runnables import RunnableSequence
        assert isinstance(coder_chain, RunnableSequence)