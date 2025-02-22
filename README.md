# Hablis Hotel Chatbot

## Overview
The **Hablis Hotel Chatbot** is an AI-powered virtual assistant designed to enhance customer engagement by providing quick and efficient responses to guest inquiries. This chatbot assists users with booking details, hotel amenities, dining options, check-in/check-out information, and more.

## Features
- **Greeting & Hospitality Assistance**: Welcomes guests and provides general hotel information.
- **Room Booking Assistance**: Helps users check availability and book rooms.
- **Restaurant & Dining Info**: Offers details about dining options and menus.
- **Facilities & Amenities**: Informs guests about hotel services such as spa, gym, and swimming pool.
- **FAQ Support**: Answers frequently asked questions about the hotel.
- **Voice & Text Interaction**: Supports both voice and text-based communication.

## Technologies Used
- **Python** (Flask, TensorFlow, NLTK)
- **Natural Language Processing (NLP)** for intent recognition
- **Speech-to-Text & Text-to-Speech** for voice interactions
- **Pre-trained BERT Model** for advanced language understanding
- **JSON-based Intent System** for chatbot responses

## Installation & Setup
### Prerequisites
- Python 3.7+
- Virtual Environment (optional but recommended)
- Required Libraries: `tensorflow`, `nltk`, `speechrecognition`, `gtts`, `flask`

### Steps
1. Clone the repository:
   ```sh
   git clone https://github.com/om-1980/hablis-hotel-chatbot.git
   cd hablis-hotel-chatbot
   ```
2. Create and activate a virtual environment:
   ```sh
   python -m venv myenv
   source myenv/bin/activate  # On Windows: myenv\Scripts\activate
   ```
3. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```
4. Train the chatbot model:
   ```sh
   python train_model.py
   ```
5. Run the chatbot:
   ```sh
   python voice_bot_gui.py
   ```

## Usage
- Launch the chatbot, and interact using voice or text.
- Ask about hotel services, booking, dining options, and more.
- The chatbot responds with accurate and helpful information.

## Future Enhancements
- Integration with hotel booking systems.
- Multi-language support.
- Advanced recommendation system for personalized guest experiences.

