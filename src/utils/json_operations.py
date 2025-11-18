import json

def read_jsonl_file(filepath):
    data = []
    with open(filepath, 'r', encoding='utf-8') as f:
        for line in f:
            json_data = json.loads(line)
            data.append(json_data['canonical_smiles'])
    return data