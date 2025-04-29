import requests
import json

# URL do webhook
url = "http://127.0.0.1:5000/webhook"

# IMPORTANTE: Número do chip de teste
NUMERO_WHATSAPP = "** * ********"  # Número do chip de teste

# Dados para enviar
payload = {
    "number": NUMERO_WHATSAPP,
    "message": "Olá, este é um teste do webhook integrado com a Evolution API!"
}

# Cabeçalhos
headers = {
    "Content-Type": "application/json"
}

# Envia a requisição POST
print(f"Enviando mensagem para o número: {NUMERO_WHATSAPP}")
print("Enviando dados para o webhook...")
try:
    response = requests.post(url, data=json.dumps(payload), headers=headers)
    
    # Verifica a resposta
    if response.status_code == 200:
        print("✅ Sucesso! O webhook respondeu com:")
        response_data = response.json()
        print("Status:", response_data.get("status"))
        print("Mensagem:", response_data.get("mensagem"))
        
        # Exibe detalhes da resposta da Evolution API, se disponível
        if "evolution_response" in response_data:
            print("\nDetalhes da resposta da Evolution API:")
            print(json.dumps(response_data["evolution_response"], indent=2))
    else:
        print(f"❌ Erro! Status code: {response.status_code}")
        print(response.text)
except Exception as e:
    print(f"❌ Erro ao enviar a requisição: {e}")

input("Pressione Enter para sair...") 
