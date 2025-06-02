import json

# Load JSON file and make a list
with open('mo-customer-support-tweets-945k.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

# Save values as text file
with open('dataset_2.txt', 'w', encoding='utf-8') as file:
    for item in data:
        file.write(f"{item['input']}\n")
        file.write(f"{item['output']}\n")
        file.write('\n\n')