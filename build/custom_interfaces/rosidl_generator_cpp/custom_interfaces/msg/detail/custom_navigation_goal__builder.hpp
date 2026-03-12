// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from custom_interfaces:msg/CustomNavigationGoal.idl
// generated code does not contain a copyright notice

#ifndef CUSTOM_INTERFACES__MSG__DETAIL__CUSTOM_NAVIGATION_GOAL__BUILDER_HPP_
#define CUSTOM_INTERFACES__MSG__DETAIL__CUSTOM_NAVIGATION_GOAL__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "custom_interfaces/msg/detail/custom_navigation_goal__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace custom_interfaces
{

namespace msg
{

namespace builder
{

class Init_CustomNavigationGoal_yaw
{
public:
  explicit Init_CustomNavigationGoal_yaw(::custom_interfaces::msg::CustomNavigationGoal & msg)
  : msg_(msg)
  {}
  ::custom_interfaces::msg::CustomNavigationGoal yaw(::custom_interfaces::msg::CustomNavigationGoal::_yaw_type arg)
  {
    msg_.yaw = std::move(arg);
    return std::move(msg_);
  }

private:
  ::custom_interfaces::msg::CustomNavigationGoal msg_;
};

class Init_CustomNavigationGoal_y
{
public:
  explicit Init_CustomNavigationGoal_y(::custom_interfaces::msg::CustomNavigationGoal & msg)
  : msg_(msg)
  {}
  Init_CustomNavigationGoal_yaw y(::custom_interfaces::msg::CustomNavigationGoal::_y_type arg)
  {
    msg_.y = std::move(arg);
    return Init_CustomNavigationGoal_yaw(msg_);
  }

private:
  ::custom_interfaces::msg::CustomNavigationGoal msg_;
};

class Init_CustomNavigationGoal_x
{
public:
  Init_CustomNavigationGoal_x()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_CustomNavigationGoal_y x(::custom_interfaces::msg::CustomNavigationGoal::_x_type arg)
  {
    msg_.x = std::move(arg);
    return Init_CustomNavigationGoal_y(msg_);
  }

private:
  ::custom_interfaces::msg::CustomNavigationGoal msg_;
};

}  // namespace builder

}  // namespace msg

template<typename MessageType>
auto build();

template<>
inline
auto build<::custom_interfaces::msg::CustomNavigationGoal>()
{
  return custom_interfaces::msg::builder::Init_CustomNavigationGoal_x();
}

}  // namespace custom_interfaces

#endif  // CUSTOM_INTERFACES__MSG__DETAIL__CUSTOM_NAVIGATION_GOAL__BUILDER_HPP_
