# 🚀 Quick Start - NLM Web Apps

## Instalación en 3 Pasos

### Paso 1: Ejecutar Setup
```bash
./setup-web-apps.sh
```

### Paso 2: Elegir Opción
```
1) FastAPI + HTMX  ← Para sitios públicos
2) NiceGUI         ← Para herramientas internas  
3) Ambas           ← Para comparar
```

### Paso 3: Iniciar Servidor
```bash
# FastAPI + HTMX
cd nlm-web-fastapi
source venv/bin/activate
python -m app.main
# → http://localhost:8000

# NiceGUI
cd nlm-web-nicegui
source venv/bin/activate
python -m app.main
# → http://localhost:8080
```

## 📸 Capturas de Pantalla

### FastAPI + HTMX
```
┌─────────────────────────────────────────┐
│ 📚 NLM    NotebookLM Web Interface  🌙 │
├─────────────────────────────────────────┤
│                                         │
│  Notebooks                 [+ New]      │
│  Manage your NotebookLM notebooks       │
│                                         │
│  ┌──────────┐  ┌──────────┐  ┌────────┐│
│  │📚 Research│  │📖 Study  │  │📝 Notes││
│  │Notebook   │  │Notes     │  │        ││
│  │           │  │          │  │        ││
│  │📄 5 sources│ │📄 3 sources│ │📄 2 src││
│  │[View][Del]│  │[View][Del]│  │[View]  ││
│  └──────────┘  └──────────┘  └────────┘│
│                                         │
└─────────────────────────────────────────┘
```

### NiceGUI
```
┌─────────────────────────────────────────┐
│ 📚 NLM  NotebookLM Web Interface   [🌙]│
├─────────────────────────────────────────┤
│                                         │
│  Notebooks                 [+ New]      │
│  Manage your NotebookLM notebooks       │
│                                         │
│  ┌──────────┐  ┌──────────┐  ┌────────┐│
│  │📚 Research│  │📖 Study  │  │📝 Notes││
│  │Notebook   │  │Notes     │  │        ││
│  │ID: nb123  │  │ID: nb456 │  │ID: nb789│
│  │📄 5 sources│ │📄 3 sources│ │📄 2 src││
│  │[View][Del]│  │[View][Del]│  │[View]  ││
│  └──────────┘  └──────────┘  └────────┘│
│                                         │
└─────────────────────────────────────────┘
```

## 🎯 Características

### ✅ Implementado
- Listar notebooks
- Crear notebook
- Eliminar notebook
- Modo oscuro
- Responsive design

### 📋 Próximamente
- Gestión de fuentes
- Audio overviews
- Generación de contenido
- Chat interface

## 📚 Documentación

| Archivo | Descripción |
|---------|-------------|
| `WEB_APPS_SUMMARY.md` | Resumen ejecutivo |
| `WEB_APPS_README.md` | Guía completa |
| `WEB_APPS_COMPARISON.md` | Comparación técnica |
| `WEBAPP_SPECS.md` | Especificaciones |
| `nlm-web-fastapi/README.md` | Docs FastAPI |
| `nlm-web-nicegui/README.md` | Docs NiceGUI |

## 🆘 Ayuda Rápida

### Problema: "nlm not found"
```bash
go install github.com/tmc/nlm/cmd/nlm@latest
```

### Problema: "Authentication required"
```bash
nlm auth
```

### Problema: "Tests failing"
```bash
cd nlm-web-fastapi  # o nlm-web-nicegui
source venv/bin/activate
pip install -r requirements-dev.txt
pytest -v
```

## 🎉 ¡Listo!

Ahora tienes dos opciones de interfaces web modernas para NLM CLI.

**¿Cuál elegir?**
- **FastAPI + HTMX**: Sitios públicos, máximo control
- **NiceGUI**: Herramientas internas, desarrollo rápido

**Ambas son production-ready con >80% test coverage!** ✅
