'''
A tiny "Lisp" to Tinderbox action code compiler.
Author: NiwTR
License: Public Domain
'''
from pyparsing import OneOrMore, nestedExpr ; import sys
unary_ops = {
        'not': '!'
        }
binary_ops = {
        "set!": '=',
        "eq" : "==",
        "gt" : '>',
        "lt" : '<',
        "or" : "|",
        "lor" : '|=',
        "and" : '&',
        "land" : '&=', 
        "neq" : '!=',
        }

arbitrary_ops = {
        '*' : '*',
        '+' : '+',
        '-' : '-',
        '/' : '/'
        }

def gen_dollar(thing): return "$" + thing 
def gen_funcall(fn, params): return fn + '(' + ','.join(params) + ')'
def gen_codeblock(codelist): return ';'.join(codelist)
def gen_ops(opname, dicta): return dicta[opname]
def gen_unary(op, hs): return gen_ops(op, unary_ops) + hs
def gen_binary(op, lhs, rhs): return lhs + gen_ops(op, binary_ops) + rhs
def gen_arbitrary(op, arglist): return gen_ops(op, arbitrary_ops).join(arglist)
def gen_var(name, val): return 'var ' + name + '('+val+')'
def gen_let(letlist): return gen_codeblock([gen_var(n, v) for (n,v) in letlist])
def gen_dollar(thing): return '$'+thing 
def gen_dot(oplist): return '.'.join(oplist)
def gen_case(caselist):
    if caselist == []: # no more and no "default" is set:
        return ";"
    thisexp=caselist[0]
    cond, exp = thisexp
    if cond == "else": 
        return exp
    return "if("+cond+"){"+exp+"}else{" + gen_case(caselist[1:]) + "}"
def gen_if(iflist): 
    cond, then, _else = iflist  
    return "if("+cond+"){"+then+"}" + ("else{" + _else + "}" if _else is not '' else '')

def parse(sexp, env=[]):
    if type(sexp) != list: # primitive!
        if sexp.startswith(tuple(map(str,range(0,9))))\
                or sexp.startswith('"')\
                or sexp.startswith('/')\
                or sexp in env\
                or sexp == 'else':
            return sexp
        else: 
            return gen_dollar(sexp)
    leader = sexp[0]
    if leader == "begin":
        return gen_codeblock([parse(p, env) for p in sexp[1:]])
    elif leader == "cond":
        return gen_case([[parse(c, env), parse(e, env)] for c, e in sexp[1:]])
    elif leader == 'let':
        names = [n for (n, v) in sexp[1]]
        return gen_codeblock(
                [gen_let([[n, parse(v, env)] for (n,v) in sexp[1]])] +
                [parse(p, names) for p in sexp[2:]])
    elif leader == '$' : # force dollar.
        return gen_dollar(sexp[1])
    elif leader == '!$' : # force undollar.
        return sexp[1]
    elif leader == '.':
        dotleader = sexp[1]
        return gen_dot([parse(dotleader, env)] +\
                [parse(p, env) if type(p) is list else p for p in sexp[2:]]) # we must prevent 
    elif leader == 'if':
        return gen_if([parse(p, env) for p in sexp[1:]]) if len(sexp) == 4 else\
                gen_if([parse(p, env) for p in sexp[1:]]+[''])
    elif leader in unary_ops:
        return gen_unary(leader, parse(sexp[1], env))
    elif leader in binary_ops:
        return gen_binary(leader, parse(sexp[1], env), parse(sexp[2], env))
    elif leader in arbitrary_ops:
        return gen_arbitrary(leader, [parse(p, env) for p in sexp[1:]])
    else:
        return gen_funcall(leader,
                [parse(p, env) for p in sexp[1:]])

with open(sys.argv[1], 'r') as f:
    sexp  = f.read()
    try:
        data = OneOrMore(nestedExpr()).parseString(sexp)
    except:
        print('Syntax error.') ; exit(1)
    print(parse(list(data)[0].asList()))
