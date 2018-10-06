from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
import os
bot=ChatBot('Bot')
bot.set_trainer(ListTrainer)

while True:
    message=input('you:')
    reply=bot.get_response(message)
    print('Chatbot: '+ reply.text)
    if message.strip() == 'Bye':
        print('Chatbot: Bye')
        break
