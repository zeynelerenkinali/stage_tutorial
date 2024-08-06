#!/usr/bin/env python3
import rospy
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan   

class ReactiveNavigation():
    def __init__(self):
        self.cmd_vel = Twist()
        self.laser_msg = LaserScan()
        self.robot_stopped = False
        self.obstacle_distance = 100
        self.rospy_sub_laser = rospy.Subscriber("base_scan", LaserScan, self.laser_cb, queue_size=1)
        self.pub_CMD = rospy.Publisher("cmd_vel", Twist, queue_size=1)
        self.rate = rospy.Rate(5)

    def laser_cb(self, msg):
        self.laser_msg = msg

    def calculate_command(self):
        if hasattr(self.laser_msg, 'ranges') and len(self.laser_msg.ranges) > 0:
            self.obstacle_distance = min(self.laser_msg.ranges)

            if self.obstacle_distance > 1.0:
                self.cmd_vel.linear.x = 2.0
                self.cmd_vel.angular.z = 0.0
            else:
                self.cmd_vel.linear.x = 0.0
                self.cmd_vel.angular.z = -2.0

    def run(self):
        while not rospy.is_shutdown():
            self.calculate_command()
            #print(self.cmd_vel)
            self.pub_CMD.publish(self.cmd_vel)
            self.rate.sleep()

if __name__ == "__main__":
    rospy.init_node("reactive_controller_py")
    controller = ReactiveNavigation()
    controller.run()
