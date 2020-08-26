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
	half_terminal_width = int(os.popen('stty size', 'r').read().split()[1]) // 2  # https://stackoverflow.com/a/943921
	seperator = '\n' + '*' * half_terminal_width

	print(TITLE, seperator)
	for word in WORDS:
		results = search(GRID, word, wrap)
		if results:
			print(word, ": FOUND")
			for stack in results:
				start, end = stack[0], stack[-1]
				msg = "=> {} TO {}".format(start, end)
				print(msg, seperator)
		else:
			print(word, ": NOT FOUND")

if __name__ == "__main__":
	main()