from ev3dev2simulator.config.config import get_simulation_settings
from ev3dev2simulator.robot.BodyPart import BodyPart


class Wheel(BodyPart):
    """
    Class representing a Wheel of the simulated robot.
    """

    def __init__(self,
                 brick: int,
                 address: str,
                 robot,
                 delta_x: int,
                 delta_y: int):
        dims = get_simulation_settings()['body_part_sizes']['wheel']
        super(Wheel, self).__init__(brick, address, robot, delta_x, delta_y, dims['width'], dims['height'], 'motor')
        self.x_offset = delta_x
        self.y_offset = delta_y

    def setup_visuals(self, scale, body):
        vis_conf = get_simulation_settings()
        self.init_sprite(vis_conf['image_paths']['wheel'], scale, body)

    def is_falling(self) -> bool:
        """
        Check if this Wheel is 'falling' of the playing field.
        :return: boolean value representing the outcome.
        """
        # for o in self.sensible_obstacles:
        #     if o.collided_with(self.center_x, self.center_y):
        #         return True

        return self.get_default_value()

    def get_default_value(self):
        return False
