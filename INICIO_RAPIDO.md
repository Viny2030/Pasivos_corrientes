# 🚀 GUÍA DE INICIO RÁPIDO - 5 MINUTOS

## ⚡ Despliegue Express en Render

### PASO 1: Preparar Archivos (1 minuto)
✅ Descarga el archivo ZIP
✅ Extrae todos los archivos en una carpeta

**Archivos incluidos:**
- `app.py` - Aplicación principal
- `requirements.txt` - Dependencias
- `Dockerfile` - Para Docker (opcional)
- `.dockerignore` - Configuración Docker
- `README.md` - Documentación
- `.streamlit/config.toml` - Configuración

---

### PASO 2: Subir a GitHub (2 minutos)

#### Opción A: Desde la Web (MÁS FÁCIL)
1. Ve a https://github.com/new
2. Nombre del repo: `pasivos-corrientes`
3. Descripción: `Sistema de Auditoría de Pasivos Corrientes`
4. Selecciona: **Public**
5. NO marques "Add README" (ya lo tenemos)
6. Click **Create repository**
7. Click **uploading an existing file**
8. Arrastra TODOS los archivos
9. Commit: "Initial commit"
10. Click **Commit changes**

#### Opción B: Con Git (Terminal)
```bash
cd carpeta-con-archivos
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/TU-USUARIO/pasivos-corrientes.git
git push -u origin main
```

---

### PASO 3: Desplegar en Render (2 minutos)

1. **Ir a Render**
   - https://render.com
   - Click **Get Started** o **Sign Up**
   - Registrarse con **GitHub** (más rápido)

2. **Crear Web Service**
   - Click **New +**
   - Seleccionar **Web Service**
   - Click **Connect a repository**
   - Buscar y seleccionar: `pasivos-corrientes`

3. **Configurar Servicio**
   ```
   Name:          pasivos-corrientes
   Region:        Frankfurt (EU Central)
   Branch:        main
   Runtime:       Python 3
   Build Command: pip install -r requirements.txt
   Start Command: streamlit run app.py --server.port=$PORT --server.address=0.0.0.0 --server.headless=true
   Plan:          Free
   ```

4. **Desplegar**
   - Click **Create Web Service**
   - Esperar 3-5 minutos
   - ¡Listo! 🎉

---

### ✅ TU APP ESTARÁ EN:
```
https://pasivos-corrientes.onrender.com
```
(Reemplaza con tu URL real)

---

## 🎯 COMANDOS DE RENDER - COPIA Y PEGA

### Build Command:
```bash
pip install -r requirements.txt
```

### Start Command:
```bash
streamlit run app.py --server.port=$PORT --server.address=0.0.0.0 --server.headless=true
```

---

## 📱 PROBAR LOCALMENTE (Opcional)

Antes de desplegar, puedes probar en tu computadora:

```bash
# Instalar dependencias
pip install -r requirements.txt

# Ejecutar aplicación
streamlit run app.py
```

Abrir: http://localhost:8501

---

## 🆘 PROBLEMAS COMUNES

### ❌ "Application failed to start"
**Solución:**
- Ir a **Logs** en Render
- Verificar el Start Command
- Redeploy: **Manual Deploy** → **Deploy latest commit**

### ❌ "No module named 'streamlit'"
**Solución:**
- Verificar que `requirements.txt` esté en la raíz
- Build Command debe ser: `pip install -r requirements.txt`

### ❌ "Port already in use"
**Solución:**
- Render asigna el puerto automáticamente con `$PORT`
- Asegúrate de usar: `--server.port=$PORT` en Start Command

### ⏰ App se duerme (Normal en plan Free)
- Plan gratuito duerme después de 15 min sin actividad
- Primera visita toma 30-60 segundos en despertar
- **Solución**: Upgrade a plan de pago ($7/mes)

---

## 📦 CONTENIDO DEL PAQUETE

✅ **app.py** - Aplicación Streamlit (7 módulos integrados)
✅ **requirements.txt** - Todas las librerías necesarias
✅ **Dockerfile** - Para despliegue con Docker
✅ **.dockerignore** - Optimización Docker
✅ **README.md** - Documentación completa
✅ **.streamlit/config.toml** - Configuración personalizada

---

## 🎨 CARACTERÍSTICAS DE LA APP

### 🏠 Página de Inicio
- Bienvenida profesional
- Descripción de módulos
- Estadísticas del sistema

### 📊 Dashboard General
- Vista consolidada de todos los pasivos
- Gráficos comparativos
- Métricas en tiempo real

### 7️⃣ Módulos Especializados
1. 📋 Cuentas por Pagar
2. 💰 Préstamos Obtenidos
3. 👥 Remuneraciones y Cargas Sociales
4. 🏛️ Cargas Fiscales
5. 💵 Dividendos a Pagar
6. 📥 Anticipos de Clientes
7. 📊 Otras Deudas

### 🔍 Análisis Avanzado
- Detección de anomalías con ML
- Visualizaciones profesionales
- Exportación de datos
- Métricas consolidadas

---

## 💡 TIPS PRO

✅ **Personalizar URL**: En Settings → Custom Domain
✅ **Ver Logs**: Dashboard → Logs (útil para debug)
✅ **Actualizar**: Solo haz push a GitHub, Render redespliega automáticamente
✅ **Monitorear**: Dashboard muestra CPU, RAM, requests
✅ **Notificaciones**: Configura en Settings para recibir alertas

---

## 📞 ¿NECESITAS MÁS AYUDA?

📖 **Documentación completa**: Lee `README.md`
📘 **Guía detallada**: Lee `GUIA_DESPLIEGUE_RENDER.md`
🌐 **Render Docs**: https://render.com/docs
💬 **Streamlit Forum**: https://discuss.streamlit.io

---

## ⏱️ RESUMEN: 5 MINUTOS

1. ✅ Extraer archivos (30 seg)
2. ✅ Subir a GitHub (2 min)
3. ✅ Configurar Render (2 min)
4. ✅ Desplegar (30 seg)

**TOTAL: ~5 minutos** ⚡

---

¡Tu aplicación profesional de auditoría estará lista en minutos! 🎉

**¿Preguntas?** Consulta la documentación completa o crea un issue en GitHub.
