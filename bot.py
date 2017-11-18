 #!/usr/bin/python
 # -*- coding: utf-8 -*-
from config import *
import re
#импорт телеграма
import telebot
from telebot import types
bot = telebot.TeleBot(token)

#импорт модуля и вход в биржу
from wex import Client
client = Client(key, secret)

#делаем клаву
markup1 = types.ReplyKeyboardMarkup()
markup1.row("Ticker", "Info")
markup1.row("Active orders")
markup1.row("Trend menu")
markup1.one_time_keyboard = False
markup2 = types.ReplyKeyboardMarkup()
markup2.row("Special Ticker", "Delete order")
markup2.row("ALL MONEY")
markup2.row("Usually menu")



white_list = []
pr1 = False
pr2 =False
 
def Special_ticker():
     mes = ""
     if True:
          q = client.active_orders()["return"]
          for i in q.keys():
               pair = q[i]["pair"]
               infa = client.ticker(pair)[pair]
               mes1 = pair.replace("_", " ").upper()
               mes2 = "sell: " + str(round(infa["sell"], 4)) + " buy: " + str(round(infa["buy"], 4))
               mes = mes + mes1 + "\n" + mes2 + "\n" + palka + "\n"

     return mes

def generate_message ():
     mes = ""
     q = ["btc_usd", "ltc_usd", "nmc_usd",
          "nvc_usd", "ppc_usd", "dsh_usd",
          "eth_usd", "bch_usd", "zec_usd"]
     for i in q:
          infa = client.ticker(i)[i]
          mes1 = i.replace("_", " ").upper()
          mes2 = "sell: " + str(round(infa["sell"], 4)) + " buy: " + str(round(infa["buy"], 4))
          mes = mes + mes1 + "\n" + mes2 + "\n" + palka + "\n"
     return mes

def getinfo():
     q = client.get_info()["return"]["funds"]
     mes = ""
     for i in q.keys():
          if round(q[i], 4) > 0:
               mes = mes + str(i) + " " + str(q[i]) + "\n"
     return mes

def allmoney():
     summ = 0
     q = client.get_info()["return"]["funds"]
     mes = ""
     for i in q.keys():
          money = q[i]
          if money != 0 and i != "usd" and i != "rur" and "usdet":
               rate = client.ticker(i+"_usd")[i+"_usd"]["sell"]
               summ = summ + money*rate
     summ += q["usd"]
     summ += q["rur"] / client.ticker("usd_rur")["usd_rur"]["sell"]
     try:    
          q = client.active_orders()["return"]
          q1 = q.keys()
          for i in q1:
               summ+= q[i]["amount"] * q[i]["rate"]
     except:
          True
     summ = round(summ,1)

     return summ

def active():
     mes = ""
     try:
          q = client.active_orders()["return"]
          q1 = q.keys()
          for i in q1:
               mes = mes + "key: " + str(i)+ "\n" + str(q[i]["pair"]).replace("_usd", "").upper()+ " " + str(q[i]["type"]) + " " + str(q[i]["rate"]) + "\n"
     except:
          mes = "No have order"
     return mes
def delete_order():
     global pr1
     if active() != "No have order":
          mes = ""
          pr1 = True
          markup3 = types.ReplyKeyboardMarkup()
          q = client.active_orders()["return"]
          q1 = q.keys()
          for i in q1:
               mes = mes + "key: " + str(i)+ " " +str(q[i]["pair"]).replace("_usd", "").upper()+ " " +str(q[i]["type"]) + " " + str(q[i]["rate"])
               markup3.row(mes)
          markup3.row("Cancel")
          return markup3
     else:
          return "Null"


@bot.message_handler(content_types=["text"])
def repeat_all_messages(message):
     global pr1
     sms = message.text
     komu = message.chat.id
     if pr1:
          if message.text == "Cancel":
               bot.send_message(komu, "Ok. Cancel.", reply_markup = markup2)
               pr1 = False
          else:
               dele = re.findall("key: (\d+)", sms)[0]
               client.cancel_order(int(dele))
               bot.send_message(komu, "Deleted", reply_markup = markup2)
               pr1 = False
     if sms == "Trend menu":
          if white_list.count(komu) != 0:
               bot.send_message(komu, "Trend menu",reply_markup= markup2)
          else:
               bot.send_message(komu, "You don't have pervission", reply_markup = markup1)
     if sms == "Ticker":
          bot.send_message(komu, "Загрузка...")
          bot.send_message(komu, generate_message(),reply_markup = markup1)
     if sms == "Info":
          bot.send_message(komu, "Загрузка...")
          bot.send_message(komu, getinfo(), reply_markup = markup1)
     if sms == "Active orders":
          bot.send_message(komu, "Загрузка...")
          bot.send_message(komu, active(), reply_markup = markup1)
     if sms == "/start":
          bot.send_message(komu, "Ticket or Info or Active Orders", reply_markup = markup1)
     if sms == "Special Ticker":
          bot.send_message(komu, "Загрузка...")
          if white_list.count(komu) != 0:
               bot.send_message(komu, Special_ticker(), reply_markup=markup2)
          else:
               bot.send_message(komu, "You don't have pervission", reply_markup = markup1)
     if sms == "ToYwjMHa698":
          bot.send_message(komu, "Загрузка...")
          white_list.append(komu)
          bot.send_message(komu, "Good", reply_markup = markup2)
     if sms == "Usually menu":
          bot.send_message(komu, "Загрузка...")
          bot.send_message(komu, "Ticket or Info or Active Orders", reply_markup = markup1)
     if sms == "/help":
          bot.send_message(komu, "Загрузка...")
          bot.send_message(komu, "Ticket \n Info \n Active Orders \n /start \n Sell \n Buy \n Special Ticker \n Delete order [nomer order]", reply_markup = markup1)
     if sms == "Delete order":
          bot.send_message(komu, "Загрузка...")
          if white_list.count(komu) != 0:
               a = delete_order()
               if a != "Null":
                    bot.send_message(komu, "Choose: ",reply_markup = a)
               else:
                    bot.send_message(komu, "No active orders",reply_markup = markup2)
          else:
               bot.send_message(komu, "You don't have pervission", reply_markup = markup1)
     if sms == "ALL MONEY":
          bot.send_message(komu, "Загрузка...")
          if white_list.count(komu) != 0:
               bot.send_message(komu, str(allmoney())+"$", reply_markup=markup2)
          else:
               bot.send_message(komu, "You don't have pervission", reply_markup = markup1)
if __name__ == '__main__':
     bot.polling(none_stop=True)

