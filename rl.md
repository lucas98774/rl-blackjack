# Reinforcement Learning

This file will be simply to formalize this problem and add some math to the problem to understand the different components of it.

## Initial Problem

The first version of this problem for reinforecement learning will simply be an agent versus the dealer. The goal is the agent will learn something similar to basic strategy and make informed decisions to play a game of blackjack. 

### Blackjack setup

The implementation could use the gym package to simulate the game however, since blackjack is a simple enough game we choose to build the game from scratch.

### Number of States

The number of states for this initial version of blackjack is:

$2, 3, ..., 30=29$ different states which represent the possibilites for the agent's hand

$2, ..., 11=10$ different states for the dealers hand which the agent can "see".

TODO: check if this statement below is correct ...
The combinations of the agents and the dealers states lead to a $10*29=290$ total possible states.

### Ideas for rl algorithm

The goal for implementing rl algorithms are to start simple but then expand to different types of methods and more complex methods. Replicated the solution from the book: Reinforcement Learning An Introduction by Sutton is probably a good place to look for a naive solution. 

## Extension

After solving the simple version of this problem an interesting extension to this problem would to play a game with more than just the dealer and the agent and add other players into the game but allow the agent to count cards and intake the other players cards into the decision making of the agent. One interesting note here is that when training the agent, number of other players in the game may need to be varied so the agent does not learn only how to play with n other players. TODO: Also figure out how to write down how this would impact the number of states for the game.