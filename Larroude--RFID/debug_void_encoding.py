#!/usr/bin/env python3
"""
Debug do problema VOID - testando diferentes codificações
"""

import win32print

def test_different_encodings():
    """Testa diferentes codificações para eliminar VOID"""
    print("🔍 Debugando problema VOID - testando codificações...")
    
    printer_name = "ZDesigner ZD621R-203dpi ZPL"
    
    # ZPL simples que funciona no ZebraDesigner
    simple_zpl = """^XA
^FO100,100^A0N,50,50^FDTESTE SEM VOID^FS
^XZ"""
    
    encodings_to_test = [
        ('utf-8', 'UTF-8'),
        ('ascii', 'ASCII'),
        ('latin-1', 'Latin-1'),
        ('cp1252', 'Windows-1252'),
        ('raw', 'RAW (sem encoding)')
    ]
    
    for encoding, name in encodings_to_test:
        print(f"\n🧪 Testando {name}...")
        
        try:
            handle = win32print.OpenPrinter(printer_name)
            doc_info = (f"Test_{encoding}", None, "RAW")
            job_id = win32print.StartDocPrinter(handle, 1, doc_info)
            
            win32print.StartPagePrinter(handle)
            
            if encoding == 'raw':
                # Enviar como bytes brutos
                bytes_written = win32print.WritePrinter(handle, simple_zpl.encode('ascii'))
            else:
                # Tentar codificação específica
                bytes_written = win32print.WritePrinter(handle, simple_zpl.encode(encoding))
            
            win32print.EndPagePrinter(handle)
            win32print.EndDocPrinter(handle)
            win32print.ClosePrinter(handle)
            
            print(f"✅ {name}: {bytes_written} bytes enviados")
            
        except Exception as e:
            print(f"❌ {name}: Erro - {e}")
        
        input(f"📋 Pressione ENTER após verificar a etiqueta {name}...")

def test_template_with_raw_bytes():
    """Testa o template oficial com bytes brutos"""
    print("\n🧪 Testando template oficial com bytes brutos...")
    
    printer_name = "ZDesigner ZD621R-203dpi ZPL"
    
    # Carregar template oficial
    try:
        with open('backend/TEMPLATE_LARROUD_OFICIAL.zpl', 'r', encoding='utf-8') as f:
            template = f.read()
    except FileNotFoundError:
        print("❌ Template oficial não encontrado!")
        return
    
    # Dados de teste
    test_data = {
        "STYLE_NAME": "TESTE RAW BYTES",
        "VPM": "L999-TEST-11.0-RED-5555",
        "COLOR": "VERMELHO",
        "SIZE": "11.0"
    }
    
    # Substituir variáveis
    vpm_parts = test_data["VPM"].split('-')
    po_number = f"PO{vpm_parts[0].replace('L', '')}" if len(vpm_parts) > 0 else "PO000"
    local_number = vpm_parts[4][:3] if len(vpm_parts) > 4 else "000"
    barcode = test_data["VPM"].replace('-', '')[:12]
    
    final_zpl = template.replace('{STYLE_NAME}', test_data["STYLE_NAME"]) \
                       .replace('{VPM}', test_data["VPM"]) \
                       .replace('{COLOR}', test_data["COLOR"]) \
                       .replace('{SIZE}', test_data["SIZE"]) \
                       .replace('{PO_INFO}', po_number) \
                       .replace('{LOCAL_INFO}', f'Local.{local_number}') \
                       .replace('{BARCODE}', barcode) \
                       .replace('{RFID_DATA}', test_data["VPM"]) \
                       .replace('{QR_DATA_1}', test_data["VPM"]) \
                       .replace('{QR_DATA_2}', test_data["VPM"]) \
                       .replace('{QR_DATA_3}', test_data["VPM"])
    
    try:
        handle = win32print.OpenPrinter(printer_name)
        doc_info = ("Template_Raw_Bytes", None, "RAW")
        job_id = win32print.StartDocPrinter(handle, 1, doc_info)
        
        win32print.StartPagePrinter(handle)
        
        # Enviar como ASCII puro (como ZebraDesigner faria)
        bytes_written = win32print.WritePrinter(handle, final_zpl.encode('ascii', errors='ignore'))
        
        win32print.EndPagePrinter(handle)
        win32print.EndDocPrinter(handle)
        win32print.ClosePrinter(handle)
        
        print(f"✅ Template oficial (ASCII): {bytes_written} bytes enviados")
        
    except Exception as e:
        print(f"❌ Erro: {e}")

def save_zpl_for_comparison():
    """Salva o ZPL gerado para comparar com ZebraDesigner"""
    print("\n💾 Salvando ZPL para comparação...")
    
    # Carregar template
    try:
        with open('backend/TEMPLATE_LARROUD_OFICIAL.zpl', 'r', encoding='utf-8') as f:
            template = f.read()
    except FileNotFoundError:
        print("❌ Template não encontrado!")
        return
    
    # Dados de teste
    test_data = {
        "STYLE_NAME": "SANDALIA TESTE",
        "VPM": "L123-TEST-9.0-BLUE-4567",
        "COLOR": "AZUL",
        "SIZE": "9.0"
    }
    
    # Substituir variáveis
    vpm_parts = test_data["VPM"].split('-')
    po_number = f"PO{vpm_parts[0].replace('L', '')}" if len(vpm_parts) > 0 else "PO000"
    local_number = vpm_parts[4][:3] if len(vpm_parts) > 4 else "000"
    barcode = test_data["VPM"].replace('-', '')[:12]
    
    final_zpl = template.replace('{STYLE_NAME}', test_data["STYLE_NAME"]) \
                       .replace('{VPM}', test_data["VPM"]) \
                       .replace('{COLOR}', test_data["COLOR"]) \
                       .replace('{SIZE}', test_data["SIZE"]) \
                       .replace('{PO_INFO}', po_number) \
                       .replace('{LOCAL_INFO}', f'Local.{local_number}') \
                       .replace('{BARCODE}', barcode) \
                       .replace('{RFID_DATA}', test_data["VPM"]) \
                       .replace('{QR_DATA_1}', test_data["VPM"]) \
                       .replace('{QR_DATA_2}', test_data["VPM"]) \
                       .replace('{QR_DATA_3}', test_data["VPM"])
    
    # Salvar em arquivo
    with open('zpl_gerado_debug.zpl', 'w', encoding='ascii', errors='ignore') as f:
        f.write(final_zpl)
    
    print("✅ ZPL salvo em: zpl_gerado_debug.zpl")
    print("🔍 Compare este arquivo com o que funciona no ZebraDesigner")
    print("📋 Abra ambos no ZebraDesigner para ver diferenças")

if __name__ == "__main__":
    print("=== DEBUG VOID - TESTANDO CODIFICAÇÕES ===")
    print("Vamos descobrir por que aparece VOID quando enviamos via código\n")
    
    # Teste 1: Diferentes codificações
    test_different_encodings()
    
    # Teste 2: Template com bytes brutos
    test_template_with_raw_bytes()
    
    # Teste 3: Salvar para comparação
    save_zpl_for_comparison()
    
    print("\n" + "="*50)
    print("🎯 PRÓXIMOS PASSOS:")
    print("1. Verifique qual codificação NÃO gerou VOID")
    print("2. Compare zpl_gerado_debug.zpl com ZebraDesigner")
    print("3. Vamos ajustar o sistema com a codificação correta")
