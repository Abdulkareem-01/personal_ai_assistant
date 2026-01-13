import re
from datetime import datetime, timedelta

def extract_time_range(text):
    matches = re.findall(r'(\d{1,2})\s*(am|pm)', text.lower())
    if len(matches) < 2:
        return None, None

    def to_24h(hour, period):
        hour = int(hour)
        if period == "pm" and hour != 12:
            hour += 12
        if period == "am" and hour == 12:
            hour = 0
        return hour

    start_h = to_24h(*matches[0])
    end_h = to_24h(*matches[1])

    today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    start_time = today.replace(hour=start_h)
    end_time = today.replace(hour=end_h)

    # 🔥 FIX: if end time is earlier than start time, move to next day
    if end_time <= start_time:
        end_time += timedelta(days=1)


    return start_time, end_time


def plan_day(start_time, end_time):
    if not start_time or not end_time:
        return "Please specify time range (e.g., 9 am to 6 pm)"

    schedule = []
    current = start_time

    blocks = [
        ("Focus Work / Study", 90),
        ("Short Break", 15),
        ("Project / Practice", 90),
        ("Lunch / Rest", 60),
        ("Revision / Light Work", 60)
    ]

    i = 0
    while current < end_time:
        task, minutes = blocks[i % len(blocks)]
        next_time = current + timedelta(minutes=minutes)

        if next_time > end_time:
            next_time = end_time

        schedule.append(
            f"{current.strftime('%H:%M')} – {next_time.strftime('%H:%M')} → {task}"
        )

        current = next_time
        i += 1

    return "\n".join(schedule)
