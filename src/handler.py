import torch
import runpod
from runpod.serverless.utils.rp_validator import validate
from transformers import AutoModelForSequenceClassification, AutoTokenizer, pipeline

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

print(device)
INPUT_SCHEMA = {
    'sequence': {
        'type': str,
        'required': True
    },
    'labels': {
        'type': list,
        'required': True,
    }
}

def classify_text(sequence, labels):
    model = AutoModelForSequenceClassification.from_pretrained(
        "facebook/bart-large-mnli",
        local_files_only=False  # Change this to False to download if not available locally
    ).to(device)
    tokenizer = AutoTokenizer.from_pretrained(
        "facebook/bart-large-mnli", local_files_only=False)  # Change this to False to download if not available locally

    classifier = pipeline(
        "zero-shot-classification",
        model=model,
        tokenizer=tokenizer,
        device=0,
    )

    return classifier(sequence, labels, multi_label=True)

async def handler(job):
    val_input = validate(job['input'], INPUT_SCHEMA)
    if 'errors' in val_input:
        return {"error": val_input['errors']}
    val_input = val_input['validated_input']

    classification_result = classify_text(val_input["sequence"], val_input["labels"])
    
    return {
        "classification_result": classification_result,
        "device": str(device)
    }

runpod.serverless.start({"handler": handler, "concurrency_modifier": lambda x: 1000})
