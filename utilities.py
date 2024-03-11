import json

from constants import SUPPORTED_DIMENTIONS
from figure import Figure 
from geometry import Point


def load_figure( filename : str ): # reads one figure from a json file
    data = json.loads( open( filename, "r").read() )
    if data[ "dimentions" ] < SUPPORTED_DIMENTIONS:
        # TODO 
        # if we can't support a superdimentional figure, it needs to be
        # projected into a lower dimention figure we can support
        pass

    # TODO
    points = list()
    for point in data[ "points" ]:
        points.append( Point( point ) )
    loaded_fig = Figure( points, 
                         data[ "edges" ], 
                         data[ "triangles" ],
                         data[ "center_point" ], 
                         data[ "dimentions" ] )
    return loaded_fig


