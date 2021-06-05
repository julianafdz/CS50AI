# Project 6a: Parser

Write an AI to parse sentences and extract noun phrases.

Parsing is the process of determining the structure of a sentence, a common task in natural language processing. knowing the structure of a sentence can help a computer to better understand the meaning of the sentence, and it can also help the computer extract information out of a sentence. In particular, it’s often useful to extract noun phrases out of a sentence to get an understanding for what the sentence is about.

In this project, is used the context-free grammar formalism to parse English sentences to determine their structure. In a context-free grammar, we repeatedly apply rewriting rules to transform symbols into other symbols.

$ python parser.py
Sentence: Holmes sat.
        S
   _____|___
  NP        VP
  |         |
  N         V
  |         |
holmes     sat

Noun Phrase Chunks
holmes