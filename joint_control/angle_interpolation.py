'''In this exercise you need to implement an angle interploation function which makes NAO executes keyframe motion

* Tasks:
    1. complete the code in `AngleInterpolationAgent.angle_interpolation`,
       you are free to use splines interploation or Bezier interploation,
       but the keyframes provided are for Bezier curves, you can simply ignore some data for splines interploation,
       please refer data format below for details.
    2. try different keyframes from `keyframes` folder

* Keyframe data format:
    keyframe := (names, times, keys)
    names := [str, ...]  # list of joint names
    times := [[float, float, ...], [float, float, ...], ...]
    # times is a matrix of floats: Each line corresponding to a joint, and column element to a key.
    keys := [[float, [int, float, float], [int, float, float]], ...]
    # keys is a list of angles in radians or an array of arrays each containing [float angle, Handle1, Handle2],
    # where Handle is [int InterpolationType, float dTime, float dAngle] describing the handle offsets relative
    # to the angle and time of the point. The first Bezier param describes the handle that controls the curve
    # preceding the point, the second describes the curve following the point.
'''


from pid import PIDAgent
from keyframes import hello


class AngleInterpolationAgent(PIDAgent):
    def __init__(self, simspark_ip='localhost',
                 simspark_port=3100,
                 teamname='DAInamite',
                 player_id=0,
                 sync_mode=True):
        super(AngleInterpolationAgent, self).__init__(simspark_ip, simspark_port, teamname, player_id, sync_mode)
        self.keyframes = ([], [], [])

    def think(self, perception):
        target_joints = self.angle_interpolation(self.keyframes, perception)
        self.target_joints.update(target_joints)
        return super(AngleInterpolationAgent, self).think(perception)

    def angle_interpolation(self, keyframes, perception):
        target_joints = {}
        # YOUR CODE HERE

        names = keyframes[0]
        keys = keyframes[2]
        times = keyframes[1]

        '''
        keys --> list of list of keys (contains keylists for HeadYaw, HeadPitch etc)
        keys[k] --> list of keys for specific joint
        keys [k][j] --> specific key --> contains angle, handle1, Handle2
        '''

        mod_time = perception.time % 4.60000

        for k in range(0, len(times)) :
            keylist = keys[k]
            timelist = times[k]
            last_time = 0
            for j in range(0, len(timelist)) :

                curr = getcurr(j, timelist, mod_time)
                next = getnext(curr, timelist)

                if (timelist[curr] <= mod_time and timelist[next] >= mod_time) \
                        or (j == 0 and timelist[j] >= mod_time)  \
                        or (j == len(timelist)-1 and timelist[j] <= mod_time) :

                    for i in range (0, 10) :

                        t = i/10.0

                        curr_time = timelist[curr]
                        next_time = timelist[next]
                        t1 = curr_time + keylist[curr][2][1]
                        t2 = next_time - keylist[next][2][1]

                        current_angle = keylist[curr][0]
                        next_angle = keylist[next][0]
                        p1 = current_angle + keylist[curr][2][2]        #dAngle of Handle1 of the curr point
                        p2 = next_angle - keylist[next][1][2]           #dAngle of Handle2 of the next point

                        bezier_val = bezier(current_angle, p1, p2, next_angle, t)
                        bezier_time = bezier(curr_time, t1, t2, next_time, t)

                        if last_time <= mod_time and bezier_time >= mod_time :
                            target_joints[names[k]] = bezier_val
                            #print str(bezier_val) + "     " + names[k]
                            break

                        last_time = bezier_time

                    break

        return target_joints

def bezier(start, p1, p2, end, t) :
    term0 = (1 - t) ** 3 * start
    term1 = 3 * (1 - t) ** 2 * t * p1
    term2 = 3 * (1 - t) * t ** 2 * p2
    term3 = t ** 3 * end

    return term0 + term1 + term2 + term3

def getnext(curr, timelist) :
    if curr == len(timelist) - 1:
        return 0
    return curr + 1

def getcurr(j, timelist, mod_time) :
    if j == 0 and timelist[j] >= mod_time:
        return len(timelist) - 1
    return j


if __name__ == '__main__':
    agent = AngleInterpolationAgent()
    agent.keyframes = hello()  # CHANGE DIFFERENT KEYFRAMES
    agent.run()

