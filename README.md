## Word to vector

This project trains word embedding based on word2vec algorithm and Skip-gram model.

### Developer

Chansoo Kim
5.30.2020

### Contents
- combine_text.py
    - This script combines all collected sentences into one single line with start and end tokens.
    - This will have you save a text file with a long line that is combined with start tokens and end tokens
- run_word2vec.py
    - This script trains word embeddings
    - This will have you save two 'tsv' files, so that you can visualize vectors.
- sample.txt
    -  This file has example sentences to train
- combined.txt
    - All sentences  are combined with start tokens and end tokens

### Procedure

 1. Collect sentence and place only one sentence in each line
 2. Run 'combine_text.py'
 3. Run 'run_word2vec.py' (This will have you save two tsv files)
 4. Hit the URL on the script 'run_word2vec.py'  
 5. Hit the 'Load' button and upload two tsv files

### Environment
- Mac OSX Catalina 10.15.4
- Python v.3.7
- Tensorflow v.2.2.0

