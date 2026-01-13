"""from flask import Flask, render_template, request, jsonify
from datetime import datetime, timedelta

from intent_classifier import predict_intent
from task_manager import add_task
from time_extractor import extract_time
from web_search import web_search
from summarizer import summarize_text
from day_planner import extract_time_range, plan_day
from memory import set_state, get_state, clear_state


app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    user_input = request.json.get("message", "").strip()
    user_input_l = user_input.lower()

    # ================================
    # FOLLOW-UP HANDLING (MEMORY)
    # ================================

    pending = get_state("pending")

    # Waiting for planner time range
    if pending == "plan_day":
        start, end = extract_time_range(user_input_l)

        if not start or not end:
            return jsonify({"reply": "Please give time range like: 9 am to 6 pm"})

        plan = plan_day(start, end)
        clear_state()
        return jsonify({"reply": plan})

    # Waiting for reminder time
    if pending == "schedule_task":
        time_str = extract_time(user_input_l)

        if not time_str:
            return jsonify({"reply": "Please tell me the time (e.g., 6 pm)."})

        task = get_state("task")
        hour, minute = map(int, time_str.split(":"))
        now = datetime.now()
        run_time = now.replace(hour=hour, minute=minute, second=0, microsecond=0)
        if run_time <= now:
            run_time += timedelta(days=1)

        add_task(task, run_time)
        clear_state()
        return jsonify({"reply": f"✅ Reminder set for {run_time.strftime('%I:%M %p')}"})

    # Waiting for summarize text
    if pending == "summarize":
        clear_state()
        summary = summarize_text(user_input)
        return jsonify({"reply": "🧠 SUMMARY:\n" + summary})

    # ================================
    # NORMAL INTENT DETECTION
    # ================================

    # Planner always highest priority
    if "plan my day" in user_input_l or "make my day" in user_input_l:
        start, end = extract_time_range(user_input_l)

        if not start or not end:
            set_state("pending", "plan_day")
            return jsonify({"reply": "📅 What time range? (e.g., 9 am to 6 pm)"})

        plan = plan_day(start, end)
        return jsonify({"reply": plan})

    intent, response = predict_intent(user_input_l)

    # ================================
    # REMINDER
    # ================================
    if intent == "schedule_task":
        time_str = extract_time(user_input_l)

        if not time_str:
            set_state("pending", "schedule_task")
            set_state("task", user_input)
            return jsonify({"reply": "⏰ When should I remind you?"})

        hour, minute = map(int, time_str.split(":"))
        now = datetime.now()
        run_time = now.replace(hour=hour, minute=minute, second=0, microsecond=0)
        if run_time <= now:
            run_time += timedelta(days=1)

        add_task(user_input, run_time)
        return jsonify({"reply": f"✅ Reminder set for {run_time.strftime('%I:%M %p')}"})

    # ================================
    # 🌐 WEB SEARCH (RAG STYLE)
    # ================================
    if intent == "web_search":
        docs = web_search(user_input_l)

        if not docs:
            return jsonify({"reply": "I couldn’t find useful information."})

        combined = " ".join(docs[:3])   # merge top 3 sources
        answer = summarize_text(combined)

        return jsonify({
            "reply": "📰 " + answer
        })


    # ================================
    # SUMMARIZE
    # ================================
    if intent == "summarize":
        if len(user_input.split()) < 3:
            set_state("pending", "summarize")
            return jsonify({"reply": "📄 Please paste the text you want summarized."})

        summary = summarize_text(user_input)
        return jsonify({"reply": "🧠 SUMMARY:\n" + summary})

    # ================================
    # DEFAULT CHAT
    # ================================
    return jsonify({"reply": response})

if __name__ == "__main__":
    app.run(debug=True)"""
    

from flask import Flask, render_template, request, jsonify
from datetime import datetime, timedelta

from intent_classifier import predict_intent
from task_manager import add_task
from time_extractor import extract_time
from web_search import web_search
from summarizer import summarize_text
from day_planner import extract_time_range, plan_day
from memory import set_state, get_state, clear_state

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    user_input = request.json.get("message", "").strip()
    user_input_l = user_input.lower()

    if not user_input:
        return jsonify({"reply": "Please type something."})

    # ================================
    # 🔁 FOLLOW-UP HANDLING (MEMORY)
    # ================================

    pending = get_state("pending")

    if pending == "plan_day":
        start, end = extract_time_range(user_input_l)
        if not start or not end:
            return jsonify({"reply": "Please give time range like: 9 am to 6 pm"})
        plan = plan_day(start, end)
        clear_state()
        return jsonify({"reply": plan})

    if pending == "schedule_task":
        time_str = extract_time(user_input_l)
        if not time_str:
            return jsonify({"reply": "Please tell me the time (e.g., 6 pm)."})
        task = get_state("task")
        hour, minute = map(int, time_str.split(":"))
        now = datetime.now()
        run_time = now.replace(hour=hour, minute=minute, second=0, microsecond=0)
        if run_time <= now:
            run_time += timedelta(days=1)
        add_task(task, run_time)
        clear_state()
        return jsonify({"reply": f"✅ Reminder set for {run_time.strftime('%I:%M %p')}"})

    if pending == "summarize":
        clear_state()
        summary = summarize_text(user_input)
        return jsonify({"reply": "🧠 SUMMARY:\n" + summary})

    # ================================
    # 🔍 HARD RULES (Search & Planner)
    # ================================

    SEARCH_KEYWORDS = ["news", "latest", "information", "about", "who is", "what is"]

    if any(k in user_input_l for k in SEARCH_KEYWORDS):
        intent = "web_search"
    elif "plan my day" in user_input_l or "make my day" in user_input_l:
        intent = "plan_day"
    else:
        intent, response = predict_intent(user_input_l)

    # ================================
    # 📅 DAY PLANNER
    # ================================
    if intent == "plan_day":
        start, end = extract_time_range(user_input_l)
        if not start or not end:
            set_state("pending", "plan_day")
            return jsonify({"reply": "📅 What time range? (e.g., 9 am to 6 pm)"})
        plan = plan_day(start, end)
        return jsonify({"reply": plan})

    # ================================
    # ⏰ REMINDER
    # ================================
    if intent == "schedule_task":
        time_str = extract_time(user_input_l)
        if not time_str:
            set_state("pending", "schedule_task")
            set_state("task", user_input)
            return jsonify({"reply": "⏰ When should I remind you?"})
        hour, minute = map(int, time_str.split(":"))
        now = datetime.now()
        run_time = now.replace(hour=hour, minute=minute, second=0, microsecond=0)
        if run_time <= now:
            run_time += timedelta(days=1)
        add_task(user_input, run_time)
        return jsonify({"reply": f"✅ Reminder set for {run_time.strftime('%I:%M %p')}"})

    # ================================
    # 🌐 WEB SEARCH (RAG)
    # ================================
    if intent == "web_search":
        docs = web_search(user_input_l)
        if not docs:
            return jsonify({"reply": "I couldn’t find useful information."})
        combined = " ".join(docs[:3])
        answer = summarize_text(combined)
        return jsonify({"reply": "📰 " + answer})

    # ================================
    # 🧠 SUMMARIZE
    # ================================
    if intent == "summarize":
        if len(user_input.split()) < 3:
            set_state("pending", "summarize")
            return jsonify({"reply": "📄 Please paste the text you want summarized."})
        summary = summarize_text(user_input)
        return jsonify({"reply": "🧠 SUMMARY:\n" + summary})

    # ================================
    # 💬 DEFAULT CHAT
    # ================================
    return jsonify({"reply": response})

if __name__ == "__main__":
    app.run(debug=True)

