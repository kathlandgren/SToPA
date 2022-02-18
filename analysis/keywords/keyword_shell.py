# README:
# - Paths may only work on Windows
# - See Requirements.txt for requirements (install with pip e.g.)
# - `stop.txt` is a list of stopwords for RAKE

# Expedite:
# - Create README.md

# Todo:
# - Generate text files in a separate module, load the text files to dicts in this module (loading currently takes about 30 seconds for our dataset of roughly 17000 entries)
# - Choose the right data structures - clean up the dictionaries for time and space complexity
# - IMPROVE HASHING by using a data type for the year-log number data as key
# - Implement fuzzy matching for keyword search (maybe even tab for suggested completions?)
# - Improve automatic keyword extraction (this is the mathy/computer sciencey part of the project), including preprocessing. Currently using RAKE
# - Clean up code
# - Actually `get` the entry, not just its index (see data structures bullet above)

# Features:
# - Implement searching by other fields (and show keywords, see below)
# - Show keywords by entry (e.g. enter "2019-04265" and get the fields and the keywords)
# - Consider scalability - what data structures do we need for about a million entries? Does a relational database make sense or is this shell ok for our purposes?

import csv
import RAKE
import operator
import shlex
import time

def main():
    while True:
        command = input("$ ")
        if command == "exit" or command == "quit":
            break
        elif command == "help":
            print("psh-police_query: a simple shell written in Python")
        else:
            execute_commands(command)

def execute_commands(command):
    try:
        run_command(command)
    except Exception:
        import traceback
        traceback.print_exc()
        print("psh-police_query: command not found or not incorrect syntax: {}".format(command))

def run_command(command):
    split = shlex.split(command)
    # $ keyword
    if split[0] == "keyword":
        print("Keyword or Keyphrase: " + split[1])
        print(keyword_dict[split[1]])
    else:
        raise Exception

narratives = dict()

# import 2020 logs
with open("..\\..\\data\\parsed_logs_2020.csv",mode='r',encoding="ANSI") as f:
    csv_reader = csv.reader(f)
    i = 0
    for line in csv_reader:
        narratives[i] = line[9]
        i += 1

# import 2019 logs        
offset = len(narratives)

with open("..\\..\\data\\parsed_logs_2019.csv",mode='r',encoding="ANSI") as f:
    csv_reader = csv.reader(f)
    i = 0
    for line in csv_reader:
        narratives[i + offset] = line[9]
        i += 1

keyword_dict = dict()

initial_time = time.time()
print("Loading data...")                
# extract some keywords
for i in range(len(narratives)):
    if (i == 0):
        pass
    else:
        rake_object = RAKE.Rake(".\\stop.txt")
        words = rake_object.run(narratives[i])
        for obj in words:
            word = obj[0]
            if word in keyword_dict:
                temp = keyword_dict[word]
                temp.append(i)
                keyword_dict[word] = temp
            else:
                temp = list()
                temp.append(i)
                keyword_dict[word] = temp

print("Data loaded in " + str(time.time() - initial_time) + " seconds.")
main()
