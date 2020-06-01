## Word to vector

This project trains word embedding based on word2vec algorithm and Skip-gram model.

### Developer

Chansoo Kim
5.30.2020

### Contents
- README.md
- word2vec
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

 1. Collect sentences on an txt file, and place only one sentence in each line
 2. Run 'combine_text.py' (You'll select the text file you wrote)
 3. Run 'run_word2vec.py' (This will have you save two tsv files)
 4. Copy URL on the script 'run_word2vec.py', and enter the webpage  
 5. Hit the 'Load' button and upload two tsv files

### Environment
- Mac OSX Catalina 10.15.4
- Python v.3.7
- Tensorflow v.2.2.0

