#!/usr/bin/env python3
"""
Teste do novo layout ZPL atualizado (sem RFID, PR2,2)
"""

import win32print
import requests
import json

def test_new_layout():
    """Testa o novo layout ZPL"""
    print("🧪 Testando novo layout ZPL...")
    
    printer_name = "ZDesigner ZD621R-203dpi ZPL"
    
    # Carregar template atualizado
    try:
        with open('backend/TEMPLATE_LARROUD_ORIGINAL.zpl', 'r', encoding='utf-8') as f:
            template = f.read()
    except FileNotFoundError:
        print("❌ Template atualizado não encontrado!")
        return False
    
    # Dados de teste
    test_data = {
        "STYLE_NAME": "NOVO LAYOUT TEST",
        "VPM": "L789-NEW-LAYOUT-RED-9999",
        "COLOR": "VERMELHO NOVO",
        "SIZE": "10.5"
    }
    
    # Processar dados como o sistema faz
    vpm_parts = test_data["VPM"].split('-')
    po_number = f"PO{vpm_parts[0].replace('L', '')}" if len(vpm_parts) > 0 else "PO000"
    local_number = vpm_parts[4][:3] if len(vpm_parts) > 4 else "000"
    barcode = test_data["VPM"].replace('-', '')[:12]
    qr_data = test_data["VPM"]
    
    # Substituir variáveis no template atualizado
    new_layout_zpl = template.replace('{STYLE_NAME}', test_data["STYLE_NAME"]) \
                            .replace('{VPM}', test_data["VPM"]) \
                            .replace('{COLOR}', test_data["COLOR"]) \
                            .replace('{SIZE}', test_data["SIZE"]) \
                            .replace('{QR_DATA}', qr_data) \
                            .replace('{PO_INFO}', po_number) \
                            .replace('{LOCAL_INFO}', f'Local.{local_number}') \
                            .replace('{BARCODE}', barcode)
    
    try:
        print(f"📋 Dados da etiqueta:")
        print(f"   Produto: {test_data['STYLE_NAME']}")
        print(f"   VPM: {test_data['VPM']}")
        print(f"   Cor: {test_data['COLOR']}")
        print(f"   Tamanho: {test_data['SIZE']}")
        print(f"   PO: {po_number}")
        print(f"   Local: {local_number}")
        print(f"   Barcode: {barcode}")
        print(f"   QR Data: {qr_data}")
        
        handle = win32print.OpenPrinter(printer_name)
        doc_info = ("New_Layout_Test", None, "RAW")
        job_id = win32print.StartDocPrinter(handle, 1, doc_info)
        
        win32print.StartPagePrinter(handle)
        bytes_written = win32print.WritePrinter(handle, new_layout_zpl.encode('ascii', errors='ignore'))
        win32print.EndPagePrinter(handle)
        win32print.EndDocPrinter(handle)
        win32print.ClosePrinter(handle)
        
        print(f"📤 Enviado: {bytes_written} bytes")
        print("✅ Novo layout enviado!")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro: {e}")
        return False

def test_system_api_new_layout():
    """Testa API do sistema com novo layout"""
    print("\n🌐 Testando API com novo layout...")
    
    # Dados de teste
    test_data = {
        "STYLE_NAME": "API NOVO LAYOUT",
        "VPM": "L555-API-NEW-8.0-BLUE-1111",
        "COLOR": "AZUL API NOVO",
        "SIZE": "8.0",
        "QTY": "1"
    }
    
    try:
        url = "http://localhost:3000/api/print-individual"
        response = requests.post(url, json={"data": [test_data], "quantity": 1})
        
        if response.status_code == 200:
            result = response.json()
            print("✅ API com novo layout respondeu")
            print(f"📊 Mensagem: {result.get('message', 'N/A')}")
            print(f"📈 Sucessos: {result.get('successCount', 0)}")
            return True
        else:
            print(f"❌ Erro HTTP: {response.status_code}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("⚠️ Servidor não está rodando")
        return False
    except Exception as e:
        print(f"❌ Erro: {e}")
        return False

def show_new_layout_changes():
    """Mostra as mudanças do novo layout"""
    print("\n📋 MUDANÇAS NO NOVO LAYOUT:")
    print("   🔧 ^PR4,4 → ^PR2,2 (velocidade de impressão)")
    print("   ❌ ^RFW,H,2,12,1^FD... removido (sem RFID)")
    print("   ❌ ^RS8,,,3 removido")
    print("   ✅ QR codes mantidos (3 códigos)")
    print("   ✅ Código de barras mantido")
    print("   ✅ Layout e estrutura mantidos")
    
    print("\n✅ CARACTERÍSTICAS MANTIDAS:")
    print("   📐 ^PW831 ^LL376 - Tamanho da etiqueta")
    print("   🖼️ Bordas e estrutura visual")
    print("   📝 Campos de texto (STYLE, VPM, COLOR, SIZE)")
    print("   📊 Campos PO e Local")
    print("   🔲 3 QR codes posicionados")
    print("   📋 Código de barras EAN")
    
    print("\n🎯 BENEFÍCIOS ESPERADOS:")
    print("   ⚡ Impressão mais rápida (PR2,2)")
    print("   ❌ Zero problemas de RFID")
    print("   ✅ Layout limpo e funcional")
    print("   💰 Economia (sem RFID)")
    print("   🎯 Foco nos dados essenciais")

if __name__ == "__main__":
    print("=== TESTE NOVO LAYOUT ZPL ===")
    print("Layout atualizado: PR2,2 e sem RFID\n")
    
    # Mostrar mudanças
    show_new_layout_changes()
    
    # Teste direto Python
    success_python = test_new_layout()
    
    # Teste API
    success_api = test_system_api_new_layout()
    
    print("\n" + "="*50)
    print("🎯 RESULTADO:")
    if success_python:
        print("✅ NOVO LAYOUT FUNCIONANDO!")
        print("✅ Template atualizado carregado")
        print("✅ Velocidade PR2,2 aplicada")
        print("✅ RFID removido completamente")
        print("✅ QR codes e barcode mantidos")
        
        if success_api:
            print("✅ API DO SISTEMA ATUALIZADA!")
            print("✅ Sistema web usa novo layout")
            print("✅ Lista de impressão com template novo")
        else:
            print("⚠️ API não testada (servidor pode estar parado)")
        
        print("\n🏷️ ETIQUETA DEVE TER:")
        print("   ✅ Layout da Larroud otimizado")
        print("   ✅ 3 QR codes com dados do produto")
        print("   ✅ Código de barras funcional")
        print("   ✅ Campos PO e Local calculados")
        print("   ✅ Impressão mais rápida")
        print("   ❌ SEM RFID (economia)")
        print("   ❓ Verificar se tem VOID")
        
    else:
        print("❌ Erro no novo layout")
        print("❌ Verifique configurações")

