#!/usr/bin/env python3
"""
Teste de modo da impressora - Zebra ZD621R
"""

import os
import subprocess
import tempfile
import time

def test_zpl_mode():
    """Testa se a impressora está em modo ZPL"""
    print("🧪 Testando modo ZPL...")
    
    # Comando para forçar modo ZPL
    zpl_mode = """~JA
^XA
^FO50,50^A0N,30,30^FDZPL MODE^FS
^XZ"""
    
    print(f"📄 ZPL: {zpl_mode}")
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as temp_file:
        temp_file.write(zpl_mode)
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
            print("✅ Modo ZPL enviado!")
            
    except Exception as e:
        print(f"❌ Erro: {e}")
    finally:
        if os.path.exists(temp_file_path):
            os.unlink(temp_file_path)

def test_text_mode():
    """Testa modo de texto"""
    print("\n🧪 Testando modo texto...")
    
    # Texto simples
    text_mode = "TESTE MODO TEXTO\nLINHA 2\nLINHA 3"
    
    print(f"📄 Texto: {text_mode}")
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as temp_file:
        temp_file.write(text_mode)
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
            print("✅ Modo texto enviado!")
            
    except Exception as e:
        print(f"❌ Erro: {e}")
    finally:
        if os.path.exists(temp_file_path):
            os.unlink(temp_file_path)

def test_mixed_mode():
    """Testa modo misto"""
    print("\n🧪 Testando modo misto...")
    
    # Mistura de texto e ZPL
    mixed_mode = """TESTE MISTO
^XA
^FO50,50^A0N,30,30^FDMISTO^FS
^XZ
FIM TESTE"""
    
    print(f"📄 Conteúdo: {mixed_mode}")
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as temp_file:
        temp_file.write(mixed_mode)
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
            print("✅ Modo misto enviado!")
            
    except Exception as e:
        print(f"❌ Erro: {e}")
    finally:
        if os.path.exists(temp_file_path):
            os.unlink(temp_file_path)

def test_printer_commands():
    """Testa comandos específicos da impressora"""
    print("\n🧪 Testando comandos da impressora...")
    
    # Comandos específicos da Zebra
    printer_commands = [
        "~HS",  # Host Status
        "~JA",  # Job Status
        "~HI",  # Host Information
    ]
    
    for cmd in printer_commands:
        print(f"📄 Comando: {cmd}")
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as temp_file:
            temp_file.write(cmd)
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
            
            if result.returncode == 0:
                print("✅ Comando enviado!")
                
        except Exception as e:
            print(f"❌ Erro: {e}")
        finally:
            if os.path.exists(temp_file_path):
                os.unlink(temp_file_path)
        
        time.sleep(1)

if __name__ == "__main__":
    print("=== Teste de Modo da Impressora ===\n")
    
    test_zpl_mode()
    time.sleep(2)
    
    test_text_mode()
    time.sleep(2)
    
    test_mixed_mode()
    time.sleep(2)
    
    test_printer_commands()
    
    print("\n✅ Testes de modo concluídos!")
    print("🔍 Verifique qual modo funcionou")
    print("💡 Se apenas texto funcionou, a impressora não está em modo ZPL")
    print("💡 Se ZPL funcionou, o problema pode ser com comandos RFID específicos")
