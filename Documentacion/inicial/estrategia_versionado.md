# Estrategia de Versionado - Generador COBOL IA

## 📋 Información General

**Proyecto:** Generador COBOL IA  
**Repositorio:** `generador-cobol-ia`  
**URL:** `https://github.com/Srozasc/generador-cobol-ia.git`  
**Estrategia:** Versionado Semántico + Git Tags + GitHub Releases  
**Fecha de Creación:** Enero 2025  
**Versión Actual:** v1.0.0 (MVP)  

---

## 🎯 Objetivos de la Estrategia

- **Simplicidad**: Comandos básicos de Git, fácil de seguir
- **Trazabilidad**: Cada versión claramente identificada y documentada
- **Escalabilidad**: Preparada para múltiples versiones y características
- **Profesionalismo**: Releases documentados y organizados
- **Seguridad**: Protección de API keys y datos sensibles

---

## 🧪 Modo Prototipo (sin tags)

- Mientras el proyecto esté en fase de prototipo, no se crean tags de versión ni se publican Releases en GitHub.
- Todos los cambios se documentan de forma acumulativa en `Documentacion/inicial/releases/UNRELEASED.md`.
- Al definir el próximo release formal:
  - Se migra el contenido de `UNRELEASED.md` a `vX.Y.Z.md` (por ejemplo `v1.0.1.md`).
  - Se crea el tag anotado `vX.Y.Z` y se publica el Release en GitHub usando la plantilla estándar.
- Criterios sugeridos de salida de prototipo: flujo MVP estable, suite de tests verde, documentación alineada.

## 🏷️ Esquema de Versionado Semántico

### Formato: `vMAJOR.MINOR.PATCH`

- **MAJOR** (v1.0.0 → v2.0.0): Cambios incompatibles, arquitectura nueva
- **MINOR** (v1.0.0 → v1.1.0): Nuevas funcionalidades compatibles
- **PATCH** (v1.0.0 → v1.0.1): Correcciones de bugs, hotfixes

### Ejemplos de Versiones Planificadas:
- **v1.0.0**: MVP con validador simulado
- **v1.1.0**: Mejoras en CLI y nuevos prompts
- **v2.0.0**: Validador real con mainframe (py3270)
- **v2.1.0**: Interfaz web (FastAPI + React)
- **v3.0.0**: Análisis de código existente

---

## 🌿 Estrategia de Branches

### **Branches Principales:**
- **`main`**: Versión estable actual, siempre funcional
- **`develop`**: Desarrollo activo de la próxima versión
- **`hotfix/descripcion`**: Correcciones urgentes para producción

### **Branches de Funcionalidades:**
- **`feature/nombre-funcionalidad`**: Nuevas características
- **`bugfix/descripcion-bug`**: Correcciones no urgentes
- **`docs/actualizacion`**: Actualizaciones de documentación

### **Flujo de Trabajo:**
```
main ←── hotfix/critical-fix
 ↑
 └── develop ←── feature/nueva-funcionalidad
      ↑
      └── feature/otra-funcionalidad
```

---

## 🚀 Proceso de Versionado

### **1. Configuración Inicial (Ya Completada)**

```bash
# Inicializar repositorio
git init
git add .
git commit -m "feat: MVP completo del Generador COBOL IA v1.0"

# Conectar con GitHub
git remote add origin https://github.com/Srozasc/generador-cobol-ia.git
git branch -M main
git push -u origin main

# Crear tag v1.0.0
git tag -a v1.0.0 -m "Versión 1.0.0 - MVP Completo"
git push origin v1.0.0
```

### **2. Para Nuevas Versiones MINOR (v1.x.0)**

```bash
# Crear branch de desarrollo
git checkout -b develop
git push -u origin develop

# Desarrollar funcionalidades
git checkout -b feature/nueva-funcionalidad
# ... desarrollo ...
git add .
git commit -m "feat: descripción de la funcionalidad"
git push origin feature/nueva-funcionalidad

# Merge a develop
git checkout develop
git merge feature/nueva-funcionalidad
git push origin develop

# Release a main
git checkout main
git merge develop
git tag -a v1.1.0 -m "Versión 1.1.0 - Nuevas funcionalidades"
git push origin main
git push origin v1.1.0
```

### **3. Para Nuevas Versiones MAJOR (v2.0.0)**

```bash
# Desde develop con cambios significativos
git checkout main
git merge develop
git tag -a v2.0.0 -m "Versión 2.0.0 - Cambios arquitectónicos importantes"
git push origin main
git push origin v2.0.0
```

### **4. Para Hotfixes (v1.0.1)**

```bash
# Desde main
git checkout -b hotfix/descripcion-critica
# ... corrección ...
git add .
git commit -m "fix: corrección crítica"
git checkout main
git merge hotfix/descripcion-critica
git tag -a v1.0.1 -m "Versión 1.0.1 - Hotfix crítico"
git push origin main
git push origin v1.0.1
```

---

## 📦 Creación de Releases en GitHub

### **Información Estándar para Releases:**

#### **Título:** `Versión X.Y.Z - Descripción Breve`

#### **Plantilla de Descripción:**
```markdown
## 🎯 Versión X.Y.Z - [Nombre de la Versión]

### ✅ Nuevas Características
- Característica 1: Descripción detallada
- Característica 2: Descripción detallada

### 🔧 Mejoras
- Mejora 1: Descripción
- Mejora 2: Descripción

### 🐛 Correcciones
- Bug 1: Descripción de la corrección
- Bug 2: Descripción de la corrección

### 🧪 Testing
- X tests pasando
- Cobertura: Y%
- Nuevos tests agregados

### 🚀 Instalación y Uso
```bash
git clone https://github.com/Srozasc/generador-cobol-ia.git
cd generador-cobol-ia
git checkout vX.Y.Z
.venv\Scripts\activate
pip install -r requirements.txt
python run_prototype.py
```

### 📋 Requisitos
- Python 3.11+
- OpenAI API Key
- [Otros requisitos específicos]

### 🔄 Migración desde Versión Anterior
[Instrucciones si aplica]
```

---

## 📂 Estructura de Archivos Versionados

### **Incluidos en Git:**
```
generador_cobol_ia/
├── agents/                 # Código de agentes
├── core/                   # Lógica central
├── validators/             # Validadores
├── tests/                  # Suite de tests
├── Documentacion/          # Documentación técnica
├── requirements.txt        # Dependencias
├── run_prototype.py        # CLI principal
├── .env.example           # Template de variables
├── .gitignore             # Exclusiones
└── README.md              # Documentación principal
```

### **Excluidos (.gitignore):**
```
.venv/                     # Entorno virtual
.env                       # Variables sensibles
__pycache__/               # Cache de Python
.pytest_cache/             # Cache de tests
*.log                      # Archivos de log
```

---

## 🔄 Comandos de Uso Frecuente

### **Cambiar a Versión Específica:**
```bash
git checkout v1.0.0        # MVP original
git checkout v2.0.0        # Versión con mainframe
git checkout main          # Última versión estable
```

### **Ver Historial de Versiones:**
```bash
git tag -l                 # Listar todos los tags
git log --oneline --graph  # Ver historial gráfico
```

### **Crear Branch de Funcionalidad:**
```bash
git checkout develop
git pull origin develop
git checkout -b feature/nombre-descriptivo
```

### **Limpiar Branches Locales:**
```bash
git branch -d feature/funcionalidad-completada
git remote prune origin
```

---

## 📋 Convenciones de Commits

### **Formato:** `tipo(scope): descripción`

### **Tipos Permitidos:**
- **feat**: Nueva funcionalidad
- **fix**: Corrección de bug
- **docs**: Cambios en documentación
- **style**: Formateo, espacios (sin cambios de lógica)
- **refactor**: Refactorización de código
- **test**: Agregar o modificar tests
- **chore**: Tareas de mantenimiento

### **Ejemplos:**
```bash
feat(agents): implementar agente de optimización
fix(validators): corregir validación de sintaxis COBOL
docs(readme): actualizar instrucciones de instalación
test(integration): agregar tests para flujo completo
refactor(core): simplificar lógica del grafo
```

---

## 🎯 Roadmap de Versiones

### **v1.0.0 - MVP (✅ Completado)**
- Agente Planificador
- Agente Codificador  
- Validador Simulado
- Orquestador LangGraph
- CLI Narrativa
- Suite de Tests

### **v1.1.0 - Mejoras MVP (🔄 Planificado)**
- Mejores prompts
- Más tipos de programas COBOL
- Interfaz CLI mejorada
- Documentación expandida

### **v2.0.0 - Validación Real (🔄 Futuro)**
- Integración py3270
- Validador con mainframe real
- Manejo de errores de compilación
- Logs detallados

### **v2.1.0 - Interfaz Web (🔄 Futuro)**
- API REST con FastAPI
- Frontend React/Vue
- Autenticación de usuarios
- Historial de generaciones

### **v3.0.0 - Análisis Avanzado (🔄 Futuro)**
- Análisis de código existente
- Refactorización automática
- Optimización de performance
- Integración con Git

---

## 🔒 Consideraciones de Seguridad

### **Variables Sensibles:**
- ✅ `.env` excluido de Git
- ✅ `.env.example` como template
- ✅ API keys nunca en código
- ✅ Repositorio privado recomendado

### **Validación Pre-Commit:**
```bash
# Verificar que no hay secrets
git diff --cached | grep -i "api_key\|secret\|password"

# Ejecutar tests antes de commit
pytest

# Verificar formato de código
black --check .
```

---

## 📞 Contacto y Mantenimiento

**Mantenedor Principal:** Srozasc  
**Última Actualización:** Enero 2025  
**Próxima Revisión:** Al completar v1.1.0  

---

## 📝 Notas Importantes

1. **Siempre crear tag** después de merge a main
2. **Documentar cambios** en cada release
3. **Mantener develop actualizado** con main periódicamente
4. **Probar exhaustivamente** antes de crear releases
5. **Seguir versionado semántico** estrictamente
6. **Actualizar este documento** con cada cambio de estrategia

---

*Este documento es parte de la documentación técnica del proyecto Generador COBOL IA y debe mantenerse actualizado con cada evolución de la estrategia de versionado.*
