// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from custom_interfaces:srv/SetCustomNavigationGoal.idl
// generated code does not contain a copyright notice

#ifndef CUSTOM_INTERFACES__SRV__DETAIL__SET_CUSTOM_NAVIGATION_GOAL__BUILDER_HPP_
#define CUSTOM_INTERFACES__SRV__DETAIL__SET_CUSTOM_NAVIGATION_GOAL__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "custom_interfaces/srv/detail/set_custom_navigation_goal__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace custom_interfaces
{

namespace srv
{

namespace builder
{

class Init_SetCustomNavigationGoal_Request_yaw
{
public:
  explicit Init_SetCustomNavigationGoal_Request_yaw(::custom_interfaces::srv::SetCustomNavigationGoal_Request & msg)
  : msg_(msg)
  {}
  ::custom_interfaces::srv::SetCustomNavigationGoal_Request yaw(::custom_interfaces::srv::SetCustomNavigationGoal_Request::_yaw_type arg)
  {
    msg_.yaw = std::move(arg);
    return std::move(msg_);
  }

private:
  ::custom_interfaces::srv::SetCustomNavigationGoal_Request msg_;
};

class Init_SetCustomNavigationGoal_Request_y
{
public:
  explicit Init_SetCustomNavigationGoal_Request_y(::custom_interfaces::srv::SetCustomNavigationGoal_Request & msg)
  : msg_(msg)
  {}
  Init_SetCustomNavigationGoal_Request_yaw y(::custom_interfaces::srv::SetCustomNavigationGoal_Request::_y_type arg)
  {
    msg_.y = std::move(arg);
    return Init_SetCustomNavigationGoal_Request_yaw(msg_);
  }

private:
  ::custom_interfaces::srv::SetCustomNavigationGoal_Request msg_;
};

class Init_SetCustomNavigationGoal_Request_x
{
public:
  Init_SetCustomNavigationGoal_Request_x()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_SetCustomNavigationGoal_Request_y x(::custom_interfaces::srv::SetCustomNavigationGoal_Request::_x_type arg)
  {
    msg_.x = std::move(arg);
    return Init_SetCustomNavigationGoal_Request_y(msg_);
  }

private:
  ::custom_interfaces::srv::SetCustomNavigationGoal_Request msg_;
};

}  // namespace builder

}  // namespace srv

template<typename MessageType>
auto build();

template<>
inline
auto build<::custom_interfaces::srv::SetCustomNavigationGoal_Request>()
{
  return custom_interfaces::srv::builder::Init_SetCustomNavigationGoal_Request_x();
}

}  // namespace custom_interfaces


namespace custom_interfaces
{

namespace srv
{

namespace builder
{

class Init_SetCustomNavigationGoal_Response_goal_accepted
{
public:
  Init_SetCustomNavigationGoal_Response_goal_accepted()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  ::custom_interfaces::srv::SetCustomNavigationGoal_Response goal_accepted(::custom_interfaces::srv::SetCustomNavigationGoal_Response::_goal_accepted_type arg)
  {
    msg_.goal_accepted = std::move(arg);
    return std::move(msg_);
  }

private:
  ::custom_interfaces::srv::SetCustomNavigationGoal_Response msg_;
};

}  // namespace builder

}  // namespace srv

template<typename MessageType>
auto build();

template<>
inline
auto build<::custom_interfaces::srv::SetCustomNavigationGoal_Response>()
{
  return custom_interfaces::srv::builder::Init_SetCustomNavigationGoal_Response_goal_accepted();
}

}  // namespace custom_interfaces

#endif  // CUSTOM_INTERFACES__SRV__DETAIL__SET_CUSTOM_NAVIGATION_GOAL__BUILDER_HPP_
