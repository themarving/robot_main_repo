// generated from rosidl_generator_cpp/resource/idl__struct.hpp.em
// with input from custom_interfaces:msg/IMUData.idl
// generated code does not contain a copyright notice

#ifndef CUSTOM_INTERFACES__MSG__DETAIL__IMU_DATA__STRUCT_HPP_
#define CUSTOM_INTERFACES__MSG__DETAIL__IMU_DATA__STRUCT_HPP_

#include <algorithm>
#include <array>
#include <memory>
#include <string>
#include <vector>

#include "rosidl_runtime_cpp/bounded_vector.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


#ifndef _WIN32
# define DEPRECATED__custom_interfaces__msg__IMUData __attribute__((deprecated))
#else
# define DEPRECATED__custom_interfaces__msg__IMUData __declspec(deprecated)
#endif

namespace custom_interfaces
{

namespace msg
{

// message struct
template<class ContainerAllocator>
struct IMUData_
{
  using Type = IMUData_<ContainerAllocator>;

  explicit IMUData_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->accelerometer_x = 0.0f;
      this->accelerometer_y = 0.0f;
      this->accelerometer_z = 0.0f;
      this->gyroscope_x = 0.0f;
      this->gyroscope_y = 0.0f;
      this->gyroscope_z = 0.0f;
    }
  }

  explicit IMUData_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    (void)_alloc;
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->accelerometer_x = 0.0f;
      this->accelerometer_y = 0.0f;
      this->accelerometer_z = 0.0f;
      this->gyroscope_x = 0.0f;
      this->gyroscope_y = 0.0f;
      this->gyroscope_z = 0.0f;
    }
  }

  // field types and members
  using _accelerometer_x_type =
    float;
  _accelerometer_x_type accelerometer_x;
  using _accelerometer_y_type =
    float;
  _accelerometer_y_type accelerometer_y;
  using _accelerometer_z_type =
    float;
  _accelerometer_z_type accelerometer_z;
  using _gyroscope_x_type =
    float;
  _gyroscope_x_type gyroscope_x;
  using _gyroscope_y_type =
    float;
  _gyroscope_y_type gyroscope_y;
  using _gyroscope_z_type =
    float;
  _gyroscope_z_type gyroscope_z;

  // setters for named parameter idiom
  Type & set__accelerometer_x(
    const float & _arg)
  {
    this->accelerometer_x = _arg;
    return *this;
  }
  Type & set__accelerometer_y(
    const float & _arg)
  {
    this->accelerometer_y = _arg;
    return *this;
  }
  Type & set__accelerometer_z(
    const float & _arg)
  {
    this->accelerometer_z = _arg;
    return *this;
  }
  Type & set__gyroscope_x(
    const float & _arg)
  {
    this->gyroscope_x = _arg;
    return *this;
  }
  Type & set__gyroscope_y(
    const float & _arg)
  {
    this->gyroscope_y = _arg;
    return *this;
  }
  Type & set__gyroscope_z(
    const float & _arg)
  {
    this->gyroscope_z = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    custom_interfaces::msg::IMUData_<ContainerAllocator> *;
  using ConstRawPtr =
    const custom_interfaces::msg::IMUData_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<custom_interfaces::msg::IMUData_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<custom_interfaces::msg::IMUData_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      custom_interfaces::msg::IMUData_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<custom_interfaces::msg::IMUData_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      custom_interfaces::msg::IMUData_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<custom_interfaces::msg::IMUData_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<custom_interfaces::msg::IMUData_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<custom_interfaces::msg::IMUData_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__custom_interfaces__msg__IMUData
    std::shared_ptr<custom_interfaces::msg::IMUData_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__custom_interfaces__msg__IMUData
    std::shared_ptr<custom_interfaces::msg::IMUData_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const IMUData_ & other) const
  {
    if (this->accelerometer_x != other.accelerometer_x) {
      return false;
    }
    if (this->accelerometer_y != other.accelerometer_y) {
      return false;
    }
    if (this->accelerometer_z != other.accelerometer_z) {
      return false;
    }
    if (this->gyroscope_x != other.gyroscope_x) {
      return false;
    }
    if (this->gyroscope_y != other.gyroscope_y) {
      return false;
    }
    if (this->gyroscope_z != other.gyroscope_z) {
      return false;
    }
    return true;
  }
  bool operator!=(const IMUData_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct IMUData_

// alias to use template instance with default allocator
using IMUData =
  custom_interfaces::msg::IMUData_<std::allocator<void>>;

// constant definitions

}  // namespace msg

}  // namespace custom_interfaces

#endif  // CUSTOM_INTERFACES__MSG__DETAIL__IMU_DATA__STRUCT_HPP_
