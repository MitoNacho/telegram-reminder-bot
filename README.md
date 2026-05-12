# 🤖 Telegram Reminder Bot

<div align="center">

![Python](https://img.shields.io/badge/Python-3.13-blue?style=for-the-badge\&logo=python)
![Telegram](https://img.shields.io/badge/Telegram-Bot-2CA5E0?style=for-the-badge\&logo=telegram)
![Railway](https://img.shields.io/badge/Deploy-Railway-0B0D0E?style=for-the-badge\&logo=railway)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-4169E1?style=for-the-badge\&logo=postgresql)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-red?style=for-the-badge\&logo=sqlalchemy)
![APScheduler](https://img.shields.io/badge/APScheduler-Async-success?style=for-the-badge)

### 🚀 Bot de Telegram para recordatorios personales con scheduler automático, persistencia y deploy en Railway.

</div>

---

# ✨ Funcionalidades

## ✅ Funcionalidades actuales del MVP

* ➕ Crear recordatorios mediante conversaciones guiadas
* 📋 Ver todas las citas personales
* 🗑️ Eliminar todas las citas con confirmación
* ⏰ Notificaciones automáticas
* 🔔 Aviso 1 hora antes
* 🚨 Aviso exacto a la hora de la cita
* 🧹 Eliminación automática tras ejecutarse el recordatorio
* 👤 Soporte multiusuario mediante Telegram ID
* 🔄 Restauración automática de jobs tras reinicios de Railway
* 🗄️ Persistencia con PostgreSQL
* ☁️ Preparado para deploy en Railway
* ⚡ Arquitectura asíncrona con python-telegram-bot v20+

---

# 🏗️ Arquitectura del Proyecto

```text
telegram-reminder-bot/
│
├── app/
│   │
│   ├── bot/
│   │   ├── conversations.py
│   │   ├── handlers.py
│   │   ├── keyboards.py
│   │   └── states.py
│   │
│   ├── database/
│   │   ├── db.py
│   │   ├── init_db.py
│   │   ├── models.py
│   │   └── queries.py
│   │
│   ├── scheduler/
│   │   └── reminder_scheduler.py
│   │
│   ├── config.py
│   └── main.py
│
├── requirements.txt
├── Procfile
├── railway.json
├── .env
└── README.md
```

---

# 🧠 Explicación de la Arquitectura

## 📦 Capa Telegram

Gestiona:

* conversaciones
* botones
* comandos
* interacción con usuarios

Archivos:

```text
app/bot/
```

---

## 🗄️ Capa Base de Datos

Gestiona:

* modelos SQLAlchemy
* conexión a base de datos
* queries
* persistencia

Archivos:

```text
app/database/
```

---

## ⏰ Capa Scheduler

Gestiona:

* jobs APScheduler
* ejecución de recordatorios
* limpieza automática
* restauración de jobs tras reinicios

Archivos:

```text
app/scheduler/
```

---

# ⚙️ Stack Tecnológico

| Tecnología          | Uso                      |
| ------------------- | ------------------------ |
| Python              | Lenguaje principal       |
| python-telegram-bot | Framework Telegram       |
| APScheduler         | Scheduler de tareas      |
| SQLAlchemy          | ORM                      |
| PostgreSQL          | Base de datos producción |
| SQLite              | Desarrollo local         |
| Railway             | Deploy cloud             |
| python-dotenv       | Variables de entorno     |
| pytz                | Manejo de timezone       |

---

# 🚀 Instalación Local

## 1️⃣ Clonar repositorio

```bash
git clone https://github.com/MitoNacho/telegram-reminder-bot.git
cd telegram-reminder-bot
```

---

## 2️⃣ Crear entorno virtual

### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

### Linux / macOS

```bash
python3 -m venv venv
source venv/bin/activate
```

---

## 3️⃣ Instalar dependencias

```bash
pip install -r requirements.txt
```

---

## 4️⃣ Crear archivo `.env`

```env
BOT_TOKEN=TU_TOKEN_TELEGRAM
DATABASE_URL=sqlite:///reminders.db
```

---

## 5️⃣ Ejecutar proyecto

```bash
python -m app.main
```

---

# 🤖 Comandos del Bot

| Comando   | Descripción                  |
| --------- | ---------------------------- |
| `/start`  | Iniciar bot                  |
| `/cancel` | Cancelar conversación actual |

---

# 💬 Flujo del Bot

## ➕ Crear Recordatorio

```text
Usuario pulsa ➕ Añadir recordatorio
        ↓
Introducir asunto
        ↓
Introducir fecha
        ↓
Introducir hora
        ↓
Confirmar recordatorio
        ↓
Guardar en base de datos
        ↓
Programar jobs APScheduler
```

---

# 🔔 Sistema de Recordatorios

Cada recordatorio crea:

## ⏰ Aviso 1 hora antes

```text
⏰ Recordatorio en 1 hora
```

---

## 🚨 Aviso exacto

```text
🚨 Recordatorio
```

Después del aviso exacto:

✅ La cita se elimina automáticamente de la base de datos.

---

# 🔄 Persistencia del Scheduler

El proyecto restaura automáticamente los jobs tras reinicios de Railway.

Flujo:

```text
Railway reinicia
      ↓
Leer reminders desde PostgreSQL
      ↓
Recrear jobs APScheduler
      ↓
Continuar ejecución normal
```

---

# ☁️ Deploy en Railway

## Crear proyecto Railway

1. Crear cuenta en Railway
2. Conectar repositorio GitHub
3. Añadir plugin PostgreSQL
4. Configurar variables de entorno
5. Deploy automático

---

## Variables de entorno Railway

```env
BOT_TOKEN=TU_BOT_TOKEN
DATABASE_URL=AUTOMÁTICA_DE_RAILWAY
```

---

# 🧪 Ejemplo Conversación

```text
Usuario:
➕ Añadir recordatorio

Bot:
Escribe el asunto del recordatorio:

Usuario:
Cita dentista

Bot:
Escribe la fecha (DD/MM/YYYY)

Usuario:
20/05/2026

Bot:
Escribe la hora (HH:MM)

Usuario:
18:30

Bot:
Confirma el recordatorio
```

---

# 🛡️ Validaciones Actuales

* Validación asunto vacío
* Validación fecha inválida
* Validación hora inválida
* Protección contra fechas pasadas
* Cancelación de conversaciones
* Prevención de jobs duplicados

---

# 📌 Funcionalidades Producción

## ✅ Incluidas

* Scheduler async
* PostgreSQL
* Deploy Railway
* Restauración de jobs
* Limpieza automática
* Manejo de timezone
* Logs
* Multiusuario

---


# 🧑‍💻 Workflow Desarrollo

```bash
git add .
git commit -m "nombre feature"
git push
```

Railway redeploya automáticamente tras cada push.

---

# 📚 Qué puedes aprender con este proyecto

Este proyecto demuestra:

* Arquitectura limpia en Python
* Desarrollo async con Telegram
* Integración SQLAlchemy
* Uso de APScheduler
* PostgreSQL en producción
* Deploy cloud en Railway
* Separación de responsabilidades
* Jobs persistentes
* Sistemas multiusuario

---

# 👨‍💻 Autor

Desarrollado por Nacho Naves con Python, Telegram Bot API y APScheduler.

---

<div align="center">

## ⭐ Si te gusta el proyecto, considera darle una estrella al repositorio.

</div>
