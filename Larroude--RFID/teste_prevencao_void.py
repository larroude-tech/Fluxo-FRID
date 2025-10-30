#!/usr/bin/env python3
"""
Teste do Sistema de Prevenção de VOID
"""

import requests
import json

def test_dangerous_command_blocked():
    """Testa se comandos perigosos são bloqueados"""
    print("🚨 TESTE: BLOQUEIO DE COMANDOS PERIGOSOS")
    print("=" * 50)
    
    # ZPL perigoso com RFID
    dangerous_zpl = """^XA
^RFW,A,U,0,11
^FD789643610064|0464|001^FS
^XZ"""
    
    try:
        print("📤 Tentando enviar ZPL PERIGOSO...")
        response = requests.post("http://localhost:3002/api/send-zpl-direct", 
                               json={"zplCommand": dangerous_zpl}, timeout=10)
        
        if response.status_code == 400:
            data = response.json()
            print("✅ BLOQUEADO CORRETAMENTE!")
            print(f"   🛡️ Erro: {data.get('error')}")
            print(f"   🚫 Comandos perigosos: {data.get('dangerousCommands')}")
            return True
        else:
            print("❌ PERIGO! Comando não foi bloqueado!")
            return False
            
    except Exception as e:
        print(f"❌ Erro: {e}")
        return False

def test_safe_command_allowed():
    """Testa se comandos seguros são permitidos"""
    print("\n✅ TESTE: COMANDOS SEGUROS PERMITIDOS")
    print("=" * 50)
    
    # ZPL seguro
    safe_zpl = """^XA
^FO50,50^A0N,30,30^FDTeste Seguro^FS
^FO50,80^BCN,60,Y,N,N
^FD123456^FS
^XZ"""
    
    try:
        print("📤 Enviando ZPL SEGURO...")
        response = requests.post("http://localhost:3002/api/send-zpl-direct", 
                               json={"zplCommand": safe_zpl}, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            print("✅ PERMITIDO CORRETAMENTE!")
            print(f"   🎯 Sucesso: {data.get('success')}")
            print(f"   📤 Método: {data.get('method')}")
            return True
        else:
            print("❌ Comando seguro foi rejeitado!")
            return False
            
    except Exception as e:
        print(f"❌ Erro: {e}")
        return False

def test_validation_with_safety():
    """Testa validação com níveis de segurança"""
    print("\n🔍 TESTE: VALIDAÇÃO COM NÍVEIS DE SEGURANÇA")
    print("=" * 50)
    
    test_cases = [
        {
            "name": "ZPL Seguro",
            "zpl": "^XA^FO50,50^A0N,30,30^FDSeguro^FS^XZ",
            "expected_safety": "SAFE"
        },
        {
            "name": "ZPL Perigoso",
            "zpl": "^XA^RFW,A,U,0,5^FDtest^FS^XZ",
            "expected_safety": "DANGEROUS"
        }
    ]
    
    for test_case in test_cases:
        print(f"\n📋 Testando: {test_case['name']}")
        
        try:
            response = requests.post("http://localhost:3002/api/validate-zpl", 
                                   json={"zplCommand": test_case['zpl']}, timeout=5)
            
            if response.status_code == 200:
                data = response.json()
                validation = data['validation']
                
                print(f"   🛡️ Nível: {validation.get('safetyLevel')}")
                print(f"   ⚠️ Risco VOID: {validation.get('voidRisk')}")
                print(f"   ✅ Válido: {validation.get('isValid')}")
                
                if validation.get('dangerousCommands'):
                    print(f"   🚫 Perigosos: {validation.get('dangerousCommands')}")
                    
            else:
                print(f"   ❌ Erro HTTP {response.status_code}")
                
        except Exception as e:
            print(f"   ❌ Erro: {e}")

def test_safe_examples():
    """Testa os novos exemplos seguros"""
    print("\n📋 TESTE: EXEMPLOS SEGUROS")
    print("=" * 50)
    
    try:
        response = requests.get("http://localhost:3002/api/zpl-examples", timeout=5)
        
        if response.status_code == 200:
            data = response.json()
            examples = data['examples']
            
            print(f"✅ {len(examples)} exemplos carregados:")
            
            for key, example in examples.items():
                safety = example.get('safety', 'UNKNOWN')
                safety_icon = '✅' if safety == 'SAFE' else '🚨' if safety == 'EMERGENCY' else '❓'
                
                print(f"   {safety_icon} {example['name']}")
                print(f"      {example['description']}")
                
            return True
        else:
            print(f"❌ Erro HTTP {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Erro: {e}")
        return False

def main():
    """Executa todos os testes de prevenção"""
    print("🛡️ TESTE SISTEMA DE PREVENÇÃO DE VOID")
    print("GARANTINDO QUE NUNCA MAIS HAVERÁ VOID!")
    print("=" * 50)
    
    results = []
    
    # 1. Testar bloqueio de comandos perigosos
    results.append(test_dangerous_command_blocked())
    
    # 2. Testar permissão de comandos seguros
    results.append(test_safe_command_allowed())
    
    # 3. Testar validação com segurança
    test_validation_with_safety()
    
    # 4. Testar exemplos seguros
    results.append(test_safe_examples())
    
    print(f"\n🏁 RESULTADO FINAL:")
    success_count = sum(results)
    total_count = len(results)
    
    if success_count == total_count:
        print("✅ SISTEMA DE PREVENÇÃO FUNCIONANDO!")
        print("🛡️ Comandos perigosos são BLOQUEADOS")
        print("✅ Comandos seguros são PERMITIDOS")
        print("🚫 ZERO risco de VOID!")
    else:
        print(f"⚠️ {success_count}/{total_count} testes passaram")
        print("🔧 Verificar implementação")
    
    print(f"\n📋 COMANDOS SEGUROS PARA USAR:")
    print("   • Texto: ^FO, ^FD, ^FS, ^A0")
    print("   • Código de barras: ^BC, ^BY")
    print("   • QR Code: ^BQ")
    print("   • Layout: ^XA, ^XZ, ^CI")
    
    print(f"\n🚫 COMANDOS BLOQUEADOS:")
    print("   • ^RFW (Write RFID)")
    print("   • ^RFR (Read RFID)")
    print("   • ^RFI, ^RFT, ^RFU (RFID Info/Test)")
    
    print(f"\n🌐 INTERFACE SEGURA:")
    print("   http://localhost:3002/zpl-tester")
    print("   • Apenas exemplos seguros")
    print("   • Validação automática")
    print("   • Bloqueio de comandos perigosos")

if __name__ == "__main__":
    main()
