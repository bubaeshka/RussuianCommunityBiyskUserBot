
from unittest import result
import telethon
from telethon.sync import TelegramClient
from telethon.tl.functions.channels import GetParticipantsRequest
from telethon.tl.types import ChannelParticipant, ChannelParticipantsSearch, phone
from telethon import functions, types


class Parser:
    
    #����������� ������ ��������� �� ����������� � ���� ini-����� � ������������� ���������� � �����������
    def __init__(self, initini):
        self.connected = False
        #������ ������ �������� �� ini-�����
        import configparser
        config = configparser.ConfigParser()
        try:
          config.read(initini)
          api_id=config.getint('telegram','api_id')
          api_hash=config.get('telegram','api_hash') 
          phone=config.get('telegram','phone') 
        except:
           raise FileNotFoundError("Config file missing or incorrect file structure")
        #�������� � ����������� ������� �� ���������� �������
        self.client = TelegramClient(phone,api_id,api_hash, system_version='10', device_model='AMD64', app_version='0.1')
        self.client.connect()
        if not self.client.is_user_authorized():
           self.client.send_code_request(phone)
           self.client.sign_in(phone, input('Enter the code: '))
        if not self.client.is_user_authorized(): 
           raise ConnectionError("could not connect telegram client")
        self.connected = True 
        
    #������� ������������� �� ������ ������ ��������/�������/����� � ���������� ������� ����������, ���������� ��� id 
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
    
    #������� ��������� ������ ������������� ����/������ 
    def get_channel_members(self,channel):
       #������ ���������� ������ �� � �����, �� ���������� ����������, ���������� ����������� ��� ������
       offset = 0
       limit = 100
       all_members = []
       all_users= []
       all_participants = []
       while True:
         result = self.client(GetParticipantsRequest(
              channel=channel,
              filter=ChannelParticipantsSearch(''),
              offset=offset,
              limit=limit,
              hash=0
         ))
         users = result.users    
         all_users.extend(users)
         all_participants.extend(result.participants)
         print(len(users))
         if len(users) < limit:
             break
         offset += limit
       ############################  
       test=0
       for participant in all_participants: 
          test+=1
          match type(participant):
             case telethon.types.ChannelParticipantBanned: print(test,' ','Banned')
             case telethon.types.ChannelParticipantAdmin:  print(test,' ','Admin')                    
             case telethon.types.ChannelParticipant: print(test,' ','Default')  
             case telethon.types.ChannelParticipantCreator: print(test,' ','Creator')
             case telethon.types.ChannelParticipantLeft: print(test,' ','Left')
             case telethon.types.ChannelParticipantSelf: print(test,' ','Self')          
             case __: print(test, ' ', 'Error')
       #��������� ����� �������� ���������    
       num=0 
       class Member: pass
       for user in all_users:
          member=Member()
          member.id = user.id
          member.first_name=user.first_name
          member.last_name=user.last_name
          member.username = user.username
          member.phone = user.phone
          found=False
          for participant in all_participants:
             if (type(participant)!=telethon.types.ChannelParticipantLeft and type(participant)!=telethon.types.ChannelParticipantBanned and participant.user_id == user.id):
                if found: raise LookupError('Duplicate user id in list of participants')
                found=True
                member.date = participant.date          
                match type(participant):
                   case telethon.types.ChannelParticipantAdmin: member.type='Admin'
                   case telethon.types.ChannelParticipant: member.type='Default'
                   case telethon.types.ChannelParticipantCreator: member.type='Creator'
                   case telethon.types.ChannelParticipantSelf: member.type='Self'
                   case __: member.type='Error'  
                #all_participants.remove(participant)      
          if not found: 
             member.date = 0
             member.type = 'NotFound or Banned or Left'
          num+=1
          all_members.append(member)
       return all_members
         
    
#�������� ��� ���������
parser = Parser('connect.ini')
members = parser.get_channel_members(parser.select_dialog())
i=0
for member in members:
   i+=1
   print(i,' ', member.id,' ',member.first_name,' ',member.last_name,' ', member.username,' ', member.phone,' ', member.date,' ',member.type)
