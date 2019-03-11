import tcod as libt

from game_messages import Message
from game_states import GameStates
from render_functions import RenderOrder



def kill_player(player):
    player.char = '%'
    player.color = libt.dark_red

    return Message('You died!', libt.red), GameStates.PLAYER_DEAD

def kill_monster(monster):
    death_message = Message('{0} is dead!'.format(monster.name.capitalize()), libt.orange)

    monster.char = '%'
    monster.color = libt.dark_red
    monster.blocks = False
    monster.fighter = None
    monster.ai = None
    monster.name = 'remains of ' + monster.name
    monster.render_order = RenderOrder.CORPSE

    return death_message

