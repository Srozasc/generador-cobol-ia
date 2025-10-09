"""
Validador Simulado de código COBOL.

Este módulo implementa un validador que simula la validación de código COBOL
sin necesidad de conectarse a un mainframe real. Es útil para desarrollo
y testing del sistema.

El validador busca patrones comunes de errores y verifica la estructura
básica del código COBOL para determinar si es válido o no.
"""

import re
from typing import Dict, List


def validate_code(code: str) -> Dict[str, str]:
    """
    Valida código COBOL usando un validador simulado.
    
    Esta función simula la validación de código COBOL sin necesidad de un
    mainframe real. Busca patrones comunes de errores y verifica la estructura
    básica del programa.
    
    Args:
        code: Código COBOL a validar como string
        
    Returns:
        Dict con 'status' ('success'/'error') y 'message' con descripción
        
    Examples:
        >>> result = validate_code("IDENTIFICATION DIVISION.\\nPROGRAM-ID. TEST.")
        >>> result['status']
        'success'
        
        >>> result = validate_code("")
        >>> result['status']
        'error'
    """
    if not code or not code.strip():
        return {
            "status": "error",
            "message": "El código está vacío. Debe proporcionar código COBOL válido."
        }
    
    # Normalizar el código para análisis
    code_upper = code.upper().strip()
    lines = [line.strip() for line in code_upper.split('\n') if line.strip()]
    
    # Lista para acumular errores encontrados
    errors = []
    
    # Verificar estructura básica de COBOL
    errors.extend(_check_basic_structure(code_upper, lines))
    
    # Verificar errores de sintaxis comunes
    errors.extend(_check_syntax_errors(code_upper, lines))
    
    # Verificar palabras clave problemáticas
    errors.extend(_check_problematic_keywords(code_upper))
    
    # Determinar resultado final
    if errors:
        return {
            "status": "error",
            "message": f"Se encontraron {len(errors)} error(es): " + "; ".join(errors)
        }
    else:
        return {
            "status": "success",
            "message": "El código COBOL es válido y cumple con la estructura básica requerida."
        }


def _check_basic_structure(code_upper: str, lines: List[str]) -> List[str]:
    """
    Verifica la estructura básica requerida de un programa COBOL.
    
    Args:
        code_upper: Código en mayúsculas
        lines: Líneas del código sin espacios
        
    Returns:
        Lista de errores encontrados
    """
    errors = []
    
    # Verificar IDENTIFICATION DIVISION
    if "IDENTIFICATION DIVISION" not in code_upper:
        errors.append("Falta IDENTIFICATION DIVISION")
    
    # Verificar PROGRAM-ID
    if "PROGRAM-ID" not in code_upper:
        errors.append("Falta PROGRAM-ID")
    
    # Verificar PROCEDURE DIVISION (opcional pero recomendado)
    if "PROCEDURE DIVISION" not in code_upper:
        # Solo advertencia para programas muy simples
        if len(lines) > 5:  # Si es un programa más complejo
            errors.append("Se recomienda incluir PROCEDURE DIVISION")
    
    # Verificar STOP RUN o EXIT (buena práctica)
    if "STOP RUN" not in code_upper and "EXIT" not in code_upper:
        if "PROCEDURE DIVISION" in code_upper:
            errors.append("Se recomienda incluir STOP RUN o EXIT")
    
    return errors


def _check_syntax_errors(code_upper: str, lines: List[str]) -> List[str]:
    """
    Verifica errores de sintaxis comunes en COBOL.
    
    Args:
        code_upper: Código en mayúsculas
        lines: Líneas del código sin espacios
        
    Returns:
        Lista de errores de sintaxis encontrados
    """
    errors = []
    
    # Buscar patrones de error comunes
    error_patterns = [
        (r'SYNTAX-ERROR', "Se encontró SYNTAX-ERROR explícito"),
        (r'INVALID-STATEMENT', "Se encontró INVALID-STATEMENT"),
        (r'ERROR-HERE', "Se encontró ERROR-HERE"),
        (r'UNDEFINED-VAR', "Se encontró variable no definida"),
        (r'MISSING-PERIOD', "Falta punto al final de statement"),
    ]
    
    for pattern, message in error_patterns:
        if re.search(pattern, code_upper):
            errors.append(message)
    
    # Verificar estructura de líneas problemáticas
    for i, line in enumerate(lines, 1):
        # Líneas que terminan abruptamente sin punto
        if line.endswith('DISPLAY') or line.endswith('MOVE'):
            errors.append(f"Línea {i}: Statement incompleto")
        
        # Verificar caracteres problemáticos
        if '???' in line or '***' in line:
            errors.append(f"Línea {i}: Caracteres problemáticos encontrados")
    
    return errors


def _check_problematic_keywords(code_upper: str) -> List[str]:
    """
    Verifica palabras clave que pueden indicar problemas.
    
    Args:
        code_upper: Código en mayúsculas
        
    Returns:
        Lista de problemas encontrados
    """
    errors = []
    
    # Palabras que indican errores intencionalmente colocados en tests
    problematic_keywords = [
        "SYNTAX-ERROR-HERE",
        "INVALID-COMMAND",
        "UNDEFINED-FUNCTION",
        "MISSING-DECLARATION",
        "COMPILATION-ERROR"
    ]
    
    for keyword in problematic_keywords:
        if keyword in code_upper:
            errors.append(f"Palabra clave problemática encontrada: {keyword}")
    
    return errors


def get_validation_info() -> Dict[str, str]:
    """
    Retorna información sobre el validador simulado.
    
    Returns:
        Dict con información del validador
    """
    return {
        "validator_type": "mock",
        "version": "1.0.0",
        "description": "Validador simulado para desarrollo y testing",
        "capabilities": "Validación básica de estructura COBOL sin mainframe"
    }


def is_valid_cobol_structure(code: str) -> bool:
    """
    Función de conveniencia que retorna True/False para validez del código.
    
    Args:
        code: Código COBOL a validar
        
    Returns:
        True si el código es válido, False en caso contrario
    """
    result = validate_code(code)
    return result["status"] == "success"


# Constantes para configuración del validador
REQUIRED_DIVISIONS = ["IDENTIFICATION DIVISION"]
RECOMMENDED_DIVISIONS = ["PROCEDURE DIVISION"]
REQUIRED_STATEMENTS = ["PROGRAM-ID"]
ERROR_KEYWORDS = [
    "SYNTAX-ERROR", "INVALID-STATEMENT", "ERROR-HERE",
    "UNDEFINED-VAR", "COMPILATION-ERROR"
]