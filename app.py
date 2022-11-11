from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

class ToDo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<note %r>' % self.id

@app.route('/', methods=['POST','GET'])
def index():
    if request.method == 'POST':
        note_content = request.form['content']
        new_note = ToDo(content=note_content)

        try:
            db.session.add(new_note)
            db.session.commit()
            return redirect('/')
        except:
            return 'Error adding note'
    else:
        notes = ToDo.query.order_by(ToDo.date_created).all()
        return render_template('index.html', notes=notes)

@app.route('/delete/<int:id>')
def delete(id):
    note_to_delete = ToDo.query.get_or_404(id)

    try:
        db.session.delete(note_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'Error deleting'

@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    note = ToDo.query.get_or_404(id)

    if request.method == 'POST':
        note.content = request.form['content']

        try:
            db.session.commit()
            return redirect('/')
        except:
            return 'Error updating'
    else:
        return render_template('update.html', note=note)

if __name__ == "__main__":
    app.run(debug=True)