import pygame


class Screen:
    def __init__( self, resolution: list[ int, int ], # horizontal, vertical
                  background_color: list[ int, int, int ], # RGB, 0-255
                  object_color: list[ int, int, int ] ): # RGB, 0-255 
        pygame.init()
        self.resolution = resolution
        self.background_color = background_color
        self.object_color = object_color

        self.display = pygame.display.set_mode( resolution )

        # --- TEMPORARY ---- TODO ---
        self.circle_radius = 1
        self.line_width = 3
        # --- --------- ---- ---- ---
        

    def draw_triangle( self, points: list[ list[ float, float ] ] ):
        pygame.draw.polygon( self.display,
                             self.object_color,
                             points,
                             width=self.line_width
                             )
        for point in points:
            draw_point( point )


    def draw_edge( self, start_point: list[ float, float ],
                    end_point: list[ float, float ] ):
        self.draw_point( start_point )
        self.draw_point( end_point )
        
        start_point = [ start_point[0] + self.resolution[0]/2,
                        start_point[1] + self.resolution[1]/2 ]
        end_point = [ end_point[0] + self.resolution[0]/2,
                      end_point[1] + self.resolution[1]/2 ]
        pygame.draw.line( self.display, 
                          self.object_color,
                          start_point,
                          end_point,
                          width=self.line_width
                          ) 

    def draw_point( self, coords: list[ float, float ] ):
        pygame.draw.circle( self.display, 
                            self.object_color,
                            [ coords[0] + self.resolution[0]/2,
                              coords[1] + self.resolution[1]/2 ],
                            self.circle_radius
                            ) 

    def fill( self ):
        self.display.fill( self.background_color )

    def update( self ):
        pygame.display.update()
