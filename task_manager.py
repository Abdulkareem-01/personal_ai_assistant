import sqlite3
from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
import time
import pyttsx3
from plyer import notification
from telegram_notifier import send_telegram_message


engine = pyttsx3.init()
engine.setProperty("rate", 160)   # speech speed
engine.setProperty("volume", 1.0)


scheduler = BackgroundScheduler()
scheduler.start()

def add_task(task, run_time):
    conn = sqlite3.connect("tasks.db")
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO tasks (task, run_at) VALUES (?, ?)",
        (task, run_time.isoformat())
    )

    conn.commit()
    conn.close()

    schedule_task(task, run_time)


from datetime import datetime, timedelta

def schedule_task(task, run_time):
    if run_time <= datetime.now():
        return  # ❌ DO NOT reschedule past tasks

    scheduler.add_job(
        notify_task,
        'date',
        run_date=run_time,
        args=[task]
    )

    print(f"✅ Reminder set for {run_time.strftime('%Y-%m-%d %H:%M')}")



from plyer import notification

def notify_task(task):
    print("🔥 notify_task() CALLED")

    # 1️⃣ Telegram (MOST IMPORTANT – send FIRST)
    try:
        send_telegram_message(task)
        print("✅ Telegram message sent")
    except Exception as e:
        print("❌ Telegram failed:", e)

    # 2️⃣ Desktop notification
    try:
        notification.notify(
            title="⏰ AI Assistant Reminder",
            message=task,
            app_name="Personal AI Assistant",
            timeout=10
        )
        print("✅ Desktop notification sent")
    except Exception as e:
        print("❌ Desktop notification failed:", e)

    # 3️⃣ Voice alert
    try:
        engine.say(f"Reminder. {task}")
        engine.runAndWait()
        print("✅ Voice alert played")
    except Exception as e:
        print("❌ Voice alert failed:", e)

    print("🔥 notify_task() COMPLETED\n")






def load_existing_tasks():
    conn = sqlite3.connect("tasks.db")
    cursor = conn.cursor()

    cursor.execute("SELECT task, run_at FROM tasks")
    rows = cursor.fetchall()
    conn.close()

    for task, run_at in rows:
        run_time = datetime.fromisoformat(run_at)
        if run_time > datetime.now():
            schedule_task(task, run_time)

