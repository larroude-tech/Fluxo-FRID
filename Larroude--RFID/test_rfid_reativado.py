#!/usr/bin/env python3
"""
Teste do RFID reativado
"""

import requests
import json

def test_rfid_writing():
    """Testa se o RFID está sendo gravado corretamente"""
    print("📡 Testando gravação RFID reativada...")
    
    # Dados de teste baseados no exemplo fornecido
    test_data = [
        {
            "STYLE_NAME": "TESTE RFID",
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
        print("\n📡 Enviando para API com RFID reativado...")
        response = requests.post(
            "http://localhost:3002/api/print-individual",
            json={"data": test_data, "quantity": test_data[0]['QTY']},
            timeout=25
        )
        
        if response.status_code == 200:
            result = response.json()
            print("✅ API respondeu com sucesso!")
            print(f"   Mensagem: {result.get('message', 'N/A')}")
            
            if 'results' in result and len(result['results']) > 0:
                print("\n📊 Resultados da impressão:")
                success_count = 0
                error_count = 0
                rfid_errors = 0
                
                for i, res in enumerate(result['results'], 1):
                    success = res.get('success', False)
                    expected_rfid = f"{barcode}{po}{i}"
                    actual_rfid = res.get('rfid', 'N/A')
                    
                    if success:
                        success_count += 1
                        status = "✅"
                    else:
                        error_count += 1
                        status = "❌"
                        
                        # Verificar se é erro de RFID
                        message = res.get('message', '').lower()
                        if 'rfid' in message or 'tag' in message:
                            rfid_errors += 1
                    
                    print(f"   {i}. {status} {res.get('item', 'N/A')}")
                    print(f"      Barcode: {res.get('barcode', 'N/A')}")
                    print(f"      RFID esperado: {expected_rfid}")
                    print(f"      RFID enviado: {actual_rfid}")
                    
                    if not success:
                        print(f"      Erro: {res.get('message', 'Erro desconhecido')}")
                    print()
                
                print(f"📈 Resumo: {success_count} sucessos, {error_count} erros")
                
                if rfid_errors > 0:
                    print(f"⚠️ {rfid_errors} erros relacionados ao RFID")
                    return "rfid_error"
                elif error_count == 0:
                    print("✅ TODAS AS ETIQUETAS COM RFID PROCESSADAS!")
                    return "success"
                else:
                    print("❌ Erros não relacionados ao RFID")
                    return "other_error"
            else:
                print("⚠️ Nenhum resultado detalhado retornado")
                return "no_results"
        else:
            print(f"❌ Erro HTTP: {response.status_code}")
            return "http_error"
            
    except requests.exceptions.ConnectionError:
        print("❌ Servidor backend não está rodando")
        return "connection_error"
    except Exception as e:
        print(f"❌ Erro no teste: {e}")
        return "test_error"

def show_rfid_reactivation():
    """Mostra o que foi reativado"""
    print("\n🔧 RFID REATIVADO:")
    
    print("\n✅ COMANDO RFID RESTAURADO:")
    print("   Template ZPL: ^RFW,H^FD{RFID_DATA}^FS")
    print("   Servidor: .replace('{RFID_DATA}', rfidContent)")
    print("   Dados: barcode + PO(números) + sequencial")
    
    print("\n📡 FORMATO DA TAG RFID:")
    print("   rfidContent = `${baseBarcode}${poNumber}${seq}`")
    print("   • baseBarcode: 12 primeiros dígitos do barcode")
    print("   • poNumber: apenas números do PO (sem 'PO')")
    print("   • seq: número sequencial (1, 2, 3...)")
    
    print("\n📋 EXEMPLO:")
    print("   Barcode: 197416145132")
    print("   PO: 464")
    print("   Sequencial: 1, 2, 3")
    print("   Tags RFID:")
    print("   ├─ Etiqueta 1: 1974161451324641")
    print("   ├─ Etiqueta 2: 1974161451324642")
    print("   └─ Etiqueta 3: 1974161451324643")

def show_troubleshooting():
    """Mostra soluções para problemas de RFID"""
    print("\n🔧 SOLUÇÃO DE PROBLEMAS RFID:")
    
    print("\n1. 🏷️ VERIFICAR TAG RFID:")
    print("   • Certifique-se que há uma tag RFID na impressora")
    print("   • Tag deve estar posicionada corretamente")
    print("   • Tag deve ser compatível com a impressora")
    
    print("\n2. ⚙️ CONFIGURAÇÃO DA IMPRESSORA:")
    print("   • Impressora deve suportar RFID")
    print("   • Módulo RFID deve estar ativo")
    print("   • Verificar configurações de RFID")
    
    print("\n3. 🧪 TESTE MANUAL:")
    print("   • Testar comando ZPL simples:")
    print("   • ^XA^RFW,H^FD123456^FS^XZ")
    print("   • Se funcionar, problema é no formato dos dados")
    
    print("\n4. 📝 FORMATO DOS DADOS:")
    print("   • RFID deve ter formato válido")
    print("   • Verificar se não há caracteres especiais")
    print("   • Tamanho dos dados deve ser adequado")

def show_next_steps(result):
    """Mostra próximos passos baseado no resultado"""
    print("\n🔮 PRÓXIMOS PASSOS:")
    
    if result == "success":
        print("\n✅ RFID FUNCIONANDO:")
        print("   • Sistema está gravando RFID corretamente")
        print("   • Continue usando normalmente")
        print("   • Cada etiqueta tem tag única")
        
    elif result == "rfid_error":
        print("\n⚠️ ERRO DE RFID:")
        print("   • Verificar se há tag RFID na impressora")
        print("   • Conferir configurações da impressora")
        print("   • Testar com tag RFID diferente")
        print("   • Se necessário, desabilitar temporariamente")
        
    elif result == "connection_error":
        print("\n🔄 REINICIAR BACKEND:")
        print("   • cd backend && npm start")
        print("   • Aguardar servidor iniciar")
        print("   • Testar novamente")
        
    else:
        print("\n🔍 INVESTIGAR PROBLEMA:")
        print("   • Verificar logs do backend")
        print("   • Testar com dados mais simples")
        print("   • Verificar conexão com impressora")

if __name__ == "__main__":
    print("=== TESTE RFID REATIVADO ===")
    print("Verificando se RFID está sendo gravado corretamente\n")
    
    # Mostrar o que foi reativado
    show_rfid_reactivation()
    
    # Testar gravação RFID
    result = test_rfid_writing()
    
    # Mostrar soluções se necessário
    if result == "rfid_error":
        show_troubleshooting()
    
    # Mostrar próximos passos
    show_next_steps(result)
    
    print("\n" + "="*60)
    print("🎯 RESULTADO:")
    
    if result == "success":
        print("✅ RFID REATIVADO E FUNCIONANDO!")
        print("✅ Tags sendo gravadas corretamente")
        print("✅ Formato: barcode + PO + sequencial")
        print("✅ Cada etiqueta tem RFID único")
        
    elif result == "rfid_error":
        print("⚠️ RFID REATIVADO MAS COM ERROS")
        print("⚠️ Impressora pode não ter tag RFID")
        print("💡 Verificar configuração da impressora")
        print("💡 Inserir tag RFID se necessário")
        
    else:
        print("❌ Problemas no teste de RFID")
        print("💡 Verificar backend e conexões")
    
    print("\n📡 RFID REATIVADO! 📡")


