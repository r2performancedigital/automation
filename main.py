import os
import json
import time
import requests
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials

TOKEN =  os.environ["API_TOKEN_MONOPOLIO"]

headers = {
  "accept": "application/json",
  "authorization": f"Token {TOKEN}"
}

def buscar_pedidos():
  todos_pedidos = []
  
  url = "https://www.monopolioshoes.com.br/api/v1/pedidos/"
  
  while url:
    response = requests.get(url, headers=headers)
    dados = response.json()
    
    todos_pedidos.extend(dados["results"])
    
    url = dados["next"]
    print("Pedidos:", len(todos_pedidos))
    time.sleep(0.2)

return pd.DataFrame(todos_pedidos)

df = buscar_pedidos()

print(df.shape)

credenciais = json.loads(os.environ["GOOGLE_CREDENTIALS"])

scope = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

creds = Credentials.from_service_account_info(
  credenciais,
  scopes=scope
)

gc = gspread.authorize(creds)

planilha = gc.open("ATM Monopolio")

aba = planilha.sheet1

aba.clear()

aba.update(
  [df.columns.tolist()] +
  df.fillna("").astype(str).values.tolist()
)

print("Sucesso")
