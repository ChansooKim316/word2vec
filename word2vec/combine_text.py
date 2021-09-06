'''

# This script combines all collected sentences into one single line with start and end tokens.
  (example : [S] I'm heading to Starbucks [E] [S] Do you want some coffee? [E] [S] I'm good, thank you [E] )


'''

import re
import sys

# Checking arguments.
if len(sys.argv) != 3:
    print("Input arguments are incorrectly provided. Two argument should be assigned.")
    print("1. Input file.")
    print("2. Save file.")
    print("*** USAGE ***")
    print("For Mac(terminal) or Windows : python3 combine_text.py (FILE TO READ).txt (FILE TO SAVE).txt") # For terminal on Mac or Windows
    print("             -------------  OR ------------- ")
    print("For Linux : python combine_text.py $(FILE TO READ).txt $(FILE TO SAVE).txt") # on Linux
    exit()

# Corpus data directory
input_text=sys.argv[1]
save_file=sys.argv[2]

# Reading text file.
print("Reading text file: {}".format(input_text))
with open(input_text,'r',encoding='utf-8') as txt:
    new_lines = txt.readlines()

    # Attaching start and end tokens each sentence.
    combined_sent = ""
    for idx, line in enumerate(new_lines):
        line = re.sub("\n", "", line)
        # Combining all sentences into one single line.
        combined_sent += "[S] "+line+" [E] "

# Save combined file.
print("Saving combined sentences....")
with open(save_file, 'w', encoding='utf-8') as wrt:
    final_sent = re.sub(" $", "", combined_sent)
    wrt.write(combined_sent+"\n")

print("DONE!")
