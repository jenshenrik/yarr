import tcod
from random import randint

from map_objects.tile import Tile
from map_objects.rectangle import Rect
from entity import Entity
from game_messages import Message
from item_functions import heal, cast_lightning, cast_fireball, cast_confuse
from render_functions import RenderOrder
from components.ai import BasicMonster
from components.fighter import Fighter
from components.item import Item
from components.stairs import Stairs

class GameMap:
    def __init__(self, width, height, dungeon_level=1):
        self.width = width
        self.height = height
        self.tiles = self.initialize_tiles()
        self.dungeon_level = dungeon_level

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
            player, entities, max_monsters_per_room, max_items_per_room):
        rooms = []
        num_rooms = 0

        center_of_last_room_x = None
        center_of_last_room_y = None

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
                    break
            else:
                self.create_room(new_room)
                (new_x, new_y) = new_room.center()
                center_of_last_room_x = new_x
                center_of_last_room_y = new_y

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
                self.place_entities(new_room, entities, max_monsters_per_room, max_items_per_room)

                num_rooms += 1

        stairs_component = Stairs(self.dungeon_level + 1)
        down_stairs = Entity(center_of_last_room_x, center_of_last_room_y, '>',
                tcod.white, 'Stairs', render_order=RenderOrder.STAIRS, 
                stairs=stairs_component)
        entities.append(down_stairs)

    def create_h_tunnel(self, x1, x2, y):
        for x in range(min(x1, x2), max(x1, x2) +1):
            self.tiles[x][y].blocked = False
            self.tiles[x][y].block_sight= False

    def create_v_tunnel(self, x, y1, y2):
        for y in range(min(y1, y2), max(y1, y2) + 1):
            self.tiles[x][y].blocked = False
            self.tiles[x][y].block_sight= False
            
    def place_entities(self, room, entities, max_monsters_per_room, max_items_per_room):
        # Get a random number of monsters and items
        number_of_monsters = randint(0, max_monsters_per_room)
        number_of_items = randint(0, max_items_per_room)

        for i in range(number_of_monsters):
            # Choose a random location in the room
            x = randint(room.x1 + 1, room.x2 - 1)
            y = randint(room.y1 + 1, room.y2 - 1)

            if not any([entity for entity in entities if entity.x == x and entity.y == y]):
                if randint(0, 100) < 80:
                    fighter_component = Fighter(hp=10, defense=0, power=3)
                    ai_component = BasicMonster()
                    monster = Entity(x, y, 'o', tcod.desaturated_green, 'Orc', blocks=True, 
                            render_order=RenderOrder.ACTOR, fighter=fighter_component, 
                            ai=ai_component)
                else:
                    fighter_component = Fighter(hp=16, defense=1, power=4)
                    ai_component = BasicMonster()
                    monster = Entity(x, y, 'T', tcod.darker_green, 'Troll', blocks=True, 
                            render_order=RenderOrder.ACTOR, fighter=fighter_component, 
                            ai=ai_component)

                entities.append(monster)

        for i in range(number_of_items):
            x = randint(room.x1 + 1, room.x2 - 1)
            y = randint(room.y1 + 1, room.y2 - 1)

            if not any([entity for entity in entities if entity.x == x and entity.y == y]):
                item_chance = randint(0, 100)

                if item_chance < 70:
                    item_component = Item(use_function=heal, amount=4)
                    item = Entity(x, y, '!', tcod.violet, 'Healing Potion', render_order=RenderOrder.ITEM, item=item_component)
                elif item_chance < 80:
                    item_component = Item(use_function=cast_fireball, targeting=True, targeting_message=Message(
                        'Left-click a target til for the fireball, or right-click to cancel.', tcod.light_cyan),
                        damage=12, radius=3)
                    item = Entity(x, y, '#', tcod.red, 'Fireball Scroll', render_order=RenderOrder.ITEM,
                            item=item_component)
                elif item_chance < 90:
                    item_component = Item(use_function=cast_confuse, targeting=True, targeting_message=Message(
                        'Left-click an enemy to confuse it. or right-click to cancel.', tcod.light_cyan))
                    item = Entity(x, y, '#', tcod.light_pink, 'Confusion Scroll', render_order=RenderOrder.ITEM,
                            item=item_component)
                else:
                    item_component = Item(use_function=cast_lightning, damage=20, maximum_range=5)
                    item = Entity(x, y, '#', tcod.yellow, 'Lightning Scroll', render_order=RenderOrder.ITEM,
                            item=item_component)
                entities.append(item)

    def next_floor(self, player, message_log, constants):
        self.dungeon_level += 1
        entities = [player]

        self.tiles = self.initialize_tiles()
        self.make_map(constants['max_rooms'], constants['room_min_size'], 
                constants['room_max_size'], constants['map_width'], 
                constants['map_height'], player, entities,
                constants['max_monsters_per_room'], constants['max_items_per_room'])

        player.fighter.heal(player.fighter.max_hp // 2)
        message_log.add_message(Message('You take a moment to rest, and recover your strength', tcod.light_violet))

        return entities
