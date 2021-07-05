import telebot
from wordnik import *

global count, word, Guess_let, Miss_let, Hint

API_KEY = "1899997640:AAHsQoWy3y3pJh6_X1Bg1b4nvawinuemM04"
bot = telebot.TeleBot(API_KEY, parse_mode=None)

apiUrl = 'http://api.wordnik.com/v4'
apiKey = 'feolbmug8axv6cs0blyfog6fjoyl1hif9j6n0r4x6eiptup36'
client = swagger.ApiClient(apiKey, apiUrl)
wordsApi = WordsApi.WordsApi(client)
wordApi = WordApi.WordApi(client)

count = 0
Guess_let = list()
Miss_let = list()

@bot.message_handler(commands=['start'])
def send_welcome(message):
    """ """
    bot.reply_to(message, "Hey, Lets Play Hangman!")
    global count, word, Guess_let, Miss_let, Hint
    count = 0
    random_word = wordsApi.getRandomWord(hasDictionaryDef='true',
                                         excludePartOfSpeech= ['Plural', 'adverb', 'past-participle'])
    while ('-' in random_word.word):
        random_word = wordsApi.getRandomWord(hasDictionaryDef='true',
                                             excludePartOfSpeech= ['Plural', 'adverb', 'past-participle'])
    word = random_word.word 
    word = word.lower()
    Hint = str()
    for letter in word:
        Hint = Hint + " _ "
    msg = "Guess the word " + Hint
    bot.send_message(message.chat.id, msg)
    Guess_let = list()
    Miss_let = list()


@bot.message_handler(regexp="\D")
def guess_letter(message):
    """ """
    global count, word, Guess_let, Miss_let, Hint
    if message.text.lower() in Guess_let:
        msg = "Letter " + message.text + " is already guessed. Guess a different letter"
        bot.reply_to(message, msg)
        flag = 0
    else:
        flag = 1
        
    Guess_let.append(message.text.lower())
    if count < 6 and flag == 1 :
        if message.text.lower() in word:
            Hint = str()
            #Creating hint for the word
            for letter in word:
                if letter in Guess_let:
                    Hint = Hint + letter
                else:
                    Hint = Hint + " _ "

            msg = "Word: " + Hint + "\nGuess: " + message.text + "\nMisses : " + str(Miss_let)
            bot.reply_to(message, msg)
            #Sending image
            photo_id = "Hangman/Hangman-" + str(count)+ ".png"
            photo = open(photo_id, 'rb')
            bot.send_photo(message.chat.id, photo)
        else:
            count = count + 1
            Miss_let.append(message.text)
            msg = "Word: " + Hint + "\nGuess:" + message.text + "\nMisses:" + str(Miss_let)
            bot.reply_to(message, msg)
            #Sending image
            photo_id = "Hangman/Hangman-" + str(count)+ ".png"
            photo = open(photo_id, 'rb')
            bot.send_photo(message.chat.id, photo)


    if Hint.strip() == word:
        """ """
        #Obtaining the definition of the word
        definitions = wordApi.getDefinitions(word)
        definition = definitions[0].text
        msg_cor = "You guessed the word correctly!!!\nWord : " + word + "\nMeaning:- " + definition + "\n/start to play agian"
        bot.send_message(message.chat.id, msg_cor)
        Guess_let = list()
        Miss_let = list()

    if count == 6:
        """ """
        #Obtaining the definition of the word
        definitions = wordApi.getDefinitions(word)
        definition = definitions[0].text
        msg_wro = "Oops.You lost the game. \nCorrect Word : " + word + "\nMeaning:- " + definition + "\n/start to play agian"
        bot.send_message(message.chat.id, msg_wro)
        Guess_let = list()
        Miss_let = list()

bot.polling()

