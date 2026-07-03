#!/usr/bin/env python3
"""
成绩计算客户端 - 请求成绩计算服务
Grade Calculation Client - Requests grade calculation service

运行: ros2 run sgj_pkg grade_client.py [成绩列表]
示例: ros2 run sgj_pkg grade_client.py 85 92 78 65
"""

import sys
import rclpy
from rclpy.node import Node
from sgj_pkg.srv import CalculateGrade


class GradeClient(Node):
    """请求成绩计算服务的客户端节点"""

    def __init__(self):
        super().__init__('grade_client')
        self.cli = self.create_client(CalculateGrade, 'calculate_grade')
        while not self.cli.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('等待成绩计算服务上线...')
        self.get_logger().info('已连接到成绩计算服务')

    def send_request(self, scores):
        """发送成绩计算请求"""
        req = CalculateGrade.Request()
        req.scores = scores
        self.future = self.cli.call_async(req)
        return self.future


def main(args=None):
    rclpy.init(args=args)
    client = GradeClient()

    # 从命令行参数读取成绩，默认值用于演示
    if len(sys.argv) > 1:
        scores = [float(arg) for arg in sys.argv[1:]]
    else:
        scores = [85.0, 92.0, 78.0, 65.0]
        client.get_logger().info(f'未提供参数，使用默认成绩: {scores}')

    future = client.send_request(scores)

    # 等待结果
    rclpy.spin_until_future_complete(client, future)
    response = future.result()

    if response is not None:
        client.get_logger().info(
            f'===== 成绩计算结果 =====\n'
            f'  各科成绩: {scores}\n'
            f'  平均分:   {response.average:.2f}\n'
            f'  等级:     {response.grade}\n'
            f'  是否及格: {"是" if response.passed else "否"}'
        )
    else:
        client.get_logger().error('服务调用失败!')

    client.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
