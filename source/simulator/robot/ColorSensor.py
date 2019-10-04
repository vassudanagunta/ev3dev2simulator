import arcade

from simulator.robot import Robot
from source.simulator.robot.BodyPart import BodyPart


class ColorSensor(BodyPart):
    """
    Class representing a ColorSensor of the simulated robot.
    """


    def __init__(self,
                 address: str,
                 img_cfg,
                 robot: Robot,
                 delta_x: int,
                 delta_y: int):
        super(ColorSensor, self).__init__(address,
                                          img_cfg['color_sensor'],
                                          0.18,
                                          robot,
                                          delta_x,
                                          delta_y)

        blue_texture = arcade.load_texture(img_cfg['color_sensor_blue'], scale=0.25)
        green_texture = arcade.load_texture(img_cfg['color_sensor_green'], scale=0.25)
        red_texture = arcade.load_texture(img_cfg['color_sensor_red'], scale=0.25)

        self.textures = []
        self.textures.append(blue_texture)
        self.textures.append(green_texture)
        self.textures.append(red_texture)
        self.cur_texture_index = 3


    def get_sensed_color(self) -> int:

        for o in self.sensible_obstacles:
            if o.collided_with(self.center_x, self.center_y):
                return o.color_code

        return 0
