import arcade

SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
SCREEN_TITLE = "Scrolling Background"

LEFT_VIEWPORT_MARGIN = 100
RIGHT_VIEWPORT_MARGIN = 100
TOP_VIEWPORT_MARGIN = 100
BOTTOM_VIEWPORT_MARGIN = 100

SCROLL_SPEED = 2

UPDATES_PER_FRAME = 40

class Layer():
    def __init__(self, image, scroll=0):
        self.texture = arcade.load_texture(image)

        # this starts relative to the initial view frame
        # TODO: generalize how x is used
        self.x = 0
        self.pos = 0
        self.scroll = scroll
        

    def draw(self):
        # draw two rectangles so you get the full effect. 
        # TODO: figure out how to keep these scrolling infinitely
        arcade.draw_lrwh_rectangle_textured(self.x, 0, SCREEN_WIDTH, SCREEN_HEIGHT, self.texture) 
        arcade.draw_lrwh_rectangle_textured(SCREEN_WIDTH+self.x, 0, SCREEN_WIDTH, SCREEN_HEIGHT, self.texture) 

    def update(self, increment):
        # the pos argument allows us to accumulate partial increments before 
        # converting to an int for self.x
        self.pos += self.scroll * increment
        self.x = int(self.pos)

class App(arcade.Window):
    def __init__(self, width, height, title):
        super().__init__(width,height,title)

        self.player_list = None
        self.layer_list = None

        self.player = None

        self.view_bottom = 0
        self.view_left = 0

    def setup(self):
        self.player_list = arcade.SpriteList()
        self.layer_list = [] 

        self.player = arcade.Sprite("character_robot_walk0.png",scale=.5)
        self.player.center_x = 320
        self.player.center_y = 100
        self.player_list.append(self.player)

        self.layer_list.append(Layer("parallax/_11_background.png"))
        self.layer_list.append(Layer("parallax/_10_distant_clouds.png",scroll=-.2))
        self.layer_list.append(Layer("parallax/_09_distant_clouds1.png",scroll=-.4))
        self.layer_list.append(Layer("parallax/_08_clouds.png",scroll=-.6))
        self.layer_list.append(Layer("parallax/_07_huge_clouds.png",scroll=-.7))
        self.layer_list.append(Layer("parallax/_06_hill2.png",scroll=-.4))
        self.layer_list.append(Layer("parallax/_05_hill1.png",scroll=-.5))
        self.layer_list.append(Layer("parallax/_04_bushes.png",scroll=-.6))
        self.layer_list.append(Layer("parallax/_03_distant_trees.png",scroll=-.7))
        self.layer_list.append(Layer("parallax/_02_trees and bushes.png",scroll=-.9))
        self.layer_list.append(Layer("parallax/_01_ground.png"))

    def on_draw(self):
        arcade.start_render()

        for layer in self.layer_list:
            layer.draw()

        self.player_list.draw()

    def on_update(self, delta_time):

        # UPDATE PLAYER AND LAYERS USING PLAYER MOVEMENT
        self.player_list.update()
        for layer in self.layer_list:
            layer.update(self.player.change_x)

        # VIEW PORT CODE
        changed = False

        left_boundary = self.view_left + LEFT_VIEWPORT_MARGIN
        if self.player.left < left_boundary:
            self.view_left -= left_boundary - self.player.left
            changed = True

        right_boundary = self.view_left + SCREEN_WIDTH - RIGHT_VIEWPORT_MARGIN
        if self.player.right > right_boundary:
            self.view_left += self.player.right - right_boundary
            changed = True

        top_boundary = self.view_bottom + SCREEN_HEIGHT - TOP_VIEWPORT_MARGIN
        if self.player.top > top_boundary:
            self.view_bottom += self.player.top - top_boundary
            changed = True

        bottom_boundary = self.view_bottom + BOTTOM_VIEWPORT_MARGIN
        if self.player.bottom < bottom_boundary:
            self.view_bottom -= bottom_boundary - self.player.bottom
            changed = True

        if changed:
            self.view_bottom = int(self.view_bottom)
            self.view_left = int(self.view_left)

            arcade.set_viewport(self.view_left, 
                                SCREEN_WIDTH + self.view_left, 
                                self.view_bottom, 
                                SCREEN_HEIGHT + self.view_bottom)

        # END VIEW PORT CODE

    # PLAYER CONTROLS
    def on_key_press(self, key, modifiers):
        if key == arcade.key.LEFT:
            self.player.change_x = -SCROLL_SPEED
        elif key == arcade.key.RIGHT:
            self.player.change_x = SCROLL_SPEED
    
    def on_key_release(self, key, modifiers):
        if key == arcade.key.LEFT or key == arcade.key.RIGHT:
            self.player.change_x = 0
    # END PLAYER CONTROLS

def main():
    app = App(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    app.setup()
    arcade.run()

if __name__ == "__main__":
    main()
