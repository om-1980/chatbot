from transformers import pipeline
import re

# Initialize the Hugging Face pipelines once
intent_classifier = pipeline(
    "zero-shot-classification",
    model="facebook/bart-large-mnli"
)

# Named Entity Recognition (NER) pipeline.
ner_pipeline = pipeline(
    "ner",
    model="dbmdz/bert-large-cased-finetuned-conll03-english",
    aggregation_strategy="simple"
)

def extract_intent(text):
    candidate_labels = ["account query", "order query", "support query", "general query"]
    result = intent_classifier(text, candidate_labels)
    top_intent = result["labels"][0] 
    normalized_intent = top_intent.replace(" ", "_")
    return normalized_intent

def extract_entities(text):
    ner_results = ner_pipeline(text)
    entities = {}
    
    for entity in ner_results:
        group = entity["entity_group"]  # e.g., "PER", "ORG", "LOC"
        word = entity["word"].strip()
        if group in entities:
            entities[group].append(word)
        else:
            entities[group] = [word]
    
    # Look for sequences of 5 or more digits
    account_nums = re.findall(r'\b\d{5,}\b', text)
    if account_nums:
        if "ACCOUNT_NUMBER" in entities:
            entities["ACCOUNT_NUMBER"].extend(account_nums)
        else:
            entities["ACCOUNT_NUMBER"] = account_nums
    
    return entities

if __name__ == "__main__":
    sample_text = "Hi, I need help with my account number 123456 and I also want to know the status of my order."
    intent = extract_intent(sample_text)
    entities = extract_entities(sample_text)
    
    print("Detected Intent:", intent)
    print("Detected Entities:", entities)
