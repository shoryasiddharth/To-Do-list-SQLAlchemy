
from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@localhost:5432/mydb'
db = SQLAlchemy(app)


class ToDo(db.Model):
    __tablename__ = 'todo'
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(), nullable=False)

    def __repr__(self):
        return f'<ToDo id = {self.id} desc = {self.description}'


db.create_all()


@app.route('/todo/create', methods=['POST'])
def create_todo():
    body={}
    description = request.get_json()['description']
    todo = ToDo(description=description)
    body['description'] = todo.description
    db.session.add(todo)
    db.session.commit()
    return jsonify(body)


@app.route('/')
def index():
    return render_template('./index.html', data=ToDo.query.all())


# always include this at the bottom of your code (port 3000 is only necessary in workspaces)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=3000)
