from flask import Flask, render_template, request, redirect, url_for, send_file
from bs4 import BeautifulSoup
import requests
import re
import pandas as pd
import json

app = Flask(__name__)

products = []
products_info = []

class ProductInfo:
    def __init__(self, product_id, opinions_count, cons_count, pros_count, average_score):
        self.product_id = product_id
        self.opinions_count = opinions_count
        self.cons_count = cons_count
        self.pros_count = pros_count
        self.average_score = average_score

def is_valid_product_id(product_id):
    return len(product_id) == 9 and product_id.isdigit()

def check_product_exists(product_id):
    url = f"https://www.ceneo.pl/{product_id}"
    response = requests.head(url)
    return response.status_code == 200

def scrape_data(product_id):
    url = f"https://www.ceneo.pl/{product_id}#tab=reviews"
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
    sum_oceny = 0
    cons_count = 0
    pros_count = 0
    for i in range(1, liczba_stron + 1):
        if i <= 1:
            url = f"https://www.ceneo.pl/{product_id}#tab=reviews"
        if i > 1:
            url = f"https://www.ceneo.pl/{product_id}/opinie-{i}"

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
                "author": author.text.strip() if author else "",
                "recomendation": author_recomendation.text.strip() if author_recomendation else "",
                "user_score": user_score.text if user_score else "",
                "purchase_confirmation": "Potwierdzenie zakupu" if purchase_confirmation else "",
                "yes_count": yes.text if yes else "",
                "no_count": no.text if no else "",
                "text": user_text.text if user_text else "",
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
                            pros_count += 1
                            zalety.append(item.text)
                        if licznik_pros_cons == 1:
                            cons_count += 1
                            wady.append(item.text)
                    licznik_pros_cons += 1
                opinia_data["zalety"] = zalety
                opinia_data["wady"] = wady
            else:
                opinia_data["zalety"] = ""
                opinia_data["wady"] = ""

            opinie_data.append(opinia_data)

            counter += 1
            count += 1

    with open(f"reviews_{product_id}.json", "w", encoding="utf-8") as json_file:
        json.dump(opinie_data, json_file, ensure_ascii=False, indent=4)

    #użycie pandas wyłącznie żeby sie zapoznać
    data = pd.read_json(f"reviews_{product_id}.json")
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
    srednia_ocen = round(sum_oceny/liczba_opini,1)
    average_score = srednia_ocen

    product_info = ProductInfo(product_id, len(opinie_data), cons_count, pros_count, average_score)
    products_info.append(product_info)


@app.route("/")
def home():
    return render_template("home.html")




@app.route('/extract')
def index():
    return render_template('extract.html', message="")




@app.route("/add_product", methods=['POST'])
def add_product():
    product_id = request.form['product_id']
    if not product_id or not is_valid_product_id(product_id) or not check_product_exists(product_id):
        return render_template('extract.html', message="Nieprawidłowy kod produktu.")
    elif product_id in products:
        return render_template('extract.html', message="Ten produkt został już dodany.")
    else:
        products.append(product_id)
        scrape_data(product_id)
        #print(products)
        return render_template('extract.html', message="Produkt został dodany.")




@app.route("/data")
def data():
    return render_template("data.html", products_info = products_info)



@app.route('/data/<product_id>')
def get_reviews(product_id):
    with open(f"reviews_{product_id}.json", "r", encoding="utf-8") as json_file:
        reviews = json.load(json_file)
    return render_template('opinions.html', product_id=product_id, opinions=reviews)

@app.route('/download_json/<product_id>')
def download_json(product_id):
    filename = f"reviews_{product_id}.json"
    return send_file(filename, as_attachment=True)


@app.route("/about")
def about():
    return render_template("about.html")

if __name__ == "__main__":
    app.run(debug=True)