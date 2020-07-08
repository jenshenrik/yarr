import tcod
from game_states import GameStates
from render_functions import RenderOrder
from game_messages import Message

def kill_player(player):
    player.char = '%'
    player.colour = tcod.dark_red
    player.render_order = RenderOrder.CORPSE

    return Message('You died!', tcod.red), GameStates.PLAYER_DEAD

def kill_monster(monster):
    death_message = '{0} is dead!'.format(monster.name.capitalize())
    monster.char = '%'
    monster.colour = tcod.dark_red
    monster.blocks = False
    monster.render_order = RenderOrder.CORPSE
    monster.fighter = None
    monster.ai = None
    monster.name = 'remains of ' + monster.name

    return Message(death_message, tcod.orange)
