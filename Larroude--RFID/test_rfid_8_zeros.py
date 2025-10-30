#!/usr/bin/env python3
"""
Teste do formato RFID com 8 zeros finais (sem caracteres especiais)
"""

import requests
import json

def test_rfid_format_8_zeros():
    """Testa o formato RFID com 8 zeros finais"""
    print("🔧 Testando formato RFID com 8 zeros finais...")
    
    # Dados de teste
    test_data = [
        {
            "STYLE_NAME": "TESTE RFID 8 ZEROS",
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
    
    print("🔧 NOVO FORMATO RFID (SEM CARACTERES ESPECIAIS):")
    print("   ANTES: barcode + PO + seq + F + 000")
    print("   AGORA: barcode + PO + seq + 8 zeros")
    print("   • Sem caracteres especiais (sem F)")
    print("   • Exatamente 8 zeros no final")
    print("   • Apenas números")
    print()
    
    # Calcular formatos esperados
    baseBarcode = test_data[0]["BARCODE"]  # 197416145132
    poNumber = test_data[0]["PO"]          # 464
    qty = test_data[0]["QTY"]              # 3
    
    expected_rfids = []
    for seq in range(1, qty + 1):
        rfid_base = f"{baseBarcode}{poNumber}{seq}"  # ex: 1974161451324641
        rfid_with_zeros = f"{rfid_base}00000000"     # ex: 197416145132464100000000
        expected_rfids.append(rfid_with_zeros)
    
    print("🎯 RFID esperados (com 8 zeros finais):")
    for i, rfid in enumerate(expected_rfids, 1):
        print(f"   {i}. {rfid} (total: {len(rfid)} caracteres)")
    print()
    
    # Verificar estrutura
    example_rfid = expected_rfids[0]
    print("🔍 ESTRUTURA DO RFID:")
    print(f"   Exemplo: {example_rfid}")
    print(f"   • Barcode: {baseBarcode} (12 chars)")
    print(f"   • PO: {poNumber} (3 chars)")
    print(f"   • Seq: 1 (1 char)")
    print(f"   • Zeros: 00000000 (8 chars)")
    print(f"   • Total: {len(example_rfid)} caracteres")
    print(f"   • Apenas números: {'✅' if example_rfid.isdigit() else '❌'}")
    print()
    
    try:
        print("📡 Enviando para API com formato 8 zeros...")
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
                format_correct = 0
                
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
                    
                    # Verificar formato
                    format_ok = (rfid == expected_rfid)
                    only_numbers = rfid.isdigit() if rfid != 'N/A' else False
                    correct_length = len(rfid) == len(expected_rfid) if rfid != 'N/A' else False
                    ends_with_zeros = rfid.endswith('00000000') if rfid != 'N/A' else False
                    
                    if format_ok:
                        format_correct += 1
                        format_status = "✅ FORMATO PERFEITO"
                    elif only_numbers and ends_with_zeros:
                        format_status = "✅ ESTRUTURA OK"
                    elif only_numbers:
                        format_status = "⚠️ APENAS NÚMEROS OK"
                    else:
                        format_status = "❌ FORMATO INCORRETO"
                    
                    print(f"   {i}. {status} {res.get('item', 'N/A')}")
                    print(f"      Barcode: {barcode}")
                    print(f"      RFID: {rfid}")
                    print(f"      Esperado: {expected_rfid}")
                    print(f"      Status: {format_status}")
                    
                    if rfid != 'N/A':
                        print(f"      Análise:")
                        print(f"        • Apenas números: {'✅' if only_numbers else '❌'}")
                        print(f"        • Termina com 8 zeros: {'✅' if ends_with_zeros else '❌'}")
                        print(f"        • Tamanho correto: {'✅' if correct_length else '❌'} ({len(rfid)} chars)")
                    
                    if not success:
                        print(f"      Erro: {res.get('message', 'Erro desconhecido')}")
                    print()
                
                print(f"📈 Resumo:")
                print(f"   • {success_count} sucessos, {error_count} erros")
                print(f"   • {format_correct}/{len(expected_rfids)} formatos RFID perfeitos")
                
                if error_count == 0 and format_correct == len(expected_rfids):
                    print("✅ FORMATO RFID COM 8 ZEROS FUNCIONANDO PERFEITAMENTE!")
                    return "success"
                elif error_count == 0:
                    print("⚠️ Impressão OK, mas formato RFID pode precisar ajuste")
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

def show_format_comparison():
    """Mostra comparação entre os formatos"""
    print("\n📊 EVOLUÇÃO DO FORMATO RFID:\n")
    
    print("🔍 FORMATO ORIGINAL:")
    print("   1974161451324641")
    print("   • 16 caracteres")
    print("   • Apenas barcode + PO + seq")
    print()
    
    print("🔍 FORMATO COM F:")
    print("   1974161451324641F000")
    print("   • 20 caracteres")
    print("   • Com caractere especial F")
    print()
    
    print("🔍 FORMATO ATUAL (8 ZEROS):")
    print("   197416145132464100000000")
    print("   • 24 caracteres")
    print("   • Apenas números (sem caracteres especiais)")
    print("   • Exatamente 8 zeros no final")
    print()
    
    print("✅ VANTAGENS DO FORMATO ATUAL:")
    print("   • Apenas números (compatibilidade RFID)")
    print("   • 8 caracteres finais para expansão")
    print("   • Sem caracteres especiais")
    print("   • Formato consistente e previsível")

def show_structure_details():
    """Mostra detalhes da estrutura"""
    print("\n🏗️ ESTRUTURA DETALHADA:\n")
    
    print("📊 COMPONENTES:")
    print("   1. Barcode: 197416145132 (12 dígitos)")
    print("   2. PO: 464 (3 dígitos, sem letras)")
    print("   3. Sequencial: 1, 2, 3... (1 dígito)")
    print("   4. Zeros finais: 00000000 (8 dígitos)")
    print()
    
    print("🔢 EXEMPLOS COMPLETOS:")
    print("   Seq 1: 197416145132 + 464 + 1 + 00000000 = 197416145132464100000000")
    print("   Seq 2: 197416145132 + 464 + 2 + 00000000 = 197416145132464200000000")
    print("   Seq 3: 197416145132 + 464 + 3 + 00000000 = 197416145132464300000000")
    print()
    
    print("✅ CARACTERÍSTICAS:")
    print("   • Total: 24 caracteres")
    print("   • Apenas números (0-9)")
    print("   • Sem caracteres especiais")
    print("   • 8 zeros reservados no final")

if __name__ == "__main__":
    print("=== TESTE FORMATO RFID COM 8 ZEROS ===")
    print("Formato: Barcode + PO + Seq + 8 zeros (apenas números)\n")
    
    # Mostrar comparação de formatos
    show_format_comparison()
    
    # Mostrar estrutura detalhada
    show_structure_details()
    
    # Testar novo formato
    result = test_rfid_format_8_zeros()
    
    print("\n" + "="*60)
    print("🎯 RESULTADO:")
    
    if result == "success":
        print("✅ FORMATO RFID COM 8 ZEROS FUNCIONANDO!")
        print("✅ Todas as etiquetas processadas corretamente")
        print("✅ Apenas números (sem caracteres especiais)")
        print("✅ Exatamente 8 zeros no final")
        
        print("\n🎊 BENEFÍCIOS:")
        print("   • Compatibilidade máxima com RFID")
        print("   • 8 caracteres reservados para expansão")
        print("   • Formato limpo (apenas números)")
        print("   • Estrutura consistente e previsível")
        
    elif result == "format_issue":
        print("⚠️ IMPRESSÃO OK, FORMATO PRECISA AJUSTE")
        print("⚠️ Verificar se tem exatamente 8 zeros finais")
        print("💡 Comparar RFID esperado vs recebido")
        
    elif result == "connection_error":
        print("❌ SERVIDOR BACKEND NÃO ESTÁ RODANDO")
        print("💡 Execute: cd backend && npm start")
        print("💡 Aguarde inicialização e teste novamente")
        
    else:
        print("❌ PROBLEMAS NO TESTE")
        print("💡 Verificar logs do backend")
        print("💡 Reiniciar servidor se necessário")
    
    print("\n🔧 FORMATO RFID 8 ZEROS IMPLEMENTADO! 🔧")


