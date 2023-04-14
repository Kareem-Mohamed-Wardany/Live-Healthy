import random
import json
import pickle
 
import nltk
nltk.download('all')
from nltk.stem import WordNetLemmatizer
from keras.models import Sequential
from keras.layers import Dense, Activation, Dropout
from keras.optimizers import SGD
 
import numpy as np
 
lemmatizer = WordNetLemmatizer()
 
intents = json.loads(open("intents.json").read())
 
words = []
classes = []
documents = []
 
ignore_letters = ["?", "!", ".", ","]
 
for intent in intents["intents"]:
    for pattern in intent["patterns"]:
        word_list = nltk.word_tokenize(pattern)
        words.extend(word_list)
        documents.append((word_list, intent["tag"]))
 
        if intent["tag"] not in classes:
            classes.append(intent["tag"])
words = [lemmatizer.lemmatize(word)
         for word in words if word not in ignore_letters]
 
words = sorted(set(words))
classes = sorted(set(classes))
 
pickle.dump(words, open('Data/words.pkl', 'wb'))
pickle.dump(classes, open('Data/classes.pkl', 'wb'))
 
dataset = []
template = [0]*len(classes)
 
for document in documents:
    bag = []
    word_patterns = document[0]
    word_patterns = [lemmatizer.lemmatize(word.lower())
                     for word in word_patterns]
 
    for word in words:
        bag.append(1) if word in word_patterns else bag.append(0)
 
    output_row = list(template)
    output_row[classes.index(document[1])] = 1
    dataset.append([bag, output_row])
 
random.shuffle(dataset)
dataset = np.array(dataset)
 
train_x = list(dataset[:, 0])
train_y = list(dataset[:, 1])
 
model = Sequential()
model.add(Dense(256, input_shape=(len(train_x[0]),),
                activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(128, activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(len(train_y[0]), activation='softmax'))
 
 
sgd = SGD(learning_rate=0.01,
          momentum=0.9, nesterov=True)
model.compile(loss='categorical_crossentropy',
              optimizer=sgd, metrics=['accuracy'])
 
hist = model.fit(np.array(train_x), np.array(train_y),
                 epochs=200, batch_size=5, verbose=1)
 
model.save("Data/chatbot_model.h5", hist)
print("Done!")