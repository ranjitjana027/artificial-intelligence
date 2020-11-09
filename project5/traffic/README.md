### Exploring Tensorflow
- #### Increase in no. of Convolutional layers with same no. of filters
  - `Accuracy gets better` but `time complexity increases linearly`.
- #### Increase in no. of filters in Convolutional layers
  - `Higher accuracy`, also ` higher time complexity`.
- #### Increase in no. of pooling layers
  - `Lower accuracy` with `lower time complexity`
- #### Increase in pool size in pooling layer
  - `Lower accuracy with larger window` but `less time complexity`
- ####  Increase in size and numbers of hidden layer
  - `Accuracy increases up to a limit`.
- #### Effect of dropout
  - `Adding a dropout layer decreases accuracy during training` but observed `better testing accuracy than training accuracy`

### Process
>  1. One Convolutional layer with 16 filters of size 3x3 , one pooling layer of size 2x2 and one hidden layer of size 128 with dropout 0.5. Accuracy was very low.
>  2. Increased the size of hidden layer to 384. Observed testing accuracy was 0.8284.
>  3. Increased the no of filters in convolutional layer to 32. Testing accuracy increased  to 0.855 but training time complexity also increases.
>  4. Replaced the single hidden layer with two hidden layers with 0.2 and 0.3 dropout respectively. Observed testing accuracy decreases drastically to 0.05.
>  5. Added another convolutional of size 3x3 with 16 filters. After Epoch 4 reached to 0.9197 accuracy. Observed testing accuracy was 0.9707. Training time complexity was higher.
>  6. Changed the no of filters of the other convolutional layer from 32 to 16.
  Observed testing accuracy was 0.9584. Training time complexity was lower than previous one.
>  7. Revert back to the no of filter from 16 to 32 and add pooling layer of size 2x2. Observed testing accuracy was 0.9748. Looked optimal.
