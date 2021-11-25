from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.properties import NumericProperty, BooleanProperty, StringProperty, ObjectProperty
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.textinput import TextInput
from kivy.uix.bubble import Bubble, BubbleButton
from kivy.core.text import LabelBase
from kivy.uix.vkeyboard import VKeyboard
from kivy.clock import Clock
from kivy.uix.slider import Slider
from time import sleep
#import RPi.GPIO as GPIO
import copy
import sys
import time
from kivy.network.urlrequest import UrlRequest
import json
import csv

LabelBase.register(name='Obelix', 
                   fn_regular='ObelixPro-cyr.ttf')

LabelBase.register(name='Impacted', 
                   fn_regular='Impacted2_0-Regular.otf')
                   
LabelBase.register(name='Impact', 
                   fn_regular='impact.ttf')

LabelBase.register(name='Digital', 
                   fn_regular='Let_s_go_Digital_Regular.ttf')


ip = 'http://192.168.1.11'

tryb_pracy = 'stop'
extra_var = 0

Builder.load_file('test.kv')
     
class MenuScreen(Screen):
    def __init__(self, **kwarg):
        super().__init__(**kwarg)
        print("__init__ of MenuScreen is Called")

    def go_to_zacieranie(self):
        global tryb_pracy
        if tryb_pracy != 'warzenie':
            self.manager.current = 'zacieranie'
            

    def go_to_warzenie(self):
        global tryb_pracy
        if tryb_pracy != 'zacieranie':
            self.manager.current = 'warzenie'
            
class ZacieranieScreen(Screen):
    temp_zadana = ObjectProperty(None)
    ilosc_slodu = ObjectProperty(None)
    krok_zacierania = StringProperty('')
    zegar = StringProperty('')
    temp_akt = StringProperty('')
    waga_akt = StringProperty('')
    ilosc_wody = StringProperty('')
    dane_state = StringProperty('')

    def __init__(self, **kwarg):
        super().__init__(**kwarg)
        print("__init__ of ZacieranieScreen is Called")
        Clock.schedule_interval(self.update, 1)
        self.temperature = 0
        self.thread_on = False
        self.krok_zacierania = 'STOP'
        self.ilosc_slodu_waga = 0
        self.threadTwo = False
        self.dane_state = 'Zbieraj dane'
        #self.data = {}
    
    def text_focused(self):
        #DEFINICJA KLAWIATURY WYŚWIETLANEJ PRZY NACIŚNIĘCIU NA 'TEXTINPUT'
        VKeyboard.layout = 'numeric.json'
        player = VKeyboard()
        
        if len(self.temp_zadana.text) <= 0:  # if text empty
            self.temp_zadana.text = '0'
        elif len(self.ilosc_slodu.text) <= 0:  # if text empty
            self.temp_zadana.text = '0'
        else:
            print('empty string')

        global ip

        self.temperature = float(self.ids.temp_zadana.text)
        self.temp_zadana.text = str(round(self.temperature,2))
        #print(self.temperature)

        data = {}
        data['temperature'] = self.temp_zadana.text
        json_data = json.dumps(data)
        response = UrlRequest(ip + '/set_temp',req_body=json_data)

        self.ilosc_slodu_waga = float(self.ids.ilosc_slodu.text)
        self.ilosc_wody = str(round(self.ilosc_slodu_waga*3.5,1))

        
    def update(self, *args):
        self.zegar = str(time.asctime())

    def start_zacieranie(self):
        global tryb_pracy
        tryb_pracy = 'zacieranie'
        global extra_var
        if extra_var == 0:
                UrlRequest(ip+'/automatic')
                print('zalacz automatic')
                extra_var += 1

        if self.thread_on == False:
            Clock.schedule_interval(self.check_stan, 1)
            self.thread_on = True

    def stop_zacieranie(self):
        global tryb_pracy
        global extra_var

        tryb_pracy = 'stop'
        extra_var = 0

        Clock.unschedule(self.check_stan)
        self.krok_zacierania = 'STOP'
        self.thread_on = False

    def gotTemperature(self,req,results):
        self.temp_akt = str((json.loads(results)["temperature"]))
        self.waga_akt = str((json.loads(results)["waga"]))

    def check_stan(self, *kwargs):
        global ip

        data = UrlRequest(ip+'/temperature',self.gotTemperature)
        
        if self.temperature >= 45 and self.temperature < 50:
            self.krok_zacierania = 'przerwa beta-glukanowa'
        elif self.temperature >= 50 and self.temperature < 53.5:
            self.krok_zacierania = 'przerwa bialkowa'
        elif self.temperature >= 60.5 and self.temperature < 66.6:
            self.krok_zacierania = 'przerwa maltozowa'
        elif self.temperature >= 71.5 and self.temperature < 73.5:
            self.krok_zacierania = 'przerwa dekstrynujaca'
        elif self.temperature >= 76 and self.temperature < 80:
            self.krok_zacierania = 'wygrzew do filtracji'
        else:
            self.krok_zacierania = 'poza progami temperatury'

    def zbieraj_dane(self):
        if self.threadTwo == False:
            self.dane_state = 'Zatrzymaj zbieranie'
            Clock.schedule_interval(self.data_update, 1)
            self.threadTwo = True
            sleep(0.5)
        elif self.threadTwo == True:
            self.dane_state = 'Zbieraj dane'
            Clock.unschedule(self.data_update)
            self.threadTwo = False

    def data_update(self,*args):
        dane_wykr = 21.37
        f = open('dane.csv','a')
        f.write(str(dane_wykr)+'\n')
        f.close()

class WarzenieScreen(Screen):
    slider = NumericProperty(0)
    moc_zad = StringProperty('')
    zegar = StringProperty('')
    moc_akt = StringProperty('')
    akt_temp = StringProperty('')
    czas_stoper = ObjectProperty(None)
    stoper = StringProperty('')

    def __init__(self, **kwarg):
        super().__init__(**kwarg)
        print("__init__ of WarzenieScreen is Called")
        Clock.schedule_interval(self.update, 1)
        self.moc = 0
        self.kasuj_moc = False
        self.pozostaly_czas = 60
        self.extraVar = False
        self.min = 0
        self.sec = 60
        self.extraVar2 = False
        self.stoper = '60.00'

    def on_enter(self):
        if self.extraVar == False:
            self.text_focused()

    def text_focused(self):
        VKeyboard.layout = 'numeric.json'
        player = VKeyboard()
        
        if len(self.czas_stoper.text) <= 0:  # if text empty
            self.czas_stoper.text = '0'

        self.pozostaly_czas = int(self.ids.czas_stoper.text)
        self.czas = self.pozostaly_czas
        self.stoper = str(self.pozostaly_czas)+'.00'

    def slider_moc(self, value):
        if self.kasuj_moc == True:
            self.moc = int(value)
            data = {}
            data['moc'] = int(self.moc)
            json_data = json.dumps(data)
            response = UrlRequest(ip+'/set_moc',req_body=json_data)
            #print(self.moc)
        else:
            value = 0
            self.moc = int(value)
            self.moc_akt = '0'
            #print(self.moc)

    def gotTemperature(self,req,results):
        self.akt_temp = str((json.loads(results)["temperature"]))

    def update(self, *args):
        self.zegar = str(time.asctime())
        global ip
        data = UrlRequest(ip+'/temperature',self.gotTemperature)

    def start_warzenie(self):
        self.kasuj_moc = True
        global extra_var
        global tryb_pracy
        tryb_pracy = 'warzenie'
        if extra_var == 0:
                UrlRequest(ip+'/manual')
                print('zalaczam manual')
                extra_var += 1

    def stop_warzenie(self):
        global tryb_pracy
        global extra_var

        tryb_pracy = 'stop'
        extra_var = 0

        self.kasuj_moc = False
        self.moc = 0
        data = {}
        data['moc'] = int(self.moc)
        json_data = json.dumps(data)
        response = UrlRequest(ip+'/set_moc',req_body=json_data)

    def stoper_start(self):
        #self.stoper = str(self.pozostaly_czas)
        if self.extraVar == False:
            Clock.schedule_interval(self.update_stoper, 1)
            self.extraVar = True

    def stoper_stop(self):
        Clock.unschedule(self.update_stoper)
        self.extraVar = False
        self.extraVar2 = True

    def stoper_zeruj(self):
        if self.extraVar2==True:
            self.pozostaly_czas = self.czas
            self.stoper = str(self.czas) + '.00'
            self.min = 0
            self.sec = 60
            self.extraVar = False

    def update_stoper(self,*args):
        #self.min = 0
        #self.sec = 60
        self.sec-=1
        if self.sec == 0:
            self.min += 1
            self.sec = 60

        if self.sec>9:
            self.stoper = str(self.pozostaly_czas-self.min-1)+'.' + str(self.sec)
        elif self.sec<10:
            self.stoper = str(self.pozostaly_czas-self.min-1)+'.0' + str(self.sec)

        if (self.pozostaly_czas-self.min-1)<10:
            self.stoper = '0'+str(self.pozostaly_czas-self.min-1)+'.' + str(self.sec)
            if self.sec<10:
                self.stoper = '0'+str(self.pozostaly_czas-self.min-1)+'.0' + str(self.sec)

        if self.pozostaly_czas-self.min == 0:
            self.stoper_stop()
            sleep(.1)
            self.stoper_zeruj()

class WagaScreen(Screen):
    pass

class WykresTempScreen(Screen):

    def __init__(self, **kwarg):
        super().__init__(**kwarg)
        print("__init__ of WarzenieScreen is Called")
        #Clock.schedule_interval(self.update, 1)
        self.moc = 0
        
    

class PrzepisyScreen(Screen):
    styl_piwa = StringProperty('')
    blg = StringProperty('')
    ibu = StringProperty('')
    slod1 = StringProperty('')
    slod2 = StringProperty('')
    slod3 = StringProperty('')
    slod4 = StringProperty('')
    temp1 = StringProperty('')
    temp2 = StringProperty('')
    temp3 = StringProperty('')
    temp4 = StringProperty('')
    visib = NumericProperty(0)

    def __init__(self, **kwarg):
        super().__init__(**kwarg)
        print("__init__ of WarzenieScreen is Called")
        self.recipe = 0
        self.extra_var = False

    def go_to_menu(self):
        Clock.unschedule(self.update)
        self.manager.current = 'menu'
        self.extra_var = False

    def schreibersdorf(self):
        if self.extra_var == False:
            Clock.schedule_interval(self.update, .5)
            self.extra_var = True
        self.recipe = 1

    def ale(self):
        if self.extra_var == False:
            Clock.schedule_interval(self.update, .5)
            self.extra_var = True
        self.recipe = 2

    def summer_ale(self):
        if self.extra_var == False:
            Clock.schedule_interval(self.update, .5)
            self.extra_var = True
        self.recipe = 3

    def stout(self):
        if self.extra_var == False:
            Clock.schedule_interval(self.update, .5)
            self.extra_var = True
        self.recipe = 4

    def update(self, *kwargs):
        if self.recipe == 0:
            self.visib = 0
        else:
            self.visib = 1

        if self.recipe == 1:
            self.styl_piwa = 'SCHREIBERSDORF ALTBIER'
            self.ibu = '17.5'
            self.blg = '11.4'
            self.slod1 = 'Monachijski Jasny - 7.5 kg'
            self.slod2 = 'Karmelowy 300EBC - 0.7 kg'
            self.slod3 = ''
            self.slod4 = ''
            self.temp1 = '53*C - 15 min'
            self.temp2 = '63*C - 30 min'
            self.temp3 = '73*C - 30 min'
            self.temp4 = '78*C - 5 min'
        elif self.recipe == 2:
            self.styl_piwa = 'DZIUBROW IPA'
            self.ibu = '40'
            self.blg = '13'
            self.slod1 = 'Monachijski Jasny - 2.5 kg'
            self.slod2 = 'Karmelowy 300EBC - 0.7 kg'
            self.slod3 = 'Pszeniczny Jasny - 1.0 kg'
            self.slod4 = 'Pilznenski Jasny - 3.0 kg'
            self.temp1 = '53*C - 15 min'
            self.temp2 = '63*C - 30 min'
            self.temp3 = '73*C - 30 min'
            self.temp4 = '78*C - 5 min'
        elif self.recipe == 3:
            self.styl_piwa = 'DZIUBROW SUMMER ALE'
            self.ibu = '37'
            self.blg = '12'
            self.slod1 = 'Monachijski Jasny - 7.5 kg'
            self.slod2 = 'Karmelowy 300EBC - 0.7 kg'
            self.slod3 = 'Pszeniczny Jasny - 1.0 kg'
            self.slod4 = 'Pilznenski Jasny - 3.0 kg'
            self.temp1 = '63*C - 30 min'
            self.temp2 = '73*C - 30 min'
            self.temp3 = '78*C - 5 min'
            self.temp4 = ''
        elif self.recipe == 4:
            self.styl_piwa = 'DZIUBROW DRY STOUT'  
            self.ibu = '20'
            self.blg = '12' 
            self.slod1 = 'Monachijski Jasny - 7.5 kg'
            self.slod2 = 'Karmelowy 300EBC - 0.7 kg'
            self.slod3 = 'Pszeniczny Jasny - 1.0 kg'
            self.slod4 = 'Pilznenski Jasny - 3.0 kg'
            self.temp1 = '53*C - 15 min'
            self.temp2 = '63*C - 30 min'
            self.temp3 = '73*C - 30 min'
            self.temp4 = '78*C - 5 min'
        elif self.recipe == 0:
            pass

class SampleApp(App):

    def build(self):
        # Create the screen manager
        sm = ScreenManager()
        sm.add_widget(MenuScreen(name='menu'))
        sm.add_widget(ZacieranieScreen(name='zacieranie'))
        sm.add_widget(WarzenieScreen(name='warzenie'))
        sm.add_widget(WagaScreen(name='waga'))
        sm.add_widget(WykresTempScreen(name='wykres'))
        sm.add_widget(PrzepisyScreen(name='przepisy'))
        
        return sm
    
if __name__ == '__main__':
    Window.size=(1024,600)
    Window.fullscreen = False
    SampleApp().run()
