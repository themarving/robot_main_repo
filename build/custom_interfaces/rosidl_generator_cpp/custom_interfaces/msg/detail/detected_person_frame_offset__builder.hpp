// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from custom_interfaces:msg/DetectedPersonFrameOffset.idl
// generated code does not contain a copyright notice

#ifndef CUSTOM_INTERFACES__MSG__DETAIL__DETECTED_PERSON_FRAME_OFFSET__BUILDER_HPP_
#define CUSTOM_INTERFACES__MSG__DETAIL__DETECTED_PERSON_FRAME_OFFSET__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "custom_interfaces/msg/detail/detected_person_frame_offset__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace custom_interfaces
{

namespace msg
{

namespace builder
{

class Init_DetectedPersonFrameOffset_y_offset
{
public:
  explicit Init_DetectedPersonFrameOffset_y_offset(::custom_interfaces::msg::DetectedPersonFrameOffset & msg)
  : msg_(msg)
  {}
  ::custom_interfaces::msg::DetectedPersonFrameOffset y_offset(::custom_interfaces::msg::DetectedPersonFrameOffset::_y_offset_type arg)
  {
    msg_.y_offset = std::move(arg);
    return std::move(msg_);
  }

private:
  ::custom_interfaces::msg::DetectedPersonFrameOffset msg_;
};

class Init_DetectedPersonFrameOffset_x_offset
{
public:
  Init_DetectedPersonFrameOffset_x_offset()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_DetectedPersonFrameOffset_y_offset x_offset(::custom_interfaces::msg::DetectedPersonFrameOffset::_x_offset_type arg)
  {
    msg_.x_offset = std::move(arg);
    return Init_DetectedPersonFrameOffset_y_offset(msg_);
  }

private:
  ::custom_interfaces::msg::DetectedPersonFrameOffset msg_;
};

}  // namespace builder

}  // namespace msg

template<typename MessageType>
auto build();

template<>
inline
auto build<::custom_interfaces::msg::DetectedPersonFrameOffset>()
{
  return custom_interfaces::msg::builder::Init_DetectedPersonFrameOffset_x_offset();
}

}  // namespace custom_interfaces

#endif  // CUSTOM_INTERFACES__MSG__DETAIL__DETECTED_PERSON_FRAME_OFFSET__BUILDER_HPP_
