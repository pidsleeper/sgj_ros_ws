#!/usr/bin/env python3
"""
机器人移动动作服务端 - 演示自定义动作的使用
Robot Movement Action Server - Demonstrates custom action usage

运行: ros2 run sgj_pkg move_robot_server.py
"""

import math
import time
import rclpy
from rclpy.node import Node
from rclpy.action import ActionServer, GoalResponse, CancelResponse
from sgj_pkg.action import MoveRobot


class MoveRobotServer(Node):
    """提供机器人导航动作服务的节点"""

    def __init__(self):
        super().__init__('move_robot_server')
        self.action_server = ActionServer(
            self,
            MoveRobot,
            'move_robot',
            execute_callback=self.execute_callback,
            goal_callback=self.goal_callback,
            cancel_callback=self.cancel_callback,
            handle_accepted_callback=self.handle_accepted_callback,
        )
        self.get_logger().info('机器人移动动作服务已就绪 (MoveRobot Action Server ready)')

    def goal_callback(self, goal_request):
        """接收目标时回调 - 验证目标是否合法"""
        self.get_logger().info(f'收到目标请求: target_x={goal_request.target_x}, target_y={goal_request.target_y}')
        # 假设有效范围是 0-100
        if 0.0 <= goal_request.target_x <= 100.0 and 0.0 <= goal_request.target_y <= 100.0:
            self.get_logger().info('目标验证通过，接受')
            return GoalResponse.ACCEPT
        else:
            self.get_logger().warn('目标超出范围，拒绝')
            return GoalResponse.REJECT

    def cancel_callback(self, goal_handle):
        """取消请求时回调"""
        self.get_logger().info('收到取消请求')
        return CancelResponse.ACCEPT

    def handle_accepted_callback(self, goal_handle):
        """目标被接受后在新线程中执行"""
        self.get_logger().info('目标已接受，开始执行...')
        goal_handle.execute()

    def execute_callback(self, goal_handle):
        """
        执行机器人移动动作（模拟）
        从原点移动到目标位置，持续发送反馈
        """
        target_x = goal_handle.request.target_x
        target_y = goal_handle.request.target_y

        self.get_logger().info(f'开始执行: 移动到 ({target_x}, {target_y})')

        # 模拟移动参数
        current_x = 0.0
        current_y = 0.0
        step_size = 5.0  # 每步移动距离
        step_time = 0.3  # 每步耗时(秒)
        start_time = time.time()

        # 目标距离
        total_distance = math.sqrt(target_x ** 2 + target_y ** 2)

        feedback_msg = MoveRobot.Feedback()

        while rclpy.ok():
            # 计算剩余距离
            dx = target_x - current_x
            dy = target_y - current_y
            dist_remaining = math.sqrt(dx ** 2 + dy ** 2)

            # 到达目标
            if dist_remaining < step_size:
                current_x = target_x
                current_y = target_y
                feedback_msg.current_x = current_x
                feedback_msg.current_y = current_y
                feedback_msg.distance_remaining = 0.0
                goal_handle.publish_feedback(feedback_msg)
                self.get_logger().info(f'到达目的地! ({current_x:.1f}, {current_y:.1f})')
                break

            # 检查是否被取消
            if goal_handle.is_cancel_requested:
                self.get_logger().info('动作被取消')
                goal_handle.canceled()
                result = MoveRobot.Result()
                result.final_x = current_x
                result.final_y = current_y
                result.elapsed = time.time() - start_time
                return result

            # 移动一步
            current_x += step_size * dx / dist_remaining
            current_y += step_size * dy / dist_remaining

            # 发布反馈
            feedback_msg.current_x = current_x
            feedback_msg.current_y = current_y
            feedback_msg.distance_remaining = dist_remaining
            goal_handle.publish_feedback(feedback_msg)

            self.get_logger().info(
                f'移动中... 当前位置: ({current_x:.1f}, {current_y:.1f}), '
                f'剩余距离: {dist_remaining:.1f}'
            )
            time.sleep(step_time)

        # 动作成功完成
        goal_handle.succeed()
        result = MoveRobot.Result()
        result.final_x = current_x
        result.final_y = current_y
        result.elapsed = time.time() - start_time
        self.get_logger().info(
            f'移动完成! 最终位置: ({result.final_x:.1f}, {result.final_y:.1f}), '
            f'耗时: {result.elapsed:.2f}s'
        )
        return result


def main(args=None):
    rclpy.init(args=args)
    node = MoveRobotServer()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
