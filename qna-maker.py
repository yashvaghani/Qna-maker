from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
import os
bot=ChatBot('Bot')
bot.set_trainer(ListTrainer)

for files in os.listdir('C:/Users/yashv/Downloads/chatterbot-corpus-master/chatterbot_corpus/data/english/'):

    data=open('C:/Users/yashv/Downloads/chatterbot-corpus-master/chatterbot_corpus/data/english/'+files,'r').readlines()
    bot.train(data)






