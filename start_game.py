import arcade
import arcade.gui
import easygui
import os
import time
import random
import sqlite3
import json
import openai

PATH_BASE = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(PATH_BASE,'data')
IMG_PATH = os.path.join(DATA_PATH,'img')
DB_PATH = os.path.join(DATA_PATH,'db')
WORLDS_BACKGROUNDS_LOCATION = os.path.join(IMG_PATH,'backgrounds')
EFFECTS_BACKGROUNDS_LOCATION = os.path.join(WORLDS_BACKGROUNDS_LOCATION,'effects')
SPRITES_LOCATION = os.path.join(IMG_PATH,'sprites')

SCREEN_WIDTH = 1300
SCREEN_HEIGHT = 1000
SCREEN_TITLE = "Voyage au centre de la galaxie"
ITEMS_DB_FILE_PATH=os.path.join(DB_PATH,'items.db')
MALUS_DB_FILE_PATH=os.path.join(DB_PATH,'malus.db')

SIDEBAR_WIDTH = SCREEN_WIDTH * 0.3
MAP_WIDTH = SCREEN_WIDTH - SIDEBAR_WIDTH
BOTTOM_BAR_HEIGHT = 150  # Set the height of the bottom bar

SPRITE_OFFSET_X = 15
SPRITE_OFFSET_Y = 5

COLUMNS_IN_A_WORLD = 5

WORLD_1_NUMBER_OF_LOCATIONS = 30
WORLD_1_NUMBER_OF_ROWS = int(WORLD_1_NUMBER_OF_LOCATIONS / COLUMNS_IN_A_WORLD)

WORLD_2_NUMBER_OF_LOCATIONS = 40
WORLD_2_NUMBER_OF_ROWS = int(WORLD_2_NUMBER_OF_LOCATIONS / COLUMNS_IN_A_WORLD)

WORLD_3_NUMBER_OF_LOCATIONS = 50
WORLD_3_NUMBER_OF_ROWS = int(WORLD_3_NUMBER_OF_LOCATIONS / COLUMNS_IN_A_WORLD)

WORLD_1_MALUS_LOCATIONS = [3,4,7,15,19,23,24,27]
WORLD_1_MERCHANT_LOCATIONS = [10,20,29]
WORLD_1_QUESTION_LOCATIONS = [2,5,11,12,13,16,18,21,25,26]
WORLD_1_NEUTRAL_LOCATIONS = [1,6,17]
WORLD_1_HAZARD_LOCATIONS = [8,14,28,30]
WORLD_1_TURBO_LOCATIONS = [9,22]

WORLD_2_MALUS_LOCATIONS = [3,8,11,14,17,23,24,27,32,35]
WORLD_2_MERCHANT_LOCATIONS = [10,20,30,39]
WORLD_2_QUESTION_LOCATIONS = [2,4,5,6,9,12,15,18,19,22,26,29,33,36,38]
WORLD_2_NEUTRAL_LOCATIONS = [1,21,31,37]
WORLD_2_HAZARD_LOCATIONS = [7,16,25,34]
WORLD_2_TURBO_LOCATIONS = [13,28,40]

WORLD_3_MALUS_LOCATIONS = [3,4,7,11,14,19,21,24,32,38,41,43,44,45,47,49]
WORLD_3_MERCHANT_LOCATIONS = [10,20,30,40]
WORLD_3_QUESTION_LOCATIONS = [5,6,8,9,12,13,16,18,20,22,26,28,30,33,34,35,37]
WORLD_3_NEUTRAL_LOCATIONS = [1,23,29,36,50]
WORLD_3_HAZARD_LOCATIONS = [2,17,27,39,46,48]
WORLD_3_TURBO_LOCATIONS = [16,31,42]

MALUS_LOCATION_COLOR = arcade.color.RED
MERCHANT_LOCATION_COLOR = arcade.color.BLUE
QUESTION_LOCATION_COLOR = arcade.color.GREEN
NEUTRAL_LOCATION_COLOR = arcade.color.WHITE
HAZARD_LOCATION_COLOR = arcade.color.YELLOW
TURBO_LOCATION_COLOR = arcade.color.ELECTRIC_CYAN

MALUS_LOCATION_ICON_FILE_PATH = os.path.join(SPRITES_LOCATION,'malus.png')
MERCHANT_LOCATION_ICON_FILE_PATH = os.path.join(SPRITES_LOCATION,'merchant.png')
QUESTION_LOCATION_ICON_FILE_PATH = os.path.join(SPRITES_LOCATION,'question.png')
NEUTRAL_LOCATION_ICON_FILE_PATH = os.path.join(SPRITES_LOCATION,'neutral.png')
HAZARD_LOCATION_ICON_FILE_PATH = os.path.join(SPRITES_LOCATION,'hazard.png')
TURBO_LOCATION_ICON_FILE_PATH = os.path.join(SPRITES_LOCATION,'turbo.png')

PLAYER1_COLOR = arcade.color.RICH_ELECTRIC_BLUE
PLAYER2_COLOR = arcade.color.AMETHYST
PLAYER3_COLOR = arcade.color.LIME_GREEN
PLAYER4_COLOR = arcade.color.MEDIUM_VERMILION

USE_ITEM_INVENTORY_ICON_FILE_PATH = os.path.join(SPRITES_LOCATION,'inventory.png')
END_TURN_ICON_FILE_PATH = os.path.join(SPRITES_LOCATION,'end_turn.png')
CURRENCY_SPRITE_ICON_FILE_PATH = os.path.join(SPRITES_LOCATION,'dollbran.png')
CURRENCY_SPRITE = arcade.Sprite(CURRENCY_SPRITE_ICON_FILE_PATH)

def get_items_from_db(number_of_items_to_get,player_in_world):
    db_connection = sqlite3.connect(ITEMS_DB_FILE_PATH)
    db_connection.row_factory = sqlite3.Row
    db_cursor = db_connection.cursor()

    class Item:
        def __init__(self,name,cost,targets,effect):
            self.name = name
            self.cost = cost
            self.targets = targets
            self.effect = effect

    db_cursor.execute('SELECT * FROM items WHERE item_avail_in_world=?', (player_in_world,))
    items_in_current_world_data = db_cursor.fetchall()
    items_for_current_world = []
    randomly_selected_items = []
    for item in items_in_current_world_data:
        item_name = item[1]
        item_cost = item[2]
        item_target = item[3]
        item_effect = item[4]
        current_item = Item(item_name,item_cost,item_target,item_effect)
        items_for_current_world.append(current_item)

    for _ in range(number_of_items_to_get):
        randomly_selected_item = random.choice(items_for_current_world)
        randomly_selected_items.append(randomly_selected_item)

    return randomly_selected_items

def get_malus_from_db(player_in_world):
    db_connection = sqlite3.connect(MALUS_DB_FILE_PATH)
    db_connection.row_factory = sqlite3.Row
    db_cursor = db_connection.cursor()

    class Malus:
        def __init__(self,name,targets,effect,takes_effect,sprite_file_name):
            self.name = name
            self.targets = targets
            self.effect = effect
            self.takes_effect = takes_effect
            self.sprite = get_effect_background_file(player_in_world,'malus',sprite_file_name)

    db_cursor.execute('SELECT * FROM malus WHERE malus_in_world=?',(player_in_world,))
    malus_in_current_world_data = db_cursor.fetchall()
    malus_for_current_world = []
    for malus in malus_in_current_world_data:
        malus_name = malus[1]
        malus_targets = malus[2]
        malus_effect = malus[3]
        malus_takes_effect = malus[5]
        malus_image_file_name = malus[6]

        current_malus = Malus(malus_name,malus_targets,malus_effect,malus_takes_effect,malus_image_file_name)
        malus_for_current_world.append(current_malus)

    randomly_selected_malus = random.choice(malus_for_current_world)

    return randomly_selected_malus

def get_question_with_choices_and_answer_from_ai(player_in_world):
    pass

def game_start_user_inputs():
    num_of_players = None
    while num_of_players is None:
        num_of_players = easygui.buttonbox("Choisir le nombre de joueurs","Début de partie", choices=['2', '3', '4'],default_choice="2")
        num_of_players = int(num_of_players)  # buttonbox returns a string, so we need to convert to int

    player_names = []
    max_name_length = 12  # Set the maximum length for a name
    for i in range(num_of_players):
        player_name = None
        while not player_name or len(player_name) > max_name_length:
            player_name = easygui.enterbox(f"Entrer le nom du joueur {i + 1} (max {max_name_length} characters):")
        player_names.append(player_name)

    return num_of_players, player_names

def get_dice_sprite(dice_number_on_face):
    sprite_file_name = str(dice_number_on_face) + ".png"
    sprite_file_path = os.path.join(SPRITES_LOCATION,sprite_file_name)

    return sprite_file_path

def get_player_sprite(player_number):
    sprite_file_name = "player_sprite" + str(player_number+1) + ".png"
    sprite_file_path = os.path.join(SPRITES_LOCATION,sprite_file_name)

    return sprite_file_path

def get_effect_background_file(current_world,type_of_effect,name_of_effect):
    first_level_directory_path = os.path.join(EFFECTS_BACKGROUNDS_LOCATION,str("world"+str(current_world)))
    second_level_directory_path = os.path.join(first_level_directory_path,type_of_effect)
    effect_background_path = os.path.join(second_level_directory_path,str(str(name_of_effect)+".png"))

    return effect_background_path

def get_player_color_by_number(player_number):
    if player_number == 0:
        player_color = PLAYER1_COLOR
    elif player_number == 1:
        player_color = PLAYER2_COLOR
    elif player_number == 2:
        player_color = PLAYER3_COLOR
    elif player_number == 3:
        player_color = PLAYER4_COLOR

    return player_color

def get_square_color_by_location_number(current_world,location_number):
    square_color = tuple[int, int, int]

    if current_world == 1:
        if location_number in WORLD_1_MALUS_LOCATIONS:
            square_color = MALUS_LOCATION_COLOR
        elif location_number in WORLD_1_MERCHANT_LOCATIONS:
            square_color = MERCHANT_LOCATION_COLOR
        elif location_number in WORLD_1_QUESTION_LOCATIONS:
            square_color = QUESTION_LOCATION_COLOR
        elif location_number in WORLD_1_NEUTRAL_LOCATIONS:
            square_color = NEUTRAL_LOCATION_COLOR
        elif location_number in WORLD_1_HAZARD_LOCATIONS:
            square_color = HAZARD_LOCATION_COLOR
        elif location_number in WORLD_1_TURBO_LOCATIONS:
            square_color = TURBO_LOCATION_COLOR

    elif current_world == 2:
        if location_number in WORLD_2_MALUS_LOCATIONS:
            square_color = MALUS_LOCATION_COLOR
        elif location_number in WORLD_2_MERCHANT_LOCATIONS:
            square_color = MERCHANT_LOCATION_COLOR
        elif location_number in WORLD_2_QUESTION_LOCATIONS:
            square_color = QUESTION_LOCATION_COLOR
        elif location_number in WORLD_2_NEUTRAL_LOCATIONS:
            square_color = NEUTRAL_LOCATION_COLOR
        elif location_number in WORLD_2_HAZARD_LOCATIONS:
            square_color = HAZARD_LOCATION_COLOR
        elif location_number in WORLD_2_TURBO_LOCATIONS:
            square_color = TURBO_LOCATION_COLOR

    elif current_world == 3:
        if location_number in WORLD_3_MALUS_LOCATIONS:
            square_color = MALUS_LOCATION_COLOR
        elif location_number in WORLD_3_MERCHANT_LOCATIONS:
            square_color = MERCHANT_LOCATION_COLOR
        elif location_number in WORLD_3_QUESTION_LOCATIONS:
            square_color = QUESTION_LOCATION_COLOR
        elif location_number in WORLD_3_NEUTRAL_LOCATIONS:
            square_color = NEUTRAL_LOCATION_COLOR
        elif location_number in WORLD_3_HAZARD_LOCATIONS:
            square_color = HAZARD_LOCATION_COLOR
        elif location_number in WORLD_3_TURBO_LOCATIONS:
            square_color = TURBO_LOCATION_COLOR

    return square_color

def get_square_icon_by_color(color):
    if color == (255, 0, 0, 175):
        icon = arcade.Sprite(MALUS_LOCATION_ICON_FILE_PATH)
    elif color == (0, 0, 255, 175):
        icon = arcade.Sprite(MERCHANT_LOCATION_ICON_FILE_PATH)
    elif color == (0, 255, 0, 175):
        icon = arcade.Sprite(QUESTION_LOCATION_ICON_FILE_PATH)
    elif color == (255, 255, 255, 175):
        icon = arcade.Sprite(NEUTRAL_LOCATION_ICON_FILE_PATH)
    elif color == (255, 255, 0, 175):
        icon = arcade.Sprite(HAZARD_LOCATION_ICON_FILE_PATH)
    elif color == (0, 255, 255, 175):
        icon = arcade.Sprite(TURBO_LOCATION_ICON_FILE_PATH)

    return icon

def get_map_background_for_world(current_world):
    background_file_name = "background_world" + str(current_world) + ".png"
    background_file_path = os.path.join(WORLDS_BACKGROUNDS_LOCATION,background_file_name)

    return background_file_path

def get_players_in_world(current_world,players):
    players_in_current_world = []
    for player in players:
        if player.current_world == current_world:
            players_in_current_world.append(player)

    return players_in_current_world

class Player:
    def __init__(self,player_number,player_name):
        self.player_id = player_number
        self.player_name = player_name
        self.player_sprite = arcade.Sprite(get_player_sprite(player_number))
        self.current_world = 1
        self.world_location = 1
        self.current_dollbran_amount = 0
        self.currently_held_items = []
        self.currently_affected_by_malus = []
        self.currently_affected_by_bonus = []
        self.number_of_dice_rolls_next_turn = 1

class Game(arcade.Window):
    def __init__(self, world_rows, number_of_players, players_names):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        self.text_visibility = True
        self.start_time = time.time()

        self.num_players = number_of_players
        self.player_names = players_names

        arcade.set_background_color(arcade.color.BLACK)

        self.current_world = 1
        self.background = arcade.load_texture(get_map_background_for_world(self.current_world))

        self.board = []
        self.square_width = MAP_WIDTH // COLUMNS_IN_A_WORLD
        self.square_height = SCREEN_HEIGHT // world_rows

        for row in range(world_rows):
            self.board.append([])
            for column in range(COLUMNS_IN_A_WORLD):
                location_number = row * COLUMNS_IN_A_WORLD + column + 1
                self.board[row].append(get_square_color_by_location_number(1,location_number))

        def define_players():
            players_list = []
            for player, player_number in enumerate(range(number_of_players)):
                player_name = players_names[player_number]
                player_id = player_number
                players_list.append(Player(player_id, player_name))

            return players_list

        self.players = define_players()

        # If you have sprite lists, you should create them here,
        # and set them to None
        self.player_sprites = arcade.SpriteList()
        self.dice_sprites = arcade.SpriteList()

        for player in self.players:
            self.player_sprites.append(player.player_sprite)

        for dice in range(0,7):
            dice_number_on_face = dice
            dice_to_add = arcade.Sprite(get_dice_sprite(dice_number_on_face))
            self.dice_sprites.append(dice_to_add)

        self.dice_sprite = self.dice_sprites[0]
        self.use_item_sprite = arcade.Sprite(USE_ITEM_INVENTORY_ICON_FILE_PATH)
        self.end_turn_sprite = arcade.Sprite(END_TURN_ICON_FILE_PATH)

        self.player_turn = 1

    def calculate_sprite_position(self,player):
        world_location = player.world_location

        row = (world_location - 1) // COLUMNS_IN_A_WORLD
        column = (world_location - 1) % COLUMNS_IN_A_WORLD

        # Count how many players are in the same location
        players_in_same_location = [player for player in self.players if player.world_location == world_location]
        player_index = players_in_same_location.index(player)

        # Calculate base position
        x = column * self.square_width + (self.square_width / 2) - 20
        y = SCREEN_HEIGHT - (row * self.square_height + (self.square_height / 2))

        # Offset position based on index
        x += player_index * SPRITE_OFFSET_X
        y += player_index * SPRITE_OFFSET_Y

        return x, y

    def update_map(self, world):
        # Determine the number of rows based on the current world
        if world == 1:
            rows = WORLD_1_NUMBER_OF_ROWS
        elif world == 2:
            rows = WORLD_2_NUMBER_OF_ROWS
        elif world == 3:
            rows = WORLD_3_NUMBER_OF_ROWS
        else:
            raise ValueError("Invalid world number")
        self.square_height = SCREEN_HEIGHT // rows

        # Create a new board with the correct number of squares
        self.board = []
        for row in range(rows):
            self.board.append([])
            for column in range(COLUMNS_IN_A_WORLD):
                location_number = row * COLUMNS_IN_A_WORLD + column + 1
                self.board[row].append(get_square_color_by_location_number(world, location_number))
        for player in self.players:
            if player.current_world == self.current_world:  # Only draw the sprite if the player is in the current world
                player.player_sprite.center_x, player.player_sprite.center_y = self.calculate_sprite_position(player)
            else:
                player.player_sprite.center_x, player.player_sprite.center_y = -100, -100  # Move the sprite off-screen

        self.player_sprites.draw()

        # Update the background
        self.background = arcade.load_texture(get_map_background_for_world(world))

    def on_draw(self):
        """
        Render the screen.
        """

        # This command should happen before we start drawing. It will clear
        # the screen to the background color, and erase what we drew last frame.
        self.clear()

        arcade.start_render()

        arcade.draw_rectangle_filled(MAP_WIDTH + SIDEBAR_WIDTH / 2, BOTTOM_BAR_HEIGHT / 2, SIDEBAR_WIDTH, BOTTOM_BAR_HEIGHT, arcade.color.BLACK)
        arcade.draw_rectangle_outline(MAP_WIDTH + SIDEBAR_WIDTH / 2, BOTTOM_BAR_HEIGHT / 2, SIDEBAR_WIDTH, BOTTOM_BAR_HEIGHT, arcade.color.ELECTRIC_VIOLET, border_width=2)

        map_center_x = MAP_WIDTH // 2
        map_center_y = SCREEN_HEIGHT // 2
        arcade.draw_texture_rectangle(map_center_x, map_center_y, MAP_WIDTH, SCREEN_HEIGHT, self.background)

        for row in range(len(self.board)):
            for column in range(COLUMNS_IN_A_WORLD):
                color = (*self.board[row][column], 175)
                icon = get_square_icon_by_color(color)

                x = column * self.square_width + (self.square_width / 2)
                y = SCREEN_HEIGHT - (row * self.square_height + (self.square_height / 2))
                arcade.draw_rectangle_filled(x, y, self.square_width, self.square_height, color)
                arcade.draw_rectangle_outline(x, y, self.square_width+2.5, self.square_height+2.5, arcade.color.ELECTRIC_VIOLET, border_width=5)

                icon_x = x - (self.square_width / 2) + 5
                icon_y = y + (self.square_height / 2) - 5
                icon.center_x = icon_x + icon.width / 2  # Add half the width of the icon to center it within that space
                icon.center_y = icon_y - icon.height / 2  # Subtract half the height of the icon to center it within that space
                icon.draw()

                text_background_width = self.square_width / 4
                text_background_height = self.square_height / 4
                text_background_x = (column + 1) * self.square_width - text_background_width / 2
                text_background_y = SCREEN_HEIGHT - ((row + 1) * self.square_height - text_background_height / 2)
                arcade.draw_rectangle_filled(text_background_x, text_background_y, text_background_width, text_background_height, arcade.color.BLACK)
                arcade.draw_rectangle_outline(text_background_x, text_background_y, text_background_width, text_background_height, arcade.color.ELECTRIC_VIOLET, border_width=2)

                location_number = row * COLUMNS_IN_A_WORLD + column + 1
                text_x = text_background_x
                text_y = text_background_y
                arcade.draw_text(str(location_number), text_x, text_y, arcade.color.WHITE, 14, align="center", anchor_x="center", anchor_y="center", width=100)

        # Draw player names and information on the sidebar
        for i, player_name in enumerate(self.player_names):
            current_player = self.players[self.player_turn - 1].player_id
            y = SCREEN_HEIGHT - (i * 150 + 30)  # Increase distance between each player's information and move it further down

            player_name_text=f"{player_name}"
            first_text_width = len(player_name_text) * 18
            if current_player == i:
                if self.text_visibility:
                    arcade.draw_text(player_name_text, MAP_WIDTH + 15, y, get_player_color_by_number(i), 18,bold=True)  # Move text further to the right
            else:
                arcade.draw_text(player_name_text, MAP_WIDTH + 15, y, get_player_color_by_number(i), 18, bold=True)

            padding = 25
            second_text_x = MAP_WIDTH + 30 + first_text_width + padding
            dollbran_amount_text = f"{self.players[i].current_dollbran_amount}"
            arcade.draw_text(dollbran_amount_text, second_text_x, y, arcade.color.GOLD, 14, bold=True)
            dollbran_amount_text_width = len(dollbran_amount_text) * 14  # Change the multiplier based on your font size
            CURRENCY_SPRITE.center_x = second_text_x + dollbran_amount_text_width + 42
            CURRENCY_SPRITE.center_y = y + 7
            CURRENCY_SPRITE.draw()
            arcade.draw_text(f"Items: {''.join(self.players[i].currently_held_items)}", MAP_WIDTH + 15, y - 28, arcade.color.WHITE, 12)
            arcade.draw_text(f"Malus actifs: {''.join(self.players[i].currently_affected_by_malus)}", MAP_WIDTH + 15, y - 70, arcade.color.ELECTRIC_GREEN, 12)
            arcade.draw_text(f"Bonus actifs: {''.join(self.players[i].currently_affected_by_bonus)}", MAP_WIDTH + 15, y - 90, arcade.color.ELECTRIC_CRIMSON, 12)

            # Draw a separator line below each player's information
            if i < len(self.player_names) - 1:  # Don't draw a line after the last player's information
                arcade.draw_line(MAP_WIDTH + 10, y - 115, SCREEN_WIDTH - 10, y - 115, arcade.color.ELECTRIC_VIOLET, 2)

        def calculate_dice_sprite_position():
            x = MAP_WIDTH + (SIDEBAR_WIDTH // 4)
            y = BOTTOM_BAR_HEIGHT // 2

            return x, y

        def calculate_inventory_sprite_position():
            x = MAP_WIDTH + (SIDEBAR_WIDTH // 2)
            y = BOTTOM_BAR_HEIGHT // 2

            return x, y

        def calculate_end_turn_sprite_position():
            x = MAP_WIDTH + ((SIDEBAR_WIDTH // 4) * 3)
            y = BOTTOM_BAR_HEIGHT // 2

            return x, y

        for player in self.players:
            if player.current_world == self.current_world:  # Only draw the sprite if the player is in the current world
                player.player_sprite.center_x, player.player_sprite.center_y = self.calculate_sprite_position(player)
            else:
                player.player_sprite.center_x, player.player_sprite.center_y = -100, -100  # Move the sprite off-screen
        self.player_sprites.draw()

        self.dice_sprite.center_x, self.dice_sprite.center_y = calculate_dice_sprite_position()
        self.use_item_sprite.center_x, self.use_item_sprite.center_y = calculate_inventory_sprite_position()
        self.end_turn_sprite.center_x, self.end_turn_sprite.center_y = calculate_end_turn_sprite_position()

        self.dice_sprite.draw()
        self.use_item_sprite.draw()
        self.end_turn_sprite.draw()

    def on_update(self, delta_time):
        """
        All the logic to move, and the game logic goes here.
        Normally, you'll call update() on the sprite lists that
        need it.
        """
        if time.time() - self.start_time > 0.5:  # Adjusts the blink speed
            self.text_visibility = not self.text_visibility
            self.start_time = time.time()

    def roll_dice_if_allowed(self):
        active_player = self.players[self.player_turn - 1]
        if active_player.number_of_dice_rolls_next_turn > 0:
            dice_number = self.roll_dice()  # Roll the dice
            active_player.number_of_dice_rolls_next_turn -= 1

    def manage_merchant_interaction(self,player_id,items):
        purchased_items = []
        for player in self.players:
            if player.player_id == player_id:
                player_amount_of_dollbran = player.current_dollbran_amount
                break

        #Draw and click functions

        selected_item = int()
        item = items[selected_item]
        if player_amount_of_dollbran >= item.cost:
            player_amount_of_dollbran -= item.cost
            for player in self.players:
                if player.player_id == player_id:
                    player.current_dollbran_amount = player_amount_of_dollbran
                    break
            purchased_items.append(item)

        for item in purchased_items:
            for player in self.players:
                if player.player_id == player_id:
                    player.currently_held_items.append(item)

        return purchased_items

    def manage_malus_effect(self,player_id,malus):
        if malus.takes_effect == 'immed':
            pass
        else:
            for player in self.players:
                if player.player_id == player_id:
                    player.currently_affected_by_malus.append(malus.name)
            if malus.takes_effect == 'next_turn':
                pass
            elif malus.takes_effect == 'next_two_turns':
                pass
            elif malus.takes_effect == 'next_merchant':
                pass
            elif malus.takes_effect == 'immed_and_next_turn':
                pass

    def manage_square_effect(self,current_player,color_of_square):
        player_id = current_player.player_id

        if color_of_square == (255, 0, 0):
            #square_type = 'malus'
            malus_background_image_file_path = os.path.join(EFFECTS_BACKGROUNDS_LOCATION,'malus.png')
            easygui.msgbox(
                "Vous êtes sur une case de malus... oups... voyons voir ce que le mauvais sort vous réserve...",
                title="Case de Malus",ok_button="Voir le malus",image=malus_background_image_file_path)
            malus = get_malus_from_db(current_player.current_world)
            self.manage_malus_effect(player_id,malus)
            easygui.msgbox(
                msg=str(malus.name+"\n"+malus.effect),title="Malus",image=malus.sprite
            )

        elif color_of_square == (0, 0, 255):
            #square_type = 'merchant'
            if current_player.current_world == 1:
                merchant_background_image_file_path = os.path.join(EFFECTS_BACKGROUNDS_LOCATION,'merchant_world1.png')
            else:
                merchant_background_image_file_path = os.path.join(EFFECTS_BACKGROUNDS_LOCATION,'merchant_world2-3.png')

            items = get_items_from_db(3,current_player.current_world)
            easygui.msgbox("Vous êtes sur une case de marchand, vous pouvez échanger vos Dollbrans pour des objets qui peuvent vous aider dans votre aventure.",
                           title="Case de Marchand",ok_button="Voir les objets en vente",image=merchant_background_image_file_path)

        elif color_of_square == (0, 255, 0):
            #square_type = 'question'
            question_background_image_file_path = os.path.join(EFFECTS_BACKGROUNDS_LOCATION,'question.png')
            #get_question_with_choices_and_answer_from_ai(current_player.current_world)
            easygui.msgbox("Vous êtes sur une case de question... voyons voir si vous méritez quelques dollbrans !",
                           title="Case de Question",ok_button="Voir la question et le choix de réponses",image=question_background_image_file_path)

        elif color_of_square == (255, 255, 255):
            #square_type = 'neutral'
            neutral_background_image_file_path = os.path.join(EFFECTS_BACKGROUNDS_LOCATION,'neutral.png')
            easygui.msgbox("Vous êtes sur une case neutre, un peu de repos ne fait jamais de tord !",
                           title="Case Neutre",ok_button="Chilling",image=neutral_background_image_file_path)

        elif color_of_square == (255, 255, 0):
            #square_type = 'hazard'
            hazard_background_image_file_path = os.path.join(EFFECTS_BACKGROUNDS_LOCATION,'hazard.png')
            easygui.msgbox("Vous êtes sur une case de hasard... ça peut être positif ou négatif...",
                           title="Case de Hasard", ok_button="Voir ce que le hasard vous réserve",image=hazard_background_image_file_path)
            type_of_hazard = random.randint(0,1)

            if type_of_hazard == 0:
                malus_background_image_file_path = os.path.join(EFFECTS_BACKGROUNDS_LOCATION, 'malus.png')
                easygui.msgbox("C'est négatif... oups... voyons voir ce que le mauvais sort vous réserve...",
                           title="Résultat de la case de hasard",ok_button="Voir le malus",image=malus_background_image_file_path)
                malus = get_malus_from_db(current_player.current_world)
                self.manage_malus_effect(player_id,malus)
                easygui.msgbox(
                    msg=str(malus.name + "\n" + malus.effect), title="Malus", image=malus.sprite
                )

            elif type_of_hazard == 1:
                item_found_image_file_path = os.path.join(EFFECTS_BACKGROUNDS_LOCATION, 'bonus_item.png')
                easygui.msgbox("C'est positif !!! Voyons voir quel trésor vous avez obtenu !",
                           title="Résultat de la case de hasard",ok_button="Voir l'objet trouvé",image=item_found_image_file_path)
                item = get_items_from_db(1,current_player.current_world)[0]
                for player in self.players:
                    if player.player_id == player_id:
                        player.currently_held_items.append(item.name)
                        break

        elif color_of_square == (0, 255, 255):
            #square_type = 'turbo'
            turbo_background_image_file_path = os.path.join(EFFECTS_BACKGROUNDS_LOCATION, 'turbo.png')
            for player in self.players:
                if player.player_id == player_id:
                    player.number_of_dice_rolls_next_turn += 1
                    easygui.msgbox("Vous êtes sur une case turbo, vous avez un lancer de dé supplémentaire !",
                                   title="Case Turbo",ok_button="Lancer le dé supplémentaire",image=turbo_background_image_file_path)
                    self.roll_dice_if_allowed()
                    break

    def item_used(self):
        pass

    def roll_dice(self):
        dice_number = random.randint(1, 6)  # Generate a random number between 1 and 6
        self.dice_sprite = self.dice_sprites[dice_number]  # Update the dice sprite

        # Get the current player
        current_player = self.players[self.player_turn - 1]  # Subtract 1 because list indices start at 0

        # Update the player's location
        current_player.world_location += dice_number
        current_player_on_type_of_square = get_square_color_by_location_number(current_player.current_world,current_player.world_location)

        # If player's location exceeds the maximum location in the world, move to next world or end game
        if current_player.current_world == 1 and current_player.world_location > WORLD_1_NUMBER_OF_LOCATIONS:
            excess_steps = current_player.world_location - WORLD_1_NUMBER_OF_LOCATIONS
            current_player.current_world = 2
            current_player.world_location = 1 + excess_steps
            self.current_world = current_player.current_world
            self.update_map(self.current_world)

        elif current_player.current_world == 2 and current_player.world_location > WORLD_2_NUMBER_OF_LOCATIONS:
            excess_steps = current_player.world_location - WORLD_2_NUMBER_OF_LOCATIONS
            current_player.current_world = 3
            current_player.world_location = 1 + excess_steps
            self.current_world = current_player.current_world
            self.update_map(self.current_world)

        elif current_player.current_world == 3 and current_player.world_location > WORLD_3_NUMBER_OF_LOCATIONS:
            # End game or wrap around to first world, depending on your game rules
            current_player.world_location = WORLD_3_NUMBER_OF_LOCATIONS
            self.update_map(self.current_world)

        self.manage_square_effect(current_player,current_player_on_type_of_square)

        return dice_number

    def manage_new_turn(self, last_player_to_play, players):
        # Update the player's turn before getting the current player
        last_player_to_play = self.player_turn
        self.players[last_player_to_play - 1].number_of_dice_rolls_next_turn = 1

        if last_player_to_play == len(self.players):
            self.player_turn = 1
        else:
            self.player_turn += 1

        active_player = self.players[self.player_turn - 1]
        self.current_world = active_player.current_world
        self.update_map(active_player.current_world)

    def on_key_press(self, key, key_modifiers):
        """
        Called whenever a key on the keyboard is pressed.

        For a full list of keys, see:
        https://api.arcade.academy/en/latest/arcade.key.html
        """
        pass

    def on_key_release(self, key, key_modifiers):
        """
        Called whenever the user lets off a previously pressed key.
        """
        pass

    def on_mouse_motion(self, x, y, delta_x, delta_y):
        """
        Called whenever the mouse moves.
        """
        pass

    def on_mouse_press(self, x, y, button, key_modifiers):
        """
        Called when the user presses a mouse button.
        """
        active_player = self.players[self.player_turn - 1]
        number_of_clicks_allowed_on_dice = active_player.number_of_dice_rolls_next_turn

        if self.dice_sprite.collides_with_point((x, y)):  # If the player clicks on the dice sprite
            if number_of_clicks_allowed_on_dice > 0:
                self.roll_dice_if_allowed()

            else:
                pass

        if self.end_turn_sprite.collides_with_point((x, y)):
            if number_of_clicks_allowed_on_dice > 0:
                pass
            else:
                self.manage_new_turn(self.player_turn, self.players)

    def on_mouse_release(self, x, y, button, key_modifiers):
        """
        Called when a user releases a mouse button.
        """
        pass

def main():
    """ Main function """
    number_of_players, players_names = game_start_user_inputs()
    window = Game(WORLD_1_NUMBER_OF_ROWS, number_of_players, players_names)
    arcade.run()

if __name__ == "__main__":
    main()