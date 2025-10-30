#!/usr/bin/env python3
"""
Script para verificar e orientar restart do backend
"""

import requests
import subprocess
import time

def check_backend_status():
    """Verifica se o backend está rodando"""
    try:
        response = requests.get("http://localhost:3000/api/status", timeout=5)
        if response.status_code == 200:
            print("✅ Backend está rodando na porta 3000")
            return True
        else:
            print(f"⚠️ Backend respondeu com status {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Backend não está rodando na porta 3000")
        return False
    except Exception as e:
        print(f"❌ Erro ao verificar backend: {e}")
        return False

def check_backend_port_3002():
    """Verifica se o backend está rodando na porta 3002"""
    try:
        response = requests.get("http://localhost:3002/api/status", timeout=5)
        if response.status_code == 200:
            print("✅ Backend está rodando na porta 3002")
            return True
        else:
            print(f"⚠️ Backend na porta 3002 respondeu com status {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Backend não está rodando na porta 3002")
        return False
    except Exception as e:
        print(f"❌ Erro ao verificar backend na porta 3002: {e}")
        return False

def show_restart_instructions():
    """Mostra instruções para reiniciar o backend"""
    print("\n🔄 COMO REINICIAR O BACKEND:")
    print("\n1. 🛑 PARAR O SERVIDOR ATUAL:")
    print("   • Pressione Ctrl+C no terminal do backend")
    print("   • Ou feche o terminal que está rodando o servidor")
    
    print("\n2. 🚀 INICIAR O SERVIDOR:")
    print("   • Abra um novo terminal")
    print("   • cd C:\\src\\Larroud--RFID\\backend")
    print("   • npm start")
    
    print("\n3. ✅ VERIFICAR SE FUNCIONOU:")
    print("   • Aguarde a mensagem 'Servidor rodando na porta 3002'")
    print("   • Teste novamente a impressão")
    
    print("\n💡 ALTERNATIVA (PowerShell):")
    print("   cd backend")
    print("   npm start")

def test_updated_rfid():
    """Testa se o RFID foi atualizado"""
    print("\n🧪 TESTANDO RFID ATUALIZADO...")
    
    test_data = [{
        "STYLE_NAME": "TESTE",
        "VPM": "L464-TEST",
        "BARCODE": "197416145132",
        "PO": "464",
        "QTY": 1
    }]
    
    ports_to_try = [3000, 3002]
    
    for port in ports_to_try:
        try:
            print(f"\n📡 Testando porta {port}...")
            response = requests.post(
                f"http://localhost:{port}/api/print-individual",
                json={"data": test_data, "quantity": 1},
                timeout=10
            )
            
            if response.status_code == 200:
                result = response.json()
                if 'results' in result and len(result['results']) > 0:
                    rfid = result['results'][0].get('rfid', '')
                    expected = "1974161451324641"
                    
                    print(f"   RFID retornado: {rfid}")
                    print(f"   RFID esperado:  {expected}")
                    
                    if rfid == expected:
                        print("   ✅ RFID CORRETO! Backend atualizado.")
                        return True
                    elif rfid == "PO464":
                        print("   ❌ RFID antigo. Backend precisa ser reiniciado.")
                        return False
                    else:
                        print("   ⚠️ RFID diferente do esperado.")
                        return False
                else:
                    print("   ⚠️ Resposta sem resultados")
            else:
                print(f"   ❌ Erro HTTP {response.status_code}")
        except requests.exceptions.ConnectionError:
            print(f"   ❌ Porta {port} não responde")
        except Exception as e:
            print(f"   ❌ Erro: {e}")
    
    return False

if __name__ == "__main__":
    print("=== VERIFICAÇÃO E RESTART DO BACKEND ===")
    print("Checando se o backend precisa ser reiniciado\n")
    
    # Verificar status do backend
    backend_3000 = check_backend_status()
    backend_3002 = check_backend_port_3002()
    
    if not backend_3000 and not backend_3002:
        print("\n❌ NENHUM BACKEND RODANDO")
        show_restart_instructions()
    else:
        # Testar se o RFID foi atualizado
        rfid_updated = test_updated_rfid()
        
        if rfid_updated:
            print("\n✅ BACKEND ATUALIZADO E FUNCIONANDO!")
            print("✅ RFID com novo formato implementado")
            print("✅ Formato: barcode + PO + sequencial")
        else:
            print("\n❌ BACKEND PRECISA SER REINICIADO")
            print("❌ Ainda está usando código antigo")
            show_restart_instructions()
            
            print("\n🔧 APÓS REINICIAR:")
            print("   1. Execute: python test_rfid_corrigido.py")
            print("   2. Verifique se RFID está no formato correto")
            print("   3. Teste impressão no sistema web")
    
    print("\n" + "="*50)
    print("💡 LEMBRE-SE:")
    print("   • Mudanças no código backend requerem restart")
    print("   • Use Ctrl+C para parar o servidor")
    print("   • Use 'npm start' para iniciar novamente")
    print("   • Aguarde a mensagem de servidor rodando")
    
    print("\n🔄 BACKEND RESTART NECESSÁRIO! 🔄")


