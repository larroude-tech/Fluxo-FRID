#!/usr/bin/env python3
"""
Verificação de interpretação ZPL - Zebra ZD621R
"""

import os
import subprocess
import tempfile
import time

def test_basic_zpl():
    """Testa ZPL básico para verificar se a impressora interpreta"""
    print("🧪 Testando ZPL básico...")
    
    # ZPL básico sem RFID
    basic_zpl = """^XA
^FO50,50^A0N,30,30^FDTESTE ZPL^FS
^XZ"""
    
    print(f"📄 ZPL: {basic_zpl}")
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as temp_file:
        temp_file.write(basic_zpl)
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
            print("✅ ZPL básico enviado!")
            
    except Exception as e:
        print(f"❌ Erro: {e}")
    finally:
        if os.path.exists(temp_file_path):
            os.unlink(temp_file_path)

def test_rfid_command_syntax():
    """Testa sintaxe do comando RFID"""
    print("\n🧪 Testando sintaxe do comando RFID...")
    
    # Comando RFID com sintaxe diferente
    rfid_syntax = """^XA
^FO50,50^A0N,30,30^FDRFID SYNTAX^FS
^RFW,H,2,12,1^FDTESTE^FS
^FO50,100^A0N,25,25^FDComando RFID^FS
^XZ"""
    
    print(f"📄 ZPL: {rfid_syntax}")
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as temp_file:
        temp_file.write(rfid_syntax)
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
            
    except Exception as e:
        print(f"❌ Erro: {e}")
    finally:
        if os.path.exists(temp_file_path):
            os.unlink(temp_file_path)

def test_rfid_alternative_syntax():
    """Testa sintaxe alternativa do RFID"""
    print("\n🧪 Testando sintaxe alternativa RFID...")
    
    # Sintaxe alternativa para RFID
    rfid_alt = """^XA
^FO50,50^A0N,30,30^FDRFID ALT^FS
^RFR,H,0,12,2^FS
^RFW,H,2,12,1^FDTESTE^FS
^FO50,100^A0N,25,25^FDSintaxe Alternativa^FS
^XZ"""
    
    print(f"📄 ZPL: {rfid_alt}")
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as temp_file:
        temp_file.write(rfid_alt)
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
            print("✅ Sintaxe alternativa enviada!")
            
    except Exception as e:
        print(f"❌ Erro: {e}")
    finally:
        if os.path.exists(temp_file_path):
            os.unlink(temp_file_path)

def test_raw_text():
    """Testa envio de texto puro"""
    print("\n🧪 Testando texto puro...")
    
    # Texto puro para verificar se imprime
    raw_text = "TESTE TEXTO PURO\nLINHA 2\nLINHA 3"
    
    print(f"📄 Texto: {raw_text}")
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as temp_file:
        temp_file.write(raw_text)
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
            print("✅ Texto puro enviado!")
            
    except Exception as e:
        print(f"❌ Erro: {e}")
    finally:
        if os.path.exists(temp_file_path):
            os.unlink(temp_file_path)

if __name__ == "__main__":
    print("=== Verificação ZPL ===\n")
    
    test_basic_zpl()
    time.sleep(2)
    
    test_rfid_command_syntax()
    time.sleep(2)
    
    test_rfid_alternative_syntax()
    time.sleep(2)
    
    test_raw_text()
    
    print("\n✅ Verificações concluídas!")
    print("🔍 Verifique se alguma etiqueta foi impressa")
    print("💡 Se apenas o texto puro imprimiu, o problema é com ZPL")
    print("💡 Se nada imprimiu, o problema é de comunicação")
