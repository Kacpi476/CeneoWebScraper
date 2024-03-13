import matplotlib.pyplot as plt
import pandas as pd

data = pd.read_json("item_data/158841627.json")

poleca = 0
nie_poleca = 0
brak_polecenia = 0

for i in data["recomendation"]:
    if i == "Polecam":
        poleca +=1
    if i == "Nie polecam":
        nie_poleca +=1
    if i == "Brak polecenia":
        brak_polecenia +=1
data_polecenie = {
    "poleca": poleca,
    "nie poleca": nie_poleca,
    "brak polecenia": brak_polecenia,
}

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

#fig, ax = plt.subplots()

names = list(data_ocena.keys())
values = list(data_ocena.values())
names2 = list(data_polecenie.keys())
values2 = list(data_polecenie.values())

#ax.bar(names, values)
#plt.show()


fig, axs = plt.subplots(1, 2, figsize=(12, 12), sharey=True)
axs[0].bar(names, values)
axs[1].scatter(names2, values2)
fig.suptitle('Categorical Plotting')

plt.show()