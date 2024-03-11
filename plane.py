from math import sqrt

class Plane:
    # points = list[ list['x','y','z'] ]
    # color = (0...255)*3
    # A, B, C, D = float, float, float, float

    def __init__( self, points, color ):
        self.points = points
        v1 = [points[0][0] - points[1][0], 
              points[0][1] - points[1][1], 
              points[0][2] - points[1][2]]
        v2 = [points[0][0] - points[2][0], 
              points[0][1] - points[2][1], 
              points[0][2] - points[2][2]]
        self.color = color

        self.A = v1[1]*v2[2] - v1[2]*v2[1]
        self.B = v1[2]*v2[0] - v1[0]*v2[2]
        self.C = v1[0]*v2[1] - v1[1]*v2[0]
        self.D = points[0][0]*(v1[2]*v2[1]-v1[1]*v2[2]) + \
                    points[0][1]*(v1[0]*v2[2]-v1[2]*v2[0]) + \
                    points[0][2]*(v1[1]*v2[0]-v1[0]*v2[1]) 

    def get_color(self):
        return self.color

    def get_point(self, vector, point ):
        vx, vy, vz = vector
        x0, y0, z0 = point
        # print('ABCD', self.A, self.B, self.C, self.D)
        # print('Points', [str(point) + " " for point in self.points])
        # print('Vyvxvy/vx', vy, vx, vy/vx)
        if (self.A + self.B*vy/vx + self.C*vy/vx) == 0:
            return [99999999, 99999999, 99999999] 
        x = (self.B*vy*x0/vx + self.C*vz*x0/vx - self.B*y0 - self.C*z0 - self.D) / (self.A + self.B*vy/vx + self.C*vy/vx)

        y = vy/vx*(x-x0) + y0
        z = vz/vx*(x-x0) + z0
        return [x,y,z]

    def check_inside(self, point ):
        av = [point[0] - self.points[0][0], 
              point[1] - self.points[0][1],
              point[2] - self.points[0][2]]
        av_sq = sqrt(av[0]**2 + av[1]**2 + av[2]**2)
        if av_sq == 0:
            # return True
            return -1
        av = [av[0]/av_sq, av[1]/av_sq, av[2]/av_sq]
        bv = [point[0] - self.points[1][0], 
              point[1] - self.points[1][1],
              point[2] - self.points[1][2]]
        bv_sq = sqrt(bv[0]**2 + bv[1]**2 + bv[2]**2)
        if bv_sq == 0:
            # return True
            return -1
        bv = [bv[0]/bv_sq, bv[1]/bv_sq, bv[2]/bv_sq]
        cv = [point[0] - self.points[2][0], 
              point[1] - self.points[2][1],
              point[2] - self.points[2][2]]
        cv_sq = sqrt(cv[0]**2 + cv[1]**2 + cv[2]**2)
        if cv_sq == 0:
            # return True
            return -1
        cv = [cv[0]/cv_sq, cv[1]/cv_sq, cv[2]/cv_sq]

        t = av[0]*(bv[0]+cv[0]) + av[1]*(bv[1]+cv[1]) + \
                av[2]*(bv[2]+cv[2]) + bv[0]*cv[0]+bv[1]*cv[1]+bv[2]*cv[2]

        return t
        if t < -1:
            return True
        else:
            return False

    def get_dist_sq(self, point_one, point_two):
        dx = point_one[0]-point_two[0]
        dy = point_one[1]-point_two[1]
        dz = point_one[2]-point_two[2]
        return dx*dx + dy*dy + dz*dz
