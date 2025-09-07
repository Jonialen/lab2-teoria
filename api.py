from fastapi import FastAPI
from pydantic import BaseModel

from shunting_yard import ShuntingYard
from ast_builder import ASTBuilder
from thompson import ThompsonConstructor
from subset_construction import SubsetConstruction
from dfa_minimizer import DFAMinimizer
from dfa_simulator import DFASimulator

app = FastAPI()

class MatchRequest(BaseModel):
    regex: str
    string: str

@app.post("/match")
def match_string(request: MatchRequest):
    """
    Checks if a string matches a regex using a minimized DFA.
    """
    try:
        # 1. Infix to Postfix
        sy = ShuntingYard()
        postfix_tokens, _ = sy.infix_to_postfix(request.regex)
        if not postfix_tokens:
            return {"match": False, "error": "Invalid regex expression"}

        # 2. Postfix to AST
        ast_builder = ASTBuilder()
        ast_root, _ = ast_builder.build_ast(postfix_tokens)

        # 3. AST to NFA (Thompson's construction)
        thompson = ThompsonConstructor()
        nfa = thompson.construct_nfa(ast_root)

        # 4. NFA to DFA (Subset construction)
        subset_builder = SubsetConstruction()
        dfa, _ = subset_builder.construct_dfa(nfa)

        # 5. Minimize DFA
        minimizer = DFAMinimizer()
        minimized_dfa, _ = minimizer.minimize_dfa(dfa)

        # 6. Simulate DFA
        simulator = DFASimulator(minimized_dfa)
        accepted, _ = simulator.simulate(request.string)

        return {"match": accepted}
    except Exception as e:
        return {"match": False, "error": str(e)}
