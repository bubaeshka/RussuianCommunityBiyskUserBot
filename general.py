from UserBot import Parser
import csv

class User_interface:
    
    #функция возвращает выбранный id конкретного диалога
    def select_dialog(dialogs):
      print('Select channel or group do you need')
      if dialogs is None: 
         raise ValueError('Your account has not chats/groups/dialogs')   
      i=1 
      choice = {}
      for _id, title in dialogs.items():
         print(i,' ',title,' ',_id)
         choice[i] = _id
         i+=1
      select = int(input())
      print(select)
      if (1>select) or (select>len(dialogs)):
         raise ValueError('You input incorrect value')
      print('You select the... ', dialogs[choice[select]])
      return choice[select]   
     
    
#основной код программы
parser = Parser('connect.ini')
members = parser.get_channel_members(User_interface.select_dialog(parser.get_dialogs()))
i=0

with open('file.csv','a', encoding="utf-8", newline='') as f:
  for member in members:
     i+=1
     new_row = [i, member.id, member.first_name, member.last_name,member.username, member.phone, member.date,member.type]
     print(i,' ', member.id,' ',member.first_name,' ',member.last_name,' ', member.username,' ', member.phone,' ', member.date,' ',member.type)
     csv.writer(f).writerow(new_row)
