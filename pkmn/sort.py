import json

def sort_json_urls(file_path):
    with open(file_path, mode='r', encoding='utf-8') as file:
        data = json.load(file)
    
    for entry in data:
        if 'urls' in entry:
            entry['urls'].sort() 
            
    with open(file_path, mode='w', encoding='utf-8') as file:
        json.dump(data, file, indent=4)

if __name__ == "__main__":
    sort_json_urls('rarity_links.json')
