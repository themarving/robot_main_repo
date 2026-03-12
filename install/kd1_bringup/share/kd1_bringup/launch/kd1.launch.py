import os

from launch import LaunchDescription
from launch.actions import TimerAction
from launch_ros.actions import Node

from ament_index_python.packages import get_package_share_directory

from launch.substitutions import Command, FindExecutable, PathJoinSubstitution
from launch_ros.parameter_descriptions import ParameterValue
from launch_ros.substitutions import FindPackageShare
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource


def generate_launch_description():  
    
    #################################################
    ### ROBOT DESCRIPTION / ROBOT STATE PUBLISHER ###
    #################################################
    
    # Get URDF via xacro
    robot_description_content = ParameterValue(
        Command(
            [
                PathJoinSubstitution([FindExecutable(name="xacro")]),
                " ",
                PathJoinSubstitution(
                    [
                        FindPackageShare("kd1_description"),
                        "urdf",
                        "kd1.urdf.xacro",
                    ]
                ),
            ]
        ),
        value_type=str,
    )

    robot_description = {"robot_description": robot_description_content}
    
    robot_state_pub_node = Node(
        package="robot_state_publisher",
        executable="robot_state_publisher",
        name="robot_state_pub_node",
        output="both", # both means screen and log for logging
        parameters=[robot_description],
    )

    
    ##########################
    ### ROBOT LOCALIZATION ###
    ##########################
    
    pkg_share = get_package_share_directory('kd1_bringup')
    
    robot_localization_node = Node(
        package='robot_localization',
        executable='ekf_node',
        name='ekf_node',
        output='screen',
        parameters=[os.path.join(pkg_share, 'config/ekf.yaml')],
    )


    #######################
    ### SECONDARY NODES ###
    #######################
    
    secondary_nodes = [
        # locomotion
        Node(package='kd1_locomotion', executable='moving_robot_node', name='moving_robot_node'),
        Node(package='kd1_locomotion', executable='wheel_encoder_tof_node', name='wheel_encoder_tof_node'),    
        Node(package='kd1_locomotion', executable='wheel_odometry_node', name='wheel_odometry_node'), 
        Node(package='kd1_locomotion', executable='motor_driver_comms_node', name='motor_driver_comms_node'),
        Node(package='kd1_locomotion', executable='emergency_stop_node', name='emergency_stop_node'),
                
        # sensors
        Node(package='kd1_sensors', executable='audio_direction_node', name='audio_direction_node'),
        Node(package='kd1_sensors', executable='oak_depthai_node', name='oak_depthai_node'),
        Node(package='kd1_sensors', executable='voice_recognition_node', name='voice_recognition_node'),    
        
        # utility
        Node(package='kd1_utility_nodes', executable='audio_playback_node', name='audio_playback_node'), 
        Node(package='kd1_utility_nodes', executable='face_animation_node', name='face_animation_node'),
        Node(package='kd1_utility_nodes', executable='light_ring_node', name='light_ring_node'),
        Node(package='kd1_utility_nodes', executable='imu_conversion_node', name='imu_conversion_node'),
        
        # navigation
        Node(package='kd1_navigation', executable='navigation_node', name='navigation_node'),
        Node(package='kd1_navigation', executable='custom_costmap_node', name='custom_costmap_node'),
    ]
    
    
    ############
    ### NAV2 ###
    ############
    
    ### only used for creating local and global costmap ###
        
    nav2_launch = TimerAction(
        period=1.0,  # 1 second delay
        actions=[
            IncludeLaunchDescription(
                PythonLaunchDescriptionSource([
                    PathJoinSubstitution([
                        FindPackageShare("nav2_bringup"),
                        "launch",
                        "navigation_launch.py"
                    ])
                ]),
                launch_arguments={
                    'use_sim_time': 'false',
                    'autostart': 'true',
                    'params_file': os.path.join(pkg_share, 'config/nav2_params.yaml'),
                    'map_subscribe_transient_local': 'true',
                    'use_map_topic': 'false', # was true
                    'use_simulator': 'false',
                    'use_rviz': 'false',
                    'headless': 'true'
                }.items()
            )
        ]
    )

    
    ####################
    ### CENTRAL NODE ###
    ####################
    
    central_processing_node = Node(
        package='kd1_central_processing',
        executable='central_processing_node',
        name='central_processing_node',
    )  
    

    return LaunchDescription([            
        robot_state_pub_node,
        robot_localization_node,
        *secondary_nodes,
        #nav2_launch,
        central_processing_node
    ])