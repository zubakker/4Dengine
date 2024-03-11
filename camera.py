# (12.03.22:)
from math import atan2, sqrt, tan

from geometry import Point, Rotation



class Camera:
    position: Point 
    rotation: Rotation 

    def move_by( self, coordinates: list[ float ] ):
        for i in range( len(coordinates) ):
            self.position[i] += coordinates[i]


    def move_to( self, coordinates: Point ):
        for i in range( len(coordinates) ):
            self.position[i] = coordinates[i]


    def rotate_by( self, angles: Rotation ):
        self.rotation = self.rotation + angles


    # TODO
    # def project_point ????
    # def project_edge ????
    # def project_triangle ????
    # ???


class CameraP3D( Camera ): # 3D to 2D camera with perspective
    def __init__( self, 
                  pos: Point,  # a list of three coordinates
                  rot: Rotation,  
                  dist: float ): 
        self.position = pos
        self.rotation = rot

        self.screen_distance = dist # self.resolution / 2*tan(self.FOV/2) 


    def project_edge( self, coordinates: list[ Point, Point ]):
        x1, y1 = self.project_point( coordinates[0] )
        x2, y2 = self.project_point( coordinates[1] )

        return [ [x1, y1], [x2, y2] ]


    def project_point( self, coordinates: Point ):
        X, Y, Z = coordinates[:3]
        dX = X - self.position[0]
        dY = Y - self.position[1]
        dZ = Z - self.position[2]
        #  find angle to the point
        angle_h = atan2( dY, dX )
        angle_v = atan2( dZ, sqrt(dX*dX + dY*dY) )
        #  substitute view angles
        angle_h -= self.rotation[0]
        angle_v -= self.rotation[1]
        #  sin & cos of angle * screen distance
        horiz_pos = tan(angle_h) * self.screen_distance
        vert_pos = tan(angle_v) * self.screen_distance

        return (horiz_pos, vert_pos)




class CameraS4D( Camera ): # 4D to 3D camera without perspective
    # TODO
    pass


class CameraP4D( Camera ): # 4D to 3D camera with perspective
    def __init__( self, 
                  pos: Point,  # a list of three coordinates
                  rot: Rotation,  
                  dist: float ):  # distance between the focal point 
                                  # and the screen space
        self.position = pos
        self.rotation = rot

        self.screen_distance = dist 


    def project_edge( self, coordinates: list[ Point, Point ]):
        x1, y1, z1 = self.project_point( coordinates[0] )
        x2, y2, z2 = self.project_point( coordinates[1] )

        return [ [x1, y1, z1], [x2, y2, z2] ]


    def project_point( self, coordinates: Point ):
        deltas = list()
        for i in range( len(coordinates) ):
            deltas.append( coordinates[i] - self.position[i] )

        point_rotation = Rotation( [ atan2( deltas[1], deltas[0] ) ] )
        deltas_square_sum = deltas[0]**2
        for i in range( 2, len(coordinates) ):
            deltas_square_sum += deltas[i-1]**2
            point_rotation.append( atan2( deltas[i], sqrt(deltas_square_sum) ) )


        res_rotation = point_rotation - self.rotation

        result_point = Point()
        for i in range(3):
            result_point.append( tan(res_rotation.angles[i]) * self.screen_distance )


        return result_point

    def project_triangle( self, coordinates: list[ Point, Point, Point ] ):
        x1, y1, z1 = self.project_point( coordinates[0] )
        x2, y2, z2 = self.project_point( coordinates[1] )
        x3, y3, z3 = self.project_point( coordinates[3] )

        return [ [x1, y1, z1], [x2, y2, z2], [x3, y3, z3] ]
        # return [horiz_pos2, vert_pos2, front_pos2]


class CameraPerspective( Camera ):
    def __init__( self, 
                  pos: Point,  # a list of three coordinates
                  rot: Rotation,  
                  dist: float ):  # distance between the focal point 
                                  # and the screen space
        self.position = pos
        self.rotation = rot

        self.screen_distance = dist 


    def project_edge( self, coordinates: list[ Point, Point ], 
                res_dimension: int ) -> list[ Point, Point ]:
        if coordinates[0].dimension > res_dimension:
            projected_p1 = self.project_point( coordinates[0], res_dimension )
            projected_p2 = self.project_point( coordinates[1], res_dimension )

            return [ projected_p1, projected_p2 ]
        else:
            return coordinates

    def project_triangle( self, coordinates: list[ Point, Point, Point],
                res_dimension: int) -> list[ Point, Point, Point ]:
        if coordinates[0].dimension > res_dimension:
            projected_p1 = self.project_point( coordinates[0], res_dimension )
            projected_p2 = self.project_point( coordinates[1], res_dimension )
            projected_p3 = self.project_point( coordinates[2], res_dimension )

            return [ projected_p1, projected_p2, projected_p3 ]
        else:
            return coordinates



    def project_point( self, coordinates: Point, res_dimension: int ) -> Point:
        if res_dimension == len( coordinates ):
            return coordinates

        deltas = list()
        for i in range( len(coordinates) ):
            if i > len(self.position) - 1 : 
                deltas.append( coordinates[i] ) # assume camera's coordinate is 0
            else:
                deltas.append( coordinates[i] - self.position[i] )

        point_rotation = Rotation()
        planes = point_rotation.get_planes( len(coordinates) )
        for plane in planes:
            angle = atan2( deltas[ plane[0] ], deltas[ plane[1] ] )
            point_rotation.append( angle )
        """
        deltas_square_sum = deltas[0]**2
        for i in range( 2, len(coordinates) ):
            deltas_square_sum += deltas[i-1]**2
            point_rotation.append( atan2( deltas[i], sqrt(deltas_square_sum) ) )

        """
        result_rotation = point_rotation # - self.rotation
        # print(result_rotation.angles)

        projected_point = Point()
        for i in range( len(coordinates) - 1 ):
            projected_point.append( tan(result_rotation[i]) * self.screen_distance )

        projected_point2 = Point()
        for i in range( len(coordinates) - 1 ):
            projected_point2.append( tan(result_rotation[3+i]) * self.screen_distance )

        
        if res_dimension < len( projected_point ):
            projected_point = self.project_point( projected_point, res_dimension )
        
        return projected_point2



import pygame
from math import sin, cos

class Camera2:
    def __init__( self, resolution, position, rotation, map ):
        self.resolution = resolution
        self.position = position
        self.map = map
        self.display = pygame.display.set_mode(resolution)

        self.rotation = [0, 0] 
        
        self.vectors = list()
        self.coords = [ [1, 0, 0], [0, 1, 0], [0, 0, 1] ]
        for i in range(self.resolution[0]):
            row = list()
            for j in range(self.resolution[1]):
                row.append([1, 1 - 2*j/self.resolution[0], 1 - 2*i/self.resolution[1]])
            self.vectors.append(row)
        self.rotate(rotation[0], rotation[1])
    def set_map(self, map):
        self.map = map
    def add_plane(self, plane):
        self.map.append(plane)

    def render(self):
        self.display.fill((0,0,0))
        '''
        # TEMP:
        for j in range(self.resolution[0]):
            plane = self.map[0]
            point = plane.get_point(self.vectors[25][j], self.position)
            dist = plane.get_dist_sq(point, self.position)
            t = plane.check_inside(point)
            print(t, end=', ')
        print()
        # 
        '''
        screen2 = [[None]*self.resolution[1] for x in range(self.resolution[0])]
        for plane in self.map:
            for i in range(self.resolution[0]):
                color = plane.get_color()
                left_border = None
                right_border = None
                lbord = 0
                rbord = self.resolution[0] -1
                lmid = lbord + (rbord - lbord) // 3
                rmid = lbord + 2*(rbord - lbord) // 3

                olb, orb, olm, orm = None, None, None, None
                while left_border == None or right_border == None:
                    if lbord != olb:
                        lpoint = plane.get_point(self.vectors[i][lbord], self.position)
                        tl = plane.check_inside(lpoint)
                        olb = lbord
                        j = lbord

                        dx = lpoint[0] - self.position[0]
                        dy = lpoint[1] - self.position[1]
                        dz = lpoint[2] - self.position[2]
                        if dx * self.vectors[i][j][0] < 0 or \
                                dy * self.vectors[i][j][1] < 0 or \
                                dz * self.vectors[i][j][2] < 0:
                            pass
                        else:
                            dist = dx*dx + dy*dy + dz*dz
                            if tl < -1 and (screen2[i][j] == None or \
                                    (screen2[i][j][0] > dist and screen2[i][j][1] != color)):
                                self.display.set_at((j, i), color)
                                screen2[i][j] = (dist, color)
                    if rbord != orb:
                        rpoint = plane.get_point(self.vectors[i][rbord], self.position)
                        tr = plane.check_inside(rpoint)
                        orb = rbord
                        j = rbord

                        dx = rpoint[0] - self.position[0]
                        dy = rpoint[1] - self.position[1]
                        dz = rpoint[2] - self.position[2]
                        if dx * self.vectors[i][j][0] < 0 or \
                                dy * self.vectors[i][j][1] < 0 or \
                                dz * self.vectors[i][j][2] < 0:
                            pass
                        else:
                            dist = dx*dx + dy*dy + dz*dz
                            if tr < -1 and (screen2[i][j] == None or \
                                    (screen2[i][j][0] > dist and screen2[i][j][1] != color)):
                                self.display.set_at((j, i), color)
                                screen2[i][j] = (dist, color)
                    if lmid != olm:
                        lmpoint = plane.get_point(self.vectors[i][lmid], self.position)
                        tlm = plane.check_inside(lmpoint)
                        olm = lmid
                        j = lmid

                        dx = lmpoint[0] - self.position[0]
                        dy = lmpoint[1] - self.position[1]
                        dz = lmpoint[2] - self.position[2]
                        if dx * self.vectors[i][j][0] < 0 or \
                                dy * self.vectors[i][j][1] < 0 or \
                                dz * self.vectors[i][j][2] < 0:
                            pass
                        else:
                            dist = dx*dx + dy*dy + dz*dz
                            if tlm < -1 and (screen2[i][j] == None or \
                                    (screen2[i][j][0] > dist and screen2[i][j][1] != color)):
                                self.display.set_at((j, i), color)
                                screen2[i][j] = (dist, color)
                    if rmid != orm:
                        rmpoint = plane.get_point(self.vectors[i][rmid], self.position)
                        trm = plane.check_inside(rmpoint)
                        orm = rmid
                        j = rmid

                        dx = rmpoint[0] - self.position[0]
                        dy = rmpoint[1] - self.position[1]
                        dz = rmpoint[2] - self.position[2]
                        if dx * self.vectors[i][j][0] < 0 or \
                                dy * self.vectors[i][j][1] < 0 or \
                                dz * self.vectors[i][j][2] < 0:
                            pass
                        else:
                            dist = dx*dx + dy*dy + dz*dz
                            if trm < -1 and (screen2[i][j] == None or \
                                    (screen2[i][j][0] > dist and screen2[i][j][1] != color)):
                                self.display.set_at((j, i), color)
                                screen2[i][j] = (dist, color)

                    if rbord == lbord:
                        right_border = 0
                        left_border = 0
                        
                    if tl <= -1 and left_border == None:
                        left_border = lbord
                        continue
                    if tr <= -1 and right_border == None:
                        right_border = rbord
                        continue

                    # тут высчитываем точки и тл
                    if tlm <= -1 and left_border == None:
                        if lmid - lbord <= 1:
                            left_border = lmid
                            lbord = lmid
                            continue
                        lmid = (lmid + lbord)//2
                    if trm <= -1 and right_border == None:
                        if rbord - rmid <= 1:
                            right_border = rmid
                            rbord = rmid
                            continue
                        rmid = (rmid + rbord)//2
                    
                    if lmid - lbord <= 0 and left_border == None:
                        left_border = lmid
                        lbrod = lmid
                        continue
                    if rbord - rmid <= 0 and right_border == None:
                        right_border = rmid
                        rbrod = rmid
                        continue
                    # 0 0 0 0: 
                    if tlm > -1 and left_border == None and \
                            trm > -1 and right_border == None:
                        if trm > tlm:
                            rbord = rmid
                            lmid = lbord + (rbord - lbord) // 3
                            rmid = lbord + 2*(rbord - lbord) // 3
                            continue
                        if tlm > trm:
                            lbord = lmid
                            lmid = lbord + (rbord - lbord) // 3
                            rmid = lbord + 2*(rbord - lbord) // 3
                            continue

                    if tlm > -1 and left_border == None:
                        lbord = lmid
                        lmid = lbord + (rbord - lbord)//3
                    if trm > -1 and right_border == None:
                        rbord = rmid
                        rmid = lbord + 2*(rbord - lbord)//3

                for j in range(left_border, right_border):
                    color = plane.get_color()

                    if screen2[i][j] != None and screen2[i][j][1] == color:
                        continue
                    point = plane.get_point( self.vectors[i][j], self.position )
                    dx = point[0] - self.position[0]
                    dy = point[1] - self.position[1]
                    dz = point[2] - self.position[2]
                    if dx * self.vectors[i][j][0] < 0 or \
                            dy * self.vectors[i][j][1] < 0 or \
                            dz * self.vectors[i][j][2] < 0:
                        continue
                    dist = dx*dx + dy*dy + dz*dz
                    # dist = plane.get_dist_sq(point, self.position)
                    if plane.check_inside(point) <= -1:
                        if screen2[i][j] == None or (screen2[i][j][0] > dist and \
                                screen2[i][j][1] != color):
                            self.display.set_at((j, i), color)
                            screen2[i][j] = (dist, color)

                    
            
        '''
        for i in range(self.resolution[0]):
            for j in range(self.resolution[1]):
                min_dist = None
                color = None 
                for plane in self.map:
                    point = plane.get_point( self.vectors[i][j], self.position )
                    dist = plane.get_dist_sq(point, self.position)
                    if plane.check_inside(point) <= -1:
                        if min_dist == None or dist < min_dist:
                            min_dist = dist
                            color = plane.get_color()
                if color:
                    self.display.set_at((i, j), color)
                    '''
        pygame.display.update()

    def move(self, d_pos):
        dx, dy, dz = d_pos
        forw, left, upward = self.coords
        self.position[0] += dx*forw[0] + dy*left[0] + dz*upward[0]
        self.position[1] += dx*forw[1] + dy*left[1] + dz*upward[1]
        self.position[2] += dx*forw[2] + dy*left[2] + dz*upward[2]
        print(self.position)

    def rotate(self, ang_hor, ang_ver):
        # TEMP: only horizontal rotation
        sin_h = sin(ang_hor)
        cos_h = cos(ang_hor)
        sin_v = sin(ang_ver)
        cos_v = cos(ang_ver)
        for i in range(self.resolution[0]):
            for j in range(self.resolution[1]):
                x, y, z = self.vectors[i][j]
                x1 = x*cos_h -y*sin_h
                y1 = x*sin_h +y*cos_h

                x2 = x1*cos_v -z*sin_v
                z2 = x1*sin_v +z*cos_v
                self.vectors[i][j] = [x2, y1, z2]
        for i in range(len(self.coords)):
            x, y, z = self.coords[i]
            x1 = x*cos_h -y*sin_h
            y1 = x*sin_h +y*cos_h

            x2 = x1*cos_v -z*sin_v
            z2 = x1*sin_v +z*cos_v
            self.coords[i] = [x2, y1, z2]







