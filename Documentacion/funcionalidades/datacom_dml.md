# Datacom DML y Áreas

Este documento describe el uso de áreas Datacom (CA Datacom) en el código COBOL generado por el proyecto, el patrón de invocación mediante `DBNTRY`, y el manejo de errores básico que se incorpora en el MVP.

## Objetivos
- Alinear el código generado con estándares empresariales donde Datacom es el gestor de datos.
- Asegurar un manejo de errores mínimo y visible en la ejecución.
- Mantener modularidad y claridad en las secciones COBOL.

## Áreas Datacom
- `RQST-AREA`: Contiene el código de operación, el retorno y metadatos de la llamada.
- `KEY-AREA`: Llave(s) del registro a consultar/actualizar.
- `DATA-AREA`: Buffer con los datos del registro leído/escrito.

Los nombres exactos pueden variar según el estándar de la instalación. En el MVP se usan identificadores genéricos estandarizados.

## Patrón de Uso con `DBNTRY`
```
CALL 'DBNTRY' USING RQST-AREA KEY-AREA DATA-AREA.
IF RQST-RET-CODE NOT = ZERO
    DISPLAY 'ERROR DATACOM: ' RQST-RET-CODE
    GO TO ERROR-HANDLING
END-IF.
```

### Consideraciones
- El retorno en `RQST-RET-CODE` debe ser verificado en cada operación.
- El manejo de error mínimo consiste en mostrar el código y derivar al bloque `ERROR-HANDLING`.
- En escenarios reales, se agregan mapeos de códigos de error y acciones (reintentos, rollback, etc.).

## Ejemplo COBOL Integrado
```
IDENTIFICATION DIVISION.
PROGRAM-ID. PGR001.

DATA DIVISION.
WORKING-STORAGE SECTION.
01  RQST-AREA.
    05  RQST-RET-CODE       PIC 9(4) COMP.
01  KEY-AREA.
    05  KEY-CUSTOMER-ID     PIC 9(9).
01  DATA-AREA.
    05  CUSTOMER-NAME       PIC X(30).

PROCEDURE DIVISION.
MAIN-PROCESS SECTION.
    MOVE 123456789 TO KEY-CUSTOMER-ID.
    CALL 'DBNTRY' USING RQST-AREA KEY-AREA DATA-AREA.
    IF RQST-RET-CODE NOT = ZERO
        DISPLAY 'ERROR DATACOM: ' RQST-RET-CODE
        GO TO ERROR-HANDLING
    END-IF
    PERFORM ESTADISTICA.
    STOP RUN.

ERROR-HANDLING SECTION.
    DISPLAY 'ERROR EN PROCESO PRINCIPAL'.
    STOP RUN.

ESTADISTICA SECTION.
    DISPLAY 'REGISTROS PROCESADOS: 1'.
```

## Validación y Pruebas
- Los stubs de LLM (Gemini) generan automáticamente las áreas y el patrón `DBNTRY`.
- Los tests de integración verifican que el bloque de manejo de error existe y se usa.
- Recomendada la cobertura con `pytest-cov`.

## Futuras Mejoras
- Mapeo de códigos de retorno (`RQST-RET-CODE`) a mensajes de negocio.
- Operaciones DML específicas: GET/PUT/UPDATE/DELETE con códigos Datacom.
- Reintentos y transacciones (COMMIT/ROLLBACK) según política.
