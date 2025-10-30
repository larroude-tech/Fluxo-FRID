#!/usr/bin/env python3
"""
Teste de impressão centralizada para etiqueta 100mm x 37mm
Zebra ZD621R
"""

import os
import subprocess
import tempfile
import time
import win32print

def test_centered_label():
    """Testa impressão centralizada na etiqueta 100mm x 37mm"""
    print("🧪 Testando impressão centralizada (100mm x 37mm)...")
    
    # Dimensões da etiqueta em dots (203 DPI)
    # 100mm = 100 * 203 / 25.4 = ~800 dots
    # 37mm = 37 * 203 / 25.4 = ~296 dots
    
    width_dots = 800
    height_dots = 296
    
    # Centralizar horizontalmente (800 - largura do texto) / 2
    # Centralizar verticalmente (296 - altura do texto) / 2
    
    # ZPL com informações centralizadas
    zpl = f"""^XA
^PW{width_dots}
^LL{height_dots}
^FO{width_dots//2 - 150},50^A0N,50,50^FDMUPA_TESTE_01^FS
^FO{width_dots//2 - 100},120^A0N,30,30^FDTeste RFID^FS
^FO{width_dots//2 - 80},160^A0N,25,25^FDData: {time.strftime('%d/%m/%Y %H:%M:%S')}^FS
^FO{width_dots//2 - 120},200^BY3^BCN,100,Y,N,N^FDMUPA_TESTE_01^FS
^FO{width_dots//2 - 80},250^A0N,20,20^FD[TESTE CENTRALIZADO]^FS
^XZ"""
    
    print(f"📄 ZPL centralizado: {zpl}")
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as temp_file:
        temp_file.write(zpl)
        temp_file_path = temp_file.name
    
    try:
        printer_name = "ZDesigner ZD621R-203dpi ZPL"
        
        result = subprocess.run(
            ['copy', temp_file_path, printer_name],
            capture_output=True,
            text=True,
            shell=True
        )
        
        print(f"📊 Resultado: {result.returncode}")
        print(f"📊 Saída: {result.stdout}")
        
        if result.returncode == 0:
            print("✅ Etiqueta centralizada enviada!")
            
    except Exception as e:
        print(f"❌ Erro: {e}")
    finally:
        if os.path.exists(temp_file_path):
            os.unlink(temp_file_path)

def test_centered_rfid():
    """Testa impressão + RFID centralizado"""
    print("\n🧪 Testando impressão + RFID centralizado...")
    
    width_dots = 800
    height_dots = 296
    
    # ZPL combinado: imprimir etiqueta + gravar RFID (formato simples)
    zpl = f"""^XA
^PW{width_dots}
^LL{height_dots}
^RU
^RFW,H^FDMUPA_TESTE_01^FS
^FO{width_dots//2 - 150},50^A0N,50,50^FDMUPA_TESTE_01^FS
^FO{width_dots//2 - 100},120^A0N,30,30^FDTeste RFID^FS
^FO{width_dots//2 - 80},160^A0N,25,25^FDData: {time.strftime('%d/%m/%Y %H:%M:%S')}^FS
^FO{width_dots//2 - 120},200^BY3^BCN,100,Y,N,N^FDMUPA_TESTE_01^FS
^FO{width_dots//2 - 80},250^A0N,20,20^FD[TESTE RFID SIMPLES]^FS
^XZ"""
    
    print(f"📄 ZPL RFID centralizado: {zpl}")
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as temp_file:
        temp_file.write(zpl)
        temp_file_path = temp_file.name
    
    try:
        printer_name = "ZDesigner ZD621R-203dpi ZPL"
        
        result = subprocess.run(
            ['copy', temp_file_path, printer_name],
            capture_output=True,
            text=True,
            shell=True
        )
        
        print(f"📊 Resultado: {result.returncode}")
        print(f"📊 Saída: {result.stdout}")
        
        if result.returncode == 0:
            print("✅ Etiqueta + RFID centralizado enviado!")
            
    except Exception as e:
        print(f"❌ Erro: {e}")
    finally:
        if os.path.exists(temp_file_path):
            os.unlink(temp_file_path)

def test_simple_centered():
    """Testa impressão simples centralizada"""
    print("\n🧪 Testando impressão simples centralizada...")
    
    width_dots = 800
    height_dots = 296
    
    # ZPL simples centralizado
    zpl = f"""^XA
^PW{width_dots}
^LL{height_dots}
^FO{width_dots//2 - 100},{height_dots//2 - 25}^A0N,50,50^FDMUPA_TESTE_01^FS
^FO{width_dots//2 - 80},{height_dots//2 + 50}^A0N,20,20^FD[TESTE SIMPLES]^FS
^XZ"""
    
    print(f"📄 ZPL simples centralizado: {zpl}")
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as temp_file:
        temp_file.write(zpl)
        temp_file_path = temp_file.name
    
    try:
        printer_name = "ZDesigner ZD621R-203dpi ZPL"
        
        result = subprocess.run(
            ['copy', temp_file_path, printer_name],
            capture_output=True,
            text=True,
            shell=True
        )
        
        print(f"📊 Resultado: {result.returncode}")
        print(f"📊 Saída: {result.stdout}")
        
        if result.returncode == 0:
            print("✅ Impressão simples centralizada enviada!")
            
    except Exception as e:
        print(f"❌ Erro: {e}")
    finally:
        if os.path.exists(temp_file_path):
            os.unlink(temp_file_path)

def test_centered_with_barcode():
    """Testa impressão com código de barras centralizado"""
    print("\n🧪 Testando impressão com código de barras centralizado...")
    
    width_dots = 800
    height_dots = 296
    
    # ZPL com código de barras centralizado
    zpl = f"""^XA
^PW{width_dots}
^LL{height_dots}
^FO{width_dots//2 - 150},50^A0N,40,40^FDMUPA_TESTE_01^FS
^FO{width_dots//2 - 120},100^BY3^BCN,80,Y,N,N^FDMUPA_TESTE_01^FS
^FO{width_dots//2 - 60},190^A0N,25,25^FD{time.strftime('%d/%m/%Y')}^FS
^FO{width_dots//2 - 80},220^A0N,20,20^FD[TESTE CODIGO BARRAS]^FS
^XZ"""
    
    print(f"📄 ZPL com código de barras centralizado: {zpl}")
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as temp_file:
        temp_file.write(zpl)
        temp_file_path = temp_file.name
    
    try:
        printer_name = "ZDesigner ZD621R-203dpi ZPL"
        
        result = subprocess.run(
            ['copy', temp_file_path, printer_name],
            capture_output=True,
            text=True,
            shell=True
        )
        
        print(f"📊 Resultado: {result.returncode}")
        print(f"📊 Saída: {result.stdout}")
        
        if result.returncode == 0:
            print("✅ Impressão com código de barras centralizado enviada!")
            
    except Exception as e:
        print(f"❌ Erro: {e}")
    finally:
        if os.path.exists(temp_file_path):
            os.unlink(temp_file_path)

def test_rfid_simple_format():
    """Testa formato simples de RFID conforme fornecido pelo usuário"""
    print("\n🧪 Testando formato simples de RFID...")
    
    # Formato simples de RFID conforme fornecido
    simple_rfid_zpl = """^XA
^RU
^RFW,H^FD313233343536373839303132^FS
^FO40,40^A0N,36,36^FDProduto: JASMINI HI MULE^FS
^FO40,90^A0N,28,28^FDEPC (hex): 313233343536373839303132^FS
^FO40,140^BY2
^BCN,90,Y,N,N
^FD>L458JASM110SILV1885^FS
^XZ"""
    
    print(f"📄 ZPL formato simples: {simple_rfid_zpl}")
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as temp_file:
        temp_file.write(simple_rfid_zpl)
        temp_file_path = temp_file.name
    
    try:
        printer_name = "ZDesigner ZD621R-203dpi ZPL"
        
        result = subprocess.run(
            ['copy', temp_file_path, printer_name],
            capture_output=True,
            text=True,
            shell=True
        )
        
        print(f"📊 Resultado: {result.returncode}")
        print(f"📊 Saída: {result.stdout}")
        
        if result.returncode == 0:
            print("✅ Formato simples RFID enviado!")
            print("🔍 Verifique se a etiqueta foi impressa e o RFID gravado")
            
    except Exception as e:
        print(f"❌ Erro: {e}")
    finally:
        if os.path.exists(temp_file_path):
            os.unlink(temp_file_path)

def test_rfid_simple_mupa():
    """Testa formato simples de RFID com dados MUPA"""
    print("\n🧪 Testando formato simples RFID com MUPA...")
    
    # Formato simples com dados MUPA
    mupa_simple_zpl = """^XA
^RU
^RFW,H^FDMUPA_TESTE_01^FS
^FO40,40^A0N,36,36^FDProduto: MUPA TESTE 01^FS
^FO40,90^A0N,28,28^FDEPC: MUPA_TESTE_01^FS
^FO40,140^BY2
^BCN,90,Y,N,N
^FDMUPA_TESTE_01^FS
^FO40,200^A0N,25,25^FD[FORMATO SIMPLES]^FS
^XZ"""
    
    print(f"📄 ZPL MUPA simples: {mupa_simple_zpl}")
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as temp_file:
        temp_file.write(mupa_simple_zpl)
        temp_file_path = temp_file.name
    
    try:
        printer_name = "ZDesigner ZD621R-203dpi ZPL"
        
        result = subprocess.run(
            ['copy', temp_file_path, printer_name],
            capture_output=True,
            text=True,
            shell=True
        )
        
        print(f"📊 Resultado: {result.returncode}")
        print(f"📊 Saída: {result.stdout}")
        
        if result.returncode == 0:
            print("✅ Formato simples MUPA enviado!")
            print("🔍 Verifique se a etiqueta foi impressa e o RFID gravado")
            
    except Exception as e:
        print(f"❌ Erro: {e}")
    finally:
        if os.path.exists(temp_file_path):
            os.unlink(temp_file_path)

def test_centered_via_win32print():
    """Testa impressão centralizada via win32print"""
    print("\n🧪 Testando impressão centralizada via win32print...")
    
    try:
        printer_name = "ZDesigner ZD621R-203dpi ZPL"
        handle = win32print.OpenPrinter(printer_name)
        
        width_dots = 800
        height_dots = 296
        
        # ZPL centralizado
        zpl_data = f"""^XA
^PW{width_dots}
^LL{height_dots}
^FO{width_dots//2 - 100},{height_dots//2 - 25}^A0N,50,50^FDMUPA_TESTE_01^FS
^FO{width_dots//2 - 80},{height_dots//2 + 50}^A0N,20,20^FD[TESTE WIN32PRINT]^FS
^XZ"""
        
        print(f"📄 Enviando ZPL centralizado: {zpl_data}")
        
        # Iniciar documento
        doc_info = ("Teste Centralizado", None, "RAW")
        job_id = win32print.StartDocPrinter(handle, 1, doc_info)
        
        # Iniciar página
        win32print.StartPagePrinter(handle)
        
        # Enviar dados
        win32print.WritePrinter(handle, zpl_data.encode('ascii'))
        
        # Finalizar página
        win32print.EndPagePrinter(handle)
        
        # Finalizar documento
        win32print.EndDocPrinter(handle)
        
        print(f"✅ ZPL centralizado via win32print enviado com ID: {job_id}")
        
        win32print.ClosePrinter(handle)
        
    except Exception as e:
        print(f"❌ Erro: {e}")

def main():
    """Função principal"""
    print("=== Teste de Impressão Centralizada - Etiqueta 100mm x 37mm ===\n")
    
    print("📏 Dimensões da etiqueta:")
    print("   - Largura: 100mm (~800 dots em 203 DPI)")
    print("   - Altura: 37mm (~296 dots em 203 DPI)")
    print("   - DPI: 203")
    print()
    
    # Teste 1: Impressão centralizada
    test_centered_label()
    time.sleep(2)
    
    # Teste 2: Impressão + RFID centralizado
    test_centered_rfid()
    time.sleep(2)
    
    # Teste 3: Impressão simples centralizada
    test_simple_centered()
    time.sleep(2)
    
    # Teste 4: Impressão com código de barras centralizado
    test_centered_with_barcode()
    time.sleep(2)
    
    # Teste 5: Formato simples de RFID (conforme fornecido)
    test_rfid_simple_format()
    time.sleep(2)
    
    # Teste 6: Formato simples RFID com MUPA
    test_rfid_simple_mupa()
    time.sleep(2)
    
    # Teste 7: Impressão centralizada via win32print
    test_centered_via_win32print()
    
    print("\n✅ Todos os testes de impressão centralizada concluídos!")
    print("🔍 Verifique se as informações aparecem centralizadas na etiqueta...")
    print("💡 Se ainda não imprimiu, verifique:")
    print("   - Se há papel na impressora")
    print("   - Se a impressora está ligada")
    print("   - Se há algum erro na tela da impressora")

if __name__ == "__main__":
    main()
