.. CheckersBot documentation master file, created by
   sphinx-quickstart on Sat Nov 10 17:25:28 2018.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to CheckersBot's documentation!
*****************************************

The Monte Carlo tree search algorithm has recently revolutionized the field of turn-based perfect information game playing. In this project, we intend use this tree search to create an artificially intelligent agent which can play checkers with a human being through a computer interface. We have implemented this algorithm using Monte Carlo tree search along with an modified Upper Confidence Bound to ensure that the search is directed toward moves which have higher probability of having a winning outcome. The modification is done to try to help the agent make agressive moves. We have collected some statistics by running multiple simulations of the agent performing at a set of specific hyperparameters against an agent with no intelligence, i.e. an agent playing random moves. Following are our observations:

- The agent wins all of the games played against a non-intelligent agent.
- The agent wins in an average of 80 moves.
- The agent wins 95% of games by eliminating all the opponents pieces and the remaining 5% by blocking all moves of the opponent.
- The agent initially eleminates a lot of pieces of the opponent but finds it harder to eliminate pieces as the game progresses which leads to prolonged games.

=======================================

.. automodule:: playCheckers
    :members:
.. automodule:: classes
    :members:
.. toctree::
   :maxdepth: 2
   :caption: Contents:



Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
