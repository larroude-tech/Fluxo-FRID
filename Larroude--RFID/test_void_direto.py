#!/usr/bin/env python3
"""
Teste direto e simples para identificar VOID
"""

import win32print

def test_minimal_zpl():
    """Teste com ZPL absolutamente mínimo"""
    print("🧪 Teste 1: ZPL mínimo...")
    
    printer_name = "ZDesigner ZD621R-203dpi ZPL"
    
    # ZPL mais simples possível
    minimal_zpl = """^XA
^FO100,100^A0N,50,50^FDTESTE SIMPLES^FS
^XZ"""
    
    try:
        handle = win32print.OpenPrinter(printer_name)
        doc_info = ("Test_Minimal", None, "RAW")
        job_id = win32print.StartDocPrinter(handle, 1, doc_info)
        
        win32print.StartPagePrinter(handle)
        bytes_written = win32print.WritePrinter(handle, minimal_zpl.encode('ascii'))
        win32print.EndPagePrinter(handle)
        win32print.EndDocPrinter(handle)
        win32print.ClosePrinter(handle)
        
        print(f"✅ Enviado: {bytes_written} bytes")
        return True
        
    except Exception as e:
        print(f"❌ Erro: {e}")
        return False

def test_template_original():
    """Teste com template original exatamente como no arquivo"""
    print("\n🧪 Teste 2: Template original...")
    
    printer_name = "ZDesigner ZD621R-203dpi ZPL"
    
    # Template original do arquivo modelo_zpl_larroude.prn
    original_zpl = """CT~~CD,~CC^~CT~
^XA
~TA000
~JSN
^LT0
^MNW
^MTT
^PON
^PMN
^LH0,0
^JMA
^PR4,4
~SD15
^JUS
^LRN
^CI27
^PA0,1,1,0
^RS8,,,3
^XZ
^XA
^MMT
^PW831
^LL376
^LS0
^FPH,3^FT187,147^A0N,20,23^FH\^CI28^FDSTYLE NAME:^FS^CI27
^FPH,3^FT188,176^A0N,20,23^FH\^CI28^FDVPM:^FS^CI27
^FPH,3^FT187,204^A0N,20,23^FH\^CI28^FDCOLOR:^FS^CI27
^FPH,3^FT187,234^A0N,20,23^FH\^CI28^FDSIZE:^FS^CI27
^FT737,167^BQN,2,3
^FH\^FDLA,TESTE123456^FS
^FT739,355^BQN,2,3
^FH\^FDLA,TESTE123456^FS
^FT77,355^BQN,2,3
^FH\^FDLA,TESTE123456^FS
^FO31,80^GB640,280,3^FS
^FO177,81^GB0,275,3^FS
^FT353,147^A0N,23,23^FH\^CI28^FDSANDALIA TESTE^FS^CI27
^FT353,175^A0N,23,23^FH\^CI28^FDL123-TEST-9.0-BLUE^FS^CI27
^FT353,204^A0N,23,23^FH\^CI28^FDAZUL CLARO^FS^CI27
^FT353,232^A0N,23,23^FH\^CI28^FD9.0^FS^CI27
^FT701,220^A0N,16,15^FB130,1,4,C^FH\^CI28^FDPO123^FS^CI27
^FT680,238^A0N,16,15^FB151,1,4,C^FH\^CI28^FDLocal.456^FS^CI27
^BY2,2,39^FT222,308^BEN,,Y,N
^FH\^FDL123TEST90BL^FS
^RFW,H,2,12,1^FDL123-TEST-9.0-BLUE^FS
^PQ1,0,1,Y
^XZ"""
    
    try:
        handle = win32print.OpenPrinter(printer_name)
        doc_info = ("Test_Original", None, "RAW")
        job_id = win32print.StartDocPrinter(handle, 1, doc_info)
        
        win32print.StartPagePrinter(handle)
        bytes_written = win32print.WritePrinter(handle, original_zpl.encode('ascii', errors='ignore'))
        win32print.EndPagePrinter(handle)
        win32print.EndDocPrinter(handle)
        win32print.ClosePrinter(handle)
        
        print(f"✅ Enviado: {bytes_written} bytes")
        return True
        
    except Exception as e:
        print(f"❌ Erro: {e}")
        return False

def test_without_rfid():
    """Teste sem comandos RFID"""
    print("\n🧪 Teste 3: Sem RFID...")
    
    printer_name = "ZDesigner ZD621R-203dpi ZPL"
    
    # Template sem RFID
    no_rfid_zpl = """^XA
^PW831
^LL376
^FO187,147^A0N,20,23^FDSTYLE NAME:^FS
^FO188,176^A0N,20,23^FDVPM:^FS
^FO187,204^A0N,20,23^FDCOLOR:^FS
^FO187,234^A0N,20,23^FDSIZE:^FS
^FO353,147^A0N,23,23^FDSANDALIA SEM RFID^FS
^FO353,175^A0N,23,23^FDL999-NORFID-10.0^FS
^FO353,204^A0N,23,23^FDVERDE^FS
^FO353,232^A0N,23,23^FD10.0^FS
^FO31,80^GB640,280,3^FS
^FO177,81^GB0,275,3^FS
^XZ"""
    
    try:
        handle = win32print.OpenPrinter(printer_name)
        doc_info = ("Test_No_RFID", None, "RAW")
        job_id = win32print.StartDocPrinter(handle, 1, doc_info)
        
        win32print.StartPagePrinter(handle)
        bytes_written = win32print.WritePrinter(handle, no_rfid_zpl.encode('ascii'))
        win32print.EndPagePrinter(handle)
        win32print.EndDocPrinter(handle)
        win32print.ClosePrinter(handle)
        
        print(f"✅ Enviado: {bytes_written} bytes")
        return True
        
    except Exception as e:
        print(f"❌ Erro: {e}")
        return False

def test_printer_reset():
    """Teste com reset da impressora"""
    print("\n🧪 Teste 4: Reset + ZPL simples...")
    
    printer_name = "ZDesigner ZD621R-203dpi ZPL"
    
    # Reset + ZPL simples
    reset_zpl = """~JA
^XA
^FO100,100^A0N,50,50^FDAPOS RESET^FS
^XZ"""
    
    try:
        handle = win32print.OpenPrinter(printer_name)
        doc_info = ("Test_Reset", None, "RAW")
        job_id = win32print.StartDocPrinter(handle, 1, doc_info)
        
        win32print.StartPagePrinter(handle)
        bytes_written = win32print.WritePrinter(handle, reset_zpl.encode('ascii'))
        win32print.EndPagePrinter(handle)
        win32print.EndDocPrinter(handle)
        win32print.ClosePrinter(handle)
        
        print(f"✅ Enviado: {bytes_written} bytes")
        return True
        
    except Exception as e:
        print(f"❌ Erro: {e}")
        return False

if __name__ == "__main__":
    print("=== TESTE DIRETO PARA IDENTIFICAR VOID ===")
    print("Vamos testar 4 cenários diferentes\n")
    
    tests = [
        ("ZPL Mínimo", test_minimal_zpl),
        ("Template Original", test_template_original),
        ("Sem RFID", test_without_rfid),
        ("Com Reset", test_printer_reset)
    ]
    
    results = []
    
    for name, test_func in tests:
        print(f"🚀 Executando: {name}")
        success = test_func()
        results.append((name, success))
        print(f"{'✅' if success else '❌'} {name}: {'Enviado' if success else 'Falhou'}")
        print("-" * 40)
    
    print("\n" + "="*50)
    print("📊 RESULTADOS:")
    for name, success in results:
        status = "✅ Enviado" if success else "❌ Falhou"
        print(f"   {status} - {name}")
    
    print("\n🔍 VERIFICAÇÃO:")
    print("1. Verifique qual etiqueta NÃO tem VOID")
    print("2. Isso nos dirá qual formato usar")
    print("3. Vamos ajustar o sistema com o formato correto")
