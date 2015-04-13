from strategy import Strategy
from strategy_minimax import StrategyMinimax


class StrategyMinimaxMemoize(Strategy):
    ''' Interface to suggest the best possible moves.
    '''
    def __init__(self, interactive=False):
        '''(Strategy, bool) -> NoneType

        Create new StrategyMinimaxMemoize (self), prompt user if interactive.
        '''

        self._stored_moves = {}

    def suggest_move(self, state):
        ''' (GameState) -> Move

        Return the best possible move available in state.

        Overrides Strategy.suggest_move
        '''

        if repr(state) not in self._stored_moves:
            gen_move_dict(state, self._stored_moves)

        moves = state.possible_next_moves()
        return moves[(self._stored_moves[repr(state)])[0]]


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


def best_move(move_dict):
    '''
    '''

    move_copy = move_dict.copy()
    if 1.0 in move_copy.values():
        for move_key in move_copy:
            if move_copy[move_key] == 1.0:
                return (move_key, 1.0)
    elif 0.0 in move_copy.values():
        for move_key in move_copy:
            if move_copy[move_key] == 0.0:
                return (move_key, 0.0)
    return move_copy.popitem()


def gen_move_dict(state, move_dict_storage):
    ''' (GameState, str, dict) -> dict of {obj: float}

    Return a dictionary with the indices of each move in
    state.possible_next_moves() as keys and the score of next_player
    after applying the corresponding move. move_dict_storage is used to keep
    track of which game states have been visited before (as keys) and which
    move is the best (represented in the corresponding values).

    '''

    possible_moves = state.possible_next_moves()
    player_int = 0 if state.next_player == 'p1' else 1
    if not possible_moves:
        return {None: score(state)[player_int]}

    elif repr(state) in move_dict_storage:
        return {move_dict_storage[repr(state)][0]:
                move_dict_storage[repr(state)][1]}

    else:
        move_dict = {}
        possible_move_length = len(possible_moves)
        for move_index in range(possible_move_length):
            applied_state = state.apply_move(possible_moves[move_index])
            temp_dict = gen_move_dict(applied_state, move_dict_storage)
            scores = temp_dict.values()
            # max(scores) represents the score of the opponent after
            # next_player plays a move. So -max(scores) represents
            # the score of next_player before the move is played.

            # Ternary if to ensure that move_dict_value doesn't get set
            # to -0.0
            move_dict_value = -max(scores) if max(scores) != 0.0 else 0.0
            move_dict[move_index] = move_dict_value

        # Store this move in move_dict_storage
        move_dict_storage[state.__repr__()] = best_move(move_dict)
        return move_dict
