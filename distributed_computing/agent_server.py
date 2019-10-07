'''In this file you need to implement remote procedure call (RPC) server

* There are different RPC libraries for python, such as xmlrpclib, json-rpc. You are free to choose.
* The following functions have to be implemented and exported:
 * get_angle
 * set_angle
 * get_posture
 * execute_keyframes
 * get_transform
 * set_transform
* You can test RPC server with ipython before implementing agent_client.py
'''

# add PYTHONPATH
import os
import sys
from SimpleXMLRPCServer import SimpleXMLRPCServer
import xmlrpclib
sys.path.append(os.path.join(os.path.abspath(os.path.dirname(__file__)), '..', 'kinematics'))

from inverse_kinematics import InverseKinematicsAgent
from recognize_posture import PostureRecognitionAgent


class ServerAgent(InverseKinematicsAgent, PostureRecognitionAgent): #else we can't recognize posture
    '''ServerAgent provides RPC service
    '''
    # YOUR CODE HERE
    def get_angle(self, joint_name):
        '''get sensor value of given joint'''
        # YOUR CODE HERE
        angle = self.perception.joint[joint_name]
        return angle

    def set_angle(self, joint_name, angle):
        '''set target angle of joint for PID controller
        '''
        self.perception.joint[joint_name] = angle
        # YOUR CODE HERE

    def get_posture(self):
        '''return current posture of robot'''
        # YOUR CODE HERE
        return self.recognize_posture(self.perception)

    def execute_keyframes(self, keyframes):
        '''excute keyframes, note this function is blocking call,
        e.g. return until keyframes are executed
        '''
        # YOUR CODE HERE
        self_keyframes = keyframes
        self.run()

    def get_transform(self, name):
        '''get transform with given name
        '''
        # YOUR CODE HERE
        return self.transforms(name)

    def set_transform(self, effector_name, transform):
        '''solve the inverse kinematics and control joints use the results
        '''
        # YOUR CODE HERE
        self.set_transform(effector_name, transform)

if __name__ == '__main__':
    #basic source code for RPC : https://docs.python.org/2/library/xmlrpclib.html

    server = SimpleXMLRPCServer(("localhost", 4445))
    print "Listening on port 4445"

    #register used functions
    server.register_function(ServerAgent.get_angle, "get_angle")
    server.register_function(ServerAgent.set_angle, "set_angle")
    server.register_function(ServerAgent.get_posture, "get_posture")
    server.register_function(ServerAgent.execute_keyframes, "execute_keyframes")
    server.register_function(ServerAgent.get_transform, "get_transform")
    server.register_function(ServerAgent.set_transform, "set_transform")


    agent = ServerAgent()
    server.register_instance(agent)
    server.serve_forever()

    agent.run()



