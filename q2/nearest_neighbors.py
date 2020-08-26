from math import sqrt

def distance(pnt1, pnt2):
	x1, y1, z1 = pnt1
	x2, y2, z2 = pnt2
	return sqrt( (x2-x1)**2 + (y2-y1)**2 + (z2-z1)**2 )

def nearest_neighbors(r, pnt, points, N):
	nn = []
	for i in range(N):
		compare_point = points[i]
		if pnt == compare_point:
			continue
		else:
			d = distance(pnt, compare_point)
			if d <= r:
				nn.append(i)
	return nn