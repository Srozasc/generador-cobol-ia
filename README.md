# 🚀 Generador COBOL IA

**Generador inteligente de código COBOL usando IA avanzada con LangChain y LangGraph**

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://python.org)
[![LangChain](https://img.shields.io/badge/LangChain-Latest-green.svg)](https://langchain.com)
[![Tests](https://img.shields.io/badge/Tests-51%20Passed-brightgreen.svg)](./tests/)
[![Coverage](https://img.shields.io/badge/Coverage-95%25-brightgreen.svg)](./tests/)

## 📋 Descripción

El **Generador COBOL IA** es una herramienta avanzada que utiliza inteligencia artificial para generar código COBOL de alta calidad a partir de descripciones en lenguaje natural. Implementa un sistema de agentes especializados con capacidades de autocorrección y validación automática.

## ✨ Funcionalidades Principales

### 🤖 Agentes de IA Especializados
- **Agente Planificador**: Convierte lenguaje natural en planes técnicos estructurados
- **Agente Codificador**: Genera código COBOL de alta calidad siguiendo estándares empresariales
- **Sistema de Autocorrección**: Ciclo automático de validación y corrección de errores

### 🏢 Cabeceras Empresariales Automáticas *(Nuevo)*
- **Generación automática** de cabeceras COBOL estandarizadas
- **Inferencia inteligente** de sistema y subsistema basada en contexto
- **Información dinámica**: Fecha, autor, objetivos y mantenimiento
- **Formato empresarial**: Cumple con estándares corporativos de documentación

### 🔄 Orquestación Inteligente
- **LangGraph**: Flujo de trabajo basado en grafos para máxima flexibilidad
- **Validación automática**: Detección y corrección de errores de sintaxis
- **Retry inteligente**: Hasta 3 intentos de corrección automática

### 🧪 Testing Exhaustivo
- **TDD**: Desarrollo guiado por pruebas con pytest
- **Cobertura completa**: 95%+ de cobertura de código
- **Tests de integración**: Validación end-to-end del flujo completo

## 🏗️ Arquitectura

```
generador_cobol_ia/
├── agents/                 # Agentes de IA especializados
│   ├── planner.py         # Agente Planificador
│   └── coder.py           # Agente Codificador + Cabeceras
├── validators/            # Sistema de validación
│   ├── mock_validator.py  # Validador simulado (MVP)
│   └── mainframe_validator.py # Validador real (futuro)
├── core/                  # Orquestación central
│   └── graph.py          # Grafo LangGraph
├── tests/                 # Suite de pruebas completa
├── Documentacion/         # Documentación técnica
│   ├── inicial/          # Arquitectura y especificaciones
│   └── funcionalidades/  # Documentación de características
└── run_prototype.py      # CLI principal
```

## 🚀 Instalación y Configuración

### Prerrequisitos
- Python 3.11+
- OpenAI API Key (o Anthropic)
- Git

### Instalación
```bash
# Clonar repositorio
git clone https://github.com/Srozasc/generador-cobol-ia.git
cd generador-cobol-ia

# Crear entorno virtual
python -m venv .venv
.venv\Scripts\activate  # Windows
# source .venv/bin/activate  # Linux/Mac

# Instalar dependencias
pip install -r requirements.txt

# Configurar variables de entorno
copy .env.example .env
# Editar .env con tu API key
```

### Configuración de API Keys
```bash
# .env
OPENAI_API_KEY=tu_api_key_aqui
# ANTHROPIC_API_KEY=opcional_anthropic_key
```

## 💻 Uso

### CLI Básico
```bash
# Ejecutar el generador
python run_prototype.py

# Ejemplo de solicitud
> "Crear programa SUPPGPR1 para gestionar información de proveedores"
```

### Ejemplo de Salida
```cobol
      ******************************************************************
      * PROGRAM-ID: SUPPGPR1                                           *
      * AUTHOR:     GENERADOR COBOL IA                                 *
      * DATE-WRITTEN: ENE-2025                                         *
      * SISTEMA:    SUMINISTROS                                        *
      * SUBSISTEMA: GESTION DE PROVEEDORES                             *
      * OBJETIVOS:  GESTIONAR INFORMACION DE PROVEEDORES               *
      * MAINTENANCE:                                                   *
      * DD/MM/YYYY AUTOR      DESCRIPCION                              *
      * 15/01/2025 COBOL-IA   CREACION INICIAL DEL PROGRAMA            *
      ******************************************************************

       IDENTIFICATION DIVISION.
       PROGRAM-ID. SUPPGPR1.
       
       DATA DIVISION.
       WORKING-STORAGE SECTION.
       01  WS-PROVEEDOR-RECORD.
           05  WS-CODIGO-PROVEEDOR    PIC X(10).
           05  WS-NOMBRE-PROVEEDOR    PIC X(50).
           05  WS-DIRECCION           PIC X(100).
           05  WS-TELEFONO            PIC X(15).
       
       PROCEDURE DIVISION.
       MAIN-PROCESS.
           DISPLAY 'SISTEMA DE GESTION DE PROVEEDORES'.
           DISPLAY 'PROGRAMA: SUPPGPR1'.
           STOP RUN.
```

## 🧪 Testing

### Ejecutar Tests
```bash
# Todos los tests
python -m pytest tests/ -v

# Tests específicos
python -m pytest tests/agents/ -v
python -m pytest tests/validators/ -v
python -m pytest tests/test_integration_flow.py -v

# Con cobertura
python -m pytest tests/ --cov=. --cov-report=html
```

### Suite de Tests
- **51 tests** implementados
- **95%+ cobertura** de código
- **Tests unitarios** para cada componente
- **Tests de integración** end-to-end
- **Tests de cabeceras empresariales** (8 tests específicos)

## 📚 Documentación

### Documentación Técnica
- [Arquitectura del Sistema](./Documentacion/inicial/arquitectura.md)
- [Especificación de Características](./Documentacion/inicial/especificacion_de_caracteristicas.md)
- [Estrategia de Versionado](./Documentacion/inicial/estrategia_versionado.md)

### Funcionalidades
- [Cabeceras Empresariales](./Documentacion/funcionalidades/cabeceras_empresariales.md)
- [Ejemplos de Cabeceras](./Documentacion/funcionalidades/ejemplos_cabeceras.md)

## 🎯 Casos de Uso

### Sistemas Soportados
- **BANCARIO**: Cuentas, transacciones, créditos
- **SUMINISTROS**: Proveedores, compras, inventario
- **RECURSOS HUMANOS**: Empleados, nómina, personal
- **CONTABILIDAD**: Balances, asientos, finanzas
- **VENTAS**: Clientes, facturación, productos
- **INVENTARIO**: Stock, almacén, control

### Ejemplos de Solicitudes
```
✅ "Crear programa CTABANK1 para gestionar cuentas bancarias"
✅ "Desarrollar EMPGEST1 para administrar empleados"
✅ "Programa de inventario INVCTRL1 para control de stock"
✅ "Sistema contable para generar balance general"
```

## 🔧 Desarrollo

### Metodología TDD
1. **Escribir test** antes de implementar
2. **Implementar** funcionalidad mínima
3. **Refactorizar** y optimizar
4. **Validar** con tests de integración

### Convenciones de Código
- **PEP 8** para estilo Python
- **Type hints** obligatorios
- **Docstrings** en formato Google
- **Tests** para cada función pública

### Contribuir
```bash
# Fork del repositorio
git fork https://github.com/Srozasc/generador-cobol-ia.git

# Crear rama feature
git checkout -b feature/nueva-funcionalidad

# Implementar con TDD
# 1. Escribir tests
# 2. Implementar código
# 3. Validar tests

# Commit y push
git commit -m "feat(agents): nueva funcionalidad X"
git push origin feature/nueva-funcionalidad

# Crear Pull Request
```

## 📈 Roadmap

### Versión 1.1 (Q2 2025)
- [ ] Validador real con mainframe (py3270)
- [ ] Interfaz web (FastAPI + React)
- [ ] Análisis de código existente
- [ ] Soporte multiidioma en cabeceras

### Versión 1.2 (Q3 2025)
- [ ] Optimización y refactorización automática
- [ ] Control de versiones integrado
- [ ] Dashboard de métricas
- [ ] Plantillas personalizables

### Versión 2.0 (Q4 2025)
- [ ] IA avanzada para inferencia de contexto
- [ ] Integración con herramientas de mainframe
- [ ] Soporte para estándares internacionales
- [ ] API REST completa

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Por favor:

1. **Fork** el repositorio
2. **Crear** rama feature (`git checkout -b feature/AmazingFeature`)
3. **Commit** cambios (`git commit -m 'Add some AmazingFeature'`)
4. **Push** a la rama (`git push origin feature/AmazingFeature`)
5. **Abrir** Pull Request

### Guías de Contribución
- Seguir metodología **TDD**
- Mantener **cobertura >90%**
- Documentar **nuevas funcionalidades**
- Usar **convenciones de commit** establecidas

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver [LICENSE](LICENSE) para más detalles.

## 👥 Equipo

- **Desarrollador Principal**: [Srozasc](https://github.com/Srozasc)
- **Arquitecto IA**: Generador COBOL IA Team
- **QA**: Suite de Tests Automatizada

## 📞 Soporte

- **Issues**: [GitHub Issues](https://github.com/Srozasc/generador-cobol-ia/issues)
- **Documentación**: [Wiki del Proyecto](https://github.com/Srozasc/generador-cobol-ia/wiki)
- **Email**: [Contacto del Proyecto]

## 🏆 Reconocimientos

- **LangChain**: Framework de IA utilizado
- **OpenAI**: Modelos de lenguaje GPT
- **Comunidad COBOL**: Inspiración y estándares

---

**⭐ Si este proyecto te resulta útil, ¡dale una estrella en GitHub!**

**🚀 Versión**: 1.0.0  
**📅 Última Actualización**: Enero 2025  
**🔧 Estado**: Producción - MVP Completo