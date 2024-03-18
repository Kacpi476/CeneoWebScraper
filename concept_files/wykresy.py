import matplotlib.pyplot as plt
import pandas as pd

data = pd.read_json("reviews_160753591.json")

#kod do liczby poszczeglonych ocen
score_0 = 0
score_05 = 0
score_1 = 0
score_15 = 0
score_2 = 0
score_25 = 0 
score_3 = 0
score_35 = 0
score_4 = 0
score_45 = 0
score_5 = 0

for i in data["user_score"]:
    if i == "0/5":
        score_0 += 1
    if i == "0,5/5":
        score_05 += 1
    if i == "1/5":
        score_1 += 1
    if i == "1,5/5":
        score_15 += 1
    if i == "2/5":
        score_2 += 1
    if i == "2,5/5":
        score_25 += 1
    if i == "3/5":
        score_3 += 1
    if i == "3,5/5":
        score_35 += 1
    if i == "4/5":
        score_4 += 1
    if i == "4,5/5":
        score_45 += 1
    if i == "5/5":
        score_5 += 1

data_ocena = {
    "0/5":score_0,
    "0,5/5": score_05,
    "1/5": score_1,
    "1,5/5": score_15,
    "2/5": score_2,
    "2,5/5": score_25,
    "3/5": score_3,
    "3,5/5": score_35,
    "4/5": score_4,
    "4,5/5": score_45,
    "5/5": score_5,
}

#kod do sreniej oceny
sum_oceny = 0
for user_score in data["user_score"]:
    if user_score == "0/5":
        sum_oceny += 0
    if user_score == "0,5/5":
        sum_oceny += 0.5
    if user_score == "1/5":
        sum_oceny += 1
    if user_score == "1,5/5":
        sum_oceny += 1.5
    if user_score == "2/5":
        sum_oceny += 2
    if user_score == "2,5/5":
        sum_oceny += 2.5
    if user_score == "3/5":
        sum_oceny += 3
    if user_score == "3,5/5":
        sum_oceny += 3.5
    if user_score == "4/5":
        sum_oceny += 4
    if user_score == "4,5/5":
        sum_oceny += 4.5
    if user_score == "5/5":
        sum_oceny += 5
srednia_ocen = sum_oceny/5
print(srednia_ocen)

y = [srednia_ocen,5]

plt.pie(y)
plt.show()