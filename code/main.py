import pandas as pd
from classifier import classify
from escalation import should_escalate
from retriever import load_documents, build_embeddings, retrieve

def build_justification(request_type, product_area, escalate, score):
    if escalate:
        return f"Escalated due to high-risk or restricted request. Classified as {request_type}/{product_area}."
    return f"Replied using semantic retrieval (similarity score={score:.2f}). Classified as {request_type}/{product_area}."

def format_response(doc):
    lines = doc.split("\n")
    clean_lines = []

    for line in lines:
        line = line.strip()
        if (
            line and
            not line.startswith("---") and
            "title:" not in line.lower() and
            "source_url" not in line.lower() and
            "final_url" not in line.lower() and
            "last_modified" not in line.lower() and
            "description:" not in line.lower()
        ):
            clean_lines.append(line)

    result = " ".join(clean_lines[:8])
    if len(result.split()) < 6:
        return ""
    return result

def main():
    df = pd.read_csv("../support_tickets/support_tickets.csv")
    documents = load_documents("../data")
    doc_embeddings = build_embeddings(documents)

    results = []

    for _, row in df.iterrows():
        issue = row["Issue"]

        request_type, product_area = classify(issue)

        escalate = should_escalate(issue)
        status = "escalated" if escalate else "replied"

        doc, score = retrieve(issue, documents, doc_embeddings)

        if escalate:
            response = "This issue involves sensitive or restricted actions and has been escalated to our support team."
        else:
            if doc:
                formatted = format_response(doc)
                if formatted:
                    response = f"Based on our support documentation:\n\n{formatted}"
                else:
                    response = "We could not find sufficient information in the help center. Escalating to support."
                    status = "escalated"
            else:
                response = "We could not find relevant information in the help center. Escalating to support."
                status = "escalated"

        if status == "escalated" and not escalate:
            justification = f"Escalated due to low retrieval confidence (score={score:.2f}). Classified as {request_type}/{product_area}."
        else:
            justification = build_justification(request_type, product_area, escalate, score)

        results.append({
            "status": status,
            "product_area": product_area,
            "response": response,
            "justification": justification,
            "request_type": request_type
        })

    output_df = pd.DataFrame(results)
    output_df.to_csv("../support_tickets/output.csv", index=False)

if __name__ == "__main__":
    main()