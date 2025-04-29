import requests
import json


api_url = ""  
api_key = ""


payload = {
    "number": "** * ********",  
    "options": {
        "delay": 1200,  
        "presence": "composing",  
        "linkPreview": False
    },
    "textMessage": {
        "text": (
            "Mensagem pretendida"


        )
    }
}


headers = {
    "Content-Type": "application/json",
    "apikey": api_key  
}


response = requests.post(api_url, headers=headers, json=payload)


if response.status_code in [200, 201]:  # Tratar 200 e 201 como sucesso
    print("✅ Mensagem enviada com sucesso!")
    response_data = response.json()
    print("Detalhes da resposta:", response_data)
else:
    print("❌ Erro ao enviar mensagem!")
    print("Status:", response.status_code)
    print("Detalhes:", response.text)
