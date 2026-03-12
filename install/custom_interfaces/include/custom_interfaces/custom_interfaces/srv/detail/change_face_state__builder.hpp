// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from custom_interfaces:srv/ChangeFaceState.idl
// generated code does not contain a copyright notice

#ifndef CUSTOM_INTERFACES__SRV__DETAIL__CHANGE_FACE_STATE__BUILDER_HPP_
#define CUSTOM_INTERFACES__SRV__DETAIL__CHANGE_FACE_STATE__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "custom_interfaces/srv/detail/change_face_state__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace custom_interfaces
{

namespace srv
{

namespace builder
{

class Init_ChangeFaceState_Request_face_state
{
public:
  Init_ChangeFaceState_Request_face_state()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  ::custom_interfaces::srv::ChangeFaceState_Request face_state(::custom_interfaces::srv::ChangeFaceState_Request::_face_state_type arg)
  {
    msg_.face_state = std::move(arg);
    return std::move(msg_);
  }

private:
  ::custom_interfaces::srv::ChangeFaceState_Request msg_;
};

}  // namespace builder

}  // namespace srv

template<typename MessageType>
auto build();

template<>
inline
auto build<::custom_interfaces::srv::ChangeFaceState_Request>()
{
  return custom_interfaces::srv::builder::Init_ChangeFaceState_Request_face_state();
}

}  // namespace custom_interfaces


namespace custom_interfaces
{

namespace srv
{

namespace builder
{

class Init_ChangeFaceState_Response_face_state_changed
{
public:
  Init_ChangeFaceState_Response_face_state_changed()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  ::custom_interfaces::srv::ChangeFaceState_Response face_state_changed(::custom_interfaces::srv::ChangeFaceState_Response::_face_state_changed_type arg)
  {
    msg_.face_state_changed = std::move(arg);
    return std::move(msg_);
  }

private:
  ::custom_interfaces::srv::ChangeFaceState_Response msg_;
};

}  // namespace builder

}  // namespace srv

template<typename MessageType>
auto build();

template<>
inline
auto build<::custom_interfaces::srv::ChangeFaceState_Response>()
{
  return custom_interfaces::srv::builder::Init_ChangeFaceState_Response_face_state_changed();
}

}  // namespace custom_interfaces

#endif  // CUSTOM_INTERFACES__SRV__DETAIL__CHANGE_FACE_STATE__BUILDER_HPP_
