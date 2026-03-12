// generated from rosidl_generator_cpp/resource/idl__traits.hpp.em
// with input from custom_interfaces:msg/IMUData.idl
// generated code does not contain a copyright notice

#ifndef CUSTOM_INTERFACES__MSG__DETAIL__IMU_DATA__TRAITS_HPP_
#define CUSTOM_INTERFACES__MSG__DETAIL__IMU_DATA__TRAITS_HPP_

#include <stdint.h>

#include <sstream>
#include <string>
#include <type_traits>

#include "custom_interfaces/msg/detail/imu_data__struct.hpp"
#include "rosidl_runtime_cpp/traits.hpp"

namespace custom_interfaces
{

namespace msg
{

inline void to_flow_style_yaml(
  const IMUData & msg,
  std::ostream & out)
{
  out << "{";
  // member: accelerometer_x
  {
    out << "accelerometer_x: ";
    rosidl_generator_traits::value_to_yaml(msg.accelerometer_x, out);
    out << ", ";
  }

  // member: accelerometer_y
  {
    out << "accelerometer_y: ";
    rosidl_generator_traits::value_to_yaml(msg.accelerometer_y, out);
    out << ", ";
  }

  // member: accelerometer_z
  {
    out << "accelerometer_z: ";
    rosidl_generator_traits::value_to_yaml(msg.accelerometer_z, out);
    out << ", ";
  }

  // member: gyroscope_x
  {
    out << "gyroscope_x: ";
    rosidl_generator_traits::value_to_yaml(msg.gyroscope_x, out);
    out << ", ";
  }

  // member: gyroscope_y
  {
    out << "gyroscope_y: ";
    rosidl_generator_traits::value_to_yaml(msg.gyroscope_y, out);
    out << ", ";
  }

  // member: gyroscope_z
  {
    out << "gyroscope_z: ";
    rosidl_generator_traits::value_to_yaml(msg.gyroscope_z, out);
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const IMUData & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: accelerometer_x
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "accelerometer_x: ";
    rosidl_generator_traits::value_to_yaml(msg.accelerometer_x, out);
    out << "\n";
  }

  // member: accelerometer_y
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "accelerometer_y: ";
    rosidl_generator_traits::value_to_yaml(msg.accelerometer_y, out);
    out << "\n";
  }

  // member: accelerometer_z
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "accelerometer_z: ";
    rosidl_generator_traits::value_to_yaml(msg.accelerometer_z, out);
    out << "\n";
  }

  // member: gyroscope_x
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "gyroscope_x: ";
    rosidl_generator_traits::value_to_yaml(msg.gyroscope_x, out);
    out << "\n";
  }

  // member: gyroscope_y
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "gyroscope_y: ";
    rosidl_generator_traits::value_to_yaml(msg.gyroscope_y, out);
    out << "\n";
  }

  // member: gyroscope_z
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "gyroscope_z: ";
    rosidl_generator_traits::value_to_yaml(msg.gyroscope_z, out);
    out << "\n";
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const IMUData & msg, bool use_flow_style = false)
{
  std::ostringstream out;
  if (use_flow_style) {
    to_flow_style_yaml(msg, out);
  } else {
    to_block_style_yaml(msg, out);
  }
  return out.str();
}

}  // namespace msg

}  // namespace custom_interfaces

namespace rosidl_generator_traits
{

[[deprecated("use custom_interfaces::msg::to_block_style_yaml() instead")]]
inline void to_yaml(
  const custom_interfaces::msg::IMUData & msg,
  std::ostream & out, size_t indentation = 0)
{
  custom_interfaces::msg::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use custom_interfaces::msg::to_yaml() instead")]]
inline std::string to_yaml(const custom_interfaces::msg::IMUData & msg)
{
  return custom_interfaces::msg::to_yaml(msg);
}

template<>
inline const char * data_type<custom_interfaces::msg::IMUData>()
{
  return "custom_interfaces::msg::IMUData";
}

template<>
inline const char * name<custom_interfaces::msg::IMUData>()
{
  return "custom_interfaces/msg/IMUData";
}

template<>
struct has_fixed_size<custom_interfaces::msg::IMUData>
  : std::integral_constant<bool, true> {};

template<>
struct has_bounded_size<custom_interfaces::msg::IMUData>
  : std::integral_constant<bool, true> {};

template<>
struct is_message<custom_interfaces::msg::IMUData>
  : std::true_type {};

}  // namespace rosidl_generator_traits

#endif  // CUSTOM_INTERFACES__MSG__DETAIL__IMU_DATA__TRAITS_HPP_
