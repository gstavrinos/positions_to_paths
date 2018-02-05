#!/usr/bin/env python
import rospy
from nav_msgs.msg import Path
from geometry_msgs.msg import PoseStamped
from gazebo_msgs.msg import ModelStates

pubs = []
models = []
paths = []
cnt = 0

def init():
    global models, pubs, paths
    rospy.init_node('positions_to_paths')
    models = rospy.get_param('~models', ['bebop', 'marker3'])
    print models
    rospy.Subscriber('gazebo/model_states', ModelStates, gazebo_callback)
    for m in models:
        pubs.append(rospy.Publisher('positions_to_paths/'+m+'/path', Path, queue_size=1))
        path = Path()
        path.header.stamp = rospy.Time.now()
        path.header.frame_id = '/odom'
        paths.append(path)
    while not rospy.is_shutdown():
        rospy.spin()

def gazebo_callback(msg):
    global models, pubs, paths, cnt
    cnt += 1
    for i in range(len(models)):
        for j in range(len(msg.name)):
            if models[i] == msg.name[j]:
                ps = PoseStamped()
                ps.header.stamp = rospy.Time.now()
                ps.pose = msg.pose[j]
                found = False
                '''for p in paths[i].poses:
                    if ps.pose.position.x == p.pose.position.x and ps.pose.position.y == p.pose.position.y and ps.pose.position.z == p.pose.position.z and ps.pose.orientation.x == p.pose.orientation.x and ps.pose.orientation.y == p.pose.orientation.y and ps.pose.orientation.z == p.pose.orientation.z and ps.pose.orientation.w == p.pose.orientation.w:
                        found = True
                        break
                '''
                if not found:
                    paths[i].poses.append(ps)
        if cnt > 200:
            cnt = 0
        if cnt == 0:
            pubs[i].publish(paths[i])

if __name__ == '__main__':
    init()