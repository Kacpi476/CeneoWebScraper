from flask import Flask, render_template, request, redirect, url_for
from bs4 import BeautifulSoup
import requests
import re
import json

app = Flask(__name__)

products = []

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

            opinie_data.append({
                "author": author.text.strip() if author else "Brak autora",
                "recomendation": author_recomendation.text.strip() if author_recomendation else "Brak polecenia",
                "user_score": user_score.text if user_score else "Brak oceny użytkownika",
                "purchase_confirmation": "Potwierdzenie zakupu" if purchase_confirmation else "Brak potwierdzenia",
                "yes_count": yes.text if yes else "Brak licznika pozytywnych opinii",
                "no_count": no.text if no else "Brak licznika negatywnych opinii",
                "text": user_text.text if user_text else "Brak tekstu opinii",
            })

            counter += 1
            count += 1

    with open(f"reviews_{product_id}.json", "w", encoding="utf-8") as json_file:
        json.dump(opinie_data, json_file, ensure_ascii=False, indent=4)

@app.route("/")
def home():
    return render_template("home.html")

@app.route('/extract')
def index():
    return render_template('extract.html')

@app.route("/add_product", methods=['POST'])
def add_product():
    product_id = request.form['product_id']
    if is_valid_product_id(product_id) and check_product_exists(product_id):
        if product_id not in products:
            products.append(product_id)
            scrape_data(product_id)
    return redirect(url_for('extract'))


@app.route("/data")
def data():
    return render_template("data.html", products=products)

@app.route('/dane/<product_id>')
def get_reviews(product_id):
    with open(f"reviews_{product_id}.json", "r", encoding="utf-8") as json_file:
        reviews = json.load(json_file)
    return render_template('opinions.html', product_id=product_id, opinions=reviews)



@app.route("/about")
def about():
    return render_template("about.html")

if __name__ == "__main__":
    app.run(debug=True)