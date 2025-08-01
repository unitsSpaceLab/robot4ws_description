#!/usr/bin/env python3

import os
from pathlib import Path

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, ExecuteProcess
from launch.substitutions import Command, LaunchConfiguration
from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue


def generate_launch_description():
    # Package directories  
    pkg_robot4ws_description = get_package_share_directory('robot4ws_description')

    #( questa robba non dovere essere qui)
    mesh_path = os.path.join(pkg_robot4ws_description, 'meshes')
    current_path = os.environ.get('GZ_SIM_RESOURCE_PATH', '')
    os.environ['GZ_SIM_RESOURCE_PATH'] = f"{current_path}:{pkg_robot4ws_description}:{mesh_path}"

    # Paths
    urdf_file = os.path.join(pkg_robot4ws_description, 'urdf', 'rover.urdf.xacro')
    bridge_config_file = os.path.join(pkg_robot4ws_description, 'config', 'bridge_config.yaml')

    # Launch arguments
    use_sim_time_arg = DeclareLaunchArgument(
        'use_sim_time',
        default_value='true',
        description='Use simulation time'
    )
    arg_add_velodyne = DeclareLaunchArgument(
        'add_velodyne',
        default_value='false',
        description='Add simulated velodyne 3d lidar'
    )

    # Robot description
    robot_description = Command([
        'xacro ', urdf_file,
        ' add_velodyneHDL32E:=', LaunchConfiguration('add_velodyne'),
        ' use_sim_time:=', LaunchConfiguration('use_sim_time')
    ])

    # Robot state publisher
    robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        name='robot_state_publisher',
        parameters=[{
            'robot_description': ParameterValue(robot_description, value_type=str),
            'use_sim_time': LaunchConfiguration('use_sim_time')
        }]
    )

    # Gazebo Harmonic launch (direct gz sim command)
    gazebo = ExecuteProcess(
        cmd=['gz', 'sim', '-v', '4', 'empty.sdf'],
        output='screen'
    )

    # Spawn robot
    spawn_robot = Node(
        package='ros_gz_sim',
        executable='create',
        arguments=[
            '-topic', 'robot_description',
            '-name', 'archimede_rover',
            '-z', '0.5'
        ],
        parameters=[{'use_sim_time': LaunchConfiguration('use_sim_time')}]
    )

    # ROS-Gazebo bridge
    # bridge = Node(
    #     package='ros_gz_bridge',
    #     executable='parameter_bridge',
    #     arguments=[
    #         '/clock@rosgraph_msgs/msg/Clock[gz.msgs.Clock',
    #         '/cmd_vel@geometry_msgs/msg/Twist@gz.msgs.Twist',
    #         '/odom@nav_msgs/msg/Odometry[gz.msgs.Odometry',
    #         '/joint_states@sensor_msgs/msg/JointState[gz.msgs.Model',
    #         '/scan@sensor_msgs/msg/LaserScan[gz.msgs.LaserScan',
    #         '/imu@sensor_msgs/msg/Imu[gz.msgs.IMU',
    #         '/Archimede/cmd_vel_motors@actuator_msgs/msg/Actuators]gz.msgs.Actuators',
    #     ],
    #     parameters=[{'use_sim_time': LaunchConfiguration('use_sim_time')}]
    # )

    # ROS-Gazebo bridge
    bridge = Node(
        package='ros_gz_bridge',
        executable='parameter_bridge',
        parameters=[{'use_sim_time': LaunchConfiguration('use_sim_time')},
                    {'config_file': bridge_config_file}]
    )

    return LaunchDescription([
        use_sim_time_arg,
        arg_add_velodyne,
        robot_state_publisher,
        gazebo,
        spawn_robot,
        bridge
    ])
