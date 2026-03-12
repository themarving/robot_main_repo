// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from custom_interfaces:msg/TOFSensorData.idl
// generated code does not contain a copyright notice

#ifndef CUSTOM_INTERFACES__MSG__DETAIL__TOF_SENSOR_DATA__STRUCT_H_
#define CUSTOM_INTERFACES__MSG__DETAIL__TOF_SENSOR_DATA__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>


// Constants defined in the message

/// Struct defined in msg/TOFSensorData in the package custom_interfaces.
typedef struct custom_interfaces__msg__TOFSensorData
{
  float front_left;
  float front_right;
  float mid_left;
  float mid_right;
} custom_interfaces__msg__TOFSensorData;

// Struct for a sequence of custom_interfaces__msg__TOFSensorData.
typedef struct custom_interfaces__msg__TOFSensorData__Sequence
{
  custom_interfaces__msg__TOFSensorData * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} custom_interfaces__msg__TOFSensorData__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // CUSTOM_INTERFACES__MSG__DETAIL__TOF_SENSOR_DATA__STRUCT_H_
