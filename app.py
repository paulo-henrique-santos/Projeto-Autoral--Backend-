from flask import Flask, jsonify, request
from flask_cors import CORS
from google import genai
import json
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

CORS(app)

API_KEY = os.getenv("GENAI_APIKEY")

client = genai.Client(api_key=API_KEY)

def pesquisar_jogo(temas):
    prompt = f"""
        Pesquise um jogo somente com os seguintes temas: {temas}. Se o tema tiver palavras ilícitas como cocô, bosta, palavras de cunho sexual ou palavras preconceituosas, pessoas relacionadas a pornografia ou que cometeu crimes na vida real e palavras muito gráficas como tripa, morte, suícidio, não apresente o jogo e avise o usuário para usar outros temas. Apresente o jogo, sem o header, com o título em h1, subtítulos em h2, tempo de gameplay em parágrafo acompanhado de um emoji de relógio, plataforma do jogo em parágrafo acompanhado de um emoji de controle de vídeogame, o custo oficial do jogo em parágrafo acompanha de um emoji de dinheiro, a lista de temas em lista não ordenada, sinopse do jogo com a sinopse oficial do jogo, não se estenda muito na sinopse também.
        SEM HEAD, SEM BODY, SEM A ESTRUTURA BÁSICA DO HTML, APENAS COM O TÍTULO EM UM H2, SEPARANDO OS PARÁGRAFOS COM A TAG P DO HTML.
        NÃO COLOQUE NADA MAIS ALÉM DO H2 E P.
        SUBSTITUA AS '#' POR <h1> E OS FECHE DPS, '##' POR <h2> E O FECHE DPS.
        Não coloque aspas simples, nem aspas duplas, nem tags HTML no começo ou no final do texto. Não coloque nada além do que foi pedido.
        POR FAVOR, TIRE AS ASPAS SIMPLES E A TAG HTML NO COMEÇO POR FAVOR, POR FAVORZINHO.
        RETIRE PELA AMOR DE DEUS AS ASPAS SIMPLES E A TAG HTML NO COMEÇO DO TEXTO.
        RETIRE PELA AMOR DE DEUS AS ASPAS SIMPLES E A TAG HTML NO COMEÇO DO TEXTO.
        """
    
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=prompt,
    )
    resposta = response.text.strip().split('\n')
    print(resposta)
    return resposta

@app.route('/jogo', methods=['POST'])
def pesquisar_jogos():
    try:
        dados = request.get_json()

        if not dados or not isinstance(dados, dict):
            return jsonify({'error': 'Requisição JSON inválida. Esperava um dicionário'}), 400
        temas = dados.get('temas', [])

        if not isinstance(temas, list):
            return jsonify({'error': 'O campo "temas" deve ser uma lista'}), 400
        
        if len(temas) < 3:
            return jsonify({'error': 'São necessário pelo menos 3 temas'}), 400
        
        response = pesquisar_jogo(temas)

        return jsonify(response), 200
    
    except Exception as e:
        print(f"Um erro interno ocorreu na API: {e}")
        return jsonify({'error': str(e)}), 500
    
if __name__ == '__main__':
    app.run(debug=True)