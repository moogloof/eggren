# Imports
from bs4 import BeautifulSoup
import requests
import sys
import pickle


# Scrape queue
descriptions = []

# Extract data
def extract(element):
    # Status message
    print("Checking card: {}".format(element.find(attrs={"class": "link-title"}).text))

    # Parse text for description (synopsis)
    soup = element
    desc = soup.find(attrs={"class": "preline"}).text

    return desc

# Get all related anime
def scrape(url):
    # Content
    content = []

    # Status message
    print(f"Scraping page: {url}")

    try:
        # Check and request the url
        response = requests.get(url)

        # Exit if response is 404
        if response.status_code == 404:
            return False
    except:
        # Pass if request error arises
        pass
    else:
        # Parse text for urls
        soup = BeautifulSoup(response.text)
        cards = soup.body.findAll(attrs={"class": "seasonal-anime"})

        for card in cards:
            content.append(extract(card))

    print(f"Finished scraping: {url}")

    return content


if __name__ == "__main__":
    print("Started scraping.")

    # Scrape pages of genre
    page_i = 1

    # Page scrape loop  
    while True:
        # Get url
        url = f"https://myanimelist.net/anime/genre/1/Action?page={page_i}"

        # Scrape url page
        page_scrape = scrape(url)

        # Break on 404
        if not page_scrape:
            break

        # Add to descriptions
        descriptions += page_scrape

        page_i += 1

    print("Done scraping.")
    print("Saving scraped data.")

    with open("./desc_data", "wb") as f:
        pickle.dump(descriptions, f)

    print("Finished saving scraped data.")
    
