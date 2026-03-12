# generated from rosidl_generator_py/resource/_idl.py.em
# with input from custom_interfaces:msg/IMUData.idl
# generated code does not contain a copyright notice


# Import statements for member types

import builtins  # noqa: E402, I100

import math  # noqa: E402, I100

import rosidl_parser.definition  # noqa: E402, I100


class Metaclass_IMUData(type):
    """Metaclass of message 'IMUData'."""

    _CREATE_ROS_MESSAGE = None
    _CONVERT_FROM_PY = None
    _CONVERT_TO_PY = None
    _DESTROY_ROS_MESSAGE = None
    _TYPE_SUPPORT = None

    __constants = {
    }

    @classmethod
    def __import_type_support__(cls):
        try:
            from rosidl_generator_py import import_type_support
            module = import_type_support('custom_interfaces')
        except ImportError:
            import logging
            import traceback
            logger = logging.getLogger(
                'custom_interfaces.msg.IMUData')
            logger.debug(
                'Failed to import needed modules for type support:\n' +
                traceback.format_exc())
        else:
            cls._CREATE_ROS_MESSAGE = module.create_ros_message_msg__msg__imu_data
            cls._CONVERT_FROM_PY = module.convert_from_py_msg__msg__imu_data
            cls._CONVERT_TO_PY = module.convert_to_py_msg__msg__imu_data
            cls._TYPE_SUPPORT = module.type_support_msg__msg__imu_data
            cls._DESTROY_ROS_MESSAGE = module.destroy_ros_message_msg__msg__imu_data

    @classmethod
    def __prepare__(cls, name, bases, **kwargs):
        # list constant names here so that they appear in the help text of
        # the message class under "Data and other attributes defined here:"
        # as well as populate each message instance
        return {
        }


class IMUData(metaclass=Metaclass_IMUData):
    """Message class 'IMUData'."""

    __slots__ = [
        '_accelerometer_x',
        '_accelerometer_y',
        '_accelerometer_z',
        '_gyroscope_x',
        '_gyroscope_y',
        '_gyroscope_z',
    ]

    _fields_and_field_types = {
        'accelerometer_x': 'float',
        'accelerometer_y': 'float',
        'accelerometer_z': 'float',
        'gyroscope_x': 'float',
        'gyroscope_y': 'float',
        'gyroscope_z': 'float',
    }

    SLOT_TYPES = (
        rosidl_parser.definition.BasicType('float'),  # noqa: E501
        rosidl_parser.definition.BasicType('float'),  # noqa: E501
        rosidl_parser.definition.BasicType('float'),  # noqa: E501
        rosidl_parser.definition.BasicType('float'),  # noqa: E501
        rosidl_parser.definition.BasicType('float'),  # noqa: E501
        rosidl_parser.definition.BasicType('float'),  # noqa: E501
    )

    def __init__(self, **kwargs):
        assert all('_' + key in self.__slots__ for key in kwargs.keys()), \
            'Invalid arguments passed to constructor: %s' % \
            ', '.join(sorted(k for k in kwargs.keys() if '_' + k not in self.__slots__))
        self.accelerometer_x = kwargs.get('accelerometer_x', float())
        self.accelerometer_y = kwargs.get('accelerometer_y', float())
        self.accelerometer_z = kwargs.get('accelerometer_z', float())
        self.gyroscope_x = kwargs.get('gyroscope_x', float())
        self.gyroscope_y = kwargs.get('gyroscope_y', float())
        self.gyroscope_z = kwargs.get('gyroscope_z', float())

    def __repr__(self):
        typename = self.__class__.__module__.split('.')
        typename.pop()
        typename.append(self.__class__.__name__)
        args = []
        for s, t in zip(self.__slots__, self.SLOT_TYPES):
            field = getattr(self, s)
            fieldstr = repr(field)
            # We use Python array type for fields that can be directly stored
            # in them, and "normal" sequences for everything else.  If it is
            # a type that we store in an array, strip off the 'array' portion.
            if (
                isinstance(t, rosidl_parser.definition.AbstractSequence) and
                isinstance(t.value_type, rosidl_parser.definition.BasicType) and
                t.value_type.typename in ['float', 'double', 'int8', 'uint8', 'int16', 'uint16', 'int32', 'uint32', 'int64', 'uint64']
            ):
                if len(field) == 0:
                    fieldstr = '[]'
                else:
                    assert fieldstr.startswith('array(')
                    prefix = "array('X', "
                    suffix = ')'
                    fieldstr = fieldstr[len(prefix):-len(suffix)]
            args.append(s[1:] + '=' + fieldstr)
        return '%s(%s)' % ('.'.join(typename), ', '.join(args))

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        if self.accelerometer_x != other.accelerometer_x:
            return False
        if self.accelerometer_y != other.accelerometer_y:
            return False
        if self.accelerometer_z != other.accelerometer_z:
            return False
        if self.gyroscope_x != other.gyroscope_x:
            return False
        if self.gyroscope_y != other.gyroscope_y:
            return False
        if self.gyroscope_z != other.gyroscope_z:
            return False
        return True

    @classmethod
    def get_fields_and_field_types(cls):
        from copy import copy
        return copy(cls._fields_and_field_types)

    @builtins.property
    def accelerometer_x(self):
        """Message field 'accelerometer_x'."""
        return self._accelerometer_x

    @accelerometer_x.setter
    def accelerometer_x(self, value):
        if __debug__:
            assert \
                isinstance(value, float), \
                "The 'accelerometer_x' field must be of type 'float'"
            assert not (value < -3.402823466e+38 or value > 3.402823466e+38) or math.isinf(value), \
                "The 'accelerometer_x' field must be a float in [-3.402823466e+38, 3.402823466e+38]"
        self._accelerometer_x = value

    @builtins.property
    def accelerometer_y(self):
        """Message field 'accelerometer_y'."""
        return self._accelerometer_y

    @accelerometer_y.setter
    def accelerometer_y(self, value):
        if __debug__:
            assert \
                isinstance(value, float), \
                "The 'accelerometer_y' field must be of type 'float'"
            assert not (value < -3.402823466e+38 or value > 3.402823466e+38) or math.isinf(value), \
                "The 'accelerometer_y' field must be a float in [-3.402823466e+38, 3.402823466e+38]"
        self._accelerometer_y = value

    @builtins.property
    def accelerometer_z(self):
        """Message field 'accelerometer_z'."""
        return self._accelerometer_z

    @accelerometer_z.setter
    def accelerometer_z(self, value):
        if __debug__:
            assert \
                isinstance(value, float), \
                "The 'accelerometer_z' field must be of type 'float'"
            assert not (value < -3.402823466e+38 or value > 3.402823466e+38) or math.isinf(value), \
                "The 'accelerometer_z' field must be a float in [-3.402823466e+38, 3.402823466e+38]"
        self._accelerometer_z = value

    @builtins.property
    def gyroscope_x(self):
        """Message field 'gyroscope_x'."""
        return self._gyroscope_x

    @gyroscope_x.setter
    def gyroscope_x(self, value):
        if __debug__:
            assert \
                isinstance(value, float), \
                "The 'gyroscope_x' field must be of type 'float'"
            assert not (value < -3.402823466e+38 or value > 3.402823466e+38) or math.isinf(value), \
                "The 'gyroscope_x' field must be a float in [-3.402823466e+38, 3.402823466e+38]"
        self._gyroscope_x = value

    @builtins.property
    def gyroscope_y(self):
        """Message field 'gyroscope_y'."""
        return self._gyroscope_y

    @gyroscope_y.setter
    def gyroscope_y(self, value):
        if __debug__:
            assert \
                isinstance(value, float), \
                "The 'gyroscope_y' field must be of type 'float'"
            assert not (value < -3.402823466e+38 or value > 3.402823466e+38) or math.isinf(value), \
                "The 'gyroscope_y' field must be a float in [-3.402823466e+38, 3.402823466e+38]"
        self._gyroscope_y = value

    @builtins.property
    def gyroscope_z(self):
        """Message field 'gyroscope_z'."""
        return self._gyroscope_z

    @gyroscope_z.setter
    def gyroscope_z(self, value):
        if __debug__:
            assert \
                isinstance(value, float), \
                "The 'gyroscope_z' field must be of type 'float'"
            assert not (value < -3.402823466e+38 or value > 3.402823466e+38) or math.isinf(value), \
                "The 'gyroscope_z' field must be a float in [-3.402823466e+38, 3.402823466e+38]"
        self._gyroscope_z = value
