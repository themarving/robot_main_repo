// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from custom_interfaces:msg/MoveRobotCommand.idl
// generated code does not contain a copyright notice

#ifndef CUSTOM_INTERFACES__MSG__DETAIL__MOVE_ROBOT_COMMAND__BUILDER_HPP_
#define CUSTOM_INTERFACES__MSG__DETAIL__MOVE_ROBOT_COMMAND__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "custom_interfaces/msg/detail/move_robot_command__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace custom_interfaces
{

namespace msg
{

namespace builder
{

class Init_MoveRobotCommand_goal_angle
{
public:
  explicit Init_MoveRobotCommand_goal_angle(::custom_interfaces::msg::MoveRobotCommand & msg)
  : msg_(msg)
  {}
  ::custom_interfaces::msg::MoveRobotCommand goal_angle(::custom_interfaces::msg::MoveRobotCommand::_goal_angle_type arg)
  {
    msg_.goal_angle = std::move(arg);
    return std::move(msg_);
  }

private:
  ::custom_interfaces::msg::MoveRobotCommand msg_;
};

class Init_MoveRobotCommand_command
{
public:
  Init_MoveRobotCommand_command()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_MoveRobotCommand_goal_angle command(::custom_interfaces::msg::MoveRobotCommand::_command_type arg)
  {
    msg_.command = std::move(arg);
    return Init_MoveRobotCommand_goal_angle(msg_);
  }

private:
  ::custom_interfaces::msg::MoveRobotCommand msg_;
};

}  // namespace builder

}  // namespace msg

template<typename MessageType>
auto build();

template<>
inline
auto build<::custom_interfaces::msg::MoveRobotCommand>()
{
  return custom_interfaces::msg::builder::Init_MoveRobotCommand_command();
}

}  // namespace custom_interfaces

#endif  // CUSTOM_INTERFACES__MSG__DETAIL__MOVE_ROBOT_COMMAND__BUILDER_HPP_
