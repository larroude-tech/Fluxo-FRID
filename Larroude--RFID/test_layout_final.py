#!/usr/bin/env python3
"""
Teste final do layout corrigido baseado na imagem
"""

import win32print
import time

def test_final_layout():
    """Testa o layout final corrigido"""
    print("🧪 Testando layout final corrigido...")
    
    printer_name = "ZDesigner ZD621R-203dpi ZPL"
    
    # Dados de teste baseados na imagem
    style_name = "JASMINI HI MULE"
    vpm = "L458-JASM-11.0-SILV-1885"
    color = "MIRROR SILVER"
    size = "11.0"
    rfid_content = vpm
    
    # Extrair PO e Local do VPM
    vpm_parts = vpm.split('-')
    po_number = f"PO{vpm_parts[0].replace('L', '')}" if len(vpm_parts) > 0 else "PO000"
    local_number = vpm_parts[4][:3] if len(vpm_parts) > 4 else "000"
    
    # Código de barras
    barcode = vpm.replace('-', '')[:12]
    
    print(f"📋 Dados processados:")
    print(f"   PO: {po_number}")
    print(f"   Local: {local_number}")
    print(f"   Barcode: {barcode}")
    
    # ZPL final
    zpl_command = f"""^XA
^CI28
^LH0,0
^MD30
^PR5
^PW812
^LL406

^FO12,12^GB788,382,2,B,24^FS

^FO36,48^GB180,290,1,B,8^FS

^FO50,70^GB80,80,2,B,8^FS
^FO65,95^A0N,16,16^FDICON^FS

^FO60,180^BQN,2,4^FD{rfid_content}^FS

^FO230,48^GB2,290,2^FS

^CF0,30
^FO250,70^FB420,2,0,L,0^FDSTYLE NAME: {style_name}^FS

^CF0,22
^FO250,120^FB420,1,0,L,0^FDVPM: {vpm}^FS

^CF0,22
^FO250,155^FB420,1,0,L,0^FDCOLOR: {color}^FS

^CF0,22
^FO250,190^FB420,1,0,L,0^FDSIZE: {size}^FS

^BY2,3,50
^FO250,240^BCN,50,Y,N,N^FD{barcode}^FS

^FO690,48^GB2,290,2^FS

^FO710,60^BQN,2,3^FD{rfid_content}-TOP^FS

^FO705,150^GB90,50,2,B,8^FS
^CF0,16
^FO710,160^FB80,1,0,C,0^FD{po_number}^FS
^CF0,14
^FO710,180^FB80,1,0,C,0^FDLocal.{local_number}^FS

^FO710,220^BQN,2,3^FD{rfid_content}-BOT^FS

^RFW,H,1,2,1^FD3000^FS
^RFW,H,2,12,1^FD{rfid_content}^FS

^XZ"""
    
    try:
        # Abrir impressora
        handle = win32print.OpenPrinter(printer_name)
        
        # Configurar para modo RAW
        doc_info = ("Layout_Final_Test", None, "RAW")
        
        # Iniciar job
        job_id = win32print.StartDocPrinter(handle, 1, doc_info)
        
        print(f"📄 Job iniciado: {job_id}")
        
        # Enviar dados
        win32print.StartPagePrinter(handle)
        bytes_written = win32print.WritePrinter(handle, zpl_command.encode('ascii'))
        win32print.EndPagePrinter(handle)
        win32print.EndDocPrinter(handle)
        
        print(f"📤 Bytes enviados: {bytes_written}")
        
        win32print.ClosePrinter(handle)
        
        print("✅ Layout final enviado!")
        print("🔍 Deveria imprimir:")
        print("   - ❌ SEM 'VOID'")
        print("   - ✅ Layout idêntico à imagem")
        print("   - ✅ Bordas arredondadas")
        print("   - ✅ Ícone à esquerda")
        print("   - ✅ QR code esquerdo")
        print("   - ✅ Informações centrais organizadas")
        print("   - ✅ Código de barras correto")
        print("   - ✅ 3 elementos à direita (QR, PO/Local, QR)")
        print("   - ✅ Dados RFID gravados")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro ao imprimir layout final: {e}")
        return False

if __name__ == "__main__":
    print("=== Teste Layout Final - SEM VOID ===")
    test_final_layout()
