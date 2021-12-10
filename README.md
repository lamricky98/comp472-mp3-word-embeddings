COMP 472 Mini Project 3 Fall 2021 by Solo Cup
-
Ricky Lam 40089502

How to run:

* Run the main_file.py file (Python 3.8 or newer is required). Edit line 29 model_to_use = "..." and place the embedding model of your choice inside the quotation marks.

* After the code is done running, a result will be appended to analysis.csv and a csv file with the name of the embedding will be generated.

* In analysis.csv, the format per line is as follows:

[name],[vocabulary size],[correct answers],[total number of questions that were not guessed],[accuracy]

* In [embedding model].csv, the format per line is as follows:

[question],[expected answer],[answer provided by model],[classification of answer provided by model]