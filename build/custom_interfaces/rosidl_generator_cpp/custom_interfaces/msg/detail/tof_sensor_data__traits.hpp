// generated from rosidl_generator_cpp/resource/idl__traits.hpp.em
// with input from custom_interfaces:msg/TOFSensorData.idl
// generated code does not contain a copyright notice

#ifndef CUSTOM_INTERFACES__MSG__DETAIL__TOF_SENSOR_DATA__TRAITS_HPP_
#define CUSTOM_INTERFACES__MSG__DETAIL__TOF_SENSOR_DATA__TRAITS_HPP_

#include <stdint.h>

#include <sstream>
#include <string>
#include <type_traits>

#include "custom_interfaces/msg/detail/tof_sensor_data__struct.hpp"
#include "rosidl_runtime_cpp/traits.hpp"

namespace custom_interfaces
{

namespace msg
{

inline void to_flow_style_yaml(
  const TOFSensorData & msg,
  std::ostream & out)
{
  out << "{";
  // member: front_left
  {
    out << "front_left: ";
    rosidl_generator_traits::value_to_yaml(msg.front_left, out);
    out << ", ";
  }

  // member: front_right
  {
    out << "front_right: ";
    rosidl_generator_traits::value_to_yaml(msg.front_right, out);
    out << ", ";
  }

  // member: mid_left
  {
    out << "mid_left: ";
    rosidl_generator_traits::value_to_yaml(msg.mid_left, out);
    out << ", ";
  }

  // member: mid_right
  {
    out << "mid_right: ";
    rosidl_generator_traits::value_to_yaml(msg.mid_right, out);
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const TOFSensorData & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: front_left
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "front_left: ";
    rosidl_generator_traits::value_to_yaml(msg.front_left, out);
    out << "\n";
  }

  // member: front_right
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "front_right: ";
    rosidl_generator_traits::value_to_yaml(msg.front_right, out);
    out << "\n";
  }

  // member: mid_left
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "mid_left: ";
    rosidl_generator_traits::value_to_yaml(msg.mid_left, out);
    out << "\n";
  }

  // member: mid_right
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "mid_right: ";
    rosidl_generator_traits::value_to_yaml(msg.mid_right, out);
    out << "\n";
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const TOFSensorData & msg, bool use_flow_style = false)
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
  const custom_interfaces::msg::TOFSensorData & msg,
  std::ostream & out, size_t indentation = 0)
{
  custom_interfaces::msg::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use custom_interfaces::msg::to_yaml() instead")]]
inline std::string to_yaml(const custom_interfaces::msg::TOFSensorData & msg)
{
  return custom_interfaces::msg::to_yaml(msg);
}

template<>
inline const char * data_type<custom_interfaces::msg::TOFSensorData>()
{
  return "custom_interfaces::msg::TOFSensorData";
}

template<>
inline const char * name<custom_interfaces::msg::TOFSensorData>()
{
  return "custom_interfaces/msg/TOFSensorData";
}

template<>
struct has_fixed_size<custom_interfaces::msg::TOFSensorData>
  : std::integral_constant<bool, true> {};

template<>
struct has_bounded_size<custom_interfaces::msg::TOFSensorData>
  : std::integral_constant<bool, true> {};

template<>
struct is_message<custom_interfaces::msg::TOFSensorData>
  : std::true_type {};

}  // namespace rosidl_generator_traits

#endif  // CUSTOM_INTERFACES__MSG__DETAIL__TOF_SENSOR_DATA__TRAITS_HPP_
