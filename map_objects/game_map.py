import tcod
from random import randint

from map_objects.tile import Tile
from map_objects.rectangle import Rect
from entity import Entity

class GameMap:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.tiles = self.initialize_tiles()

    def initialize_tiles(self):
        tiles = [[Tile(True) for y in range(self.height)] for x in range(self.width)]

        return tiles

    def is_blocked(self, x, y):
        if self.tiles[x][y].blocked:
            return True
        return False

    def create_room(self, room):
        for x in range(room.x1 + 1, room.x2):
            for y in range(room.y1 + 1, room.y2):
                self.tiles[x][y].blocked = False
                self.tiles[x][y].block_sight = False

    def make_map(self, max_rooms, room_min_size, room_max_size, map_width, map_height,
            player, entities, max_monsters_per_room):
        rooms = []
        num_rooms = 0

        for r in range(max_rooms):
            # Random height and width of room
            w = randint(room_min_size, room_max_size)
            h = randint(room_min_size, room_max_size)
            # Random position within boundaries
            x = randint(0, map_width - w - 1)
            y = randint(0, map_height - h - 1)

            new_room = Rect(x, y, w, h)
            for other_room in rooms:
                if new_room.intersects(other_room):
                    print("Intersection detected")
                    break
            else:
                self.create_room(new_room)
                (new_x, new_y) = new_room.center()
                print("new room created")
                if len(rooms) == 0:
                    # Start player in the first room
                    player.x = new_x
                    player.y = new_y
                    print("player starting position set")
                else:
                    # All rooms after the first:
                    # connect it to the prev one with a tunnel

                    # Center coords of prev room
                    (prev_x, prev_y) = rooms[num_rooms - 1].center()

                    # Flip a coin whether to go vert or hor first
                    if randint(0, 1) == 1:
                        self.create_h_tunnel(prev_x, new_x, prev_y)
                        self.create_v_tunnel(new_x, prev_y, new_y)
                    else:
                        self.create_v_tunnel(prev_x, prev_y, new_y)
                        self.create_h_tunnel(prev_x, new_x, new_y)

                # Append the new room to the list of rooms
                rooms.append(new_room)
                self.place_entities(new_room, entities, max_monsters_per_room)

                num_rooms += 1

    def create_h_tunnel(self, x1, x2, y):
        for x in range(min(x1, x2), max(x1, x2) +1):
            self.tiles[x][y].blocked = False
            self.tiles[x][y].block_sight= False

    def create_v_tunnel(self, x, y1, y2):
        for y in range(min(y1, y2), max(y1, y2) + 1):
            self.tiles[x][y].blocked = False
            self.tiles[x][y].block_sight= False
            
    def place_entities(self, room, entities, max_monsters_per_room):
        # Get a random number of monsters
        number_of_monsters = randint(0, max_monsters_per_room)

        for i in range(number_of_monsters):
            # Choose a random location in the room
            x = randint(room.x1 + 1, room.x2 - 1)
            y = randint(room.y1 + 1, room.y2 - 1)

            if not any([entity for entity in entities if entity.x == x and entity.y == y]):
                if randint(0, 100) < 80:
                    monster = Entity(x, y, 'o', tcod.desaturated_green)
                else:
                    monster = Entity(x, y, 'T', tcod.darker_green)

                entities.append(monster)
