import sys, yaml
from super_word_search import search

INPUT_FILE = sys.argv[1]
with open(INPUT_FILE) as f:
	config = yaml.load(f, Loader=yaml.FullLoader)
GRID, WRAP_MODE, WORDS = config.values()


def main():
	for word in WORDS:
		r = search(GRID, word, wrap=WRAP_MODE)
		print(word, r)

if __name__ == "__main__":
	main()