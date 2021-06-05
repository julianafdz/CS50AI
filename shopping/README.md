# Shopping

Write an AI to predict whether online shopping customers will complete a purchase.

This is done using a nearest-neighbor classifier with scikit-learn package. Given information about a user — how many pages they’ve visited, whether they’re shopping on a weekend, what web browser they’re using, etc. (data from a shopping website from about 12,000 users sessions) — the classifier predict whether or not the user will make a purchase. 

$ python shopping.py shopping.csv
Correct: 4088
Incorrect: 844
True Positive Rate: 41.02%
True Negative Rate: 90.55%