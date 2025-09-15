from flask import Flask, jsonify

app = Flask(__name__)

books = [
    {"id": 1, "title": "Сборник цитат", "author": "Кама Пуля"},
    {"id": 2, "title": "Мне этот мир абсолюно понятен", "author": "Идущий к реке"},
    {"id": 3, "title": "Наеби но не проколись", "author": "Дастан Жанибеков"}
]

@app.route("/books", methods=["GET"])
def get_books():
    return jsonify(books)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)

