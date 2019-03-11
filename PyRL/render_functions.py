
import tcod as libt

from enum import Enum

from game_states import GameStates
from menus import inventory_menu

class RenderOrder(Enum):
    CORPSE = 1
    ITEM = 2
    ACTOR = 3

def get_names_under_mouse(mouse, entities, fov_map):
    (x, y) = (mouse.cx, mouse.cy)

    names = [entity.name for entity in entities
             if entity.x == x and entity.y == y and
             libt.map_is_in_fov(fov_map, entity.x, entity.y)]
    names = ', '.join(names)

    return names.capitalize()

def render_bar(panel, x, y, total_width, name, value, maximum, bar_color, back_color):
    bar_width = int(float(value) / maximum * total_width)

    libt.console_set_default_background(panel, back_color)
    libt.console_rect(panel, x, y, total_width, 1, False, libt.BKGND_SCREEN)

    libt.console_set_default_background(panel, bar_color)
    if bar_width > 0:
        libt.console_rect(panel, x, y, bar_width, 1, False, libt.BKGND_SCREEN)

    libt.console_set_default_foreground(panel, libt.white)
    libt.console_print_ex(panel, int(x + total_width / 2), y, libt.BKGND_NONE, libt.CENTER,
                          '{0}: {1}/{2}'.format(name, value, maximum))

def render_all(con, panel, entities, player, game_map, fov_map, fov_recompute, 
               message_log, screen_width, screen_height, bar_width, panel_height,
               panel_y, mouse, colors, game_state):
    if fov_recompute:
        # draw all the tiles in the game map
        for y in range(game_map.height):
            for x in range(game_map.width):
                visible = libt.map_is_in_fov(fov_map, x, y)
                wall = game_map.tiles[x][y].block_sight

                if visible:
                    if wall:
                        libt.console_set_char_background(con, x, y, colors.get('light_wall'),
                                                         libt.BKGND_SET)
                    else:
                        libt.console_set_char_background(con, x, y, colors.get('light_ground'),
                                                         libt.BKGND_SET)

                    game_map.tiles[x][y].explored = True

                elif game_map.tiles[x][y].explored:
                    if wall:
                        libt.console_set_char_background(con, x, y, colors.get('dark_wall'),
                                                         libt.BKGND_SET)
                    else:
                        libt.console_set_char_background(con, x, y, colors.get('dark_ground'),
                                                         libt.BKGND_SET)

    entities_in_render_order = sorted(entities, key=lambda x: x.render_order.value)

    # Draw all entities in the list
    for entity in entities_in_render_order:
        draw_entity(con, entity, fov_map)

    libt.console_blit(con, 0, 0, screen_width, screen_height, 0, 0, 0)

    libt.console_set_default_background(panel, libt.black)
    libt.console_clear(panel)

    # Print the game messages, one line at a time
    y = 1
    for message in message_log.messages:
        libt.console_set_default_foreground(panel, message.color)
        libt.console_print_ex(panel, message_log.x, y, libt.BKGND_NONE, libt.LEFT, message.text)
        y += 1

    render_bar(panel, 1, 1, bar_width, 'HP', player.fighter.hp, player.fighter.max_hp,
               libt.light_red, libt.darker_red)

    libt.console_set_default_foreground(panel, libt.light_grey)
    libt.console_print_ex(panel, 1, 0, libt.BKGND_NONE, libt.LEFT, 
                          get_names_under_mouse(mouse, entities, fov_map))

    libt.console_blit(panel, 0, 0, screen_width, panel_height, 0, 0, panel_y)

    if game_state in (GameStates.SHOW_INVENTORY, GameStates.DROP_INVENTORY):
        if game_state == GameStates.SHOW_INVENTORY:
            inventory_title = 'Press the key next to an item to use it, or Esc to cancel.\n'
        else:
            inventory_title = 'Press the key next to an item to drop it, or Esc to cancel.\n'

        inventory_menu(con, inventory_title, player.inventory, 50, screen_width, screen_height)


def clear_all(con, entities):
    for entity in entities:
        clear_entity(con, entity)

def draw_entity(con, entity, fov_map):
    if libt.map_is_in_fov(fov_map, entity.x, entity.y):
        libt.console_set_default_foreground(con, entity.color)
        libt.console_put_char(con, entity.x, entity.y, entity.char, libt.BKGND_NONE)

def clear_entity(con, entity):
    # erase the character that represents this object
    libt.console_put_char(con, entity.x, entity.y, ' ', libt.BKGND_NONE)

