from flask import Flask, render_template, request, url_for, redirect, jsonify
from flask_cors import CORS
import csv
import google.generativeai as genai
from markdown import markdown

app = Flask(__name__)
CORS(app)

genai.configure(api_key="AIzaSyDyU_qmGEJaZyuq1VYqCVoxZzxAnLRBVDc")

def chamar_api_gemini(pergunta):
    model = genai.GenerativeModel('gemini-2.0-flash', system_instruction="De respostas curtas e objetivas, com exemplos em codigos.")
    response = model.generate_content(pergunta)
    return response.text

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/sobre-equipe')
def sobre_equipe():
    return render_template('sobre.html')

@app.route('/fundamentos')
def fundamentos():
    return render_template('fundamentos.html')

@app.route('/duvidas', methods=['GET', 'POST'])
def duvidas():
    resposta = ""
    if request.method == 'POST':
        pergunta = request.form.get('pergunta', '')
        if pergunta.strip():
            try:
                resposta_bruta = chamar_api_gemini(pergunta)
                resposta = markdown(resposta_bruta)
            except Exception as e:
                resposta = f"Ocorreu um erro ao consultar a IA: {str(e)}"
    return render_template('duvidas.html', resposta=resposta)

@app.route('/dicionario')
def dicionario():
    return render_template('dicionario.html')

@app.route('/glossario')
def glossario():
    glossario_de_termos = []
    with open('bd_glossario.csv', newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile, delimiter=';')
        for linha in reader:
            glossario_de_termos.append(linha)
    return render_template('glossario.html', glossario=glossario_de_termos)

@app.route('/novo_termo')
def novo_termo():
    return render_template('novo_termo.html')

@app.route('/criar_termo', methods=['POST'])
def criar_termo():
    termo = request.form['termo']
    definicao = request.form['definicao']
    with open('bd_glossario.csv', 'a', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile, delimiter=';')
        writer.writerow([termo, definicao])
    return redirect(url_for('glossario'))

ARQUIVO_TERMO = 'termos.txt'

def carregar_termos():
    termos = []
    try:
        with open(ARQUIVO_TERMO, 'r', encoding='utf-8') as f:
            for linha in f:
                if ':' in linha:
                    termo, definicao = linha.strip().split(':', 1)
                    termos.append({'termo': termo, 'definicao': definicao})
    except FileNotFoundError:
        pass
    return termos

def salvar_termos(termos):
    with open(ARQUIVO_TERMO, 'w', encoding='utf-8') as f:
        for termo in termos:
            f.write(f"{termo['termo']}:{termo['definicao']}\n")

@app.route('/api/termos', methods=['GET'])
def get_termos():
    return jsonify(carregar_termos())

@app.route('/api/termos', methods=['POST'])
def adicionar_termo():
    dados = request.get_json()
    termo = dados.get('termo')
    definicao = dados.get('definicao')
    if not termo or not definicao:
        return jsonify({'erro': 'Termo e definição são obrigatórios'}), 400

    termos = carregar_termos()
    if any(t['termo'].lower() == termo.lower() for t in termos):
        return jsonify({'erro': 'Termo já existe'}), 400

    termos.append({'termo': termo, 'definicao': definicao})
    salvar_termos(termos)
    return jsonify({'mensagem': 'Termo adicionado com sucesso'})

@app.route('/api/termos/<termo>', methods=['PUT'])
def alterar_termo(termo):
    dados = request.get_json()
    nova_definicao = dados.get('definicao')
    if not nova_definicao:
        return jsonify({'erro': 'Nova definição é obrigatória'}), 400

    termos = carregar_termos()
    for t in termos:
        if t['termo'].lower() == termo.lower():
            t['definicao'] = nova_definicao
            salvar_termos(termos)
            return jsonify({'mensagem': 'Definição atualizada com sucesso'})
    return jsonify({'erro': 'Termo não encontrado'}), 404

@app.route('/api/termos/<termo>', methods=['DELETE'])
def deletar_termo(termo):
    termos = carregar_termos()
    novos_termos = [t for t in termos if t['termo'].lower() != termo.lower()]
    if len(novos_termos) == len(termos):
        return jsonify({'erro': 'Termo não encontrado'}), 404
    salvar_termos(novos_termos)
    return jsonify({'mensagem': 'Termo deletado com sucesso'})

if __name__ == '__main__':
    app.run(debug=True)
