# Tokenizer class for Core Interpreter
# Author: Wilmer Pellicier

import sys
import re


class Tokenizer:
    # constructor for tokenizer
    def __init__(self, filename):
        # Legal tokens from 1 to 33
        self.reserved = {'program': 1, 'begin': 2, 'end': 3,
                         'int': 4, 'if': 5, 'then': 6, 'else': 7,
                         'while': 8, 'loop': 9, 'read': 10, 'write': 11}

        self.special = {';': 12, ',': 13, '=': 14, '!': 15, '[': 16, ']': 17,
                        '&&': 18, '||': 19, '(': 20, ')': 21, '+': 22, '-': 23,
                        '*': 24, '!=': 25, '==': 26, '<': 27, '>': 28,
                        '<=': 29, '>=': 30}
        self.integer = 31
        self. identifier = 32
        self.eof = 33

        self.whitespace = ' \t\n\r'
        self.current_tokens = []

        # Opening file for reading
        self.f = open(filename)
        self.consumeLine()

        self.curr = 0

    # Takes a line from file and tokenizes it
    def consumeLine(self):
        line = self.f.readline()  # Get next line from file
        while line == '\n' or line == '\t' or line == '\r' or line == ' ':
            line = self.f.readline()

        pos = 0
        while pos < len(line):
            token = self.nextWordOrSeparator(line, pos)

            if line[pos] not in self.whitespace:
                # Append appropriate token number for each token
                if token in self.special:
                    self.current_tokens.append([self.special[token]])
                elif token in self.reserved:
                    self.current_tokens.append([self.reserved[token]])
                elif token.isnumeric() and int(token) >= 0:
                    self.current_tokens.append([31, int(token)])
                elif token.strip('-').isnumeric() and int(token) < 0:
                    self.current_tokens.append([-1])
                elif token:
                    self.current_tokens.append([32, token])
            pos += len(token)
        # Reached EOF
        if line == '':
            self.current_tokens.append([33])

    # Locates individual tokens and/or whitespace
    def nextWordOrSeparator(self, line, pos):
        holder = line[pos]
        c = line[pos]

        if c not in self.whitespace:
            i = pos + 1
            while i < len(line) and line[i] not in self.whitespace:
                # if two special characters appear in a row
                if holder in self.special and line[i] in self.special:
                    temp = holder + line[i]
                    # check if both together make a valid token
                    if temp in self.special:
                        holder = temp;
                        return holder
                    # if they don't make a valid token, return the first token
                    else:
                        return holder

                # if either the characters we've seen or the next are special chars
                # return what we've seen so far to separate them
                if holder in self.special or line[i] in self.special:
                    return holder
                # If not, keep consuming characters
                else:
                    holder = holder + line[i]
                    i += 1
        # If it's whitespace, consume them until we reach the next possible token
        else:
            i = pos + 1
            while i < len(line) and line[i] in self.whitespace:
                holder = holder + line[i]
                i += 1

        # If we get here we are potentially dealing with reserved, ids
        # integers or whitespace

        # Check if whitespace
        if holder in self.whitespace:
            return holder

        # Check if reserved
        if holder in self.reserved:
            return holder

        # Check if special
        if holder in self.special:
            return holder

        # Check if integer
        if holder.isnumeric():
            return holder

        # Check if identifier and fits ID format
        # Regex for identifier: ^(?=.{1,7}$)[A-Z]+[\d]*$
        is_match = re.match(r"(?=.{1,7}$)[A-Z]+[\d]*$", holder)
        if is_match:
            return holder

        # Anything else is invalid
        return '-'+'1'*(len(holder) - 1)

    # Returns info about current token
    # Repeated calls return token
    def getToken(self):
        return self.current_tokens[self.curr]

    # Skips current token, next token will be current
    def skipToken(self):
        if self.curr < len(self.current_tokens) - 1:
            self.curr += 1
        else:
            self.current_tokens = []
            self.consumeLine()
            self.curr = 0
        if self.getToken()[0] == 33:
            self.f.close()

    # Returns value of integer token
    # Returns error if current is not integer
    def intVal(self):
        if self.getToken()[0] == 31:
            return self.getToken()[1]
        else:
            return "Error: current token is not an integer."

    # Returns the name (string) of current identifier token
    # Returns error if current is not identifier
    def idName(self):
        if self.getToken()[0] == 32:
            return self.getToken()[1]
        else:
            return "Error: current token is not an identifier."

'''
def main():
    # Main for isolated tokenizer testing
    f = sys.argv[1]

    # call constructor
    tokenizer = Tokenizer(f)
    # repeatedly call get token until it's done
    # output returned token numbers one per line
    t = tokenizer.getToken()

    while True:
        t = tokenizer.getToken()
        print(t[0])
        if t[0] == 33:
            break
        elif t[0] < 0:
            print("Error: Invalid token")
            break
        
        elif t[0] == 31:
            print(tokenizer.intVal())
        elif t[0] == 32:
            print(tokenizer.idName())
        
        tokenizer.skipToken()


if __name__ == '__main__':
    main()
'''


