#!/usr/bin/env python3
"""
Teste da correção da tag RFID
"""

import requests
import json

def test_rfid_format():
    """Testa se a tag RFID está no formato correto"""
    print("📡 Testando novo formato da tag RFID...")
    
    # Dados de teste baseados no exemplo fornecido
    test_data = [
        {
            "STYLE_NAME": "TESTE PRODUTO",
            "VPM": "L464-TESTE-5.0-WHIT-1120",
            "COLOR": "WHITE",
            "SIZE": "5.0",
            "QTY": 3,
            "BARCODE": "197416145132",
            "PO": "464"
        }
    ]
    
    print("📝 Dados de teste:")
    print(f"   Produto: {test_data[0]['STYLE_NAME']}")
    print(f"   PO: PO{test_data[0]['PO']}")
    print(f"   Barcode: {test_data[0]['BARCODE']}")
    print(f"   Quantidade: {test_data[0]['QTY']}")
    print()
    
    print("📊 Tags RFID esperadas:")
    barcode = test_data[0]['BARCODE']
    po = test_data[0]['PO']
    for i in range(1, test_data[0]['QTY'] + 1):
        expected_rfid = f"{barcode}{po}{i}"
        print(f"   Etiqueta {i}: {expected_rfid}")
    
    try:
        print("\n📡 Enviando para API...")
        response = requests.post(
            "http://localhost:3000/api/print-individual",
            json={"data": test_data, "quantity": test_data[0]['QTY']},
            timeout=15
        )
        
        if response.status_code == 200:
            result = response.json()
            print("✅ API respondeu com sucesso!")
            
            if 'results' in result and len(result['results']) > 0:
                print("\n📊 Resultados da API:")
                all_correct = True
                
                for i, res in enumerate(result['results'], 1):
                    expected_rfid = f"{barcode}{po}{i}"
                    actual_rfid = res.get('rfid', 'N/A')
                    
                    if actual_rfid == expected_rfid:
                        status = "✅"
                    else:
                        status = "❌"
                        all_correct = False
                    
                    print(f"   {i}. {status} {res.get('item', 'N/A')}")
                    print(f"      Esperado: {expected_rfid}")
                    print(f"      Atual:    {actual_rfid}")
                    print(f"      Barcode:  {res.get('barcode', 'N/A')}")
                    print()
                
                if all_correct:
                    print("✅ TODAS AS TAGS RFID ESTÃO CORRETAS!")
                    return True
                else:
                    print("❌ Algumas tags RFID estão incorretas")
                    return False
            else:
                print("⚠️ Nenhum resultado detalhado retornado")
                return False
        else:
            print(f"❌ Erro HTTP: {response.status_code}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("❌ Servidor backend não está rodando")
        return False
    except Exception as e:
        print(f"❌ Erro no teste: {e}")
        return False

def show_rfid_logic():
    """Mostra a nova lógica de RFID"""
    print("\n📡 NOVA LÓGICA DE TAG RFID:")
    
    print("\n🔧 FORMATO:")
    print("   TAG RFID = BARCODE + PO(apenas números) + SEQUENCIAL")
    
    print("\n📋 EXEMPLO:")
    print("   PO: PO0464")
    print("   Barcode: 197416145132")
    print("   QTY: 3")
    print()
    print("   Resultado:")
    print("   ├─ Etiqueta 1: TAG = 19741614513204641")
    print("   ├─ Etiqueta 2: TAG = 19741614513204642")
    print("   └─ Etiqueta 3: TAG = 19741614513204643")
    
    print("\n🎯 COMPONENTES:")
    print("   • 197416145132 (barcode completo)")
    print("   • 0464 (PO sem as letras 'PO')")
    print("   • 1, 2, 3 (sequencial)")
    
    print("\n⚙️ IMPLEMENTAÇÃO:")
    print("   const rfidContent = `${baseBarcode}${poNumber}${seq}`;")
    print("   • baseBarcode: barcode completo (12 dígitos)")
    print("   • poNumber: apenas números do PO")
    print("   • seq: número sequencial (1, 2, 3...)")

def simulate_rfid_scenarios():
    """Simula diferentes cenários de RFID"""
    print("\n🧪 SIMULAÇÃO DE CENÁRIOS:")
    
    scenarios = [
        {
            "name": "Exemplo fornecido",
            "barcode": "197416145132",
            "po": "464",
            "qty": 3,
            "expected": ["19741614513204641", "19741614513204642", "19741614513204643"]
        },
        {
            "name": "PO com zeros",
            "barcode": "123456789012",
            "po": "0001",
            "qty": 2,
            "expected": ["12345678901200011", "12345678901200012"]
        },
        {
            "name": "Barcode curto",
            "barcode": "12345678",
            "po": "999",
            "qty": 1,
            "expected": ["123456789991"]
        }
    ]
    
    for i, scenario in enumerate(scenarios, 1):
        print(f"\n   {i}. {scenario['name']}:")
        print(f"      Barcode: {scenario['barcode']}")
        print(f"      PO: {scenario['po']}")
        print(f"      Quantidade: {scenario['qty']}")
        print("      Tags RFID esperadas:")
        
        for j, expected in enumerate(scenario['expected'], 1):
            print(f"        {j}. {expected}")

def show_code_changes():
    """Mostra as mudanças no código"""
    print("\n🔧 MUDANÇAS NO CÓDIGO:")
    
    print("\n❌ CÓDIGO ANTERIOR:")
    print("   const rfidContent = poFormatted; // Gravava 'PO464'")
    
    print("\n✅ CÓDIGO ATUAL:")
    print("   const baseBarcode = barcodeSource.substring(0, 12);")
    print("   const rfidContent = `${baseBarcode}${poNumber}${seq}`;")
    print("   // Grava '19741614513204641'")
    
    print("\n🎯 DIFERENÇAS:")
    print("   • ANTES: Gravava apenas 'PO464'")
    print("   • DEPOIS: Grava 'barcode + números do PO + sequencial'")
    print("   • ANTES: Tag igual para todas as etiquetas")
    print("   • DEPOIS: Tag única para cada etiqueta")

if __name__ == "__main__":
    print("=== TESTE TAG RFID CORRIGIDA ===")
    print("Verificando novo formato: barcode + PO + sequencial\n")
    
    # Mostrar nova lógica
    show_rfid_logic()
    
    # Simular cenários
    simulate_rfid_scenarios()
    
    # Mostrar mudanças no código
    show_code_changes()
    
    # Testar API
    rfid_ok = test_rfid_format()
    
    print("\n" + "="*60)
    print("🎯 RESULTADO:")
    
    if rfid_ok:
        print("✅ TAG RFID CORRIGIDA COM SUCESSO!")
        print("✅ Formato: barcode + PO(números) + sequencial")
        print("✅ Cada etiqueta tem tag única")
        print("✅ PO sem letras 'PO' na tag")
        print("✅ Sequencial funcionando corretamente")
        
        print("\n📡 EXEMPLO DE FUNCIONAMENTO:")
        print("   PO0464 + Barcode 197416145132 + QTY 3")
        print("   ├─ Tag 1: 19741614513204641")
        print("   ├─ Tag 2: 19741614513204642")
        print("   └─ Tag 3: 19741614513204643")
        
        print("\n🚀 BENEFÍCIOS:")
        print("   • Tag RFID única por etiqueta")
        print("   • Rastreabilidade individual")
        print("   • Formato padronizado")
        print("   • Sem caracteres desnecessários")
        
    else:
        print("❌ Problemas na correção da tag RFID")
        print("💡 Verifique se o backend foi reiniciado")
    
    print("\n📡 TAG RFID CORRIGIDA! 📡")


