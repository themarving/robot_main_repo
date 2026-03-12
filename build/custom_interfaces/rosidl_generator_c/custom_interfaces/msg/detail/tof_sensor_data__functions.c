// generated from rosidl_generator_c/resource/idl__functions.c.em
// with input from custom_interfaces:msg/TOFSensorData.idl
// generated code does not contain a copyright notice
#include "custom_interfaces/msg/detail/tof_sensor_data__functions.h"

#include <assert.h>
#include <stdbool.h>
#include <stdlib.h>
#include <string.h>

#include "rcutils/allocator.h"


bool
custom_interfaces__msg__TOFSensorData__init(custom_interfaces__msg__TOFSensorData * msg)
{
  if (!msg) {
    return false;
  }
  // front_left
  // front_right
  // mid_left
  // mid_right
  return true;
}

void
custom_interfaces__msg__TOFSensorData__fini(custom_interfaces__msg__TOFSensorData * msg)
{
  if (!msg) {
    return;
  }
  // front_left
  // front_right
  // mid_left
  // mid_right
}

bool
custom_interfaces__msg__TOFSensorData__are_equal(const custom_interfaces__msg__TOFSensorData * lhs, const custom_interfaces__msg__TOFSensorData * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  // front_left
  if (lhs->front_left != rhs->front_left) {
    return false;
  }
  // front_right
  if (lhs->front_right != rhs->front_right) {
    return false;
  }
  // mid_left
  if (lhs->mid_left != rhs->mid_left) {
    return false;
  }
  // mid_right
  if (lhs->mid_right != rhs->mid_right) {
    return false;
  }
  return true;
}

bool
custom_interfaces__msg__TOFSensorData__copy(
  const custom_interfaces__msg__TOFSensorData * input,
  custom_interfaces__msg__TOFSensorData * output)
{
  if (!input || !output) {
    return false;
  }
  // front_left
  output->front_left = input->front_left;
  // front_right
  output->front_right = input->front_right;
  // mid_left
  output->mid_left = input->mid_left;
  // mid_right
  output->mid_right = input->mid_right;
  return true;
}

custom_interfaces__msg__TOFSensorData *
custom_interfaces__msg__TOFSensorData__create()
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  custom_interfaces__msg__TOFSensorData * msg = (custom_interfaces__msg__TOFSensorData *)allocator.allocate(sizeof(custom_interfaces__msg__TOFSensorData), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(custom_interfaces__msg__TOFSensorData));
  bool success = custom_interfaces__msg__TOFSensorData__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
custom_interfaces__msg__TOFSensorData__destroy(custom_interfaces__msg__TOFSensorData * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    custom_interfaces__msg__TOFSensorData__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
custom_interfaces__msg__TOFSensorData__Sequence__init(custom_interfaces__msg__TOFSensorData__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  custom_interfaces__msg__TOFSensorData * data = NULL;

  if (size) {
    data = (custom_interfaces__msg__TOFSensorData *)allocator.zero_allocate(size, sizeof(custom_interfaces__msg__TOFSensorData), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = custom_interfaces__msg__TOFSensorData__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        custom_interfaces__msg__TOFSensorData__fini(&data[i - 1]);
      }
      allocator.deallocate(data, allocator.state);
      return false;
    }
  }
  array->data = data;
  array->size = size;
  array->capacity = size;
  return true;
}

void
custom_interfaces__msg__TOFSensorData__Sequence__fini(custom_interfaces__msg__TOFSensorData__Sequence * array)
{
  if (!array) {
    return;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();

  if (array->data) {
    // ensure that data and capacity values are consistent
    assert(array->capacity > 0);
    // finalize all array elements
    for (size_t i = 0; i < array->capacity; ++i) {
      custom_interfaces__msg__TOFSensorData__fini(&array->data[i]);
    }
    allocator.deallocate(array->data, allocator.state);
    array->data = NULL;
    array->size = 0;
    array->capacity = 0;
  } else {
    // ensure that data, size, and capacity values are consistent
    assert(0 == array->size);
    assert(0 == array->capacity);
  }
}

custom_interfaces__msg__TOFSensorData__Sequence *
custom_interfaces__msg__TOFSensorData__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  custom_interfaces__msg__TOFSensorData__Sequence * array = (custom_interfaces__msg__TOFSensorData__Sequence *)allocator.allocate(sizeof(custom_interfaces__msg__TOFSensorData__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = custom_interfaces__msg__TOFSensorData__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
custom_interfaces__msg__TOFSensorData__Sequence__destroy(custom_interfaces__msg__TOFSensorData__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    custom_interfaces__msg__TOFSensorData__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
custom_interfaces__msg__TOFSensorData__Sequence__are_equal(const custom_interfaces__msg__TOFSensorData__Sequence * lhs, const custom_interfaces__msg__TOFSensorData__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!custom_interfaces__msg__TOFSensorData__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
custom_interfaces__msg__TOFSensorData__Sequence__copy(
  const custom_interfaces__msg__TOFSensorData__Sequence * input,
  custom_interfaces__msg__TOFSensorData__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    const size_t allocation_size =
      input->size * sizeof(custom_interfaces__msg__TOFSensorData);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    custom_interfaces__msg__TOFSensorData * data =
      (custom_interfaces__msg__TOFSensorData *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!custom_interfaces__msg__TOFSensorData__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          custom_interfaces__msg__TOFSensorData__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!custom_interfaces__msg__TOFSensorData__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}
