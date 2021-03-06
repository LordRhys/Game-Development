import random
from map_objects.rectangle import Rect

class Leaf: # used for the BSP tree algorithm
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.MIN_LEAF_SIZE = 10
        self.child_1 = None
        self.child_2 = None
        self.room = None
        self.hall = None

    def splitLeaf(self):
        # begin splitting the leaf into two children
        if (self.child_1 != None) or (self.child_2 != None):
            return False # This leaf has already been split

        '''
        ==== Determine the direction of the split ====
        If the width of the leaf is >25% larger than the height,
        split the leaf vertically.
        If the height of the leaf is >25 larger than the width,
        split the leaf horizontally.
        Otherwise, choose the direction at random.
        '''
        splitHorizontally = random.choice([True, False])
        if (self.width/self.height >= 1.25):
            splitHorizontally = False
        elif (self.height/self.width >= 1.25):
            splitHorizontally = True

        if (splitHorizontally):
            max = self.height - self.MIN_LEAF_SIZE
        else:
            max = self.width - self.MIN_LEAF_SIZE

        if (max <= self.MIN_LEAF_SIZE):
            return False # the leaf is too small to split further

        split = random.randint(self.MIN_LEAF_SIZE,max) #determine where to split the leaf

        if (splitHorizontally):
            self.child_1 = Leaf(self.x, self.y, self.width, split)
            self.child_2 = Leaf( self.x, self.y+split, self.width, self.height-split)
        else:
            self.child_1 = Leaf( self.x, self.y,split, self.height)

            self.child_2 = Leaf( self.x + split, self.y, self.width-split, self.height)

        return True

    #def createRooms(self, bspTree, entities, max_monsters_per_room, max_items_per_room):
    #    if (self.child_1) or (self.child_2):
    #        # recursively search for children until you hit the end of the branch
    #        if (self.child_1):
    #            self.child_1.createRooms(bspTree, entities, max_monsters_per_room, max_items_per_room)
    #        if (self.child_2):
    #            self.child_2.createRooms(bspTree, entities, max_monsters_per_room, max_items_per_room)

    #        if (self.child_1 and self.child_2):
    #            bspTree.createHall(self.child_1.getRoom(),
    #                self.child_2.getRoom())

    #    else:
    #    # Create rooms in the end branches of the bsp tree
    #        w = random.randint(bspTree.ROOM_MIN_SIZE, min(bspTree.ROOM_MAX_SIZE,self.width-1))
    #        h = random.randint(bspTree.ROOM_MIN_SIZE, min(bspTree.ROOM_MAX_SIZE,self.height-1))
    #        x = random.randint(self.x, self.x+(self.width-1)-w)
    #        y = random.randint(self.y, self.y+(self.height-1)-h)
    #        self.room = Rect(x,y,w,h)
    #        bspTree.createRoom(self.room)

    #        # append the new room to the list
    #        bspTree.rooms.append(new_room)
    #        if bspTree.num_rooms == 0:
    #            # center coordinates of the new room, useful later
    #            (new_x, new_y) = new_room.center()
    #            player.x = new_x
    #            player.y = new_y

    #        bspTree.place_entities(new_room, entities, max_monsters_per_room, max_items_per_room)

    #        bspTree.num_rooms += 1

    #def getRoom(self):
    #    if (self.room): return self.room

    #    else:
    #        if (self.child_1):
    #            self.room_1 = self.child_1.getRoom()
    #        if (self.child_2):
    #            self.room_2 = self.child_2.getRoom()

    #        if (not self.child_1 and not self.child_2):
    #            # neither room_1 nor room_2
    #            return None

    #        elif (not self.room_2):
    #            # room_1 and !room_2
    #            return self.room_1

    #        elif (not self.room_1):
    #            # room_2 and !room_1
    #            return self.room_2

    #        # If both room_1 and room_2 exist, pick one
    #        elif (random.random() < 0.5):
    #            return self.room_1
    #        else:
    #            return self.room_2
