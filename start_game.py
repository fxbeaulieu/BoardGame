import arcade
import arcade.gui
import easygui
import os

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

WORLD_2_MALUS_LOCATIONS = []
WORLD_2_MERCHANT_LOCATIONS = []
WORLD_2_QUESTION_LOCATIONS = []
WORLD_2_NEUTRAL_LOCATIONS = []

WORLD_3_MALUS_LOCATIONS = []
WORLD_3_MERCHANT_LOCATIONS = []
WORLD_3_QUESTION_LOCATIONS = []
WORLD_3_NEUTRAL_LOCATIONS = []

MALUS_LOCATION_COLOR = arcade.color.RED
MERCHANT_LOCATION_COLOR = arcade.color.BLUE
QUESTION_LOCATION_COLOR = arcade.color.GREEN
NEUTRAL_LOCATION_COLOR = arcade.color.WHITE

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

class Game(arcade.Window):
    def __init__(self, world_rows, number_of_players, players_names):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
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
        self.player_sprites = arcade.SpriteList()
        self.dice_sprites = arcade.SpriteList()
        for player in self.players:
            self.player_sprites.append(player.player_sprite)
        for dice in range(0,6):
            dice_number_on_face = dice
            self.dice_sprites.append(arcade.Sprite(get_dice_sprite(dice_number_on_face)))
        self.dice_sprite = self.dice_sprites[0]
        self.use_item_sprite = arcade.Sprite(USE_ITEM_INVENTORY_ICON_FILE_PATH)
        self.player_turn = 1

        # If you have sprite lists, you should create them here,
        # and set them to None

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
                x = column * self.square_width + (self.square_width / 2)
                y = SCREEN_HEIGHT - (row * self.square_height + (self.square_height / 2))
                arcade.draw_rectangle_filled(x, y, self.square_width, self.square_height, color)
                arcade.draw_rectangle_outline(x, y, self.square_width+2.5, self.square_height+2.5, arcade.color.ELECTRIC_VIOLET, border_width=5)

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
            y = SCREEN_HEIGHT - (i * 150 + 30)  # Increase distance between each player's information and move it further down
            player_name_text=f"{player_name}"
            first_text_width = len(player_name_text) * 18
            arcade.draw_text(player_name_text, MAP_WIDTH + 15, y, arcade.color.ELECTRIC_VIOLET, 18,bold=True)  # Move text further to the right
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
            x = MAP_WIDTH + ((SIDEBAR_WIDTH // 4) * 3)
            y = bottom_bar_height // 2

            return x, y

        for player in self.players:
            player.player_sprite.center_x, player.player_sprite.center_y = calculate_sprite_position(player)

        self.dice_sprite.center_x, self.dice_sprite.center_y = calculate_dice_sprite_position()
        self.use_item_sprite.center_x, self.use_item_sprite.center_y = calculate_inventory_sprite_position()
        # Call draw() on all your sprite lists below
        self.player_sprites.draw()
        self.dice_sprite.draw()
        self.use_item_sprite.draw()

    def on_update(self, delta_time):
        """
        All the logic to move, and the game logic goes here.
        Normally, you'll call update() on the sprite lists that
        need it.
        """

        def refresh_map_for_new_turn(current_player_turn, current_player_world, current_player_location, players):
            map_background_to_display_file_path = get_map_background_for_world(current_player_world)
            players_to_display_on_map = get_players_in_world(current_player_world, players)
            for player in players_to_display_on_map:
                player_location_on_map = player.world_location

        def manage_new_turn(last_player_to_play, players):
            if last_player_to_play == len(players):
                active_player_id = 1
            else:
                active_player_id = last_player_to_play + 1

            active_player = players[active_player_id - 1]
            active_player_world = active_player.current_world
            active_player_location = active_player.world_location
            refresh_map_for_new_turn(active_player_id, active_player_world, active_player_location, players)

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
        pass

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