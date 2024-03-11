import time
import pygame
from math import sin, cos, pi


from camera import CameraP3D, CameraP4D, CameraPerspective, Camera2
from figure import Figure 
from plane import Plane
from screen import Screen
from geometry import Point, Rotation
from utilities import load_figure

from constants import *



display = Screen( SCREEN_RESOLUTION, BACKGROUND_COLOR, OBJECTS_COLOR )

camera = CameraP3D( INIT_CAM_3D_POS, INIT_CAM_3D_ROTAT, SCREEN_DIST )
camera4D = CameraPerspective( INIT_CAM_4D_POS, INIT_CAM_4D_ROTAT, SCREEN_DIST_4D )
cam = Camera2( SCREEN_RESOLUTION, (-1.5, 0, 0), (0,0), list() )


# -- TEMPORARY --- TODO ----
# FILENAME = "figures/tetrahedron.json"
FILENAME = "figures/cube_4D.json"

figure = load_figure( FILENAME )
figures = [ figure ]

cam_angle = 0
rotation2 = Rotation( [ 0.02, 0.01, 0.0 , -0.0, 0.01, 0.0])

# print( figure.points[0] )
# figure.rotate_by( Rotation( [ 0, 0, 0, pi/4, 0, 0 ] ) )
# print(  figure.points[0] )

# cam_rotation = Rotation( [ -0.01, 0, 0 ] )
# camera.rotate_by( Rotation( [ pi/2, 0 ] ) )
# camera.move_to( Point( [ 1000, 0, 0 ] ) )
# --- ------ ----- ---- ----

while  True:
    rotation = Rotation( [0]*6 ) 
    keys = pygame.key.get_pressed()
    for event in pygame.event.get():
        pass
    if keys[pygame.K_UP]:
        rotation = Rotation( [0.2, 0, 0, 0, 0, 0] )
    if keys[pygame.K_DOWN]:
        rotation = Rotation( [-0.2, 0, 0, 0, 0, 0] )
    if keys[pygame.K_LEFT]:
        rotation = Rotation( [0, 0.2, 0, 0, 0, 0] )
    if keys[pygame.K_RIGHT]:
        rotation = Rotation( [0, -0.2, 0, 0, 0, 0] )
    if keys[pygame.K_w]:
        rotation = Rotation( [0, 0, 0.2, 0, 0, 0] )
    if keys[pygame.K_s]:
        rotation = Rotation( [0, 0, -0.2, 0, 0, 0] )
    if keys[pygame.K_q]:
        rotation = Rotation( [0, 0, 0, 0.2, 0, 0] )
    if keys[pygame.K_a]:
        rotation = Rotation( [0, 0, 0, -0.2, 0, 0] )
    if keys[pygame.K_e]:
        rotation = Rotation( [0, 0, 0, 0, 0.2, 0] )
    if keys[pygame.K_d]:
        rotation = Rotation( [0, 0, 0, 0, -0.2, 0] )
    if keys[pygame.K_r]:
        rotation = Rotation( [0, 0, 0, 0, 0, 0.2] )
    if keys[pygame.K_f]:
        rotation = Rotation( [0, 0, 0, 0, 0, -0.2] )


    display.fill()
    # cam_angle += 0.01

    # rotation = Rotation( [0, 0, 0, 0, -0.02, 0] )
    # FOR EDGES
    '''
    coords = list()
    for figure in figures:
        figure.rotate_by( rotation )
        for edge in figure.get_edges():
            start_point, end_point = camera4D.project_edge( edge, 3 )
            print(start_point, end_point)

            start_point, end_point = camera.project_edge( [start_point, end_point] )
            coords.append( [start_point, end_point] )
            display.draw_edge( start_point, end_point )
    # FOR TRIANGLES
    '''
    i = 0
    coords = list()
    cam.set_map(list())
    for figure in figures:
        figure.rotate_by( rotation )
        for triangle in figure.get_triangles():
            triangle = camera4D.project_triangle( triangle, 3 )
            # print([str(point)+' ' for point in triangle])
            # print(start_point, end_point)
            plane = Plane(triangle, (255- 5*i, 127 + 5*i, 8*i))
            cam.add_plane(plane)
            i += 1
    # print('hi')
    bef = time.time()
    cam.render()
    print(time.time() - bef)

            

    

    # camera.rotate_by( cam_rotation )
    # camera.move_to( Point( [1500*sin(cam_angle), 1500*cos(cam_angle), 0] ) )
    
    display.update()
    # time.sleep( 1 / 6 )


