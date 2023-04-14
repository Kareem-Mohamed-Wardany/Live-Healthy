from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer
from chatterbot.conversation import Statement

# Create a new ChatBot instance
bot = ChatBot('PulmonaryBot')

# Train the bot using a corpus of pulmonary-related conversations
trainer = ChatterBotCorpusTrainer(bot)
trainer.train("chatterbot.corpus.english.medical")

# Define a function to process the patient's input and generate a response
def get_bot_response(patient_input):
    # Check if the patient has an X-ray scan for their lungs
    if 'x-ray' in patient_input.lower():
        return Statement('Please import your X-ray scan so that we can analyze it.')
    
    # Check if the patient has any symptoms and how long they have had them
    elif 'symptoms' in patient_input.lower():
        return Statement('What symptoms are you experiencing, and how long have you had them?')
    
    # Check if the patient is taking any medication
    elif 'medication' in patient_input.lower():
        return Statement('Are you currently taking any medication?')
    
    # Check if the patient has any additional information to share
    elif 'extra information' in patient_input.lower():
        return Statement('Is there anything else you would like to tell us about your condition?')
    
    # Make a prediction based on the information provided by the patient
    else:
        prediction = bot.get_response(patient_input)
        
        # If the prediction indicates that the patient's health state is critical, advise them to speak with a doctor
        if prediction.text == 'Your health state appears to be critical. Please speak with one of our doctors for further advice.':
            return Statement(prediction.text + ' Would you like to chat with one of our doctors now?')
        
        return prediction

# Start the conversation
print('Welcome to PulmonaryBot. How can we assist you today?')

while True:
    patient_input = input('You: ')
    
    if patient_input.lower() == 'exit':
        print('Thank you for using PulmonaryBot.')
        break
    
    bot_response = get_bot_response(patient_input)
    print('PulmonaryBot:', bot_response.text)