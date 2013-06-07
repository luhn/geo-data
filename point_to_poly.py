
import math

def point_to_poly(x, y, poly):
    p1 = poly[-1]
    winner = float('inf')
    for p2 in poly:
        dist = p2s(p1, p2, (x, y))
        if dist < winner:
            winner = dist
        p1 = p2
    return winner
 
def p2s( a, b, p ):
    """Determine shortest distance from point to line segment.  Taken from
    http://onezstudio.blogspot.com/2007/11/code-distance-from-point-to-line.html"""
    dX = b[0] - a[0]
    dY = b[1] - a[1]
    segmentLen = math.sqrt( dX * dX + dY * dY )
    halfLen = segmentLen / 2
 
    pX = p[0] - a[0]
    pY = p[1] - a[1]
    if segmentLen < 1E-6:
        return math.sqrt( pX * pX + pY * pY )
 
    newX = abs( ( pX * dX + pY * dY ) / segmentLen - halfLen )
    newY = abs( - pX * dY + pY * dX ) / segmentLen
 
    if newX > halfLen:
        newX = newX - halfLen
        return math.sqrt( newX * newX + newY * newY )
    else:
        return newY
 
