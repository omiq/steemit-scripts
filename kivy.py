import time
import kivy
from kivy.app import App
from kivy.core.window import Window
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.core.audio import SoundLoader
from kivy.core.window import Window
from kivy.uix.camera import Camera

# logging
from kivy.logger import Logger
import logging

Logger.setLevel(logging.TRACE)


def end():
    sound = SoundLoader.load('fantastic.mp3')
    sound.play()
    time.sleep(4)
    exit()


def snap(instance):
    root = (instance.parent).parent
    camera = (root.children[0])
    camera.export_to_png("snap.png")


def callback(instance):
    root = instance.parent
    root.children[0].text = ('"%s" was clicked!' % str(instance.pos))
    if (instance.text == "Exit"):
        end()
    if (instance.text == "Snap"):
        snap(instance)


class MyApp(App):

    def build(self):
        # Fix the window size
        # Window.size = (800, 800)

        # Camera
        camera = Camera()

        # Label
        lab = Label(text="Label")

        # First Button
        butt1 = Button(text='Hello world 1')
        butt1.bind(on_press=callback)

        # Second Button
        butt2 = Button(text='Snap')
        butt2.bind(on_press=callback)

        # Exit Button
        butt3 = Button(text='Exit')
        butt3.bind(on_press=callback)

        # Container Widget
        layout = BoxLayout(padding=50)
        wid = Widget()
        #        layout.add_widget(wid)
        wid.add_widget(butt1)
        wid.add_widget(butt2)
        wid.add_widget(butt3)
        wid.add_widget(lab)

        #        lab.y = 100
        #        lab.x = 0
        #        lab.width = 500
        #        butt2.x = 200
        #        butt3.x = 300
        layout.add_widget(camera)
        camera.resolution = (640, 480)
        #        camera.size=(320,200)
        camera.play = True

        return layout


if __name__ == '__main__':
    # run
    MyApp().run()
