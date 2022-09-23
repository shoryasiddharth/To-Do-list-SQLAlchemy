
from crypt import methods
from email.policy import default
import sys
from flask import Flask, render_template, request, redirect, url_for, jsonify, abort
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@localhost:5432/mydb'
db = SQLAlchemy(app)


class ToDo(db.Model):
    __tablename__ = 'todo'
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(), nullable=False)
    completed = db.Column(db.Boolean, default=False, nullable=False)

    def __repr__(self):
        return f'<ToDo id = {self.id} desc = {self.description}'


db.create_all()


@app.route('/todo/create', methods=['POST'])
def create_todo():
    body = {}
    error = False
    try:
        description = request.get_json()['description']
        todo = ToDo(description=description)
        body['description'] = todo.description
        db.session.add(todo)
        db.session.commit()
    except:
        error = True
        db.session.rollback()
        print(sys.exc_info())
    finally:
        db.session.close()
    if error:
        abort(500)
    return jsonify(body)


@app.route('/todo/<item_id>/update-checked', methods=['POST'])
def updateCheckStatus(item_id):
    body = {}
    try:
        checkStatus = request.get_json()['completed']
        todo = ToDo.query.get(item_id)
        todo.completed = checkStatus
        db.session.commit()
    except:
        db.session.rollback()
    finally:
        db.session.close()
    return redirect(url_for('index'))


@app.route('/todo/<deleteId>/delete-item', methods=['DELETE'])
def deleteItem(deleteId):
    try:
        todo = ToDo.query.get(deleteId)
        db.session.delete(todo)
        db.session.commit()
    except:
        db.session.rollback()
    finally:
        db.session.close()
    return jsonify({'success': True})


@app.route('/')
def index():
    return render_template('./index.html', data=ToDo.query.order_by("id").all())


# always include this at the bottom of your code (port 3000 is only necessary in workspaces)

if __name__ == '__main__':
    # app.run(debug=True)
    app.run(host="0.0.0.0", port=3000)
