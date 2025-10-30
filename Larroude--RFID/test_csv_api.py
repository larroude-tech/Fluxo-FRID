#!/usr/bin/env python3
"""
Teste da API CSV via requests
"""

import requests
import json

def test_csv_api():
    """Testa endpoints da API CSV"""
    base_url = "http://localhost:3002/api/csv"
    
    print("🧪 Testando API CSV...")
    
    # 1. Testar informações
    try:
        print("\n📋 1. Testando /csv/info...")
        response = requests.get(f"{base_url}/info")
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Info obtida com sucesso:")
            print(f"   Total de etiquetas: {data['data']['totalLabels']}")
            print(f"   Impressora: {data['data']['printerName']}")
        else:
            print(f"❌ Erro na info: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Erro na conexão info: {e}")
    
    # 2. Testar listagem de etiquetas
    try:
        print("\n📋 2. Testando /csv/labels...")
        response = requests.get(f"{base_url}/labels")
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Labels obtidas com sucesso:")
            print(f"   Total: {len(data['data']['labels'])}")
            if data['data']['labels']:
                first_label = data['data']['labels'][0]
                print(f"   Primeira etiqueta: {first_label['style_name']}")
        else:
            print(f"❌ Erro nas labels: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Erro na conexão labels: {e}")
    
    # 3. Testar impressão de etiqueta individual
    try:
        print("\n🖨️ 3. Testando impressão individual...")
        
        payload = {
            "labelIndex": 1,
            "rfidData": "TESTE_API_CSV"
        }
        
        response = requests.post(
            f"{base_url}/print-label",
            headers={"Content-Type": "application/json"},
            data=json.dumps(payload)
        )
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Impressão individual bem-sucedida:")
            print(f"   Mensagem: {data['message']}")
        else:
            print(f"❌ Erro na impressão: {response.status_code}")
            print(f"   Resposta: {response.text}")
            
    except Exception as e:
        print(f"❌ Erro na impressão individual: {e}")

if __name__ == "__main__":
    print("=== Teste da API CSV ===")
    test_csv_api()
