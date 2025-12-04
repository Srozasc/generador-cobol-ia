---
description: Genera la documentación inicial (Arquitectura, Especificaciones, Plan de Acción) a partir de un requerimiento.
---

1. **Obtener Requerimientos**: Asegúrate de tener una definición clara o requerimiento del proyecto por parte del usuario. Si no la tienes, pídela.

2. **Crear Directorio**: Crea el directorio `Documentacion/inicial/` si no existe.

3. **Generar Arquitectura**:
   Genera el archivo `Documentacion/inicial/arquitectura.md` utilizando la siguiente plantilla. Debes actuar como el rol descrito y procesar el requerimiento del usuario.

   **Plantilla para Arquitectura:**
   """
   <goal>
   Quiero que me ayudes a idear la estructura general de mi aplicación. Deberías actuar como un ingeniero de Software Senior con amplia experiencia desarrollando y diseñando la arquitectura de aplicaciones web a gran escala. Deberías hacerme preguntas de seguimiento si consideras que es necesario para tener una visión más completa.

   Para lograr esto, toma el Contexto de abajo considerando:
   Qué estoy intentando construir (QUÉ)
   Para quién lo estoy construyendo (QUIÉN)
   Qué problemas resuelve (POR QUÉ)
   En qué se diferencia del estado actual de las cosas (CÓMO)
   Cualquier otro detalle que te proporcione
   </goal>

   <format>
   Devuelve tu respuesta en formato Markdown, sin texto introductorio ni conclusiones.
   </format>

   ## Funcionalidades de Lanzamiento (MVP)
   ### Nombre de la Funcionalidad
   "Resumen contundente" de 2-3 frases explicando qué es o qué hace la funcionalidad
   * Lista
   * De
   * Requisitos
   * O funciones principales
   ### Tecnología Involucrada
   "Tecnologías principales utilizadas en la funcionalidad
   ### Requisitos Principales
   * Cualquier
   * Requisito
   * De la funcionalidad

   ## Funcionalidades Futuras (Post MVP)
   ### Nombre de la Funcionalidad
   * Lista
   * De
   * Requisitos
   * O funciones principales
   ### Tecnología Involucrada
   """

4. **Generar Especificación de Características**:
   Genera el archivo `Documentacion/inicial/especificacion_caracteristicas.md` utilizando la siguiente plantilla. Usa el requerimiento original y la arquitectura generada como contexto.

   **Plantilla para Especificaciones:**
   """
   <goal>
   Eres un ingeniero de software veterano en la industria, responsable de desarrollar funcionalidades de alto impacto para las mayores empresas SaaS del mundo al estilo FANG. Eres excelente creando especificaciones técnicas detalladas para funcionalidades, y entendiendo cómo se conectan e interrelacionan entre sí.

   Debes revisar el <context> que aparece a continuación y usarlo para generar un documento de especificaciones de funcionalidades completo, sin dejar ningún detalle fuera.

   NO ESCRIBAS CÓDIGO EN ESTA RESPUESTA, A MENOS QUE SEA PSEUDOCÓDIGO PARA UNA SITUACIÓN TÉCNICA
   </goal>

   <format>
   Estructura tu salida de la siguiente manera:

   ## Sistema de Archivos
   Estructura de carpetas y archivos tanto para el repositorio del frontend como del backend

   ## Especificaciones de Funcionalidades
   ### Funcionalidad N
   Objetivo de la funcionalidad
   Relaciones con APIs
   Requisitos detallados de la funcionalidad
   Guía detallada de implementación

   ### Funcionalidad N+1
   Objetivo de la funcionalidad
   Relaciones con APIs
   Requisitos detallados de la funcionalidad
   Guía detallada de implementación
   </format>

   <warnings-and-guidelines>
   * <warning-1>No omitas ningún paso. Esta salida debe ser absolutamente paso a paso y permitir que cualquier persona que la reciba sepa exactamente qué construir y cómo hacerlo</warning-1>
   * <warning-2>No es una etapa para escribir código. Solo se acepta pseudocódigo si es estrictamente necesario para mostrar al lector/desarrollador...
   </warnings-and-guidelines>
   """

5. **Generar Plan de Acción**:
   Genera el archivo `Documentacion/inicial/plan_accion.md` utilizando la siguiente plantilla. Usa todo el contexto anterior.

   **Plantilla para Plan de Acción:**
   """
   <goal>
   Eres un product manager altamente experimentado que ha desplegado software de primer nivel para empresas SaaS al estilo FANG. Sobresales en tomar sistemas complejos y descomponerlos en tareas individuales manejables.

   Debes crear un plan de acción extremadamente detallado, paso por paso.

   Este plan será enviado a un equipo de desarrolladores para su implementación, por lo que debes ser riguroso en tus estándares y no dejar ningún detalle sin tratar.
   </goal>

   <format>
   Escribe tu resultado en formato Markdown.

   ## Nombre de la Tarea
   ### Paso N. Nombre del Paso N
   #### Explicación técnica detallada de lo que estamos logrando en este paso
   ##### Desglose de Tareas
   ###### Nombre de la SubTarea N
   * Descripción del cambio de la SubTarea N
   * ruta/relativa/del/archivo/modificado
   * Operación realizada (Crear, Actualizar, Eliminar)

   ###### Nombre de la SubTarea N+1
   * Descripción del cambio de la SubTarea N+1
   * ruta/relativa/del/archivo/modificado
   * Operación realizada (Crear, Actualizar, Eliminar)

   #### Otros Comentarios del Paso N. Nombre del Paso N
   * Cualquier otra tarea crítica de la que dependa este paso
   * Cualquier tarea manual crítica que el usuario deba realizar para completar este paso
   </format>

   <warnings-and-guidelines>
   Puedes modificar múltiples archivos según sea necesario como parte de tu plan.

   Debes dar instrucciones al usuario para cualquier acción que requiera intervención manual (por ejemplo, iniciar sesión en Firebase) para obtener información de configuración.
   </warnings-and-guidelines>
   """
