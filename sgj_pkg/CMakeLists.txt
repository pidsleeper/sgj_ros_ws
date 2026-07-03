cmake_minimum_required(VERSION 3.8)
project(sgj_pkg)

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

# find dependencies
find_package(ament_cmake REQUIRED)
find_package(rclcpp REQUIRED)
find_package(rclpy REQUIRED)
find_package(std_msgs REQUIRED)
find_package(action_msgs REQUIRED)
find_package(rosidl_default_generators REQUIRED)

# 生成自定义消息、服务、动作的代码
rosidl_generate_interfaces(${PROJECT_NAME}
  "msg/Student.msg"
  "srv/CalculateGrade.srv"
  "action/MoveRobot.action"
  DEPENDENCIES std_msgs action_msgs
)

# 安装 Python 模块
install(DIRECTORY
  sgj_pkg
  DESTINATION share/${PROJECT_NAME}
)

# 安装可执行脚本
install(PROGRAMS
  scripts/student_publisher.py
  scripts/student_subscriber.py
  scripts/grade_server.py
  scripts/grade_client.py
  scripts/move_robot_server.py
  scripts/move_robot_client.py
  DESTINATION lib/${PROJECT_NAME}
)

if(BUILD_TESTING)
  find_package(ament_lint_auto REQUIRED)
  set(ament_cmake_copyright_FOUND TRUE)
  set(ament_cmake_cpplint_FOUND TRUE)
  ament_lint_auto_find_test_dependencies()
endif()

ament_package()
