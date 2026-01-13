import re

def extract_time(text):
    match = re.search(r'(\d{1,2})\s*(:)?\s*(\d{2})?\s*(am|pm)?', text.lower())
    
    if not match:
        return None

    hour = int(match.group(1))
    minute = int(match.group(3)) if match.group(3) else 0
    period = match.group(4)

    if period == "pm" and hour != 12:
        hour += 12
    if period == "am" and hour == 12:
        hour = 0

    return f"{hour:02d}:{minute:02d}"
