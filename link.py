import requests
from bs4 import BeautifulSoup, NavigableString
import sys
import string

# Your existing function to check if a word exists on Wiktionary
def check_wiktionary_entry(word, lang='en') -> bool:
    url = f"https://{lang}.wiktionary.org/w/api.php"
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
    
    return 'missing' not in page  # Returns True if word exists, False if 'missing' is in the page


# Function to update HTML content with links to Wiktionary
def update_html_with_wiktionary_links(html_file_path: str):
    # Read the HTML content
    with open(html_file_path, 'r', encoding='utf-8') as file:
        soup = BeautifulSoup(file, 'html.parser')
    
    # Find all paragraphs in the HTML (assuming your poem is in a <p> tag)
    paragraphs = soup.find_all('p')
    
    for paragraph in paragraphs:
        words = paragraph.get_text().split()  # Split text into words
        new_content = []

        for word in words:
            # Check if the word exists on Wiktionary
            stripped = word.strip(string.punctuation)
            if check_wiktionary_entry(stripped):
                link_tag = soup.new_tag('a', href=f"https://en.wiktionary.org/wiki/{stripped}", target="_blank")
                link_tag.string = word
                new_content.append(link_tag)
                new_content.append(NavigableString(" "))
            elif check_wiktionary_entry(stripped, 'ka'):
                link_tag = soup.new_tag('a', href=f"https://ka.wiktionary.org/wiki/{stripped}", target="_blank")
                link_tag.string = word
                new_content.append(link_tag)
                new_content.append(NavigableString(" "))
            else:
                new_content.append(NavigableString(f"{word} "))

        # Clear the current paragraph content
        paragraph.clear()

        # Rebuild the paragraph with the new content (words and links)
        for content in new_content:
            paragraph.append(content)
    
    # Write the updated HTML content back to the file
    with open(html_file_path, 'w', encoding='utf-8') as file:
        file.write(str(soup))


def main():
    # # Read in command line args
    if len(sys.argv) != 2:
        print("Usage: python link.py <html_file_path>")
        sys.exit(1)

    html_file_path = sys.argv[1]
    update_html_with_wiktionary_links(html_file_path)    
    print(f"Links to Wiktionary have been added to the HTML file: {html_file_path}")

    # print(check_wiktionary_entry('ყოფილა', 'ka'))

if __name__ == "__main__":
    main()