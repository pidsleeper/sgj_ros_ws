#!/usr/bin/env python3
"""
机器人移动动作客户端 - 发送导航目标并接收反馈
Robot Movement Action Client - Sends navigation goal and receives feedback

运行: ros2 run sgj_pkg move_robot_client.py [target_x] [target_y]
示例: ros2 run sgj_pkg move_robot_client.py 30 40
"""

import sys
import rclpy
from rclpy.node import Node
from rclpy.action import ActionClient
from sgj_pkg.action import MoveRobot


class MoveRobotClient(Node):
    """发送机器人移动动作目标的客户端节点"""

    def __init__(self):
        super().__init__('move_robot_client')
        self.action_client = ActionClient(self, MoveRobot, 'move_robot')
        self.get_logger().info('机器人移动客户端已启动 (MoveRobot Client started)')

    def send_goal(self, target_x, target_y):
        """发送导航目标"""
        goal_msg = MoveRobot.Goal()
        goal_msg.target_x = target_x
        goal_msg.target_y = target_y

        self.get_logger().info('等待动作服务器上线...')
        self.action_client.wait_for_server()

        self.get_logger().info(f'发送目标: target_x={target_x}, target_y={target_y}')

        send_goal_future = self.action_client.send_goal_async(
            goal_msg,
            feedback_callback=self.feedback_callback
        )
        send_goal_future.add_done_callback(self.goal_response_callback)

    def goal_response_callback(self, future):
        """目标响应回调"""
        goal_handle = future.result()
        if not goal_handle.accepted:
            self.get_logger().error('目标被服务器拒绝!')
            rclpy.shutdown()
            return

        self.get_logger().info('目标已接受，等待结果...')
        get_result_future = goal_handle.get_result_async()
        get_result_future.add_done_callback(self.result_callback)

    def feedback_callback(self, feedback_msg):
        """处理动作反馈"""
        fb = feedback_msg.feedback
        self.get_logger().info(
            f'反馈: 当前位置=({fb.current_x:.1f}, {fb.current_y:.1f}), '
            f'剩余距离={fb.distance_remaining:.1f}'
        )

    def result_callback(self, future):
        """处理动作结果"""
        result = future.result().result
        self.get_logger().info(
            f'===== 移动结果 =====\n'
            f'  最终位置: ({result.final_x:.1f}, {result.final_y:.1f})\n'
            f'  耗时:     {result.elapsed:.2f}s'
        )
        rclpy.shutdown()


def main(args=None):
    rclpy.init(args=args)

    target_x = float(sys.argv[1]) if len(sys.argv) > 1 else 30.0
    target_y = float(sys.argv[2]) if len(sys.argv) > 2 else 40.0

    client = MoveRobotClient()
    client.send_goal(target_x, target_y)
    rclpy.spin(client)


if __name__ == '__main__':
    main()
