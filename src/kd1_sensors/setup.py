from setuptools import find_packages, setup

package_name = 'kd1_sensors'

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
            "audio_direction_node = kd1_sensors.audio_direction_node:main",
            "oak_depthai_node = kd1_sensors.oak_depthai_node:main",
            "voice_recognition_node = kd1_sensors.voice_recognition_node:main"
        ],
    },
)
