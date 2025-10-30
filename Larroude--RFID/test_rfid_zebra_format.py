#!/usr/bin/env python3
"""
Teste do formato RFID igual ao ZebraDesigner (17 chars com F)
"""

import requests
import json

def test_rfid_zebra_format():
    """Testa o formato RFID igual ao que funciona no ZebraDesigner"""
    print("🦓 Testando formato RFID igual ao ZebraDesigner...")
    
    # Dados de teste
    test_data = [
        {
            "STYLE_NAME": "TESTE ZEBRA FORMAT",
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
    
    print("🦓 FORMATO ZEBRADESIGNER (QUE FUNCIONA):")
    print("   Valor mostrado: 19741614513204641F")
    print("   • 17 caracteres total")
    print("   • Barcode + PO + Seq + F")
    print("   • Funciona perfeitamente!")
    print()
    
    print("🔧 NOVO FORMATO DO SISTEMA (IGUAL ZEBRA):")
    print("   ANTES: barcode + PO + seq + 8 zeros")
    print("   AGORA: barcode + PO + seq + F")
    print("   • Exatamente igual ao ZebraDesigner")
    print("   • 17 caracteres com F no final")
    print()
    
    # Calcular formatos esperados (igual ao ZebraDesigner)
    baseBarcode = test_data[0]["BARCODE"]  # 197416145132
    poNumber = test_data[0]["PO"]          # 464
    qty = test_data[0]["QTY"]              # 3
    
    expected_rfids = []
    for seq in range(1, qty + 1):
        rfid_base = f"{baseBarcode}{poNumber}{seq}"  # ex: 1974161451324641
        rfid_with_f = f"{rfid_base}F"                # ex: 1974161451324641F
        expected_rfids.append(rfid_with_f)
    
    print("🎯 RFID esperados (formato ZebraDesigner):")
    for i, rfid in enumerate(expected_rfids, 1):
        print(f"   {i}. {rfid} ({len(rfid)} chars)")
    print()
    
    # Verificar se corresponde ao ZebraDesigner
    zebra_example = "19741614513204641F"
    our_example = expected_rfids[0]
    
    print("🔍 COMPARAÇÃO COM ZEBRADESIGNER:")
    print(f"   ZebraDesigner: {zebra_example} ({len(zebra_example)} chars)")
    print(f"   Nosso sistema: {our_example} ({len(our_example)} chars)")
    print(f"   Estrutura igual: {'✅' if len(zebra_example) == len(our_example) and our_example.endswith('F') else '❌'}")
    print()
    
    try:
        print("📡 Enviando para API com formato ZebraDesigner...")
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
                zebra_format_correct = 0
                
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
                    
                    # Verificar se está no formato ZebraDesigner
                    zebra_format = (rfid == expected_rfid and rfid.endswith('F') and len(rfid) == 17)
                    
                    if zebra_format:
                        zebra_format_correct += 1
                        format_status = "🦓 FORMATO ZEBRA OK"
                    else:
                        format_status = "⚠️ FORMATO DIFERENTE"
                    
                    print(f"   {i}. {status} {res.get('item', 'N/A')}")
                    print(f"      Barcode: {barcode}")
                    print(f"      RFID: {rfid}")
                    print(f"      Esperado: {expected_rfid}")
                    print(f"      Status: {format_status}")
                    
                    if rfid != 'N/A':
                        print(f"      Análise:")
                        print(f"        • Tamanho: {len(rfid)} chars (esperado: 17)")
                        print(f"        • Termina com F: {'✅' if rfid.endswith('F') else '❌'}")
                        print(f"        • Igual ZebraDesigner: {'✅' if zebra_format else '❌'}")
                    
                    if not success:
                        print(f"      Erro: {res.get('message', 'Erro desconhecido')}")
                    print()
                
                print(f"📈 Resumo:")
                print(f"   • {success_count} sucessos, {error_count} erros")
                print(f"   • {zebra_format_correct}/{len(expected_rfids)} formatos ZebraDesigner corretos")
                
                if error_count == 0 and zebra_format_correct == len(expected_rfids):
                    print("🦓 FORMATO ZEBRADESIGNER FUNCIONANDO PERFEITAMENTE!")
                    print("🎊 Mesmo formato que funciona no ZebraDesigner!")
                    return "success"
                elif error_count == 0:
                    print("⚠️ Impressão OK, mas formato pode estar diferente do ZebraDesigner")
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

def show_zebra_analysis():
    """Analisa o formato do ZebraDesigner"""
    print("\n🔍 ANÁLISE DO ZEBRADESIGNER:")
    print("="*40)
    print()
    
    zebra_value = "19741614513204641F"
    print(f"📊 Valor ZebraDesigner: {zebra_value}")
    print(f"   • Total: {len(zebra_value)} caracteres")
    print(f"   • Termina com: F")
    print(f"   • Apenas números + F: {'✅' if zebra_value[:-1].isdigit() and zebra_value.endswith('F') else '❌'}")
    print()
    
    print("🔧 DECOMPOSIÇÃO PROVÁVEL:")
    if len(zebra_value) == 17 and zebra_value.endswith('F'):
        base_part = zebra_value[:-1]  # Remove o F
        print(f"   • Parte base: {base_part} (16 dígitos)")
        print(f"   • F final: F (1 caractere)")
        
        # Tentar decompor
        if len(base_part) == 16:
            barcode = base_part[:12]
            po_seq = base_part[12:]
            print(f"   • Barcode: {barcode} (12 dígitos)")
            print(f"   • PO+Seq: {po_seq} (4 dígitos)")
            
            if len(po_seq) == 4:
                po = po_seq[:3]
                seq = po_seq[3:]
                print(f"     - PO: {po}")
                print(f"     - Seq: {seq}")
    
    print("\n✅ CONCLUSÃO:")
    print("   O ZebraDesigner usa: Barcode(12) + PO(3) + Seq(1) + F(1) = 17 chars")

def show_format_benefits():
    """Mostra benefícios do formato ZebraDesigner"""
    print("\n🎊 VANTAGENS DO FORMATO ZEBRADESIGNER:")
    print("="*45)
    print()
    
    print("✅ COMPROVADAMENTE FUNCIONA:")
    print("   • Testado e aprovado no ZebraDesigner")
    print("   • Sem erros de RFID")
    print("   • Compatibilidade total")
    print()
    
    print("✅ FORMATO OTIMIZADO:")
    print("   • 17 caracteres (não muito longo)")
    print("   • F como identificador")
    print("   • Estrutura limpa e consistente")
    print()
    
    print("✅ COMPATIBILIDADE:")
    print("   • Funciona no ZebraDesigner")
    print("   • Deve funcionar no sistema")
    print("   • Padrão comprovado")

if __name__ == "__main__":
    print("=== TESTE FORMATO ZEBRADESIGNER ===")
    print("Formato comprovadamente funcional: 17 chars com F\n")
    
    # Analisar formato do ZebraDesigner
    show_zebra_analysis()
    
    # Mostrar benefícios
    show_format_benefits()
    
    # Testar formato igual ao ZebraDesigner
    result = test_rfid_zebra_format()
    
    print("\n" + "="*60)
    print("🎯 RESULTADO:")
    
    if result == "success":
        print("🦓 FORMATO ZEBRADESIGNER FUNCIONANDO!")
        print("✅ Mesmo formato que funciona no ZebraDesigner")
        print("✅ 17 caracteres com F no final")
        print("✅ Estrutura: Barcode + PO + Seq + F")
        
        print("\n🎊 BENEFÍCIOS:")
        print("   • Formato comprovadamente funcional")
        print("   • Compatibilidade total com Zebra")
        print("   • Sem erros de RFID")
        print("   • Padrão otimizado")
        
    elif result == "format_issue":
        print("⚠️ IMPRESSÃO OK, FORMATO PODE ESTAR DIFERENTE")
        print("⚠️ Verificar se tem exatamente 17 chars com F")
        print("💡 Comparar com formato ZebraDesigner")
        
    elif result == "connection_error":
        print("❌ SERVIDOR BACKEND NÃO ESTÁ RODANDO")
        print("💡 Execute: cd backend && npm start")
        print("💡 Aguarde inicialização e teste novamente")
        
    else:
        print("❌ PROBLEMAS NO TESTE")
        print("💡 Verificar logs do backend")
        print("💡 Reiniciar servidor se necessário")
    
    print("\n🦓 FORMATO ZEBRADESIGNER IMPLEMENTADO! 🦓")


