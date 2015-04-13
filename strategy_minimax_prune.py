from strategy import Strategy


class StrategyMinimaxPrune(Strategy):
    ''' Interface to suggest the best possible moves.
    '''

    def suggest_move(self, state):
        ''' (GameState) -> Move

        Return the best possible move available in state.

        Overrides Strategy.suggest_move
        '''

        move_dict = gen_move_dict(state)
        possible_moves = state.possible_next_moves()
        if 1.0 in move_dict.values():
            for move_key in move_dict:
                if move_dict[move_key] == 1.0:
                    move = possible_moves[move_key]
                    return move
        elif 0.0 in move_dict.values():
            for move_key in move_dict:
                if move_dict[move_key] == 0.0:
                    move = possible_moves[move_key]
                    return move
        move = possible_moves[move_dict.popitem()[0]]
        return move


def score(state):
    ''' (GameState) -> tup of (float, float)

    Precondition: state.over

    Return a two item tuple representing the score of next_player and
    state.opponent() respectively.
    '''

    outcome = state.outcome()
    next_player = state.next_player
    outcome_tup = (outcome, outcome * -1.0) if next_player == 'p1' else\
                  (outcome * -1.0, outcome)
    return outcome_tup


def gen_move_dict(state, best_score=-1.0):
    ''' (GameState, str, float) -> dict of {obj: float}

    Return a dictionary with the indices of each move in
    state.possible_next_moves() as keys and the score of next_player
    after applying the corresponding move. best_score represents the best
    score for next_player seen so far (-1.0 by default).

    '''

    possible_moves = state.possible_next_moves()
    player_int = 0 if state.next_player == 'p1' else 1

    if not possible_moves:
        return {None: score(state)[player_int]}

    else:
        move_dict = {}
        possible_move_length = len(possible_moves)
        move_index = 0
        while (move_index in range(possible_move_length) and
               1.0 not in move_dict.values()):

            applied_state = state.apply_move(possible_moves[move_index])
            applied_state_moves = applied_state.possible_next_moves()
            if applied_state_moves:
                temp_dict = {}
                n = 0
                move = 0
                while move in range(len(applied_state_moves)) and n == 0:

                    # Look another move ahead
                    further_state = applied_state.apply_move(
                        applied_state_moves[move])
                    further_dict = gen_move_dict(further_state, best_score)

                    # max(scores) represents the score of the opponent after
                    # next_player plays a move. So -max(scores) represents
                    # the score of next_player before the move is played.

                    # Ternary if is to ensure that move_dict_value doesn't get
                    # set to -0.0
                    next_player_score = -max(further_dict.values()) \
                        if max(further_dict.values()) != 0.0 \
                        else 0.0

                    # Decide if we can stop looking in this applied state
                    n = 1 if next_player_score >= (-1 * best_score) else 0

                    # This is the dictionary that would be returned if
                    # next_player called this function.

                    # Ensure that this move is never picked if we already have
                    # a move of better or the same value.
                    temp_dict[move] = next_player_score if n == 0 else 1.0
                    move += 1
            else:
                temp_dict = gen_move_dict(applied_state, best_score)
            scores = temp_dict.values()
            move_dict_value = -max(scores) if max(scores) != 0.0 else 0.0
            best_score = max(move_dict_value, best_score)
            move_dict[move_index] = move_dict_value
            move_index += 1
        return move_dict
