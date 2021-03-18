import sys
from Tokenizer import Tokenizer
from Parser import Parser


def main():
    # get file
    f = sys.argv[1]

    # Tokenize Core file
    tokenizer = Tokenizer(f)

    # Generate parse tree
    parse_tree = Parser()
    parse_tree = parse_tree.startParsing(tokenizer)

    # Print program
    parse_tree.printProgram()

    # Execute program
    print('\n**** Output ****')
    parse_tree.execProgram()


if __name__ == '__main__':
    main()
