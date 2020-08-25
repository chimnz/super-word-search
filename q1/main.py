import sys, yaml

INPUT_FILE = sys.argv[1]
with open(INPUT_FILE) as f:
	config = yaml.load(f, Loader=yaml.FullLoader)
GRID, WRAP_MODE, WORDS = config.values()


def main():
	pass


if __name__ == "__main__":
	main()