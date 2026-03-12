// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from custom_interfaces:msg/MoveRobotCommand.idl
// generated code does not contain a copyright notice

#ifndef CUSTOM_INTERFACES__MSG__DETAIL__MOVE_ROBOT_COMMAND__STRUCT_H_
#define CUSTOM_INTERFACES__MSG__DETAIL__MOVE_ROBOT_COMMAND__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>


// Constants defined in the message

// Include directives for member types
// Member 'command'
#include "rosidl_runtime_c/string.h"

/// Struct defined in msg/MoveRobotCommand in the package custom_interfaces.
typedef struct custom_interfaces__msg__MoveRobotCommand
{
  rosidl_runtime_c__String command;
  float goal_angle;
} custom_interfaces__msg__MoveRobotCommand;

// Struct for a sequence of custom_interfaces__msg__MoveRobotCommand.
typedef struct custom_interfaces__msg__MoveRobotCommand__Sequence
{
  custom_interfaces__msg__MoveRobotCommand * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} custom_interfaces__msg__MoveRobotCommand__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // CUSTOM_INTERFACES__MSG__DETAIL__MOVE_ROBOT_COMMAND__STRUCT_H_
