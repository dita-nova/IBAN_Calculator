from bs4 import BeautifulSoup
import requests

def get_website_code():
    url = "https://www.cnb.cz/cs/platebni-styk/iban/kalkulator-iban-ceska-republika/"
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
    
    # Fetch HTML content
    response = requests.get(url, headers=headers)
    content = response.text

    # Parse HTML with BeautifulSoup
    soup = BeautifulSoup(content, 'html.parser')

    save_to_file(content)

def save_to_file(content, filename='code.html'):
    with open(filename, 'w', encoding='utf-8') as file:
        file.write(content)
    print(f"Content saved to {filename}")

if __name__ == "__main__":
    get_website_code()
