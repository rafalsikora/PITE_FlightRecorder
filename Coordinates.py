# This module provides methods which translates
# coordinates of points on the sphere to coordinates
# of points on the flat surface


def xy(philambda):
    return ( philambda[1] / 360 + 0.5, philambda[0] / 180 + 0.5 )
