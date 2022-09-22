
from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('./index.html', data=[{
        'description': 'Todo 1'
    }, {
        'description': 'Todo 2'
    }, {
        'description': 'Todo 3'
    }])


# always include this at the bottom of your code (port 3000 is only necessary in workspaces)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=3000)
