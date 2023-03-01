# Refer to :
# https://bmmahmud.medium.com/my-first-self-made-python-project-restaurant-order-system-part-1-bc7e057e6a2c
# https://www.geeksforgeeks.org/python-convert-speech-to-text-and-text-to-speech/

import speech_recognition as sr
import pyttsx3
from transformers import AutoModelForQuestionAnswering, AutoTokenizer, pipeline


# Initialize the recognizer
r = sr.Recognizer()
items = "None"
table_no = "None"
data = "None"

# Function to convert text to
# speech


def SpeakText(command):

    # Initialize the engine
    engine = pyttsx3.init()
    engine.say(command)
    engine.runAndWait()


# Loop infinitely for user to speak

# Restaurent Order System using Function
def load_model():

    model_name = "deepset/roberta-base-squad2"

    # a) Get predictions
    nlp = pipeline('question-answering', model=model_name, tokenizer=model_name)
    

    # b) Load model & tokenizer
    model = AutoModelForQuestionAnswering.from_pretrained(model_name)
    tokenizer = AutoTokenizer.from_pretrained(model_name)

    return(nlp,model,tokenizer)

def get_answer_order(context,nlp):
    QA_input = {
    'question': 'what are the dishes that I want to order from the restaurant?',
    'context': 'I visit a restaurant. the menu is as follows: 1. Biryani, 2. Pizza, 3. Burger, 4. Pasta. '+context
    }
    answer = nlp(QA_input)
    return answer['answer']

def get_answer_table(context,nlp):
    QA_input = {
    'question': 'What table number am I sitting at?',
    'context': 'I visit a restaurant. the menu is as follows: 1. Biryani, 2. Pizza, 3. Burger, 4. Pasta. '+context
    }
    answer = nlp(QA_input)
    return answer['answer']
    

# Function for order items
def item_func(val):
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
                items = r.recognize_google(audio2)
                items = items.lower()
                print("Did you say ",items)
                SpeakText(items)
        except sr.RequestError as e:
            print("Could not request results; {0}".format(e))
        except sr.UnknownValueError:
            print("unknown error occurred")
        return items

# function for table number
def table_func(val):
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
                table_no = r.recognize_google(audio2)

                table_no = table_no.lower()
                print("Did you say ",table_no)
                SpeakText(table_no)
        except sr.RequestError as e:
            print("Could not request results; {0}".format(e))
        except sr.UnknownValueError:
            print("unknown error occurred")
        return table_no

# def reply_func(val):
#     while (1):
#         try:

#             # use the microphone as source for input.
#             with sr.Microphone() as source2:

#                 # wait for a second to let the recognizer
#                 # adjust the energy threshold based on
#                 # the surrounding noise level
#                 r.adjust_for_ambient_noise(source2, duration=0.2)
#                 SpeakText(val)
#                 audio2 = r.listen(source2)
			
# 			# Using google to recognize audio
#                 data = r.recognize_google(audio2)
#                 data = data.lower()
#                 print("Did you say ", data)
#                 SpeakText(data)
#         except sr.RequestError as e:
#             print("Could not request results; {0}".format(e))
#         except sr.UnknownValueError:
#             print("unknown error occurred")
#         return data


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

# Add Order items
def order_items(orders):
    order_items.total_price = 0
    run = True
    while run:
        orderList = orders
        # items = numeric_validation("Enter Item No:")
        items = item_func("What is your order number")
        # items = reply_func("What is your order number")
        if (items in orderList):
            # print("Already ordered!!! Try Somthing New")
            only_speak("Already ordered!!! Try Somthing New")
            continue
        else:
            items_no = int(items)
            # qty = numeric_validation("Quantity:")
            order_items.total_price += (menu[items_no]['price'] * qty)
            orderList.append(menu[items_no]['item'])
            # order = input("Do you want to order more? y/n:")
            order = item_func("Do you want to order more? Yes or no?")
            # order = reply_func("Do you want to order more? Yes or no?")
            if order == 'yes':
                continue
            else:
                run = False
    return order_items


# Start main function
# print("#"*30+"\n    Welcome To Our Restaurant\n"+"#"*30 +
#       "\nPlease Chose your Order Number:")
#only_speak("Welcome To Our Restaurant! Here is a list of our items: 1 coffee, price: 3 dollars, 2 Samosa, price: 5 dollars, 3 Tea, price: 3 dollars, 4 Paratha, price: 4 dollars.  Please Chose your Order Number")

# Declare Variablesmenu = {1: {'item': 'Coffee', 'price': 3},       ,
menu = { 1: {"item": "coffee", "price": 3},
         2: {"item": "samosa", "price": 3},
         3: {"item": "tea", "price": 3},
         4: {"item": "paratha", "price": 4}
         }

orders = []  # issue it has to be a dictionary not a list
qty = 1
nlp,model,tokenizer =load_model()

context='i want a burger and a pizza'
answer = get_answer_order(context,nlp)
print(answer)
only_speak(answer)

context='i think im at number 3'
answer = get_answer_table(context,nlp)
print(answer)
only_speak(answer)
# Show menu
for item, value in menu.items():
    print("No#", item, ": Item: ", value["item"].title(
    ), "- Price:"+str(value["price"])+"CAD")
print('#'*30)

# Add item
order_items(orders)
table_no = table_func("Please let me know the table number")
# table_no = reply_func("Please let me know the table number")
only_speak("Your table number is " + table_no)
print("The table number is: " + table_no)
# print('#'*30)

# Show card list
# print("You order the follwing Items: ")
only_speak("You ordered the follwing Items")
for i in range(len(orders)):
    only_speak(str(i+1)+"- "+orders[i].title())
only_speak("Your Total Price is "+ str(order_items.total_price)+"Canadian dollars")
#     print(str(i+1)+"- "+orders[i].title())
# print("-"*30+"\nYour Total Price: "+str(order_items.total_price)+"Tk")


# End
# print('#'*30+"\nThanks! Order Again.\n")
only_speak("Thanks! Do visit us again")