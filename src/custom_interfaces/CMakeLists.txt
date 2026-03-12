cmake_minimum_required(VERSION 3.8)
project(custom_interfaces)

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

# find dependencies
find_package(ament_cmake REQUIRED)

# self added dependencies
find_package(rosidl_default_generators REQUIRED)

# installing custom interfaces
rosidl_generate_interfaces(${PROJECT_NAME}
  "srv/ChangeFaceState.srv"
  "msg/TOFSensorData.msg"
  "msg/DetectedPersonFrameOffset.msg"
  "msg/IMUData.msg"
  "msg/DetectedVoiceCommand.msg"
  "msg/MoveRobotCommand.msg"
  "msg/CustomNavigationGoal.msg"
  "srv/SetCustomNavigationGoal.srv"
)

ament_package()