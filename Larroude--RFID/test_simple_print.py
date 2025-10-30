#!/usr/bin/env python3
"""
Teste Simples de Impressão - Zebra ZD621R
"""

import subprocess
import tempfile
import os

def test_simple_print():
    """Testa impressão simples"""
    print("=== Teste Simples de Impressão ===\n")
    
    # ZPL muito simples
    zpl = """^XA
^FO50,50^A0N,30,30^FDTESTE SIMPLES^FS
^FO50,100^A0N,25,25^FD21/08/2025^FS
^XZ"""
    
    print(f"📄 ZPL: {zpl}")
    
    # Criar arquivo temporário
    with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as temp_file:
        temp_file.write(zpl)
        temp_file_path = temp_file.name
    
    try:
        printer_name = "ZDesigner ZD621R-203dpi ZPL"
        
        print(f"🖨️ Enviando para impressora: {printer_name}")
        
        result = subprocess.run(
            ['copy', temp_file_path, printer_name],
            capture_output=True,
            text=True,
            shell=True
        )
        
        print(f"📊 Resultado: {result.returncode}")
        print(f"📊 Saída: {result.stdout}")
        
        if result.returncode == 0:
            print("✅ Comando enviado com sucesso!")
        else:
            print(f"❌ Erro: {result.stderr}")
            
    except Exception as e:
        print(f"❌ Erro: {e}")
    finally:
        if os.path.exists(temp_file_path):
            os.unlink(temp_file_path)

def test_raw_text():
    """Testa envio de texto simples"""
    print("\n=== Teste de Texto Simples ===\n")
    
    text = "TESTE TEXTO SIMPLES\n21/08/2025\n"
    
    print(f"📄 Texto: {text}")
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as temp_file:
        temp_file.write(text)
        temp_file_path = temp_file.name
    
    try:
        printer_name = "ZDesigner ZD621R-203dpi ZPL"
        
        print(f"🖨️ Enviando texto para: {printer_name}")
        
        result = subprocess.run(
            ['copy', temp_file_path, printer_name],
            capture_output=True,
            text=True,
            shell=True
        )
        
        print(f"📊 Resultado: {result.returncode}")
        print(f"📊 Saída: {result.stdout}")
        
        if result.returncode == 0:
            print("✅ Texto enviado com sucesso!")
        else:
            print(f"❌ Erro: {result.stderr}")
            
    except Exception as e:
        print(f"❌ Erro: {e}")
    finally:
        if os.path.exists(temp_file_path):
            os.unlink(temp_file_path)

if __name__ == "__main__":
    test_simple_print()
    test_raw_text()
    
    print("\n🔍 Verifique se:")
    print("1. A impressora está ligada")
    print("2. Há papel na impressora")
    print("3. A porta está fechada")
    print("4. Não há erros na tela da impressora")
    print("5. A impressora não está em PAUSE")
