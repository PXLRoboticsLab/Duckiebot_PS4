import pyglet
import rospy
import sys, signal

from sensor_msgs.msg import Joy

DEBUG = False

class PS4Controller:
    DRIVE_FWD_BUTTON = 5 # R1
    DRIVE_BWD_BUTTON = 4 # L1
    TURN_SMOOTH = 0.4
    INTERVAL = 0.1

    def __init__(self, duckiebot):
        self.pub = rospy.Publisher("/%s/joy" % duckiebot, Joy, queue_size=1)
        self.vx = 0
        self.vy = 0

    def on_joyaxis_motion(self, joystick, axis, value):
        if DEBUG:
            print("Joystick move %s %s" % (str(axis), str(value)))

        if axis == "x": # horizontal
            self.vy = -value*self.TURN_SMOOTH if abs(value) > 0.1 else 0
            if self.vx == -1: # driving backwards
                self.vy *= -1

    def on_joybutton_press(self, joystick, button):
        if DEBUG:
            print("Press " + str(button))

        if button == self.DRIVE_FWD_BUTTON:
            self.vx = 1
        elif self.vx == 0 and button == self.DRIVE_BWD_BUTTON:
            self.vx = -1

    def on_joybutton_release(self, joystick, button): # left joystick
        if DEBUG:
            print("Release " + str(button))

        if button == self.DRIVE_FWD_BUTTON or button == self.DRIVE_BWD_BUTTON:
            self.vx = 0

    def update(self, dt):	
        msg = Joy()
        msg.axes = [0.0, self.vx, 0.0, self.vy, 0.0, 0.0, 0.0, 0.0]
        self.pub.publish(msg)

def on_close(sig, frame):
    print("Shutting down")
    stop_message = Joy()
    stop_message.axes = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
    pyglet.app.exit()
    sys.exit()

if __name__ == "__main__":
    rospy.init_node('duckieps4', anonymous=True)
    signal.signal(signal.SIGINT, on_close)
    duckie = "emil" if len(sys.argv) <= 1 else str(sys.argv[1]) # TODO catch error on no argument
    controller = PS4Controller(duckie)
    pyglet.clock.schedule_interval(controller.update, controller.INTERVAL)

    joysticks = pyglet.input.get_joysticks()
    if joysticks:
        joystick = joysticks[0]
    joystick.open()
    joystick.push_handlers(controller)

    print("Waiting for input...")

    pyglet.app.run()
    rospy.spin()