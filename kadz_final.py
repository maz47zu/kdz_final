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

Builder.load_string('''
<MenuScreen>
    name: 'menu'
    FloatLayout:
        FloatLayout:
            size: root.width, root.height
            
            Image:
                source: 'menu_kadz_1.jpg'
                size: (1024,600)
                pos_hint: {'x':0,'y':0}
                #GRAFIKA: https://www.foghornbrewhouse.com.au/newcastle/craft-beer-brewhouse-brewery/
                
        GridLayout:
            #pos: (256,340)
            pos_hint: {'x':0.1,'y':0.42}
            size_hint: (.8,.25)
            cols: 4
            rows: 1
            
            spacing: 5
            
            Button:
                size_hint: (.2, .2)
                font_name:"Impacted"
                font_size: 36
                text: 'ZACIERANIE'
                on_press: root.go_to_zacieranie()
                #on_press: root.manager.current = 'zacieranie'
                background_color: (71/255,71/255,69/255,1)
            Button:
                size_hint: (.2, .2)
                font_name:"Impacted"
                font_size: 36
                text: 'WARZENIE'
                on_press: root.go_to_warzenie()
                #on_press: root.manager.current = 'warzenie'
                background_color: (71/255,71/255,69/255,1)
            Button:
                size_hint: (.2, .2)
                font_name:"Impacted"
                font_size: 36
                text: 'WAGA'
                #on_press: root.manager.current = 'waga'
                background_color: (71/255,71/255,69/255,1)
            Button:
                size_hint: (.2, .2)
                font_name:"Impacted"
                font_size: 36
                text: 'PRZEPISY'
                on_press: root.manager.current = 'przepisy'
                background_color: (71/255,71/255,69/255,1)
                
<ZacieranieScreen>
    name: 'zacieranie'
    temp_zadana: temp_zadana

    FloatLayout:
        FloatLayout:
            size: root.width, root.height

            Image:
                source: 'Logo_male_tlo_czarne.jpg'
                size: .2,.1
                pos_hint: {'x':-.35,'y':-.42}
            
            Button:
                size_hint: (0.25, 0.1)
                pos: (10,530)
                font_name:"Impacted"
                font_size: 36
                text: 'menu'
                background_color: (71/255,71/255,69/255,1)
                on_press: root.manager.current = 'menu'
                
            Button:
                size_hint: (0.25, 0.1)
                pos: (495,530)
                font_name:"Impacted"
                font_size: 32
                text: 'ZACIERANIE START'
                background_color: (47/255,204/255,12/255,1)
                on_press: root.start_zacieranie()

            Button:
                size_hint: (0.25, 0.1)
                pos: (755,530)
                font_name:"Impacted"
                font_size: 32
                text: 'ZACIERANIE STOP'
                background_color: (255/255,0/255,0/255,1)
                on_press: root.stop_zacieranie()

        GridLayout:
            pos: (450,300)
            size_hint: (.5,.3)
            cols: 3
            rows: 3
        
            Label:
                text: "Temp. Zadana (wpisz) :"
                halign: 'left'
                font_name:"Impacted"
                font_size: 32
                size_hint: (1.5,1)
                background_color: (71/255,71/255,69/255,1)
            Label:
                text: ""
                halign: 'left'
                font_name:"Impacted"
                font_size: 32
                size_hint: (1,1)
                background_color: (0,0,0,1)

            TextInput:
                id: temp_zadana
                text: "0"
                halign: 'center'
                font_name:"Digital"
                font_size: 55
                size_hint: (1,1)
                multiline: False
                #background_color: (71/255,71/255,69/255,1)
                background_color: (0/255,0/255,0/255,1)
                foreground_color: [1,1,1,1]
                on_focus: root.text_focused()
            Label:
                text: "temp. Aktualna :"
                halign: 'left'
                font_name:"Impacted"
                font_size: 32
                size_hint: (1.5,1)
                background_color: (71/255,71/255,69/255,1)
            Label:
                text: ""
                halign: 'left'
                font_name:"Impacted"
                font_size: 32
                size_hint: (1,1)
                background_color: (0,0,0,1)
            Label:
                id: temp_akt
                text: root.temp_akt
                halign: 'left'
                font_name:"Digital"
                font_size: 55
                size_hint: (1,1)
                background_color: (0,0,0,1)
            Label:
                text: "Waga aktualna :"
                halign: 'left'
                font_name:"Impacted"
                font_size: 32
                size_hint: (1.5,1)
                background_color: (71/255,71/255,69/255,1)
            Label:
                text: ""
                halign: 'left'
                font_name:"Impacted"
                font_size: 32
                size_hint: (1,1)
                background_color: (0,0,0,1)
            Label:
                id: waga_akt
                text: root.waga_akt
                halign: 'left'
                font_name:"Digital"
                font_size: 55
                size_hint: (1,1)
                background_color: (0,0,0,1)

        GridLayout:
            pos_hint: {'x':.55,'y':-.05}
            size_hint: (.4,.2)
            cols: 1
            rows: 1
            Label:
                id: zegar
                text: root.zegar
                font_name:"Digital"
                halign: 'right'
                font_size: 50
                size_hint: (.5,1)

        GridLayout:
            pos_hint: {'x':.5,'y':.25}
            size_hint: (.4,.2)
            cols: 1
            rows: 2
        
            Label:
                text: "AKTUALNY KROK ZACIERANIA (wg. temp) :"
                halign: 'left'
                font_name:"Impacted"
                font_size: 30
                size_hint: (1,1)
                background_color: (71/255,71/255,69/255,1)
            Label:
                id: krok_zacierania
                text: root.krok_zacierania
                font_name:"Impacted"
                halign: 'left'
                font_size: 36
                size_hint: (1,1)
                background_color: (71/255,71/255,69/255,1)

            
        
<WarzenieScreen>
    name: 'warzenie'
    FloatLayout:
        FloatLayout:
            size: root.width, root.height
            
            Button:
                size_hint: (0.25, 0.1)
                pos: (10,530)
                font_name:"Impacted"
                font_size: 36
                text: 'menu'
                background_color: (71/255,71/255,69/255,1)
                on_press: root.manager.current = 'menu'
            Button:
                size_hint: (0.25, 0.1)
                pos: (495,530)
                font_name:"Impacted"
                font_size: 32
                text: 'Warzenie START'
                background_color: (47/255,204/255,12/255,1)
                on_press: root.start_warzenie()

            Button:
                size_hint: (0.25, 0.1)
                pos: (755,530)
                font_name:"Impacted"
                font_size: 32
                text: 'Warzenie STOP'
                background_color: (255/255,0/255,0/255,1)
                on_press: root.stop_warzenie()

            Label:
                text: "Ustaw moc grzania [%]:"
                font_name:"Impacted"
                halign: 'left'
                font_size: 30
                size_hint: (.3,.1)
                pos_hint: {'x':.5,'y':.75}

            Image:
                source: 'Logo_male_tlo_czarne.jpg'
                size: (100,50)
                pos_hint: {'x':-.35,'y':-.42}

            Slider:
                id: slider
                min: 0
                max: 100
                step: 1
                value_track: True
                value_track_color: (0,1,0,1)
                orientation: 'horizontal'
                pos_hint: {'x':.45,'y':.6}
                size_hint: (.5,.2)
                on_value: moc_zad.text = str(int(self.value))
                on_touch_up: root.slider_moc(moc_zad.text)
            
            
        
        GridLayout:
            pos_hint: {'x':.5,'y':.35}
            size_hint: (.4,.3)
            cols: 2
            rows: 3
            Label:
                text: "USTAWIONA MOC:"
                font_name:"Impacted"
                halign: 'left'
                font_size: 30
                size_hint: (1.5,1)
            Label:
                id: moc_zad
                text: '0'
                font_name:"Digital"
                halign: 'right'
                font_size: 55
                size_hint: (.5,1)
            Label:
                text: "Aktualna MOC:"
                font_name:"Impacted"
                halign: 'left'
                font_size: 30
                size_hint: (1.5,1)
            Label:
                id: moc_akt
                text: '0'
                font_name:"Digital"
                halign: 'right'
                font_size: 55
                size_hint: (.5,1)
            Label:
                text: "Temp. Aktualna:"
                font_name:"Impacted"
                halign: 'left'
                font_size: 30
                size_hint: (1.5,1)
            Label:
                id: akt_temp
                text: root.akt_temp
                font_name:"Digital"
                halign: 'right'
                font_size: 55
                size_hint: (.5,1)
        
        GridLayout:
            pos_hint: {'x':.55,'y':-.05}
            size_hint: (.4,.2)
            cols: 1
            rows: 1
            Label:
                id: zegar
                text: root.zegar
                font_name:"Digital"
                halign: 'right'
                font_size: 50
                size_hint: (.5,1)
                
<WagaScreen>
    name: 'waga'
    FloatLayout:
        FloatLayout:
            size: root.width, root.height
            
            Button:
                size_hint: (0.25, 0.1)
                pos: (10,530)
                font_name:"Impacted"
                font_size: 36
                text: 'menu'
                background_color: (71/255,71/255,69/255,1)
                on_press: root.manager.current = 'menu'

            Image:
                source: 'Logo_male_tlo_czarne.jpg'
                size: (100,50)
                pos_hint: {'x':-.35,'y':-.42}

<PrzepisyScreen>
    name: 'przepisy'
    FloatLayout:
        FloatLayout:
            size: root.width, root.height

            Button:
                size_hint: (0.25, 0.1)
                pos: (10,530)
                font_name:"Impacted"
                font_size: 36
                text: 'menu'
                background_color: (71/255,71/255,69/255,1)
                on_press: root.go_to_menu()

            Image:
                source: 'Logo_male_tlo_czarne.jpg'
                size: (100,50)
                pos_hint: {'x':-.35,'y':-.42}
            
            Label:
                id: styl_piwa
                text: root.styl_piwa
                font_name:"Impacted"
                halign: 'right'
                font_size: 55
                size_hint: (.5,.1)
                pos_hint: {'x':.4,'y':.9}
            
            Label:
                text: 'Surowce (40L):'
                font_name:"Impacted"
                halign: 'left'
                font_size: 28
                color: 194/255,130/255,12/255,root.visib
                size_hint: (.1,.1)
                pos_hint: {'x':.3,'y':.74}
            Label:
                text: 'Zacieraniie :'
                font_name:"Impacted"
                halign: 'left'
                font_size: 28
                color: 194/255,130/255,12/255,root.visib
                size_hint: (.1,.1)
                pos_hint: {'x':.315,'y':.45}

        GridLayout:
            pos_hint: {'x':.28,'y':.55}
            size_hint: (.35,.2)
            cols: 1
            rows: 4

            Label:
                id: slod1
                text: root.slod1
                text_size: self.size
                font_name:"Impacted"
                halign: 'left'
                valign: 'middle'
                font_size: 28
                color: 194/255,130/255,12/255,root.visib
                size_hint: (.1,.1)
            Label:
                id: slod2
                text: root.slod2
                font_name:"Impacted"
                text_size: self.size
                halign: 'left'
                valign: 'middle'
                font_size: 28
                color: 194/255,130/255,12/255,root.visib
                size_hint: (.1,.1)
            Label:
                id: slod3
                text: root.slod3
                font_name:"Impacted"
                text_size: self.size
                halign: 'left'
                valign: 'middle'
                font_size: 28
                color: 194/255,130/255,12/255,root.visib
                size_hint: (.1,.1)
            Label:
                id: slod4
                text: root.slod4
                font_name:"Impacted"
                text_size: self.size
                halign: 'left'
                valign: 'middle'
                font_size: 28
                color: 194/255,130/255,12/255,root.visib
                size_hint: (.1,.1)

        GridLayout:
            pos_hint: {'x':.28,'y':.26}
            size_hint: (.35,.2)
            cols: 1
            rows: 4

            Label:
                id: temp1
                text: root.temp1
                text_size: self.size
                font_name:"Impacted"
                halign: 'left'
                valign: 'middle'
                font_size: 28
                color: 194/255,130/255,12/255,root.visib
                size_hint: (.1,.1)
            Label:
                id: temp2
                text: root.temp2
                font_name:"Impacted"
                text_size: self.size
                halign: 'left'
                valign: 'middle'
                font_size: 28
                color: 194/255,130/255,12/255,root.visib
                size_hint: (.1,.1)
            Label:
                id: temp3
                text: root.temp3
                font_name:"Impacted"
                text_size: self.size
                halign: 'left'
                valign: 'middle'
                font_size: 28
                color: 194/255,130/255,12/255,root.visib
                size_hint: (.1,.1)
            Label:
                id: temp4
                text: root.temp4
                font_name:"Impacted"
                text_size: self.size
                halign: 'left'
                valign: 'middle'
                font_size: 28
                color: 194/255,130/255,12/255,root.visib
                size_hint: (.1,.1)
        
        GridLayout:
            pos_hint: {'x':.4,'y':.82}
            size_hint: (.5,.1)
            cols: 4
            rows: 1

            Label:
                text: "IBU"
                font_name:"Impacted"
                halign: 'right'
                font_size: 40
                color: 0,138/255,0,root.visib
                size_hint: (.5,.1)
            Label:
                id: ibu
                text: root.ibu
                font_name:"Impacted"
                halign: 'center'
                font_size: 40
                color: 0,138/255,0,root.visib
                size_hint: (.5,.1)
            Label:
                text: "BLG"
                font_name:"Impacted"
                halign: 'center'
                font_size: 40
                color: 222/255,81/255,0,root.visib
                size_hint: (.5,.1)
            Label:
                id: blg
                text: root.blg
                font_name:"Impacted"
                halign: 'center'
                font_size: 40
                color: 222/255,81/255,0,root.visib
                size_hint: (.5,.1)

        GridLayout:
            pos_hint: {'x':.01,'y':.25}
            size_hint: (.25,.6)
            cols: 1
            rows: 4

            spacing: 5

            Button:
                size_hint: (.2, .2)
                font_name:"Impacted"
                font_size: 24
                text: 'Schreibersdorf ALTBIER'
                on_press: root.schreibersdorf()
                background_color: (71/255,71/255,69/255,1)
            Button:
                size_hint: (.2, .2)
                font_name:"Impacted"
                font_size: 24
                text: 'Dziubrow IPA'
                on_press: root.ale()
                background_color: (71/255,71/255,69/255,1)
            Button:
                size_hint: (.2, .2)
                font_name:"Impacted"
                font_size: 24
                text: 'Dziubrow SUMMER ALE'
                on_press: root.summer_ale()
                background_color: (71/255,71/255,69/255,1)
            Button:
                size_hint: (.2, .2)
                font_name:"Impacted"
                font_size: 24
                text: 'Dziubrow DRY STOUT'
                on_press: root.stout()
                background_color: (71/255,71/255,69/255,1)
''')
        
        
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
    krok_zacierania = StringProperty('')
    zegar = StringProperty('')
    temp_akt = StringProperty('')
    waga_akt = StringProperty('')

    def __init__(self, **kwarg):
        super().__init__(**kwarg)
        print("__init__ of ZacieranieScreen is Called")
        Clock.schedule_interval(self.update, 1)
        self.temperature = 0
        self.thread_on = False
        self.krok_zacierania = 'STOP'
        #self.data = {}
    
    def text_focused(self):
        #DEFINICJA KLAWIATURY WYŚWIETLANEJ PRZY NACIŚNIĘCIU NA 'TEXTINPUT'
        VKeyboard.layout = 'numeric.json'
        player = VKeyboard()
        
        if len(self. temp_zadana.text) <= 0:  # if text empty
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

class WarzenieScreen(Screen):
    slider = NumericProperty(0)
    moc_zad = StringProperty('')
    zegar = StringProperty('')
    moc_akt = StringProperty('')
    akt_temp = StringProperty('')

    def __init__(self, **kwarg):

        super().__init__(**kwarg)
        print("__init__ of WarzenieScreen is Called")
        Clock.schedule_interval(self.update, 1)
        self.moc = 0
        self.kasuj_moc = False

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

class WagaScreen(Screen):
    pass

class WykresTempScreen(Screen):
    pass
    
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

class TestApp(App):

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
    TestApp().run()
