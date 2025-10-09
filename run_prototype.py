#!/usr/bin/env python3
"""
Script principal CLI para el Generador COBOL IA.

Este script proporciona una interfaz de línea de comandos narrativa
que guía al usuario a través del proceso de generación de código COBOL
usando inteligencia artificial.
"""

import os
import sys
from typing import Optional
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

def print_banner():
    """Muestra el banner de bienvenida del sistema."""
    print("=" * 60)
    print("🤖 GENERADOR COBOL IA - PROTOTIPO MVP")
    print("=" * 60)
    print("Sistema de generación automática de código COBOL")
    print("usando agentes de inteligencia artificial.")
    print("=" * 60)
    print()

def print_step(step_number: int, description: str):
    """Muestra un paso del proceso con formato narrativo."""
    print(f"📋 PASO {step_number}: {description}")
    print("-" * 50)

def print_status(message: str, status_type: str = "info"):
    """Muestra un mensaje de estado con formato."""
    icons = {
        "info": "ℹ️",
        "success": "✅", 
        "error": "❌",
        "warning": "⚠️",
        "processing": "⏳"
    }
    icon = icons.get(status_type, "ℹ️")
    print(f"{icon} {message}")

def print_code_block(title: str, code: str):
    """Muestra un bloque de código con formato."""
    print(f"\n📄 {title}")
    print("=" * len(title) + "===")
    print(code)
    print("=" * (len(title) + 3))
    print()

def get_user_request() -> str:
    """Solicita al usuario la descripción del programa COBOL a generar."""
    print_step(1, "SOLICITUD DEL USUARIO")
    print("Describe el programa COBOL que deseas generar.")
    print("Ejemplo: 'Crear un programa que calcule el factorial de un número'")
    print()
    
    while True:
        request = input("👤 Tu solicitud: ").strip()
        if request:
            return request
        print_status("Por favor, ingresa una descripción válida.", "warning")

def validate_environment() -> bool:
    """Valida que las variables de entorno necesarias estén configuradas."""
    print_step(0, "VALIDACIÓN DEL ENTORNO")
    
    required_vars = ["OPENAI_API_KEY"]
    missing_vars = []
    
    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)
    
    if missing_vars:
        print_status("Variables de entorno faltantes:", "error")
        for var in missing_vars:
            print(f"  - {var}")
        print()
        print("💡 Configura las variables en el archivo .env")
        return False
    
    print_status("Entorno configurado correctamente", "success")
    print()
    return True

def run_generation_process(request: str) -> Optional[dict]:
    """Ejecuta el proceso de generación de código COBOL."""
    try:
        # Importar aquí para evitar errores si las dependencias no están instaladas
        from core.graph import get_compiled_graph
        
        print_step(2, "INICIALIZANDO SISTEMA")
        print_status("Cargando agentes de IA...", "processing")
        
        # Obtener el grafo compilado
        graph = get_compiled_graph()
        print_status("Sistema inicializado correctamente", "success")
        print()
        
        # Estado inicial
        initial_state = {
            "request": request,
            "plan": None,
            "code": None,
            "error_message": None,
            "retry_count": 0
        }
        
        print_step(3, "PROCESO DE GENERACIÓN")
        print_status("Planificando solución...", "processing")
        
        # Ejecutar el grafo
        result = graph.invoke(initial_state)
        
        return result
        
    except ImportError as e:
        print_status(f"Error de importación: {e}", "error")
        print("💡 Asegúrate de que todas las dependencias estén instaladas")
        return None
    except Exception as e:
        print_status(f"Error durante la generación: {e}", "error")
        return None

def display_results(result: dict):
    """Muestra los resultados del proceso de generación."""
    print_step(4, "RESULTADOS")
    
    if result.get("error_message"):
        print_status("Generación completada con errores", "warning")
        print(f"Error final: {result['error_message']}")
        print(f"Intentos realizados: {result.get('retry_count', 0)}")
    else:
        print_status("Generación completada exitosamente", "success")
        if result.get("retry_count", 0) > 0:
            print_status(f"Se realizaron {result['retry_count']} correcciones automáticas", "info")
    
    print()
    
    # Mostrar el plan si está disponible
    if result.get("plan"):
        plan = result["plan"]
        if isinstance(plan, dict):
            print_code_block("PLAN TÉCNICO GENERADO", 
                           f"Modo: {plan.get('mode', 'N/A')}\n"
                           f"Descripción: {plan.get('plan', 'N/A')}\n"
                           f"Pasos: {', '.join(plan.get('steps', []))}")
        else:
            print_code_block("PLAN TÉCNICO GENERADO", str(plan))
    
    # Mostrar el código generado
    if result.get("code"):
        print_code_block("CÓDIGO COBOL GENERADO", result["code"])
    else:
        print_status("No se pudo generar código COBOL", "error")

def main():
    """Función principal del CLI."""
    print_banner()
    
    # Validar entorno
    if not validate_environment():
        sys.exit(1)
    
    try:
        # Obtener solicitud del usuario
        user_request = get_user_request()
        print()
        
        # Ejecutar proceso de generación
        result = run_generation_process(user_request)
        
        if result:
            # Mostrar resultados
            display_results(result)
            
            # Mensaje final
            print_step(5, "PROCESO COMPLETADO")
            print_status("¡Gracias por usar el Generador COBOL IA!", "success")
            print("💡 El código generado puede requerir ajustes adicionales")
            print("   según los estándares específicos de tu entorno.")
        else:
            print_status("No se pudo completar la generación", "error")
            sys.exit(1)
            
    except KeyboardInterrupt:
        print("\n")
        print_status("Proceso interrumpido por el usuario", "warning")
        sys.exit(0)
    except Exception as e:
        print_status(f"Error inesperado: {e}", "error")
        sys.exit(1)

if __name__ == "__main__":
    main()