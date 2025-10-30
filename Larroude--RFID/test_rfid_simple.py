#!/usr/bin/env python3
"""
Teste simples de RFID - Zebra ZD621R
"""

import os
import subprocess
import tempfile
import time

def test_simple_rfid_write():
    """Teste simples de gravação RFID"""
    print("🧪 Teste simples de gravação RFID...")
    
    # Comando RFID mais simples possível
    simple_rfid = """^XA
^RFW,H,2,12,1^FDTESTE^FS
^XZ"""
    
    print(f"📄 ZPL: {simple_rfid}")
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as temp_file:
        temp_file.write(simple_rfid)
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
            print("✅ Comando RFID enviado!")
            print("🔍 Verifique se a etiqueta foi impressa")
            
    except Exception as e:
        print(f"❌ Erro: {e}")
    finally:
        if os.path.exists(temp_file_path):
            os.unlink(temp_file_path)

def test_rfid_with_text():
    """Teste RFID com texto visível"""
    print("\n🧪 Teste RFID com texto visível...")
    
    # RFID com texto para verificar se imprime
    rfid_with_text = """^XA
^FO50,50^A0N,30,30^FDRFID TEST^FS
^RFW,H,2,12,1^FDTESTE^FS
^XZ"""
    
    print(f"📄 ZPL: {rfid_with_text}")
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as temp_file:
        temp_file.write(rfid_with_text)
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
            print("✅ RFID com texto enviado!")
            print("🔍 Verifique se o texto foi impresso")
            
    except Exception as e:
        print(f"❌ Erro: {e}")
    finally:
        if os.path.exists(temp_file_path):
            os.unlink(temp_file_path)

def test_rfid_read():
    """Teste de leitura RFID"""
    print("\n🧪 Teste de leitura RFID...")
    
    # Comando de leitura RFID
    rfid_read = """^XA
^RFR,H,0,12,2^FS
^XZ"""
    
    print(f"📄 ZPL: {rfid_read}")
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as temp_file:
        temp_file.write(rfid_read)
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
            print("✅ Comando de leitura enviado!")
            
    except Exception as e:
        print(f"❌ Erro: {e}")
    finally:
        if os.path.exists(temp_file_path):
            os.unlink(temp_file_path)

if __name__ == "__main__":
    print("=== Teste Simples RFID ===\n")
    
    test_simple_rfid_write()
    time.sleep(2)
    
    test_rfid_with_text()
    time.sleep(2)
    
    test_rfid_read()
    
    print("\n✅ Testes concluídos!")
    print("🔍 Verifique se alguma etiqueta foi impressa")
