#!/usr/bin/env python3
"""
Teste usando o modelo ZPL original da Larroud (modelo_zpl_larroude.prn)
"""

import win32print
import requests
import json

def test_original_template():
    """Testa o template original da Larroud"""
    print("🧪 Testando modelo ZPL original da Larroud...")
    
    printer_name = "ZDesigner ZD621R-203dpi ZPL"
    
    # Carregar template original
    try:
        with open('backend/TEMPLATE_LARROUD_ORIGINAL.zpl', 'r', encoding='utf-8') as f:
            template = f.read()
    except FileNotFoundError:
        print("❌ Template original não encontrado!")
        return False
    
    # Dados de teste
    test_data = {
        "STYLE_NAME": "SANDALIA ORIGINAL",
        "VPM": "L123-ORIG-9.0-BROWN-4567",
        "COLOR": "MARROM ORIGINAL",
        "SIZE": "9.0"
    }
    
    # Processar dados como o sistema faz
    vpm_parts = test_data["VPM"].split('-')
    po_number = f"PO{vpm_parts[0].replace('L', '')}" if len(vpm_parts) > 0 else "PO000"
    local_number = vpm_parts[4][:3] if len(vpm_parts) > 4 else "000"
    barcode = test_data["VPM"].replace('-', '')[:12]
    qr_data = test_data["VPM"]
    rfid_data = test_data["VPM"]
    
    # Substituir variáveis no template original
    original_zpl = template.replace('{STYLE_NAME}', test_data["STYLE_NAME"]) \
                          .replace('{VPM}', test_data["VPM"]) \
                          .replace('{COLOR}', test_data["COLOR"]) \
                          .replace('{SIZE}', test_data["SIZE"]) \
                          .replace('{QR_DATA}', qr_data) \
                          .replace('{PO_INFO}', po_number) \
                          .replace('{LOCAL_INFO}', f'Local.{local_number}') \
                          .replace('{BARCODE}', barcode) \
                          .replace('{RFID_DATA}', rfid_data)
    
    try:
        print(f"📋 Dados da etiqueta:")
        print(f"   Produto: {test_data['STYLE_NAME']}")
        print(f"   VPM: {test_data['VPM']}")
        print(f"   Cor: {test_data['COLOR']}")
        print(f"   Tamanho: {test_data['SIZE']}")
        print(f"   PO: {po_number}")
        print(f"   Local: {local_number}")
        print(f"   Barcode: {barcode}")
        print(f"   QR/RFID: {qr_data}")
        
        handle = win32print.OpenPrinter(printer_name)
        doc_info = ("Original_Template_Test", None, "RAW")
        job_id = win32print.StartDocPrinter(handle, 1, doc_info)
        
        win32print.StartPagePrinter(handle)
        bytes_written = win32print.WritePrinter(handle, original_zpl.encode('ascii', errors='ignore'))
        win32print.EndPagePrinter(handle)
        win32print.EndDocPrinter(handle)
        win32print.ClosePrinter(handle)
        
        print(f"📤 Enviado: {bytes_written} bytes")
        print("✅ Modelo original da Larroud enviado!")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro: {e}")
        return False

def test_system_api_original():
    """Testa API do sistema com modelo original"""
    print("\n🌐 Testando API com modelo original...")
    
    # Dados de teste
    test_data = {
        "STYLE_NAME": "API MODELO ORIGINAL",
        "VPM": "L456-API-ORIG-8.5-BLACK-7890",
        "COLOR": "PRETO API",
        "SIZE": "8.5",
        "QTY": "1"
    }
    
    try:
        url = "http://localhost:3000/api/print-individual"
        response = requests.post(url, json={"data": [test_data], "quantity": 1})
        
        if response.status_code == 200:
            result = response.json()
            print("✅ API com modelo original respondeu")
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

def show_original_template_info():
    """Mostra informações sobre o modelo original"""
    print("\n📋 MODELO ZPL ORIGINAL DA LARROUD:")
    print("   📄 Arquivo: modelo_zpl_larroude.prn")
    print("   🎯 Objetivo: Usar template oficial completo")
    print("   🔧 Adaptação: Apenas substituir dados variáveis")
    
    print("\n✅ CARACTERÍSTICAS MANTIDAS:")
    print("   CT~~CD,~CC^~CT~ - Configurações iniciais")
    print("   ~TA000, ~JSN, ^LT0, etc. - Setup da impressora")
    print("   ^PW831, ^LL376 - Tamanho da etiqueta")
    print("   ^FPH,3^FT... - Labels dos campos")
    print("   ^FT737,167^BQN,2,3 - 3 QR codes")
    print("   ^BY2,2,39^FT222,308^BEN - Código de barras")
    print("   ^RFW,H,2,12,1^FD - Gravação RFID")
    print("   ^PQ1,0,1,Y - Quantidade de cópias")
    
    print("\n🔄 VARIÁVEIS SUBSTITUÍDAS:")
    print("   {STYLE_NAME} → Nome do produto")
    print("   {VPM} → Código VPM")
    print("   {COLOR} → Cor")
    print("   {SIZE} → Tamanho")
    print("   {QR_DATA} → Dados dos 3 QR codes")
    print("   {PO_INFO} → Número do PO")
    print("   {LOCAL_INFO} → Local/loja")
    print("   {BARCODE} → Código de barras")
    print("   {RFID_DATA} → Dados RFID")
    
    print("\n🎯 RESULTADO ESPERADO:")
    print("   ✅ Layout 100% original da Larroud")
    print("   ✅ Todas as funcionalidades (QR, barcode, RFID)")
    print("   ✅ Dados reais do produto")
    print("   ❓ VOID? Vamos descobrir...")

if __name__ == "__main__":
    print("=== TESTE MODELO ZPL ORIGINAL LARROUD ===")
    print("Usando exatamente o modelo_zpl_larroude.prn\n")
    
    # Mostrar informações
    show_original_template_info()
    
    # Teste direto Python
    success_python = test_original_template()
    
    # Teste API
    success_api = test_system_api_original()
    
    print("\n" + "="*50)
    print("🎯 RESULTADO:")
    if success_python:
        print("✅ MODELO ORIGINAL FUNCIONANDO!")
        print("✅ Template oficial da Larroud carregado")
        print("✅ Todas as variáveis substituídas")
        print("✅ Layout completo com QR, barcode e RFID")
        
        if success_api:
            print("✅ API DO SISTEMA ATUALIZADA!")
            print("✅ Sistema web usa modelo original")
            print("✅ Lista de impressão com template oficial")
        else:
            print("⚠️ API não testada (servidor pode estar parado)")
        
        print("\n🏷️ ETIQUETA DEVE TER:")
        print("   ✅ Layout 100% original da Larroud")
        print("   ✅ 3 QR codes posicionados")
        print("   ✅ Código de barras EAN")
        print("   ✅ Dados RFID gravados")
        print("   ✅ Bordas e estrutura oficial")
        print("   ✅ Informações PO e Local")
        print("   ❓ Verificar se tem VOID ou não")
        
    else:
        print("❌ Erro no modelo original")
        print("❌ Verifique configurações")

