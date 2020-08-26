import sys, yaml, os
from super_word_search import search

INPUT_FILE = sys.argv[1]
with open(INPUT_FILE) as f:
	config = yaml.load(f, Loader=yaml.FullLoader)
TITLE = config['title']
GRID = config['grid']
WRAP_MODE = config['wrap']
WORDS = config['words']

def main():
	wrap = True if WRAP_MODE == 'WRAP' else False
	terminal_width = int(os.popen('stty size', 'r').read().split()[1])  # https://stackoverflow.com/a/943921
	seperator = "-" * terminal_width

	print(TITLE + '\n' + seperator)
	for word in WORDS:
		results = search(GRID, word, wrap)
		if results:
			print(word, ": FOUND")
			for stack in results:
				start, end = stack[0], stack[-1]
				msg = "=> {} TO {}".format(start, end)
				print(msg)
		else:
			print(word, ": NOT FOUND")
		print(seperator)

if __name__ == "__main__":
	main()