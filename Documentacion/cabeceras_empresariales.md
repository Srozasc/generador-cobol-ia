# Cabeceras Empresariales COBOL - Documentación Técnica

## Descripción General

El sistema de **Cabeceras Empresariales** es una funcionalidad implementada en el Generador COBOL IA que garantiza que todos los programas COBOL generados incluyan cabeceras empresariales completas y estandarizadas, siguiendo las mejores prácticas de desarrollo en entornos mainframe bancarios.

## Características Principales

### 🎯 **Generación Automática**
- **Inferencia inteligente**: El sistema analiza el contexto del request del usuario para inferir automáticamente información relevante
- **Información dinámica**: Genera fechas actuales, sistemas, subsistemas y objetivos basados en el contexto
- **Formato estándar**: Mantiene consistencia con las convenciones empresariales bancarias

### 📋 **Elementos de la Cabecera**
Cada cabecera empresarial incluye obligatoriamente:

1. **IDENTIFICATION DIVISION** con formato empresarial
2. **PROGRAM-ID** inferido del contexto o generado automáticamente
3. **AUTHOR** estandarizado como "SISTEMA GENERADOR COBOL IA"
4. **DATE-WRITTEN** con fecha actual en formato DD/MM/YYYY
5. **Sección de información del sistema** con:
   - SISTEMA: Descripción del sistema basada en el contexto
   - SUBSISTEMA: Inferido del tipo de programa
   - OBJETIVOS: Extraídos del request del usuario
6. **Sección de mantenciones** con entrada inicial automática

## Formato de Cabecera Estándar

```cobol
       IDENTIFICATION DIVISION.
      *************************
       PROGRAM-ID.    PROG001.
       AUTHOR.        SISTEMA GENERADOR COBOL IA.
       DATE-WRITTEN.  ENE-2025.
      *****************************************************************
      * SISTEMA   : PROCESAMIENTO BANCARIO EMPRESARIAL               *
      * SUBSISTEMA: BANCARIO                                          *
      * OBJETIVOS : PROCESAR TRANSACCIONES BANCARIAS                 *
      *****************************************************************
      *                  M A N T E N C I O N E S                      *
      * FECHA      RESPONSABLE MOTIVO                                 *
      * 15/12/2024 COBOL-IA    GENERACION INICIAL DEL PROGRAMA       *
      *****************************************************************
```

## Lógica de Inferencia

### 🔍 **Inferencia de Sistema**
El sistema analiza el contexto del request para determinar el tipo de sistema:

| Palabras Clave en Request | Sistema Inferido |
|---------------------------|------------------|
| "bancario", "banco", "transacciones" | PROCESAMIENTO BANCARIO EMPRESARIAL |
| "provisiones", "segmentación" | SISTEMA DE PROVISIONES Y SEGMENTACION |
| "interfaz", "archivo" | GENERACION DE INTERFACES DE DATOS |
| "validación", "control" | SISTEMA DE VALIDACIONES Y CONTROLES |
| Por defecto | SISTEMA DE PROCESAMIENTO EMPRESARIAL |

### 🏗️ **Inferencia de Subsistema**
Basado en el nombre del programa o tipo de funcionalidad:

| Patrón del Programa | Subsistema |
|---------------------|------------|
| Programas que empiecen con "SUP" | SUP |
| Programas bancarios | BANCARIO |
| Programas de validación | VALIDACIONES |
| Por defecto | GENERAL |

### 🎯 **Extracción de Objetivos**
- Analiza el request del usuario para extraer el propósito principal
- Limita a máximo 50 caracteres para mantener formato
- Usa patrones de reconocimiento para identificar verbos de acción y objetos

## Implementación Técnica

### 📁 **Archivos Modificados**

#### `agents/coder.py`
- **Funciones auxiliares agregadas**:
  - `_get_current_date_formatted()`: Genera fecha actual en formato DD/MM/YYYY
  - `_infer_system_from_request()`: Infiere sistema basado en contexto
  - `_infer_subsystem_from_program()`: Infiere subsistema del nombre de programa
  - `_extract_objectives_from_request()`: Extrae objetivos del request
  - `_generate_enterprise_header()`: Genera cabecera completa

- **Modificaciones al prompt**:
  - Prompt del sistema actualizado con instrucciones explícitas sobre cabeceras
  - Prompt humano enriquecido con información dinámica
  - Función `enrich_context()` para inyectar datos dinámicos

## Requisitos de Formato y Modularidad

- Etiqueta de mantenimiento: usar `MANTENCIONES` (formato en español) en todas las cabeceras. Sustituye `MAINTENANCE` donde aplique.
- Estructura modular obligatoria:
  - `MAIN-PROCESS SECTION.` como sección principal del flujo
  - `ESTADISTICA SECTION.` para reporte y métricas del proceso
  - `PERFORM ESTADISTICA` desde el flujo principal para mantener separación de responsabilidades
- Integración con Datacom DML: cuando aplique, usar patrón `CALL 'DBNTRY'` con verificación de retorno y desvío a `ERROR-HANDLING` ante códigos no cero. Ver guía: `Documentacion/funcionalidades/datacom_dml.md`.

### 🧪 **Tests Implementados**

#### `tests/agents/test_enterprise_headers.py`
Suite completa de tests que valida:

1. **`test_current_date_formatting`**: Formato correcto de fecha
2. **`test_system_inference_from_request`**: Inferencia de sistema
3. **`test_subsystem_inference_from_program`**: Inferencia de subsistema
4. **`test_objectives_extraction_from_request`**: Extracción de objetivos
5. **`test_enterprise_header_generation`**: Generación completa de cabecera
6. **`test_enterprise_header_in_generated_code`**: Inclusión en código generado
7. **`test_different_program_types_generate_appropriate_headers`**: Diferentes tipos de programas
8. **`test_header_format_compliance`**: Cumplimiento de formato

## Ejemplos de Uso

### 📝 **Ejemplo 1: Programa Bancario**

**Request del usuario:**
```
"Crear un programa bancario para procesar transacciones de clientes"
```

**Cabecera generada:**
```cobol
       IDENTIFICATION DIVISION.
      *************************
       PROGRAM-ID.    PROG001.
       AUTHOR.        SISTEMA GENERADOR COBOL IA.
       DATE-WRITTEN.  15/12/2024.
      *****************************************************************
      * SISTEMA   : PROCESAMIENTO BANCARIO EMPRESARIAL               *
      * SUBSISTEMA: BANCARIO                                          *
      * OBJETIVOS : PROCESAR TRANSACCIONES DE CLIENTES               *
      *****************************************************************
      *                  M A N T E N C I O N E S                      *
      * FECHA      RESPONSABLE MOTIVO                                 *
      * 15/12/2024 COBOL-IA    GENERACION INICIAL DEL PROGRAMA       *
      *****************************************************************
```

### 📝 **Ejemplo 2: Programa de Validación**

**Request del usuario:**
```
"Generar programa de validación de archivos de entrada"
```

**Cabecera generada:**
```cobol
       IDENTIFICATION DIVISION.
      *************************
       PROGRAM-ID.    PROG001.
       AUTHOR.        SISTEMA GENERADOR COBOL IA.
       DATE-WRITTEN.  15/12/2024.
      *****************************************************************
      * SISTEMA   : SISTEMA DE VALIDACIONES Y CONTROLES              *
      * SUBSISTEMA: VALIDACIONES                                      *
      * OBJETIVOS : VALIDAR ARCHIVOS DE ENTRADA                      *
      *****************************************************************
      *                  M A N T E N C I O N E S                      *
      * FECHA      RESPONSABLE MOTIVO                                 *
      * 15/12/2024 COBOL-IA    GENERACION INICIAL DEL PROGRAMA       *
      *****************************************************************
```

## Beneficios

### ✅ **Para el Desarrollo**
- **Consistencia**: Todos los programas siguen el mismo estándar empresarial
- **Trazabilidad**: Información clara sobre origen, fecha y propósito
- **Mantenibilidad**: Sección de mantenciones preparada para futuras modificaciones
- **Cumplimiento**: Adherencia a estándares bancarios y empresariales

### ✅ **Para el Negocio**
- **Profesionalismo**: Código que cumple con estándares empresariales
- **Auditoría**: Información completa para procesos de auditoría
- **Documentación**: Auto-documentación del propósito y contexto
- **Escalabilidad**: Preparado para entornos de producción

## Configuración y Personalización

### ⚙️ **Variables de Entorno**
Utiliza las mismas variables del sistema principal:
- `GOOGLE_API_KEY`: Para acceso a Gemini (Google AI Studio)
- `LLM_MODEL`: Modelo por defecto `gemini-1.5-flash`
- `LLM_TEMPERATURE`: Temperatura del modelo (por defecto: 0.1)

Además, la suite de tests emplea un stub determinista de LLM en `tests/conftest.py` para garantizar reproducibilidad.

### 🔧 **Personalización**
Para personalizar la lógica de inferencia, modificar las funciones en `agents/coder.py`:
- `_infer_system_from_request()`: Agregar nuevos patrones de sistema
- `_infer_subsystem_from_program()`: Modificar lógica de subsistemas
- `_extract_objectives_from_request()`: Ajustar extracción de objetivos

## Versionado y Compatibilidad

### 📋 **Versión Actual**: v1.0.0
- **Compatibilidad**: Compatible con todas las versiones del Generador COBOL IA
- **Retrocompatibilidad**: No afecta código existente, solo mejora nuevas generaciones
- **Dependencias**: Requiere Python 3.11+ y dependencias del proyecto principal

### 🔄 **Futuras Mejoras**
- Soporte para múltiples formatos de cabecera según cliente
- Integración con sistemas de control de versiones
- Personalización de plantillas por tipo de proyecto
- Análisis más avanzado de contexto usando NLP

## Troubleshooting

### ❗ **Problemas Comunes**

#### **Cabecera no se genera**
- **Causa**: Prompt del sistema no está siendo seguido por el LLM
- **Solución**: Verificar configuración del modelo y temperatura

#### **Información incorrecta en cabecera**
- **Causa**: Lógica de inferencia no reconoce el contexto
- **Solución**: Revisar y ajustar patrones en funciones de inferencia

#### **Formato incorrecto**
- **Causa**: Cambios en el prompt o template
- **Solución**: Verificar que el formato en el prompt del sistema sea correcto

### 🔍 **Debugging**
Para debuggear problemas:
1. Ejecutar tests específicos: `pytest tests/agents/test_enterprise_headers.py -v`
2. Revisar logs del LLM para ver si sigue las instrucciones
3. Verificar que la función `enrich_context()` esté pasando datos correctos

## Conclusión

La funcionalidad de **Cabeceras Empresariales** eleva significativamente la calidad y profesionalismo del código COBOL generado, asegurando que cada programa cumpla con los estándares empresariales más exigentes del sector bancario y financiero.

Esta implementación demuestra el compromiso del Generador COBOL IA con la excelencia técnica y la adherencia a las mejores prácticas de la industria.
