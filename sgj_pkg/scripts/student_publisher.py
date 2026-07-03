#!/usr/bin/env python3
"""
学生信息发布者 - 演示自定义消息的使用
Student Info Publisher - Demonstrates custom message usage

运行: ros2 run sgj_pkg student_publisher.py
"""

import rclpy
from rclpy.node import Node
from sgj_pkg.msg import Student


class StudentPublisher(Node):
    """发布学生信息消息的节点"""

    def __init__(self):
        super().__init__('student_publisher')
        self.publisher_ = self.create_publisher(Student, 'student_info', 10)
        self.timer = self.create_timer(1.0, self.timer_callback)
        self.count = 0
        self.get_logger().info('学生信息发布者已启动 (Student Publisher started)')

    def timer_callback(self):
        """定时发布学生信息"""
        msg = Student()
        msg.name = f'张三_{self.count}'
        msg.age = 20 + (self.count % 3)
        msg.scores = [85.5 + self.count, 90.0 + self.count * 0.5, 78.0 + self.count]
        msg.major = '机器人工程'
        self.publisher_.publish(msg)
        self.get_logger().info(f'发布: name={msg.name}, age={msg.age}, scores={msg.scores}, major={msg.major}')
        self.count += 1


def main(args=None):
    rclpy.init(args=args)
    node = StudentPublisher()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
