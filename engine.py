import sys
import os
import os.path
from ctypes import *

if sys.platform.startswith('win32'):
    # assume SDL2.dll is distributed alongside
    os.environ['PYSDL2_DLL_PATH'] = os.path.dirname(__file__)

from sdl2 import *


class Application:
    def __init__(self):
        self._windows = {}

    def __enter__(self):
        SDL_Init(SDL_INIT_EVERYTHING)
        return self

    def __exit__(self, type, value, traceback):
        SDL_Quit()

    def process_events(self):
        e = SDL_Event()
        while SDL_PollEvent(byref(e)):
            if e.type == SDL_QUIT:
                self.on_user_quit()
            elif e.type == SDL_KEYDOWN:
                if e.key.windowID in self._windows:
                    self._windows[e.key.windowID].on_key_press(str(SDL_GetKeyName(e.key.keysym.sym), 'UTF-8'))
            elif e.type == SDL_KEYUP:
                if e.key.windowID in self._windows:
                    self._windows[e.key.windowID].on_key_release(str(SDL_GetKeyName(e.key.keysym.sym), 'UTF-8'))

    def run_event_loop(self):
        while True:
            self.process_events()

    def on_user_quit(self):
        sys.exit()


class Window:
    def __init__(self, application, **parameters):
        self._application = application

        self._window = SDL_CreateWindow(
            b'',
            SDL_WINDOWPOS_UNDEFINED, SDL_WINDOWPOS_UNDEFINED,
            0, 0,
            SDL_WINDOW_RESIZABLE
        )

        self._application._windows[SDL_GetWindowID(self._window)] = self

        self.title = parameters.pop('title', '')
        self.size = parameters.pop('size', (800, 600))

    @property
    def context(self):
        return self._application

    @property
    def title(self):
        return str(SDL_GetWindowTitle(self._window), 'UTF-8')

    @title.setter
    def title(self, title):
        SDL_SetWindowTitle(self._window, title.encode('UTF-8'))

    @property
    def size(self):
        w, h = c_int(), c_int()
        SDL_GetWindowSize(self._window, byref(w), byref(h))
        return w.value, h.value

    @size.setter
    def size(self, size):
        w, h = size
        SDL_SetWindowSize(self._window, w, h)

    def on_key_press(self, key):
        pass

    def on_key_release(self, key):
        pass
