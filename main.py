#scripted by Laxier
#that bot is a helper to enter Uni
#It was working at heroku server
import telebot
import requests
import json
import time

def update():
    global url = r""
    #getting the json table
    resp = requests.get(url)
    data = json.loads(resp.text)
    array=[]
    for i in data['data']['list_applicants']:
        if i['СогласиеНаЗачисление']=='Да':
            array.append(i)
    return array #return data

def entering(array):
    kcp=58
    #return the grade of the last one
    return array[kcp]['СуммаБаллов']

API = ''
#setting up a telegram bot
bot = telebot.TeleBot(API)
Button_Pressed = False
#user has not signed up to get updates
@bot.message_handler(commands=['start'])
def start_message(message):
    keyboard = telebot.types.ReplyKeyboardMarkup(True)
    keyboard.row('/start', '/updates')
    text = 'Привет! Добро пожаловать в бот! В данный момент проходной балл на направление составляет: ' + entering()
    bot.send_message(message.chat.id, text, reply_markup=keyboard)

@bot.message_handler(commands=['updates'])
def start_message(message):
    global Button_Pressed
    Button_Pressed = not(Button_Pressed)
    #button is changed
    if Button_Pressed:
        #if it tested then loop the updating system 
        bot.send_message(message.chat.id, 'Теперь Вы будете получать уведомления при измненении проходного балла!')
        prev=0
        while True:
            if (not(Button_Pressed)):
                bot.send_message(message.chat.id, 'Вы успешно отписались от уведомлений!')
                #user unpressed the button so the loop is shutted down
                break
            try:
                array=update()
                now = entering(array)
            except: now=prev
            #try made to avoid network problems
            if now!=prev:
                #send notification if grade has changed
                text='Проходной балл изменился на: ' + str(now)
                bot.send_message(message.chat.id, text)
            prev=now
            #server rests for 10 seconds
            time.sleep(10)

bot.polling()
#starting the telebot
