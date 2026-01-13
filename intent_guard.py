def validate_intent(intent, user_input, extracted):
    if intent == "schedule_task":
        if not extracted.get("time"):
            return False, "⏰ When should I remind you? (e.g., 6 pm)"

    if intent == "summarize":
        if not extracted.get("text"):
            return False, "📄 Please paste the text you want me to summarize."

    if intent == "web_search":
        if len(user_input.split()) < 3:
            return False, "🔍 What should I search for?"

    if intent == "plan_day":
        if not extracted.get("start") or not extracted.get("end"):
            return False, "📅 Please specify a time range (e.g., 9 am to 6 pm)."

    return True, None
