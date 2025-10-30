#!/usr/bin/env python3
"""
Teste com ZPL mínimo e limpo para eliminar VOID
"""

import win32print
import time

def test_minimal_clean():
    """Testa ZPL mínimo sem comandos problemáticos"""
    print("🧪 Testando ZPL mínimo e limpo...")
    
    printer_name = "ZDesigner ZD621R-203dpi ZPL"
    
    # ZPL super simples, só com o essencial
    zpl_command = """^XA
^PW812
^LL406

^FO50,50^A0N,40,40^FDJASMINI HI MULE^FS
^FO50,100^A0N,30,30^FDVPM: L458-JASM-11.0-SILV-1885^FS
^FO50,140^A0N,30,30^FDCOLOR: MIRROR SILVER^FS
^FO50,180^A0N,30,30^FDSIZE: 11.0^FS

^FO50,250^BY2,3,50^BCN,50,Y,N,N^FDL458JASM110SILV1885^FS

^FO600,50^BQN,2,4^FDL458-JASM-11.0-SILV-1885^FS

^XZ"""
    
    try:
        handle = win32print.OpenPrinter(printer_name)
        doc_info = ("Minimal_Clean_Test", None, "RAW")
        job_id = win32print.StartDocPrinter(handle, 1, doc_info)
        
        print(f"📄 Job iniciado: {job_id}")
        
        win32print.StartPagePrinter(handle)
        bytes_written = win32print.WritePrinter(handle, zpl_command.encode('ascii'))
        win32print.EndPagePrinter(handle)
        win32print.EndDocPrinter(handle)
        
        print(f"📤 Bytes enviados: {bytes_written}")
        win32print.ClosePrinter(handle)
        
        print("✅ ZPL mínimo enviado!")
        print("🔍 Se ainda aparecer VOID, o problema é:")
        print("   - Configuração da impressora")
        print("   - Driver da impressora")
        print("   - Firmware da impressora")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro: {e}")
        return False

def test_without_special_commands():
    """Teste sem comandos especiais que podem causar VOID"""
    print("\n🧪 Testando sem comandos especiais...")
    
    printer_name = "ZDesigner ZD621R-203dpi ZPL"
    
    # ZPL sem comandos que podem causar problemas
    zpl_command = """^XA
^PW812
^LL406

^FO100,80^A0N,35,35^FDSTYLE: JASMINI HI MULE^FS
^FO100,130^A0N,28,28^FDVPM: L458-JASM-11.0-SILV-1885^FS
^FO100,170^A0N,28,28^FDCOLOR: MIRROR SILVER^FS
^FO100,210^A0N,28,28^FDSIZE: 11.0^FS

^FO100,270^BY2,3,40^BCN,40,Y,N,N^FDL458JASM110^FS

^XZ"""
    
    try:
        handle = win32print.OpenPrinter(printer_name)
        doc_info = ("No_Special_Commands", None, "RAW")
        job_id = win32print.StartDocPrinter(handle, 1, doc_info)
        
        print(f"📄 Job iniciado: {job_id}")
        
        win32print.StartPagePrinter(handle)
        bytes_written = win32print.WritePrinter(handle, zpl_command.encode('ascii'))
        win32print.EndPagePrinter(handle)
        win32print.EndDocPrinter(handle)
        
        print(f"📤 Bytes enviados: {bytes_written}")
        win32print.ClosePrinter(handle)
        
        print("✅ ZPL sem comandos especiais enviado!")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro: {e}")
        return False

def reset_printer():
    """Envia comando de reset para a impressora"""
    print("\n🔄 Enviando comando de reset...")
    
    printer_name = "ZDesigner ZD621R-203dpi ZPL"
    
    # Comandos de reset da impressora
    reset_command = """~JA
^XA
^JUS
^XZ"""
    
    try:
        handle = win32print.OpenPrinter(printer_name)
        doc_info = ("Printer_Reset", None, "RAW")
        job_id = win32print.StartDocPrinter(handle, 1, doc_info)
        
        win32print.StartPagePrinter(handle)
        bytes_written = win32print.WritePrinter(handle, reset_command.encode('ascii'))
        win32print.EndPagePrinter(handle)
        win32print.EndDocPrinter(handle)
        
        print(f"📤 Reset enviado: {bytes_written} bytes")
        win32print.ClosePrinter(handle)
        
        print("✅ Comando de reset enviado!")
        print("⏳ Aguarde 5 segundos...")
        time.sleep(5)
        
        return True
        
    except Exception as e:
        print(f"❌ Erro no reset: {e}")
        return False

if __name__ == "__main__":
    print("=== Eliminando VOID - Testes Progressivos ===")
    
    # 1. Reset da impressora
    reset_printer()
    
    # 2. Teste mínimo
    test_minimal_clean()
    
    # 3. Aguardar e testar sem comandos especiais
    print("\n⏳ Aguardando 3 segundos...")
    time.sleep(3)
    
    test_without_special_commands()
    
    print("\n💡 Se ainda aparecer VOID:")
    print("1. Problema no firmware da impressora")
    print("2. Configuração do driver")
    print("3. Etiquetas incompatíveis")
    print("4. Necessário calibração da impressora")
