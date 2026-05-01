# Support Triage Agent

## Overview

This project implements a terminal-based support triage agent that processes support tickets across multiple domains (HackerRank, Claude, Visa).
The agent classifies each ticket, determines whether it can be safely answered, retrieves relevant documentation from the provided corpus, and generates a grounded response or escalates the case when necessary.

---

## How to Run

1. Navigate to the `code/` directory:

```bash
cd code
```

2. Install required dependencies:

```bash
pip install pandas sentence-transformers torch
```

3. Run the agent:

```bash
python main.py
```

4. Output will be generated at:

```
support_tickets/output.csv
```

---

## Project Structure

```
code/
├── main.py            # Orchestrates full pipeline
├── classifier.py      # Classification logic
├── escalation.py      # Escalation rules
├── retriever.py       # Semantic retrieval
├── README.md
```

---

## Approach

### 1. Classification
A rule-based classifier assigns:
- `request_type` (product_issue, bug, feature_request, invalid)
- `product_area` (billing, technical, account, security, general)

Rules are ordered by priority to improve accuracy.

---

### 2. Escalation Logic
The agent escalates:
- High-risk cases (fraud, identity, security)
- Unsupported or restricted requests
- Low-confidence retrieval cases

This ensures safe and reliable handling.

---

### 3. Retrieval (Semantic Search)
- Uses `sentence-transformers` (MiniLM model)
- Documents are split into chunks
- Embeddings are generated
- Cosine similarity is used for matching

A confidence threshold ensures only strong matches are used.

---

### 4. Response Generation
- Responses are strictly based on retrieved corpus content
- Metadata (titles, URLs, etc.) is removed
- Weak or empty outputs are discarded and escalated instead

---

### 5. Justification
Each output includes:
- Reason for escalation or reply
- Similarity score (for transparency)

---

## Design Decisions

- Rule-based classification for determinism
- Semantic retrieval for better relevance
- Confidence thresholding to avoid weak responses
- Escalation-first design for safety

---

## Limitations

- Rule-based classification may miss edge cases
- Retrieval depends on embedding quality
- No advanced reranking beyond similarity score

---

## Future Improvements

- Domain-aware retrieval
- Hybrid (keyword + semantic) search
- ML-based classification
- Better response summarization

---

## Key Highlights

- No hallucination (strict corpus usage)
- Strong safety via escalation
- Semantic retrieval
- Clean and modular design