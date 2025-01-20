import arcade
import arcade.gui
import easygui
import os
import time
import random

from arcade.examples.minimap import MAP_HEIGHT

PATH_BASE = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(PATH_BASE,'data')
IMG_PATH = os.path.join(DATA_PATH,'img')
DB_PATH = os.path.join(DATA_PATH,'db')
WORLDS_BACKGROUNDS_LOCATION = os.path.join(IMG_PATH,'backgrounds')
SPRITES_LOCATION = os.path.join(IMG_PATH,'sprites')

SCREEN_WIDTH = 1300
SCREEN_HEIGHT = 1000
SCREEN_TITLE = "Voyage au centre de la galaxie"
MAIN_MENU_BACKGROUND_FILE_PATH = os.path.join(WORLDS_BACKGROUNDS_LOCATION,'main.png')
USE_ITEM_INVENTORY_ICON_FILE_PATH = os.path.join(SPRITES_LOCATION,'inventory.png')
END_TURN_ICON_FILE_PATH = os.path.join(SPRITES_LOCATION,'end_turn.png')

SIDEBAR_WIDTH = SCREEN_WIDTH * 0.3
MAP_WIDTH = SCREEN_WIDTH - SIDEBAR_WIDTH
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
WORLD_1_NEUTRAL_LOCATIONS = [1,6,8,9,14,17,22,28,30]

WORLD_2_MALUS_LOCATIONS = [3,8,11,14,17,23,24,27,32,35]
WORLD_2_MERCHANT_LOCATIONS = [10,20,30,39]
WORLD_2_QUESTION_LOCATIONS = [2,4,5,6,9,12,15,18,19,22,26,29,33,36,38]
WORLD_2_NEUTRAL_LOCATIONS = [1,7,13,16,21,25,28,31,34,37,40]

WORLD_3_MALUS_LOCATIONS = [3,4,7,11,14,19,21,24,32,38,41,43,44,45,47,49]
WORLD_3_MERCHANT_LOCATIONS = [10,15,25,40]
WORLD_3_QUESTION_LOCATIONS = [5,6,8,9,12,13,16,18,20,22,26,28,30,33,34,35,37]
WORLD_3_NEUTRAL_LOCATIONS = [1,2,16,17,23,27,29,31,36,39,42,46,48,50]

MALUS_LOCATION_COLOR = arcade.color.RED
MERCHANT_LOCATION_COLOR = arcade.color.BLUE
QUESTION_LOCATION_COLOR = arcade.color.GREEN
NEUTRAL_LOCATION_COLOR = arcade.color.WHITE

MALUS_LOCATION_ICON_FILE_PATH = os.path.join(SPRITES_LOCATION,'malus.png')
MERCHANT_LOCATION_ICON_FILE_PATH = os.path.join(SPRITES_LOCATION,'merchant.png')
QUESTION_LOCATION_ICON_FILE_PATH = os.path.join(SPRITES_LOCATION,'question.png')
NEUTRAL_LOCATION_ICON_FILE_PATH = os.path.join(SPRITES_LOCATION,'neutral.png')

PLAYER1_COLOR = arcade.color.RICH_ELECTRIC_BLUE
PLAYER2_COLOR = arcade.color.AMETHYST
PLAYER3_COLOR = arcade.color.LIME_GREEN
PLAYER4_COLOR = arcade.color.MEDIUM_VERMILION

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

def get_map_background_for_world(current_world):
    background_file_name = "background_world" + str(current_world) + ".png"
    background_file_path = os.path.join(WORLDS_BACKGROUNDS_LOCATION,background_file_name)

    return background_file_path

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

    elif current_world == 2:
        if location_number in WORLD_2_MALUS_LOCATIONS:
            square_color = MALUS_LOCATION_COLOR
        elif location_number in WORLD_2_MERCHANT_LOCATIONS:
            square_color = MERCHANT_LOCATION_COLOR
        elif location_number in WORLD_2_QUESTION_LOCATIONS:
            square_color = QUESTION_LOCATION_COLOR
        elif location_number in WORLD_2_NEUTRAL_LOCATIONS:
            square_color = NEUTRAL_LOCATION_COLOR

    elif current_world == 3:
        if location_number in WORLD_3_MALUS_LOCATIONS:
            square_color = MALUS_LOCATION_COLOR
        elif location_number in WORLD_3_MERCHANT_LOCATIONS:
            square_color = MERCHANT_LOCATION_COLOR
        elif location_number in WORLD_3_QUESTION_LOCATIONS:
            square_color = QUESTION_LOCATION_COLOR
        elif location_number in WORLD_3_NEUTRAL_LOCATIONS:
            square_color = NEUTRAL_LOCATION_COLOR

    return square_color

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

        arcade.set_background_color(arcade.color.BLACK)
        self.num_players = number_of_players
        self.player_names = players_names

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

        # Create a new board with the correct number of squares
        self.board = []
        for row in range(rows):
            self.board.append([])
            for column in range(COLUMNS_IN_A_WORLD):
                location_number = row * COLUMNS_IN_A_WORLD + column + 1
                self.board[row].append(get_square_color_by_location_number(world, location_number))

        # Update the background
        self.background = arcade.load_texture(get_map_background_for_world(world))

    def roll_dice(self):
        dice_number = random.randint(1, 6)  # Generate a random number between 1 and 6
        self.dice_sprite = self.dice_sprites[dice_number]  # Update the dice sprite

        # Get the current player
        current_player = self.players[self.player_turn - 1]  # Subtract 1 because list indices start at 0

        # Update the player's location
        current_player.world_location += dice_number

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
            pass

        return dice_number

    def on_draw(self):
        """
        Render the screen.
        """

        # This command should happen before we start drawing. It will clear
        # the screen to the background color, and erase what we drew last frame.
        self.clear()
        arcade.start_render()
        bottom_bar_height = 150  # Set the height of the bottom bar
        arcade.draw_rectangle_filled(MAP_WIDTH + SIDEBAR_WIDTH / 2, bottom_bar_height / 2, SIDEBAR_WIDTH, bottom_bar_height, arcade.color.BLACK)
        arcade.draw_rectangle_outline(MAP_WIDTH + SIDEBAR_WIDTH / 2, bottom_bar_height / 2, SIDEBAR_WIDTH, bottom_bar_height, arcade.color.ELECTRIC_VIOLET, border_width=2)

        map_center_x = MAP_WIDTH // 2
        map_center_y = SCREEN_HEIGHT // 2
        arcade.draw_texture_rectangle(map_center_x, map_center_y, MAP_WIDTH, SCREEN_HEIGHT, self.background)
        for row in range(len(self.board)):
            for column in range(COLUMNS_IN_A_WORLD):
                color = (*self.board[row][column], 175)
                if color == (255, 0, 0, 175):
                    icon = arcade.Sprite(MALUS_LOCATION_ICON_FILE_PATH)
                elif color == (0, 0, 255, 175):
                    icon = arcade.Sprite(MERCHANT_LOCATION_ICON_FILE_PATH)
                elif color == (0, 255, 0, 175):
                    icon = arcade.Sprite(QUESTION_LOCATION_ICON_FILE_PATH)
                elif color == (255, 255, 255, 175):
                    icon = arcade.Sprite(NEUTRAL_LOCATION_ICON_FILE_PATH)

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
            second_text_x = MAP_WIDTH + 15 + first_text_width + padding
            arcade.draw_text(f"{self.players[i].current_dollbran_amount} Dollbrans", second_text_x, y, arcade.color.GOLD, 12, bold=True)
            arcade.draw_text(f"Items: {''.join(self.players[i].currently_held_items)}", MAP_WIDTH + 15, y - 25, arcade.color.WHITE, 12)
            arcade.draw_text(f"Malus actifs: {''.join(self.players[i].currently_affected_by_malus)}", MAP_WIDTH + 15, y - 70, arcade.color.ELECTRIC_GREEN, 12)
            arcade.draw_text(f"Bonus actifs: {''.join(self.players[i].currently_affected_by_bonus)}", MAP_WIDTH + 15, y - 90, arcade.color.ELECTRIC_CRIMSON, 12)
            # Draw a separator line below each player's information
            if i < len(self.player_names) - 1:  # Don't draw a line after the last player's information
                arcade.draw_line(MAP_WIDTH + 10, y - 115, SCREEN_WIDTH - 10, y - 115, arcade.color.ELECTRIC_VIOLET, 2)

        def calculate_sprite_position(player):
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

        def calculate_dice_sprite_position():
            x = MAP_WIDTH + (SIDEBAR_WIDTH // 4)
            y = bottom_bar_height // 2

            return x, y

        def calculate_inventory_sprite_position():
            x = MAP_WIDTH + (SIDEBAR_WIDTH // 2)
            y = bottom_bar_height // 2

            return x, y

        def calculate_end_turn_sprite_position():
            x = MAP_WIDTH + ((SIDEBAR_WIDTH // 4) * 3)
            y = bottom_bar_height // 2

            return x, y

        for player in self.players:
            if player.current_world == self.current_world:  # Only draw the sprite if the player is in the current world
                player.player_sprite.center_x, player.player_sprite.center_y = calculate_sprite_position(player)
            else:
                player.player_sprite.center_x, player.player_sprite.center_y = -100, -100  # Move the sprite off-screen

        self.dice_sprite.center_x, self.dice_sprite.center_y = calculate_dice_sprite_position()
        self.use_item_sprite.center_x, self.use_item_sprite.center_y = calculate_inventory_sprite_position()
        self.end_turn_sprite.center_x, self.end_turn_sprite.center_y = calculate_end_turn_sprite_position()
        # Call draw() on all your sprite lists below
        self.player_sprites.draw()
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


    def manage_new_turn(self, last_player_to_play, players):
        # Update the player's turn before getting the current player
        last_player_to_play = self.player_turn
        self.players[last_player_to_play - 1].number_of_dice_rolls_next_turn = 1

        if last_player_to_play == len(self.players):
            self.player_turn = 1
        else:
            self.player_turn += 1

        active_player = self.players[self.player_turn - 1]

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
                dice_number = self.roll_dice()  # Roll the dice
                number_of_clicks_allowed_on_dice -= 1
                self.players[self.player_turn - 1].number_of_dice_rolls_next_turn = number_of_clicks_allowed_on_dice
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