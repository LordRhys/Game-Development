
import tcod as libt
import random

from components.ai import BasicMonster
from components.fighter import Fighter
from components.item import Item

from entity import Entity
from components.stairs import Stairs
from game_messages import Message
from item_functions import heal, cast_lightning, cast_fireball, cast_confuse
from render_functions import RenderOrder
from map_objects.rectangle import Rect
from map_objects.tile import Tile
from random_utils import random_choice_from_dict
from map_objects.leaf import Leaf


# ==== BSP Tree ====
class BSPTree:

    def __init__(self, width, height, dungeon_level):
        self.width = width
        self.height = height
        self.tiles = self.initialize_tiles()
        self.dungeon_level = dungeon_level

        self.room = None
        self.MAX_LEAF_SIZE = 24
        self.ROOM_MAX_SIZE = 15
        self.ROOM_MIN_SIZE = 6

    def initialize_tiles(self):
        """
        initialze map tiles
        """
        tiles = [[Tile(True) for y in range(self.height)]
                 for x in range(self.width)]        

        return tiles

    def make_map(self, max_rooms, room_min_size, room_max_size, map_width, map_height, player, entities, max_monsters_per_room, max_items_per_room):
        
        self._leafs = []

        rooms = []
        num_rooms = 0

        rootLeaf = Leaf(0,0,map_width,map_height)
        self._leafs.append(rootLeaf)

        splitSuccessfully = True
        # loop through all leaves until they can no longer split successfully
        while (splitSuccessfully):
            splitSuccessfully = False
            for l in self._leafs:
                if (l.child_1 == None) and (l.child_2 == None):
                    if ((l.width > self.MAX_LEAF_SIZE) or 
                        (l.height > self.MAX_LEAF_SIZE) or
                        (random.random() > 0.8)):
                            if (l.splitLeaf()): #try to split the leaf
                                self._leafs.append(l.child_1)
                                self._leafs.append(l.child_2)
                                splitSuccessfully = True

        create_rooms(rootLeaf)

    def place_entities(self, room, entities, max_monters_per_room, max_items_per_room):
        # Get a random number of monsters
        number_of_monsters = randint(0, max_monters_per_room)
        number_of_items = randint(0, max_items_per_room)

        monster_chances = {'orc': 80, 'troll': 20}
        item_chances = {'healing_potion': 70, 'lightning_scroll': 10, 'fireball_scroll': 10,
                        'confusion_scroll': 10}

        for i in range(number_of_monsters):
            # choose a random location in the room
            x = randint(room.x1 + 1, room.x2 - 1)
            y = randint(room.y1 + 1, room.y2 - 1)

            if not any([entity for entity in entities if entity.x == x and
                       entity.y == y]):
                monster_choice = random_choice_from_dict(monster_chances)

                if monster_choice == 'orc':
                    treasure_drop = randint(1,20)
                    fighter_component = Fighter(hp=10, defense=0, power=3, xp=35, coins=treasure_drop)
                    ai_component = BasicMonster()
                    monster = Entity(x, y, 'o', libt.desaturated_green, 'Orc', blocks=True, render_order=RenderOrder.ACTOR, 
                                     fighter=fighter_component, ai=ai_component)
                else:
                    treasure_drop = randint(1,50)
                    fighter_component = Fighter(hp=16, defense=1, power=4, xp=100, coins=treasure_drop)
                    ai_component = BasicMonster()
                    monster = Entity(x, y, 'T', libt.darker_green, 'Troll', blocks=True, render_order=RenderOrder.ACTOR, 
                                     fighter=fighter_component, ai=ai_component)

                entities.append(monster)

        for i in range(number_of_items):
            # choose a random location in the room
            x = randint(room.x1 + 1, room.x2 - 1)
            y = randint(room.y1 + 1, room.y2 - 1)

            if not any([entity for entity in entities if entity.x == x and
                       entity.y == y]):
                item_choice = random_choice_from_dict(item_chances)

                if item_choice == 'healing_potion':
                    item_component = Item(use_function=heal, amount=4)
                    item = Entity(x, y, '!', libt.violet, 'Healing Potion', render_order=RenderOrder.ITEM, 
                                  item=item_component)
                elif item_choice == 'fireball_scroll':
                    item_component = Item(use_function=cast_fireball, targeting=True, targeting_message=Message(
                        'Left-click a target tile for the fireball, or right-click to cancel.', libt.light_cyan),
                                         damage=12, radius=3)
                    item = Entity(x, y, '#', libt.red, 'Fireball Scroll', render_order=RenderOrder.ITEM, 
                                  item=item_component)
                elif item_choice == 'confusion_scroll':
                    item_component = Item(use_function=cast_confuse, targeting=True, targeting_message=Message(
                        'Left-click an enemy to confuse it, or right-click to cancel.', libt.light_cyan))
                    item = Entity(x, y, '#', libt.light_pink, 'Confusion Scroll', render_order=RenderOrder.ITEM, 
                                  item=item_component)
                else:
                    item_component = Item(use_function=cast_lightning, damage=20, maximum_range=5)
                    item = Entity(x, y, '#', libt.yellow, 'Lightning Scroll', render_order=RenderOrder.ITEM, 
                                  item=item_component)
                
                entities.append(item)

    def createRoom(self, room):
        # set all tiles within a rectangle to 0
        for x in range(room.x1 + 1, room.x2):
            for y in range(room.y1+1, room.y2):
                self.tiles[x][y].blocked = False
                self.tiles[x][y].block_sight = False

    def create_rooms(self):
        if (self.child_1) or (self.child_2):
            # recursively search for children until you hit the end of the branch
            if (self.child_1):
                create_rooms(self.child_1)
            if (self.child_2):
                create_rooms(self.child_2)

            if (self.child_1 and self.child_2):
                createHall(getRoom(self.child_1),
                           getRoom(self.child_2))

        else:
        # Create rooms in the end branches of the bsp tree
            w = random.randint(bspTree.ROOM_MIN_SIZE, min(bspTree.ROOM_MAX_SIZE,self.width-1))
            h = random.randint(bspTree.ROOM_MIN_SIZE, min(bspTree.ROOM_MAX_SIZE,self.height-1))
            x = random.randint(self.x, self.x+(self.width-1)-w)
            y = random.randint(self.y, self.y+(self.height-1)-h)
            self.room = Rect(x,y,w,h)
            createRoom(self.room)

            # append the new room to the list
            rooms.append(new_room)
            if num_rooms == 0:
                # center coordinates of the new room, useful later
                (new_x, new_y) = new_room.center()
                player.x = new_x
                player.y = new_y

            place_entities(new_room, entities, max_monsters_per_room, max_items_per_room)

            num_rooms += 1

    def getRoom(self):
        if (self.room): return self.room

        else:
            if (self.child_1):
                self.room_1 = getRoom(self.child_1)
            if (self.child_2):
                self.room_2 = getRoom(self.child_2)

            if (not self.child_1 and not self.child_2):
                # neither room_1 nor room_2
                return None

            elif (not self.room_2):
                # room_1 and !room_2
                return self.room_1

            elif (not self.room_1):
                # room_2 and !room_1
                return self.room_2

            # If both room_1 and room_2 exist, pick one
            elif (random.random() < 0.5):
                return self.room_1
            else:
                return self.room_2

    def createHall(self, room1, room2):
        # connect two rooms by hallways
        x1, y1 = room1.center()
        x2, y2 = room2.center()
        # 50% chance that a tunnel will start horizontally
        if random.randint(0,1) == 1:
            self.createHorTunnel(x1, x2, y1)
            self.createVirTunnel(y1, y2, x2)

        else: # else it starts virtically
            self.createVirTunnel(y1, y2, x1)
            self.createHorTunnel(x1, x2, y2)

    def createHorTunnel(self, x1, x2, y):
        for x in range(min(x1,x2),max(x1,x2)+1):
            self.tiles[x][y].blocked = False
            self.tiles[x][y].block_sight = False

    def createVirTunnel(self, y1, y2, x):
        for y in range(min(y1,y2),max(y1,y2)+1):
            self.tiles[x][y].blocked = False
            self.tiles[x][y].block_sight = False

