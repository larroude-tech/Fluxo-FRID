#!/usr/bin/env python3
"""
Teste com o formato que funciona - baseado no diagnose_void_problem.py
"""

import win32print
import time

def test_working_format():
    """Testa o formato que funcionou, mas com dados completos"""
    print("🧪 Testando formato que funciona - com dados completos...")
    
    printer_name = "ZDesigner ZD621R-203dpi ZPL"
    
    # Dados da etiqueta
    style_name = "JASMINI HI MULE"
    vpm = "L458-JASM-11.0-SILV-1885"
    color = "MIRROR SILVER"
    size = "11.0"
    
    # Extrair PO e Local
    vpm_parts = vpm.split('-')
    po_number = f"PO{vpm_parts[0].replace('L', '')}" if len(vpm_parts) > 0 else "PO000"
    local_number = vpm_parts[4][:3] if len(vpm_parts) > 4 else "000"
    barcode = vpm.replace('-', '')[:12]
    
    # ZPL baseado no formato que funcionou (mínimo) mas com dados completos
    working_zpl = f"""^XA
^FO50,50^A0N,35,35^FD{style_name}^FS
^FO50,100^A0N,28,28^FDVPM: {vpm}^FS
^FO50,140^A0N,28,28^FDCOLOR: {color}^FS
^FO50,180^A0N,28,28^FDSIZE: {size}^FS
^FO50,240^BY2,3,40^BCN,40,Y,N,N^FD{barcode}^FS
^FO500,50^BQN,2,4^FD{vpm}^FS
^FO600,200^A0N,20,20^FD{po_number}^FS
^FO600,230^A0N,16,16^FDLocal.{local_number}^FS
^XZ"""
    
    try:
        handle = win32print.OpenPrinter(printer_name)
        doc_info = ("Working_Format_Test", None, "RAW")
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
        bytes_written = win32print.WritePrinter(handle, working_zpl.encode('ascii'))
        win32print.EndPagePrinter(handle)
        win32print.EndDocPrinter(handle)
        
        print(f"📤 Bytes enviados: {bytes_written}")
        win32print.ClosePrinter(handle)
        
        print("✅ Formato que funciona enviado!")
        print("🔍 Esta etiqueta deve ter:")
        print("   ❌ ZERO VOID")
        print("   ✅ Todos os dados da etiqueta")
        print("   ✅ Código de barras")
        print("   ✅ QR code")
        print("   ✅ Layout organizado")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro: {e}")
        return False

def test_working_with_rfid():
    """Testa o formato que funciona + RFID"""
    print("\n🧪 Testando formato que funciona + RFID...")
    
    printer_name = "ZDesigner ZD621R-203dpi ZPL"
    
    # Dados da etiqueta
    style_name = "JASMINI HI MULE"
    vpm = "L458-JASM-11.0-SILV-1885"
    color = "MIRROR SILVER"
    size = "11.0"
    
    # ZPL com RFID (formato que funciona)
    working_rfid_zpl = f"""^XA
^FO50,50^A0N,35,35^FD{style_name}^FS
^FO50,100^A0N,28,28^FDVPM: {vpm}^FS
^FO50,140^A0N,28,28^FDCOLOR: {color}^FS
^FO50,180^A0N,28,28^FDSIZE: {size}^FS
^FO50,240^BY2,3,40^BCN,40,Y,N,N^FDL458JASM110^FS
^FO500,50^BQN,2,4^FD{vpm}^FS
^RFW,H,2,12,1^FD{vpm}^FS
^XZ"""
    
    try:
        handle = win32print.OpenPrinter(printer_name)
        doc_info = ("Working_RFID_Test", None, "RAW")
        job_id = win32print.StartDocPrinter(handle, 1, doc_info)
        
        win32print.StartPagePrinter(handle)
        bytes_written = win32print.WritePrinter(handle, working_rfid_zpl.encode('ascii'))
        win32print.EndPagePrinter(handle)
        win32print.EndDocPrinter(handle)
        
        print(f"📤 Bytes enviados: {bytes_written}")
        win32print.ClosePrinter(handle)
        
        print("✅ Formato com RFID enviado!")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro: {e}")
        return False

if __name__ == "__main__":
    print("=== TESTE DO FORMATO QUE FUNCIONA ===")
    print("Baseado no diagnose_void_problem.py que funcionou\n")
    
    # Teste 1: Formato completo
    result1 = test_working_format()
    
    # Aguardar
    time.sleep(3)
    
    # Teste 2: Formato com RFID
    result2 = test_working_with_rfid()
    
    print("\n" + "="*50)
    print("🎯 RESULTADO:")
    print("Se estas etiquetas saíram SEM VOID:")
    print("✅ Encontramos o formato correto!")
    print("✅ Vou atualizar o sistema para usar este formato")
    print("\nSe ainda aparecer VOID:")
    print("❌ O problema pode ser com comandos específicos")
    print("❌ Vamos usar apenas o ZPL mais básico")
