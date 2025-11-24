## Funcionalidades de Lanzamiento (MVP)
### Generación de Código Base (Agente Codificador)
Este componente es el núcleo de la generación de código. Su única responsabilidad es recibir un plan de acción técnico y estructurado, y traducirlo en un programa COBOL completo y sintácticamente correcto, actuando como un programador experto.
* Recibir un plan en formato estructurado (ej. JSON) con las instrucciones de lo que el código debe hacer.
* Generar el código COBOL correspondiente, incluyendo todas las divisiones necesarias (`IDENTIFICATION`, `DATA`, `PROCEDURE`).
* El código generado debe ser autocontenido y listo para ser compilado.
* Actuar de forma determinista y sin estado (la misma entrada de plan debe producir un resultado similar).

### Tecnología Involucrada
Python, LangChain (Google Generative AI - Gemini), TDD con `pytest`.

### Requisitos Principales
* El desarrollo seguirá un enfoque TDD. Se crearán tests unitarios que validen que, para un plan de entrada conocido (ej: "hola mundo"), el código de salida contiene las secciones y sentencias COBOL esperadas (`IDENTIFICATION DIVISION.`, `DISPLAY '...'`, etc.).
* El prompt del agente será diseñado para evitar la "conversación" o texto explicativo en la salida, entregando únicamente el código.

### Orquestación y Ciclo de Autocorrección (Simulado)
Esta es la "inteligencia" central del sistema, donde múltiples agentes colaboran. El sistema recibe una petición en lenguaje natural, la planifica, la codifica y simula una validación. Si la validación simulada falla, el sistema es capaz de analizar el error y reintentar el proceso con un plan de corrección.
* **Agente Planificador:** Convierte una petición en lenguaje natural a un plan técnico estructurado.
* **Agente Codificador:** Utiliza el plan para generar el código (componente anterior).
* **Validador Simulado (Mock):** Una función que inspecciona el código en busca de "errores" predefinidos (palabras clave) y devuelve un estado de `éxito` o `error` con un mensaje.
* **Ciclo de Corrección:** Si el validador devuelve `error`, el flujo vuelve al Planificador, entregándole el código erróneo y el mensaje de error para que genere un nuevo plan de corrección.

### Tecnología Involucrada
Python, LangGraph, LangChain (Gemini), TDD con `pytest` y `pytest-mock`.

### Requisitos Principales
* El desarrollo de cada componente (Planificador, Validador) se hará con TDD. Por ejemplo, se crearán tests para el Planificador que validen que transforma correctamente frases de entrada en JSON de salida.
* Se creará un test de integración para el grafo completo. Este test simulará una petición de usuario diseñada para fallar, y validará que el sistema realiza al menos un ciclo de corrección y finalmente devuelve un estado de `éxito`.
* En la suite de tests se utilizará un **stub de LLM** determinista (`tests/conftest.py`) que simula respuestas de Gemini para asegurar reproducibilidad.

### Interfaz de Línea de Comandos (CLI) Narrativa
Es la interfaz de usuario para el prototipo. Permite a un usuario interactuar con el sistema, introducir peticiones y ver de forma clara y descriptiva cada paso que el sistema está tomando, desde la planificación inicial hasta los ciclos de corrección y la entrega final del código.
* Solicitar al usuario que ingrese una petición en lenguaje natural.
* Imprimir en la consola mensajes descriptivos del estado actual del proceso ("Planificando...", "Generando código...", "Error detectado, re-planificando...").
* Mostrar el código generado en cada etapa (inicial y corregido).
* Presentar el código final validado.

### Tecnología Involucrada
Python (módulos `input`, `print`).

### Requisitos Principales
* Las funciones que generan los mensajes narrativos serán probadas con TDD para asegurar un formato consistente.
* Se usará `unittest.mock` para simular la entrada del usuario en los tests automatizados, haciendo el proceso de prueba no interactivo.

### Integración Real con Mainframe (Validador Real)
Este componente reemplaza al Validador Simulado. Su función es tomar el código COBOL generado, conectarse a un entorno mainframe real, subir el código, ejecutarlo a través de un JCL, capturar la salida y analizarla para determinar si la compilación y ejecución fueron exitosas.
* Conectarse a un emulador 3270 usando credenciales proporcionadas.
* Navegar por los menús de ISPF/TSO para crear un miembro en un PDS.
* Escribir el código COBOL en dicho miembro.
* Someter un trabajo (JCL) que compile y ejecute el programa.
* Navegar a la cola de trabajos (JES/SDSF) para encontrar el resultado.
* Extraer el log de salida (spool) y analizarlo para encontrar el código de retorno (`MAXCC`) y mensajes de error.

### Tecnología Involucrada
Python, py3270, TDD con `pytest` y `pytest-mock`.

### Requisitos Principales
* El desarrollo se enfocará en TDD usando intensivamente *mocks*. Se crearán tests que simulen la respuesta del emulador `py3270` para validar la lógica de navegación sin necesidad de una conexión real continua.
* La función de análisis del spool será probada unitariamente con archivos de texto que contengan logs de salida reales (tanto de éxito como de error), asegurando que el parsing es correcto.

## Funcionalidades Futuras (Post MVP)
### Interfaz de Usuario Web
Reemplazar la CLI por una interfaz web moderna y amigable.
* Área de texto para que el usuario ingrese la petición.
* Visualización en tiempo real del estado del proceso.
* Resaltado de sintaxis (syntax highlighting) para el código COBOL generado.
* Historial de peticiones y gestor de fragmentos de código.

### Tecnología Involucrada
FastAPI/Flask (Backend), React/Vue (Frontend).

### Análisis y Modificación de Código Existente
Extender la capacidad del sistema para que no solo genere código nuevo, sino que pueda leer un programa COBOL existente, entenderlo y aplicar modificaciones basadas en peticiones en lenguaje natural.
* Capacidad de "ingestar" o recibir un fichero de código COBOL.
* Un agente especializado en análisis de código para interpretar la estructura y lógica del programa.
* Generación de un "plan de modificación" en lugar de un plan de creación.
* Aplicación de los cambios en el código original.

### Tecnología Involucrada
Técnicas de parsing de código (ej. Abstract Syntax Trees - AST), RAG (Retrieval-Augmented Generation) sobre el código fuente.

### Optimización y Refactorización de Código
Añadir un agente especializado que pueda analizar un programa COBOL y sugerir mejoras.
* Detección de código muerto o inalcanzable.
* Sugerencias de refactorización para mejorar la legibilidad (ej. renombrar variables, extraer párrafos).
* Potencialmente, sugerencias de optimización de rendimiento basadas en patrones conocidos.

### Tecnología Involucrada
Modelos LLM entrenados o fine-tuned en buenas prácticas de COBOL, análisis estático de código.

### Gestión de Proyectos y Control de Versiones
Integrar la herramienta con sistemas de control de versiones para gestionar el código generado.
* Conexión a repositorios Git.
* Capacidad de crear commits con el código nuevo o modificado.
* Visualización de diferencias (diff) entre versiones.
* Asignación de peticiones a "proyectos" o "módulos" específicos dentro de la aplicación.

### Tecnología Involucrada
GitPython (o similar), APIs de plataformas como GitHub/GitLab.
