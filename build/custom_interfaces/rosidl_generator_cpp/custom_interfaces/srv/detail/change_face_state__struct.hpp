// generated from rosidl_generator_cpp/resource/idl__struct.hpp.em
// with input from custom_interfaces:srv/ChangeFaceState.idl
// generated code does not contain a copyright notice

#ifndef CUSTOM_INTERFACES__SRV__DETAIL__CHANGE_FACE_STATE__STRUCT_HPP_
#define CUSTOM_INTERFACES__SRV__DETAIL__CHANGE_FACE_STATE__STRUCT_HPP_

#include <algorithm>
#include <array>
#include <memory>
#include <string>
#include <vector>

#include "rosidl_runtime_cpp/bounded_vector.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


#ifndef _WIN32
# define DEPRECATED__custom_interfaces__srv__ChangeFaceState_Request __attribute__((deprecated))
#else
# define DEPRECATED__custom_interfaces__srv__ChangeFaceState_Request __declspec(deprecated)
#endif

namespace custom_interfaces
{

namespace srv
{

// message struct
template<class ContainerAllocator>
struct ChangeFaceState_Request_
{
  using Type = ChangeFaceState_Request_<ContainerAllocator>;

  explicit ChangeFaceState_Request_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->face_state = "";
    }
  }

  explicit ChangeFaceState_Request_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : face_state(_alloc)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->face_state = "";
    }
  }

  // field types and members
  using _face_state_type =
    std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>;
  _face_state_type face_state;

  // setters for named parameter idiom
  Type & set__face_state(
    const std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>> & _arg)
  {
    this->face_state = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    custom_interfaces::srv::ChangeFaceState_Request_<ContainerAllocator> *;
  using ConstRawPtr =
    const custom_interfaces::srv::ChangeFaceState_Request_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<custom_interfaces::srv::ChangeFaceState_Request_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<custom_interfaces::srv::ChangeFaceState_Request_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      custom_interfaces::srv::ChangeFaceState_Request_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<custom_interfaces::srv::ChangeFaceState_Request_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      custom_interfaces::srv::ChangeFaceState_Request_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<custom_interfaces::srv::ChangeFaceState_Request_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<custom_interfaces::srv::ChangeFaceState_Request_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<custom_interfaces::srv::ChangeFaceState_Request_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__custom_interfaces__srv__ChangeFaceState_Request
    std::shared_ptr<custom_interfaces::srv::ChangeFaceState_Request_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__custom_interfaces__srv__ChangeFaceState_Request
    std::shared_ptr<custom_interfaces::srv::ChangeFaceState_Request_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const ChangeFaceState_Request_ & other) const
  {
    if (this->face_state != other.face_state) {
      return false;
    }
    return true;
  }
  bool operator!=(const ChangeFaceState_Request_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct ChangeFaceState_Request_

// alias to use template instance with default allocator
using ChangeFaceState_Request =
  custom_interfaces::srv::ChangeFaceState_Request_<std::allocator<void>>;

// constant definitions

}  // namespace srv

}  // namespace custom_interfaces


#ifndef _WIN32
# define DEPRECATED__custom_interfaces__srv__ChangeFaceState_Response __attribute__((deprecated))
#else
# define DEPRECATED__custom_interfaces__srv__ChangeFaceState_Response __declspec(deprecated)
#endif

namespace custom_interfaces
{

namespace srv
{

// message struct
template<class ContainerAllocator>
struct ChangeFaceState_Response_
{
  using Type = ChangeFaceState_Response_<ContainerAllocator>;

  explicit ChangeFaceState_Response_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->face_state_changed = false;
    }
  }

  explicit ChangeFaceState_Response_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    (void)_alloc;
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->face_state_changed = false;
    }
  }

  // field types and members
  using _face_state_changed_type =
    bool;
  _face_state_changed_type face_state_changed;

  // setters for named parameter idiom
  Type & set__face_state_changed(
    const bool & _arg)
  {
    this->face_state_changed = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    custom_interfaces::srv::ChangeFaceState_Response_<ContainerAllocator> *;
  using ConstRawPtr =
    const custom_interfaces::srv::ChangeFaceState_Response_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<custom_interfaces::srv::ChangeFaceState_Response_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<custom_interfaces::srv::ChangeFaceState_Response_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      custom_interfaces::srv::ChangeFaceState_Response_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<custom_interfaces::srv::ChangeFaceState_Response_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      custom_interfaces::srv::ChangeFaceState_Response_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<custom_interfaces::srv::ChangeFaceState_Response_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<custom_interfaces::srv::ChangeFaceState_Response_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<custom_interfaces::srv::ChangeFaceState_Response_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__custom_interfaces__srv__ChangeFaceState_Response
    std::shared_ptr<custom_interfaces::srv::ChangeFaceState_Response_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__custom_interfaces__srv__ChangeFaceState_Response
    std::shared_ptr<custom_interfaces::srv::ChangeFaceState_Response_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const ChangeFaceState_Response_ & other) const
  {
    if (this->face_state_changed != other.face_state_changed) {
      return false;
    }
    return true;
  }
  bool operator!=(const ChangeFaceState_Response_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct ChangeFaceState_Response_

// alias to use template instance with default allocator
using ChangeFaceState_Response =
  custom_interfaces::srv::ChangeFaceState_Response_<std::allocator<void>>;

// constant definitions

}  // namespace srv

}  // namespace custom_interfaces

namespace custom_interfaces
{

namespace srv
{

struct ChangeFaceState
{
  using Request = custom_interfaces::srv::ChangeFaceState_Request;
  using Response = custom_interfaces::srv::ChangeFaceState_Response;
};

}  // namespace srv

}  // namespace custom_interfaces

#endif  // CUSTOM_INTERFACES__SRV__DETAIL__CHANGE_FACE_STATE__STRUCT_HPP_
