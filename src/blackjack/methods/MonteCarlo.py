from ._base_ import RLMethod, _state, _state_and_action, iterative_mean
from random import choice
from typing import Dict

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
        for player_value, dealer_value in player_values, dealer_values:
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

        for player_value, dealer_value, action in player_values, dealer_values, actions.keys():
            q_func[player_value, dealer_value, action] = self.init_val

        return q_func

    def policy_improvement(self, state_w_action, current_val, q_func) -> Dict[_state_and_action, float]:
        """ 
        Function to update the q (state-action) function

        Parameters
        ----------
        state_w_action : List[(int, int), str]
            current state with the action as well
        current_val : float
            the current value for the state-action (value) function
        Returns
        -------
        
        """
        # NOTE: This should technically be from the returns and not the q function --- is the returns needed??? 
        count, current_return = self.q_func[state_w_action]

        # NOTE: an explicit return list is not needed since we can incrementally keep track of the mean using the current
        # mean and the number of observations ...
        new_return, new_count = iterative_mean(current_val, current_return, count)
        q_func[state_w_action] = (new_count, new_return)
        return q_func

    def policy_evaluation(self, current_state, actions, policy_func) -> Dict[_state, str]:
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

        # note this is pass by reference but still return it anyway ...
        policy_func[current_state] = greedy_action
        return policy_func
