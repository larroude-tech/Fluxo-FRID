#!/usr/bin/env python3
"""
Teste de conexão simples e direta com a impressora Zebra ZD621R
"""

import os
import sys
import time
import subprocess
import win32print
import tempfile

def test_direct_copy():
    """Testa envio direto via comando copy"""
    print("🧪 Testando envio direto via copy...")
    
    # Comando ZPL muito simples
    simple_zpl = """^XA
^FO50,50^A0N,30,30^FDHELLO^FS
^XZ"""
    
    # Criar arquivo temporário
    with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as temp_file:
        temp_file.write(simple_zpl)
        temp_file_path = temp_file.name
    
    print(f"📄 Arquivo criado: {temp_file_path}")
    print(f"📄 Conteúdo: {simple_zpl}")
    
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
        print(f"📊 Erro: {result.stderr}")
        
        if result.returncode == 0:
            print("✅ Comando copy executado com sucesso!")
        else:
            print("❌ Erro no comando copy")
            
    except Exception as e:
        print(f"❌ Erro: {e}")
    finally:
        # Limpar arquivo
        if os.path.exists(temp_file_path):
            os.unlink(temp_file_path)
            print(f"🗑️ Arquivo removido: {temp_file_path}")

def test_win32print():
    """Testa envio via win32print"""
    print("\n🧪 Testando envio via win32print...")
    
    try:
        printer_name = "ZDesigner ZD621R-203dpi ZPL"
        
        # Abrir impressora
        handle = win32print.OpenPrinter(printer_name)
        print(f"✅ Impressora aberta: {printer_name}")
        
        # Comando ZPL simples
        simple_zpl = """^XA
^FO50,50^A0N,30,30^FDWIN32PRINT^FS
^XZ"""
        
        # Enviar dados
        win32print.StartDocPrinter(handle, 1, ("Teste", None, "RAW"))
        win32print.StartPagePrinter(handle)
        win32print.WritePrinter(handle, simple_zpl.encode('utf-8'))
        win32print.EndPagePrinter(handle)
        win32print.EndDocPrinter(handle)
        win32print.ClosePrinter(handle)
        
        print("✅ Dados enviados via win32print!")
        
    except Exception as e:
        print(f"❌ Erro win32print: {e}")

def test_printer_status():
    """Verifica status detalhado da impressora"""
    print("\n📊 Verificando status detalhado da impressora...")
    
    try:
        printer_name = "ZDesigner ZD621R-203dpi ZPL"
        handle = win32print.OpenPrinter(printer_name)
        
        # Obter informações detalhadas
        info = win32print.GetPrinter(handle, 2)
        
        print(f"📋 Nome: {info['pPrinterName']}")
        print(f"📋 Porta: {info['pPortName']}")
        print(f"📋 Driver: {info['pDriverName']}")
        print(f"📋 Status: {info['Status']}")
        print(f"📋 Attributes: {info['Attributes']}")
        print(f"📋 Priority: {info['Priority']}")
        print(f"📋 DefaultPriority: {info['DefaultPriority']}")
        
        # Verificar se está pronto
        if info['Status'] == 0:
            print("✅ Impressora está PRONTA")
        else:
            print(f"⚠️ Impressora com status: {info['Status']}")
            
        win32print.ClosePrinter(handle)
        
    except Exception as e:
        print(f"❌ Erro ao verificar status: {e}")

def test_multiple_methods():
    """Testa múltiplos métodos de envio"""
    print("\n🚀 Testando múltiplos métodos de envio...")
    
    # Método 1: Copy direto
    print("\n1️⃣ Método 1: Copy direto")
    test_direct_copy()
    
    # Método 2: Win32print
    print("\n2️⃣ Método 2: Win32print")
    test_win32print()
    
    # Método 3: Echo + copy
    print("\n3️⃣ Método 3: Echo + copy")
    try:
        result = subprocess.run(
            ['echo', '^XA^FO50,50^A0N,30,30^FDECHO^FS^XZ', '|', 'copy', '/', 'ZDesigner ZD621R-203dpi ZPL'],
            capture_output=True,
            text=True,
            shell=True
        )
        print(f"📊 Resultado echo: {result.returncode}")
    except Exception as e:
        print(f"❌ Erro echo: {e}")

if __name__ == "__main__":
    print("=== Teste de Conexão Simples - Zebra ZD621R ===\n")
    
    # Verificar status
    test_printer_status()
    
    # Testar múltiplos métodos
    test_multiple_methods()
    
    print("\n✅ Testes concluídos!")
