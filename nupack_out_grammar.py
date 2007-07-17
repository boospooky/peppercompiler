"""Grammar for Joe Zadeh's thermodynamic design output format"""

from pyparsing import *

List = lambda x: Group(ZeroOrMore(x))
Map = lambda f: (lambda s,t,l: map(f, l))

ParserElement.setDefaultWhitespaceChars(" \t")


var = Word(alphanums+"_-*")
int_ = Word(nums).setParseAction(Map(int))
float_ = Word(nums+"-.").setParseAction(Map(float))

seq = Word("ATUCG+")
struct = Word(".()+")

# (Variable_name, sequence, n(s*), gc content, mfe distance, ideal struct, actual mfe struct)
# Ignoring arbitrary integer ids
statement = Group(Suppress(int_ + ":") + var + Suppress(LineEnd()) + \
                  seq + float_ + float_ + int_ + Suppress(LineEnd()) + \
                  struct + Suppress(LineEnd()) + \
                  struct + Suppress(LineEnd()) )

# (struct1, struct2, sequence, n(s*), gc content, mfe distance, ideal struct, actual mfe struct)
# Ignoring arbitrary integer ids
bad_inter = Group(Suppress(int_ + ":") + var + Suppress("N") + var + Suppress(LineEnd()) + \
                  seq + float_ + float_ + int_ + Suppress(LineEnd()) + \
                  struct + Suppress(LineEnd()) + \
                  struct + Suppress(LineEnd()) )

end_statement = Suppress("Total n(s*) =") + float_

# Ignoring bad interactions for now.
document = StringStart() + List(statement) + Suppress(List(bad_inter)) + end_statement + Suppress(ZeroOrMore(LineEnd())) + StringEnd()

