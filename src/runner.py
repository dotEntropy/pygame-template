import pygame 
import sys
import os
import pathlib
import importlib
from pygame.event import Event
from src.variables import GameVars
from src.states.parent import State
from utils.colored_print import print_error


class StateRunner:
    def __init__(self) -> None:
        self._load_states()
        self._load_default_state()
    
    def _load_states(self) -> None:
        STATE_DIR = pathlib.Path(__file__).parent / 'states'
        for state in os.listdir(STATE_DIR):
            self._load_state(state)
    
    def _load_state(self, state: str) -> None:
        if not state.endswith('.py') or state == 'parent.py':
            return
        try:
            state = state.removesuffix('.py')
            module = importlib.import_module(f'src.states.{state}')
            setup_func = getattr(module, 'setup', None)
            if callable(setup_func):
                setup_func()
            else:
                print_error(f'State "{state}" must have a setup function!')
        except ImportError as e:
            print_error(f'State "{state}" setup failed: {e}')

    def _load_default_state(self) -> None:
        GameVars.active_state = GameVars.states.get('default')
        if GameVars.active_state is None:
            print_error('There is no "default" state!\nTerminating...')
            exit()

    def run(self, dt: float) -> None:
        self.active_state: State = GameVars.active_state
        self.active_state.update(dt)
        self.active_state.draw()
        self._handle_events()

    def _handle_events(self) -> None:
        for event in pygame.event.get():
            self._quit_event(event)
            self._key_down_events(event)
            self._mouse_events(event)
        
        keys = pygame.key.get_pressed()
        self.active_state.handle_key_held(keys)

        mouse_buttons = pygame.mouse.get_pressed()
        self.active_state.handle_mouse_held(mouse_buttons)
    
    def _key_down_events(self, event: Event) -> None:
        if event.type == pygame.KEYDOWN:
            self.active_state.handle_key_tap(event.key)
    
    def _mouse_events(self, event: Event) -> None:
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.active_state.handle_mouse_tap(event.button)
    
    @staticmethod
    def _quit_event(event: Event) -> None:
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type != pygame.KEYDOWN: 
            return
        if event.key == pygame.K_ESCAPE:
            pygame.quit()
            sys.exit()
