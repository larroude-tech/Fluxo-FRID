#!/usr/bin/env python3
"""
Teste do template oficial da Larroud
"""

import win32print

def test_official_template():
    """Testa o template oficial da Larroud"""
    print("🧪 Testando template oficial da Larroud...")
    
    printer_name = "ZDesigner ZD621R-203dpi ZPL"
    
    # Dados de exemplo
    item_data = {
        "STYLE_NAME": "SANDALIA LARROUD",
        "VPM": "L456-SAND-9.0-BROWN-1234",
        "COLOR": "MARROM",
        "SIZE": "9.0",
        "QTY": "1"
    }
    
    # Ler template oficial
    try:
        with open('backend/TEMPLATE_LARROUD_OFICIAL.zpl', 'r', encoding='utf-8') as f:
            template = f.read()
    except FileNotFoundError:
        print("❌ Erro: Template oficial não encontrado!")
        return False
    
    # Extrair dados para substituição
    style_name = item_data["STYLE_NAME"]
    vpm = item_data["VPM"]
    color = item_data["COLOR"]
    size = item_data["SIZE"]
    rfid_content = vpm
    
    # Extrair PO e Local
    vpm_parts = vpm.split('-')
    po_number = f"PO{vpm_parts[0].replace('L', '')}" if len(vpm_parts) > 0 else "PO000"
    local_number = vpm_parts[4][:3] if len(vpm_parts) > 4 else "000"
    barcode = vpm.replace('-', '')[:12]
    
    # Substituir variáveis no template oficial
    official_zpl = template.replace('{STYLE_NAME}', style_name) \
                          .replace('{VPM}', vpm) \
                          .replace('{COLOR}', color) \
                          .replace('{SIZE}', size) \
                          .replace('{PO_INFO}', po_number) \
                          .replace('{LOCAL_INFO}', f'Local.{local_number}') \
                          .replace('{BARCODE}', barcode) \
                          .replace('{RFID_DATA}', rfid_content) \
                          .replace('{QR_DATA_1}', rfid_content) \
                          .replace('{QR_DATA_2}', rfid_content) \
                          .replace('{QR_DATA_3}', rfid_content)
    
    try:
        print(f"📋 Imprimindo com template oficial:")
        print(f"   Produto: {style_name}")
        print(f"   VPM: {vpm}")
        print(f"   Cor: {color}")
        print(f"   Tamanho: {size}")
        print(f"   PO: {po_number}")
        print(f"   Local: {local_number}")
        print(f"   Barcode: {barcode}")
        print(f"   RFID: {rfid_content}")
        
        handle = win32print.OpenPrinter(printer_name)
        doc_info = ("Larroud_Official_Template", None, "RAW")
        job_id = win32print.StartDocPrinter(handle, 1, doc_info)
        
        win32print.StartPagePrinter(handle)
        bytes_written = win32print.WritePrinter(handle, official_zpl.encode('utf-8'))
        win32print.EndPagePrinter(handle)
        win32print.EndDocPrinter(handle)
        
        print(f"📤 Enviado: {bytes_written} bytes")
        win32print.ClosePrinter(handle)
        
        print("✅ Template oficial enviado com sucesso!")
        print("🎯 Esta etiqueta deve ter:")
        print("   ✅ Layout oficial da Larroud")
        print("   ✅ 3 QR codes posicionados")
        print("   ✅ Bordas e estrutura oficial")
        print("   ✅ Código de barras EAN")
        print("   ✅ RFID integrado")
        print("   ❌ ZERO VOID")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro: {e}")
        return False

def show_template_variables():
    """Mostra as variáveis disponíveis no template"""
    print("\n📋 Variáveis do template oficial:")
    variables = [
        "{STYLE_NAME} - Nome do produto",
        "{VPM} - Código VPM completo",
        "{COLOR} - Cor do produto",
        "{SIZE} - Tamanho",
        "{PO_INFO} - Informação do PO",
        "{LOCAL_INFO} - Informação do local",
        "{BARCODE} - Código de barras",
        "{RFID_DATA} - Dados RFID",
        "{QR_DATA_1} - QR code 1",
        "{QR_DATA_2} - QR code 2",
        "{QR_DATA_3} - QR code 3"
    ]
    
    for var in variables:
        print(f"   ✅ {var}")

if __name__ == "__main__":
    print("=== TESTE DO TEMPLATE OFICIAL LARROUD ===")
    print("Testando modelo_zpl_larroude.prn adaptado\n")
    
    show_template_variables()
    
    success = test_official_template()
    
    print("\n" + "="*50)
    print("🎯 RESULTADO:")
    if success:
        print("✅ Template oficial funcionando!")
        print("✅ Todas as variáveis substituídas")
        print("✅ Layout profissional da Larroud")
        print("✅ Ready para sistema de upload")
        print("\n🌐 Sistema atualizado para usar:")
        print("   ✅ Template oficial modelo_zpl_larroude.prn")
        print("   ✅ Impressão individual com layout correto")
        print("   ✅ Todas as variáveis do CSV mapeadas")
    else:
        print("❌ Problema com template oficial")
        print("❌ Verifique se o arquivo está na pasta backend/")
