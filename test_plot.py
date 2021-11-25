# importing pyplot for graph plotting
from matplotlib import pyplot as plt
  
# importing numpy
import numpy as np
from kivy.garden.matplotlib import FigureCanvasKivyAgg
from kivy.clock import Clock
from kivy.uix.screenmanager import ScreenManager, Screen

# importing kivyapp
from kivy.app import App
  
# importing kivy builder
from kivy.lang import Builder
from random import *
  
# this is the main class which will 
# render the whole application
class MenuScreen(Screen):
    def update(self,*kwargs):
        self.signal.append(randrange(15))
        print(self.signal)
        plt.clf()
        plt.plot(np.array(self.signal))

    def build(self):
        self.str = Builder.load_string(""" 
  
BoxLayout:
    layout:layout
      
    BoxLayout:
      
        id:layout
      
                                """)
  
        self.signal = [7, 89.6, 45,-56.34]
  
        signalnp = np.array(self.signal)
          
        # this will plot the signal on graph
        plt.plot(signalnp)

        # setting x label
        plt.xlabel('Time(s)')
          
        # setting y label
        plt.ylabel('signal (norm)')
        plt.grid(True, color='lightgray')
        Clock.schedule_interval(self.update, 1)
        # adding plot to kivy boxlayout
        self.str.layout.add_widget(FigureCanvasKivyAgg(plt.gcf()))
        return self.str
  
class uiApp(App):

    def build(self):
        # Create the screen manager
        sm = ScreenManager()
        
        sm.add_widget(MenuScreen(name='menu'))
        sm.current = 'menu'
        
        return sm
    
if __name__ == '__main__':

    uiApp().run()
# running the application
