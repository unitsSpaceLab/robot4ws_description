#!/usr/bin/env python3

import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import Command, LaunchConfiguration
from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue


def generate_launch_description():
    # Package directory
    pkg_robot4ws_description = get_package_share_directory('robot4ws_description')

    # Paths
    urdf_file = os.path.join(pkg_robot4ws_description, 'urdf', 'rover.urdf.xacro')
    rviz_file = os.path.join(pkg_robot4ws_description, 'rviz', 'default.rviz')

    # Arguments
    model_arg = DeclareLaunchArgument(
        'model',
        default_value=urdf_file,
        description='Path to robot URDF file'
    )

    use_sim_time_arg = DeclareLaunchArgument(
        'use_sim_time',
        default_value='false',
        description='Use simulation time'
    )

    # Robot description
    robot_description = Command([
        'xacro ', LaunchConfiguration('model'),
        ' rocker_differential:=true',
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

    # Joint state publisher
    joint_state_publisher = Node(
        package='joint_state_publisher',
        executable='joint_state_publisher',
        name='joint_state_publisher',
        parameters=[{'use_sim_time': LaunchConfiguration('use_sim_time')}]
    )

    # RViz2
    rviz = Node(
        package='rviz2',
        executable='rviz2',
        name='archimede_rviz_node',
        arguments=['-d', rviz_file],
        parameters=[{'use_sim_time': LaunchConfiguration('use_sim_time')}]
    )

    return LaunchDescription([
        model_arg,
        use_sim_time_arg,
        robot_state_publisher,
        joint_state_publisher,
        rviz
    ])
