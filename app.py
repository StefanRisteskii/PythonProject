from flask import Flask, render_template, request, redirect, url_for , flash
from models import db, Item
import os
app = Flask(__name__)
app.secret_key = "super-secret-key"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

from google import genai

MODEL_NAME = "gemini-3-flash-preview"

GEMINI_API_KEY = "AIzaSyCnoLWEsfX7hqCHq20d88cNWwVrtodiRYY"

with app.app_context():
    db.create_all()


def generate_text(prompt: str) -> str:
        # ова е функцијата којашто ќе ја користиме за да добиеме notes и description со помош на AI
        api_key = GEMINI_API_KEY

        if not api_key:
            return "GEMINI_API_KEY недостасува или е погрешен"

        client = genai.Client(
            api_key=api_key)  # креираме гемини клиент којшто ни овозможува комуникација со нивното АПИ

        try:
            response = client.models.generate_content(
                model=MODEL_NAME,
                contents=prompt,
            )
            return (response.text or "").strip() or "Нема резултат од AI (празен текст)."
        except Exception as e:
            return f"AI грешка: {e}"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/signup', methods=['POST'])
def signup():
    name = request.form.get('name')
    email = request.form.get('email')
    password = request.form.get('password')
    confirm = request.form.get('confirm_password')

    if not name or not email or not password or not confirm:
        flash("Fill all fields")
        return redirect(url_for('index'))

    if password != confirm:
        flash("Passwords do not match")
        return redirect(url_for('index'))

    return redirect(url_for('create'))

@app.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        item = Item(
            type=request.form['type'],
            title=request.form['title'],
            description=request.form['description'],
            location=request.form['location'],
            date=request.form['date'],
            contact=request.form['contact']
        )
        db.session.add(item)
        db.session.commit()
        return redirect(url_for('list_items'))

    return render_template('create.html')

@app.route('/list')
def list_items():
    items = Item.query.all()
    return render_template('list.html', items=items)

@app.route('/item/<int:item_id>')
def detail(item_id):
    item = Item.query.get_or_404(item_id)

    matches = Item.query.filter(
        Item.type != item.type,
        Item.location == item.location
    ).all()

    return render_template('detail.html', item=item, matches=matches)

@app.route('/ai/<int:item_id>')
def ai_improve(item_id):
    item = Item.query.get_or_404(item_id)
    prompt =  f"""
    Improve the description for this item. Create short description 2-3 sentences with these infomation in macedonian. Keep only the description nothing else.
    This {item.title.lower()} was {item.type.lower()}.
    Location: {item.location}.
    Please contact: {item.contact}.
    """
    item.ai_description = generate_text(prompt)

    db.session.commit()
    return redirect(url_for('detail', item_id=item.id))

@app.route('/delete/<int:id>', methods=['POST'])
def delete_item(id):
    item = Item.query.get_or_404(id)
    db.session.delete(item)
    db.session.commit()
    return redirect(url_for('list_items'))



if __name__ == '__main__':
    app.run(debug=True)


