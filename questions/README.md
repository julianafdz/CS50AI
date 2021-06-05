# Questions

Write an AI to answer questions.

Question Answering (QA) is a field within natural language processing focused on designing systems that can answer questions.
This question answering system perform two tasks, document retrieval and passage retrieval. This is done using tf-idf to rank documents based both on term frequency for words in the query as well as inverse document frequency for words in the query. Then is used a combination of inverse document frequency and a query term density measure (the proportion of words in the sentence that are also words in the query). 

$ python questions.py corpus
Query: What are the types of supervised learning?
Types of supervised learning algorithms include Active learning , classification and regression.

$ python questions.py corpus
Query: When was Python 3.0 released?
Python 3.0 was released on 3 December 2008.

$ python questions.py corpus
Query: How do neurons connect in a neural network?
Neurons of one layer connect only to neurons of the immediately preceding and immediately following layers.