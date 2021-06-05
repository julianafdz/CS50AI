# Heredity

Write an AI to assess the likelihood that a person will have a particular genetic trait. These relationships are modeled by forming a Bayesian Network of all the relevant variables.

Given information about people, who their parents are, and whether they have a particular observable trait caused by a given gene, the AI infer the probability distribution for each person’s genes, as well as the probability distribution for whether any person will exhibit the trait in question.

$ python heredity.py data/family0.csv
Harry:
  Gene:
    2: 0.0092
    1: 0.4557
    0: 0.5351
  Trait:
    True: 0.2665
    False: 0.7335
James:
  Gene:
    2: 0.1976
    1: 0.5106
    0: 0.2918
  Trait:
    True: 1.0000
    False: 0.0000
Lily:
  Gene:
    2: 0.0036
    1: 0.0136
    0: 0.9827
  Trait:
    True: 0.0000
    False: 1.0000