from compiler.grammar import Grammar


grammar_text = """
E -> E + T | T
T -> T * F | F
F -> ( E ) | id
"""


grammar = Grammar(grammar_text)

grammar.parse()

first_sets = grammar.calculate_first_sets()
follow_sets = grammar.calculate_follow_sets()


print("Non-terminals:")
print(grammar.non_terminals)

print("\nTerminals:")
print(grammar.terminals)

print("\nStart symbol:")
print(grammar.start_symbol)

print("\nProductions:")
for lhs, alternatives in grammar.productions.items():
    print(lhs, "->", alternatives)

print("\nFIRST sets:")
for non_terminal, first_set in first_sets.items():
    print(f"FIRST({non_terminal}) =", first_set)

print("\nFOLLOW sets:")
for non_terminal, follow_set in follow_sets.items():
    print(f"FOLLOW({non_terminal}) =", follow_set)

print("\nFIRST of sequences:")

print("FIRST(F) =", grammar.first_of_sequence(["F"]))

print("FIRST(T * F) =", grammar.first_of_sequence(["T", "*", "F"]))

print("FIRST(( E )) =", grammar.first_of_sequence(["(", "E", ")"]))

print("\nDirect left recursion:")

left_recursive = grammar.find_direct_left_recursion()

print(left_recursive)

print("\nGrammar after removing left recursion:")

grammar.remove_direct_left_recursion()

for lhs, alternatives in grammar.productions.items():
    print(lhs, "->", alternatives)

print("\nFIRST sets after removing left recursion:")

first_sets_after = grammar.calculate_first_sets()

for non_terminal, first_set in first_sets_after.items():
    print(f"FIRST({non_terminal}) =", first_set)


print("\nFOLLOW sets after removing left recursion:")

follow_sets_after = grammar.calculate_follow_sets()

for non_terminal, follow_set in follow_sets_after.items():
    print(f"FOLLOW({non_terminal}) =", follow_set)

print("\nLL(1) Parsing Table:")

parsing_table = grammar.build_parsing_table()

for non_terminal, row in parsing_table.items():

    print(f"\n{non_terminal}:")

    for terminal, production in row.items():

        print(
            f"  M[{non_terminal}, {terminal}] "
            f"= {non_terminal} -> {' '.join(production)}"
        )

print("\nLL(1) Parser Test:")

#result = grammar.parse_input("id + id * id")
result = grammar.parse_input("id + * id")

print("\nResult:")

if result["accepted"]:
    print("Input accepted")
else:
    print("Input rejected")
    print(result["error"])

print("\nParsing Steps:")

for step in result["steps"]:
    print(
        f"Stack: {step['stack']:<30}"
        f"Input: {step['input']:<25}"
        f"Action: {step['action']}"
    )


print("\nLeft Factoring Test:")

#factor_test = Grammar("""
#S -> a b | a c
#""")
factor_test = Grammar("""
S -> a b c | a b d
""")

factor_test.parse()

print("\nBefore left factoring:")

for lhs, alternatives in factor_test.productions.items():
    print(lhs, "->", alternatives)

factor_test.left_factor()

print("\nAfter left factoring:")

for lhs, alternatives in factor_test.productions.items():
    print(lhs, "->", alternatives)