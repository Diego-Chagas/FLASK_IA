from flask import Flask, render_template, request
from flask import Flask, render_template
import requests, os, uuid, json
from dotenv import load_dotenv
load_dotenv()



app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/', methods=['POST'])
def index_post():
    # Valores de formulários sendo realizados
    original_text = request.form['text']
    target_language = request.form['language']

    # Vai carregar valores de: .env
    key = os.environ['KEY']
    endpoint = os.environ['ENDPOINT']
    location = os.environ['LOCATION']

    # Indica oque podemos traduzir na API version (3.0) and the target language
    path = '/translate?api-version=3.0'
    # Adiciona o parâmetro de idioma de destino
    target_language_parameter = '&to=' + target_language
    # Cria a URL por inteira
    constructed_url = endpoint + path + target_language_parameter

    #Configura as informações do cabeçalho,onde incluem a chave de assinatura
    headers = {
        'Ocp-Apim-Subscription-Key': key,
        'Ocp-Apim-Subscription-Region': location,
        'Content-type': 'application/json',
        'X-ClientTraceId': str(uuid.uuid4())
    }

    # Cria o corpo da solicitação com o texto a ser traduzido
    body = [{ 'text': original_text }]

    # Faz a ligação usando o post
    translator_request = requests.post(constructed_url, headers=headers, json=body)
    #Recupera a resposta JSON
    translator_response = translator_request.json()
    # Recupera a tradução
    translated_text = translator_response[0]['translations'][0]['text']

    # Chama o modelo de renderização, passando o texto traduzido,
    # Texto original e idioma de chegada para o modelo
    return render_template(
        'results.html',
        translated_text=translated_text,
        original_text=original_text,
        target_language=target_language
    )

