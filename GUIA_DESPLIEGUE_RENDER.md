# 📘 GUÍA COMPLETA DE DESPLIEGUE EN RENDER

## 📋 Tabla de Contenidos
1. [Requisitos Previos](#requisitos-previos)
2. [Subir Archivos a GitHub](#paso-1-github)
3. [Configurar Render](#paso-2-render)
4. [Verificar Despliegue](#paso-3-verificar)
5. [Solución de Problemas](#solución-de-problemas)
6. [Configuraciones Avanzadas](#configuraciones-avanzadas)

---

## 📋 Requisitos Previos

### ✅ Necesitas:
- Cuenta en GitHub (gratuita) - https://github.com
- Cuenta en Render (gratuita) - https://render.com
- Archivos del proyecto descargados

### 📦 Archivos del Proyecto:
```
pasivos-corrientes/
├── app.py                    # ⭐ Aplicación principal
├── requirements.txt          # 📦 Dependencias Python
├── Dockerfile               # 🐳 Configuración Docker
├── .dockerignore            # 🚫 Exclusiones Docker
├── README.md                # 📖 Documentación
└── .streamlit/
    └── config.toml          # ⚙️ Config Streamlit
```

---

## PASO 1: SUBIR ARCHIVOS A GITHUB

### 1.1 Crear Repositorio en GitHub

1. **Ir a GitHub**
   - Abre https://github.com
   - Inicia sesión (o crea cuenta si no tienes)

2. **Crear Nuevo Repositorio**
   - Click en el botón **"+"** (arriba derecha)
   - Selecciona **"New repository"**

3. **Configurar Repositorio**
   ```
   Repository name:  pasivos-corrientes-audit
   Description:      Sistema de Auditoría de Pasivos Corrientes
   Visibility:       Public ✅ (recomendado para Render Free)
   Initialize:       ❌ NO marcar ninguna opción
   ```

4. **Crear**
   - Click en **"Create repository"**

### 1.2 Subir Archivos

#### MÉTODO A: Desde la Web de GitHub (RECOMENDADO - MÁS FÁCIL)

1. **En tu nuevo repositorio vacío:**
   - Verás instrucciones para "Quick setup"
   - Busca el enlace **"uploading an existing file"**
   - Click en ese enlace

2. **Subir Archivos:**
   - Arrastra TODOS los archivos del ZIP a la ventana
   - O click en **"choose your files"** y selecciona todo
   - **IMPORTANTE**: Asegúrate de incluir la carpeta `.streamlit`

3. **Commit:**
   - En "Commit changes"
   - Mensaje: `Initial commit`
   - Click **"Commit changes"**

4. **Verificar:**
   - Deberías ver todos tus archivos listados
   - Verifica que `.streamlit/config.toml` esté presente

#### MÉTODO B: Con Git en Terminal (Para usuarios avanzados)

```bash
# Navegar a la carpeta con los archivos
cd ruta/a/tus/archivos

# Inicializar Git
git init

# Agregar todos los archivos
git add .

# Hacer commit
git commit -m "Initial commit"

# Cambiar a branch main
git branch -M main

# Conectar con GitHub (reemplaza TU-USUARIO)
git remote add origin https://github.com/TU-USUARIO/pasivos-corrientes-audit.git

# Subir archivos
git push -u origin main
```

### 1.3 Verificación Final

✅ Tu repositorio debe tener:
- `app.py`
- `requirements.txt`
- `Dockerfile`
- `.dockerignore`
- `README.md`
- `.streamlit/config.toml`

---

## PASO 2: CONFIGURAR RENDER

### 2.1 Crear Cuenta en Render

1. **Ir a Render**
   - Abre https://render.com
   - Click en **"Get Started"** o **"Sign Up"**

2. **Registrarse**
   - Opción recomendada: **"Sign up with GitHub"**
   - Esto facilita la conexión con tus repositorios
   - Autoriza a Render para acceder a GitHub

3. **Verificar Email**
   - Revisa tu email y confirma la cuenta

### 2.2 Conectar Repositorio

1. **En el Dashboard de Render:**
   - Click en **"New +"** (arriba derecha)
   - Selecciona **"Web Service"**

2. **Conectar GitHub:**
   - Si es tu primer servicio:
     - Click en **"Connect a repository"**
     - Autoriza a Render
   
3. **Buscar Repositorio:**
   - Si NO ves tu repositorio:
     - Click en **"Configure account"**
     - Da acceso a `pasivos-corrientes-audit`
   - Selecciona el repositorio `pasivos-corrientes-audit`
   - Click en **"Connect"**

### 2.3 Configurar Web Service

**IMPORTANTE**: Copia exactamente estos valores

#### Configuración Básica:

```
Name:               pasivos-corrientes
(Este será parte de tu URL)

Region:             Frankfurt (EU Central)
(O el más cercano a ti)

Branch:             main
(Branch principal de GitHub)

Root Directory:     [Dejar VACÍO]
(Archivos en la raíz del repo)

Runtime:            Python 3
(Auto-detectado)
```

#### Build & Deploy Settings:

**Build Command:**
```bash
pip install -r requirements.txt
```

**Start Command:**
```bash
streamlit run app.py --server.port=$PORT --server.address=0.0.0.0 --server.headless=true
```

⚠️ **MUY IMPORTANTE**: 
- No olvides `--server.port=$PORT`
- No olvides `--server.headless=true`
- El nombre del archivo es `app.py` (sin "s")

#### Plan:

```
Instance Type:      Free
(512 MB RAM, suficiente para esta app)
```

### 2.4 Variables de Entorno (Opcional)

Para esta aplicación NO es necesario agregar variables de entorno.

Si en el futuro necesitas agregar:
- Click en **"Add Environment Variable"**
- Ingresa KEY y VALUE
- Para esta app: **No agregar nada**

### 2.5 Desplegar

1. **Revisar Configuración:**
   - Verifica que todo esté correcto
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `streamlit run app.py --server.port=$PORT --server.address=0.0.0.0 --server.headless=true`

2. **Crear Servicio:**
   - Click en **"Create Web Service"**
   - Render comenzará a construir tu aplicación

3. **Proceso de Build:**
   - Verás logs en tiempo real
   - **Paso 1**: Clonando repositorio (~10 seg)
   - **Paso 2**: Instalando dependencias (~2 min)
   - **Paso 3**: Iniciando aplicación (~30 seg)
   - **Total**: 3-5 minutos

4. **Estado:**
   - Cuando veas **"Your service is live 🎉"**
   - Tu aplicación está lista

---

## PASO 3: VERIFICAR DESPLIEGUE

### 3.1 Obtener URL

Tu aplicación estará disponible en:
```
https://pasivos-corrientes.onrender.com
```
(El nombre puede variar si ya existía)

### 3.2 Probar la Aplicación

1. **Abrir URL en navegador**
   - Click en la URL en Render Dashboard
   - O copia y pega en tu navegador

2. **Verificar Funcionalidad:**
   - ✅ Página de Inicio se carga
   - ✅ Sidebar con módulos visible
   - ✅ Dashboard General funciona
   - ✅ Cada módulo carga datos correctamente

3. **Probar Módulos:**
   - Click en cada módulo del sidebar
   - Click en "Iniciar Análisis"
   - Verifica que gráficos se generen
   - Revisa que datos se muestren

### 3.3 Monitoreo en Render

En el Dashboard de Render verás:
- **Status**: Running (verde) ✅
- **CPU Usage**: Uso del procesador
- **Memory**: Uso de RAM
- **Requests**: Número de visitas

---

## 🔧 SOLUCIÓN DE PROBLEMAS

### ❌ Error: "Application failed to start"

**Causas comunes:**
1. Start Command incorrecto
2. Puerto no configurado correctamente
3. Falta archivo requirements.txt

**Solución:**
1. Ve a **Settings** → **Build & Deploy**
2. Verifica Start Command:
   ```bash
   streamlit run app.py --server.port=$PORT --server.address=0.0.0.0 --server.headless=true
   ```
3. Click en **"Manual Deploy"** → **"Deploy latest commit"**

### ❌ Error: "Module not found: streamlit"

**Causa:** Build Command no ejecutado correctamente

**Solución:**
1. Verifica que `requirements.txt` esté en la raíz del repo
2. Ve a **Logs** y busca errores de instalación
3. Build Command debe ser: `pip install -r requirements.txt`
4. Redeploy

### ❌ Error: "Address already in use"

**Causa:** Puerto hardcodeado en lugar de usar $PORT

**Solución:**
- Start Command DEBE incluir: `--server.port=$PORT`
- Render asigna puerto dinámicamente

### ❌ Error: "Connection refused"

**Causa:** Server address incorrecta

**Solución:**
- Start Command debe incluir: `--server.address=0.0.0.0`
- Esto permite conexiones externas

### ⚠️ App se duerme después de inactividad

**Causa:** Comportamiento normal del plan Free

**Detalles:**
- Plan gratuito duerme apps después de 15 min sin actividad
- Primera visita después toma 30-60 seg en despertar
- Totalmente normal

**Soluciones:**
1. **Aceptar el comportamiento** (gratis)
2. **Upgrade a plan de pago** ($7/mes - 24/7 activo)
3. **Usar servicio de ping** (ej: UptimeRobot) para mantener activo

### 🐛 Error: "Build failed"

**Solución:**
1. Ve a **Logs**
2. Busca la línea con el error específico
3. Comunes:
   - Typo en requirements.txt → Corregir y push
   - Versión incompatible → Ajustar versiones
   - Falta librería → Agregar a requirements.txt

### 📊 App muy lenta

**Causas:**
1. Primera carga (normal - 30-60 seg)
2. Plan Free con recursos limitados
3. Muchos datos generándose

**Soluciones:**
1. Reduce `num_registros` en funciones (de 50 a 30)
2. Upgrade a plan de pago (más RAM/CPU)
3. Optimizar código

---

## ⚙️ CONFIGURACIONES AVANZADAS

### 🌐 Dominio Personalizado

1. Ve a **Settings** → **Custom Domain**
2. Click en **"Add Custom Domain"**
3. Ingresa tu dominio: `auditoria.tuempresa.com`
4. Configura DNS según instrucciones:
   ```
   Type:  CNAME
   Name:  auditoria (o www)
   Value: pasivos-corrientes.onrender.com
   ```
5. Espera propagación DNS (5-30 min)

### 🔔 Notificaciones

1. Ve a **Settings** → **Notifications**
2. Activa:
   - Deploy Success/Failure
   - Service Health Alerts
3. Ingresa email o Slack webhook

### 🔄 Auto-Deploy

**Ya está activado por defecto:**
- Cada push a `main` en GitHub dispara nuevo deploy
- Render detecta cambios automáticamente
- Deploy toma ~3 min

**Desactivar Auto-Deploy:**
1. Settings → Build & Deploy
2. Desactiva **"Auto-Deploy"**
3. Deploys manuales: **"Manual Deploy"**

### 📈 Métricas y Logs

**Ver Logs:**
- Tab **"Logs"** en Dashboard
- Logs en tiempo real
- Útil para debugging

**Métricas:**
- Tab **"Metrics"**
- CPU, RAM, Bandwidth
- Historial de requests

### 💾 Variables de Entorno Secretas

Si necesitas API keys o secrets:
1. Settings → Environment
2. **Add Secret File** o **Add Environment Variable**
3. Nunca pongas secrets en código

### 🔒 HTTPS / SSL

- Render provee HTTPS automáticamente
- Certificado SSL gratuito
- Auto-renueva
- No requiere configuración

---

## 📊 MONITOREO Y MANTENIMIENTO

### Revisar Estado

**Diariamente:**
- Ver Dashboard → Status
- Debe estar "Running" (verde)

**Semanalmente:**
- Revisar Metrics → Memory usage
- Si >80% considerar optimización

**Mensualmente:**
- Revisar Logs por errores
- Actualizar dependencias si hay parches

### Actualizar Aplicación

```bash
# En tu computadora
cd pasivos-corrientes-audit

# Hacer cambios en archivos
nano app.py  # o tu editor favorito

# Commit y push
git add .
git commit -m "Descripción del cambio"
git push

# Render redespliega automáticamente
# Esperar 3-5 minutos
```

### Rollback (Volver a versión anterior)

1. Dashboard → **"Manual Deploy"**
2. Selecciona commit anterior
3. Click **"Deploy selected commit"**

---

## 💰 PLANES Y COSTOS

### Free Plan (Actual)
- ✅ 512 MB RAM
- ✅ Shared CPU
- ✅ 750 horas/mes
- ✅ HTTPS incluido
- ⚠️ Duerme después de 15 min
- ⚠️ Build time más lento

### Starter Plan ($7/mes)
- ✅ 512 MB RAM
- ✅ Activo 24/7 (no duerme)
- ✅ Build más rápido
- ✅ Soporte prioritario

### Pro Plan ($25/mes)
- ✅ 2 GB RAM
- ✅ 1 CPU
- ✅ Mayor velocidad
- ✅ Métricas avanzadas

---

## 🎓 RECURSOS ADICIONALES

### Documentación Oficial

- **Render Docs**: https://render.com/docs
- **Streamlit Docs**: https://docs.streamlit.io
- **Python Docs**: https://docs.python.org

### Comunidad

- **Render Community**: https://community.render.com
- **Streamlit Forum**: https://discuss.streamlit.io
- **Stack Overflow**: Tag `render` o `streamlit`

### Soporte

- **Render Support**: support@render.com
- **Status Page**: https://status.render.com

---

## ✅ CHECKLIST FINAL

Antes de dar por terminado, verifica:

- [ ] Repositorio en GitHub creado
- [ ] Todos los archivos subidos correctamente
- [ ] Cuenta en Render creada y verificada
- [ ] Web Service configurado con comandos correctos
- [ ] Build exitoso (sin errores en logs)
- [ ] Aplicación accesible por URL
- [ ] Página de Inicio carga correctamente
- [ ] Dashboard General funciona
- [ ] Los 7 módulos cargan datos
- [ ] Gráficos se visualizan correctamente
- [ ] Botones de análisis funcionan
- [ ] No hay errores en consola del navegador

---

## 🎉 ¡FELICITACIONES!

Tu aplicación de **Auditoría de Pasivos Corrientes** está ahora en línea y accesible desde cualquier lugar del mundo.

**URL de tu app:**
```
https://pasivos-corrientes.onrender.com
```

**Próximos pasos:**
1. Comparte la URL con tu equipo
2. Recopila feedback
3. Realiza mejoras según necesidades
4. Considera upgrade si necesitas más recursos

---

**¿Preguntas?** Consulta el README.md o crea un issue en GitHub.

**¡Éxito con tu aplicación! 🚀**
