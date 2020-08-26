import sys, yaml
from super_word_search import search

INPUT_FILE = sys.argv[1]
with open(INPUT_FILE) as f:
	config = yaml.load(f, Loader=yaml.FullLoader)
GRID = config['grid']
WRAP_MODE = True if config['wrap'] == 'WRAP' else False
WORDS = config['words']

def main():
	for word in WORDS:
		results = search(GRID, word, WRAP_MODE)
		print(results)

if __name__ == "__main__":
	main()