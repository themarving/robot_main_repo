from setuptools import find_packages, setup

package_name = 'kd1_locomotion'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='name',
    maintainer_email='name@todo.todo',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            "motor_driver_comms_node = kd1_locomotion.motor_driver_comms_node:main",
            "moving_robot_node = kd1_locomotion.moving_robot_node:main",
            "wheel_encoder_tof_node = kd1_locomotion.wheel_encoder_tof_node:main",
            "wheel_odometry_node = kd1_locomotion.wheel_odometry_node:main",
            "teleop_node = kd1_locomotion.teleop_node:main",
            "emergency_stop_node = kd1_locomotion.emergency_stop_node:main"
        ],
    },
)
