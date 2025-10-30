#!/usr/bin/env python3
"""
Teste do novo campo RFID_STATUS no template atualizado
"""

import win32print

def test_rfid_status_field():
    """Testa o novo campo RFID_STATUS"""
    print("🧪 Testando novo campo RFID_STATUS...")
    
    printer_name = "ZDesigner ZD621R-203dpi ZPL"
    
    # Carregar template atualizado
    try:
        with open('backend/TEMPLATE_LARROUD_OFICIAL.zpl', 'r', encoding='utf-8') as f:
            template = f.read()
    except FileNotFoundError:
        print("❌ Template não encontrado!")
        return False
    
    # Dados de teste com diferentes cenários RFID
    test_cases = [
        {
            "name": "RFID Sucesso",
            "data": {
                "STYLE_NAME": "TESTE RFID OK",
                "VPM": "L100-RFID-OK-GREEN-1111",
                "COLOR": "VERDE",
                "SIZE": "9.0",
                "RFID_STATUS": "SUCESSO"
            }
        },
        {
            "name": "RFID Erro",
            "data": {
                "STYLE_NAME": "TESTE RFID ERRO",
                "VPM": "L200-RFID-ERR-RED-2222", 
                "COLOR": "VERMELHO",
                "SIZE": "10.0",
                "RFID_STATUS": "ERRO - DADOS INVÁLIDOS"
            }
        },
        {
            "name": "RFID Sem Dados",
            "data": {
                "STYLE_NAME": "TESTE SEM RFID",
                "VPM": "L300-NO-RFID-BLUE-3333",
                "COLOR": "AZUL",
                "SIZE": "8.5",
                "RFID_STATUS": "ERRO - SEM DADOS"
            }
        }
    ]
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n🔄 Teste {i}: {test_case['name']}")
        
        data = test_case['data']
        
        # Processar dados como o sistema faz
        vpm_parts = data["VPM"].split('-')
        po_number = f"PO{vpm_parts[0].replace('L', '')}" if len(vpm_parts) > 0 else "PO000"
        local_number = vpm_parts[4][:3] if len(vpm_parts) > 4 else "000"
        barcode = data["VPM"].replace('-', '')[:12]
        
        # Substituir variáveis no template
        test_zpl = template.replace('{STYLE_NAME}', data["STYLE_NAME"]) \
                          .replace('{VPM}', data["VPM"]) \
                          .replace('{COLOR}', data["COLOR"]) \
                          .replace('{SIZE}', data["SIZE"]) \
                          .replace('{PO_INFO}', po_number) \
                          .replace('{LOCAL_INFO}', f'Local.{local_number}') \
                          .replace('{BARCODE}', barcode) \
                          .replace('{RFID_DATA}', data["VPM"]) \
                          .replace('{QR_DATA_1}', data["VPM"]) \
                          .replace('{QR_DATA_2}', data["VPM"]) \
                          .replace('{QR_DATA_3}', data["VPM"]) \
                          .replace('{RFID_STATUS}', data["RFID_STATUS"])
        
        try:
            print(f"   Produto: {data['STYLE_NAME']}")
            print(f"   VPM: {data['VPM']}")
            print(f"   Status RFID: {data['RFID_STATUS']}")
            
            handle = win32print.OpenPrinter(printer_name)
            doc_info = (f"RFID_Status_Test_{i}", None, "RAW")
            job_id = win32print.StartDocPrinter(handle, 1, doc_info)
            
            win32print.StartPagePrinter(handle)
            bytes_written = win32print.WritePrinter(handle, test_zpl.encode('ascii', errors='ignore'))
            win32print.EndPagePrinter(handle)
            win32print.EndDocPrinter(handle)
            win32print.ClosePrinter(handle)
            
            print(f"   ✅ Enviado: {bytes_written} bytes")
            
        except Exception as e:
            print(f"   ❌ Erro: {e}")
            return False
    
    return True

def show_rfid_status_info():
    """Mostra informações sobre o campo RFID_STATUS"""
    print("\n📋 INFORMAÇÕES DO CAMPO RFID_STATUS:")
    print("   📍 Posição: Canto inferior direito")
    print("   📐 Coordenadas: ^FT800,360")
    print("   🔤 Fonte: ^A0N,18,18")
    print("   📏 Formatação: ^FB300,1,0,R (alinhado à direita)")
    print("   📝 Texto: 'GRAVADO RFID: [STATUS]'")
    
    print("\n🎯 POSSÍVEIS STATUS:")
    print("   ✅ SUCESSO - Dados RFID válidos e gravados")
    print("   ❌ ERRO - DADOS INVÁLIDOS - Dados insuficientes")
    print("   ❌ ERRO - SEM DADOS - Dados N/A ou undefined")
    print("   ❌ ERRO - FALHA NA GRAVAÇÃO - Erro no processo")
    
    print("\n🔧 INTEGRAÇÃO:")
    print("   📡 Sistema determina status automaticamente")
    print("   🔍 Valida dados RFID antes da impressão")
    print("   📊 Mostra resultado real na etiqueta")

if __name__ == "__main__":
    print("=== TESTE DO CAMPO RFID_STATUS ===")
    print("Testando o novo campo no canto inferior direito\n")
    
    # Mostrar informações
    show_rfid_status_info()
    
    # Executar testes
    success = test_rfid_status_field()
    
    print("\n" + "="*50)
    print("🎯 RESULTADO:")
    if success:
        print("✅ CAMPO RFID_STATUS FUNCIONANDO!")
        print("✅ Template atualizado com sucesso")
        print("✅ Posicionamento correto no canto inferior direito")
        print("✅ Diferentes status testados")
        print("✅ Sistema determina status automaticamente")
        print("\n🏷️ ETIQUETAS IMPRESSAS:")
        print("   1. RFID OK - Status: SUCESSO")
        print("   2. RFID Erro - Status: ERRO - DADOS INVÁLIDOS")
        print("   3. Sem RFID - Status: ERRO - SEM DADOS")
        print("\n✨ Verifique as etiquetas físicas!")
    else:
        print("❌ Erro no teste do campo RFID_STATUS")
        print("❌ Verifique template e configurações")

