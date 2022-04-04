from ._base_ import RLMethod, _state, _state_and_action, iterative_mean
from random import choice
from typing import Dict, Tuple

class MonteCarloExploringStarts(RLMethod):
    """
    Class for monte carlo with exploring starts   

    """
    def __init__(self, init_val = 5) -> None:
        assert isinstance(init_val, (int,float)) or callable(init_val), "initial value must either be a float, int or callable" 
        self.init_val = init_val

    def _init_policy(self, player_values, dealer_values, actions) -> Dict[_state, str]:
        """ 
        Function to initialize the policy function --- policy intakes the state and then chooses an action 

        Parameters
        ----------
        player_values : List[int]
            possible values for the agents hand
        dealer_values : List[int]
            possible values for the dealers face up card
        actions : Dict[str, int]
            possible actions

        Returns
        -------
        policy_func : Dict[_state, str]
            an initialized poliy
        """
        policy_func = {}
        for player_value, dealer_value in [(player_value, dealer_value)  for player_value in  player_values for dealer_value in dealer_values]:
            # TODO: check this random initialization
            policy_func[(player_value, dealer_value)] = choice(list(actions.keys()))

        return policy_func

    def _init_q_func(self, player_values, dealer_values, actions) -> Dict[_state_and_action, float]:
        """ 
        Function to init the state-action function --- will estimate the return from the current state and action 
        
        Parameters
        ----------
        player_values : List[int]
            possible values for the agents hand
        dealer_values : List[int]
            possible values for the dealers face up card
        actions : Dict[str, int]
            possible actions

        Returns
        -------
        q_func : Dict[_state_and_action, float]
            initialized state-action function
        """
        q_func = {}

        for player_value, dealer_value, action in [(player_value, dealer_value, action) for player_value in player_values for dealer_value in dealer_values for action in actions.keys()]:
            val = self.init_val if isinstance(self.init_val, (float, int)) else self.init_val()
            q_func[player_value, dealer_value, action] = val

        return q_func

    def policy_evaluation(self, state_w_action, current_val, q_func, returns) -> Tuple[Dict[_state_and_action, float], Dict[_state_and_action, float]]:
        """ 
        Function to update the q (state-action) function

        Parameters
        ----------
        state_w_action : List[(int, int), str]
            current state with the action as well
        current_val : float
            current return for this episode
        q_func : Dict[_state_and_action, float]
            state-action function
        returns : Dict[_state_and_action, float]
            returns function --- NOTE: how is this different than the q_func???
        Returns
        -------
        q_func : Dict[_state_and_action, float]
            updated q_func --- (this is pass by reference but be explicity anyway)

        returns : Dict[_state_and_action, float]
            long term rewards from a state and action pair (this is pass by reference but be explicity anyway)
        """
        # TODO: is the returns dictionary needed? 
        count, previous_return = returns[state_w_action]

        new_count, new_return = iterative_mean(current_val, previous_return, count)
        returns[state_w_action] = (new_count, new_return) 
        q_func[state_w_action] = new_return
        return q_func, returns

    def policy_improvement(self, current_state, actions, policy_func) -> Dict[_state, str]:
        """ 
        Function to update the policy --- make it greedy wrt to the current state-action function
        
        Parameters
        ----------
        current_state : List[]
            current state (agent's total [int], dealer's total[int])
        actions : Dict[str, int]
            possible actions
        policy_func : Dict[(int, int), str]
            current policy

        Returns
        -------
        policy_func : Dict[(int, int), str]
            updated policy --- this is pass by reference but be explicity anyway
        """
        
        # find applicable states:
        relevant_actions = [(*current_state, action) for action in actions.keys()]
        # setup action space where we need to find the max
        action_space = {k:v for k,v in self.q_func if k in relevant_actions}

        # get the best action ...
        _, _, greedy_action = max(action_space, action_space.get)

        policy_func[current_state] = greedy_action
        return policy_func
