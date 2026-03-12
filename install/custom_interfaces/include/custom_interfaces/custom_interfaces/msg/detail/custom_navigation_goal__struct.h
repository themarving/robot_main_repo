// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from custom_interfaces:msg/CustomNavigationGoal.idl
// generated code does not contain a copyright notice

#ifndef CUSTOM_INTERFACES__MSG__DETAIL__CUSTOM_NAVIGATION_GOAL__STRUCT_H_
#define CUSTOM_INTERFACES__MSG__DETAIL__CUSTOM_NAVIGATION_GOAL__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>


// Constants defined in the message

/// Struct defined in msg/CustomNavigationGoal in the package custom_interfaces.
typedef struct custom_interfaces__msg__CustomNavigationGoal
{
  double x;
  double y;
  double yaw;
} custom_interfaces__msg__CustomNavigationGoal;

// Struct for a sequence of custom_interfaces__msg__CustomNavigationGoal.
typedef struct custom_interfaces__msg__CustomNavigationGoal__Sequence
{
  custom_interfaces__msg__CustomNavigationGoal * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} custom_interfaces__msg__CustomNavigationGoal__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // CUSTOM_INTERFACES__MSG__DETAIL__CUSTOM_NAVIGATION_GOAL__STRUCT_H_
