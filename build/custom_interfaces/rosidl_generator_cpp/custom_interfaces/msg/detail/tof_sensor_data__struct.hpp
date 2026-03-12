// generated from rosidl_generator_cpp/resource/idl__struct.hpp.em
// with input from custom_interfaces:msg/TOFSensorData.idl
// generated code does not contain a copyright notice

#ifndef CUSTOM_INTERFACES__MSG__DETAIL__TOF_SENSOR_DATA__STRUCT_HPP_
#define CUSTOM_INTERFACES__MSG__DETAIL__TOF_SENSOR_DATA__STRUCT_HPP_

#include <algorithm>
#include <array>
#include <memory>
#include <string>
#include <vector>

#include "rosidl_runtime_cpp/bounded_vector.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


#ifndef _WIN32
# define DEPRECATED__custom_interfaces__msg__TOFSensorData __attribute__((deprecated))
#else
# define DEPRECATED__custom_interfaces__msg__TOFSensorData __declspec(deprecated)
#endif

namespace custom_interfaces
{

namespace msg
{

// message struct
template<class ContainerAllocator>
struct TOFSensorData_
{
  using Type = TOFSensorData_<ContainerAllocator>;

  explicit TOFSensorData_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->front_left = 0.0f;
      this->front_right = 0.0f;
      this->mid_left = 0.0f;
      this->mid_right = 0.0f;
    }
  }

  explicit TOFSensorData_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    (void)_alloc;
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->front_left = 0.0f;
      this->front_right = 0.0f;
      this->mid_left = 0.0f;
      this->mid_right = 0.0f;
    }
  }

  // field types and members
  using _front_left_type =
    float;
  _front_left_type front_left;
  using _front_right_type =
    float;
  _front_right_type front_right;
  using _mid_left_type =
    float;
  _mid_left_type mid_left;
  using _mid_right_type =
    float;
  _mid_right_type mid_right;

  // setters for named parameter idiom
  Type & set__front_left(
    const float & _arg)
  {
    this->front_left = _arg;
    return *this;
  }
  Type & set__front_right(
    const float & _arg)
  {
    this->front_right = _arg;
    return *this;
  }
  Type & set__mid_left(
    const float & _arg)
  {
    this->mid_left = _arg;
    return *this;
  }
  Type & set__mid_right(
    const float & _arg)
  {
    this->mid_right = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    custom_interfaces::msg::TOFSensorData_<ContainerAllocator> *;
  using ConstRawPtr =
    const custom_interfaces::msg::TOFSensorData_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<custom_interfaces::msg::TOFSensorData_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<custom_interfaces::msg::TOFSensorData_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      custom_interfaces::msg::TOFSensorData_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<custom_interfaces::msg::TOFSensorData_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      custom_interfaces::msg::TOFSensorData_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<custom_interfaces::msg::TOFSensorData_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<custom_interfaces::msg::TOFSensorData_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<custom_interfaces::msg::TOFSensorData_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__custom_interfaces__msg__TOFSensorData
    std::shared_ptr<custom_interfaces::msg::TOFSensorData_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__custom_interfaces__msg__TOFSensorData
    std::shared_ptr<custom_interfaces::msg::TOFSensorData_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const TOFSensorData_ & other) const
  {
    if (this->front_left != other.front_left) {
      return false;
    }
    if (this->front_right != other.front_right) {
      return false;
    }
    if (this->mid_left != other.mid_left) {
      return false;
    }
    if (this->mid_right != other.mid_right) {
      return false;
    }
    return true;
  }
  bool operator!=(const TOFSensorData_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct TOFSensorData_

// alias to use template instance with default allocator
using TOFSensorData =
  custom_interfaces::msg::TOFSensorData_<std::allocator<void>>;

// constant definitions

}  // namespace msg

}  // namespace custom_interfaces

#endif  // CUSTOM_INTERFACES__MSG__DETAIL__TOF_SENSOR_DATA__STRUCT_HPP_
