# Plan de Implementación: Agente de Documentación Técnica (COBOL)

## 1. Objetivo
Implementar un nuevo agente de IA (`Documenter`) capaz de analizar código fuente COBOL existente y generar documentación técnica estructurada automáticamente. Este agente se integrará en la arquitectura actual basada en LangGraph.

## 2. Arquitectura Propuesta

### 2.1 Nuevo Módulo: `agents/documenter.py`
Se creará un nuevo módulo dedicado que contendrá la lógica del agente.

**Responsabilidades:**
- Recibir código COBOL en formato texto.
- Ejecutar una cadena de LangChain especializada.
- Extraer metadatos clave (Autor, Fecha, Sistema).
- Analizar variables de entrada/salida (File Section, Linkage Section).
- Resumir la lógica de negocio (Procedure Division).
- Generar salida en formato Markdown estandarizado.

**Componentes Clave:**
- `get_documenter_chain()`: Función factoría similar a `get_coder_chain` y `get_planner_chain`.
- **Prompt Especializado**: Diseñado para actuar como un "Analista Funcional Senior".

### 2.2 Integración en el Grafo (`core/graph.py`)
El grafo actual se extenderá para soportar un flujo de documentación, que es distinto al flujo de generación de código.

**Nuevo Nodo:**
- `documenter_node(state)`: Invoca al agente de documentación.

**Nuevo Estado del Grafo:**
Se necesita ampliar `GraphState` o reutilizar los campos existentes de manera inteligente.
```python
class GraphState(TypedDict):
    # ... campos existentes ...
    documentation: str  # Nuevo campo para guardar el resultado
    mode: str          # 'generation', 'correction', 'documentation'
```

**Flujo de Trabajo:**
El sistema deberá decidir qué camino tomar basado en el `request` del usuario o un flag explícito.
1. **Inicio** -> **Router/Clasificador** (o lógica en `main`)
2. Si es Documentación: **Inicio** -> **Documenter** -> **Fin**
3. Si es Generación: **Inicio** -> **Planner** -> **Coder** -> **Validator** -> **Fin**

## 3. Estrategia de Prompting (Prompt Engineering)

El prompt para el modelo Gemini deberá estructurarse para extraer secciones específicas.

**Estructura del Prompt:**
1. **Rol**: Documentador Técnico de Mainframe.
2. **Input**: Código COBOL crudo.
3. **Instrucciones de Extracción**:
   - **Identificación**: Program-ID, Autor, Objetivos (de comentarios).
   - **Datos**: Archivos (FD), Copybooks, Variables principales.
   - **Lógica**: Explicación narrativa de qué hace cada `SECTION` o `PARAGRAPH` principal.
4. **Formato de Salida**: Markdown con secciones claras.

## 4. Plan de Trabajo Detallado

### Fase 1: Creación del Agente (`agents/documenter.py`)
- [ ] Definir la función `get_documenter_chain`.
- [ ] Diseñar el prompt para análisis de COBOL.
- [ ] Implementar pruebas unitarias aisladas para verificar que el agente genera Markdown válido a partir de un snippet de COBOL.

### Fase 2: Actualización del Núcleo (`core/graph.py`)
- [ ] Modificar `GraphState` para incluir el campo `documentation`.
- [ ] Implementar `documenter_node`.
- [ ] Ajustar la lógica de enrutamiento (edges) para permitir la ejecución aislada de este nodo.

### Fase 3: Interfaz de Usuario (`run_prototype.py`)

**Estrategia de Implementación: Menú Interactivo**

Se implementará un sistema de menú que permita al usuario elegir entre dos modos de operación al inicio del programa:

#### 3.1 Selección de Modo
- [ ] Crear función `select_mode()` que muestre un menú numerado:
  - Opción 1: Generar nuevo programa COBOL
  - Opción 2: Documentar programa COBOL existente
- [ ] Validar la entrada del usuario (solo acepta '1' o '2')
- [ ] Retornar el modo seleccionado para dirigir el flujo

#### 3.2 Carga de Archivos COBOL
- [ ] Crear función `get_file_path()` para solicitar la ruta del archivo `.cbl`
- [ ] Implementar validación de existencia del archivo con `os.path.exists()`
- [ ] Permitir rutas absolutas y relativas
- [ ] Manejar encoding apropiado (`latin-1` o `cp1252` para archivos mainframe)
- [ ] Validación básica: verificar que contenga `IDENTIFICATION DIVISION`
- [ ] Opción de reintentar si el archivo no existe

#### 3.3 Flujo de Ejecución
```python
def main():
    print_banner()
    validate_environment()
    
    mode = select_mode()  # Nuevo paso
    
    if mode == '1':
        # Flujo existente de generación
        user_request = get_user_request()
        result = run_generation_process(user_request)
        display_results(result)
    else:
        # Nuevo flujo de documentación
        file_path = get_file_path()
        cobol_code = load_cobol_file(file_path)
        result = run_documentation_process(cobol_code)
        display_documentation(result)
```

#### 3.4 Visualización de Resultados
- [ ] Crear función `display_documentation(result)` específica para mostrar Markdown
- [ ] Opción de guardar en archivo `.md` con nombre basado en el PROGRAM-ID
- [ ] Mostrar preview en consola con formato legible

## 5. Ejemplo de Salida Esperada

```markdown
# Documentación Técnica: PROG001

## Información General
- **ID**: PROG001
- **Sistema**: BANCARIO
- **Descripción**: Procesa transacciones diarias y genera reporte de cuadratura.

## Archivos y Datos
- **Entrada**: ARCHIVO-TRANSACCIONES (Secuencial)
- **Salida**: REPORTE-DIARIO (Impresora/Spool)

## Lógica Principal
1. **Inicialización**: Abre archivos y valida fecha de proceso.
2. **Proceso**: Lee transacciones una a una. Si el monto > 1000, aplica retención.
3. **Finalización**: Cierra archivos y muestra estadísticas de control.
```
