import arcade

from ev3dev2simulator.config.config import get_config
from ev3dev2simulator.robot.BodyPart import BodyPart

COLORS = dict()
COLORS[0] = 0  # set black for no color
COLORS[1] = 0
COLORS[2] = 1
COLORS[3] = 2
COLORS[4] = 5
COLORS[5] = 3
COLORS[6] = 4


class ColorSensor(BodyPart):
    """
    Class representing a ColorSensor of the simulated robot.
    """

    def __init__(self,
                 brick: int,
                 address: str,
                 robot,
                 delta_x: int,
                 delta_y: int,
                 name: str):
        super(ColorSensor, self).__init__(brick, address, robot, delta_x, delta_y, 'color_sensor')
        self.name = name
        self.old_texture_index = 0

    def setup_visuals(self, scale):
        img_cfg = get_config().get_visualisation_config()['image_paths']
        black_texture = arcade.load_texture(img_cfg['color_sensor_black'], scale=scale * 0.26)
        blue_texture = arcade.load_texture(img_cfg['color_sensor_blue'], scale=scale * 0.26)
        green_texture = arcade.load_texture(img_cfg['color_sensor_green'], scale=scale * 0.26)
        red_texture = arcade.load_texture(img_cfg['color_sensor_red'], scale=scale * 0.26)
        white_texture = arcade.load_texture(img_cfg['color_sensor_white'], scale=scale * 0.26)
        yellow_texture = arcade.load_texture(img_cfg['color_sensor_yellow'], scale=scale * 0.26)

        self.textures.append(black_texture)
        self.textures.append(blue_texture)
        self.textures.append(green_texture)
        self.textures.append(red_texture)
        self.textures.append(white_texture)
        self.textures.append(yellow_texture)

        self.set_texture(0)

    def get_latest_value(self):
        latest_data = self.get_sensed_color()
        self.set_color_texture(latest_data)
        return latest_data

    def get_sensed_color(self) -> int:
        """
        Get the color this ColorSensor is currently 'seeing'.
        :return: integer value representing the color.
        """

        for o in self.sensible_obstacles:
            if o.collided_with(self.center_x, self.center_y):
                return o.color_code

        return self.get_default_value()

    def get_default_value(self):
        """
        1 is the color of black for the real robot. Playing field surface is black.
        :return: integer value representing the color black.
        """
        return 0

    def set_color_texture(self, color):
        converted = COLORS[color]

        if self.old_texture_index != converted:
            self.old_texture_index = converted
            self.set_texture(converted)
