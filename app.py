from flask import Flask, jsonify, request
import mysql.connector
from  mysql.connector import Error

mydb = mysql.connector.connect(
    host = 'localhost',
    user = 'root',
    password = '',
    database = 'books'
)

app = Flask(__name__)

@app.route('/livros', methods=['GET'])
def get_books():

    my_cursor = mydb.cursor()
    my_cursor.execute('SELECT * FROM books')
    books = my_cursor.fetchall()

    new_list_books = list()

    for book in books:
        new_list_books.append(
            {
                'id': book[0],
                'titulo': book[1],
                'autor': book[2],
            }
        )

    return jsonify(new_list_books)

@app.route('/livros', methods=['POST'])
def create_book():
    new_book = request.get_json()
    
    my_cursor = mydb.cursor()
    sql = f"INSERT INTO books (title, author) VALUES ('{new_book['titulo']}', '{new_book['autor']}')"
    my_cursor.execute(sql)
    mydb.commit()

    my_cursor.execute('SELECT * FROM books')
    books = my_cursor.fetchall()

    new_list_books = list()

    for book in books:
        new_list_books.append(
            {
                'id': book[0],
                'titulo': book[1],
                'autor': book[2],
            }
        )


    return jsonify(new_list_books)

@app.route('/livros/<int:id>', methods=['GET'])
def get_book_by_id(id):
    
    my_cursor = mydb.cursor()
    sql = f"SELECT * FROM books WHERE id = {id}"
    my_cursor.execute(sql)
    books = my_cursor.fetchall()
    
    if books == []:
        return jsonify(
            Mensagem = "Nenhum livro encontrado com esse id"
        )

    new_list_books = list()
    for book in books:
        new_list_books.append(
            {
                'id': book[0],
                'titulo': book[1],
                'autor': book[2],
            }
        )
    return jsonify(new_list_books)

@app.route('/livros/<int:id>', methods=['PUT'])
def edit_book_by_id(id):
    book_edited = request.get_json()
    
    my_cursor = mydb.cursor()
    sql = f'SELECT * FROM books where id = "{id}"'
    my_cursor.execute(sql)
    book1 = my_cursor.fetchall()

    for data in book_edited:
        sql = f"UPDATE books SET {data} = '{book_edited[data]}' WHERE id = {id}"
        my_cursor.execute(sql)
        mydb.commit()

    sql = f'SELECT * FROM books where id = {id}'
    my_cursor.execute(sql)
    book2 = my_cursor.fetchall()

    response = list()

    for book in book2:
        response.append(
            {
                'registro': 'novo',
                'id': book[0],
                'titulo': book[1],
                'autor': book[2],
            }
        )
    for book in book1:
        response.append(
            {
                'registro': 'antigo',
                'id': book[0],
                'titulo': book[1],
                'autor': book[2],
            }
        )

    return jsonify(response)

@app.route('/livros/<int:id>', methods=['DELETE'])
def drop_book(id):
    my_cursor = mydb.cursor()
    sql = f"SELECT * FROM books WHERE id = {id}"
    my_cursor.execute(sql)
    books = my_cursor.fetchall()

    if books == []:
        return jsonify(
                Mensagem = "Erro, livro não encontrado"
        )


    response = list()
    for book in books:
        response.append(
            {
                'id': book[0],
                'titulo': book[1],
                'autor': book[2],
            }
        )

    sql = f"DELETE FROM books WHERE id = {id}"
    my_cursor.execute(sql)
    bookas = my_cursor.fetchall()

    sql = f"SELECT * FROM books WHERE id = {id}"
    my_cursor.execute(sql)
    books_after = my_cursor.fetchall()

    if books_after == []:
        response.append(
            {
                "Mensagem" : "Deletado com sucesso"
            }
        )
    else :
        response.append(
            {
                "Mensagem" : "Falha ao tentar deletar"
            }
        )
    
    return jsonify(response)

app.run(port=5000, host='localhost', debug=True)