"""
Orquestador principal del generador COBOL IA usando LangGraph.

Este módulo implementa el grafo de estados que coordina los agentes
de planificación y codificación con el validador para generar código COBOL.
"""

import logging
import os
from typing import Literal, TypedDict

from langgraph.graph import END, START, StateGraph

from agents.coder import get_coder_chain
from agents.documenter import generate_documentation
from agents.planner import get_planner_chain
from validators.mock_validator import validate_code


class GraphState(TypedDict, total=False):
    """Estado del grafo de LangGraph.
    
    Soporta tres modos de operación:
    - 'generation': Generación de código COBOL nuevo
    - 'correction': Corrección de código existente
    - 'documentation': Generación de documentación técnica
    """

    request: str
    plan: str
    code: str
    error_message: str
    retry_count: int
    documentation: str  # Documentación generada (modo documentation)
    mode: str  # 'generation', 'correction', 'documentation'


def planner_node(state: GraphState) -> dict:
    """
    Nodo del agente planificador.

    Args:
        state: Estado actual del grafo

    Returns:
        Dict con el plan generado
    """
    planner_chain = get_planner_chain()

    # Preparar entrada según el modo
    if state.get("code") and state.get("error_message"):
        # Modo corrección
        input_data = {
            "request": state["request"],
            "code": state["code"],
            "error_message": state["error_message"],
        }
    else:
        # Modo creación
        input_data = {"request": state["request"]}

    logger.info("Ejecutando nodo planner")
    result = planner_chain.invoke(input_data)
    logger.debug(f"Plan generado: {result}")
    return {"plan": result}


def coder_node(state: GraphState) -> dict:
    """
    Nodo del agente codificador.

    Args:
        state: Estado actual del grafo

    Returns:
        Dict con el código generado
    """
    logger.info("Ejecutando nodo coder")
    coder_chain = get_coder_chain()
    result = coder_chain.invoke({"plan": state["plan"]})
    logger.debug("Código generado (primeras 120 chars): %s", str(result)[:120])
    return {"code": result}


def validator_node(state: GraphState) -> dict:
    """
    Nodo del validador de código.

    Args:
        state: Estado actual del grafo

    Returns:
        Dict con el resultado de la validación
    """
    logger.info("Ejecutando nodo validator")
    validation_result = validate_code(state["code"])
    logger.debug(f"Resultado validación: {validation_result}")

    if validation_result["status"] == "error":
        return {
            "error_message": validation_result["message"],
            "retry_count": state.get("retry_count", 0) + 1,
        }
    else:
        return {"error_message": None, "retry_count": state.get("retry_count", 0)}


def should_continue(state: GraphState) -> Literal["planner", "__end__"]:
    """
    Función condicional que determina si continuar o terminar.

    Args:
        state: Estado actual del grafo

    Returns:
        Siguiente nodo o END
    """
    # Si hay error y no hemos excedido el límite de reintentos
    if state.get("error_message") and state.get("retry_count", 0) < 3:
        logger.info("Se detectó error. Reintentando con planner")
        return "planner"
    else:
        logger.info("Finalizando flujo")
        return "__end__"


def get_compiled_graph():
    """
    Construye y compila el grafo de LangGraph.

    Returns:
        Grafo compilado listo para ejecutar
    """
    # Crear el grafo de estados
    workflow = StateGraph(GraphState)

    # Agregar nodos
    workflow.add_node("planner", planner_node)
    workflow.add_node("coder", coder_node)
    workflow.add_node("validator", validator_node)

    # Definir aristas
    workflow.add_edge(START, "planner")
    workflow.add_edge("planner", "coder")
    workflow.add_edge("coder", "validator")

    # Arista condicional desde validator
    workflow.add_conditional_edges(
        "validator", should_continue, {"planner": "planner", "__end__": END}
    )

    # Compilar el grafo
    return workflow.compile()


def run_cobol_generation(request: str) -> GraphState:
    """
    Ejecuta el proceso completo de generación de código COBOL.

    Args:
        request: Solicitud en lenguaje natural

    Returns:
        Estado final con el código generado
    """
    graph = get_compiled_graph()

    initial_state = {
        "request": request,
        "plan": "",
        "code": "",
        "error_message": "",
        "retry_count": 0,
    }

    final_state = graph.invoke(initial_state)
    return final_state


def documenter_node(state: GraphState) -> dict:
    """
    Nodo del agente de documentación.
    
    Args:
        state: Estado actual del grafo
    
    Returns:
        Dict con la documentación generada
    """
    logger.info("Ejecutando nodo documenter")
    
    cobol_code = state.get("code", "")
    
    if not cobol_code or not cobol_code.strip():
        logger.warning("Código COBOL vacío en documenter_node")
        return {
            "error_message": "Código COBOL vacío",
            "documentation": "# Error\n\nNo se proporcionó código COBOL para documentar.",
        }
    
    try:
        documentation = generate_documentation(cobol_code)
        logger.debug(
            "Documentación generada (primeras 100 chars): %s", documentation[:100]
        )
        return {"documentation": documentation, "error_message": ""}
    except Exception as e:
        logger.error(f"Error al generar documentación: {e}")
        return {
            "error_message": str(e),
            "documentation": f"# Error\n\nNo se pudo generar documentación: {str(e)}",
        }


def get_documentation_graph():
    """
    Construye y compila el grafo de LangGraph para documentación.
    
    Este grafo es más simple que el de generación:
    START -> documenter -> END
    
    Returns:
        Grafo compilado listo para ejecutar
    """
    # Crear el grafo de estados
    workflow = StateGraph(GraphState)
    
    # Agregar solo el nodo documenter
    workflow.add_node("documenter", documenter_node)
    
    # Definir aristas: flujo lineal simple
    workflow.add_edge(START, "documenter")
    workflow.add_edge("documenter", END)
    
    # Compilar el grafo
    return workflow.compile()


def run_documentation_process(cobol_code: str) -> GraphState:
    """
    Ejecuta el proceso completo de generación de documentación.
    
    Args:
        cobol_code: Código fuente COBOL a documentar
    
    Returns:
        Estado final con la documentación generada
    """
    graph = get_documentation_graph()
    
    initial_state: GraphState = {
        "request": "Generar documentación técnica",
        "plan": "",
        "code": cobol_code,
        "error_message": "",
        "retry_count": 0,
        "documentation": "",
        "mode": "documentation",
    }
    
    final_state = graph.invoke(initial_state)
    return final_state


# Configuración básica de logging
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()
logging.basicConfig(
    level=getattr(logging, LOG_LEVEL, logging.INFO),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger("core.graph")
