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
from kivy.uix.vkeyboard import VKeyboard
from kivy.clock import Clock
from time import sleep
#import RPi.GPIO as GPIO
import copy
import sys
import time


Builder.load_string('''
<MenuScreen>
    name: 'menu'
    FloatLayout:
        FloatLayout:
            size: root.width, root.height
            
            Label:
                text: "APLIKACJA STEROWANIA KADZIĄ DO WARZENIA BRZECZKI PIWNEJ"
                pos_hint: {'x':0.275,'y':0.9}
                font_size: 30
                halign: 'center'
                size_hint: (.45, .115)
            
            Image:
                source: 'brewing-process.jpg'
                size: (900,120)
                pos_hint: {'x':0.001,'y':-0.23}
                #GRAFIKA: https://www.foghornbrewhouse.com.au/newcastle/craft-beer-brewhouse-brewery/
                
        GridLayout:
            #pos: (256,340)
            pos_hint: {'x':0.1,'y':0.6}
            size_hint: (.8,.25)
            cols: 4
            rows: 1
            
            spacing: 0
            
            Button:
                size_hint: (.2, .2)
                font_size: 32
                text: 'ZACIERANIE'
                on_press: root.manager.current = 'zacieranie'
                background_color: (71/255,71/255,69/255,1)
            Button:
                size_hint: (.2, .2)
                font_size: 32
                text: 'WARZENIE'
                on_press: root.manager.current = 'warzenie'
                background_color: (71/255,71/255,69/255,1)
            Button:
                size_hint: (.2, .2)
                font_size: 32
                text: 'WAGA'
                on_press: root.manager.current = 'waga'
                background_color: (71/255,71/255,69/255,1)
            Button:
                size_hint: (.2, .2)
                font_size: 32
                text: 'PRZEPISY'
                on_press: root.manager.current = 'przepisy'
                background_color: (71/255,71/255,69/255,1)
                
<ZacieranieScreen>
    name: 'zacieranie'
    FloatLayout:
        FloatLayout:
            size: root.width, root.height
            
            Button:
                size_hint: (0.2, 0.1)
                pos: (10,530)
                font_size: 26
                text: 'Powr\u00f3t do menu'
                #background_color: (34/255,227/255,20/255,1)
                on_press: root.manager.current = 'menu'
                
            Label:
                text: "STEROWANIE KADZIĄ DO WARZENIA BRZECZKI PIWNEJ"
                pos: (0.5,0)
                pos: (0.5,0)
                font_size: 30
                size_hint: (.45, .115)
                background_color: (2/255,20/255,33/255,1)
                canvas.before:
                    Color:
                        rgba: self.background_color
                    Rectangle:
                        size: self.size
                        pos: self.pos
        
        
<WarzenieScreen>
    name: 'warzenie'
    FloatLayout:
        FloatLayout:
            size: root.width, root.height
            
            Button:
                size_hint: (0.2, 0.1)
                pos: (10,530)
                font_size: 26
                text: 'Powr\u00f3t do menu'
                #background_color: (34/255,227/255,20/255,1)
                on_press: root.manager.current = 'menu'
                
<WagaScreen>
    name: 'waga'
    FloatLayout:
        FloatLayout:
            size: root.width, root.height
            
            Button:
                size_hint: (0.2, 0.1)
                pos: (10,530)
                font_size: 26
                text: 'Powr\u00f3t do menu'
                #background_color: (34/255,227/255,20/255,1)
                on_press: root.manager.current = 'menu'
''')
        
        
class MenuScreen(Screen):
    pass
    
class ZacieranieScreen(Screen):
    pass
    
class WarzenieScreen(Screen):
    pass
    
class WagaScreen(Screen):
    pass

class WykresTempScreen(Screen):
    pass
    
class PrzepisyScreen(Screen):
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
