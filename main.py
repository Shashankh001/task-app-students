from tkinter.ttk import Separator
import kivy
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


mega = Mega()
mega._login_user()

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


<Menu>:
    Label: 
        text: 'Main Menu'
        font_size: 28
        pos_hint: {'center_x': 0.5, 'center_y':0.7}

    MDFillRoundFlatButton:
        text: "Notices"
        font_size: 18
        size_hint_x: .2
        pos_hint: {'center_x': 0.5, 'center_y':0.4}
        on_release: root.notice()

    MDFillRoundFlatButton:
        text: "Homework"
        font_size: 18
        size_hint_x: .2
        pos_hint: {'center_x': 0.5, 'center_y':0.5}
        on_release: root.homework()

    MDFillRoundFlatButton:
        text: "Downloads"
        font_size: 18
        size_hint_x: .2
        pos_hint: {'center_x': 0.5, 'center_y':0.3}
        on_release: root.downloads()

    Label:
        text: 'Version 1.0.0'
        font_size: 16
        pos_hint: {'center_x': 0.5, 'center_y':0.02}

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
"""



class Menu(Screen):
    def notice(self):
        TaskAppApp.build.kv.current = 'notice'

    def homework(self):
        TaskAppApp.build.kv.current = 'hw'

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
        data = client.get_homework()
        global MainData
        MainData = data
        
        for i in range(0, len(data)):          
            notice = Label(text=f"{data[i]['Context']}\n\n[b]Sent by - {data[i]['Teacher']} Mam | {data[i]['Subject']}[/b] | {data[i]['Time']} {data[i]['Date']}",
                        markup= True,
                        padding= [15,15],
                        size_hint=(1,None),
                        halign="left", 
                        valign="middle")


            download_attch = MDRectangleFlatIconButton(
                text = 'Download Attachment',
                icon = 'download',
                pos_hint = {'center_x':0.5},
                on_release = lambda a:self.download_thread(i)
            )

            download_attch.bind()

            notice.bind(size=notice.setter('text_size')) 
            notice._label.refresh()
            notice.height= (notice._label.texture.size[1] + 2*notice.padding[1])

            card = MDCard(
                style='elevated',
                size_hint=(1, None),
                height=notice.height,
                orientation = 'vertical'
                
            )

            self.layout.add_widget(download_attch)
            self.layout.add_widget(card)
            card.add_widget(notice)
            

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

    def download_thread(self, index):
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
        data = client.get_notices()
        global MainData
        MainData = data
        
        for i in range(0, len(data)):          
            notice = Label(text=f"{data[i]['Context']}\n\n[b]Sent by - {data[i]['Teacher']} | {data[i]['Subject']}[/b] | {data[i]['Time']} {data[i]['Date']}",
                        markup= True,
                        padding= [15,15],
                        size_hint=(1,None),
                        halign="left", 
                        valign="middle")

            download_attch = MDRectangleFlatIconButton(
                text = 'Download Attachment',
                icon = 'download',
                pos_hint = {'center_x':0.5},
                on_release = lambda a:self.download_thread(i)
            )

            download_attch.bind()

            notice.bind(size=notice.setter('text_size')) 
            notice._label.refresh()
            notice.height= (notice._label.texture.size[1] + 2*notice.padding[1])

            card = MDCard(
                style='elevated',
                size_hint=(1, None),
                height=notice.height
                
            )

            
            self.layout.add_widget(download_attch)
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

    def home(self):
        for child in [child for child in self.layout.children]:
            self.layout.remove_widget(child)

        TaskAppApp.build.kv.current = 'menu'
        TaskAppApp.build.kv.transition.direction = 'right'

class WindowManager(ScreenManager):
    pass



class TaskAppApp(MDApp):
    def __init__(self, **kwargs):
        self.title = "Task App - Students"
        super().__init__(**kwargs)

    def build(self):
        TaskAppApp.build.kv = Builder.load_string(kv_string)
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Gray"
        return TaskAppApp.build.kv


if __name__ == '__main__':
    TaskAppApp().run()
