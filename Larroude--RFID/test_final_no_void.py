#!/usr/bin/env python3
"""
Teste final - versão super limpa que deve eliminar VOID
"""

import win32print
import time

def test_final_no_void():
    """Teste final com ZPL super limpo"""
    print("🧪 Teste final - ZPL super limpo SEM VOID...")
    
    printer_name = "ZDesigner ZD621R-203dpi ZPL"
    
    # Dados de exemplo
    style_name = "JASMINI HI MULE"
    vpm = "L458-JASM-11.0-SILV-1885"
    color = "MIRROR SILVER"
    size = "11.0"
    rfid_content = vpm
    
    # Extrair dados
    vpm_parts = vpm.split('-')
    po_number = f"PO{vpm_parts[0].replace('L', '')}" if len(vpm_parts) > 0 else "PO000"
    local_number = vpm_parts[4][:3] if len(vpm_parts) > 4 else "000"
    barcode = vpm.replace('-', '')[:12]
    
    # ZPL super limpo - igual ao que está no sistema agora
    zpl_command = f"""^XA
^PW812
^LL406

^FO50,50^A0N,35,35^FDSTYLE: {style_name}^FS
^FO50,100^A0N,28,28^FDVPM: {vpm}^FS
^FO50,140^A0N,28,28^FDCOLOR: {color}^FS
^FO50,180^A0N,28,28^FDSIZE: {size}^FS

^FO50,240^BY2,3,40^BCN,40,Y,N,N^FD{barcode}^FS

^FO500,50^BQN,2,4^FD{rfid_content}^FS

^FO600,200^A0N,20,20^FD{po_number}^FS
^FO600,230^A0N,16,16^FDLocal.{local_number}^FS

^RFW,H,2,12,1^FD{rfid_content}^FS

^XZ"""
    
    try:
        handle = win32print.OpenPrinter(printer_name)
        doc_info = ("Final_No_VOID", None, "RAW")
        job_id = win32print.StartDocPrinter(handle, 1, doc_info)
        
        print(f"📄 Job iniciado: {job_id}")
        print(f"📋 Dados:")
        print(f"   Style: {style_name}")
        print(f"   VPM: {vpm}")
        print(f"   Color: {color}")
        print(f"   Size: {size}")
        print(f"   PO: {po_number}")
        print(f"   Local: {local_number}")
        print(f"   Barcode: {barcode}")
        
        win32print.StartPagePrinter(handle)
        bytes_written = win32print.WritePrinter(handle, zpl_command.encode('ascii'))
        win32print.EndPagePrinter(handle)
        win32print.EndDocPrinter(handle)
        
        print(f"📤 Bytes enviados: {bytes_written}")
        win32print.ClosePrinter(handle)
        
        print("✅ Etiqueta FINAL enviada!")
        print("\n🔍 Esta etiqueta deve ter:")
        print("   ❌ ZERO 'VOID'")
        print("   ✅ Texto limpo e claro")
        print("   ✅ Código de barras")
        print("   ✅ QR code")
        print("   ✅ Informações do produto")
        print("   ✅ Dados RFID gravados")
        print("   ✅ Layout simples e funcional")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro: {e}")
        return False

if __name__ == "__main__":
    print("=== TESTE FINAL - SEM VOID ===")
    test_final_no_void()
    
    print("\n" + "="*50)
    print("🎯 RESULTADO ESPERADO:")
    print("- Se esta etiqueta imprimir SEM VOID")
    print("- Então o sistema CSV está corrigido")
    print("- Use a página web normalmente")
    print("\n🌐 Acesse: http://localhost:3000")
    print("   → Aba 'Etiquetas CSV'")
    print("   → Clique 'Abrir Gerenciador de Etiquetas'")
    print("   → Teste a impressão individual")
