#!/usr/bin/env python3
"""
Teste do novo formato RFID com F no final e zeros
"""

import requests
import json

def test_rfid_format_with_f():
    """Testa o novo formato RFID com F + zeros"""
    print("🔧 Testando novo formato RFID com F + zeros...")
    
    # Dados de teste
    test_data = [
        {
            "STYLE_NAME": "TESTE RFID F+ZEROS",
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
    
    print("🔧 NOVO FORMATO RFID:")
    print("   ANTES: barcode + PO + seq (ex: 1974161451324641)")
    print("   AGORA: barcode + PO + seq + F + 000 (ex: 1974161451324641F000)")
    print("   • F no final para identificação")
    print("   • 000 (zeros) para preenchimento/verificação")
    print()
    
    # Calcular formatos esperados
    baseBarcode = test_data[0]["BARCODE"]  # 197416145132
    poNumber = test_data[0]["PO"]          # 464
    qty = test_data[0]["QTY"]              # 3
    
    expected_rfids = []
    for seq in range(1, qty + 1):
        rfid_base = f"{baseBarcode}{poNumber}{seq}"  # ex: 1974161451324641
        rfid_with_f = f"{rfid_base}F000"             # ex: 1974161451324641F000
        expected_rfids.append(rfid_with_f)
    
    print("🎯 RFID esperados:")
    for i, rfid in enumerate(expected_rfids, 1):
        print(f"   {i}. {rfid}")
    print()
    
    try:
        print("📡 Enviando para API com novo formato RFID...")
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
                rfid_format_correct = 0
                
                for i, res in enumerate(result['results'], 1):
                    success = res.get('success', False)
                    barcode = res.get('barcode', 'N/A')
                    rfid = res.get('rfid', 'N/A')
                    expected_rfid = expected_rfids[i-1] if i <= len(expected_rfids) else 'N/A'
                    
                    if success:
                        success_count += 1
                        status = "✅"
                    else:
                        error_count += 1
                        status = "❌"
                    
                    # Verificar se o formato está correto
                    if rfid == expected_rfid:
                        rfid_format_correct += 1
                        format_status = "✅ FORMATO OK"
                    else:
                        format_status = "⚠️ FORMATO DIFERENTE"
                    
                    print(f"   {i}. {status} {res.get('item', 'N/A')}")
                    print(f"      Barcode: {barcode}")
                    print(f"      RFID: {rfid}")
                    print(f"      Esperado: {expected_rfid}")
                    print(f"      Status: {format_status}")
                    
                    if not success:
                        print(f"      Erro: {res.get('message', 'Erro desconhecido')}")
                    print()
                
                print(f"📈 Resumo:")
                print(f"   • {success_count} sucessos, {error_count} erros")
                print(f"   • {rfid_format_correct}/{len(expected_rfids)} formatos RFID corretos")
                
                if error_count == 0 and rfid_format_correct == len(expected_rfids):
                    print("✅ NOVO FORMATO RFID FUNCIONANDO PERFEITAMENTE!")
                    return "success"
                elif error_count == 0:
                    print("⚠️ Impressão OK, mas formato RFID pode estar diferente")
                    return "format_issue"
                else:
                    print("❌ Erros na impressão")
                    return "print_error"
            else:
                print("⚠️ Nenhum resultado detalhado retornado")
                return "no_results"
        else:
            print(f"❌ Erro HTTP: {response.status_code}")
            try:
                error_data = response.json()
                print(f"   Detalhes: {error_data}")
            except:
                print(f"   Resposta: {response.text}")
            return "http_error"
            
    except requests.exceptions.ConnectionError:
        print("❌ Servidor backend não está rodando")
        print("💡 Execute: cd backend && npm start")
        return "connection_error"
    except Exception as e:
        print(f"❌ Erro no teste: {e}")
        return "test_error"

def show_format_explanation():
    """Explica o novo formato RFID"""
    print("\n🔍 EXPLICAÇÃO DO NOVO FORMATO RFID:\n")
    
    print("📊 COMPONENTES:")
    print("   • Barcode: 197416145132 (12 dígitos)")
    print("   • PO: 464 (sem letras)")
    print("   • Sequencial: 1, 2, 3, ...")
    print("   • F: Identificador fixo")
    print("   • 000: Zeros para verificação/preenchimento")
    print()
    
    print("🔧 EXEMPLOS:")
    print("   Seq 1: 197416145132 + 464 + 1 + F + 000 = 1974161451324641F000")
    print("   Seq 2: 197416145132 + 464 + 2 + F + 000 = 1974161451324642F000")
    print("   Seq 3: 197416145132 + 464 + 3 + F + 000 = 1974161451324643F000")
    print()
    
    print("💡 BENEFÍCIOS:")
    print("   • F: Identificador único da Larroudé")
    print("   • 000: Espaço para códigos de verificação")
    print("   • Formato consistente e rastreável")
    print("   • Compatibilidade com sistema RFID")

def show_comparison():
    """Mostra comparação entre formatos"""
    print("\n📊 COMPARAÇÃO DE FORMATOS:\n")
    
    print("🔍 FORMATO ANTERIOR:")
    print("   1974161451324641")
    print("   • 12 dígitos barcode")
    print("   • 3 dígitos PO")
    print("   • 1 dígito sequencial")
    print("   • Total: 16 caracteres")
    print()
    
    print("🔍 FORMATO ATUAL:")
    print("   1974161451324641F000")
    print("   • 12 dígitos barcode")
    print("   • 3 dígitos PO")
    print("   • 1 dígito sequencial")
    print("   • 1 caractere F")
    print("   • 3 dígitos zeros")
    print("   • Total: 20 caracteres")
    print()
    
    print("✅ VANTAGENS DO NOVO FORMATO:")
    print("   • Identificação única com F")
    print("   • Espaço para expansão (000)")
    print("   • Melhor rastreabilidade")
    print("   • Compatibilidade RFID aprimorada")

if __name__ == "__main__":
    print("=== TESTE NOVO FORMATO RFID ===")
    print("Formato: Barcode + PO + Seq + F + 000\n")
    
    # Mostrar explicação do formato
    show_format_explanation()
    
    # Mostrar comparação
    show_comparison()
    
    # Testar novo formato
    result = test_rfid_format_with_f()
    
    print("\n" + "="*60)
    print("🎯 RESULTADO:")
    
    if result == "success":
        print("✅ NOVO FORMATO RFID COM F+000 FUNCIONANDO!")
        print("✅ Todas as etiquetas processadas corretamente")
        print("✅ Formato RFID conforme especificado")
        print("✅ F no final + zeros implementados")
        
        print("\n🎊 BENEFÍCIOS:")
        print("   • Identificação única da Larroudé (F)")
        print("   • Espaço para códigos de verificação (000)")
        print("   • Formato consistente e rastreável")
        print("   • Melhor compatibilidade RFID")
        
    elif result == "format_issue":
        print("⚠️ IMPRESSÃO OK, FORMATO RFID PODE ESTAR DIFERENTE")
        print("⚠️ Verificar se F+000 estão sendo adicionados")
        print("💡 Comparar RFID esperado vs recebido")
        
    elif result == "connection_error":
        print("❌ SERVIDOR BACKEND NÃO ESTÁ RODANDO")
        print("💡 Execute: cd backend && npm start")
        print("💡 Aguarde inicialização e teste novamente")
        
    else:
        print("❌ PROBLEMAS NO TESTE DO NOVO FORMATO")
        print("💡 Verificar logs do backend")
        print("💡 Testar conexões e configurações")
    
    print("\n🔧 NOVO FORMATO RFID IMPLEMENTADO! 🔧")


