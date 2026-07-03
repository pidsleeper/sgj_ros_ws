#!/usr/bin/env python3
"""
成绩计算服务端 - 演示自定义服务的使用
Grade Calculation Server - Demonstrates custom service usage

运行: ros2 run sgj_pkg grade_server.py
"""

import rclpy
from rclpy.node import Node
from sgj_pkg.srv import CalculateGrade


class GradeServer(Node):
    """提供成绩计算服务的节点"""

    def __init__(self):
        super().__init__('grade_server')
        self.srv = self.create_service(
            CalculateGrade,
            'calculate_grade',
            self.calculate_grade_callback
        )
        self.get_logger().info('成绩计算服务已就绪 (Grade Server ready)')

    def calculate_grade_callback(self, request, response):
        """
        计算平均分并评定等级
        A: 90+, B: 80-89, C: 70-79, D: 60-69, F: <60
        """
        scores = request.scores
        if not scores:
            response.average = 0.0
            response.grade = 'F'
            response.passed = False
            self.get_logger().info('收到空成绩列表，返回不及格')
            return response

        response.average = sum(scores) / len(scores)
        avg = response.average

        if avg >= 90.0:
            response.grade = 'A'
            response.passed = True
        elif avg >= 80.0:
            response.grade = 'B'
            response.passed = True
        elif avg >= 70.0:
            response.grade = 'C'
            response.passed = True
        elif avg >= 60.0:
            response.grade = 'D'
            response.passed = True
        else:
            response.grade = 'F'
            response.passed = False

        self.get_logger().info(
            f'收到请求: scores={scores}, '
            f'返回: average={response.average:.2f}, grade={response.grade}, passed={response.passed}'
        )
        return response


def main(args=None):
    rclpy.init(args=args)
    node = GradeServer()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
