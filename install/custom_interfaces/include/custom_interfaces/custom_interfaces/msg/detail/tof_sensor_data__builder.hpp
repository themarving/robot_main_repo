// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from custom_interfaces:msg/TOFSensorData.idl
// generated code does not contain a copyright notice

#ifndef CUSTOM_INTERFACES__MSG__DETAIL__TOF_SENSOR_DATA__BUILDER_HPP_
#define CUSTOM_INTERFACES__MSG__DETAIL__TOF_SENSOR_DATA__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "custom_interfaces/msg/detail/tof_sensor_data__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace custom_interfaces
{

namespace msg
{

namespace builder
{

class Init_TOFSensorData_mid_right
{
public:
  explicit Init_TOFSensorData_mid_right(::custom_interfaces::msg::TOFSensorData & msg)
  : msg_(msg)
  {}
  ::custom_interfaces::msg::TOFSensorData mid_right(::custom_interfaces::msg::TOFSensorData::_mid_right_type arg)
  {
    msg_.mid_right = std::move(arg);
    return std::move(msg_);
  }

private:
  ::custom_interfaces::msg::TOFSensorData msg_;
};

class Init_TOFSensorData_mid_left
{
public:
  explicit Init_TOFSensorData_mid_left(::custom_interfaces::msg::TOFSensorData & msg)
  : msg_(msg)
  {}
  Init_TOFSensorData_mid_right mid_left(::custom_interfaces::msg::TOFSensorData::_mid_left_type arg)
  {
    msg_.mid_left = std::move(arg);
    return Init_TOFSensorData_mid_right(msg_);
  }

private:
  ::custom_interfaces::msg::TOFSensorData msg_;
};

class Init_TOFSensorData_front_right
{
public:
  explicit Init_TOFSensorData_front_right(::custom_interfaces::msg::TOFSensorData & msg)
  : msg_(msg)
  {}
  Init_TOFSensorData_mid_left front_right(::custom_interfaces::msg::TOFSensorData::_front_right_type arg)
  {
    msg_.front_right = std::move(arg);
    return Init_TOFSensorData_mid_left(msg_);
  }

private:
  ::custom_interfaces::msg::TOFSensorData msg_;
};

class Init_TOFSensorData_front_left
{
public:
  Init_TOFSensorData_front_left()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_TOFSensorData_front_right front_left(::custom_interfaces::msg::TOFSensorData::_front_left_type arg)
  {
    msg_.front_left = std::move(arg);
    return Init_TOFSensorData_front_right(msg_);
  }

private:
  ::custom_interfaces::msg::TOFSensorData msg_;
};

}  // namespace builder

}  // namespace msg

template<typename MessageType>
auto build();

template<>
inline
auto build<::custom_interfaces::msg::TOFSensorData>()
{
  return custom_interfaces::msg::builder::Init_TOFSensorData_front_left();
}

}  // namespace custom_interfaces

#endif  // CUSTOM_INTERFACES__MSG__DETAIL__TOF_SENSOR_DATA__BUILDER_HPP_
