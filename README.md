# Vuyiswa ID Properties Chatbot

This is a chatbot for ID Properties, a real estate agency in East London, South Africa. The chatbot, named after agent Vuyiswa Sauli-Mkhokeli, assists users with property inquiries, including sales, rentals, and management services in East London and Cintsa.

## Project Structure
```
vuyiswa-idproperties-chatbot/
├── app/
│   ├── backend/
│   │   ├── crawler.py      # Web crawler for scraping website data
│   │   └── backend.py      # Flask backend for handling API requests
│   ├── frontend/
│   │   ├── static/
│   │   │   ├── images/     # Static images (agent.jpg, banner.jpg, logo.png)
│   │   │   └── favicon.ico # Favicon for the website
│   │   └── templates/
│   │       └── index.html  # React-based frontend
│   └── logs/               # Application logs (ignored by .gitignore)
├── scripts/
│   └── ngrok               # ngrok binary for public access
├── data/                   # Scraped data (ignored by .gitignore)
├── .gitignore              # Git ignore file
├── README.md               # Project documentation
└── requirements.txt        # Python dependencies
```

## Features
- Chat interface to answer property-related questions.
- URL scraping to extract data from websites.
- File upload support for text and PDF files.
- Responsive design with a professional UI.

## Prerequisites
- Python 3.x
- Git
- Ollama (for LLM functionality)
- ngrok (for public access)

## Setup
1. Clone the repository:
   ```bash
   git clone https://github.com/Razworld00/vuyiswa-idproperties-chatbot.git
   cd vuyiswa-idproperties-chatbot
   ```
2. Install dependencies:
   ```bash
   sudo swupd bundle-add python3-basic wget
   pip3 install -r requirements.txt --user
   ```
3. Start the Ollama service:
   ```bash
   ollama serve &
   ```
4. Run the web crawler to scrape data:
   ```bash
   python3 app/backend/crawler.py
   ```
5. Start the Flask server:
   ```bash
   python3 app/backend/backend.py &
   ```
6. Access the chatbot locally at `http://localhost:5001`.
7. (Optional) Expose the chatbot publicly using ngrok:
   ```bash
   ./scripts/ngrok http 5001
   ```
   - Copy the public URL (e.g., `https://abc123.ngrok.io`) and access it in your browser.

## Contact
- **Agent**: Vuyiswa Sauli-Mkhokeli (vuyiswa@idproperties.co.za, 066 085 8828)
- **Developer**: Raznet Solutions (bathie28@gmail.com)
