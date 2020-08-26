import sys
from nearest_neighbors import nearest_neighbors

RADIUS = float(sys.argv[1])
POINTS_FILE = sys.argv[2]

def get_points():
	with open(POINTS_FILE) as f:
		contents = f.read().strip()

	points = []  # [(x1, y1, z1), (x2, y2, z3), ...]
	for line in contents.split('\n'):
		pnt = tuple(float(n) for n in line.split())
		points.append(pnt)
	return points

def main():
	points = get_points()
	N = len(points)

	for idx, pnt in enumerate(points):
		nn = nearest_neighbors(RADIUS, pnt, points, N)
		print(idx, ':', nn)

if __name__ == '__main__':
	main()