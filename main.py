import requests
import sqlite3
from datetime import datetime


API_KEY = '27567e51'


url = f'https://api.hgbrasil.com/finance?format=json&key={API_KEY}'

try:
    
    response = requests.get(url)
    response.raise_for_status() 

    data = response.json()

    if 'results' in data:
        
        dolar = data['results']['currencies']['USD']['buy']
        euro = data['results']['currencies']['EUR']['buy']
        data_atual = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        print(f"Dólar: {dolar} | Euro: {euro} | Data: {data_atual}")

        
        conn = sqlite3.connect('bdcotacoes.db')
        cursor = conn.cursor()

    
        
        cursor.execute('''
            INSERT INTO moedas (data, dolar, euro) VALUES (?, ?, ?)
        ''', (data_atual, dolar, euro))

        
        conn.commit()
        conn.close()

        print("Dados salvos no banco com sucesso!")

    else:
        print("Erro ao obter dados da API:", data)

except requests.RequestException as e:
    print("Erro na conexão com a API:", e)

except sqlite3.Error as e:
    print("💾 Erro no banco de dados:", e)