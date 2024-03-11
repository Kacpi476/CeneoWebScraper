from bs4 import BeautifulSoup
import requests
import re
import json
import os

url_item_id = "158841627"
url_item_id2 = "149676629"

file_name = f"item_data/{url_item_id}.json"
if os.path.exists(file_name):
    print("File already exists")
else:
    url = f"https://www.ceneo.pl/{url_item_id}#tab=reviews"
    page = requests.get(url)
    soup = BeautifulSoup(page.text, "html.parser")

    liczba_opini_div = soup.find("div", class_="score-extend__review")
    liczba_opini_text = liczba_opini_div.text

    xd = re.findall(r'\d+', liczba_opini_text)
    liczba_opini = int(xd[0])

    opinie_data = []

    last_digit = liczba_opini % 10

    liczba_stron = int(((liczba_opini - last_digit) / 10) + 1)
    count = 0
    counter = 0

    for i in range(1, liczba_stron + 1):
        print(i)
        if i <= 1:
            url = f"https://www.ceneo.pl/{url_item_id}#tab=reviews"
        if i > 1:
            url = f"https://www.ceneo.pl/{url_item_id}/opinie-{i}"

        page = requests.get(url)
        soup = BeautifulSoup(page.text, "html.parser")
        opinie = soup.find_all(class_="user-post user-post__card js_product-review")

        for comment in opinie:
            if counter == 10:
                counter = 0
            data_id = soup.find_all("a", class_="user-post", attrs={'data-review-id': True})
            comment_id = (data_id[counter]["data-review-id"])

            author = comment.find("span", class_="user-post__author-name")
            author_recomendation = comment.find('span', class_="user-post__author-recomendation")
            user_score = comment.find('span', class_="user-post__score-count")
            purchase_confirmation = comment.find('div', class_="review-pz")
            user_text = comment.find('div', class_="user-post__text")
            yes = comment.find('span', id=f"votes-yes-{int(comment_id)}")
            no = comment.find('span', id=f"votes-no-{int(comment_id)}")

            opinia_data = {
                "id": comment_id,
                "author": author.text.strip() if author else "Brak autora",
                "recomendation": author_recomendation.text.strip() if author_recomendation else "Brak polecenia",
                "user_score": user_score.text if user_score else "Brak oceny użytkownika",
                "purchase_confirmation": "Potwierdzenie zakupu" if purchase_confirmation else "Brak potwierdzenia",
                "yes_count": yes.text if yes else "Brak licznika pozytywnych opinii",
                "no_count": no.text if no else "Brak licznika negatywnych opinii",
                "text": user_text.text if user_text else "Brak tekstu opinii",
            }
            elements_with_timeline = comment.find_all(attrs={"datetime": True})
            opinia_data["date_posted"] = elements_with_timeline[0]["datetime"] if elements_with_timeline else ""
            opinia_data["date_purchased"] = elements_with_timeline[1]["datetime"] if len(elements_with_timeline) > 1 else ""

            licznik_pros_cons = 0
            pros_cons = comment.find_all("div", class_="review-feature__col")
            if pros_cons:
                zalety = []
                wady = []
                for element in pros_cons:
                    items = element.find_all("div", class_="review-feature__item")
                    for item in items:
                        if licznik_pros_cons == 0:
                            zalety.append(item.text)
                        if licznik_pros_cons == 1:
                            wady.append(item.text)
                    licznik_pros_cons += 1
                opinia_data["zalety"] = zalety
                opinia_data["wady"] = wady
            else:
                opinia_data["zalety"] = []
                opinia_data["wady"] = []

            opinie_data.append(opinia_data)

            counter += 1
            count += 1

    with open(f"item_data/{url_item_id}.json", "w", encoding="utf-8") as json_file:
        json.dump(opinie_data, json_file, ensure_ascii=False, indent=4)