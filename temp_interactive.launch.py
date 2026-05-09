
import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    pkg_dir = get_package_share_directory('robot_proximity')
    
    # Try looking in the source directory first so changes take effect without rebuilding
    src_config_dir = '/home/jatin/ros2_assign_2_10_robo_modified_tonew/hehe_to_trutle/src/robot_proximity/config/simulation.rviz'
    if os.path.exists(src_config_dir):
        rviz_config_dir = src_config_dir
    else:
        rviz_config_dir = os.path.join(pkg_dir, 'config', 'simulation.rviz')

    # User Defined Robots
    robots = [{'id': 'robot1', 'color': 'red', 'path': 'A1,A2,A3,A4,A5,A6,A7,A8,A9,A10,B10,C10,D10,E10,F10,G10,H10', 'speed': 0.8, 'radius': 2.0}, {'id': 'robot2', 'color': 'blue', 'path': 'A1,B1,C1,D1,E1,F1,G1,H1,H2,H3,H4,H5,H6,H7,H8,H9,H10', 'speed': 0.8, 'radius': 2.0}, {'id': 'robot3', 'color': 'green', 'path': 'A1,A2,A3,B3,B4,C4,C5,D5,D6,E6,E7,F7,F8,G8,G9,H9,H10', 'speed': 0.8, 'radius': 2.0}]

    robot_nodes = []
    robot_ids = []

    for r in robots:
        robot_ids.append(r['id'])
        robot_nodes.append(
            Node(
                package='robot_proximity',
                executable='robot_node',
                name=r['id'],
                parameters=[{
                    'robot_id': r['id'],
                    'color': r['color'],
                    'path': r['path'],
                    'speed': r['speed'],
                    'radius': r['radius']
                }],
                output='screen'
            )
        )

    return LaunchDescription([
        *robot_nodes,

        Node(
            package='robot_proximity',
            executable='proximity_monitor',
            name='proximity_monitor',
            parameters=[{
                'threshold': 3.5,
                'robot_ids': ','.join(robot_ids)
            }],
            output='screen'
        ),
        Node(
            package='robot_proximity',
            executable='graph_visualizer',
            name='graph_visualizer',
            parameters=[{'spawn_interval': 6.0}],
            output='screen'
        ),
        Node(
            package='rviz2',
            executable='rviz2',
            name='rviz2',
            arguments=['-d', rviz_config_dir],
            output='screen'
        )
    ])
