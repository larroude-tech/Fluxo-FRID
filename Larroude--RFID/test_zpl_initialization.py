#!/usr/bin/env python3
"""
Teste de inicialização e configuração ZPL para Zebra ZD621R
"""

import os
import subprocess
import tempfile
import time

def test_zpl_initialization():
    """Testa comandos de inicialização ZPL"""
    print("🧪 Testando inicialização ZPL...")
    
    # Comando de inicialização ZPL
    init_zpl = """~HS
~JA
^XA
^FO50,50^A0N,30,30^FDINIT TEST^FS
^XZ"""
    
    print(f"📄 Comando de inicialização: {init_zpl}")
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as temp_file:
        temp_file.write(init_zpl)
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
            print("✅ Inicialização enviada!")
            
    except Exception as e:
        print(f"❌ Erro: {e}")
    finally:
        if os.path.exists(temp_file_path):
            os.unlink(temp_file_path)

def test_zpl_with_crlf():
    """Testa ZPL com quebras de linha CR+LF"""
    print("\n🧪 Testando ZPL com CR+LF...")
    
    # ZPL com quebras de linha explícitas
    zpl_crlf = "^XA\r\n^FO50,50^A0N,30,30^FDCRLF TEST^FS\r\n^XZ\r\n"
    
    print(f"📄 ZPL com CR+LF: {repr(zpl_crlf)}")
    
    with tempfile.NamedTemporaryFile(mode='wb', suffix='.txt', delete=False) as temp_file:
        temp_file.write(zpl_crlf.encode('ascii'))
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
            print("✅ ZPL CR+LF enviado!")
            
    except Exception as e:
        print(f"❌ Erro: {e}")
    finally:
        if os.path.exists(temp_file_path):
            os.unlink(temp_file_path)

def test_zpl_status_commands():
    """Testa comandos de status ZPL"""
    print("\n🧪 Testando comandos de status ZPL...")
    
    # Comandos de status
    status_commands = [
        "~HS",  # Host Status
        "~JA",  # Print Job Status
        "~HI",  # Host Information
        "~HS~JA~HI"  # Todos os status
    ]
    
    for cmd in status_commands:
        print(f"📄 Enviando comando: {cmd}")
        
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
                print("✅ Comando de status enviado!")
                
        except Exception as e:
            print(f"❌ Erro: {e}")
        finally:
            if os.path.exists(temp_file_path):
                os.unlink(temp_file_path)
        
        time.sleep(1)  # Aguardar entre comandos

def test_zpl_configuration():
    """Testa comandos de configuração ZPL"""
    print("\n🧪 Testando comandos de configuração ZPL...")
    
    # Comandos de configuração
    config_commands = [
        "^XA^MMD^XZ",  # Set Print Mode to Direct
        "^XA^MMT^XZ",  # Set Print Mode to Tear Off
        "^XA^MMC^XZ",  # Set Print Mode to Cutter
        "^XA^MMP^XZ",  # Set Print Mode to Peel Off
        "^XA^MMR^XZ"   # Set Print Mode to Rewind
    ]
    
    for cmd in config_commands:
        print(f"📄 Enviando configuração: {cmd}")
        
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
                print("✅ Configuração enviada!")
                
        except Exception as e:
            print(f"❌ Erro: {e}")
        finally:
            if os.path.exists(temp_file_path):
                os.unlink(temp_file_path)
        
        time.sleep(1)  # Aguardar entre comandos

def test_zpl_with_delay():
    """Testa ZPL com delay entre comandos"""
    print("\n🧪 Testando ZPL com delay...")
    
    # Sequência de comandos com delay
    commands = [
        "~HS",  # Status
        "^XA^FO50,50^A0N,30,30^FDDELAY TEST^FS^XZ",  # Print
        "~JA"   # Job Status
    ]
    
    for i, cmd in enumerate(commands, 1):
        print(f"📄 Comando {i}: {cmd}")
        
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
        
        print("⏳ Aguardando 3 segundos...")
        time.sleep(3)  # Delay entre comandos

if __name__ == "__main__":
    print("=== Teste de Inicialização ZPL - Zebra ZD621R ===\n")
    
    # Teste 1: Inicialização
    test_zpl_initialization()
    
    # Teste 2: CR+LF
    test_zpl_with_crlf()
    
    # Teste 3: Comandos de status
    test_zpl_status_commands()
    
    # Teste 4: Configurações
    test_zpl_configuration()
    
    # Teste 5: Com delay
    test_zpl_with_delay()
    
    print("\n✅ Todos os testes de inicialização concluídos!")
    print("🔍 Verifique se algum comando fez a impressora imprimir...")
