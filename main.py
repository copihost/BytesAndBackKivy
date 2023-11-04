from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from tkinter import filedialog
from kivy.properties import ObjectProperty
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from bytesAndBack import BytesAndBack
from kivy.uix.progressbar import ProgressBar
from threading import Thread
BNBClass = BytesAndBack()


class MainWindow(Screen):

    pathToFile = ObjectProperty(None)

    def submit(self):
        if self.pathToFile.text != "":
            BNBClass.filePath = self.pathToFile.text
            sm.current = "second"
        else:
            invalidPath()

    def pickFile(self):
        try:
            self.pathToFile.text = ""
            self.pathToFile.text += filedialog.askopenfile().name
        except:
            pass

class SecondWindow(Screen):
    pathToFolder = ObjectProperty(None)

    def submit(self):
        if self.pathToFolder.text != "":
                BNBClass.storagePath = self.pathToFolder.text
                BNBClass.destPath = self.pathToFolder.text
                sm.current = "third"

        else:
            invalidPath()

    def pickFile(self):
        try:
            self.pathToFolder.text = ""
            self.pathToFolder.text += filedialog.askdirectory()
        except:
            pass

class ThirdWindow(Screen):
    check = False
    startButton = ObjectProperty(None)
    prog = ProgressBar(max=100,pos_hint={'x':.25 , 'y':.2 },size_hint=(.5,.1 ))
    def __init__(self, **kwargs):
        super(ThirdWindow, self).__init__(**kwargs)
        
    
    def unpackFile(self):
        t1 = Thread(target=BNBClass.unpackFile, args=(self.prog,))
        t1.start()
        self.check = True
        self.ids.FLayout.add_widget(self.prog)
        hide_widget(self.startButton)
        
    def submit(self):
        if self.check:
            sm.current = "fourth"

class FourthWindow(Screen):
    pathToFolder = ObjectProperty(None)

    def submit(self):
        if self.pathToFolder.text != "":
                BNBClass.destPath = self.pathToFolder.text
                sm.current = "fifth"
        else:
            invalidPath()

    def pickFile(self):
        try:
            self.pathToFolder.text = ""
            self.pathToFolder.text += filedialog.askdirectory()
        except:
            pass

class FifthWindow(Screen):
    check = False
    startButton = ObjectProperty(None)
    prog = ProgressBar(max=100,pos_hint={'x':.25 , 'y':.2 },size_hint=(.5,.1 ))
    def __init__(self, **kwargs):

        super(FifthWindow, self).__init__(**kwargs)

    def packFile(self):
        t1 = Thread(target=BNBClass.packFile, args=(self.prog,))
        t1.start()
        self.ids.FLayout.add_widget(self.prog)
        hide_widget(self.startButton)
        

def hide_widget(wid, dohide=True):

    if hasattr(wid, 'saved_attrs'):
        if not dohide:
            wid.height, wid.size_hint_y, wid.opacity, wid.disabled = wid.saved_attrs
            del wid.saved_attrs

    elif dohide:
        wid.saved_attrs = wid.height, wid.size_hint_y, wid.opacity, wid.disabled
        wid.height, wid.size_hint_y, wid.opacity, wid.disabled = 0, None, 0, True


class WindowManager(ScreenManager):
    pass

def invalidPath():

    pop = Popup(title="Invalid Path",
                content=Label(text="please choose a correct path"),
                size_hint=(None, None), size=(200,200))
    pop.open()

sm = WindowManager()
kv = Builder.load_file("appstyle.kv")


screens = [MainWindow(name="main"), SecondWindow(name="second"), 
           ThirdWindow(name="third"), FourthWindow(name='fourth'),FifthWindow(name="fifth")]

for screen in screens:

    sm.add_widget(screen)

sm.current = 'main'


class MyMainApp(App):
    def build(self):
        return sm

if __name__=="__main__":
    MyMainApp().run()
