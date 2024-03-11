# (15.03.22:)
from math import atan2, sin, cos, sqrt

from geometry import Point, Rotation


class Figure:
    points: list[ Point ] # -> 
            # list of three N-dimentional points' coordinates:
    # I'm not sure if a list of edges will be needed # TODO
    """
    edges: list[ list[ list[ float] ] ] # -> 
            # list of three pairs of N-dimentional poinsts' coordinates:
    """
    dimentions: int # N for N-dimentional figure

    center_point: Point # ->
            # N-dimentional coordinates of the "central" point of the
            # figure
    edges: list[ list[ int, int ] ] # ->
            # a list of pairs of indexes of points that are connected
            # with an edge
    triangles: list[ list[ int, int, int ] ] # ->
            # a list of triplets of indexes of points that are connected
            # with a triangle

    def __init__( self, 
                  points: list[ Point ],
                  edges: list[ list[ int, int ] ],
                  triangles: list[ list[ int, int, int ] ],
                  center_point: Point,
                  dimentions: int):
        self.points = points.copy()
        self.center_point = center_point.copy()
        self.dimentions = dimentions
        self.edges = edges
        self.triangles = triangles

    def move_by( self, coordinates: list[ float ] ): # move all of the points
        for i in range( len(coordinates) ):
            for j in range( len( points ) ):
                self.points[j][i] += coordinates[i]
            self.center_point[i] += coordinates[i]

    def move_to( self, coordinates: Point ): # -> 
                # move all the points,
                # so that the center point moves to given coordinates
        # TODO
        pass

    def rotate_by( self, angles: Rotation ): # ->
                    # angles in radian, N angles
                    # rotates around self.center_point

        for point in self.points:
            for i in range( len(angles.angles) ):
                plane = angles.planes[i]
                dfirst = point[ plane[0] ] - self.center_point[ plane[0] ]
                dsecond = point[ plane[1] ] - self.center_point[ plane[1] ]
                distance = sqrt( dfirst**2 + dsecond**2 )

                angle = atan2( dsecond, dfirst ) + angles.angles[ i ]

                point[ plane[0] ] = distance * cos( angle )
                point[ plane[1] ] = distance * sin( angle )

    def transform( self ): # ( TODO ): # move only some points
        # TODO
        pass

    def get_edges( self ):
        result = list()
        for edge in self.edges:
            start_point = self.points[ edge[0] ]
            end_point = self.points[ edge[1] ]
            result.append( [ start_point, end_point ] )
        return result

    def get_triangles( self ):
        result = list()
        for triangle in self.triangles:
            p1 = self.points[ triangle[0] ]
            p2 = self.points[ triangle[1] ]
            p3 = self.points[ triangle[2] ]
            result.append( [p1, p2, p3] )
        return result








