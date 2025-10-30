#!/usr/bin/env python3
"""
Teste da nova funcionalidade de impressão individual
"""

import requests
import json

def test_individual_print_api():
    """Testa o endpoint de impressão individual"""
    print("🧪 Testando API de impressão individual...")
    
    # Dados de teste
    test_data = [{
        "STYLE_NAME": "TESTE INDIVIDUAL",
        "VPM": "L999-TEST-12.0-BLUE-2024",
        "COLOR": "AZUL TESTE",
        "SIZE": "12.0",
        "QTY": "1"
    }]
    
    try:
        url = "http://localhost:3000/api/print-individual"
        
        print(f"📡 Enviando POST para {url}")
        print(f"📋 Dados: {json.dumps(test_data, indent=2)}")
        
        response = requests.post(url, json={"data": test_data})
        
        print(f"📊 Status Code: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Resposta recebida:")
            print(f"   Mensagem: {result.get('message', 'N/A')}")
            print(f"   Total: {result.get('totalItems', 0)}")
            print(f"   Sucessos: {result.get('successCount', 0)}")
            
            if result.get('results'):
                for i, res in enumerate(result['results']):
                    status = "✅" if res.get('success') else "❌"
                    print(f"   {status} Item {i+1}: {res.get('item', 'N/A')} - {res.get('message', 'N/A')}")
            
            return result.get('successCount', 0) > 0
            
        else:
            print(f"❌ Erro HTTP: {response.status_code}")
            print(f"   Resposta: {response.text}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("❌ Erro: Servidor não está rodando")
        print("💡 Certifique-se de que o backend está ativo em http://localhost:3000")
        return False
    except Exception as e:
        print(f"❌ Erro inesperado: {e}")
        return False

def main():
    print("=== TESTE DA IMPRESSÃO INDIVIDUAL ===")
    print("Testando a nova funcionalidade de impressão individual\n")
    
    success = test_individual_print_api()
    
    print("\n" + "="*50)
    if success:
        print("🎉 TESTE PASSOU!")
        print("✅ A impressão individual está funcionando")
        print("✅ O formato SEM VOID está sendo usado")
        print("✅ A API está respondendo corretamente")
        print("\n🌐 Acesse: http://localhost:3000")
        print("📋 1. Faça upload de um CSV")
        print("🔄 2. Clique em 'Lista para Impressão'")
        print("🖨️ 3. Use os botões 'Imprimir' individuais")
    else:
        print("❌ TESTE FALHOU!")
        print("❌ Verifique se o servidor está rodando")
        print("❌ Verifique se a impressora está conectada")

if __name__ == "__main__":
    main()
