"""
Orquestador principal del generador COBOL IA usando LangGraph.

Este módulo implementa el grafo de estados que coordina los agentes
de planificación y codificación con el validador para generar código COBOL.
"""

from typing import TypedDict, Literal
from langgraph.graph import StateGraph, START, END
from agents.planner import get_planner_chain
from agents.coder import get_coder_chain
from validators.mock_validator import validate_code


class GraphState(TypedDict):
    """Estado del grafo de LangGraph."""
    request: str
    plan: str
    code: str
    error_message: str
    retry_count: int


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
            "error_message": state["error_message"]
        }
    else:
        # Modo creación
        input_data = {"request": state["request"]}
    
    result = planner_chain.invoke(input_data)
    return {"plan": result}


def coder_node(state: GraphState) -> dict:
    """
    Nodo del agente codificador.
    
    Args:
        state: Estado actual del grafo
        
    Returns:
        Dict con el código generado
    """
    coder_chain = get_coder_chain()
    result = coder_chain.invoke({"plan": state["plan"]})
    return {"code": result}


def validator_node(state: GraphState) -> dict:
    """
    Nodo del validador de código.
    
    Args:
        state: Estado actual del grafo
        
    Returns:
        Dict con el resultado de la validación
    """
    validation_result = validate_code(state["code"])
    
    if validation_result["status"] == "error":
        return {
            "error_message": validation_result["message"],
            "retry_count": state.get("retry_count", 0) + 1
        }
    else:
        return {
            "error_message": None,
            "retry_count": state.get("retry_count", 0)
        }


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
        return "planner"
    else:
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
        "validator",
        should_continue,
        {
            "planner": "planner",
            "__end__": END
        }
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
        "retry_count": 0
    }
    
    final_state = graph.invoke(initial_state)
    return final_state