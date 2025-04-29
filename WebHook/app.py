from flask import Flask, request, jsonify, render_template_string
import requests
import json
from datetime import datetime

app = Flask(__name__)

# Configurações da Evolution API
EVOLUTION_API_URL = ""
EVOLUTION_API_KEY = ""

@app.route('/', methods=['GET'])
def home():
    return """
    <html>
        <head>
            <title>Webhook para Evolution API</title>
            <style>
                body { font-family: Arial, sans-serif; margin: 40px; line-height: 1.6; }
                h1 { color: #4CAF50; }
                .container { max-width: 800px; margin: 0 auto; }
                .success { color: green; font-weight: bold; }
                code { background: #f4f4f4; padding: 2px 5px; border-radius: 3px; }
                .btn {
                    display: inline-block;
                    background-color: #4CAF50;
                    color: white;
                    padding: 12px 20px;
                    text-align: center;
                    text-decoration: none;
                    border-radius: 4px;
                    font-size: 16px;
                    margin-top: 20px;
                    cursor: pointer;
                    border: none;
                    transition: background-color 0.3s;
                }
                .btn:hover {
                    background-color: #45a049;
                }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>Evolution API Webhook Funcionando!</h1>
                <p class="success">✅ O servidor está online e pronto para receber requisições.</p>
                <h2>Como testar:</h2>
                <p>Você pode enviar uma requisição POST para <code>/webhook</code> com dados JSON contendo uma mensagem, e ela será enviada para a Evolution API.</p>
                <p>Exemplo de dados JSON:</p>
                <pre><code>{
  "number": "5531993663334",
  "message": "Olá, esta é uma mensagem de teste!"
}</code></pre>
                
                <a href="/webhook" class="btn">Acessar Webhook</a>
            </div>
        </body>
    </html>
    """

@app.route('/webhook', methods=['POST', 'GET'])
def webhook():
    if request.method == 'GET':
        return """
        <html>
            <head>
                <title>Evolution API Webhook</title>
                <style>
                    body { font-family: Arial, sans-serif; margin: 40px; line-height: 1.6; }
                    h1 { color: #2196F3; }
                    .container { max-width: 800px; margin: 0 auto; }
                    .note { background-color: #fff3cd; padding: 15px; border-radius: 5px; }
                    code { background: #f4f4f4; padding: 2px 5px; border-radius: 3px; }
                    .form-group { margin-bottom: 15px; }
                    label { display: block; margin-bottom: 5px; font-weight: bold; }
                    input, textarea { 
                        width: 100%; 
                        padding: 8px; 
                        border: 1px solid #ddd; 
                        border-radius: 4px;
                        box-sizing: border-box;
                    }
                    textarea { height: 100px; }
                    .submit-btn {
                        background-color: #2196F3;
                        color: white;
                        padding: 10px 15px;
                        border: none;
                        border-radius: 4px;
                        cursor: pointer;
                        font-size: 16px;
                    }
                    .submit-btn:hover {
                        background-color: #0b7dda;
                    }
                </style>
            </head>
            <body>
                <div class="container">
                    <h1>Evolution API Webhook</h1>
                    <div class="note">
                        <p>Esta é a rota do webhook que aceita requisições GET e POST.</p>
                        <p>Preencha o formulário abaixo para enviar uma mensagem via Evolution API:</p>
                    </div>
                    
                    <form action="/webhook" method="post" id="messageForm">
                        <div class="form-group">
                            <label for="number">Número do WhatsApp (com código do país):</label>
                            <input type="text" id="number" name="number" value="5531993663334" required>
                        </div>
                        <div class="form-group">
                            <label for="message">Mensagem:</label>
                            <textarea id="message" name="message" required>Olá, esta é uma mensagem de teste!</textarea>
                        </div>
                        <button type="button" class="submit-btn" onclick="submitForm()">Enviar Mensagem</button>
                    </form>
                    
                    <div id="result" style="margin-top: 20px;"></div>
                    
                    <script>
                    function submitForm() {
                        const number = document.getElementById('number').value;
                        const message = document.getElementById('message').value;
                        const resultDiv = document.getElementById('result');
                        
                        resultDiv.innerHTML = '<p>Enviando mensagem...</p>';
                        
                        fetch('/webhook', {
                            method: 'POST',
                            headers: {
                                'Content-Type': 'application/json',
                            },
                            body: JSON.stringify({
                                number: number,
                                message: message
                            }),
                        })
                        .then(response => response.json())
                        .then(data => {
                            if (data.status === 'recebido') {
                                resultDiv.innerHTML = '<p style="color: green;">✅ Mensagem enviada com sucesso!</p>';
                                if (data.evolution_response) {
                                    resultDiv.innerHTML += '<p>Resposta da Evolution API:</p><pre>' + JSON.stringify(data.evolution_response, null, 2) + '</pre>';
                                }
                            } else {
                                resultDiv.innerHTML = '<p style="color: red;">❌ Erro ao enviar mensagem!</p><pre>' + JSON.stringify(data, null, 2) + '</pre>';
                            }
                        })
                        .catch(error => {
                            resultDiv.innerHTML = '<p style="color: red;">❌ Erro ao enviar mensagem: ' + error + '</p>';
                        });
                        
                        return false;
                    }
                    </script>
                    
                    <p style="margin-top: 20px;">
                        <a href="/">Voltar para a página inicial</a>
                    </p>
                </div>
            </body>
        </html>
        """
    else:  # POST
        try:
            # Registra os dados recebidos em log
            webhook_data = request.json
            print("🔔 Webhook recebido:")
            print(webhook_data)
            
            # Verifica se são dados do nosso formulário ou da Evolution API
            
            # Formato do nosso formulário
            if webhook_data and isinstance(webhook_data, dict) and 'number' in webhook_data and 'message' in webhook_data:
                number = webhook_data.get('number')
                message = webhook_data.get('message')
                
                # Prepara os dados para envio para a Evolution API
                evolution_payload = {
                    "number": number,
                    "options": {
                        "delay": 1200,
                        "presence": "composing",
                        "linkPreview": False
                    },
                    "textMessage": {
                        "text": message
                    }
                }
                
                # Prepara os cabeçalhos para a requisição
                headers = {
                    "Content-Type": "application/json",
                    "apikey": EVOLUTION_API_KEY
                }
                
                # Envia para a Evolution API
                print(f"📤 Enviando para Evolution API: {json.dumps(evolution_payload)}")
                response = requests.post(
                    EVOLUTION_API_URL, 
                    headers=headers, 
                    json=evolution_payload
                )
                
                # Verifica a resposta da Evolution API
                if response.status_code in [200, 201]:
                    print("✅ Mensagem enviada com sucesso para Evolution API!")
                    response_data = response.json()
                    print("Detalhes da resposta:", response_data)
                    return jsonify({
                        "status": "recebido", 
                        "mensagem": "Mensagem enviada com sucesso", 
                        "evolution_response": response_data
                    }), 200
                else:
                    print("❌ Erro ao enviar mensagem para Evolution API!")
                    print("Status:", response.status_code)
                    print("Detalhes:", response.text)
                    return jsonify({
                        "status": "erro", 
                        "mensagem": f"Erro ao enviar para Evolution API: {response.status_code}", 
                        "detalhes": response.text
                    }), 500
            
            # Se chegou até aqui, provavelmente é o webhook sendo chamado pela Evolution API
            # Nesse caso, apenas responda com sucesso
            return jsonify({
                "status": "webhook_recebido",
                "mensagem": "Webhook processado com sucesso",
                "dados_recebidos": webhook_data
            }), 200
                
        except Exception as e:
            print(f"❌ Erro ao processar webhook: {e}")
            return jsonify({"status": "erro", "mensagem": str(e)}), 500

@app.errorhandler(404)
def page_not_found(e):
    # Registrar a URL que não foi encontrada
    print(f"Erro 404: URL não encontrada: {request.url}")
    return """
    <html>
        <head>
            <title>Página não encontrada</title>
            <style>
                body { font-family: Arial, sans-serif; margin: 40px; line-height: 1.6; text-align: center; }
                h1 { color: #f44336; }
                .container { max-width: 800px; margin: 0 auto; }
                .home-link { margin-top: 20px; }
                .home-link a { color: #2196F3; text-decoration: none; }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>Página não encontrada</h1>
                <p>A URL solicitada não existe neste servidor.</p>
                <div class="home-link">
                    <a href="/">Voltar para a página inicial</a>
                </div>
            </div>
        </body>
    </html>
    """, 404

@app.errorhandler(405)
def method_not_allowed(e):
    print(f"Erro 405: Método não permitido: {request.method} {request.url}")
    return """
    <html>
        <head>
            <title>Método não permitido</title>
            <style>
                body { font-family: Arial, sans-serif; margin: 40px; line-height: 1.6; text-align: center; }
                h1 { color: #ff9800; }
                .container { max-width: 800px; margin: 0 auto; }
                .home-link { margin-top: 20px; }
                .home-link a { color: #2196F3; text-decoration: none; }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>Método não permitido</h1>
                <p>O método da requisição não é permitido para esta URL.</p>
                <div class="home-link">
                    <a href="/">Voltar para a página inicial</a>
                </div>
            </div>
        </body>
    </html>
    """, 405

if __name__ == '__main__':
    print("Servidor iniciado! Acesse: http://127.0.0.1:5000")
    app.run(host='0.0.0.0', port=5000, debug=True) 
