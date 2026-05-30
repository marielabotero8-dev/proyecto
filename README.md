# 🚌 AMCO - Centro Inteligente Metropolitano
## Dashboard Avanzado con Mapas de Calor y Semáforos de Congestión

---

## 📋 Descripción del Proyecto

Sistema integral de monitoreo y optimización de transporte metropolitano con:
- ✅ **Fase 1-3**: API con Grafo, Dijkstra, Asignación de Rutas
- ✅ **Fase 4-5**: Dashboard Streamlit con Mapas de Calor y Semáforos

---

## 🛠️ INSTALACIÓN RÁPIDA

### Paso 1: Clonar o Descargar el Proyecto
```bash
cd C:\Users\jodan\Downloads\proyecto-main
# o donde hayas descargado el proyecto
```

### Paso 2: Crear Entorno Virtual
```bash
python -m venv venv
```

### Paso 3: Activar Entorno Virtual
```powershell
# Windows (PowerShell):
venv\Scripts\Activate.ps1

# Windows (CMD):
venv\Scripts\activate

# Mac/Linux:
source venv/bin/activate
```

### Paso 4: Instalar Dependencias
```bash
pip install -r requirements.txt
```

### Paso 5: Inicializar Base de Datos
```bash
python seed.py
```

---

## 🚀 EJECUTAR EL SISTEMA

**Debes abrir 3 terminales diferentes:**

### Terminal 1: IoT Simulator (Genera datos de telemetría)
```bash
python iot_simulator.py
```
✅ Verás: `[Simulator Running] Enviando telemetría cada 2 segundos...`

### Terminal 2: API FastAPI (Backend)
```bash
python api.py
```
✅ Verás: `INFO:     Uvicorn running on http://127.0.0.1:8000`

### Terminal 3: Dashboard Streamlit (Frontend)
```bash
streamlit run dashboard_avanzado.py
```
✅ Se abrirá automáticamente en tu navegador: `http://localhost:8501`

---

## 📊 CARACTERÍSTICAS DEL DASHBOARD

### 🗺️ Vista 1: Mapa en Tiempo Real
- Mapa 3D interactivo con Pydeck
- Capa hexagonal de densidad de buses
- Rutas coloreadas
- Métricas en vivo (flota, pasajeros, velocidad, energía)

### 🔥 Vista 2: Mapa de Calor
- Heatmap de demanda en paradas
- Top 10 paradas con mayor congestión
- Histograma de distribución de personas

### 🚦 Vista 3: Semáforo de Congestión
- Estado de salud de la flota (🟢 Excelente | 🟡 Aceptable | 🔴 Crítica)
- Semáforos por ruta (🟢 Baja | 🟡 Media | 🔴 Alta | 🔴 Crítica)
- Gráficos comparativos

### 📈 Vista 4: Analytics
- **Tab Rendimiento**: Distribución de velocidades
- **Tab Energía**: Análisis de batería/combustible por motor
- **Tab Pasajeros**: Ocupación y relación con velocidad
- **Tab Alertas**: Sistema de alertas en tiempo real

---

## 🔄 Opciones de Actualización

En la barra lateral del dashboard puedes elegir:
- **Manual**: Sin actualización automática
- **2 segundos**: Refresco rápido (baja latencia)
- **5 segundos**: Refresco moderado (balance consumo)

---

## 🗂️ Estructura de Archivos

```
proyecto/
├── api.py                    # Backend FastAPI (puerto 8000)
├── dashboard.py              # Dashboard básico
├── dashboard_avanzado.py     # Dashboard avanzado (NUEVO)
├── database.py               # Configuración SQLite
├── models.py                 # Modelos SQLAlchemy
├── graph_engine.py           # Grafo y Dijkstra
├── route_optimizer.py        # Asignación inteligente de rutas
├── iot_simulator.py          # Simulador de telemetría
├── seed.py                   # Inicialización de datos (NUEVO)
├── schemas.py                # Validación de datos Pydantic
├── utils.py                  # Funciones auxiliares
├── requirements.txt          # Dependencias Python
├── empresa_transporte.db     # Base de datos SQLite
└── README.md                 # Este archivo
```

---

## ⚡ Endpoints Disponibles

### Telemetría
- `GET /telemetria` - Datos GPS de toda la flota
- `POST /telemetria/{vehiculo_id}` - Actualizar telemetría

### Grafo y Rutas
- `GET /grafo/matriz-adyacencia` - Matriz de conectividad
- `GET /grafo/matriz-ponderada` - Distancias entre paradas
- `GET /ruta-optima/{origen_id}/{destino_id}` - Dijkstra
- `GET /grafo/centralidad` - Paradas más conectadas

### Congestión y Salud
- `GET /congestión/por-ruta` - Nivel de congestión
- `GET /salud/flota` - Estado general de flota
- `GET /salud/bus/{vehiculo_id}` - Estado de un bus
- `GET /mapa-calor/paradas` - Demanda en paradas

### Alertas
- `GET /alertas/activas` - Alertas en tiempo real
- `POST /incidentes` - Reportar incidente

---

## 🐛 Solución de Problemas

### ❌ Error: "can't open file 'seed.py': No such file or directory"
**Solución:**
- Verifica que estés en el directorio correcto
- Usa: `cd C:\Users\jodan\Downloads\proyecto-main` (tu ruta)
- Luego: `python seed.py`

### ❌ Error: "No se puede conectar a la API"
**Solución:**
1. Abre **Terminal 2**
2. Ejecuta: `python api.py`
3. Verifica que veas: `Uvicorn running on http://127.0.0.1:8000`

### ❌ Error: "No hay telemetría"
**Solución:**
1. Abre **Terminal 1**
2. Ejecuta: `python iot_simulator.py`
3. Verifica que esté enviando datos

### ❌ Error: "ModuleNotFoundError: No module named 'plotly'"
**Solución:**
```bash
pip install plotly
# o reinstala todo:
pip install -r requirements.txt --upgrade
```

### ❌ Puerto 8501 en uso
**Solución:**
```bash
streamlit run dashboard_avanzado.py --server.port 8502
```

### ❌ Error en Windows con venv
**Solución:**
```powershell
# Si Get-ExecutionPolicy está restrictivo:
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Luego:
venv\Scripts\Activate.ps1
```

---

## 📱 Ejecución Rápida (Comandos Directos)

```bash
# 1. Clonar/navegar
cd C:\Users\jodan\Downloads\proyecto-main

# 2. Crear virtual env
python -m venv venv

# 3. Activar
venv\Scripts\activate

# 4. Instalar
pip install -r requirements.txt

# 5. Inicializar BD
python seed.py

# 6. En TERMINAL 1
python iot_simulator.py

# 7. En TERMINAL 2
python api.py

# 8. En TERMINAL 3
streamlit run dashboard_avanzado.py
```

---

## 🎯 URL de Acceso

| Servicio | URL | Descripción |
|----------|-----|-------------|
| **Dashboard** | http://localhost:8501 | Dashboard Streamlit (abre automáticamente) |
| **API Docs** | http://127.0.0.1:8000/docs | Documentación interactiva FastAPI |
| **API Redoc** | http://127.0.0.1:8000/redoc | Documentación alternativa |

---

## 📊 Flujo de Datos

```
IoT Simulator (Terminal 1)
        ↓
   [Genera telemetría]
        ↓
   API FastAPI (Terminal 2)
        ↓
   [Procesa y almacena]
        ↓
Dashboard Streamlit (Terminal 3)
        ↓
   [Visualiza en tiempo real]
```

---

## 🔐 Variables de Entorno (Opcional)

Puedes crear un archivo `.env` para configurar:

```bash
# .env
DATABASE_URL=sqlite:///./empresa_transporte.db
API_HOST=127.0.0.1
API_PORT=8000
STREAMLIT_PORT=8501
```

---

## 📝 Notas Importantes

1. **Orden de ejecución**: Simulator → API → Dashboard
2. **Ventanas abiertas**: Mantén las 3 terminales abiertas
3. **Base de datos**: Se crea automáticamente con `seed.py`
4. **Cache de Streamlit**: Se actualiza cada 2-5s según configuración
5. **Seguridad**: Usa HTTPS en producción

---

## 🚀 Próximos Pasos

- [ ] Agregar autenticación de usuarios
- [ ] Optimizar queries de base de datos
- [ ] Implementar WebSockets para tiempo real
- [ ] Deploy a Heroku/AWS
- [ ] Agregar notificaciones por email/SMS

---

## 📞 Soporte

Si tienes problemas:
1. Verifica que Python 3.8+ está instalado: `python --version`
2. Revisa que todos los servicios estén corriendo
3. Limpia cache: `pip cache purge`
4. Reinstala: `pip install -r requirements.txt --force-reinstall`

---

## 📄 Licencia

© 2026 AMCO - Centro Inteligente Metropolitano

---

**¡Listo para ejecutar! 🎉**
