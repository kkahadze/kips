import requests

def check_wiktionary_entry(word):
    url = "https://en.wiktionary.org/w/api.php"
    params = {
        "action": "query",
        "format": "json",
        "titles": word,
        "redirects": 1
    }
    
    response = requests.get(url, params=params)
    data = response.json()
    
    pages = data['query']['pages']
    page = next(iter(pages.values()))  # Get the first page result
    
    if 'missing' in page:
        return f"The word '{word}' does not exist on Wiktionary."
    else:
        return f"The word '{word}' exists on Wiktionary with page ID: {page['pageid']}."

word = "გონება"
print(check_wiktionary_entry(word))
