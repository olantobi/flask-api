from flask import Flask, request, jsonify, abort, make_response
from flask_httpauth import HTTPBasicAuth
import sys

if sys.version_info[0] >= 3:
    unicode = str

app = Flask(__name__)
app.config["DEBUG"] = True
auth = HTTPBasicAuth()

# Create some test data for our catalog in the form of a list of dictionaries.
books = [
    {'id': 1,
     'title': 'A Fire Upon the Deep',
     'author': 'Vernor Vinge',
     'first_sentence': 'The coldsleep itself was dreamless.',
     'published': '1992'},
    {'id': 2,
     'title': 'The Ones Who Walk Away From Omelas',
     'author': 'Ursula K. Le Guin',
     'first_sentence': 'With a clamor of bells that set the swallows soaring, the Festival of Summer came to the city Omelas, bright-towered by the sea.',
     'published': '1973'},
    {'id': 3,
     'title': 'Dhalgren',
     'author': 'Samuel R. Delany',
     'first_sentence': 'to wound the autumnal city.',
     'published': '1975'}
]

@auth.get_password
def get_password(username):
    if (username == 'tobi'):
        return 'ola'
    return None

@auth.error_handler
def unauthorized():
    return make_response(jsonify({'error': 'Unauthorized access'}), 401)

@app.route('/', methods=['GET'])
@auth.login_required
def home():
    return 'Hello World!'

@app.route('/books', methods=['GET'])
@auth.login_required
def allBooks():
    return jsonify({'books': books})

@app.route('/books/<int:id>', methods=['GET'])
@auth.login_required
def getBook(id):
    book = [book for book in books if book['id'] == id]
    if len(book) == 0:
        abort(404)
    return jsonify({'book': book[0]})

@app.route('/books', methods=['POST'])
@auth.login_required
def addBook():
    if not request.json or not 'title' in request.json or not 'author' in request.json:
        abort(400)
    book = {
        'id': books[-1]['id'] + 1,
        'title': request.json['title'],
        'author': request.json['author'],
        'first_sentence': request.json.get('description', ""),
        'published': request.json.get('published', None)
    }
    books.append(book)
    return jsonify({'book': book}), 201

@app.route('/books/<int:id>', methods=['PUT'])
@auth.login_required
def updateBook(id):
    book = [book for book in books if book['id'] == id]
    if len(book) == 0:
        abort(404)
    if not request.json or not 'title' in request.json or not 'author' in request.json: 
        abort(400)
    book[0]['title'] = request.json.get('title', book[0]['title'])
    book[0]['author'] = request.json.get('author', book[0]['author'])
    book[0]['first_sentence'] = request.json.get('first_sentence', book[0]['first_sentence'])
    book[0]['published'] = request.json.get('published', book[0]['published'])

    return jsonify({'book' : book[0]})

@app.route('/books/<int:id>', methods=['DELETE'])
@auth.login_required
def deleteBook(id):
    book = [book for book in books if book['id'] == id]
    if len(book) == 0:
        abort(404)
    books.remove(book[0])
    return jsonify({'status': 'Deleted'})

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

@app.errorhandler(400)
def not_found(error):
    return make_response(jsonify({'error': 'Bad request'}), 400)

app.run()