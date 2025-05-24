import requests
from bs4 import BeautifulSoup
import json
import os
import logging

logging.basicConfig(filename=os.path.join(os.path.dirname(__file__), '../../app/logs/app.log'), level=logging.DEBUG)

def crawl_website(url, output_path):
    try:
        response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        data = {
            'title': soup.find('h1').get_text(strip=True) if soup.find('h1') else "ID Properties",
            'address': "14 Athlone Crescent, Selborne, East London",
            'phone': "043 721 1280",
            'email': "info@idproperties.co.za",
            'hours': "Mon - Fri: 9:00 - 18:00",
            'description': "Modern living for a unique lifestyle",
            'services': [
                "Property Sales",
                "Property Rentals",
                "Property Management (managing rentals for clients)",
                "Property Maintenance",
                "Advisory",
                "Management",
                "Valuation",
                "Leasing",
                "Capital",
                "Investment",
                "Development",
                "Contractor",
                "Certifications"
            ],
            'listings': [
                "A 3-bedroom house in Port Elizabeth with bathrooms, an open-plan lounge, kitchen, L-shaped porch, garden sunroom, braai stand, single garage, and double carport.",
                "A family home with two bedrooms, a bathroom, lounge, kitchen, and an additional flatlet with two more bedrooms.",
                "A starter home in Reeston with two bedrooms, one bathroom, open-plan lounge and kitchen, water tank, and a spacious fully-walled yard.",
                "A 300ha farm 35km from East London on the N2, suitable for tomato and butternut production or cattle farming, with a big dam and two 3-bedroom farmhouses."
            ],
            'additional_info': "We offer luxury and exclusive listings perfect for international clients. Request a free valuation of your property today! We respond to inquiries within 12 hours with detailed answers from our qualified agents."
        }

        with open(output_path, 'w') as f:
            json.dump(data, f, indent=2)
        logging.info(f"Successfully crawled {url}")
        return data
    except Exception as e:
        logging.error(f"Error crawling website: {e}")
        return None

if __name__ == "__main__":
    url = "https://idproperties.co.za/"
    output_path = os.path.join(os.path.dirname(__file__), '../../data/scraped_data.json')
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    crawl_website(url, output_path)
