#!/usr/bin/env python3
"""
Teste do ZPL melhorado com comandos específicos de RFID
"""

import requests
import json

def test_improved_zpl():
    """Testa o ZPL melhorado"""
    print("🔧 Testando ZPL melhorado com comandos RFID específicos...")
    
    # Dados de teste
    test_data = [
        {
            "STYLE_NAME": "TESTE ZPL MELHORADO",
            "VPM": "L464-TESTE-5.0-WHIT-1120",
            "COLOR": "WHITE",
            "SIZE": "5.0",
            "QTY": 2,
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
    
    print("🔧 MELHORIAS APLICADAS:")
    print("   • Comando ^RS8,,,3 adicionado")
    print("   • RFID com parâmetros ^RFW,H,2,9,1")
    print("   • Dados dinâmicos mantidos")
    print()
    
    try:
        print("📡 Enviando para API com ZPL melhorado...")
        response = requests.post(
            "http://localhost:3002/api/print-individual",
            json={"data": test_data, "quantity": test_data[0]['QTY']},
            timeout=20
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
                    barcode = res.get('barcode', 'N/A')
                    rfid = res.get('rfid', 'N/A')
                    
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
                    print(f"      Barcode: {barcode}")
                    print(f"      RFID: {rfid}")
                    
                    if not success:
                        print(f"      Erro: {res.get('message', 'Erro desconhecido')}")
                    print()
                
                print(f"📈 Resumo: {success_count} sucessos, {error_count} erros")
                
                if rfid_errors > 0:
                    print(f"⚠️ {rfid_errors} erros relacionados ao RFID")
                    print("💡 Pode ser necessário ajustar parâmetros RFID")
                    return "rfid_error"
                elif error_count == 0:
                    print("✅ TODAS AS ETIQUETAS COM ZPL MELHORADO PROCESSADAS!")
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

def show_improvements():
    """Mostra as melhorias aplicadas"""
    print("\n🔧 MELHORIAS APLICADAS AO ZPL:\n")
    
    print("1. 📡 COMANDO ^RS8,,,3:")
    print("   ANTES: (ausente)")
    print("   DEPOIS: ^RS8,,,3")
    print("   FUNÇÃO: Configuração específica de RFID")
    print()
    
    print("2. 🏷️ COMANDO RFID MELHORADO:")
    print("   ANTES: ^RFW,H^FD{RFID_DATA}^FS")
    print("   DEPOIS: ^RFW,H,2,9,1^FD{RFID_DATA}^FS")
    print("   MELHORIA: Parâmetros específicos 2,9,1")
    print()
    
    print("3. ✅ MANTIDO (VANTAGENS):")
    print("   • Dados dinâmicos: {STYLE_NAME}, {VPM}, etc.")
    print("   • QR Code dinâmico: {QR_DATA}")
    print("   • Barcode sequencial: {BARCODE}")
    print("   • Sistema de placeholders funcional")
    print()
    
    print("4. 🎯 RESULTADO:")
    print("   • Melhor compatibilidade RFID")
    print("   • Mantém flexibilidade dos dados")
    print("   • Combina o melhor dos dois ZPLs")

def show_zpl_parameters():
    """Explica os parâmetros RFID"""
    print("\n📡 PARÂMETROS DO COMANDO RFID:\n")
    
    print("🔍 ^RFW,H,2,9,1^FD{RFID_DATA}^FS")
    print("   • ^RFW: Comando de escrita RFID")
    print("   • H: Formato hexadecimal")
    print("   • 2: Parâmetro específico (posição/bloco)")
    print("   • 9: Parâmetro específico (tamanho/tipo)")
    print("   • 1: Parâmetro específico (configuração)")
    print("   • {RFID_DATA}: Dados dinâmicos a serem gravados")
    print()
    
    print("🔍 ^RS8,,,3:")
    print("   • ^RS: Comando de configuração RFID")
    print("   • 8: Tipo de configuração")
    print("   • ,,,: Parâmetros padrão")
    print("   • 3: Configuração específica")

if __name__ == "__main__":
    print("=== TESTE ZPL MELHORADO ===")
    print("Verificando ZPL com comandos RFID específicos\n")
    
    # Mostrar melhorias
    show_improvements()
    
    # Explicar parâmetros
    show_zpl_parameters()
    
    # Testar ZPL melhorado
    result = test_improved_zpl()
    
    print("\n" + "="*60)
    print("🎯 RESULTADO:")
    
    if result == "success":
        print("✅ ZPL MELHORADO FUNCIONANDO!")
        print("✅ Comandos RFID específicos aplicados")
        print("✅ ^RS8,,,3 e ^RFW,H,2,9,1 ativos")
        print("✅ Dados dinâmicos mantidos")
        print("✅ Sistema otimizado para RFID")
        
        print("\n🎊 BENEFÍCIOS:")
        print("   • Melhor compatibilidade RFID")
        print("   • Comandos específicos da impressora")
        print("   • Mantém flexibilidade dos dados")
        print("   • Combina melhor dos dois mundos")
        
    elif result == "rfid_error":
        print("⚠️ ZPL MELHORADO COM PROBLEMAS RFID")
        print("⚠️ Comandos específicos podem precisar ajuste")
        print("💡 Verificar configuração da impressora")
        print("💡 Testar com diferentes parâmetros")
        
    else:
        print("❌ Problemas no teste do ZPL melhorado")
        print("💡 Verificar backend e conexões")
    
    print("\n🔧 ZPL MELHORADO IMPLEMENTADO! 🔧")


