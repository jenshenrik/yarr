from __future__ import annotations

from typing import Optional, TYPE_CHECKING

import tcod

from actions import Action, BumpAction, EscapeAction, MovementAction

from game_states import GameStates

if TYPE_CHECKING:
    from engine2 import Engine


class EventHandler(tcod.event.EventDispatch[Action]):
    def __init__(self, engine: Engine):
        self.engine = engine

    def handle_events(self) -> None:
        for event in tcod.event.wait():
            action = self.dispatch(event)

            if action is None:
                continue

            action.perform()
            self.engine.handle_enemy_turns()
            self.engine.update_fov()

    def ev_quit(self, event: tcod.event.Quit) -> Optional[Action]:
        raise SystemExit()

    def ev_keydown(self, event: tcod.event.KeyDown) -> Optional[Action]:
        action: Optional[Action] = None

        key = event.sym
        player = self.engine.player

        if key == tcod.event.K_UP:
            action = BumpAction(player, dx=0, dy=-1)
        elif key == tcod.event.K_DOWN:
            action = BumpAction(player, dx=0, dy=1)
        elif key == tcod.event.K_LEFT:
            action = BumpAction(player, dx=-1, dy=0)
        elif key == tcod.event.K_RIGHT:
            action = BumpAction(player, dx=1, dy=0)

        elif key == tcod.event.K_ESCAPE:
            action = EscapeAction(player)

        return action


def handle_keys(key, game_state):
    if game_state == GameStates.PLAYERS_TURN:
        return handle_player_turn_keys(key)
    elif game_state == GameStates.PLAYER_DEAD:
        return handle_player_dead_keys(key)
    elif game_state == GameStates.TARGETING:
        return handle_targeting_keys(key)
    elif game_state in (GameStates.SHOW_INVENTORY, GameStates.DROP_INVENTORY):
        return handle_inventory_keys(key)
    elif game_state == GameStates.LEVEL_UP:
        return handle_level_up_menu(key)
    elif game_state == GameStates.CHARACTER_SCREEN:
        return handle_character_screen(key)

    return {}


def handle_main_menu(key):
    key_char = chr(key.c)

    if key_char == "a":
        return {"new_game": True}
    elif key_char == "b":
        return {"load_game": True}
    elif key_char == "c" or key.vk == tcod.KEY_ESCAPE:
        return {"exit": True}
    elif key.vk == tcod.KEY_ENTER and key.lalt:
        # Alt+Enter: toggle full screen
        return {"fullscreen": True}

    return {}


def handle_level_up_menu(key):
    if key:
        key_char = chr(key.c)

        if key_char == "a":
            return {"level_up": "hp"}
        elif key_char == "b":
            return {"level_up": "str"}
        elif key_char == "c":
            return {"level_up": "def"}
    return {}


def handle_character_screen(key):
    if key.vk == tcod.KEY_ESCAPE:
        return {"exit": True}

    return {}


def handle_targeting_keys(key):
    if key.vk == tcod.KEY_ESCAPE:
        return {"exit": True}

    return {}


def handle_mouse(mouse):
    (x, y) = (mouse.cx, mouse.cy)

    if mouse.lbutton_pressed:
        return {"left_click": (x, y)}
    elif mouse.rbutton_pressed:
        return {"right_click": (x, y)}

    return {}


def handle_inventory_keys(key):
    index = key.c - ord("a")

    if index >= 0:
        return {"inventory_index": index}

    if key.vk == tcod.KEY_ENTER and key.lalt:
        # Alt+Enter: toggle full screen
        return {"fullscreen": True}
    elif key.vk == tcod.KEY_ESCAPE:
        # Exit the menu
        return {"exit": True}

    return {}


def handle_player_dead_keys(key):
    key_char = chr(key.c)

    if key_char == "i":
        return {"show_inventory": True}

    if key.vk == tcod.KEY_ENTER and key.lalt:
        # Alt+Enter: toggle full screen
        return {"fullscreen": True}
    elif key.vk == tcod.KEY_ESCAPE:
        # Exit the menu
        return {"exit": True}

    return {}


def handle_player_turn_keys(key):
    key_char = chr(key.c)

    # Movement keys
    if key.vk == tcod.KEY_UP or key_char == "k":
        return {"move": (0, -1)}
    elif key.vk == tcod.KEY_DOWN or key_char == "j":
        return {"move": (0, 1)}
    elif key.vk == tcod.KEY_LEFT or key_char == "h":
        return {"move": (-1, 0)}
    elif key.vk == tcod.KEY_RIGHT or key_char == "l":
        return {"move": (1, 0)}
    elif key_char == "y":
        return {"move": (-1, -1)}
    elif key_char == "u":
        return {"move": (1, -1)}
    elif key_char == "b":
        return {"move": (-1, 1)}
    elif key_char == "n":
        return {"move": (1, 1)}
    elif key_char == "z":
        return {"wait": True}
    elif key.vk == tcod.KEY_ENTER:
        return {"take_stairs": True}
    elif key_char == "c":
        return {"show_character_screen": True}
    elif key_char == "g":
        return {"pickup": True}
    elif key_char == "i":
        return {"show_inventory": True}
    elif key_char == "d":
        return {"drop_inventory": True}

    if key.vk == tcod.KEY_ENTER and key.lalt:
        return {"fullscreen": True}

    if key.vk == tcod.KEY_ESCAPE:
        return {"exit": True}

    return {}
