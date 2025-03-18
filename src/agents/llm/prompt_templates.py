BASIC_PROMPT = """
You are playing Iterated Prisoner's Dilemma. 
{history}
Your current reputation is {reputation:.2f}.
Based on this, decide whether to cooperate (C) or defect (D).
"""

ADVANCED_PROMPT = """
You are playing Iterated Prisoner's Dilemma.

GAME RULES:
- If both players cooperate (C,C), both get {payoff_cc} points
- If you cooperate but opponent defects (C,D), you get {payoff_cd} and opponent gets {payoff_dc}
- If you defect but opponent cooperates (D,C), you get {payoff_dc} and opponent gets {payoff_cd}
- If both defect (D,D), both get {payoff_dd} points

GAME STATE:
{history}
Your current reputation: {reputation:.2f}
{rewards_info}

Based on this information, decide whether to cooperate (C) or defect (D).
"""