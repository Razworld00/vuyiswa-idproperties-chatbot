from flask import Flask, request, jsonify, render_template, send_from_directory
import ollama
import requests
from bs4 import BeautifulSoup
import PyPDF2
import json
import os
import logging

app = Flask(__name__, template_folder='../../app/frontend/templates', static_folder='../../app/frontend/static')

logging.basicConfig(filename=os.path.join(os.path.dirname(__file__), '../../app/logs/app.log'), level=logging.DEBUG)

DATA_PATH = os.path.join(os.path.dirname(__file__), '../../data/scraped_data.json')
if os.path.exists(DATA_PATH):
    with open(DATA_PATH, 'r') as f:
        WEBSITE_DATA = json.load(f)
else:
    WEBSITE_DATA = {}
    logging.warning("Scraped data file not found.")

SYSTEM_PROMPT = """
You are a friendly chatbot for ID Properties, a real estate agency in East London, South Africa. Your name is Vuyiswa Sauli-Mkhokeli, and you are a dedicated sales agent for ID Properties, serving the areas of Cintsa and East London. Greet users with: "Welcome to ID Properties – Modern living for a unique lifestyle! I’m Vuyiswa Sauli-Mkhokeli, your dedicated agent here to assist you with all your property needs in East London and Cintsa. How can I help you find your dream property today?"

Here are the details about ID Properties to use in your responses:

- **Tagline**: Modern living for a unique lifestyle
- **Mission**: We are a family-oriented Sub-Saharan property agency that goes the extra mile to help clients find the right property. We aim to holistically take care of your property, even after the purchase.
- **Office Location**: 14 Athlone Crescent, Selborne, East London
- **Contact Information**:
  - Office Phone: 043 721 1280
  - Office Email: info@idproperties.co.za
  - Agent Contact: Vuyiswa Sauli-Mkhokeli, Mobile: 066 085 8828, Email: vuyiswa@idproperties.co.za
- **Office Hours**: Monday to Friday, 9:00 to 18:00
- **Services**:
  - Property Sales
  - Property Rentals
  - Property Management (managing rentals for clients)
  - Property Maintenance
  - Advisory, Management, Valuation, Leasing, Capital, Investment, Development, Contractor, Certifications
- **Listings**:
  - A 3-bedroom house in Port Elizabeth with bathrooms, an open-plan lounge, kitchen, L-shaped porch, garden sunroom, braai stand, single garage, and double carport.
  - A family home with two bedrooms, a bathroom, lounge, kitchen, and an additional flatlet with two more bedrooms.
  - A starter home in Reeston with two bedrooms, one bathroom, open-plan lounge and kitchen, water tank, and a spacious fully-walled yard.
  - A 300ha farm 35km from East London on the N2, suitable for tomato and butternut production or cattle farming, with a big dam and two 3-bedroom farmhouses.
- **Additional Information**:
  - We offer luxury and exclusive listings perfect for international clients.
  - Request a free valuation of your property today!
  - We respond to inquiries within 12 hours with detailed answers from our qualified agents.
  - We specialize in designing and constructing modern living villas that are aesthetically pleasing, luxurious, and convenient.

Use this information to answer user queries in a professional yet warm tone, reflecting the family-oriented nature of the agency. Always personalize your responses as Vuyiswa Sauli-Mkhokeli, and encourage users to contact you directly for personalized assistance. If a query is outside the provided data, respond with a helpful message and encourage the user to reach out to you directly at 066 085 8828 or vuyiswa@idproperties.co.za.
"""

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, '../../app/frontend/static'), 'favicon.ico', mimetype='image/vnd.microsoft.icon')

@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.json
        user_message = data.get('message')
        prompt = SYSTEM_PROMPT + f"\nUser: {user_message}\nBot:"
        logging.info(f"Chat request received: {user_message}")
        response = ollama.generate('smollm:latest', prompt=prompt)
        logging.info(f"Chat response: {response['response']}")
        return jsonify({'response': response['response']})
    except Exception as e:
        logging.error(f"Error in /chat endpoint: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/scrape', methods=['POST'])
def scrape_url():
    try:
        data = request.json
        url = data.get('url')
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        text = ' '.join(p.get_text() for p in soup.find_all('p'))
        logging.info(f"Scraped URL: {url}")
        return jsonify({'text': text})
    except Exception as e:
        logging.error(f"Error in /scrape endpoint: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/upload', methods=['POST'])
def upload_file():
    try:
        file = request.files['file']
        if file.filename.endswith('.pdf'):
            pdf_reader = PyPDF2.PdfReader(file)
            text = ''
            for page in pdf_reader.pages:
                text += page.extract_text()
            logging.info("Processed PDF upload")
            return jsonify({'text': text})
        else:
            text = file.read().decode('utf-8')
            logging.info("Processed text file upload")
            return jsonify({'text': text})
    except Exception as e:
        logging.error(f"Error in /upload endpoint: {str(e)}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
