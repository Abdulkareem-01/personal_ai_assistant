import sys
import os
from datetime import datetime, timedelta
from summarizer import summarize_text
from day_planner import extract_time_range, plan_day




# Ensure current directory is in path (Windows fix)
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from intent_classifier import predict_intent
from task_manager import add_task, load_existing_tasks
from time_extractor import extract_time
from web_search import web_search

# Load only FUTURE tasks (no duplicates)
load_existing_tasks()

print("🤖 Personal AI Assistant Started (type 'exit' to quit)")

while True:
    user_input = input("You: ").strip()
    if user_input.lower() == "exit":
        print("👋 Goodbye!")
        break

    intent, response = predict_intent(user_input)
    # 🔥 INTENT OVERRIDE FOR DAY PLANNING
    if "plan my day" in user_input.lower():
        intent = "plan_day"


    # 🔹 PHASE 2 – Task Scheduling
    if intent == "schedule_task":
        time_str = extract_time(user_input)

        if not time_str:
            print("Bot: Please specify time (e.g., remind me at 6 pm)")
            continue

        hour, minute = map(int, time_str.split(":"))
        now = datetime.now()

        run_time = now.replace(
            hour=hour,
            minute=minute,
            second=0,
            microsecond=0
        )

        # ⏭ Schedule for tomorrow if time passed
        if run_time <= now:
            run_time += timedelta(days=1)

        add_task(user_input, run_time)

    # 🔹 PHASE 3 – Web Search
    elif intent == "web_search":
        print("🔎 Searching the web...\n")
        results = web_search(user_input)

        if not results:
            print("Bot: No results found.")
        else:
            for i, r in enumerate(results, 1):
                print(f"{i}. {r['title']}")
                print(f"   {r['body']}")
                print(f"   🔗 {r['link']}\n")
    
    elif intent == "summarize":
        print("✂️ Summarizing...\n")
        print("Paste the text (end with an empty line):")

        lines = []
        while True:
            line = input()
            if line.strip() == "":
                break
            lines.append(line)

        full_text = " ".join(lines)

        summary = summarize_text(full_text)
        print("\n🧠 SUMMARY:")
        print(summary)
    
    elif intent == "plan_day":
        start, end = extract_time_range(user_input)
        plan = plan_day(start, end)
        print("\n📅 YOUR DAY PLAN:")
        print(plan)



    # 🔹 PHASE 1 – Normal Chat
    else:
        print("Bot:", response)


