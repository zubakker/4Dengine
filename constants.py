import math
from geometry import Point, Rotation

SCREEN_RESOLUTION = [ 100, 100 ]
BACKGROUND_COLOR = [ 0, 0, 0 ]
OBJECTS_COLOR = [ 0, 100, 28 ]

# --- camera constants ---
INIT_CAM_3D_POS = Point( [ 0, -1.5, 0 ] )
INIT_CAM_3D_ROTAT = Rotation( [ -math.pi/2, 0, 0 ] )
INIT_CAM_4D_POS = Point( [ 0, 0, 0, -2.0 ] )
INIT_CAM_4D_ROTAT = Rotation( [ 0, 0, 0, math.pi/2, 0, 0 ] )
FOV = math.pi/2

SCREEN_DIST = SCREEN_RESOLUTION[0] / 2*math.tan(FOV/2) 
SCREEN_DIST_4D = 0.5 

SUPPORTED_DIMENTIONS = 4
