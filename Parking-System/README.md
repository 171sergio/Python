# 🚗 Sistema de Controle de Estacionamento

Este é um sistema web simples para controle de entrada e saída de veículos em um estacionamento, desenvolvido com **Django**.

## ✅ Funcionalidades

- Registrar entrada de veículos
- Listar veículos atualmente estacionados
- Registrar saída de veículos
- Exibir extrato da saída com:
  - Horário de entrada
  - Horário de saída
  - Tempo total (horas e minutos)
  - Valor a ser pago
- Dashboard com indicadores:
  - Total de veículos com saída registrada
  - Total de veículos atualmente estacionados
  - Total arrecadado
  - Média de tempo de permanência

## 💰 Regras de Cobrança

- **Até 10 minutos:** Grátis
- **Até 1 hora:** R$ 5,00
- **A partir da 2ª hora:** R$ 2,00 por hora adicional

> ⚠️ O tempo é **arredondado para a próxima hora cheia** caso haja qualquer fração.
>
> **Exemplos:**
>
> - 1h 02min → 2 horas → R$ 7,00  
> - 2h 59min → 3 horas → R$ 9,00  
> - 10 minutos ou menos → Grátis

## 🛠️ Tecnologias Utilizadas

- Python 3
- Django 4
- SQLite (como banco de dados padrão)
- Bootstrap 5 (estilização)

## 📁 Estrutura de Pastas

estacionamento/ ├── estacionamento/ # Configurações do projeto Django ├── controle/ # Aplicação principal │ ├── templates/ │ │ ├── index.html │ │ ├── entrada.html │ │ ├── home.html │ │ ├── saida.html │ │ └── dashboard.html │ ├── models.py │ ├── views.py │ └── urls.py └── db.sqlite3 # Banco de dados padrão

## ▶️ Como Executar o Projeto

1. Clone o repositório

```bash
git clone https://github.com/171sergio/Parking-System.git
cd Parking-System

2. Crie e ative um ambiente virtual

WINDOWS:
python -m venv venv
venv\Scripts\activate
LINUX/Mac:
python3 -m venv venv
source venv/bin/activate

3. Instale as dependências

pip install django

4. Aplique as migraçõos do banco de dados

python manage.py makemigrations
python manage.py migrate

5. Inicie o servidor de desenvolvimento

python manage.py runserver

6. Acesse no navegador

http://127.0.0.1:8000/

