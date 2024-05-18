from kivy.config import Config

Config.set("graphics", "resizable", 0)
Config.set("graphics", "width", 350)
Config.set("graphics", "height", 600)
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.popup import Popup
from kivy.core.window import Window
from kivy.properties import NumericProperty, StringProperty
from kivy.core.audio import SoundLoader
from kivy.clock import Clock

#Window.size = (450,700)

class MyPopup(Popup): 
    def __init__(self, masage,**kwargs):
        self.Masage = masage
        super().__init__(**kwargs)

class Auth(Screen):
    def check_pas(self):
        if self.ids["inp_name"].text == "" and self.ids["inp_pasw"].text == "":
            self.manager.current= 'choice'
            self.manager.transition.direction = "up"
        else:
            self.popup = MyPopup("Невірне ім'я чи пароль",title="Помилка авторизації")
            self.popup.open()

class Choise(Screen):
    score = NumericProperty()
    def on_enter(self, *args):
        self.txt = 0
        Clock.schedule_interval(self.to_do,0.1) 
        return super().on_enter(*args)
    def to_do(self,td):
        if self.txt < self.score:
            self.txt += 1
            self.ids["mark"].text = str(self.txt)
        else:
            self.ids["mark"].text = str(self.score)
            return False
class Learn(Screen):
    word = StringProperty()
    def say(self,btn):
        self.word = btn.word
        try:
            audio = SoundLoader.load(btn.audio)
            audio.play()
        except:
            pass


class Test(Screen):
    word = StringProperty()
    word_ua = StringProperty()
    markk = NumericProperty()
    def __init__(self, **kw):
        self.markk = 0
        super().__init__(**kw)
    def say(self,btn):
        self.word = btn.word
        self.word_ua = btn.word_ua
        SoundLoader.load(btn.audio).play()
    def check(self):
        txt = ""
        if self.ids["en"].text.lower() == self.word:
            txt += "Англ слово вірне +1 бал \n "
            self.markk += 1
        else:
            txt += "Англ слово невірне -1 бал \n "
            self.markk -= 1
        if self.ids["ua"].text.lower()  == self.word_ua:
            txt += "Укр слово вірне +1 бал \n "
            self.markk += 1
        else:
            txt += "Укр слово невірне -1 бал \n "
            self.markk -= 1
        msg = MyPopup(txt,title="Result",size_hint=(0.7,0.45))
        msg.open()
        self.ids["en"].text = ""
        self.ids["ua"].text = ""

class EnglishApp(App):
    icon = "image\icon.jpg"
    mark = NumericProperty()
    data_key = StringProperty()
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.mark = 15
        self.data_key = "animal"
    def build(self):
        sm = ScreenManager()
        sm.add_widget(Auth(name="auth"))
        sm.add_widget(Choise(name="choice"))
        sm.add_widget(Learn(name="learn"))
        sm.add_widget(Test(name="test"))
        return sm
EnglishApp().run()

        