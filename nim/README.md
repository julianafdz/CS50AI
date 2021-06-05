# Nim

Write an AI that teaches itself to play Nim through reinforcement learning.

In particular, we use Q-learning for this project, where we try to learn a reward value (a number) for every (state, action) pair. An action that loses the game have a reward of -1, an action that results in the other player losing the game have a reward of 1, and an action that results in the game continuing has an immediate reward of 0, but also have some future reward.

The key formula for Q-learning is below.

**Q(s, a) <- Q(s, a) + alpha * (new value estimate - old value estimate)**

$ python play.py
Playing training game 1
Playing training game 2
Playing training game 3
...
Playing training game 9999
Playing training game 10000
Done training

Piles:
Pile 0: 1
Pile 1: 3
Pile 2: 5
Pile 3: 7

AI's Turn
AI chose to take 1 from pile 2.