#!/usr/bin/env python3
"""
Teste com comando ZPL mínimo para verificar se imprime
"""

import os
import subprocess
import tempfile

def test_minimal_zpl():
    """Testa com comando ZPL mínimo"""
    print("🧪 Testando comando ZPL mínimo...")
    
    # Comando ZPL MUITO simples
    minimal_zpl = "^XA^FO50,50^A0N,30,30^FDTESTE^FS^XZ"
    
    print(f"📄 Comando ZPL: {minimal_zpl}")
    
    # Criar arquivo
    with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as temp_file:
        temp_file.write(minimal_zpl)
        temp_file_path = temp_file.name
    
    try:
        # Enviar para impressora
        printer_name = "ZDesigner ZD621R-203dpi ZPL"
        
        print(f"🖨️ Enviando para: {printer_name}")
        
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
            print("🔍 Verifique se a impressora imprimiu algo...")
        else:
            print("❌ Erro no envio")
            
    except Exception as e:
        print(f"❌ Erro: {e}")
    finally:
        if os.path.exists(temp_file_path):
            os.unlink(temp_file_path)

def test_raw_text():
    """Testa envio de texto puro"""
    print("\n🧪 Testando envio de texto puro...")
    
    # Texto puro (não ZPL)
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
            print("✅ Texto enviado com sucesso!")
            print("🔍 Verifique se a impressora imprimiu o texto...")
            
    except Exception as e:
        print(f"❌ Erro: {e}")
    finally:
        if os.path.exists(temp_file_path):
            os.unlink(temp_file_path)

def test_zpl_with_encoding():
    """Testa ZPL com diferentes codificações"""
    print("\n🧪 Testando ZPL com diferentes codificações...")
    
    # ZPL com encoding UTF-8
    zpl_utf8 = "^XA^FO50,50^A0N,30,30^FDUTF8 TEST^FS^XZ"
    
    print(f"📄 ZPL UTF-8: {zpl_utf8}")
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False, encoding='utf-8') as temp_file:
        temp_file.write(zpl_utf8)
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
            print("✅ ZPL UTF-8 enviado com sucesso!")
            
    except Exception as e:
        print(f"❌ Erro: {e}")
    finally:
        if os.path.exists(temp_file_path):
            os.unlink(temp_file_path)

if __name__ == "__main__":
    print("=== Teste de Comando ZPL Mínimo ===\n")
    
    # Teste 1: ZPL mínimo
    test_minimal_zpl()
    
    # Teste 2: Texto puro
    test_raw_text()
    
    # Teste 3: ZPL com encoding
    test_zpl_with_encoding()
    
    print("\n✅ Todos os testes concluídos!")
    print("🔍 Verifique se algum dos comandos imprimiu na impressora...")
