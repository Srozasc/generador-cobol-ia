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
        Test que verifica que el Agente Codificador genera código COBOL válido.
        
        Este test verifica que:
        1. La función get_coder_chain() existe y es invocable
        2. Acepta un diccionario con clave "plan"
        3. Retorna un string con código COBOL
        4. El código contiene las divisiones esenciales de COBOL
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
        
        # Verificar que contiene elementos del programa "HOLA MUNDO"
        assert "HOLA MUNDO" in result or "HELLO WORLD" in result, "Debe contener el mensaje solicitado"
        assert "DISPLAY" in result, "Debe usar la instrucción DISPLAY para mostrar texto"
        assert "STOP RUN" in result, "Debe terminar con STOP RUN"

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