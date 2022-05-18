from typing import Union
from fastapi import FastAPI
import transformers
import os
import datetime
import numpy as np
# from main import ChatBot

class ChatBot():
    def __init__(self, name):
        print("----- Starting up", name, "-----")
        self.name = name

    def speech_to_text(self,userMSg):
        self.text = "ERROR"
        try:
            # Taking Input
            self.text = userMSg
        except:
            return {"error": "We could not process your response"}

    @staticmethod
    def text_to_speech(text):
        # Generating Output
        return {"chatbot_response": text}

    def wake_up(self, text):
        return True if self.name in text.lower() else False

    @staticmethod
    def action_time():
        return datetime.datetime.now().time().strftime('%H:%M')

app = FastAPI()
ai = ChatBot(name="Ai Bot")
nlp = transformers.pipeline("conversational", model="microsoft/DialoGPT-medium")
os.environ["TOKENIZERS_PARALLELISM"] = "true"

@app.get("/start") # welcome function
def read_root():
    return "Welcome to world of AI Chatbots!! Please Start Your Conversation! 🤖"


@app.get("/chatsession/{user_msg}") # chat function
async def chat_session(user_msg):
    ai.speech_to_text(userMSg= user_msg)

    ## action time
    if "time" in ai.text:
        res = ai.action_time()

    elif "name" in ai.text:
        res = "My name is Ai Chatbot"

    elif "days in a year" in ai.text:
        res = "I am not sure! but i think 365 Days."

    elif "days in a month" in ai.text:
        res = "That's so tough for me, but i think depends on the month."

    elif "days in a week" in ai.text:
        res = "I am not sure! but i think 7 Days."

        # Jokes
    elif "tell me a joke" in ai.text:
        res = "I finally decided to sell my vacuum cleaner. All it was doing was gathering dust!"

    elif "tell me another joke" in ai.text:
        res = "A chubbier woman: Mirror, Mirror on the wall, who’s the fairest of them all? Mirror: “Kindly move aside. I can’t see anything."


    elif "tell me a joke" in ai.text:
        res = "I finally decided to sell my vacuum cleaner. All it was doing was gathering dust!"

    elif "who are you" in ai.text:
        res = "I am a Chatbot, Created by Comsains."

        # Fiver and Upwork
    elif "what is fiver?" in ai.text:
        res = "Fiverr is an online marketplace for freelance services. Fiverr serves to allow listing and applying for small one-off jobs, or gigs, online."

    elif "what is upwork?" in ai.text:
        res = "Upwork, formerly Elance-oDesk, is an American freelancing platform. In 2015, the Elance-oDesk merger was rebranded as Upwork and the company's full name is now Upwork Global Inc."

        ## respond politely
    elif any(i in ai.text for i in ["thank", "thanks"]):
        res = np.random.choice(
            ["you're welcome!", "anytime!", "no problem!", "cool!", "I'm here if you need me!", "mention not"])

    elif any(i in ai.text for i in ["exit", "close", "bye"]):
        res = np.random.choice(["Tata", "Have a good day", "Bye", "Goodbye", "Hope to meet soon", "peace out!"])

    ## conversation
    else:
        if ai.text == "ERROR":
            res = "Sorry, come again?"
        else:
            chat = nlp(transformers.Conversation(ai.text), pad_token_id=50256)
            res = str(chat)
            res = res[res.find("bot >> ") + 6:].strip()
    # ai.text_to_speech(res)

    return  res