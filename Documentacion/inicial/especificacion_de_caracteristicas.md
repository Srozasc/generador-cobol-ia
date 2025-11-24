## Sistema de Archivos
La estructura del proyecto estará organizada para separar claramente la lógica de los agentes, los validadores y las pruebas, facilitando el desarrollo guiado por tests (TDD).

```
generador_cobol_ia/
│
├── .venv/                  # Entorno virtual de Python
│
├── agents/                 # Lógica de los agentes de IA
│   ├── __init__.py
│   ├── planner.py          # Módulo para el Agente Planificador
│   └── coder.py            # Módulo para el Agente Codificador
│
├── validators/             # Lógica para la validación del código
│   ├── __init__.py
│   ├── mock_validator.py   # Validador Simulado para la Parte 1
│   └── mainframe_validator.py # Validador Real para la Parte 2
│
├── core/                   # Lógica central y orquestación
│   ├── __init__.py
│   └── graph.py            # Definición y compilación del grafo de LangGraph
│
├── tests/                  # Pruebas unitarias y de integración
│   ├── __init__.py
│   ├── agents/
│   │   ├── __init__.py
│   │   ├── test_planner.py
│   │   └── test_coder.py
│   ├── validators/
│   │   ├── __init__.py
│   │   └── test_mock_validator.py
│   └── test_integration_flow.py # Prueba del flujo completo con mocks
│
├── .env                    # Archivo para variables de entorno (API Keys)
├── .gitignore              # Archivo para ignorar directorios y archivos en Git
├── requirements.txt        # Lista de dependencias del proyecto
└── run_prototype.py        # Script principal para ejecutar el prototipo (CLI)
```

## Especificaciones de Funcionalidades

### Funcionalidad 1: Agente Codificador
**Objetivo de la funcionalidad:**
Crear un componente de IA determinista y reutilizable que reciba un plan de acción técnico y lo traduzca a código COBOL de alta calidad, sin añadir texto o explicaciones adicionales.

**Relaciones con APIs:**
*   **API Externa:** Google AI Studio (Gemini) por defecto; OpenAI/Anthropic opcionales. La comunicación se gestionará a través de `langchain_google_genai` (o el conector equivalente del proveedor elegido).

**Requisitos detallados de la funcionalidad:**
1.  **Entrada:** Debe aceptar un diccionario con una clave `"plan"` que contenga una cadena de texto (string) con la descripción técnica de la tarea a realizar.
2.  **Salida:** Debe devolver una única cadena de texto (string) que contenga exclusivamente código COBOL.
3.  **Prompting:** El prompt de sistema debe instruir explícitamente al modelo para que asuma el rol de un programador COBOL senior, se adhiera estrictamente al plan proporcionado y se abstenga de generar cualquier texto que no sea código.
4.  **Modelo:** Utilizará un modelo de lenguaje avanzado; por defecto `gemini-1.5-flash` para asegurar calidad y costo/latencia adecuados.
5.  **Determinismo:** Se configurará una `temperatura` baja (ej. 0.1) en la llamada al LLM para que los resultados sean consistentes y predecibles.
6.  **Aislamiento:** El agente debe ser "agnóstico" al resto del sistema; no debe conocer la existencia de otros agentes.
7.  **Estructura empresarial:** El código generado debe incluir cabeceras empresariales y mantener modularidad con `MAIN-PROCESS SECTION.` y `ESTADISTICA SECTION.` usando `PERFORM`.

**Guía detallada de implementación (TDD):**
1.  **Crear el archivo de prueba:** `tests/agents/test_coder.py`.
2.  **Escribir el primer test (`test_generates_hello_world`):**
    *   Simular un plan de entrada: `plan = "Crear un programa COBOL que muestre 'HOLA MUNDO'."`
    *   Llamar a la función que crea el agente codificador.
    *   Invocar el agente con el plan.
    *   Aseverar (assert) que la salida es un string.
    *   Aseverar que la salida contiene subcadenas clave como `IDENTIFICATION DIVISION.`, `PROCEDURE DIVISION.` y `DISPLAY "HOLA MUNDO"`.
3.  **Crear el archivo del módulo:** `agents/coder.py`.
4.  **Implementar la función `get_coder_chain()`:**
    *   Definir la plantilla del prompt (`ChatPromptTemplate`).
    *   Inicializar el LLM (entorno real: `ChatGoogleGenerativeAI`; en tests: stub determinista).
    *   Definir el parser de salida (`StrOutputParser`).
    *   Encadenar los componentes usando el operador pipe (`|`): `prompt | llm | output_parser`.
5.  **Ejecutar el test:** `pytest tests/agents/test_coder.py`. El test debe pasar.
6.  **Refactorizar:** Asegurarse de que el código sea limpio y la función esté bien documentada.

---

### Funcionalidad 2: Validador Simulado (Mock)
**Objetivo de la funcionalidad:**
Crear un sustituto del validador real que permita el desarrollo y la prueba del ciclo de autocorrección sin depender de una conexión a un mainframe. Debe ser una función pura que devuelva resultados predecibles basados en el contenido del código.

**Relaciones con APIs:**
*   Ninguna. Es una función interna de Python.

**Requisitos detallados de la funcionalidad:**
1.  **Entrada:** Aceptará una única cadena de texto (string) que representa el código COBOL generado.
2.  **Salida:** Devolverá un diccionario con dos claves obligatorias:
    *   `"status"`: un string con el valor `"success"` o `"error"`.
    *   `"message"`: un string que describe el resultado (ej. `"Compilación exitosa."` o un mensaje de error simulado).
3.  **Lógica de Error:** Debe implementar al menos dos reglas de error basadas en la presencia de palabras clave en el código de entrada. Por ejemplo:
    *   Si el código contiene `"VARIABLE-INCORRECTA"`, devuelve un error de "variable no definida".
    *   Si el código contiene `"FICHERO-FANTASMA"`, devuelve un error de "archivo no encontrado".
4.  **Lógica de Éxito:** Si ninguna de las reglas de error se cumple, debe devolver un estado de `"success"` por defecto.

**Guía detallada de implementación (TDD):**
1.  **Crear el archivo de prueba:** `tests/validators/test_mock_validator.py`.
2.  **Escribir los tests:**
    *   `test_returns_success_on_valid_code`: Pasa un código simple y asevera que el status es `"success"`.
    *   `test_returns_error_on_undefined_variable`: Pasa un código con la palabra clave de error y asevera que el status es `"error"` y el mensaje es el esperado.
    *   Repetir para la segunda regla de error.
3.  **Crear el archivo del módulo:** `validators/mock_validator.py`.
4.  **Implementar la función `validate_code(code: str) -> dict`:**
    *   Utilizar una estructura `if/elif/else` para comprobar la presencia de las palabras clave de error en el string de entrada.
    *   Construir y devolver el diccionario de respuesta apropiado en cada caso.
5.  **Ejecutar los tests:** `pytest tests/validators/test_mock_validator.py`. Todos deben pasar.

---

### Funcionalidad 3: Agente Planificador
**Objetivo de la funcionalidad:**
Actuar como el "cerebro" inicial del sistema. Debe ser capaz de interpretar una petición en lenguaje natural y convertirla en un plan técnico estructurado. Además, debe poder recibir un error y generar un plan de corrección.

**Relaciones con APIs:**
*   **API Externa:** Google AI Studio (Gemini) por defecto; OpenAI/Anthropic opcionales, gestionadas a través de `langchain_google_genai` (u otros conectores según el proveedor).

**Requisitos detallados de la funcionalidad:**
1.  **Modo dual:** El agente operará en dos modos implícitos basados en la entrada.
2.  **Modo Creación:**
    *   **Entrada:** Un diccionario con una clave `"request"` que contiene la petición del usuario.
    *   **Salida:** Un string que es un JSON válido, conteniendo el plan técnico.
3.  **Modo Corrección:**
    *   **Entrada:** Un diccionario que contiene la petición original, el código erróneo (`"code"`) y el mensaje de error (`"error_message"`).
    *   **Salida:** Un string en formato JSON con un nuevo plan enfocado exclusivamente en corregir el error reportado.
4.  **Prompting:** El prompt debe ser sofisticado, explicando ambos modos de operación. Debe instruir al modelo para que priorice la corrección del error cuando se le proporcione uno.
5.  **Formato de Salida:** Forzar la salida en formato JSON para que sea fácilmente parseable por los siguientes componentes del sistema.

**Guía detallada de implementación (TDD):**
1.  **Crear el archivo de prueba:** `tests/agents/test_planner.py`.
2.  **Escribir los tests:**
    *   `test_generates_plan_in_creation_mode`: Pasa una petición simple y asevera que la salida es un string que se puede parsear como JSON y contiene las claves esperadas.
    *   `test_generates_correction_plan_in_correction_mode`: Pasa un código de ejemplo y un mensaje de error. Asevera que el plan JSON resultante menciona explícitamente la corrección del error.
3.  **Crear el archivo del módulo:** `agents/planner.py`.
4.  **Implementar la función `get_planner_chain()`:**
    *   Diseñar el prompt complejo que maneje ambos casos de uso.
    *   Usar `ChatGoogleGenerativeAI` (entorno real) y un `JsonOutputParser` para garantizar la salida estructurada. En tests, utilizar el stub determinista.
    *   Encadenar los componentes.
5.  **Ejecutar los tests:** `pytest tests/agents/test_planner.py`. Todos deben pasar.

---

### Funcionalidad 4: Orquestador del Flujo de Agentes (Grafo)
**Objetivo de la funcionalidad:**
Conectar todos los agentes y componentes en un flujo de trabajo coherente y con estado, capaz de ejecutar el ciclo de autocorrección. Será la columna vertebral de la aplicación.

**Relaciones con APIs:**
*   Ninguna directamente. Orquesta los componentes que sí las utilizan.

**Requisitos detallados de la funcionalidad:**
1.  **Estado:** Definir una estructura de datos (ej. `TypedDict`) para el estado del grafo que contenga `request`, `plan`, `code`, `error_message`, `retry_count`, etc.
2.  **Nodos:** Cada agente o función principal (Planificador, Codificador, Validador) será encapsulado en un nodo del grafo. Cada nodo recibe el estado actual y devuelve un diccionario para actualizarlo.
3.  **Flujo Básico:** Definir las aristas (edges) que conectan los nodos en la secuencia lógica: `START -> planner -> coder -> validator`.
4.  **Flujo Condicional:** Implementar una arista condicional después del nodo `validator`. Esta función leerá el `status` del validador del estado y decidirá el siguiente paso:
    *   Si es `"success"`, la transición será hacia el nodo `END`.
    *   Si es `"error"`, la transición volverá al nodo `planner`.
5.  **Compilación:** El grafo debe ser compilado para crear un objeto `Runnable` que pueda ser invocado.

**Guía detallada de implementación (TDD):**
1.  **Crear el archivo de prueba de integración:** `tests/test_integration_flow.py`.
2.  **Escribir el test (`test_correction_loop`):**
    *   Usar `pytest-mock` para "parchear" los agentes Planificador y Codificador, forzándolos a devolver resultados predecibles.
    *   Configurar el `mock_validator` para que falle la primera vez y tenga éxito la segunda.
    *   Invocar el grafo compilado.
    *   Aseverar que los agentes fueron llamados el número correcto de veces (planner y coder dos veces, validador dos veces).
3.  **Crear el archivo del módulo:** `core/graph.py`.
4.  **Implementar la lógica del grafo:**
    *   Definir la clase de estado.
    *   Crear las funciones de nodo que invocan a los respectivos agentes y actualizan el estado.
    *   Crear la función de la arista condicional.
    *   Instanciar `StateGraph`, añadir los nodos, definir el punto de entrada, y añadir las aristas normales y condicionales.
    *   Compilar el grafo con `.compile()`.
5.  **Ejecutar el test de integración:** `pytest tests/test_integration_flow.py`. El test debe pasar, validando que el flujo completo funciona como se espera.

---

## Convenciones COBOL

- **Mayúsculas**: todo el código COBOL en MAYÚSCULAS.
- **Indentación**: 4 espacios en niveles de datos; 8 espacios en procedimientos.
- **Columnas**: 1–6 numeración (opcional), 7 indicador, 8–72 código.
- **Cabecera**: etiqueta `MANTENCIONES` (formato español), no `MAINTENANCE`.
- **Fechas**: `DATE-WRITTEN` en `MMM-YYYY`; entradas de `MANTENCIONES` en `DD/MM/YYYY`.
- **Secciones**: `MAIN-PROCESS SECTION.` y `ESTADISTICA SECTION.` con `PERFORM ESTADISTICA`.
- **Datacom**: comprobar `RQST-RET-CODE` tras `CALL 'DBNTRY'` y desviar a `ERROR-HANDLING` si el retorno no es cero.
