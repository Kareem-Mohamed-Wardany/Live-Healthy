import random
import json
import pickle
from typing import final

import nltk
from nltk.stem import WordNetLemmatizer
from keras.models import load_model

import numpy as np
import pyttsx3
import time
nltk.download('punkt')
lemmatizer = WordNetLemmatizer()
intents = json.loads(open("intents.json").read())

words = pickle.load(open('Data/words.pkl', 'rb'))
classes = pickle.load(open('Data/classes.pkl', 'rb'))
model = load_model('Data/chatbot_model.h5')


def clean_up_sentence(sentence):
	sentence_words = nltk.word_tokenize(sentence)
	sentence_words = [lemmatizer.lemmatize(word)
					for word in sentence_words]

	return sentence_words


def bag_of_words(sentence):
	sentence_words = clean_up_sentence(sentence)
	bag = [0] * len(words)

	for w in sentence_words:
		for i, word in enumerate(words):
			if word == w:
				bag[i] = 1
	return np.array(bag)


def predict_class(sentence):
	bow = bag_of_words(sentence)
	res = model.predict(np.array([bow]))[0]

	ERROR_THRESHOLD = 0.25

	results = [[i, r] for i, r in enumerate(res) if r > ERROR_THRESHOLD]

	results.sort(key=lambda x: x[1], reverse=True)

	return_list = []

	for r in results:
		return_list.append({'intent': classes[r[0]],
							'probability': str(r[1])})
	return return_list


def get_response(intents_list, intents_json):
    tag = intents_list[0]['intent']
    list_of_intents = intents_json['intents']
    print(tag)
    result = ''

    for i in list_of_intents:
        if i['tag'] == tag:
            result = random.choice(i['responses'])
            break
        else:
            result = "Sorry, I don't understand you"
    return result


# This function will take the voice input converted
# into string as input and predict and return the result in both
# text as well as voice format.
def calling_the_bot(txt):
	global res
	predict = predict_class(txt)
	res = get_response(predict, intents)
	print(f"BOT: {res}")


if __name__ == '__main__':
	print("Bot is Running")

	while True:

		text = input("You:")
		calling_the_bot(text)


		if text in ['no', 'please exit']:
			print("Bot has been stopped by the user")
			exit(0)
