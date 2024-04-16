# Copyright (c) 2024, RoboVerse community
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice, this
#    list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the documentation
#    and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

import asyncio


from rclpy.node import Node
from rclpy.qos import QoSProfile
from sensor_msgs.msg import JointState
from geometry_msgs.msg import TransformStamped
from tf2_ros import TransformBroadcaster


class RobotBaseNode(Node):
    def __init__(self):
        super().__init__('go2_driver_node')
        qos_profile = QoSProfile(depth=10)
        self.joint_pub = self.create_publisher(JointState, 'joint_states', qos_profile)
        self.broadcaster = TransformBroadcaster(self, qos=qos_profile)

    def publish_joints(self, joint_names_lst, joint_state_lst):
        # Create message
        joint_state = JointState()
        joint_state.header.stamp = self.get_clock().now().to_msg()
        
        joint_state.name = joint_names_lst
        
        joint_state.position = [
            joint_state_lst[0].item(), joint_state_lst[1].item(), joint_state_lst[2].item(),
            joint_state_lst[3].item(), joint_state_lst[4].item(), joint_state_lst[5].item(),
            joint_state_lst[6].item(), joint_state_lst[7].item(), joint_state_lst[8].item(),
            joint_state_lst[9].item(), joint_state_lst[10].item(), joint_state_lst[11].item(),
            ]

        self.joint_pub.publish(joint_state)

    def publish_odom(self, base_pos, base_rot):

        odom_trans = TransformStamped()
        odom_trans.header.stamp = self.get_clock().now().to_msg()
        odom_trans.header.frame_id = 'odom'
        odom_trans.child_frame_id = 'base_link'
        odom_trans.transform.translation.x = base_pos[0].item()
        odom_trans.transform.translation.y = base_pos[1].item()
        odom_trans.transform.translation.z = base_pos[2].item() + 0.07
        odom_trans.transform.rotation.x = base_rot[1].item()
        odom_trans.transform.rotation.y = base_rot[2].item()
        odom_trans.transform.rotation.z = base_rot[3].item()
        odom_trans.transform.rotation.w = base_rot[0].item()
        self.broadcaster.sendTransform(odom_trans)

    async def run(self):
        while True:
            self.publish_lidar()
            await asyncio.sleep(0.1)