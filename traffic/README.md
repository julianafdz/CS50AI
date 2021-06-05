# TRAFFIC

## The Process

First i took as starting base the convolutional neural network model of the lecture.
which has:

- a convolutional layer, learning 32 filters using a 3x3 kernel (activation function ReLU and an input shape as indicated in the project specification).
- a max-pooling layer, using a 2x2 pool size.
- a hidden layer with 128 units and a dropout of 0.5 (activation function ReLU).
- an output layer with output 43 (NUM_CATEGORIES) units for each of the traffic sign categories (activation function Softmax).

the results for this setting were: 3s - loss: 3.5070 - accuracy: 0.0520.

Then from this point i experiment with diferent alternatives, aiming for better accuracy results.

| Step  | Description                                                      | Accuracy  | Loss    |
|:-----:|:----------------------------------------------------------------:| ---------:| -------:|
| 1     | add second convolutional layer (= to firts layer)                |    0.9786 |  0.0928 |
| 2     | add third convolutional layer (= to firts layer)                 |    0.0560 |  3.4976 |
| 3     | delete the third convolutional layer                             |           |         |
| 4     | add second max-pooling layer (= to firts layer)                  |    0.9721 |  0.1117 |
| 5     | change setting position to conv layer - maxp layer - conv - maxp |    0.9357 |  0.2479 |
| 6     | delete the second max-pooling layer                              |           |         |
| 7     | double number of filters (64) for one convolutional layer        |    0.9426 |  0.2468 |
| 8     | restore number of filters to 32 for that convolutional layer     |           |         |
| 9     | double size of filters to 6x6 for one convolutional layer        |    0.9776 |  0.1149 |
| 10    | restore size of filters to 3x3 for that convolutional layer      |           |         |
| 11    | increase pool size to 4x4                                        |    0.9710 |  0.1113 |
| 12    | restore size of pool to 2x2                                      |           |         |
| 13    | add second hidden layer (= to firts layer)                       |    0.9627 |  0.1853 |
| 14    | delete the second hidden layer                                   |           |         |
| 15    | increase number of units inside hidden layer to 300              |    0.9657 |  0.1580 |
| 16    | decrease number of units inside hidden layer to 90               |    0.9610 |  0.1634 |
| 17    | restore number of units in hidden layer to 128                   |           |         |
| 18    | increase dropuot to 0.8                                          |    0.8775 |  0.4805 |
| 19    | decrease droputo to 0.2                                          |    0.9553 |  0.2073 |
| 20    | restore dropout to 0.5                                           |           |         |

## Conclusion

Based on the previous results, after traying different settings, adding, deleting and changing sizes of layers, the setting for the model that returns the highest accuracy rate is:

- 2 convolutional layers, learning 32 filters using a 3x3 kernel (activation function ReLU and an input shape as indicated in the project specification).
- 1 max-pooling layer, using a 2x2 pool size.
- 1 hidden layer with 128 units and a dropout of 0.5 (activation function ReLU).
- an output layer with output 43 (NUM_CATEGORIES) units for each of the traffic sign categories (activation function Softmax).

However, the results were not always the same and varied a little when repeating the process repeatedly in the same model.
