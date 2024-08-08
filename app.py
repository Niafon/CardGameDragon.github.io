from flask import Flask, render_template, request, jsonify, abort
import random
import os
import json
from flask_cors import CORS

app = Flask(__name__)
cors = CORS(app)

class Card:
    def __init__(self, name, rarity, grade, image_url=None):
        self.name = name
        self.rarity = rarity
        self.grade = grade
        self.image_url = image_url
        self.price = self.set_price()

    def set_price(self):
        rarity_multiplier = {"Common": 1, "Rare": 2, "Epic": 4, "Legendary": 8}
        grade_multiplier = {"F": 1, "E": 2, "D": 3, "C": 4, "B": 5, "A": 6, "S": 7, "SS": 8}
        return random.randint(1, 10) * rarity_multiplier[self.rarity] * grade_multiplier[self.grade]

class User:
    def __init__(self):
        self.coins = 1000
        self.collection = []

user = User()
market = []

all_cards = [
    Card("Warrior", "Common", "C", "https://i.pinimg.com/originals/d3/e1/4b/d3e14b7c318ff2ddb4fe25fda8757d4f.jpg"),
    Card("Archer", "Common", "B", "https://furman.top/uploads/posts/2023-09/1694208426_furman-top-p-chernii-luchnik-oboi-instagram-46.jpg"),
    Card("Mage", "Rare", "A", "https://i.pinimg.com/originals/c2/2c/c8/c22cc8c30e7384e96c809fb8df10cdb4.jpg"),
    Card("Dragon", "Epic", "S", "https://gas-kvas.com/grafic/uploads/posts/2023-09/1695941957_gas-kvas-com-p-kartinki-drakon-drakon-43.jpg"),
    Card("Unicorn", "Legendary", "SS", "https://gas-kvas.com/grafic/uploads/posts/2023-09/1695883346_gas-kvas-com-p-kartinki-s-yedinorogom-19.jpg"),
    Card("Goblin", "Common", "F", "https://avavatar.ru/images/full/6/J87qemGYR9aGPBKt.jpg"),
    Card("Elf", "Rare", "B", "https://avatars.mds.yandex.net/i?id=3fa2c01846f29f769035cd3f461dd7ed057779f6-9181720-images-thumbs&n=13"),
    Card("Dwarf", "Epic", "A", "https://avatars.mds.yandex.net/i?id=21ffdfa25248671e7686b34391c9e56ded0738da295288a8-5248760-images-thumbs&n=13"),
    Card("Phoenix", "Legendary", "S", "https://img.razrisyika.ru/kart/116/1200/463754-ptica-feniks-24.jpg"),
]

@app.route('/')
def index():
    return render_template('index.html', user=user, market=market)

@app.route('/buy_pack')
def buy_pack():
    if user.coins >= 100:
        user.coins -= 100
        new_cards = random.choices(all_cards, k=3)
        user.collection.extend(new_cards)
        return jsonify({"success": True, "new_cards": [{"name": card.name, "rarity": card.rarity, "grade": card.grade} for card in new_cards]})
    return jsonify({"success": False, "message": "Not enough coins"})

@app.route('/market_sell', methods=['POST'])
def market_sell():
    card_name = request.form['card_name']
    price = int(request.form['price'])
    for card in user.collection:
        if card.name == card_name:
            user.collection.remove(card)
            market.append({"card": card, "price": price})
            return jsonify({"success": True})
    return jsonify({"success": False, "message": "Card not found in collection"})

@app.route('/market_buy', methods=['POST'])
def market_buy():
    card_name = request.form['card_name']
    for item in market:
        if item["card"].name == card_name:
            if user.coins >= item["price"]:
                user.coins -= item["price"]
                user.collection.append(item["card"])
                market.remove(item)
                return jsonify({"success": True, "coins": user.coins})
            else:
                return jsonify({"success": False, "message": "Not enough coins"})
    return jsonify({"success": False, "message": "Card not found in market"})

if __name__ == "__main__":
    app.run(port=8080)