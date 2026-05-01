def classify(text):
    text = text.lower()
    
    if any(word in text for word in ["refund", "payment", "charge", "invoice", "dispute"]):
        return "product_issue", "billing"

    if any(word in text for word in ["fraud", "stolen", "unauthorized", "vulnerability", "breach", "identity"]):
        return "product_issue", "security"

    if any(word in text for word in ["error", "not working", "failing", "down", "issue", "unable"]):
        return "bug", "technical"

    if any(word in text for word in [
        "access", "login", "password", "account",
        "certificate", "name", "remove", "subscription"
    ]):
        return "product_issue", "account"

    if any(word in text for word in ["feature", "add", "request", "pause"]):
        return "feature_request", "account"

    if "interview" in text or "assessment" in text:
        return "bug", "technical"
    if "claude" in text:
        return "product_issue", "technical"
    if "visa" in text:
        return "product_issue", "billing"
    
    return "invalid", "general"