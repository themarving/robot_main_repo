// generated from rosidl_generator_cpp/resource/idl__struct.hpp.em
// with input from custom_interfaces:msg/DetectedVoiceCommand.idl
// generated code does not contain a copyright notice

#ifndef CUSTOM_INTERFACES__MSG__DETAIL__DETECTED_VOICE_COMMAND__STRUCT_HPP_
#define CUSTOM_INTERFACES__MSG__DETAIL__DETECTED_VOICE_COMMAND__STRUCT_HPP_

#include <algorithm>
#include <array>
#include <memory>
#include <string>
#include <vector>

#include "rosidl_runtime_cpp/bounded_vector.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


#ifndef _WIN32
# define DEPRECATED__custom_interfaces__msg__DetectedVoiceCommand __attribute__((deprecated))
#else
# define DEPRECATED__custom_interfaces__msg__DetectedVoiceCommand __declspec(deprecated)
#endif

namespace custom_interfaces
{

namespace msg
{

// message struct
template<class ContainerAllocator>
struct DetectedVoiceCommand_
{
  using Type = DetectedVoiceCommand_<ContainerAllocator>;

  explicit DetectedVoiceCommand_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->command_direction = 0;
      this->command = "";
    }
  }

  explicit DetectedVoiceCommand_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : command(_alloc)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->command_direction = 0;
      this->command = "";
    }
  }

  // field types and members
  using _command_direction_type =
    int16_t;
  _command_direction_type command_direction;
  using _command_type =
    std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>;
  _command_type command;

  // setters for named parameter idiom
  Type & set__command_direction(
    const int16_t & _arg)
  {
    this->command_direction = _arg;
    return *this;
  }
  Type & set__command(
    const std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>> & _arg)
  {
    this->command = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    custom_interfaces::msg::DetectedVoiceCommand_<ContainerAllocator> *;
  using ConstRawPtr =
    const custom_interfaces::msg::DetectedVoiceCommand_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<custom_interfaces::msg::DetectedVoiceCommand_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<custom_interfaces::msg::DetectedVoiceCommand_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      custom_interfaces::msg::DetectedVoiceCommand_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<custom_interfaces::msg::DetectedVoiceCommand_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      custom_interfaces::msg::DetectedVoiceCommand_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<custom_interfaces::msg::DetectedVoiceCommand_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<custom_interfaces::msg::DetectedVoiceCommand_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<custom_interfaces::msg::DetectedVoiceCommand_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__custom_interfaces__msg__DetectedVoiceCommand
    std::shared_ptr<custom_interfaces::msg::DetectedVoiceCommand_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__custom_interfaces__msg__DetectedVoiceCommand
    std::shared_ptr<custom_interfaces::msg::DetectedVoiceCommand_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const DetectedVoiceCommand_ & other) const
  {
    if (this->command_direction != other.command_direction) {
      return false;
    }
    if (this->command != other.command) {
      return false;
    }
    return true;
  }
  bool operator!=(const DetectedVoiceCommand_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct DetectedVoiceCommand_

// alias to use template instance with default allocator
using DetectedVoiceCommand =
  custom_interfaces::msg::DetectedVoiceCommand_<std::allocator<void>>;

// constant definitions

}  // namespace msg

}  // namespace custom_interfaces

#endif  // CUSTOM_INTERFACES__MSG__DETAIL__DETECTED_VOICE_COMMAND__STRUCT_HPP_
