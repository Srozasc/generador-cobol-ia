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
        "processing": "⏳",
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

    # Migración a Google AI Studio (Gemini)
    required_vars = ["GOOGLE_API_KEY"]
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

    print_status("Entorno configurado correctamente (Gemini)", "success")
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
            "retry_count": 0,
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
            print_status(
                f"Se realizaron {result['retry_count']} correcciones automáticas",
                "info",
            )

    print()

    # Mostrar el plan si está disponible
    if result.get("plan"):
        plan = result["plan"]
        if isinstance(plan, dict):
            print_code_block(
                "PLAN TÉCNICO GENERADO",
                f"Modo: {plan.get('mode', 'N/A')}\n"
                f"Descripción: {plan.get('plan', 'N/A')}\n"
                f"Pasos: {', '.join(plan.get('steps', []))}",
            )
        else:
            print_code_block("PLAN TÉCNICO GENERADO", str(plan))

    # Mostrar el código generado
    if result.get("code"):
        print_code_block("CÓDIGO COBOL GENERADO", result["code"])
    else:
        print_status("No se pudo generar código COBOL", "error")


def select_mode() -> str:
    """
    Permite al usuario seleccionar el modo de operación.
    
    Returns:
        str: '1' para generación, '2' para documentación
    """
    print_step(1, "SELECCIÓN DE MODO")
    print("Selecciona el modo de operación:")
    print("  1. Generar nuevo programa COBOL")
    print("  2. Documentar programa COBOL existente")
    print()
    
    while True:
        choice = input("👤 Selecciona una opción (1-2): ").strip()
        if choice in ['1', '2']:
            return choice
        print_status("Opción inválida. Elige 1 o 2.", "warning")


def get_file_path() -> str:
    """
    Solicita la ruta del archivo COBOL a documentar.
    
    Returns:
        str: Ruta del archivo COBOL
    
    Raises:
        SystemExit: Si el usuario cancela
    """
    print_step(2, "ARCHIVO A DOCUMENTAR")
    print("Ingresa la ruta del archivo .cbl (absoluta o relativa)")
    print("Ejemplo: ./ejemplo_codigo/SUPPGPR1.txt")
    print()
    
    while True:
        path = input("📁 Ruta del archivo: ").strip()
        if os.path.exists(path):
            return path
        
        print_status(f"Archivo no encontrado: {path}", "error")
        retry = input("¿Intentar de nuevo? (s/n): ").strip().lower()
        if retry != 's':
            print_status("Operación cancelada por el usuario", "warning")
            sys.exit(0)


def load_cobol_file(file_path: str) -> str:
    """
    Carga el contenido de un archivo COBOL.
    
    Args:
        file_path: Ruta del archivo a cargar
    
    Returns:
        str: Contenido del archivo COBOL
    
    Raises:
        FileNotFoundError: Si el archivo no existe
        ValueError: Si el archivo no contiene código COBOL válido
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Archivo no encontrado: {file_path}")
    
    # Intentar con encoding latin-1 (común en mainframes)
    try:
        with open(file_path, 'r', encoding='latin-1') as f:
            content = f.read()
    except UnicodeDecodeError:
        # Fallback a UTF-8
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    
    # Validación básica: debe contener IDENTIFICATION DIVISION
    if 'IDENTIFICATION DIVISION' not in content.upper():
        raise ValueError(
            "El archivo no parece contener código COBOL válido "
            "(falta IDENTIFICATION DIVISION)"
        )
    
    return content


def display_documentation(result: dict):
    """
    Muestra la documentación generada en consola.
    
    Args:
        result: Diccionario con la documentación generada
    """
    print_step(4, "DOCUMENTACIÓN GENERADA")
    
    if result.get("error_message"):
        print_status("Error al generar documentación", "error")
        print(f"Error: {result['error_message']}")
        return
    
    documentation = result.get("documentation", "")
    
    if not documentation:
        print_status("No se generó documentación", "warning")
        return
    
    print_status("Documentación generada exitosamente", "success")
    print()
    print("=" * 60)
    print(documentation)
    print("=" * 60)
    print()
    
    # Ofrecer guardar
    save = input("¿Deseas guardar la documentación en un archivo? (s/n): ").strip().lower()
    if save == 's':
        # Extraer PROGRAM-ID del contenido si es posible
        program_id = "DOCUMENTATION"
        if "PROGRAM-ID" in result.get("code", ""):
            # Intentar extraer el ID
            import re
            match = re.search(r'PROGRAM-ID[.\s]+([A-Z0-9]+)', result.get("code", ""))
            if match:
                program_id = match.group(1)
        
        filename = f"{program_id}_DOC.md"
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(documentation)
        print_status(f"Documentación guardada en: {filename}", "success")


def run_documentation_process(cobol_code: str) -> Optional[dict]:
    """
    Ejecuta el proceso de generación de documentación.
    
    Args:
        cobol_code: Código fuente COBOL
    
    Returns:
        Dict con la documentación generada
    """
    try:
        from core.graph import run_documentation_process as graph_run_doc
        
        print_step(3, "GENERANDO DOCUMENTACIÓN")
        print_status("Analizando código COBOL...", "processing")
        
        result = graph_run_doc(cobol_code)
        
        return result
    
    except ImportError as e:
        print_status(f"Error de importación: {e}", "error")
        return None
    except Exception as e:
        print_status(f"Error durante la documentación: {e}", "error")
        return None


def main():
    """Función principal del CLI."""
    print_banner()

    # Validar entorno
    if not validate_environment():
        sys.exit(1)

    try:
        # Seleccionar modo de operación
        mode = select_mode()
        print()
        
        if mode == '1':
            # Flujo de generación (existente)
            user_request = get_user_request()
            print()
            result = run_generation_process(user_request)

            if result:
                display_results(result)
                print_step(5, "PROCESO COMPLETADO")
                print_status("¡Gracias por usar el Generador COBOL IA!", "success")
                print("💡 El código generado puede requerir ajustes adicionales")
                print("   según los estándares específicos de tu entorno.")
            else:
                print_status("No se pudo completar la generación", "error")
                sys.exit(1)
        
        else:
            # Flujo de documentación (nuevo)
            file_path = get_file_path()
            print()
            
            print_status("Cargando archivo COBOL...", "processing")
            cobol_code = load_cobol_file(file_path)
            print_status(f"Archivo cargado: {len(cobol_code)} caracteres", "success")
            print()
            
            result = run_documentation_process(cobol_code)
            
            if result:
                display_documentation(result)
                print_step(5, "PROCESO COMPLETADO")
                print_status("¡Gracias por usar el Generador COBOL IA!", "success")
            else:
                print_status("No se pudo completar la documentación", "error")
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
