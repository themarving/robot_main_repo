// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from custom_interfaces:msg/DetectedVoiceCommand.idl
// generated code does not contain a copyright notice

#ifndef CUSTOM_INTERFACES__MSG__DETAIL__DETECTED_VOICE_COMMAND__BUILDER_HPP_
#define CUSTOM_INTERFACES__MSG__DETAIL__DETECTED_VOICE_COMMAND__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "custom_interfaces/msg/detail/detected_voice_command__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace custom_interfaces
{

namespace msg
{

namespace builder
{

class Init_DetectedVoiceCommand_command
{
public:
  explicit Init_DetectedVoiceCommand_command(::custom_interfaces::msg::DetectedVoiceCommand & msg)
  : msg_(msg)
  {}
  ::custom_interfaces::msg::DetectedVoiceCommand command(::custom_interfaces::msg::DetectedVoiceCommand::_command_type arg)
  {
    msg_.command = std::move(arg);
    return std::move(msg_);
  }

private:
  ::custom_interfaces::msg::DetectedVoiceCommand msg_;
};

class Init_DetectedVoiceCommand_command_direction
{
public:
  Init_DetectedVoiceCommand_command_direction()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_DetectedVoiceCommand_command command_direction(::custom_interfaces::msg::DetectedVoiceCommand::_command_direction_type arg)
  {
    msg_.command_direction = std::move(arg);
    return Init_DetectedVoiceCommand_command(msg_);
  }

private:
  ::custom_interfaces::msg::DetectedVoiceCommand msg_;
};

}  // namespace builder

}  // namespace msg

template<typename MessageType>
auto build();

template<>
inline
auto build<::custom_interfaces::msg::DetectedVoiceCommand>()
{
  return custom_interfaces::msg::builder::Init_DetectedVoiceCommand_command_direction();
}

}  // namespace custom_interfaces

#endif  // CUSTOM_INTERFACES__MSG__DETAIL__DETECTED_VOICE_COMMAND__BUILDER_HPP_
