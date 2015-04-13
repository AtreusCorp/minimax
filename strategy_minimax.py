from strategy import Strategy


class StrategyMinimax(Strategy):
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


def gen_move_dict(state):
    ''' (GameState, str) -> dict of {obj: float}

    Return a dictionary with the indices of each move in
    state.possible_next_moves() as keys and the score of next_player
    after applying the corresponding move.

    '''

    possible_moves = state.possible_next_moves()
    player_int = 0 if state.next_player == 'p1' else 1
    if not possible_moves:
        return {None: score(state)[player_int]}
    else:
        move_dict = {}
        possible_move_length = len(possible_moves)
        for move_index in range(possible_move_length):
            applied_state = state.apply_move(possible_moves[move_index])
            temp_dict = gen_move_dict(applied_state)
            scores = temp_dict.values()

            # max(scores) represents the score of the opponent after
            # next_player plays a move. So -max(scores) represents
            # the score of next_player before the move is played.

            # Ternary if is to ensure that move_dict_value doesn't get set
            # to -0.0
            move_dict_value = -max(scores) if max(scores) != 0.0 else 0.0
            move_dict[move_index] = move_dict_value
        return move_dict
