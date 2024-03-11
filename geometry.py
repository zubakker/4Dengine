# (01.04.22:)
from typing_extensions import Self


class GeomtryObject:
    # TODO
    pass

class Space:
    # TODO
    pass

class Rotation: 
        # a collection simple rotations in cardinal planes that produce
        # any complex rotation.
        
        # This class object only stores rotation angles in the right 
        # order

        # The order of cardinal planes in an N-dimentional space is as 
        # follows:
        #   XY,  XZ, YZ,  XW, YW, ZW,  XV, YV, ZV, WV,  
        #   XU, YU, ZU, WU, VU, ...
        # As you can see, a two-dimentional space only has the first 
        # plane, a three-dimentional space has the first three, a four-
        # dimentional space has the first six planes, etc.
        # 
        # The algorithm for N-dimentional space rotations list is:
        # for dimention in range( N-1 ):
        #     (N-1)_dimentional_rotations_list += [ dimention, N ], 
        #           where N is the last N's dimention

    def __init__( self, angles: list[ float ] = list() ):
        self.angles = angles.copy()

        if len( angles ) < 1:
            self.planes = list()
        else: 
            # Getting the amount of dimentions of the angles list
            n = 2
            sum_n = 1
            while True:
                if sum_n >= len(angles):
                    break
                sum_n += n
                n += 1
                
            self.planes = self.get_planes( n )
        self.dimension = len( self.angles )


    def get_planes( self, dimensions: int ): 
            # generate a list of cardinal planes (see above)
            # depending on the number of dimensions given
        if dimensions <= 1:
            return list()
        else:
            dimensions -= 1
            prev_list = self.get_planes( dimensions )
            for i in range( dimensions ):
                prev_list.append( [ i, dimensions ] )
            return prev_list

    def append( self, value ):
        self.angles.append( value )
        self.dimesion = len( self.angles )


    def __add__( self, other: Self ):
        result = Rotation()
        min_len = min( len(self.angles), len(other.angles) )
        max_len = max( len(self.angles), len(other.angles) )

        if max_len == len(other.angles):
            max_list = other.angles
        else:
            max_list = self.angles

        
        for i in range( min_len ):
            result.append( self.angles[i] + other.angles[i] )

        for j in range( min_len, max_len ):
            result.append( max_list[j] )

        return result
        
    def __sub__( self, other: Self ):
        result = Rotation()
        min_len = min( len(self.angles), len(other.angles) )
        max_len = max( len(self.angles), len(other.angles) )

        if max_len == len(other.angles):
            max_list = other.angles
            subb = True
        else:
            max_list = self.angles
            subb = False

        
        for i in range( min_len ):
            result.append( self.angles[i] - other.angles[i] )

        for j in range( min_len, max_len ):
            if subb:
                result.append( -max_list[j] )
            else:
                result.append( max_list[j] )

        return result

    def __setitem__( self, index: int, value: float ):
        self.angles[ index ] = value

    def __getitem__( self, index: int ):
        return self.angles[ index ] 

    def __len__( self ):
        return len( self.angles )


class Plane:
    # TODO 
    def __init__( self, coordinates: list[ float ] ):
        # TODO
        pass

    # TODO
    pass

class Line:
    # TODO
    pass

class Point:
    def __init__( self, coordinates: list[ float ] = list() ):
        self.coordinates = coordinates.copy()
        self.dimension = len( coordinates )

    def __getitem__( self, index: int ):
        return self.coordinates[ index ]

    def __setitem__( self, index: int, value: float ):
        self.coordinates[ index ] = value
    
    def __len__( self ):
        return len( self.coordinates )

    def append( self, value: float ):
        self.coordinates.append( value )
        self.dimension = len( self.coordinates )

    def __str__( self ):
        return str( self.coordinates )


