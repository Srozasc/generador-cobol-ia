# Documentación Técnica: SUPPGNF6

## Información General
- **Program ID**: SUPPGNF6
- **Sistema**: GENERACION DE INFOME DE PROCESO SEGMENTAC
- **Subsistema**: SUP
- **Autor**: JGM
- **Fecha**: NOV-2014
- **Descripción**: Programa para la generación de informes relacionados con el proceso de segmentación de provisiones.

## Archivos y Datos

### Archivos de Entrada
- **TABUSR**: Archivo de tabla de usuarios/ejecutivos.
  - **Estructura (REG-STAB)**: Contiene códigos de tipo de tabla, usuario, vigencia, fecha, ubicación, número de usuario, descripción, abreviatura, códigos de oficina, agencia, banco, regla, plataforma, negocio, tipo de ejecutivo y sus respectivas glosas/descripciones. Los campos `STAB-GLS-FIxx` son separadores.
- **ENTCLI**: Archivo de entrada de información de clientes.
  - **Estructura (REG-INF-CLI)**: Contiene fecha de proceso, RUT, CIC de cliente, código de calificación, indicador de tarjeta de débito/crédito, código de banco, indicador de tipo de banco, segmentación antigua y nueva, valores máximos, deuda total (D00, FAC, WOL, MES), promedio de deuda mensual (6 meses), glosa de segmentación y meses de período. Los campos `SCLI-GLS-xx` son separadores.
- **SGCDBC**: Archivo de entrada de segmentación de clientes.
  - **Estructura (REG-SSGC)**: Contiene fecha de proceso, RUT, verificador de RUT, CIC de cliente, código de banco, indicador de tipo de cliente, código de ejecutivo, código de oficina, código de sector, fechas de inicio y término de proceso, código de origen de registro, apellidos y nombre del cliente. Incluye una subestructura `REG-CAL-SDBC` con fecha de calificación, código de banco y código SBIF. Los campos `SDBC-GLS-xx` son separadores.
- **ENTD0P**: Archivo de entrada de operaciones D00.
  - **Estructura**: Definida por el copybook `SUPBRD0G`. Contiene datos detallados de operaciones, incluyendo RUT, fechas, sistemas, tipos de cartera, estados, códigos de proceso, NIID, tipos de operación, indicadores de estado, fechas de foto, tipos de crédito, cuentas contables, fechas de inicio de mora, origen de registro, valores de saldo, IPCV, reevaluación y monto de operación.

### Archivos de Salida
- **INFD00**: Archivo de informe de operaciones D00.
  - **Estructura (REG-INF-D00)**: Contiene fecha de proceso, fecha de período, macro sistema, tipo y estado de cartera, código de clasificación, código de proceso, código de sistema, NIID, tipo de operación, indicador de estado, fecha de foto, tipo de crédito, cuenta contable, fecha de inicio de mora, origen de registro, dos valores de saldo (`ID00-VAL-SCON-01`, `ID00-VAL-SCON-02`), IPCV, reevaluación, monto de operación, indicador de tarjeta de débito/crédito de operación y de cliente. Los campos `ID00-GLS-xxx` son separadores.
- **INFCOM**: Archivo de informe consolidado de clientes.
  - **Estructura (REG-INF-COM)**: Contiene códigos de banco, oficina, plataforma y origen de registro del ejecutivo, código de ejecutivo, fecha de proceso, CIC de cliente, RUT y verificador de RUT, apellidos y nombre del cliente, código de calificación, código de clasificación, deuda total promedio, calificación total promedio, deuda promedio mensual, calificación promedio mensual, código de tarjeta de débito/crédito, fecha de segmentación e indicador de alerta. Los campos `ICOM-GLS-xx` son separadores.
- **INFOPE**: Archivo de informe de operaciones segmentadas.
  - **Estructura (REG-INF-OPE)**: Contiene código de sistema, CIC de operación/cliente, RUT y código de segmentación.
- **INFCLI**: Archivo de informe de clientes segmentados.
  - **Estructura (REG-SCC)**: Contiene RUT, CIC de cliente, código de banco, número de meses, valor máximo, deuda total y código de segmentación. Los campos `SCC-GLS-xx` son separadores.
- **CTRCLI**: Archivo de control de clientes.
  - **Estructura (REG-CTRC)**: Contiene período (fecha), número de registros procesados y seis contadores de totales de clientes (`CTRC-TOT-CLI-1` a `CTRC-TOT-CLI-6`).

### Variables Principales
- **WS-STATUS-XXXX**: Variables `PIC 9(02)` para almacenar el estado de los archivos (File Status).
- **WR-ENT-XXXX**: Flags `PIC X(01)` ('1': primer registro, '2': siguiente, '3': fin de archivo) para controlar el estado de lectura de los archivos de entrada.
- **TABLA-USR**: Tabla en memoria (`OCCURS 30000 TIMES`) para almacenar datos de usuarios/ejecutivos (`TUSR-COD-USER`, `TUSR-COD-TBAN`, `TUSR-COD-OFIC`, `TUSR-COD-PLAT`, `TUSR-COD-REGL`).
- **WI-TOP, WI-USR**: Contadores `PIC 9(06)` para la gestión de la tabla `TABLA-USR`.
- **WSS-NUM-LD00, WSS-NUM-LSGC, WSS-NUM-LSGM, WSS-NUM-LUSR**: Contadores `PIC 9(08)` de registros leídos de los archivos de entrada.
- **WSS-GRB-ID00, WSS-GRB-ICOM, WSS-GRB-IOPE, WSS-INF-GCLI**: Contadores `PIC 9(08)` de registros grabados en los archivos de salida.
- **WSS-NUM-EDBC**: Contador `PIC 9(08)` de clientes no encontrados en `SGCDBC`.
- **WSS-OPE-COM**: Contador `PIC 9(08)` de operaciones de tipo 'COM'.
- **REG-XDBC (primera definición)**: Almacena temporalmente datos de `SGCDBC` para el cliente actual.
- **REG-XDBC (segunda definición, `XSGM-` campos)**: Almacena temporalmente datos de segmentación de `ENTCLI` para el cliente actual.
- **PXX-VAR**: Almacena RUT y verificador del registro `ENTD0P` actual para comparaciones.
- **COB-VAR**: Almacena RUT y verificador del cliente en procesamiento, junto con flags de existencia en `SGCDBC` y `ENTCLI`.
- **VAR-PARAME**: Almacena las fechas de período y proceso (`PAR-FEC-FPER`, `PAR-FEC-FPRO`).
- **WCC-VAR**: Constantes utilizadas en la lógica del programa (ej. `CC-COM`, `CC-N`, `CC-S`).

## Lógica Principal

### Flujo de Ejecución
1.  **INI-MAIN**: Punto de entrada principal.
    *   Llama a `OPEN-FILES-INP` para abrir los archivos de entrada.
    *   Llama a `OPEN-FILES-OUT` para abrir los archivos de salida.
    *   Llama a `LEE-TAB-USR` para cargar la tabla de usuarios/ejecutivos en memoria.
    *   Llama a `PROC-REG-ENT` para iniciar el procesamiento principal de los registros.
    *   Llama a `PUT-REG-CTR` para grabar el registro de control final.
    *   Llama a `ESTADISTICA` para mostrar un resumen del proceso.
    *   Llama a `CLOSE-FILES` para cerrar todos los archivos.
    *   Finaliza el programa (`GOBACK`).

### Secciones y Párrafos Principales
-   **OPEN-FILES-INP**: Abre los archivos de entrada (`SGCDBC`, `ENTD0P`, `ENTCLI`, `TABUSR`) en modo `INPUT`. Inicializa los flags de estado de lectura.
-   **OPEN-FILES-OUT**: Abre los archivos de salida (`INFD00`, `INFCOM`, `INFOPE`, `INFCLI`, `CTRCLI`) en modo `OUTPUT`.
-   **LEE-TAB-USR**: Lee secuencialmente el archivo `TABUSR` y carga los datos relevantes de cada registro en la tabla `TABLA-USR` en `WORKING-STORAGE`. Muestra un mensaje de error si la tabla excede 30000 entradas.
-   **PROC-REG-ENT**: Controla el flujo principal de procesamiento de registros.
    *   Lee el primer registro de `ENTD0P` y `SGCDBC`.
    *   Inicializa variables de cliente (`COB-VAR`) con datos del primer registro de `ENTD0P`.
    *   Itera a través de los registros de `ENTD0P` (bucle `LUP-PROC-REG-ENT`).
        *   Si el RUT del registro `ENTD0P` actual es diferente al RUT del cliente en procesamiento (`COB-NUM-RUTD`), significa que se ha terminado de procesar un cliente. Se llama a `PUT-INF-X-CLI` para grabar la información consolidada del cliente anterior y se actualizan las variables de cliente (`COB-VAR`) con el nuevo RUT.
        *   Si el tipo de cartera (`D0P-TIP-CART`) es 'COM', incrementa un contador y llama a `PUT-SEGMEN-OPE`.
        *   Llama a `PUT-INF-X-OPE` para grabar el registro de operación D00.
        *   Lee el siguiente registro de `ENTD0P`.
    *   Al finalizar el archivo `ENTD0P`, llama a `PUT-INF-X-CLI` para procesar el último cliente.
-   **MOV-DAT-COB**: Mueve el RUT y verificador del registro `ENTD0P` actual a `COB-VAR` y las fechas de proceso y período a `VAR-PARAME`.
-   **PUT-INF-X-OPE**: Prepara y escribe un registro en el archivo de salida `INFD00` utilizando datos del registro `ENTD0P` y `XSGM-IND-CDET`. Calcula dos valores de saldo.
-   **PUT-INF-X-CLI**: Prepara y escribe un registro en el archivo de salida `INFCOM`.
    *   Llama a `BUS-REG-SGCDBC` para buscar información adicional del cliente en `SGCDBC`.
    *   Llama a `BUS-REG-ENTCLI` para buscar información de segmentación del cliente en `ENTCLI`.
    *   Llama a `MOV-FIL-INFCOM` para inicializar los separadores del registro de salida.
    *   Mueve datos de `XDBC`, `D0P`, `COB` y `XSGM` al registro `REG-INF-COM` y lo escribe.
-   **PUT-SEGMEN-OPE**: Prepara y escribe un registro en el archivo de salida `INFOPE` con datos de la operación D00.
-   **BUS-REG-SGCDBC**: Busca en el archivo `SGCDBC` el registro correspondiente al RUT del cliente actual (`COB-NUM-RUTD`). Si lo encuentra, carga los datos en `REG-XDBC` y establece un flag.
-   **BUS-REG-ENTCLI**: Busca en el archivo `ENTCLI` el registro correspondiente al RUT del cliente actual (`COB-NUM-RUTD`). Si lo encuentra, carga los datos de segmentación en `XSGM-` y, si `WSS-OPE-COM` es mayor que 0, llama a `PUT-SEGMEN-CLI`.
-   **PUT-SEGMEN-CLI**: Prepara y escribe un registro en el archivo de salida `INFCLI` con datos de segmentación del cliente.
-   **BUS-COD-EJC**: Busca en la tabla `TABLA-USR` en memoria el código de ejecutivo (`XDBC-COD-EJEC`) y, si lo encuentra, mueve los datos asociados (banco, oficina, regla, plataforma) al registro `REG-INF-COM`.
-   **PUT-REG-CTR**: Prepara y escribe un registro de control final en el archivo `CTRCLI`, incluyendo la fecha de proceso y el total de clientes segmentados.
-   **LEER-ENTD0P, LEER-ENTCLI, LEER-SGCDBC, LEER-TABUSR**: Secciones genéricas para leer un registro de cada archivo de entrada, actualizar contadores y establecer el flag de fin de archivo.
-   **MOV-FIL-INFD00, MOV-FIL-INFCOM**: Inicializan los campos separadores (GLS-XX) en los registros de salida `REG-INF-D00` y `REG-INF-COM` con el carácter '|'.
-   **ESTADISTICA**: Muestra en la consola un resumen de la ejecución del programa, incluyendo fechas de proceso y período, y contadores de registros leídos y grabados.
-   **CLOSE-FILES**: Cierra todos los archivos de entrada y salida.

### Validaciones y Controles
-   **Control de Apertura de Archivos**: Verifica el `FILE STATUS` después de cada `OPEN`. Si es mayor que 0, muestra un mensaje de error y aborta el programa (`PERFORM GNS-PRO-ABT`).
-   **Control de Escritura de Archivos**: Verifica el `FILE STATUS` después de cada `WRITE`. Si es mayor que 0 (o diferente de 00 para `INFCLI`), muestra un mensaje de error y aborta el programa (`PERFORM GNS-PRO-ABT`).
-   **Control de Fin de Archivo**: Utiliza flags `WR-ENT-XXXX` para detectar el fin de los archivos de entrada y controlar los bucles de lectura.
-   **Control de Tamaño de Tabla**: En `LEE-TAB-USR`, verifica que el número de entradas en `TABLA-USR` no exceda 30000. Si lo hace, aborta el programa.
-   **Validación de Archivo Vacío**: Si `ENTD0P` o `TABUSR` están vacíos al inicio, el programa muestra un mensaje y termina el procesamiento principal o la carga de la tabla.
-   **Comparación de RUT**: La lógica principal en `PROC-REG-ENT` y las búsquedas en `BUS-REG-SGCDBC` y `BUS-REG-ENTCLI` se basan en la comparación del RUT para agrupar y procesar la información por cliente.

## Dependencias
-   **Copybooks**:
    -   `SUPBRD0G`: Define la estructura del registro para el archivo `ENTD0P`.
    -   `GNSWCFIO`: No especificado, probablemente contiene definiciones de variables de control o constantes.
    -   `GNSWVFIO`: No especificado, probablemente contiene definiciones de variables de control o constantes.
    -   `GNSBTABT`: No especificado, probablemente parte de la librería de utilidades `GNS`.
    -   `GNSBGABT`: No especificado, probablemente parte de la librería de utilidades `GNS`.
    -   `GNSBGEND`: No especificado, probablemente parte de la librería de utilidades `GNS`.
-   **Programas Llamados**:
    -   `GNS-PRO-ABT`: Programa de utilidad llamado en caso de errores críticos (ej. errores de I/O) para abortar la ejecución.
-   **Acceso a Datos**:
    -   Acceso a archivos secuenciales (VSAM o QSAM) para todos los archivos de entrada y salida. No se detecta acceso directo a bases de datos (DB2, Datacom, etc.) en el código proporcionado.

## Notas Técnicas
-   El programa utiliza un patrón de procesamiento de "control de corte" basado en el RUT del cliente para consolidar información de múltiples archivos de entrada antes de generar los registros de salida.
-   La estructura `REG-XDBC` aparece dos veces en `WORKING-STORAGE SECTION` con diferentes conjuntos de campos. Esto es un error de sintaxis COBOL o una redefinición implícita. Se ha interpretado la segunda aparición como una estructura lógica separada para datos de segmentación (`XSGM-`).
-   Los campos `GLS-FIxx` y `GLS-xx` en las estructuras de registro se utilizan como separadores de campo, lo que sugiere un formato de archivo delimitado (ej. CSV con '|' como delimitador).
-   La carga de `TABUSR` en una tabla en memoria (`TABLA-USR`) indica que este archivo es relativamente pequeño y se utiliza para búsquedas rápidas durante el procesamiento.
-   El programa muestra mensajes de progreso y estadísticas en la consola, lo cual es útil para el monitoreo de la ejecución por parte del operador.