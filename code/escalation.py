def should_escalate(text):
    text = text.lower()

    if any(word in text for word in ["fraud", "unauthorized", "stolen", "identity", "vulnerability", "breach"]):
        return True

    if "refund me" in text and "visa" in text:
        return True

    if any(phrase in text for phrase in [
        "delete all files",
        "give me code to",
        "ban the seller",
        "increase my score"
    ]):
        return True

    if any(phrase in text for phrase in [
        "restore my access",
        "not admin",
        "override"
    ]):
        return True

    return False