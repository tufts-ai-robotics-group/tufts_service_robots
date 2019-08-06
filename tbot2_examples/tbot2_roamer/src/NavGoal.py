#!/usr/bin/env python
import rospy
import numpy as np
import tf
import math
import geometry_msgs.msg
from geometry_msgs.msg import Point
from visualization_msgs.msg import Marker
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
import actionlib
from actionlib_msgs.msg import *


class NavGoal(object):
    def __init__(self):

        self.path = Marker()
        rospy.init_node('echoer')
        # subscribe to "/move_base_simple/goal" topic to pick location using 2D Nav Goal in rviz
        rospy.Subscriber("/move_base_simple/goal", geometry_msgs.msg.PoseStamped, self.get_way_point)

        # displays path in rviz
        self.publisher = rospy.Publisher('visualization_marker', Marker, queue_size=10)

        # actionlib creates servers that execute long-running goals that can be preempted.
        # It also provides a client interface in order to send requests to the server.
        self.move_base = actionlib.SimpleActionClient("move_base", MoveBaseAction)

        self.move_base.wait_for_server(rospy.Duration(10))

    # fetch clicked way points
    def get_way_point(self, msg):

        # print picked way points in terminal
        # print msg.pose.position.x, msg.pose.position.y
        # get orientationn and convert quternion to euler (roll pitch yaw)
        # returns coordinates in string array
        quaternion = (
            msg.pose.orientation.x,
            msg.pose.orientation.y,
            msg.pose.orientation.z,
            msg.pose.orientation.w)

        # euler angles
        euler = tf.transformations.euler_from_quaternion(quaternion)
        yaw = math.degrees(euler[2])
        print
        "Going to location: X ", msg.pose.position.x, " Y ", msg.pose.position.y, " Yaw ", yaw, "degrees"

        coordinates = (str(msg.pose.position.x), str(msg.pose.position.y), str(yaw))
        print
        coordinates
        return coordinates

    def move(self, coordinates):
        s = coordinates
        x = float(s[0])
        y = float(s[1])
        z = float(s[2])

        self.goal_sent = True
        goal = MoveBaseGoal()
        # uses the map that is already on rviz (halligan 2nd floor)
        goal.target_pose.header.frame_id = 'map'
        goal.target_pose.header.stamp = rospy.Time.now()
        goal.target_pose.pose.position.x = x
        goal.target_pose.pose.position.y = y
        goal.target_pose.pose.position.z = z

        quat = tf.transformations.quaternion_from_euler(0, 0, 0)
        goal.target_pose.pose.orientation.x = quat[0]
        goal.target_pose.pose.orientation.y = quat[1]
        goal.target_pose.pose.orientation.z = quat[2]
        goal.target_pose.pose.orientation.w = quat[3]

        success = self.move_base.send_goal(goal)

        the_state = self.move_base.get_state()

        result = False

        # defines what sucess is and stops the robot once it reaches the goal
        # this part does not currently work. Working on fix.
        if success and the_state == GoalStatus.SUCCEEDED:
            result = True

        else:
            self.move_base.cancel_goal()

            self.goal_sent = False

        if result:
            rospy.loginfo("Yay")
        else:
            rospy.loginfo("FAILED")

    rospy.sleep(1)

    # display way points on the map
    # keeps node from exiting until it is stopped
    def run(self):
        rospy.spin()


if __name__ == '__main__':
    try:
        print
        "*********** Pick a destination ***********"
        NavGoal().run()

    except rospy.ROSInterruptException:
        rospy.loginfo("Quitting")
