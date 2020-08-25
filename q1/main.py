import sys, yaml
from super_word_search import search

INPUT_FILE = sys.argv[1]
with open(INPUT_FILE) as f:
	config = yaml.load(f, Loader=yaml.FullLoader)
GRID, WRAP_MODE, WORDS = config.values()


def main():
	for word in WORDS:
		res = search(
			grid=GRID,
			word=word
		)
		print(word, res)


if __name__ == "__main__":
	main()