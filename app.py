from flask import Flask, render_template, request, redirect, url_for
from database import get_connection, create_table

app = Flask(__name__)

create_table()

# LISTAR
@app.route('/')
def index():
    conn = get_connection()
    registros = conn.execute('SELECT * FROM lista').fetchall()
    conn.close()
    return render_template('index.html', registros=registros)

# ADICIONAR
@app.route('/add', methods=('GET', 'POST'))
def add():
    if request.method == 'POST':
        titulo = request.form['titulo']
        tipo = request.form['tipo']
        indicado_por = request.form['indicado_por']

        if not titulo or not tipo:
            return "Título e Tipo são obrigatórios!"

        conn = get_connection()
        conn.execute(
            'INSERT INTO lista (titulo, tipo, indicado_por) VALUES (?, ?, ?)',
            (titulo, tipo, indicado_por)
        )
        conn.commit()
        conn.close()
        return redirect(url_for('index'))

    return render_template('form.html', registro=None)

# EDITAR
@app.route('/edit/<int:id>', methods=('GET', 'POST'))
def edit(id):
    conn = get_connection()
    registro = conn.execute('SELECT * FROM lista WHERE id = ?', (id,)).fetchone()

    if request.method == 'POST':
        titulo = request.form['titulo']
        tipo = request.form['tipo']
        indicado_por = request.form['indicado_por']

        conn.execute(
            'UPDATE lista SET titulo = ?, tipo = ?, indicado_por = ? WHERE id = ?',
            (titulo, tipo, indicado_por, id)
        )
        conn.commit()
        conn.close()
        return redirect(url_for('index'))

    conn.close()
    return render_template('form.html', registro=registro)

# EXCLUIR
@app.route('/delete/<int:id>')
def delete(id):
    conn = get_connection()
    conn.execute('DELETE FROM lista WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)