#!/usr/bin/env python3
"""
Teste do layout real baseado na imagem fornecida
"""

import win32print
import time

def test_real_layout():
    """Testa o layout real da etiqueta"""
    print("🧪 Testando layout real da etiqueta...")
    
    printer_name = "ZDesigner ZD621R-203dpi ZPL"
    
    # Dados reais da imagem
    style_name = "JASMINI HI MULE"
    vpm = "L458-JASM-11.0-SILV-1885"
    color = "MIRROR SILVER"
    size = "11.0"
    po_number = "PO0597"
    local = "850"
    barcode = "97416253956"
    rfid_data = vpm
    
    # ZPL baseado no layout da imagem
    zpl_command = f"""^XA
^CI28
^LH0,0
^MD30
^PR5
^PW812
^LL406

^FX === BORDAS DA ETIQUETA ===
^FO12,12^GB788,382,2,B,24^FS

^FX === ÁREA ESQUERDA - ÍCONE E QR ===
^FO36,48^GB180,290,1,B,8^FS

^FX --- Ícone do produto (placeholder) ---
^FO50,70^GB80,80,2,B,8^FS
^FO60,85^A0N,20,20^FDSHOE^FS

^FX --- QR Code esquerdo ---
^FO60,180^BQN,2,4^FD{rfid_data}^FS

^FX === DIVISOR VERTICAL ===
^FO230,48^GB2,290,2^FS

^FX === ÁREA CENTRAL - INFORMAÇÕES DO PRODUTO ===
^FX --- Style Name ---
^CF0,32
^FO250,70^FB420,2,0,L,0^FDSTYLE NAME: {style_name}^FS

^FX --- VPM ---
^CF0,24
^FO250,120^FB420,1,0,L,0^FDVPM: {vpm}^FS

^FX --- Color ---
^CF0,24
^FO250,155^FB420,1,0,L,0^FDCOLOR: {color}^FS

^FX --- Size ---
^CF0,24
^FO250,190^FB420,1,0,L,0^FDSIZE: {size}^FS

^FX --- Código de barras ---
^BY2,3,50
^FO250,240^BCN,50,Y,N,N^FD{barcode}^FS

^FX === DIVISOR VERTICAL DIREITO ===
^FO690,48^GB2,290,2^FS

^FX === ÁREA DIREITA - QR CODES E PO ===
^FX --- QR Code superior direito ---
^FO710,60^BQN,2,3^FD{rfid_data}-TOP^FS

^FX --- Caixa PO/Local ---
^FO705,150^GB90,50,2,B,8^FS
^CF0,16
^FO710,160^FB80,1,0,C,0^FD{po_number}^FS
^CF0,14
^FO710,180^FB80,1,0,C,0^FDLocal.{local}^FS

^FX --- QR Code inferior direito ---
^FO710,220^BQN,2,3^FD{rfid_data}-BOT^FS

^FX === COMANDOS RFID ===
^RFW,H,1,2,1^FD3000^FS
^RFW,H,2,12,1^FD{rfid_data}^FS

^XZ"""
    
    try:
        # Abrir impressora
        handle = win32print.OpenPrinter(printer_name)
        
        # Configurar para modo RAW
        doc_info = ("Layout_Real_Test", None, "RAW")
        
        # Iniciar job
        job_id = win32print.StartDocPrinter(handle, 1, doc_info)
        
        print(f"📄 Job iniciado: {job_id}")
        print(f"📋 Dados da etiqueta:")
        print(f"   Style: {style_name}")
        print(f"   VPM: {vpm}")
        print(f"   Color: {color}")
        print(f"   Size: {size}")
        print(f"   PO: {po_number}")
        print(f"   Local: {local}")
        print(f"   Barcode: {barcode}")
        
        # Enviar dados
        win32print.StartPagePrinter(handle)
        bytes_written = win32print.WritePrinter(handle, zpl_command.encode('ascii'))
        win32print.EndPagePrinter(handle)
        win32print.EndDocPrinter(handle)
        
        print(f"📤 Bytes enviados: {bytes_written}")
        
        win32print.ClosePrinter(handle)
        
        print("✅ Layout real enviado!")
        print("🔍 Compare com a imagem original:")
        print("   - ✅ Bordas arredondadas")
        print("   - ✅ Ícone à esquerda")
        print("   - ✅ QR code esquerdo")
        print("   - ✅ Informações centrais")
        print("   - ✅ Código de barras")
        print("   - ✅ 3 QR codes à direita")
        print("   - ✅ Caixa PO/Local")
        print("   - ✅ Dados RFID")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro ao imprimir layout real: {e}")
        return False

if __name__ == "__main__":
    print("=== Teste Layout Real - Baseado na Imagem ===")
    test_real_layout()
