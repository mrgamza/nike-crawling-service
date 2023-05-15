def to_boolean(value):
    if type(value) is bool:
        return value
    lower = value.lower()
    if lower == 'true':
        return True
    elif lower == 'false':
        return False
    return False
