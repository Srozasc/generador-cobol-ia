"""
Agente Codificador - Generador de Código COBOL.

Este módulo contiene la lógica del Agente Codificador que convierte
un plan técnico estructurado en código COBOL funcional.
"""

import os
from typing import Dict, Any
from dotenv import load_dotenv

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

# Cargar variables de entorno
load_dotenv()


def get_coder_chain():
    """
    Crea y retorna una cadena de LangChain para generar código COBOL.
    
    Esta función encapsula:
    - El prompt especializado para generación de código COBOL
    - La configuración del modelo LLM (ChatOpenAI)
    - El parser de salida (StrOutputParser)
    - La cadena secuencial que los conecta
    
    Returns:
        RunnableSequence: Cadena de LangChain lista para invocar
    """
    
    # Configuración del modelo LLM desde variables de entorno
    llm = ChatOpenAI(
        model=os.getenv("LLM_MODEL", "gpt-5-nano-2025-08-07"),
        temperature=float(os.getenv("LLM_TEMPERATURE", "0.1")),
        api_key=os.getenv("OPENAI_API_KEY")
    )
    
    # Prompt especializado para generación de código COBOL
    prompt_template = ChatPromptTemplate.from_messages([
        ("system", """Eres un programador COBOL senior con más de 20 años de experiencia.
Tu tarea es convertir un plan técnico en código COBOL funcional y bien estructurado.

REGLAS IMPORTANTES:
1. Genera ÚNICAMENTE código COBOL puro, sin explicaciones adicionales
2. Usa MAYÚSCULAS para todo el código COBOL
3. Respeta el formato de columnas COBOL (1-6 números, 7 indicador, 8-72 código)
4. Incluye siempre las 4 divisiones obligatorias:
   - IDENTIFICATION DIVISION
   - ENVIRONMENT DIVISION (si es necesario)
   - DATA DIVISION (si es necesario)
   - PROCEDURE DIVISION
5. Usa indentación de 4 espacios para niveles de datos
6. Usa indentación de 8 espacios para procedimientos
7. Termina siempre con STOP RUN
8. Usa nombres descriptivos para variables (formato WS-NOMBRE-VARIABLE)
9. Usa DISPLAY para mostrar mensajes en pantalla
10. Adhiérete estrictamente al plan proporcionado

FORMATO DE SALIDA:
- Solo código COBOL
- Sin comentarios explicativos
- Sin texto adicional antes o después del código"""),
        
        ("human", """Plan técnico a implementar:
{plan}

Genera el código COBOL correspondiente:""")
    ])
    
    # Parser de salida para obtener string limpio
    output_parser = StrOutputParser()
    
    # Crear la cadena secuencial
    chain = (
        RunnablePassthrough.assign(plan=lambda x: x["plan"])
        | prompt_template
        | llm
        | output_parser
    )
    
    return chain


def generate_cobol_code(plan: str) -> str:
    """
    Función de conveniencia para generar código COBOL desde un plan.
    
    Args:
        plan: Descripción técnica del programa a generar
        
    Returns:
        str: Código COBOL generado
        
    Raises:
        ValueError: Si el plan está vacío o es inválido
        Exception: Si hay errores en la generación
    """
    if not plan or not plan.strip():
        raise ValueError("El plan no puede estar vacío")
    
    try:
        coder_chain = get_coder_chain()
        result = coder_chain.invoke({"plan": plan})
        
        if not result or not result.strip():
            raise Exception("El LLM no generó código válido")
            
        return result.strip()
        
    except Exception as e:
        raise Exception(f"Error al generar código COBOL: {str(e)}")


# Función auxiliar para validar estructura básica de COBOL
def _validate_cobol_structure(code: str) -> bool:
    """
    Valida que el código generado tenga estructura COBOL básica.
    
    Args:
        code: Código COBOL a validar
        
    Returns:
        bool: True si tiene estructura válida
    """
    required_elements = [
        "IDENTIFICATION DIVISION.",
        "PROGRAM-ID.",
        "PROCEDURE DIVISION."
    ]
    
    return all(element in code for element in required_elements)