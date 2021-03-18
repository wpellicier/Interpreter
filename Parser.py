# Parser class for Core Interpreter
# Allows for parsing, printing, and executing
# Author: Wilmer Pellicier
import sys


class Parser:
    # Constructor for Parser, starts generating parse tree
    def __init__(self):
        pass

    def startParsing(self, tokenizer):
        # Starts parsing from program keyword
        pt = Prog()
        pt.parseProg(tokenizer)
        return pt


# Class for Program node. Allows for parsing, printing, and executing
class Prog:
    def __init__(self):
        self.decl_seq = None
        self.stmt_seq = None

    # Parses program node
    def parseProg(self, tokenizer):
        t = tokenizer.getToken()
        if t[0] != 1:  # Should be 'program'
            print('Error: Keyword did not match "program"')
            sys.exit()
        tokenizer.skipToken()

        self.decl_seq = DeclSeq()
        self.decl_seq.parseDeclSeq(tokenizer)

        t = tokenizer.getToken()
        if t[0] != 2:  # Should be 'begin'
            print('Error: Keyword did not match "begin"')
            sys.exit()
        tokenizer.skipToken()

        self.stmt_seq = StmtSeq()
        self.stmt_seq.parseStmtSeq(tokenizer)

        t = tokenizer.getToken()
        if t[0] != 3:  # Should be 'end'
            print('Error: Keyword did not match "end"')
            sys.exit()
        tokenizer.skipToken()

    # Pretty prints program node
    def printProgram(self):
        print('program')
        self.decl_seq.printDeclSeq()
        print('begin')
        self.stmt_seq.printStmtSeq(1)
        print('end')

    # Executes program node
    def execProgram(self):
        self.decl_seq.execDeclSeq()
        self.stmt_seq.execStmtSeq()


# Class for Declaration Sequence. Allows for parsing, printing, and executing
class DeclSeq:
    def __init__(self):
        self.altNo = 0  # <decl> or <decl><decl seq> ?
        self.decl = None
        self.decl_seq = None

    # Parses declaration sequence node
    def parseDeclSeq(self, tokenizer):
        self.decl = Decl()
        self.decl.parseDecl(tokenizer)

        t = tokenizer.getToken()
        if t[0] != 2:  # Haven't hit 'begin'. This is case <decl><decl seq>
            self.altNo = 1
            self.decl_seq = DeclSeq()
            self.decl_seq.parseDeclSeq(tokenizer)

    # Pretty prints declaration sequence node
    def printDeclSeq(self):
        indentation(1)
        self.decl.printDecl()
        if self.altNo == 1:
            self.decl_seq.printDeclSeq()

    # Executes declaration sequence
    def execDeclSeq(self):
        self.decl.execDecl()
        if self.altNo == 1:
            self.decl_seq.execDeclSeq()


# Class for Statement Sequence. Allows for parsing, printing, and executing
class StmtSeq:
    def __init__(self):
        self.altNo = 0  # <stmt> or <decl><decl seq> ?
        self.stmt = None
        self.stmt_seq = None

    # Parses statement sequence node
    def parseStmtSeq(self, tokenizer):
        self.stmt = Stmt()
        self.stmt.parseStmt(tokenizer)

        t = tokenizer.getToken()
        if t[0] != 3 and t[0] != 7:  # Haven't hit 'end'. This is case <stmt><stmt seq>
            self.altNo = 1
            self.stmt_seq = StmtSeq()
            self.stmt_seq.parseStmtSeq(tokenizer)

    # Pretty prints statement sequence
    # Parameter i indicates indentation
    def printStmtSeq(self, i):
        indentation(i)
        self.stmt.printStmt(i)
        if self.altNo == 1:
            self.stmt_seq.printStmtSeq(i)

    # Executes statement sequence
    def execStmtSeq(self):
        self.stmt.execStmt()
        if self.altNo == 1:
            self.stmt_seq.execStmtSeq()


# Class for Declaration. Allows for parsing, printing, and executing
class Decl:
    def __init__(self):
        self.idList = None

    # Parses declaration node
    def parseDecl(self, tokenizer):
        t = tokenizer.getToken()
        if t[0] != 4:  # Should be 'int'
            print('Error: Keyword did not match "int"')
            sys.exit()
        tokenizer.skipToken()

        self.idList = ID_List()
        self.idList.parseIdList(tokenizer)

        t = tokenizer.getToken()
        if t[0] != 12:  # Should be '';''
            print('Error: Token did not match ";"')
            sys.exit()
        tokenizer.skipToken()

    # Pretty prints declaration
    def printDecl(self):
        print('int', end=' ')
        self.idList.printIdList()
        print(';')

    # Executes declaration
    def execDecl(self):
        self.idList.execIdList()


# Class for ID List. Allows for parsing, printing, and executing
class ID_List:
    def __init__(self):
        self.altNo = 0  # <id> or <id>, <id list>
        self.id = None
        self.idList = None

    # Parses ID list node
    def parseIdList(self, tokenizer):
        self.id = ID()
        self.id = self.id.parseID(tokenizer)

        t = tokenizer.getToken()
        if t[0] == 13:  # Found ',' indicating more IDs in DS. Case <id>, <id list>
            self.altNo = 1
            tokenizer.skipToken()
            self.idList = ID_List()
            self.idList.parseIdList(tokenizer)

    # Pretty prints ID List
    def printIdList(self):
        print(self.id.getIDName(), end='')
        if self.altNo == 1:
            print(',', end=' ')
            self.idList.printIdList()

    # Executes ID List
    def execIdList(self):
        # Check if ID has already been declared, if so, throw error
        if self.id.isDeclared():
            print("Error: " + self.id.getIDName() + " already declared")
            sys.exit()
        # Set id to declared
        self.id.setDeclared()
        if self.altNo == 1:
            self.idList.execIdList()

    # Handles reading ID value from standard input stream
    def execReadIdList(self):
        if not self.id.isDeclared():
            print("Error: " + self.id.getIDName() + " not declared")
            sys.exit()
        # Get ID value from standard input stream
        print('\nEnter value for ' + self.id.getIDName() + ':') # Comment this line if not needed
        self.id.setIdVal(input())
        self.id.setInitialized()

        # Check if there are more ID waiting for read values
        if self.altNo == 1:
            self.idList.execReadIdList()

    # Handles writing ID value to standard output stream
    def execWriteIdList(self):
        if not self.id.isDeclared():
            print("Error: " + self.id.getIDName() + " not declared")
            sys.exit()
        if not self.id.isInitialized():
            print("Error: " + self.id.getIDName() + " not initialized")
            sys.exit()

        print(self.id.getIDName() + ' = ' + str(self.id.getIdVal()))

        if self.altNo == 1:
            self.idList.execWriteIdList()


# Class for Statement. Allows for parsing, printing, and executing
class Stmt:
    def __init__(self):
        self.altNo = 0  # <assign> or <if> or <loop> or <in> or <out>
        self.assign = None
        self.if_stmt = None
        self.loop = None
        self.in_stmt = None
        self.out_stmt = None

    # Parses statement node
    def parseStmt(self, tokenizer):
        t = tokenizer.getToken()

        if t[0] == 32:   # Case <assign>
            self.altNo = 0
            self.assign = Assign()
            self.assign.parseAssign(tokenizer)
        elif t[0] == 5:   # Case <if>
            self.altNo = 1
            self.if_stmt = If()
            self.if_stmt.parseIf(tokenizer)
        elif t[0] == 8:   # Case <loop>
            self.altNo = 2
            self.loop = Loop()
            self.loop.parseLoop(tokenizer)
        elif t[0] == 10:   # Case <in>
            self.altNo = 3
            self.in_stmt = InStmt()
            self.in_stmt.parseInStmt(tokenizer)
        elif t[0] == 11:   # Case <out>
            self.altNo = 4
            self.out_stmt = OutStmt()
            self.out_stmt.parseOutStmt(tokenizer)
        else:
            print('Error: Token did not match statement')
            sys.exit()

        t = tokenizer.getToken()
        if t[0] != 12:  # Should be ';'
            print('Error: Token did not match ";"')
            sys.exit()
        tokenizer.skipToken()

    # Pretty print statement
    # Parameter indicates appropriate indentation
    def printStmt(self, i):
        if self.altNo == 0:   # Case <assign>
            self.assign.printAssign()
        elif self.altNo == 1:   # Case <if>
            self.if_stmt.printIf(i)
        elif self.altNo == 2:   # Case <loop>
            self.loop.printLoop(i)
        elif self.altNo == 3:   # Case <in>
            self.in_stmt.printInStmt()
        elif self.altNo == 4:  # Case <out>
            self.out_stmt.printOutStmt()

    # Execute statement
    def execStmt(self):
        if self.altNo == 0:  # Case <assign>
            self.assign.execAssign()
        elif self.altNo == 1:  # Case <if>
            self.if_stmt.execIf()
        elif self.altNo == 2:  # Case <loop>
            self.loop.execLoop()
        elif self.altNo == 3:  # Case <in>
            self.in_stmt.execInStmt()
        elif self.altNo == 4:  # <out>
            self.out_stmt.execOutStmt()


# Class for Assign. Allows for parsing, printing, and executing
class Assign:
    def __init__(self):
        self.id = None
        self.exp = None

    # Parses assign node
    def parseAssign(self, tokenizer):
        t = tokenizer.getToken()
        if t[0] != 32:  # Should be identifier
            print("Error: Token is not an identifier")
            sys.exit()
        self.id = ID()
        self.id = self.id.parseID(tokenizer)

        t = tokenizer.getToken()
        if t[0] != 14:  # Should be '='
            print('Error: Token did not match "="')
            sys.exit()

        tokenizer.skipToken()

        self.exp = Exp()
        self.exp.parseExp(tokenizer)

    # Pretty prints assign
    def printAssign(self):
        print(self.id.name + ' =', end=' ')
        self.exp.printExp()
        print(';')

    # Executes assignment
    def execAssign(self):
        if self.id.isDeclared():
            self.id.setIdVal(self.exp.execExp())
            self.id.setInitialized()


# Class for If. Allows for parsing, printing, and executing
class If:
    def __init__(self):
        self.altNo = 0  # if-then or if-then-else
        self.c = None
        self.stmtSeq1 = None
        self.stmtSeq2 = None

    # Parses if node
    def parseIf(self, tokenizer):
        t = tokenizer.getToken()
        if t[0] != 5:  # should be 'if'
            print('Error: Keyword does not match "if"')
            sys.exit()
        tokenizer.skipToken()

        self.c = Cond()
        self.c.parseCond(tokenizer)

        t = tokenizer.getToken()
        if t[0] != 6:  # should be "then"
            print('Error: Keyword does not match "then"')
            sys.exit()
        tokenizer.skipToken()

        self.stmtSeq1 = StmtSeq()
        self.stmtSeq1.parseStmtSeq(tokenizer)

        t = tokenizer.getToken()
        if t[0] == 7:  # Case if <cond> then <stmt seq> else <stmt seq> end;
            self.altNo = 1
            tokenizer.skipToken()
            self.stmtSeq2 = StmtSeq()
            self.stmtSeq2.parseStmtSeq(tokenizer)

        t = tokenizer.getToken()
        if t[0] != 3:  # Should be 'end'
            print('Error: Keyword did not match "end"')
            sys.exit()
        tokenizer.skipToken()

    # Pretty prints if statement
    def printIf(self, i):
        print('if', end=' ')
        self.c.printCond()
        print('then')
        self.stmtSeq1.printStmtSeq(i + 1)
        if self.altNo == 1:
            indentation(i)
            print('else')
            self.stmtSeq2.printStmtSeq(i + 1)
        indentation(i)
        print('end;')

    # Executes if statement
    def execIf(self):
        if self.c.execCond():
            self.stmtSeq1.execStmtSeq()
        elif self.altNo == 1:
            self.stmtSeq2.execStmtSeq()


# Class for Loop. Allows for parsing, printing, and executing
class Loop:
    def __init__(self):
        self.c = None
        self.stmt_seq = None

    # Parses loop node
    def parseLoop(self, tokenizer):
        t = tokenizer.getToken()
        if t[0] != 8:  # should be 'while'
            print('Error: Keyword does not match "while"')
            sys.exit()
        tokenizer.skipToken()

        self.c = Cond()
        self.c.parseCond(tokenizer)

        t = tokenizer.getToken()
        if t[0] != 9:  # should be 'loop'
            print('Error: Keyword does not match "loop"')
            sys.exit()
        tokenizer.skipToken()

        self.stmt_seq = StmtSeq()
        self.stmt_seq.parseStmtSeq(tokenizer)

        t = tokenizer.getToken()
        if t[0] != 3:  # Should be 'end'
            print('Error: Keyword did not match "end"')
            sys.exit()
        tokenizer.skipToken()

    # Pretty prints loop
    # Parameter i indicates appropriate indentation
    def printLoop(self, i):
        print('while', end=' ')
        self.c.printCond()
        print('loop')
        self.stmt_seq.printStmtSeq(i + 1)
        print('end;')

    # Executes loop
    def execLoop(self):
        while self.c.execCond():
            self.stmt_seq.execStmtSeq()


# Class for In. Allows for parsing, printing, and executing
class InStmt:
    def __init__(self):
        self.idList = None

    # Parses in node
    def parseInStmt(self, tokenizer):
        t = tokenizer.getToken()
        if t[0] != 10:  # should be 'read'
            print('Error: Keyword does not match "read"')
            sys.exit()
        tokenizer.skipToken()

        self.idList = ID_List()
        self.idList.parseIdList(tokenizer)

    # Pretty prints read statement
    def printInStmt(self):
        print('read', end=' ')
        self.idList.printIdList()
        print(';')

    # Executes read statement
    def execInStmt(self):
        self.idList.execReadIdList()


# Class for Out. Allows for parsing, printing, and executing
class OutStmt:
    def __init__(self):
        self.idList = None

    # Parses out node
    def parseOutStmt(self, tokenizer):
        t = tokenizer.getToken()
        if t[0] != 11:  # should be 'write'
            print('Error: Keyword does not match "write"')
            sys.exit()
        tokenizer.skipToken()

        self.idList = ID_List()
        self.idList.parseIdList(tokenizer)

    # Pretty prints write statement
    def printOutStmt(self):
        print('write', end=' ')
        self.idList.printIdList()
        print(';')

    # Executes write statement
    def execOutStmt(self):
        self.idList.execWriteIdList()


# Class for Cond. Allows for parsing, printing, and executing
class Cond:
    def __init__(self):
        self.altNo = 0  # <comp> or !<comd> or [<cond>&&<cond>] || [<cond>&&<cond>]
        self.comp = None
        self.not_cond = None
        self.left_cond = None
        self.right_cond = None
        self.operator = None

    # Parses condition node
    def parseCond(self, tokenizer):
        t = tokenizer.getToken()
        if t[0] == 15:  # !<cond>
            self.altNo = 1
            tokenizer.skipToken()
            self.not_cond = Cond()
            self.not_cond.parseCond(tokenizer)
        elif t[0] == 16:  # '[' indicates start of && or ||
            tokenizer.skipToken()
            self.left_cond = Cond()
            self.left_cond.parseCond(tokenizer)

            t = tokenizer.getToken()
            if t[0] == 18:  # [<cond> && <cond>]
                self.altNo = 2
                self.operator = '&&'
                tokenizer.skipToken()
            elif t[0] == 19:  # [<cond> || <cond>]
                self.altNo = 3
                self.operator = '||'
                tokenizer.skipToken()
            else:
                print('Error: Token does not match "&&" or "||"')
                sys.exit()
            # parsing right hand condition
            self.right_cond = Cond()
            self.right_cond.parseCond(tokenizer)
            tokenizer.skipToken()
            t = tokenizer.getToken()
        else:  # <comp>
            self.altNo = 0
            self.comp = Comp()
            self.comp.parseComp(tokenizer)

    # Pretty prints condition
    def printCond(self):
        if self.altNo == 0:
            self.comp.printComp()
        elif self.altNo == 1:
            print('!', end='')
            self.not_cond.printCond()
        elif self.altNo == 2:
            print('[', end=' ')
            self.left_cond.printCond()
            print('&&', end=' ')
            self.right_cond.printCond()
            print(']', end=' ')
        elif self.altNo == 3:
            print('[', end='')
            self.left_cond.printCond()
            print('||', end=' ')
            self.right_cond.printCond()
            print(']', end=' ')

    # Executes condition
    def execCond(self):
        if self.altNo == 0:
            return self.comp.execComp()
        elif self.altNo == 1:
            return not self.not_cond.execCond()
        elif self.altNo == 2:
            left = self.left_cond.execCond()
            right = self.right_cond.execCond()
            return left and right
        elif self.altNo == 3:
            left = self.left_cond.execCond()
            right = self.right_cond.execCond()
            return left or right


# Class for Comp. Allows for parsing, printing, and executing
class Comp:
    def __init__(self):
        self.op1 = None
        self.comp_op = None
        self.op2 = None

    # Parses comparison node
    def parseComp(self, tokenizer):
        t = tokenizer.getToken()
        if t[0] != 20:  # opening parenthesis
            print("Error: Token does not match '('")
            sys.exit()
        tokenizer.skipToken()

        self.op1 = Op()
        self.op1.parseOp(tokenizer)

        self.comp_op = CompOp()
        self.comp_op.parseCompOp(tokenizer)

        self.op2 = Op()
        self.op2.parseOp(tokenizer)

        t = tokenizer.getToken()
        if t[0] != 21:  # closing parenthesis
            print("Error: Token does not match ')'")
            sys.exit()
        tokenizer.skipToken()

    # Pretty prints comparison
    def printComp(self):
        print('(', end=' ')
        self.op1.printOp()
        self.comp_op.printCompOp()
        self.op2.printOp()
        print(')', end=' ')

    # Executes comparison
    def execComp(self):
        left = self.op1.execOp()
        right = self.op2.execOp()
        comp = self.comp_op.getCompOp()

        if comp == '!=':
            return left != right
        elif comp == '==':
            return left == right
        elif comp == '<':
            return left < right
        elif comp == '>':
            ans = left > right
            return ans
        elif comp == '<=':
            return left <= right
        elif comp == '>=':
            return left >= right


# Class for Exp. Allows for parsing, printing, and executing
class Exp:
    def __init__(self):
        self.altNo = 0   # <fac> or <fac> + <exp> or <fac> - <exp>
        self.fac = None
        self.operator = None
        self.exp = None

    # Parses expression node
    def parseExp(self, tokenizer):
        self.fac = Fac()
        self.fac.parseFac(tokenizer)

        t = tokenizer.getToken()
        if t[0] == 22:   # case: <fac> + <exp>
            self.altNo = 1
            self.operator = '+'
            tokenizer.skipToken()
            self.exp = Exp()
            self.exp.parseExp(tokenizer)

        elif t[0] == 23:  # case: <fac> - <exp>
            self.altNo = 2
            self.operator = '-'
            tokenizer.skipToken()
            self.exp = Exp()
            self.exp.parseExp(tokenizer)

    # Pretty prints expression
    def printExp(self):
        self.fac.printFac()
        if self.altNo != 0:
            print(self.operator, end=' ')
            self.exp.printExp()

    # Executes expression
    def execExp(self):
        res = self.fac.execFac()
        # case: <fac> + <exp>
        if self.altNo == 1:
            res += self.exp.execExp()
        # case: <fac> - <exp>
        elif self.altNo == 2:
            res -= self.exp.execExp()
        return res


# Class for Fac. Allows for parsing, printing, and executing
class Fac:
    def __init__(self):
        self.altNo = 0   # <op> or <op> * < fac>
        self.op = None
        self.operator = None
        self.fac = None

    # Parses factor node
    def parseFac(self, tokenizer):
        self.op = Op()
        self.op.parseOp(tokenizer)

        t = tokenizer.getToken()
        if t[0] == 24:  # case: <op> * <fac>
            self.altNo = 1
            self.operator = '*'
            tokenizer.skipToken()
            self.fac = Fac()
            self.fac.parseFac(tokenizer)

    # Pretty prints factor
    def printFac(self):
        self.op.printOp()
        if self.altNo == 1:
            print(self.operator, end=' ')
            self.fac.printFac()

    # Executes factor
    def execFac(self):
        res = self.op.execOp()
        if self.altNo == 1:
            res *= self.fac.execFac()
        return res


# Class for Op. Allows for parsing, printing, and executing
class Op:
    def __init__(self):
        self.altNo = 0   # <int> or <id> or (<exp>)
        self.int_obj = None
        self.id = None
        self.exp = None

    # Parses operand node
    def parseOp(self, tokenizer):
        t = tokenizer.getToken()

        if t[0] == 31:
            self.altNo = 0
            self.int_obj = IntObj()
            self.int_obj = self.int_obj.parseIntObj(tokenizer)
        elif t[0] == 32:
            self.altNo = 1
            self.id = ID()
            self.id = self.id.parseID(tokenizer)
        elif t[0] == 20:
            self.altNo = 2
            tokenizer.skipToken()
            self.exp = Exp()
            self.exp.parseExp(tokenizer)
            t = tokenizer.getToken()
            if t[0] != 21:   # should be ')'
                print("Error: Token did not match ')'")
                sys.exit()
            tokenizer.skipToken()   # Added this
        else:
            return 'Error: Token did not match op'

    # Pretty print operand
    def printOp(self):
        if self.altNo == 0:
            print(self.int_obj, end='')
        elif self.altNo == 1:
            print(self.id.getIDName(), end=' ')
        elif self.altNo == 2:
            print('(', end=' ')
            self.exp.printExp()
            print(')', end=' ')

    # Execute operand
    def execOp(self):
        if self.altNo == 0:
            return self.int_obj
        elif self.altNo == 1:
            return self.id.getIdVal()
        elif self.altNo == 2:
            return self.exp.execExp()


# Class for CompOp. Allows for parsing, printing, and executing
class CompOp:
    def __init__(self):
        self.comp_operator = None

    # Parses comparison operator
    def parseCompOp(self, tokenizer):
        t = tokenizer.getToken()

        if t[0] == 25:
            self.comp_operator = '!='
        elif t[0] == 26:
            self.comp_operator = '=='
        elif t[0] == 27:
            self.comp_operator = '<'
        elif t[0] == 28:
            self.comp_operator = '>'
        elif t[0] == 29:
            self.comp_operator = '<='
        elif t[0] == 30:
            self.comp_operator = '>='

        tokenizer.skipToken()

    # Pretty prints comparison operator
    def printCompOp(self):
        print(self.comp_operator, end=' ')

    # Returns comparison operator represented by this node
    def getCompOp(self):
        return self.comp_operator


# Class for ID. Allows for parsing, printing, and executing
class ID:
    # Variables available to all instances of ID
    id_list = []   # contains all existing IDs

    def __init__(self):
        self.name = None
        self.val = None
        self.declared = False
        self.initialized = False

    # Parses identifiers, only adds them to id_list if they have not been initialized
    @staticmethod
    def parseID(tokenizer):
        t = tokenizer.getToken()

        if t[0] != 32:    # should be an identifier
            print("Error: Token is not an identifier")
            sys.exit()

        # Check if ID we're parsing is in the ID List
        for ident in ID.id_list:
            # Return it if it is
            if ident.name == t[1]:
                tokenizer.skipToken()
                return ident
        # If not, add it to the list
        new_id = ID()
        new_id.name = t[1]

        ID.id_list.append(new_id)
        tokenizer.skipToken()

        return new_id

    # Returns value held by this identifier
    def getIdVal(self):
        if not self.initialized:
            print('Error: Identifier not initialized')
            sys.exit()
        return int(self.val)

    # Sets an ID value for this identifier
    def setIdVal(self, value):
        self.val = value

    # Gets identifier name for this identifier
    def getIDName(self):
        return self.name

    # Checks if identifier has been declared
    def isDeclared(self):
        return self.declared

    # Marks identifier as declared
    def setDeclared(self):
        self.declared = True

    # Checks if identifier has been initialized
    def isInitialized(self):
        return self.initialized

    # Marks identifier as initialized
    def setInitialized(self):
        self.initialized = True


# Class for Int. Allows for parsing, printing, and executing
class IntObj:
    def __init__(self):
        self.num = None

    # Parses int
    def parseIntObj(self, tokenizer):
        t = tokenizer.getToken()
        if t[0] != 31:   # Should be a valid integer
            print('Error: Token is not a valid int')
            sys.exit()

        self.num = t[1]
        tokenizer.skipToken()
        return self.num

    # Pretty prints int
    def printIntObj(self):
        return self.num

    # Returns value of int as int
    def getVal(self):
        return int(self.num)


# Adds appropriate number of tabs according to n
def indentation(n):
    print('\t' * n, end='')



