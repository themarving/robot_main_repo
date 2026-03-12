// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from custom_interfaces:msg/IMUData.idl
// generated code does not contain a copyright notice

#ifndef CUSTOM_INTERFACES__MSG__DETAIL__IMU_DATA__BUILDER_HPP_
#define CUSTOM_INTERFACES__MSG__DETAIL__IMU_DATA__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "custom_interfaces/msg/detail/imu_data__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace custom_interfaces
{

namespace msg
{

namespace builder
{

class Init_IMUData_gyroscope_z
{
public:
  explicit Init_IMUData_gyroscope_z(::custom_interfaces::msg::IMUData & msg)
  : msg_(msg)
  {}
  ::custom_interfaces::msg::IMUData gyroscope_z(::custom_interfaces::msg::IMUData::_gyroscope_z_type arg)
  {
    msg_.gyroscope_z = std::move(arg);
    return std::move(msg_);
  }

private:
  ::custom_interfaces::msg::IMUData msg_;
};

class Init_IMUData_gyroscope_y
{
public:
  explicit Init_IMUData_gyroscope_y(::custom_interfaces::msg::IMUData & msg)
  : msg_(msg)
  {}
  Init_IMUData_gyroscope_z gyroscope_y(::custom_interfaces::msg::IMUData::_gyroscope_y_type arg)
  {
    msg_.gyroscope_y = std::move(arg);
    return Init_IMUData_gyroscope_z(msg_);
  }

private:
  ::custom_interfaces::msg::IMUData msg_;
};

class Init_IMUData_gyroscope_x
{
public:
  explicit Init_IMUData_gyroscope_x(::custom_interfaces::msg::IMUData & msg)
  : msg_(msg)
  {}
  Init_IMUData_gyroscope_y gyroscope_x(::custom_interfaces::msg::IMUData::_gyroscope_x_type arg)
  {
    msg_.gyroscope_x = std::move(arg);
    return Init_IMUData_gyroscope_y(msg_);
  }

private:
  ::custom_interfaces::msg::IMUData msg_;
};

class Init_IMUData_accelerometer_z
{
public:
  explicit Init_IMUData_accelerometer_z(::custom_interfaces::msg::IMUData & msg)
  : msg_(msg)
  {}
  Init_IMUData_gyroscope_x accelerometer_z(::custom_interfaces::msg::IMUData::_accelerometer_z_type arg)
  {
    msg_.accelerometer_z = std::move(arg);
    return Init_IMUData_gyroscope_x(msg_);
  }

private:
  ::custom_interfaces::msg::IMUData msg_;
};

class Init_IMUData_accelerometer_y
{
public:
  explicit Init_IMUData_accelerometer_y(::custom_interfaces::msg::IMUData & msg)
  : msg_(msg)
  {}
  Init_IMUData_accelerometer_z accelerometer_y(::custom_interfaces::msg::IMUData::_accelerometer_y_type arg)
  {
    msg_.accelerometer_y = std::move(arg);
    return Init_IMUData_accelerometer_z(msg_);
  }

private:
  ::custom_interfaces::msg::IMUData msg_;
};

class Init_IMUData_accelerometer_x
{
public:
  Init_IMUData_accelerometer_x()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_IMUData_accelerometer_y accelerometer_x(::custom_interfaces::msg::IMUData::_accelerometer_x_type arg)
  {
    msg_.accelerometer_x = std::move(arg);
    return Init_IMUData_accelerometer_y(msg_);
  }

private:
  ::custom_interfaces::msg::IMUData msg_;
};

}  // namespace builder

}  // namespace msg

template<typename MessageType>
auto build();

template<>
inline
auto build<::custom_interfaces::msg::IMUData>()
{
  return custom_interfaces::msg::builder::Init_IMUData_accelerometer_x();
}

}  // namespace custom_interfaces

#endif  // CUSTOM_INTERFACES__MSG__DETAIL__IMU_DATA__BUILDER_HPP_
