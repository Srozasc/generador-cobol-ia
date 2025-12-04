# Plan de Implementación: Modificación de Reglas de Negocio en COBOL

## 1. Objetivo
Habilitar al **Generador COBOL IA** para recibir un programa COBOL existente y una solicitud de cambio en lenguaje natural, generando una nueva versión del código con las reglas de negocio actualizadas.

### Caso de Uso de Referencia (Golden Path)
**Escenario**: Ajuste de regla de negocio condicional.
**Input**: *"Necesito modificar el programa COBPROG01 para que, si el monto del pago supera los $10.000 y el cliente tiene mora, se envíe una alerta al log y se proceda con la cancelación parcial."*
**Desafío**: El agente debe identificar el punto de inserción correcto, agregar la lógica condicional (`IF/AND`), y generar las llamadas correspondientes (`PERFORM` o `CALL`), asegurando que el resto del flujo se mantenga intacto.

## 2. Análisis del Estado Actual
Actualmente, el sistema soporta modos de **Creación**, **Corrección** y **Documentación**.
Se requiere el modo **Modificación** (`modification`) capaz de entender lógica existente e insertar nueva lógica compleja.

## 3. Arquitectura Propuesta

### 3.1. Actualización del Grafo (`core/graph.py`)
-   **Nuevo Modo**: `modification`.
-   **Flujo**: `START` -> `Planner` -> `Coder` -> `Validator` -> `END`.

### 3.2. Agente Planificador (`agents/planner.py`)
-   **Rol**: Analista de Impacto y Diseño Técnico.
-   **Responsabilidad**:
    1.  Localizar el punto exacto de inserción (ej: párrafo de validación de pagos).
    2.  Identificar variables existentes necesarias (ej: `WS-MONTO-PAGO`, `WS-ESTADO-CLIENTE`).
    3.  Definir nuevas variables si faltan.
    4.  Estructurar la lógica de cambio (pseudo-código o instrucciones precisas).

### 3.3. Agente Codificador (`agents/coder.py`)
-   **Rol**: Desarrollador de Mantenimiento.
-   **Responsabilidad**: Implementar el plan preservando la integridad del código.
-   **Capacidades Críticas**:
    -   Insertar bloques `IF/EVALUATE` complejos.
    -   Agregar llamadas `CALL` o `PERFORM`.
    -   No "alucinar" borrando código no relacionado.

### 3.4. Interfaz de Usuario (`run_prototype.py`)
-   Opción "3. Modificar programa existente".
-   Carga de archivo fuente + Input de solicitud de cambio.

## 4. Estrategia de Prompting Refinada

### 4.1. Prompt del Planificador (Modo Modificación)
```text
Eres un Analista Técnico Senior COBOL.
Tu tarea es analizar un programa existente y planificar los cambios para cumplir un nuevo requerimiento de negocio.

CÓDIGO ACTUAL:
{original_code}

SOLICITUD DE CAMBIO:
{user_request}

TAREA DE ANÁLISIS:
1. **Identificación de Variables**: Busca en DATA DIVISION las variables que corresponden a los conceptos del requerimiento (ej: "monto del pago", "mora"). Si no existen, especifica que deben crearse.
2. **Punto de Inserción**: Identifica en PROCEDURE DIVISION el párrafo o sección lógica donde debe aplicarse la nueva regla.
3. **Lógica de Cambio**: Define la estructura lógica (IF, PERFORM, CALL) necesaria.

GENERA UN PLAN TÉCNICO JSON:
{
  "analysis": "Se identificó WS-IMPORTE como monto y WS-STATUS como estado. El cambio debe ir en PAR-VALIDACION.",
  "steps": [
    "En WORKING-STORAGE: Verificar existencia de variables para log y cancelación.",
    "En PROCEDURE DIVISION (Párrafo XXX): Insertar lógica: SI WS-IMPORTE > 10000 Y WS-STATUS = 'MORA' ENTONCES...",
    "Acción 1: PERFORM RUTINA-LOG-ALERTA (o crearla si no existe)",
    "Acción 2: PERFORM RUTINA-CANCELACION-PARCIAL"
  ]
}
```

### 4.2. Prompt del Codificador (Modo Modificación)
```text
Eres un Desarrollador COBOL experto en mantenimiento.
Implementa los cambios solicitados en el código fuente original.

CÓDIGO ORIGINAL:
{original_code}

PLAN DE CAMBIOS:
{plan}

REGLAS CRÍTICAS:
1. **Preservación**: NO elimines ni modifiques lógica existente a menos que el plan lo pida explícitamente.
2. **Integración**: Inserta la nueva lógica (IF/PERFORM/CALL) en el punto exacto indicado.
3. **Completitud**: Si el plan pide llamar a una rutina (ej: CANCELACION-PARCIAL) y no existe, crea un párrafo stub (esqueleto) al final del programa para evitar errores de compilación.
4. **Formato**: Respeta las márgenes (Área A/B) estrictamente.

SALIDA:
Genera el CÓDIGO COBOL COMPLETO y compilable.
```

## 5. Plan de Trabajo (TDD)

### Fase 1: Agente Planificador (Modo Modificación)
- [ ] 1.1 Crear test: `planner` analiza código y detecta variables para el caso "Monto > 10000 y Mora".
- [ ] 1.2 Actualizar `agents/planner.py` para manejar `original_code` y el nuevo prompt.

### Fase 2: Agente Codificador (Modo Modificación)
- [ ] 2.1 Crear test: `coder` inserta bloque `IF` complejo sin romper el código circundante.
- [ ] 2.2 Actualizar `agents/coder.py` con el nuevo prompt de mantenimiento.

### Fase 3: Integración y CLI
- [ ] 3.1 Actualizar `run_prototype.py` con la opción de menú.
- [ ] 3.2 Implementar flujo `modification` en `core/graph.py`.

## 6. Validación
*Nota: En este entorno prototipo, la validación se limita a sintaxis y estructura correcta del código generado. La validación funcional en mainframe (ej: ejecución de JCL) está fuera del alcance actual, pero el código generado estará listo para ser transferido y probado.*
