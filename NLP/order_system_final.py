# Code for Order Taking System for Robot Waiter Project (Group 5)
# Course: MIE 1075

# Referred to :
# https://bmmahmud.medium.com/my-first-self-made-python-project-restaurant-order-system-part-1-bc7e057e6a2c
# https://www.geeksforgeeks.org/python-convert-speech-to-text-and-text-to-speech/


# Import libraries
import speech_recognition as sr
import pyttsx3
from transformers import AutoModelForQuestionAnswering, AutoTokenizer, pipeline
import random
# import re

# Initialize the recognizer
r = sr.Recognizer()
table_no = "None"
data = "None"
order = "None"

# Function to convert text to speech
def SpeakText(command):

    # Initialize the engine
    engine = pyttsx3.init()
    engine.say(command)
    engine.runAndWait()

# Load NLP Model
def load_model():

    model_name = "deepset/roberta-base-squad2"

    # a) Get predictions
    nlp = pipeline('question-answering', model=model_name, tokenizer=model_name)
    

    # b) Load model & tokenizer
    model = AutoModelForQuestionAnswering.from_pretrained(model_name)
    tokenizer = AutoTokenizer.from_pretrained(model_name)

    return(nlp,model,tokenizer)

# Order Function 
def get_answer_order(item,nlp):
    QA_input = {
    'question': 'what are the dishes that I want to order from the restaurant?',
    # 'context': 'I visit a restaurant. the menu is as follows: number 1 Biryani, number 2 Pizza, number 3 Burger, number 4 Pasta. ' + order
    'context': 'The menu of the restaurant is number 1 Biryani, number 2 Pizza, number 3 Burger, number 4 Pasta. ' + order
    }
    answer = nlp(QA_input)
    print(answer)
    return answer['answer']

# Table Number Function
def get_answer_table(table,nlp):
    QA_input = {
    'question': 'What table number am I sitting at?',
    'context': 'I visit a restaurant. the menu is as follows: 1. Biryani, 2. Pizza, 3. Burger, 4. Pasta. '+ table
    }
    answer = nlp(QA_input)
    print(answer)
    return answer['answer']
    
# Function for Speech Input   
def speech_input_func(val):
    while (1):
        try:

            # use the microphone as source for input.
            with sr.Microphone() as source2:

                # wait for a second to let the recognizer
                # adjust the energy threshold based on
                # the surrounding noise level
                r.adjust_for_ambient_noise(source2, duration=0.2)
                SpeakText(val)
                audio2 = r.listen(source2)
			
			# Using google to recognize audio
                data = r.recognize_google(audio2)
                data = data.lower()
                print("Did you say ", data)
                # SpeakText(data)
        except sr.RequestError as e:
            print("Could not request results; {0}".format(e))
        except sr.UnknownValueError:
            print("unknown error occurred")
        return data

# Function for Speech output
def only_speak(val):
    # while(1):
        try:
            with sr.Microphone() as source2:

                # wait for a second to let the recognizer
                # adjust the energy threshold based on
                # the surrounding noise level
                r.adjust_for_ambient_noise(source2, duration=0.2)
                SpeakText(val)
        except sr.RequestError as e:
            print("Could not request results; {0}".format(e))
        except sr.UnknownValueError:
            print("unknown error occurred")

# Greet and Take Order          
only_speak("Welcome To Our Restaurant!")
# if order in context:
nlp,model,tokenizer = load_model()

# context='i want a burger and a pizza'
# order = item_func("What do you want to order")
order = speech_input_func("What do you want to order") # Preferable use "and" between food items when speaking
my_order = get_answer_order(order,nlp) # returns a string with order items 
my_order_list = my_order.split("and") # Creating list of ordered items
# my_order_list = re.split(', and', my_order)
# print(order)
# print(my_order_list)

cost_list = []
cost_list = random.sample(range(1, 15), len(my_order_list)) # Creating list of cost of ordered items
# print(cost_list)
zipbObj = zip(my_order_list, cost_list)
menu = dict(zipbObj)  # Creating a dictionary to print the ordered food items and their costs
print(menu)
only_speak("You ordered the follwing Items")
price = 0
for key in menu:
    only_speak(key)
    price = price + menu[key]
print(price)
only_speak("Your Total Price is "+ str(price)+"Canadian dollars") # Total cost

table=speech_input_func("What is your table number") # Get table number
table_no = get_answer_table(table,nlp)
print("The table number is: " + table_no)

only_speak("Bon appetit! Do visit us again!")
# End

# Tried to put the Order taking system in a function, but for some reason, the nlp response becomes messy 
# def order_func():
#     # nlp,model,tokenizer = load_model()
#     only_speak("Welcome To Our Restaurant!")
#     # order = item_func("What do you want to order")
#     order = reply_func("What do you want to order")
#     my_order = get_answer_order(order,nlp)
#     my_order_list = my_order.split("and")
#     # print(order)
#     # print(my_order_list)

#     cost_list = []
#     cost_list = random.sample(range(1, 15), len(my_order_list))
#     # print(cost_list)
#     zipbObj = zip(my_order_list, cost_list)
#     menu = dict(zipbObj)
#     print(menu)
#     only_speak("You ordered the follwing Items")
#     price = 0
#     for key in menu:
#         only_speak(key)
#         price = price + menu[key]
#     print(price)
#     only_speak("Your Total Price is "+ str(price)+"Canadian dollars")

#     # table=table_func("What is your table number")
#     table=reply_func("What is your table number")
#     table_no = get_answer_table(table,nlp)

#     # only_speak("Your table number is " + table_no)
#     print("The table number is: " + table_no)

# # End
# # print('#'*30+"\nThanks! Order Again.\n")
#     only_speak("Thanks! Do visit us again")
#     return order, table_no

# order_func()