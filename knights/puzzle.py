from logic import *

AKnight = Symbol("A is a Knight")
AKnave = Symbol("A is a Knave")

BKnight = Symbol("B is a Knight")
BKnave = Symbol("B is a Knave")

CKnight = Symbol("C is a Knight")
CKnave = Symbol("C is a Knave")

#Base Knowledge about game
#If a knight states a sentece the sentence is true. If a knave states a sentece the sentece is false.
#Each character is either a knight or a knave

# Puzzle 0
# A says "I am both a knight and a knave.""
message_puzzle0 = And(AKnight,AKnave)
knowledge0 = And(
    Or(AKnight, AKnave),
    Or(
        And(AKnave,Not(message_puzzle0)),
        And(AKnight,(message_puzzle0)),
    )
)

# Puzzle 1
# A says "We are both knaves."
# B says nothing.
message_puzzle1 = And(AKnave,BKnave)
knowledge1 = And(
    Or(AKnave,AKnight),
    Or(BKnave,BKnight),
    Biconditional(AKnight,message_puzzle1),
    Biconditional(AKnave,Not(message_puzzle1))
)

# Puzzle 2
# A says "We are the same kind."
# B says "We are of different kinds."
message_puzzle2A = Or(
    And(AKnave,BKnave),
    And(AKnight,BKnight)
)
message_puzzle2B = Or(
    And(AKnave,BKnight),
    And(BKnave,AKnight)
)
knowledge2 = And(
    Or(AKnight,AKnave),
    Or(BKnave,BKnight),
    Biconditional(AKnave,Not(message_puzzle2A)),
    Biconditional(AKnight,message_puzzle2A),
    Biconditional(BKnave,Not(message_puzzle2B)),
    Biconditional(BKnight,message_puzzle2B)
)

# Puzzle 3
# A says either "I am a knight." or "I am a knave.", but you don't know which.
# B says "A said 'I am a knave'."
# B says "C is a knave."
# C says "A is a knight."
message_puzzle3C = AKnight
message_puzzle3B = And(
    CKnave,
    AKnave,
)
message_puzzle3A = Or(
    AKnight,
    AKnave
)

knowledge3 = And(
    Or(AKnight,AKnave),
    Or(BKnave,BKnight),
    Or(CKnave,CKnight),

    Biconditional(AKnight,message_puzzle3A),
    Biconditional(AKnave,Not(message_puzzle3A)),
    Biconditional(BKnave,Not(message_puzzle3B)),
    Biconditional(BKnight,message_puzzle3B),
    Biconditional(CKnave,Not(message_puzzle3C)),
    Biconditional(CKnight,message_puzzle3C),
)


def main():
    symbols = [AKnight, AKnave, BKnight, BKnave, CKnight, CKnave]
    puzzles = [
        ("Puzzle 0", knowledge0),
        ("Puzzle 1", knowledge1),
        ("Puzzle 2", knowledge2),
        ("Puzzle 3", knowledge3)
    ]
    for puzzle, knowledge in puzzles:
        print(puzzle)
        if len(knowledge.conjuncts) == 0:
            print("    Not yet implemented.")
        else:
            for symbol in symbols:
                if model_check(knowledge, symbol):
                    print(f"    {symbol}")


if __name__ == "__main__":
    main()
