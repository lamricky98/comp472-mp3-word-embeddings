import csv
import json

import pandas as pd
import gensim.downloader as api

if __name__ == '__main__':
    pd.set_option('display.max_columns', None)

    synom = pd.read_csv("synonyms.csv")

    csvLines = synom.iloc[:, 0:].values
    questionList = []
    answerList = []
    choice1List = []
    choice2List = []
    choice3List = []
    choice4List = []

    # Appending question words into a new list
    for line in csvLines:
        questionList.append(line[0])
        answerList.append(line[1])
        choice1List.append(line[2])
        choice2List.append(line[3])
        choice3List.append(line[4])
        choice4List.append(line[5])

    model_to_use = "glove-twitter-200"

    model = api.load(model_to_use)

    f = open('{}-details.csv'.format(model_to_use), 'w', newline='')
    # create the csv writer
    writer = csv.writer(f)

    correct_C = 0
    no_guess_V = 0
    for i in range(len(questionList)):
        counter = 0
        cosineList = []
        most_similar_key = ""
        answerCorrect = ""

        #Check to see if question-word is in the vocabulary
        try:
            result = model.most_similar(questionList[i])
            most_similar_key, similarity = result[0]
        except KeyError:
            answerCorrect = "guess"
            most_similar_key = "question-word not found in model"
            print("{},{},{},{}".format(questionList[i], answerList[i], most_similar_key, answerCorrect))
            data = [questionList[i], answerList[i], most_similar_key, answerCorrect]
            writer.writerow(data)
            continue

        # Check the "most similar words", using the default "cosine similarity" measure.

        try:
            cosineList.append(model.similarity(questionList[i], choice1List[i]))
        except Exception:
            counter += 1
            cosineList.append(0)

        try:
            cosineList.append(model.similarity(questionList[i], choice2List[i]))
        except Exception:
            counter += 1
            cosineList.append(0)

        try:
            cosineList.append(model.similarity(questionList[i], choice3List[i]))
        except Exception:
            counter += 1
            cosineList.append(0)

        try:
            cosineList.append(model.similarity(questionList[i], choice4List[i]))
        except Exception:
            counter += 1
            cosineList.append(0)

        if counter >= 4:
            #this is the case if none of the words from the choices exist in the vocabulary
            #we extract from the model the most similar word to the question word
            answerCorrect = "guess"
            result = model.similar_by_word(questionList[i])
            most_similar_key, similarity = result[0]
            print("{},{},{},{}".format(questionList[i], answerList[i], most_similar_key, answerCorrect))
            data = [questionList[i], answerList[i], most_similar_key, answerCorrect]
            writer.writerow(data)
            continue

        max_value = max(cosineList)
        max_index = cosineList.index(max_value)

        if max_index == 0:
            most_similar_key = choice1List[i]
        elif max_index == 1:
            most_similar_key = choice2List[i]
        elif max_index == 2:
            most_similar_key = choice3List[i]
        elif max_index == 3:
            most_similar_key = choice4List[i]

        if (most_similar_key == answerList[i]):
            answerCorrect = "correct"
            correct_C += 1
            no_guess_V += 1
        elif (most_similar_key == choice1List[i] or most_similar_key == choice2List[i] or most_similar_key ==
              choice3List[i] or most_similar_key == choice4List[i] and most_similar_key != answerList[i]):
            answerCorrect = "wrong"
            no_guess_V += 1
        print("{},{},{},{}".format(questionList[i], answerList[i], most_similar_key, answerCorrect))

        data = [questionList[i], answerList[i], most_similar_key, answerCorrect]
        writer.writerow(data)

    model_info = api.info(model_to_use)
    vocab_len = model_info["num_records"]

    accuracy = correct_C/no_guess_V
    analysis_f = open('analysis.csv', 'a+', newline='')
    # create the csv writer
    analysis_writer = csv.writer(analysis_f)

    data = [model_to_use, vocab_len, correct_C, no_guess_V, accuracy]
    analysis_writer.writerow(data)




