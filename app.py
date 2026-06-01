from flask import Flask, render_template, request, redirect, url_for, jsonify
import json
import os

app = Flask(__name__)

CAMINHO_JSON = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'inventario.json')

def ler_inventario():
    try:
        with open(CAMINHO_JSON, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def gravar_inventario(dados):
    with open(CAMINHO_JSON, 'w', encoding='utf-8') as f:
        json.dump(dados, f, indent=4, ensure_ascii=False)


@app.route('/')
def index():
    produtos = ler_inventario()
    return render_template('index.html', produtos=produtos)


@app.route('/adicionar', methods=['POST'])
def adicionar():
    nome = request.form.get('nome', '').strip()
    preco = request.form.get('preco', '').strip()
    quantidade = request.form.get('quantidade', '').strip()

    if not nome or not preco or not quantidade:
        return redirect(url_for('index'))

    preco = float(preco)
    quantidade = int(quantidade)

    if preco < 0 or quantidade < 0:
        return redirect(url_for('index'))

    produtos = ler_inventario()

    # Bônus: bloquear nome duplicado (sem diferenciar maiúsculas/minúsculas)
    for p in produtos:
        if p['nome'].lower() == nome.lower():
            return redirect(url_for('index', erro='duplicado'))

    novo_id = (produtos[-1]['id'] + 1) if produtos else 1

    novo_produto = {
        'id': novo_id,
        'nome': nome,
        'preco': preco,
        'quantidade': quantidade
    }

    produtos.append(novo_produto)
    gravar_inventario(produtos)

    return redirect(url_for('index'))


@app.route('/atualizar/<int:produto_id>/<acao>', methods=['POST'])
def atualizar(produto_id, acao):
    produtos = ler_inventario()

    for p in produtos:
        if p['id'] == produto_id:
            if acao == 'aumentar':
                p['quantidade'] += 1
            elif acao == 'diminuir' and p['quantidade'] > 0:
                p['quantidade'] -= 1
            break

    gravar_inventario(produtos)
    return redirect(url_for('index') + '#consulta')


@app.route('/excluir/<int:produto_id>', methods=['POST'])
def excluir(produto_id):
    produtos = ler_inventario()
    produtos = [p for p in produtos if p['id'] != produto_id]
    gravar_inventario(produtos)
    return redirect(url_for('index') + '#consulta')


if __name__ == '__main__':
    app.run(debug=True)