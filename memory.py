conversation_state = {}

def set_state(key, value):
    conversation_state[key] = value

def get_state(key):
    return conversation_state.get(key)

def clear_state():
    conversation_state.clear()
