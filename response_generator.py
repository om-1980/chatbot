import json
import nltk
import numpy as np
import pickle
import random
import tensorflow as tf
from nltk.stem import WordNetLemmatizer
from tensorflow.keras.models import load_model

lemmatizer = WordNetLemmatizer()
intents = json.load(open('intents.json'))
words = pickle.load(open('words.pkl', 'rb'))
classes = pickle.load(open('classes.pkl', 'rb'))
model = load_model('chatbot_model.h5')

def clean_up_sentence(sentence):
    sentence_words = nltk.word_tokenize(sentence)
    sentence_words = [lemmatizer.lemmatize(word.lower()) for word in sentence_words]
    return sentence_words

def bow(sentence, words):
    sentence_words = clean_up_sentence(sentence)
    bag = [0] * len(words)
    for s in sentence_words:
        for i, w in enumerate(words):
            if w == s:
                bag[i] = 1
    return np.array(bag)

def predict_class(sentence):
    bow_vector = bow(sentence, words)
    res = model.predict(np.array([bow_vector]))[0]
    ERROR_THRESHOLD = 0.25
    results = [[i, r] for i, r in enumerate(res) if r > ERROR_THRESHOLD]
    results.sort(key=lambda x: x[1], reverse=True)
    return_list = []
    for r in results:
        return_list.append({'intent': classes[r[0]], 'probability': str(r[1])})
    return return_list

def get_response(intents_list, intents_json):
    if len(intents_list) == 0:
        return "I'm sorry, I didn't understand that."
    
    tag = intents_list[0]['intent']
    for intent in intents_json['intents']:
        if intent['intent'] == tag:
            return random.choice(intent['responses'])
    
    return "I'm sorry, I didn't understand that."

def generate_response(user_input):
    intents_list = predict_class(user_input)
    response = get_response(intents_list, intents)
    return response

if __name__ == "__main__":
    while True:
        user_input = input("You: ")
        if user_input.lower() == 'exit':
            break
        print("Bot:", generate_response(user_input))
