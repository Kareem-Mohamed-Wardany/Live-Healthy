import queue
from Database import *
from datetime import timedelta, date
BloodTypes = ["O-", "O+", "B-", "B+", "A-", "A+", "AB-", "AB+"]
from textblob import TextBlob

def autocorrect(text):
    blob = TextBlob(text)
    return str(blob.correct())

text = "Thiis sentnce has mani speling errirs."
corrected_text = autocorrect(text)
print(corrected_text)
