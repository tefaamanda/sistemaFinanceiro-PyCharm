from flask import Flask, render_template, request, flash, url_for, redirect
import fdb

app = Flask(__name__)
app.config['SECRET_KEY'] = 'sua_chave_secreta_aqui'

host = 'localhost'
database = r'C:\Users\Aluno\Downloads\BANCOOO\BANCOSSS.FDB'
user = 'sysdba'
password = 'sysdba'

con = fdb.connect(host=host, database=database, user=user, password=password)

class livros:
    def __init__(self, id_livro, titulo, autor, ano_publicacao):
        self.id_livro = id_livro
        self.titulo = titulo
        self.autor = autor
        self.ano_publicacao = ano_publicacao

@app.route('/')
def index():
    cursor = con.cursor()
    cursor.execute('SELECT id_livro, titulo, autor, ano_publicacao FROM livros')
    livros = cursor.fetchall()
    cursor.close()
    return render_template('livros.html', livros=livros)

@app.route('/novo')
def novo():
    return render_template('novo.html', titulo='Novo Livro')

@app.route('/criar', methods=['POST'])
def criar():
    titulo = request.form['titulo']
    autor = request.form['autor']
    ano_publicacao = request.form['ano_publicacao']

    cursor = con.cursor()

    try:
        cursor.execute('select 1 from livros where titulo = ?', (titulo,))
        if cursor.fetchone():
            flash('Erro: Livro já cadastrado', 'error')
            return redirect(url_for('novo'))
        cursor.execute('INSERT INTO livros (TITULO, AUTOR, ANO_PUBLICACAO) VALUES (?, ?, ?)', (titulo, autor, ano_publicacao))
        con.commit()

    finally:
        cursor.close()
    flash('Livro cadastrado com sucesso!', 'success')
    return redirect(url_for('index'))

@app.route('/atualizar')
def atualizar():
    return render_template('editar.html', titulo='Editar Livro')

@app.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar(id):
    cursor = con.cursor()
    cursor.execute("SELECT id_livro, titulo, autor, ano_publicacao FROM livros WHERE ID_LIVRO = ?", (id,))
    livro = cursor.fetchone()

    if not livro:
        cursor.close()
        flash('Livro não encontrado', 'error')
        return redirect(url_for('index'))
    if request.method == 'POST':
        titulo = request.form['titulo']
        autor = request.form['autor']
        ano_publicacao = request.form['ano_publicacao']

        cursor.execute("UPDATE livros SET titulo = ?, autor = ?, ano_publicacao = ? WHERE id_livro = ?", (titulo, autor, ano_publicacao, id))

        con.commit()
        cursor.close()
        flash('Livro atualizado com sucesso!', 'success')
        return redirect(url_for('index'))

    cursor.close()
    return render_template('editar.html', livro=livro, titulo='Editar Livro')

@app.route('/deletar/<int:id>', methods=['POST'])
def deletar(id):
    cursor = con.cursor()
    try:
        cursor.execute("DELETE FROM livros WHERE id_livro = ?", (id,))
        con.commit()
        flash('Livro Excluído com sucesso!', 'success')
    except Exception as e:
        con.rollback()
        flash('Erro ao excluir o livro.', 'error')
    finally:
        cursor.close()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)