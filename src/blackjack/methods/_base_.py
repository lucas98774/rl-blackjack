from abc import ABC, abstractclassmethod
from functools import wraps
from random import random
from typing import Tuple

# setup helpers for types
_state = Tuple[int, int]
_state_and_action = Tuple[int, int, str]

# utility functions

def iterative_mean(current_val, current_mean, count) -> Tuple[float, int]:
    """
    Function to compute the iterative mean

    Parameters
    ----------
    current_val : float
        the current value to add to the mean (this will be the reward)
    current_mean : float
        the current mean (this will be the current return)
    count : int
        the number of observations so far

    Returns
    -------
    new_mean : float
        the updated mean
    count : int
        the updated number of observations
    """
    # see here: https://datagenetics.com/blog/november22017/index.html#:~:text=To%20find%20the%20mean%2C%20you,Done!
    # NOTE: could also use the sum of the numbers which may be better in the long term
    return count+1, current_mean + (current_val - current_mean) / (count+1)


def make_soft_policy(actions, prob=.05):
    """ decorator with args """
    def outer(func):
        """ decorator to make a policy e-greedy (instead of just deterministic) """
        @wraps(func)
        def inner(*args, **kwargs):
            greedy_action = func(*args, **kwargs)

            # TODO: check this conditions ...
            if random() < prob:
                other_action = [other_action for other_action in actions if other_action != greedy_action][0]
                return other_action


            return greedy_action
        return inner
    return outer


class RLMethod(ABC):
    """
    This is a template for a reinforcement learning algorithm

    Reinforemcent learning algorithms will be responsible for two functions:
    1. providing a method to update the policy --- policy improvement
    2. providing a method to update the state-action (value function) --- policy evaluation
    """
    @abstractclassmethod
    def policy_improvement(self):
        """ Function to update a given policy """
        pass

    @abstractclassmethod
    def policy_evaluation(self):
        """ Function to update a given state-action function """
        pass
