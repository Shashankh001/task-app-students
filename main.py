from functools import partial
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import *
from kivymd.app import MDApp
import os
from kivymd.uix.card import MDCard
from kivymd.uix.card import MDSeparator
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivymd.uix.button import MDFlatButton
from kivy.uix.gridlayout import GridLayout
from kivy.uix.stacklayout import StackLayout
from kivy.effects.scroll import ScrollEffect
from kivymd.uix.button import *
import client
import json
from kivymd.uix.dialog import MDDialog
from mega import Mega
from threading import Thread
from kivy.clock import Clock
from tkinter import filedialog
import tkinter
from kivy.core.window import Window
from kivymd.uix.spinner import MDSpinner

Window.size = (1080, 720)

def get_ip():
    with open('ip.txt') as f:
        return f.read()

IP = get_ip()

mega = Mega()
mega._login_user('','')
CLASS = None

kv_string = """
#:kivy 2.1.0
#:import toast kivymd.toast.toast

WindowManager:
    Menu:
        name: 'menu'
    Homework:    
        name: 'hw'
    Notice: 
        name: 'notice'
    Saved:
        name: 'saved'


<Menu>:
    MDCard:
        size_hint: None,None
        size: '265dp','150dp'
        pos_hint: {'center_x': 0.35, 'center_y':0.65}
        orientation: 'vertical'
        line_color: 150/255,150/255,150/255,1
        focus_behavior: True
        ripple_behavior: True
        on_release: root.homework()

        
        Label:
            text: 'Homework'
            font_size: '18sp'

        MDSeparator:

        Label:
            text: 'Click to view homework/assignments'
            font_size: '14sp'
            color: 150/255,150/255,150/255,1

    MDCard:
        size_hint: None,None
        size: '265dp','150dp'
        pos_hint: {'center_x': 0.65, 'center_y':0.65}
        orientation: 'vertical'
        line_color: 150/255,150/255,150/255,1
        focus_behavior: True
        ripple_behavior: True
        on_release: root.notice()
        
        Label:
            text: 'Notices'
            font_size: '18sp'

        MDSeparator:

        Label:
            text: 'Click to view Notices/Announcements'
            font_size: '14sp'
            color: 150/255,150/255,150/255,1

    MDCard:
        size_hint: None,None
        size: '265dp','150dp'
        pos_hint: {'center_x': 0.35, 'center_y':0.35}
        orientation: 'vertical'
        line_color: 150/255,150/255,150/255,1
        focus_behavior: True
        ripple_behavior: True
        on_release: root.saved()
        
        Label:
            text: 'Saved'
            font_size: '18sp'

        MDSeparator:

        Label:
            text: 'Click to view saved notices and homework'
            font_size: '14sp'
            color: 150/255,150/255,150/255,1

    MDCard:
        size_hint: None,None
        size: '265dp','150dp'
        pos_hint: {'center_x': 0.65, 'center_y':0.35}
        orientation: 'vertical'
        line_color: 150/255,150/255,150/255,1
        focus_behavior: True
        ripple_behavior: True
        on_release: root.downloads()
        
        Label:
            text: 'Downloads'
            font_size: '18sp'

        MDSeparator:

        Label:
            text: 'Click to change or view downloads'
            font_size: '14sp'
            color: 150/255,150/255,150/255,1

        


<Homework>:
    Label:
        text: 'Homework'
        font_size: 28
        pos_hint: {'center_x': 0.5, 'center_y':0.9}

    MDRectangleFlatButton:
        text: 'Back'
        pos_hint: {'center_x': 0.95, 'center_y':0.95}
        on_release: root.home()
        
<Notice>:
    Label:
        text: 'Notices'
        font_size: 28
        pos_hint: {'center_x': 0.5, 'center_y':0.9}

    MDRectangleFlatButton:
        text: 'Back'
        pos_hint: {'center_x': 0.95, 'center_y':0.95}
        on_release: root.home()

<Saved>:
    Label:
        text: 'Saved'
        font_size: 28
        pos_hint: {'center_x': 0.5, 'center_y':0.9}

    MDRectangleFlatButton:
        text: 'Back'
        pos_hint: {'center_x': 0.95, 'center_y':0.95}
        on_release: root.home()
"""

class Menu(Screen):
    def notice(self):
        TaskAppApp.build.kv.current = 'notice'
        TaskAppApp.build.kv.transition.direction = 'left'

    def homework(self):
        TaskAppApp.build.kv.current = 'hw'
        TaskAppApp.build.kv.transition.direction = 'left'

    def saved(self):
        TaskAppApp.build.kv.current = 'saved'
        TaskAppApp.build.kv.transition.direction = 'left'

    def downloads(self):
        Menu.downloads.dialog = MDDialog(
            title = 'Choose an option',
            buttons=[
                    MDRaisedButton(
                        text="Change Downloads Folder",
                        on_release= self.change_dest
                    ),
                    MDRaisedButton(
                        text="Open Downloads Folder",
                        on_release= self.open_dest
                    )
                ],
        )

        Menu.downloads.dialog.open()

    def change_dest(self, dt):
        root = tkinter.Tk()
        root.withdraw()

        destination = filedialog.askdirectory(parent=root,initialdir="/",title='Please select a directory')

        with open('appinfo.json','r') as f:
            data = json.load(f)
            f.close()

        data[0]["downloads_folder"] = destination.replace("/","\\")

        with open('appinfo.json','w') as f:
            json.dump(data, f, indent=4)
            f.close()

        Menu.downloads.dialog.dismiss()

    def open_dest(self, dt):
        with open('appinfo.json','r') as f:
            data = json.load(f)
            f.close()


        os.system(f'explorer "{data[0]["downloads_folder"]}"')
        Menu.downloads.dialog.dismiss()

MainData = None

class Homework(Screen):
    layout = StackLayout(size_hint=(1, None),orientation='rl-bt', spacing=20)
    layout.bind(minimum_height=layout.setter('height'))

    root = ScrollView(size_hint=(1, 0.8), effect_cls=ScrollEffect)
    root.add_widget(layout)

    def on_enter(self, *args):
        try:
            data = client.get_homework()
        except ConnectionRefusedError:
            popup2 = MDDialog(
                text= "Server offline."
            )
            self.home()
            popup2.open()
            return

        global MainData
        MainData = data

        for i in range(0, len(data)):  
            homework = Label(text=f"{data[i]['Context']}\n\nSent by - {data[i]['Teacher']} | [b]{data[i]['Subject']}[/b] | {data[i]['Time']} {data[i]['Date']} | Due Date: {data[i]['DueDate']}",
                        markup= True,
                        padding= [15,15],
                        size_hint=(1,None),
                        halign="left", 
                        valign="middle")

            download_attch = MDRectangleFlatIconButton(
                text = 'Download Attachment',
                icon = 'download',
                pos_hint = {'center_x':0.5},
                ids = {'b':i}
            )

            download_attch.bind(on_release = partial(self.download_thread, i))

            save = MDRectangleFlatIconButton(
                text = 'Save',
                icon = 'star',
                pos_hint = {'center_x':0.5},
                ids = {'b':i}
            )

            save.bind(on_release = partial(self.save_homework, i))

            homework.bind(size=homework.setter('text_size')) 
            homework._label.refresh()
            homework.height= (homework._label.texture.size[1] + 2*homework.padding[1])

            card = MDCard(
                style='elevated',
                size_hint=(1, None),
                height=homework.height
            )

            self.layout.add_widget(download_attch)
            self.layout.add_widget(save)
            self.layout.add_widget(card)
            card.add_widget(homework)
            

        try:
            self.add_widget(self.root)
        except:
            print("[ERROR] Couldn't add root widget, reason: root widget already exists.")

        return super().on_enter(*args)
        
    def popup_open(self, dt):
        Homework.popup_open.popup = MDDialog(
            text = "Downloading Attachments. Please Wait.",
            auto_dismiss=False

        )
        Homework.popup_open.popup.open()

    def popup_open_inv(self, dt):
        popup = MDDialog(
            text = "No Attachments have been assigned to this Notice"

        )
        popup.open()

    def popup_close(self, dt):
        Homework.popup_open.popup.dismiss()

    def save_homework(self, index, dt):
        with open('saved_data.json','r') as f:
            data = json.load(f)
            f.close()

        new_data = MainData[index]

        data.append(new_data)

        with open('saved_data.json','w') as f:
            data = json.dump(data, f, indent=4)
            f.close()


    def download_thread(self, index, dt):
        t = Thread(target = Homework.downloadAttch, args=(self,index,))
        t.daemon = True
        t.start()
        
    def downloadAttch(self, index):
        Clock.schedule_once(self.popup_open, 0)

        with open('appinfo.json','r') as f:
            data = json.load(f)
            f.close()

        try:
            print(MainData[index]["Attachments"][0])
        except IndexError:
            Clock.schedule_once(self.popup_close, 0)
            Clock.schedule_once(self.popup_open_inv, 0)
            return
        
        for i in range(0, len(MainData[index]["Attachments"])):
            try:
                mega.download_url(MainData[index]["Attachments"][i], data[0]["downloads_folder"])
            except:
                continue

        Clock.schedule_once(self.popup_close, 0)



    def home(self):
        for child in [child for child in self.layout.children]:
            self.layout.remove_widget(child)
            
        TaskAppApp.build.kv.current = 'menu'
        TaskAppApp.build.kv.transition.direction = 'right'



class Notice(Screen):
    layout = StackLayout(size_hint=(1, None),orientation='rl-bt', spacing=20)
    layout.bind(minimum_height=layout.setter('height'))

    root = ScrollView(size_hint=(1, 0.8), effect_cls=ScrollEffect)
    root.add_widget(layout)
 
    def on_enter(self, *args):
        try:
            data = client.get_notices()
        except ConnectionRefusedError:
            popup2 = MDDialog(
                text= "Server offline."
            )
            self.home()
            popup2.open()
            return

        global MainData
        MainData = data
        
        for i in range(0, len(data)):          
            notice = Label(text=f"{data[i]['Context']}\n\nSent by - {data[i]['Teacher']} | [b]{data[i]['Subject']}[/b] | {data[i]['Time']} {data[i]['Date']} | Due Date: {data[i]['DueDate']}",
                        markup= True,
                        padding= [15,15],
                        size_hint=(1,None),
                        halign="left", 
                        valign="middle")

            download_attch = MDRectangleFlatIconButton(
                text = 'Download Attachment',
                icon = 'download'
            )

            download_attch.bind(on_release = partial(self.download_thread, i))

            save = MDRectangleFlatIconButton(
                text = 'Save',
                icon = 'star',
                pos_hint = {'center_x':0.5},
                ids = {'b':i}
            )

            save.bind(on_release = partial(self.save_notice, i))

            notice.bind(size=notice.setter('text_size')) 
            notice._label.refresh()
            notice.height= (notice._label.texture.size[1] + 2*notice.padding[1])

            card = MDCard(
                height=notice.height,
                style = 'elevated',
                size_hint= (1,None),
                orientation = 'vertical'
            )

            self.layout.add_widget(download_attch)
            self.layout.add_widget(save)
            self.layout.add_widget(card)
            card.add_widget(notice)
            

        try:
            self.add_widget(self.root)
        except:
            print("[ERROR] Couldn't add root widget, reason: root widget already exists.")
 
        return super().on_enter(*args)

    def popup_open(self, dt):
        Notice.popup_open.popup = MDDialog(
            text = "Downloading Attachments. Please Wait.",
            auto_dismiss=False

        )
        Notice.popup_open.popup.open()

    def popup_open_inv(self, dt):
        popup = MDDialog(
            text = "No Attachments have been assigned to this Notice"

        )
        popup.open()

    def popup_close(self, dt):
        Notice.popup_open.popup.dismiss()

    def download_thread(self, index):
        t = Thread(target = Notice.downloadAttch, args=(self,index,))
        t.daemon = True
        t.start()
        
    def downloadAttch(self, index):
        Clock.schedule_once(self.popup_open, 0)
        
        with open('appinfo.json','r') as f:
            data = json.load(f)
            f.close()
        try:
            print(MainData[index]["Attachments"][0])
        except IndexError:
            Clock.schedule_once(self.popup_close, 0)
            Clock.schedule_once(self.popup_open_inv, 0)
            return

        for i in range(0, len(MainData[index]["Attachments"])):
            try:
                mega.download_url(MainData[index]["Attachments"][i], data[0]["downloads_folder"])
            except:
                continue

        Clock.schedule_once(self.popup_close, 0)

    def save_notice(self, index, dt):
        with open('saved_data.json','r') as f:
            data = json.load(f)
            f.close()

        new_data = MainData[index]

        data.append(new_data)

        with open('saved_data.json','w') as f:
            data = json.dump(data, f, indent=4)
            f.close()

    def home(self):
        for child in [child for child in self.layout.children]:
            self.layout.remove_widget(child)

        TaskAppApp.build.kv.current = 'menu'
        TaskAppApp.build.kv.transition.direction = 'right'


class Saved(Screen):
    layout = StackLayout(size_hint=(1, None),orientation='rl-bt', spacing=20)
    layout.bind(minimum_height=layout.setter('height'))

    root = ScrollView(size_hint=(1, 0.8), effect_cls=ScrollEffect)
    root.add_widget(layout)
 
    def on_enter(self, *args):
        with open('saved_data.json','r') as f:
            data = json.load(f)

        global MainData
        MainData = data
        
        for i in range(0, len(data)):          
            notice = Label(text=f"{data[i]['Context']}\n\nSent by - {data[i]['Teacher']} | [b]{data[i]['Subject']}[/b] | {data[i]['Time']} {data[i]['Date']} | Due Date: {data[i]['DueDate']}",
                        markup= True,
                        padding= [15,15],
                        size_hint=(1,None),
                        halign="left", 
                        valign="middle")

            download_attch = MDRectangleFlatIconButton(
                text = 'Download Attachment',
                icon = 'download',
                pos_hint = {'center_x':0.5},
                ids = {'b':i}
            )

            download_attch.bind(on_release = partial(self.download_thread, i))

            notice.bind(size=notice.setter('text_size')) 
            notice._label.refresh()
            notice.height= (notice._label.texture.size[1] + 2*notice.padding[1])

            card = MDCard(
                height=notice.height,
                style = 'elevated',
                size_hint= (1,None),
                orientation = 'vertical'
            )

            delete = MDRectangleFlatIconButton(
                text = 'Delete',
                icon = 'trash-can-outline',
                pos_hint = {'center_x':0.5},
                ids = {'b':i}
            )

            delete.bind(on_release = partial(self.delete, i))
            
            self.layout.add_widget(delete)
            self.layout.add_widget(download_attch)
            self.layout.add_widget(card)
            card.add_widget(notice)
            
        try:
            self.add_widget(self.root)
        except:
            print("[ERROR] Couldn't add root widget, reason: root widget already exists.")
 
        return super().on_enter(*args)

    def delete(self, index, inst):
        with open('saved_data.json','r') as f:
            data = json.load(f)
            f.close()

        del data[index]

        with open('saved_data.json','w') as f:
            data = json.dump(data, f, indent=4)
            f.close()

        for child in [child for child in self.layout.children]:
            self.layout.remove_widget(child)
            
        self.on_enter()

    def popup_open(self, dt):
        Notice.popup_open.popup = MDDialog(
            text = "Downloading Attachments. Please Wait.",
            auto_dismiss=False

        )
        Notice.popup_open.popup.open()

    def popup_open_inv(self, dt):
        popup = MDDialog(
            text = "No Attachments have been assigned to this Notice"

        )
        popup.open()

    def popup_close(self, dt):
        Notice.popup_open.popup.dismiss()

    def download_thread(self, index, inst):
        t = Thread(target = Notice.downloadAttch, args=(self,index,))
        t.daemon = True
        t.start()
        
    def downloadAttch(self, index):
        Clock.schedule_once(self.popup_open, 0)
        
        with open('appinfo.json','r') as f:
            data = json.load(f)
            f.close()
        try:
            print(MainData[index]["Attachments"][0])
        except IndexError:
            Clock.schedule_once(self.popup_close, 0)
            Clock.schedule_once(self.popup_open_inv, 0)
            return

        for i in range(0, len(MainData[index]["Attachments"])):
            try:
                mega.download_url(MainData[index]["Attachments"][i], data[0]["downloads_folder"])
            except:
                continue

        Clock.schedule_once(self.popup_close, 0)

    def home(self):
        for child in [child for child in self.layout.children]:
            self.layout.remove_widget(child)

        TaskAppApp.build.kv.current = 'menu'
        TaskAppApp.build.kv.transition.direction = 'right'






class WindowManager(ScreenManager):
    pass

class TaskAppApp(MDApp):
    num = 0
    num2 = 0

    def __init__(self, **kwargs):
        self.title = "Task App - Students"
        super().__init__(**kwargs)

    def build(self):
        TaskAppApp.build.kv = Builder.load_string(kv_string)
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "DeepPurple"
        return TaskAppApp.build.kv

    def change_theme(self):
        opts = ['Red', 'Pink', 'Purple', 'DeepPurple', 'Indigo', 'Blue', 'LightBlue', 'Cyan', 'Teal', 'Green', 'LightGreen', 'Lime', 'Yellow', 'Amber', 'Orange', 'DeepOrange', 'Brown', 'Gray', 'BlueGray']
        
        try:
            self.theme_cls.primary_palette = opts[self.num]
        except IndexError:
            self.num = 0
        print(opts[self.num])

        self.num += 1

    def change_style(self):
        print(self.num2)
        opts = ['Light','Dark']
        try:
            self.theme_cls.theme_style = opts[self.num2]
        except IndexError:
            self.num2 = 0

        self.num2 += 1
        if self.num2 == 2:
            self.num2 = 0



if __name__ == '__main__':
    TaskAppApp().run()
