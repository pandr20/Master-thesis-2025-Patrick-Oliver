import json
import random

system_instruction = {
    "role": "system",
    "parts": [
        {
            "text": "Du er en chatbot for firmaet CJComplex der laver online marketing med fokus på e-commerce og AI hjælpemidler."
        }
    ]
}

with open('../version_1/dataset_3.txt', 'r', encoding='utf-8') as file:
    lines = [line.strip() for line in file if line.strip()]

# Group into (question, answer) pairs
pairs = [(lines[i], lines[i+1]) for i in range(0, len(lines)-1, 3)]

random.shuffle(pairs)
split_idx = int(len(pairs) * 0.9)
train_pairs = pairs[:split_idx]
val_pairs = pairs[split_idx:]

def write_jsonl(pairs, filename):
    with open(filename, 'w', encoding='utf-8') as f:
        for question, answer in pairs:
            entry = {
                "systemInstruction": system_instruction,
                "contents": [
                    {
                        "role": "user",
                        "parts": [{"text": question}]
                    },
                    {
                        "role": "model",
                        "parts": [{"text": answer}]
                    }
                ]
            }
            f.write(json.dumps(entry, ensure_ascii=False) + '\n')

write_jsonl(train_pairs, 'training_dataset.jsonl')
write_jsonl(val_pairs, 'validation_dataset.jsonl')