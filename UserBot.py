
from unittest import result
from telethon.sync import TelegramClient
from telethon.tl.types import phone


class Parser:
    
    #конструктор читает настройки из переданного в него ini-файла и устанавливает соединение с телеграммом
    def __init__(self, initini):
        self.connected = False
        #секция чтения настроек из ini-файла
        import configparser
        config = configparser.ConfigParser()
        try:
          config.read(initini)
          api_id=config.getint('telegram','api_id')
          api_hash=config.get('telegram','api_hash') 
          phone=config.get('telegram','phone') 
        except:
           raise FileNotFoundError("Config file missing or incorrect file structure")
        #создание и подключение клиента из библиотеки телетон
        self.client = TelegramClient(phone,api_id,api_hash, system_version='10', device_model='AMD64', app_version='0.1')
        self.client.connect()
        if not self.client.is_user_authorized():
           self.client.send_code_request(phone)
           self.client.sign_in(phone, input('Enter the code: '))
        if not self.client.is_user_authorized(): 
           raise ConnectionError("could not connect telegram client")
        self.connected = True 
        
    #функция распечатывает на экране список диалогов/каналов/групп и предлагает выбрать конкретный, возвращает его id 
    def select_dialog(self):
      if not self.connected: 
         raise ConnectionError("could not connect telegram client")
      i=1
      dialogs=[]
      print('Select channel or group do you need')
      for dialog in self.client.iter_dialogs(): 
         print(i,' ',dialog.title,' ',dialog.id)
         dialogs.append((dialog.id,dialog.title))
         i+=1     
      if len(dialogs)==0: 
         print('Your account has not chats/groups/dialogs')
         return
      select = int(input())
      print(select)
      if (1>select) or (select>len(dialogs)):
         raise ValueError('You input incorrect value')
      print('You select the... ', dialogs[select-1][1])
      return dialogs[select-1][0]

         

#channel = client.get_entity('https://t.me/Biysk_RO')

#def get_channel_members():
#    offset = 0
#    limit = 20
    

#    return 0
    
#основной код программы
parser = Parser('connect.ini')
print(parser.select_dialog())
