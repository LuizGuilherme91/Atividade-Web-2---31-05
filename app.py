from flask import Flask, render_template, request, redirect, url_for
import json
import os

app = Flask(__name__)

# Caminho absoluto do inventario.json (funciona em qualquer computador)
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

    # Regras de negócio: campos não podem ser vazios
    if not nome or not preco or not quantidade:
        return redirect(url_for('index'))  # você pode melhorar isso com uma mensagem de erro

    preco = float(preco)
    quantidade = int(quantidade)

    # Regra: não aceitar valores negativos
    if preco < 0 or quantidade < 0:
        return redirect(url_for('index'))

    produtos = ler_inventario()

    # ID automático simples
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


if __name__ == '__main__':
    app.run(debug=True)
