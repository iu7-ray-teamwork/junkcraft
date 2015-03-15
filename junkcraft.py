# coding=UTF-8

from engine import *


class MyApplication(Application):
    pass

class MyWindow(Window):
    def on_key_press(self, key):
        print('key_press {}'.format(key))

    def on_key_release(self, key):
        print('key_release {}'.format(key))


if __name__ == '__main__':
    with MyApplication() as application:
        window = MyWindow(application, title='JunkCraft', size=(800, 600))
        application.run_event_loop()






