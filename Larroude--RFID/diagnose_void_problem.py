#!/usr/bin/env python3
"""
Diagnóstico completo do problema VOID
"""

import win32print
import time

def test_absolute_minimal():
    """Teste com ZPL absolutamente mínimo"""
    print("🧪 Teste 1: ZPL absolutamente mínimo...")
    
    printer_name = "ZDesigner ZD621R-203dpi ZPL"
    
    # ZPL mais básico possível
    minimal_zpl = """^XA
^FO100,100^A0N,50,50^FDTESTE^FS
^XZ"""
    
    try:
        handle = win32print.OpenPrinter(printer_name)
        doc_info = ("Minimal_Test", None, "RAW")
        job_id = win32print.StartDocPrinter(handle, 1, doc_info)
        
        win32print.StartPagePrinter(handle)
        bytes_written = win32print.WritePrinter(handle, minimal_zpl.encode('ascii'))
        win32print.EndPagePrinter(handle)
        win32print.EndDocPrinter(handle)
        
        print(f"📤 Enviado: {bytes_written} bytes")
        win32print.ClosePrinter(handle)
        
        print("✅ ZPL mínimo enviado!")
        return True
        
    except Exception as e:
        print(f"❌ Erro: {e}")
        return False

def force_printer_reset():
    """Reset forçado da impressora"""
    print("\n🔄 Teste 2: Reset forçado...")
    
    printer_name = "ZDesigner ZD621R-203dpi ZPL"
    
    # Comandos de reset mais agressivos
    reset_commands = """~JA
^XA^JUF^XZ
^XA^JUS^XZ
^XA^JUB^XZ"""
    
    try:
        handle = win32print.OpenPrinter(printer_name)
        doc_info = ("Force_Reset", None, "RAW")
        job_id = win32print.StartDocPrinter(handle, 1, doc_info)
        
        win32print.StartPagePrinter(handle)
        bytes_written = win32print.WritePrinter(handle, reset_commands.encode('ascii'))
        win32print.EndPagePrinter(handle)
        win32print.EndDocPrinter(handle)
        
        print(f"📤 Reset enviado: {bytes_written} bytes")
        win32print.ClosePrinter(handle)
        
        print("✅ Reset forçado enviado!")
        print("⏳ Aguardando 15 segundos...")
        time.sleep(15)
        
        return True
        
    except Exception as e:
        print(f"❌ Erro: {e}")
        return False

def test_without_any_special():
    """Teste sem NENHUM comando especial"""
    print("\n🧪 Teste 3: Sem comandos especiais...")
    
    printer_name = "ZDesigner ZD621R-203dpi ZPL"
    
    # Apenas texto, sem barcode, sem QR, sem RFID
    simple_text = """^XA
^FO50,50^A0N,40,40^FDJASMINI HI MULE^FS
^FO50,120^A0N,30,30^FDVPM: L458-JASM-11.0^FS
^FO50,170^A0N,30,30^FDCOLOR: MIRROR SILVER^FS
^FO50,220^A0N,30,30^FDSIZE: 11.0^FS
^FO50,270^A0N,25,25^FDTESTE SEM VOID^FS
^XZ"""
    
    try:
        handle = win32print.OpenPrinter(printer_name)
        doc_info = ("Simple_Text_Only", None, "RAW")
        job_id = win32print.StartDocPrinter(handle, 1, doc_info)
        
        win32print.StartPagePrinter(handle)
        bytes_written = win32print.WritePrinter(handle, simple_text.encode('ascii'))
        win32print.EndPagePrinter(handle)
        win32print.EndDocPrinter(handle)
        
        print(f"📤 Enviado: {bytes_written} bytes")
        win32print.ClosePrinter(handle)
        
        print("✅ Texto simples enviado!")
        return True
        
    except Exception as e:
        print(f"❌ Erro: {e}")
        return False

def check_printer_mode():
    """Verifica e força modo ZPL"""
    print("\n🔧 Teste 4: Forçando modo ZPL...")
    
    printer_name = "ZDesigner ZD621R-203dpi ZPL"
    
    # Comandos para garantir modo ZPL
    mode_commands = """^XA
^SZ
^XZ

^XA
^MNN
^XZ

^XA
^PR4
^XZ

^XA
^MD15
^XZ"""
    
    try:
        handle = win32print.OpenPrinter(printer_name)
        doc_info = ("Force_ZPL_Mode", None, "RAW")
        job_id = win32print.StartDocPrinter(handle, 1, doc_info)
        
        win32print.StartPagePrinter(handle)
        bytes_written = win32print.WritePrinter(handle, mode_commands.encode('ascii'))
        win32print.EndPagePrinter(handle)
        win32print.EndDocPrinter(handle)
        
        print(f"📤 Comandos de modo enviados: {bytes_written} bytes")
        win32print.ClosePrinter(handle)
        
        print("✅ Modo ZPL forçado!")
        time.sleep(5)
        
        return True
        
    except Exception as e:
        print(f"❌ Erro: {e}")
        return False

def test_different_sizes():
    """Testa diferentes tamanhos de etiqueta"""
    print("\n📏 Teste 5: Diferentes tamanhos...")
    
    printer_name = "ZDesigner ZD621R-203dpi ZPL"
    
    sizes = [
        ("4x2", "^PW812^LL406"),
        ("4x3", "^PW812^LL609"),
        ("3x2", "^PW609^LL406"),
        ("Auto", "")
    ]
    
    for size_name, size_cmd in sizes:
        print(f"   Testando {size_name}...")
        
        zpl = f"""^XA
{size_cmd}
^FO100,100^A0N,30,30^FDTESTE {size_name}^FS
^FO100,150^A0N,25,25^FDSEM VOID^FS
^XZ"""
        
        try:
            handle = win32print.OpenPrinter(printer_name)
            doc_info = (f"Size_Test_{size_name}", None, "RAW")
            job_id = win32print.StartDocPrinter(handle, 1, doc_info)
            
            win32print.StartPagePrinter(handle)
            bytes_written = win32print.WritePrinter(handle, zpl.encode('ascii'))
            win32print.EndPagePrinter(handle)
            win32print.EndDocPrinter(handle)
            
            print(f"      ✅ {size_name}: {bytes_written} bytes")
            win32print.ClosePrinter(handle)
            
            time.sleep(2)
            
        except Exception as e:
            print(f"      ❌ {size_name}: {e}")

def main():
    print("=== DIAGNÓSTICO COMPLETO DO VOID ===")
    print("Vamos testar progressivamente até encontrar a causa\n")
    
    # Teste 1: Mínimo absoluto
    result1 = test_absolute_minimal()
    input("\n⏸️ Pressione ENTER após verificar se apareceu VOID na etiqueta 1...")
    
    # Teste 2: Reset forçado
    force_printer_reset()
    
    # Teste 3: Sem comandos especiais
    result3 = test_without_any_special()
    input("\n⏸️ Pressione ENTER após verificar se apareceu VOID na etiqueta 2...")
    
    # Teste 4: Modo ZPL
    check_printer_mode()
    
    # Teste 5: Diferentes tamanhos
    test_different_sizes()
    input("\n⏸️ Pressione ENTER após verificar todas as etiquetas de tamanho...")
    
    print("\n" + "="*60)
    print("🎯 ANÁLISE DOS RESULTADOS:")
    print("1. Se TODAS as etiquetas têm VOID:")
    print("   → Problema no firmware/configuração da impressora")
    print("   → Necessário calibração manual na impressora")
    print("   → Verificar tipo de etiqueta (térmica direta vs transfer)")
    print("\n2. Se ALGUMAS etiquetas não têm VOID:")
    print("   → Problema com comandos específicos")
    print("   → Usar apenas os comandos que funcionaram")
    print("\n3. Se NENHUMA etiqueta tem VOID:")
    print("   → Problema resolvido!")
    print("   → Usar o ZPL que funcionou no sistema")

if __name__ == "__main__":
    main()
