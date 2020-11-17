'''

# This script trains word embedding based on word2vec algorithm and Skip-gram model.

# Before you run this file, you need a txt file that is processed by the script 'combine_text.py'

# 'combine_text.py' combines all collected sentences into one single line with start and end tokens.

# When you finish the process in this script,
  you'll save 2 tsv files(word embedding matrix) to upload,
  and you can visualize vectors on the word2vec module online.

5.30.2020
Chansoo Kim

'''

import io
import numpy as np
from tensorflow import keras
from tensorflow.keras import layers
import matplotlib.pyplot as plt

# Setting parameter values.

input_text = "text_with_tokens.txt" # Choosing text to load.
word_range = 5 # Declaring the total number of words for input and output,
               # and it should be odd number and bigger than 3.
hidden_units = 1024 # Number of units in each hidden layer
batch_size = 32 # Size of the word chunk on each training loop
epoch = 20 # Total epochs
activation_function = 'relu' # Choosing activation function

# Splitting data ( total ratio should be 1.)
train_ratio = 0.8 # Traing data ratio (0.8 out of 1)
val_ratio = 0.1 # Validation data ratio (0.1 out of 1)
test_ratio = 0.1 # Test data ratio (0.1 out of 1)

# Function to convert word to one-hot vector
def word2onehot(word_list, word_dict):
    if type(word_list) is not list:
        word_list = [word_list]
    onehot_size = len(word_dict.keys())
    word_len = len(word_list)
    onehot = np.zeros([word_len, onehot_size], dtype="float32")
    for idx, word in enumerate(word_list):
        onehot[idx, word_dict[word]] = 1
    return onehot.flatten()

# Function to convert one-hot vector to word
def onehot2word(onehot_list, inverse_word_dict):
    onehot_len = len(onehot_list)
    word_len = len(inverse_word_dict.keys())
    word_range = int(onehot_len/word_len)
    new_onehot = onehot_list.reshape(word_range, word_len)
    recovered_word = []
    for idx in range(word_range):
        one_idx = int(np.where(new_onehot[idx]==1)[0])
        recovered_word.append(inverse_word_dict[one_idx])
    return recovered_word

# Checking window size. (total number of an input word and output words)
minimum_range = 3 # Minimum window size
                  # Skip-Gram model requires 1 input word, and at least 2 output words

# The minimum window size should be 3 (1 for input, 2 for output)
if word_range < minimum_range or word_range % 2 == 0:
    print("Word_range is too small or even number. it should be an odd number that is larger than 3.")
    exit()
# Defining index of the middle word
mid_idx = int(np.ceil(word_range / 2))

# Loading text
print("Loading text file...")
with open(input_text,'r',encoding='utf-8') as txt:
    new_lines = txt.readlines()[0]
    word_chunk = new_lines.split(' ')

# Creating dictionary
print("Extracting dictonary information from data...")
word_dict = {}
for w in word_chunk:
    if w not in word_dict.keys():
        word_dict[w] = len(word_dict)
# Creating inverse dictionary
inverse_word_dict = {v: k for k, v in word_dict.items()}

# Splitting data into input list and output list
print("Splitting data into input list and output list...")
word_num = len(word_chunk)
total_range = word_num - word_range
# Creating empty list (creating lists before the for loop to run it fast)
input_list = [None] * total_range
output_list = [None] * total_range
for start_idx in range(total_range):
    if start_idx % 100 == 0:
        print("Processing... {}/{}".format(start_idx, total_range))
    last_idx = start_idx + word_range
    input_list[start_idx] = word2onehot(word_chunk[start_idx+mid_idx-1], word_dict) # The middle word (input word)
    front_list = word2onehot(word_chunk[start_idx:start_idx+mid_idx-1], word_dict) # Words brefore the middle word
    end_list =word2onehot(word_chunk[start_idx+mid_idx:last_idx], word_dict) # Words after the middle word
    output_list[start_idx] = np.append(front_list,end_list) # Combining 'front_list' and 'end_list' into 'output_list'
# Changing lists into numpy arrays
input_list = np.asarray(input_list)
output_list = np.asarray(output_list)

# Splitting all data in to train, validation, test
print("Splitting all data into train, validation, test ...")
input_num = len(input_list)
train_range = int(np.round(input_num * train_ratio))
val_range = train_range + int(np.round(input_num * val_ratio))

train_input = input_list[0:train_range]
train_output = output_list[0:train_range]
val_input = input_list[train_range:val_range]
val_output = output_list[train_range:val_range]
test_input = input_list[val_range:]
test_output = output_list[val_range:]

# Building ANN
print("Building ANN...")
input_dim = input_list.shape[1]
output_dim = output_list.shape[1]

inputs = keras.Input(shape=(input_dim,), name='digits')
x = layers.Dense(hidden_units, activation=activation_function, name='dense_1')(inputs)
x = layers.Dense(hidden_units, activation=activation_function, name='dense_2')(x)
outputs = layers.Dense(output_dim, name='predictions')(x)

model = keras.Model(inputs=inputs, outputs=outputs)

model.compile(optimizer=keras.optimizers.RMSprop(),  # Optimizer.
              # Choosing loss function
              loss=keras.losses.CategoricalCrossentropy(from_logits=True),
              # List of metrics to monitor.
              metrics=['categorical_accuracy'])

print('Start training !')
# Training the model
history = model.fit(train_input, train_output,
                    batch_size=batch_size,
                    epochs=epoch,
                    # In order to monitor
                    # validation loss and metrics
                    # at the end of each epoch,
                    # some validation will be skipped
                    validation_data=(val_input, val_output))

# Training results
print('\nTraining result:', history.history)

# Extracting results from the model training
print('\nExtracting result from the model training...')
results = model.evaluate(test_input, test_output, batch_size=batch_size)
print('test loss, test acc:', results)

### Extracting trained word embeddings
e = model.layers[1]
weights = e.get_weights()[0]
print("word embedding matrix (total number of words, embedding size): {}".format(weights.shape)) # shape: (vocab_size, embedding_dim)

# Saving tsv files for visualization
out_v = io.open('vecs.tsv', 'w', encoding='utf-8')
out_m = io.open('meta.tsv', 'w', encoding='utf-8')

word_list = list(word_dict.keys())
for num, word in enumerate(word_list):
  vec = weights[num]
  out_m.write(word + "\n")
  out_v.write('\t'.join([str(x) for x in vec]) + "\n")
out_v.close()
out_m.close()

# Visualization
# Please hit the link below, click 'load' button to upload tsv files


####### http://projector.tensorflow.org/ #########

