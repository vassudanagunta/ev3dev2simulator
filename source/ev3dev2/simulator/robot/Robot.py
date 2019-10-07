import math

from arcade import Sprite

from ev3dev2.simulator.obstacle import ColorObstacle
from ev3dev2.simulator.robot import BodyPart
from ev3dev2.simulator.robot.Body import Body
from ev3dev2.simulator.robot.ColorSensor import ColorSensor
from ev3dev2.simulator.robot.TouchSensor import TouchSensor
from ev3dev2.simulator.robot.UltrasonicSensor import UltrasonicSensor
from ev3dev2.simulator.robot.Wheel import Wheel
from ev3dev2.simulator.util.Util import apply_scaling, calc_differential_steering_angle_x_y


class Robot:
    """
    Class representing the simulated robot. This robot has a number
    of parts defined by BodyParts and ExtraBodyParts.
    """


    def __init__(self, cfg, center_x: int, center_y: int, orientation: int):

        self.wheel_center_x = center_x
        self.wheel_center_y = center_y + apply_scaling(22.5)

        img_cfg = cfg['image_paths']
        alloc_cfg = cfg['alloc_settings']

        address_left_motor = alloc_cfg['motor']['left']
        address_right_motor = alloc_cfg['motor']['right']
        address_center_cs = alloc_cfg['color_sensor']['center']
        address_left_cs = alloc_cfg['color_sensor']['left']
        address_right_cs = alloc_cfg['color_sensor']['right']
        address_left_ts = alloc_cfg['touch_sensor']['left']
        address_right_ts = alloc_cfg['touch_sensor']['right']
        address_us = alloc_cfg['ultrasonic_sensor']['top']

        self.wheel_distance = apply_scaling(cfg['wheel_settings']['spacing'])

        self.body = Body(img_cfg, self, 0, apply_scaling(-22.5))
        self.left_wheel = Wheel(address_left_motor, img_cfg, self, (self.wheel_distance / -2), 0.01)
        self.right_wheel = Wheel(address_right_motor, img_cfg, self, (self.wheel_distance / 2), 0.01)

        self.center_color_sensor = ColorSensor(address_center_cs, img_cfg, self, 0, apply_scaling(81))
        # self.left_color_sensor = ColorSensor(address_left_cs, img_cfg, self, -45, apply_scaling(55))
        # self.right_color_sensor = ColorSensor(address_right_cs, img_cfg, self, 45, apply_scaling(55))

        self.left_touch_sensor = TouchSensor(address_left_ts, img_cfg, self, apply_scaling(-75), apply_scaling(102), True)
        self.right_touch_sensor = TouchSensor(address_right_ts, img_cfg, self, apply_scaling(75), apply_scaling(102), False)

        self.ultrasonic_sensor = UltrasonicSensor(address_us, img_cfg, self, 0, apply_scaling(-91.5))

        self.sprites = [self.body,
                        self.left_wheel,
                        self.right_wheel,
                        self.center_color_sensor,
                        # self.left_color_sensor,
                        # self.right_color_sensor,
                        self.left_touch_sensor,
                        self.right_touch_sensor,
                        self.ultrasonic_sensor]

        if orientation != 0:
            self._rotate(math.radians(orientation))


    def _move_x(self, distance: float):
        """
        Move all parts of this robot by the given distance in the x-direction.
        :param distance: to move
        """

        for s in self.get_sprites():
            s.move_x(distance)


    def _move_y(self, distance: float):
        """
        Move all parts of this robot by the given distance in the y-direction.
        :param distance: to move
        """

        for s in self.get_sprites():
            s.move_y(distance)


    def _rotate(self, radians: float):
        """
        Rotate all parts of this robot by the given angle in radians.
        :param radians to rotate
        """
        for s in self.get_sprites():
            s.rotate(radians)


    def execute_movement(self, left_ppf: float, right_ppf: float):
        """
        Move the robot and its parts by providing the speed of the left and right motor
        using the differential steering principle.
        :param left_ppf: speed in pixels per second of the left motor.
        :param right_ppf: speed in pixels per second of the right motor.
        """

        distance_left = left_ppf if left_ppf is not None else 0
        distance_right = right_ppf if right_ppf is not None else 0

        cur_angle = math.radians(self.body.angle + 90)

        diff_angle, diff_x, diff_y = \
            calc_differential_steering_angle_x_y(self.wheel_distance,
                                                 distance_left,
                                                 distance_right,
                                                 cur_angle)

        self.wheel_center_x += diff_x
        self.wheel_center_y += diff_y

        self._rotate(diff_angle)
        self._move_x(diff_x)
        self._move_y(diff_y)


    def set_color_obstacles(self, obstacles: [ColorObstacle]):
        """
        Set the obstacles which can be detected by the color sensors of this robot.
        :param obstacles: to be detected.
        """

        self.center_color_sensor.set_sensible_obstacles(obstacles)
        # self.left_color_sensor.set_sensible_obstacles(obstacles)
        # self.right_color_sensor.set_sensible_obstacles(obstacles)


    def set_touch_obstacles(self, obstacles):
        """
        Set the obstacles which can be detected by the touch sensors of this robot.
        :param obstacles: to be detected.
        """

        self.left_touch_sensor.set_sensible_obstacles(obstacles)
        self.right_touch_sensor.set_sensible_obstacles(obstacles)


    def get_sprites(self) -> [Sprite]:
        return self.sprites


    def get_sensors(self) -> [BodyPart]:
        return [self.center_color_sensor,
                self.right_touch_sensor,
                self.left_touch_sensor,
                self.ultrasonic_sensor]
