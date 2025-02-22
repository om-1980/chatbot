from speech_to_text import listen_and_transcribe
from nlu import extract_intent, extract_entities
from response_generator import generate_response
from text_to_speech import speak_text
from backend import init_db, log_interaction

def main():
    init_db()
    
    print("Welcome to the Intelligent Voice Bot. Say 'exit' to quit.")
    
    while True:
        user_text = listen_and_transcribe()
        if user_text.lower() == "exit":
            print("Exiting the Voice Bot. Goodbye!")
            break
        
        if not user_text:
            continue 
        
        # Process Natural Language Understanding (NLU)
        intent = extract_intent(user_text)
        entities = extract_entities(user_text)
        
        # Generate a response based on the user's query
        response_text = generate_response(intent, entities, user_text)
        print("Bot:", response_text)
        
        # Log the interaction in the database
        log_interaction(user_text, intent, response_text)
        
        # Use text-to-speech to speak out the response
        speak_text(response_text)
        
        print("\n--- Ready for the next query ---\n")

if __name__ == "__main__":
    main()
