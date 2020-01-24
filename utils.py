def safe_add(v1, v2):
    if v1 == "undefined" or v2 == "undefined":
        return "undefined"

    if not v1 or not v2: #if either is None
        return None

    return v1 + v2
