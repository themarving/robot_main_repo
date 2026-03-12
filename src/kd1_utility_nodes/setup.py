from setuptools import find_packages, setup

package_name = 'kd1_utility_nodes'

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
            "audio_playback_node = kd1_utility_nodes.audio_playback_node:main",
            "face_animation_node = kd1_utility_nodes.face_animation_node:main",
            "imu_conversion_node = kd1_utility_nodes.imu_conversion_node:main",
            "light_ring_node = kd1_utility_nodes.light_ring_node:main"
        ],
    },
)
