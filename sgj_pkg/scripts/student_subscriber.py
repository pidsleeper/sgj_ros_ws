#!/usr/bin/env python3
"""
学生信息订阅者 - 演示接收自定义消息
Student Info Subscriber - Demonstrates receiving custom messages

运行: ros2 run sgj_pkg student_subscriber.py
"""

import rclpy
from rclpy.node import Node
from sgj_pkg.msg import Student


class StudentSubscriber(Node):
    """订阅学生信息消息的节点"""

    def __init__(self):
        super().__init__('student_subscriber')
        self.subscription = self.create_subscription(
            Student,
            'student_info',
            self.callback,
            10
        )
        self.get_logger().info('学生信息订阅者已启动 (Student Subscriber started)')

    def callback(self, msg: Student):
        """接收并处理学生信息"""
        avg_score = sum(msg.scores) / len(msg.scores) if msg.scores else 0.0
        self.get_logger().info(
            f'收到学生: {msg.name}, 年龄: {msg.age}, '
            f'专业: {msg.major}, 平均分: {avg_score:.2f}'
        )


def main(args=None):
    rclpy.init(args=args)
    node = StudentSubscriber()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
