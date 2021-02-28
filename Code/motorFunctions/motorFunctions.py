
import board
from adafruit_motorkit import MotorKit
from adafruit_motor import stepper






class ECEGMotor():
    RATIO = 63.68395
    STEPS_FOR_FULL = 4096

    def __init__(self):
        self.kit = MotorKit(i2c=board.I2C())
        self.stepper = self.kit.stepper1
        self.__find_home()
        self.current_step = 0


    def __find_home(self):
        for i in range(ECEGMotor.STEPS_FOR_FULL):
           self.stepper.onestep()

    def get_current_step(self):
        return self.current_step

    def get_current_degree(self):
        return (self.current_step/ECEGMotor.STEPS_FOR_FULL)*360

    def set_position_degrees(self, pos):

        goal_pos_in_steps = int(((pos/360) * ECEGMotor.STEPS_FOR_FULL)/2)
        steps_to_take = self.current_step - goal_pos_in_steps


        for i in range(abs(steps_to_take)):
            if(steps_to_take < 0):
                self.stepper.onestep(direction = stepper.BACKWARD,style = stepper.DOUBLE)
                self.current_step += 1
            else:
                self.stepper.onestep(style = stepper.DOUBLE)
                self.current_step -= 1

    def reset_position(self):
        for i in range(self.current_step):
            self.stepper.onestep(style = stepper.DOUBLE)
        self.current_step = 0

    #clockwise is positive, ccw is negative
    def move_arm_steps(self, amount):
        for i in range(abs(amount)):
            if(amount < 0):
                if(self.current_step == 4096):
                    return
                self.stepper.onestep(direction = stepper.BACKWARD,style = stepper.DOUBLE)
                self.current_step += 1
            else:
                if(self.current_step == 0):
                    return
                self.stepper.onestep(style = stepper.DOUBLE)
                self.current_step -= 1



myMotor = ECEGMotor()

myMotor.move_arm_steps(-50)

myMotor.set_position_degrees(90)
myMotor.reset_position()

myMotor.set_position_degrees(90)
myMotor.reset_position()
myMotor.set_position_degrees(90)
myMotor.reset_position()
myMotor.stepper.release()