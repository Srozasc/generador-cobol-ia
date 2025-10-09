# Reglas del Proyecto - Generador COBOL IA

## Documentación de Referencia
- **Arquitectura:** `Documentacion/inicial/arquitectura.md`
- **Especificaciones:** `Documentacion/inicial/especificacion_de_caracteristicas.md`
- **Estrategia de Versionado:** `Documentacion/inicial/estrategia_versionado.md`

## Metodología de Desarrollo

### Enfoque TDD (Test-Driven Development)
- **OBLIGATORIO:** Escribir tests ANTES de implementar cualquier funcionalidad
- Usar `pytest` como framework de testing principal
- Usar `pytest-mock` para mocking en tests de integración
- Cada componente debe tener tests unitarios completos
- Crear test de integración para el flujo completo del sistema

### Estructura del Proyecto
```
generador_cobol_ia/
├── .venv/                  # Entorno virtual de Python
├── agents/                 # Lógica de los agentes de IA
│   ├── __init__.py
│   ├── planner.py          # Agente Planificador
│   └── coder.py            # Agente Codificador
├── validators/             # Lógica para validación del código
│   ├── __init__.py
│   ├── mock_validator.py   # Validador Simulado (MVP)
│   └── mainframe_validator.py # Validador Real (Futuro)
├── core/                   # Lógica central y orquestación
│   ├── __init__.py
│   └── graph.py            # Grafo de LangGraph
├── tests/                  # Pruebas unitarias e integración
│   ├── __init__.py
│   ├── agents/
│   ├── validators/
│   └── test_integration_flow.py
├── .env                    # Variables de entorno (API Keys)
├── .gitignore
├── requirements.txt
└── run_prototype.py        # Script principal CLI
```

## Tecnologías y Dependencias

### Stack Principal
- **Lenguaje:** Python
- **Framework IA:** LangChain + LangGraph
- **LLM Provider:** LangChain-OpenAI (o Anthropic)
- **Testing:** pytest + pytest-mock
- **Mainframe (Futuro):** py3270

### Configuración de LLM
- **Modelo:** gpt-4-turbo (o equivalente avanzado)
- **Temperatura:** 0.1 (para determinismo)
- **Parser:** StrOutputParser para código, JsonOutputParser para planes

## Funcionalidades MVP (Orden de Implementación)

### 1. Agente Codificador (`agents/coder.py`)
**Responsabilidad:** Convertir plan técnico → código COBOL
- **Entrada:** Diccionario con clave `"plan"` (string)
- **Salida:** String con código COBOL puro (sin explicaciones)
- **Función principal:** `get_coder_chain()`
- **Prompt:** Rol de programador COBOL senior, adherirse al plan
- **Test:** `tests/agents/test_coder.py` - validar "HOLA MUNDO"

### 2. Validador Simulado (`validators/mock_validator.py`)
**Responsabilidad:** Simular validación sin mainframe real
- **Entrada:** String con código COBOL
- **Salida:** Dict con `"status"` ("success"/"error") y `"message"`
- **Lógica:** Buscar palabras clave de error predefinidas
- **Función principal:** `validate_code(code: str) -> dict`
- **Test:** `tests/validators/test_mock_validator.py`

### 3. Agente Planificador (`agents/planner.py`)
**Responsabilidad:** Lenguaje natural → plan técnico estructurado
- **Modo Creación:** `{"request": "..."}` → JSON plan
- **Modo Corrección:** `{"request": "...", "code": "...", "error_message": "..."}` → JSON plan corrección
- **Función principal:** `get_planner_chain()`
- **Salida:** JSON válido siempre
- **Test:** `tests/agents/test_planner.py`

### 4. Orquestador (Grafo) (`core/graph.py`)
**Responsabilidad:** Conectar agentes en flujo con autocorrección
- **Estado:** TypedDict con `request`, `plan`, `code`, `error_message`, `retry_count`
- **Flujo:** START → planner → coder → validator → (END | planner)
- **Arista condicional:** Basada en `status` del validador
- **Test:** `tests/test_integration_flow.py` - ciclo completo con mocks

### 5. CLI Narrativa (`run_prototype.py`)
**Responsabilidad:** Interfaz de usuario descriptiva
- Mensajes de estado ("Planificando...", "Generando código...")
- Mostrar código en cada etapa
- Presentar resultado final

## Reglas de Implementación

### Agentes
- **Aislamiento:** Cada agente debe ser agnóstico a otros componentes
- **Determinismo:** Configuración de temperatura baja
- **Pureza:** Sin efectos secundarios, funciones puras donde sea posible
- **Prompting:** Evitar texto explicativo en salidas, solo código/datos

### Testing
- **Cobertura:** Cada función pública debe tener test
- **Mocking:** Usar mocks para APIs externas y componentes costosos
- **Integración:** Test end-to-end del flujo completo
- **Datos de prueba:** Casos de éxito y error bien definidos

### Estructura de Código
- **Imports:** Usar imports absolutos desde raíz del proyecto
- **Documentación:** Docstrings en funciones principales
- **Configuración:** Variables de entorno en `.env`
- **Dependencias:** Especificar versiones en `requirements.txt`

## Funcionalidades Futuras (Post-MVP)
- Validador real con mainframe (py3270)
- Interfaz web (FastAPI + React/Vue)
- Análisis de código existente
- Optimización y refactorización
- Control de versiones (Git integration)

## Convenciones de Código Python

### Estilo y Formato
- **PEP 8:** Seguir estrictamente las convenciones de estilo de Python
- **Líneas:** Máximo 88 caracteres por línea (compatible con Black)
- **Imports:** Usar imports absolutos desde la raíz del proyecto
- **Orden de imports:** stdlib → third-party → local (separados por línea en blanco)

### Naming Conventions
- **Funciones y variables:** snake_case (`get_planner_chain`, `error_message`)
- **Clases:** PascalCase (`CobolGenerator`, `MockValidator`)
- **Constantes:** UPPER_SNAKE_CASE (`MAX_RETRY_COUNT`, `DEFAULT_TEMPERATURE`)
- **Archivos:** snake_case.py (`mock_validator.py`, `test_integration_flow.py`)
- **Directorios:** snake_case (`agents/`, `validators/`, `tests/`)

### Documentación de Código
- **Docstrings:** Usar formato Google/NumPy para todas las funciones públicas
- **Type hints:** Obligatorio para parámetros y valores de retorno
- **Comentarios:** Solo para lógica compleja, evitar comentarios obvios

```python
def validate_code(code: str) -> dict[str, str]:
    """Valida código COBOL usando el validador simulado.
    
    Args:
        code: Código COBOL a validar
        
    Returns:
        Dict con 'status' ('success'/'error') y 'message'
    """
```

## Configuración de Desarrollo

### Entorno Virtual
- **Obligatorio:** Usar `.venv/` en la raíz del proyecto
- **Python:** Versión 3.11+ requerida
- **Activación:** Documentar comandos en README

### Herramientas de Calidad
- **Black:** Formateo automático de código (línea 88 caracteres)
- **isort:** Ordenamiento automático de imports
- **flake8:** Linting y detección de errores
- **mypy:** Verificación de tipos estática

### Pre-commit Hooks
- Configurar hooks para Black, isort, flake8 antes de cada commit
- Ejecutar tests unitarios en pre-commit
- Validar formato de mensajes de commit

### Variables de Entorno
- **Archivo:** `.env` (nunca commitear)
- **Template:** `.env.example` con valores de ejemplo
- **Carga:** Usar `python-dotenv` para cargar variables
- **Requeridas:** `OPENAI_API_KEY`, `ANTHROPIC_API_KEY` (opcional)

## Convenciones de Git

### Mensajes de Commit
- **Formato:** `tipo(scope): descripción`
- **Tipos:** feat, fix, docs, style, refactor, test, chore
- **Ejemplos:**
  - `feat(agents): implementar agente codificador`
  - `test(validators): agregar tests para mock validator`
  - `fix(core): corregir lógica de retry en grafo`

### Branching Strategy
- **Main:** Rama principal, siempre estable
- **Feature:** `feature/nombre-funcionalidad`
- **Bugfix:** `fix/descripcion-bug`
- **Hotfix:** `hotfix/descripcion-critica`

### Estrategia de Versionado
- **OBLIGATORIO:** Seguir la estrategia definida en `Documentacion/inicial/estrategia_versionado.md`
- **Versionado Semántico:** vMAJOR.MINOR.PATCH
- **Tags:** Crear tags para cada versión estable
- **Releases:** Documentar cada release en GitHub
- **Repositorio:** `https://github.com/Srozasc/generador-cobol-ia.git`

### .gitignore
```
.venv/
.env
__pycache__/
*.pyc
.pytest_cache/
.coverage
.mypy_cache/
*.log
```

## Manejo de Errores y Logging

### Logging Estándar
- **Librería:** `logging` estándar de Python
- **Formato:** `%(asctime)s - %(name)s - %(levelname)s - %(message)s`
- **Niveles por componente:**
  - Agentes: INFO para operaciones principales
  - Validadores: DEBUG para detalles de validación
  - Grafo: INFO para transiciones de estado
  - CLI: INFO para feedback al usuario

### Excepciones Personalizadas
```python
class CobolGeneratorError(Exception):
    """Excepción base del generador COBOL."""
    pass

class ValidationError(CobolGeneratorError):
    """Error en validación de código COBOL."""
    pass

class PlanningError(CobolGeneratorError):
    """Error en planificación de código."""
    pass
```

### Manejo de Errores de API
- **Retry:** Implementar retry automático para APIs (max 3 intentos)
- **Timeout:** Configurar timeouts apropiados (30s para LLM)
- **Fallback:** Tener estrategias de fallback para fallos de API

## Convenciones Específicas del Dominio COBOL

### Formato de Código COBOL Generado
- **Mayúsculas:** Todo el código COBOL en MAYÚSCULAS
- **Indentación:** 4 espacios para niveles de datos, 8 espacios para procedimientos
- **Columnas:** Respetar formato de columnas COBOL (1-6 números, 7 indicador, 8-72 código)

### Convenciones de Nombres COBOL
- **Programas:** Máximo 8 caracteres, formato `PROG001`, `UTIL001`
- **Variables:** Descriptivas, formato `WS-CONTADOR`, `WS-NOMBRE-CLIENTE`
- **Secciones:** `MAIN-PROCESS`, `ERROR-HANDLING`, `FILE-OPERATIONS`

### Validación de Sintaxis
- **Palabras reservadas:** Validar uso correcto de COBOL keywords
- **Estructura:** IDENTIFICATION DIVISION, ENVIRONMENT DIVISION, DATA DIVISION, PROCEDURE DIVISION
- **Terminadores:** Verificar puntos y comas correctos

### Estándares de Código COBOL
```cobol
IDENTIFICATION DIVISION.
PROGRAM-ID. PROG001.

DATA DIVISION.
WORKING-STORAGE SECTION.
01  WS-CONTADOR          PIC 9(3) VALUE ZERO.
01  WS-MENSAJE           PIC X(50) VALUE SPACES.

PROCEDURE DIVISION.
MAIN-PROCESS.
    DISPLAY 'HOLA MUNDO'.
    STOP RUN.
```

## Estándares de Calidad y Documentación

### Cobertura de Tests
- **Mínimo:** 90% de cobertura de código
- **Crítico:** 100% para funciones de validación y generación
- **Herramienta:** `pytest-cov` para medición

### Datos de Prueba
- **Ubicación:** `tests/fixtures/` para datos de prueba
- **Formato:** JSON para planes, archivos .cbl para código COBOL
- **Casos:** Incluir casos de éxito, error y edge cases

### Documentación de Casos de Uso
- **Ejemplos:** Mantener ejemplos actualizados en documentación
- **Escenarios:** Documentar escenarios complejos y sus soluciones
- **API:** Documentar interfaces de agentes y validadores

### Performance
- **Tiempo de respuesta:** < 30 segundos para generación completa
- **Memoria:** Monitorear uso de memoria en tests de integración
- **Concurrencia:** Preparar para múltiples requests simultáneos

## Notas Importantes
- **Prioridad:** MVP primero, funcionalidades futuras después
- **Calidad:** Código limpio y bien testeado sobre velocidad
- **Documentación:** Mantener documentos de arquitectura actualizados
- **Seguridad:** No exponer API keys en código, usar variables de entorno
- **Consistencia:** Seguir estas convenciones en todo el proyecto
- **Versionado:** SIEMPRE seguir la estrategia definida en `Documentacion/inicial/estrategia_versionado.md`
- **Revisión:** Revisar y actualizar convenciones según evolución del proyecto