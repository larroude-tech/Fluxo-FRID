#!/usr/bin/env python3
"""
Teste de impressão forçada e comandos específicos para Zebra ZD621R
"""

import os
import subprocess
import tempfile
import time

def test_force_print_commands():
    """Testa comandos de impressão forçada"""
    print("🧪 Testando comandos de impressão forçada...")
    
    # Comandos de impressão forçada
    force_commands = [
        "^XA^FO50,50^A0N,30,30^FDFORCE PRINT^FS^XZ^FF",  # Form Feed
        "^XA^FO50,50^A0N,30,30^FDFORCE PRINT^FS^XZ^CI28",  # Clear Image Buffer
        "^XA^FO50,50^A0N,30,30^FDFORCE PRINT^FS^XZ^CI28^FF",  # Clear + Form Feed
        "^XA^FO50,50^A0N,30,30^FDFORCE PRINT^FS^XZ^CI28^XA^XZ",  # Clear + New Label
    ]
    
    for i, cmd in enumerate(force_commands, 1):
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
                print("✅ Comando de impressão forçada enviado!")
                
        except Exception as e:
            print(f"❌ Erro: {e}")
        finally:
            if os.path.exists(temp_file_path):
                os.unlink(temp_file_path)
        
        print("⏳ Aguardando 5 segundos...")
        time.sleep(5)

def test_print_mode_commands():
    """Testa diferentes modos de impressão"""
    print("\n🧪 Testando diferentes modos de impressão...")
    
    # Modos de impressão
    print_modes = [
        "^XA^MMD^XZ",  # Direct Mode
        "^XA^MMT^XZ",  # Tear Off Mode
        "^XA^MMC^XZ",  # Cutter Mode
        "^XA^MMP^XZ",  # Peel Off Mode
        "^XA^MMR^XZ",  # Rewind Mode
        "^XA^MMK^XZ",  # Keep Back Mode
    ]
    
    for mode in print_modes:
        print(f"📄 Configurando modo: {mode}")
        
        # Configurar modo
        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as temp_file:
            temp_file.write(mode)
            temp_file_path = temp_file.name
        
        try:
            printer_name = "ZDesigner ZD621R-203dpi ZPL"
            
            result = subprocess.run(
                ['copy', temp_file_path, printer_name],
                capture_output=True,
                text=True,
                shell=True
            )
            
            if result.returncode == 0:
                print("✅ Modo configurado!")
                
                # Tentar imprimir após configurar modo
                print_zpl = "^XA^FO50,50^A0N,30,30^FDMODE TEST^FS^XZ"
                
                with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as print_file:
                    print_file.write(print_zpl)
                    print_file_path = print_file.name
                
                try:
                    result2 = subprocess.run(
                        ['copy', print_file_path, printer_name],
                        capture_output=True,
                        text=True,
                        shell=True
                    )
                    
                    if result2.returncode == 0:
                        print("✅ Impressão tentada após configurar modo!")
                        
                except Exception as e:
                    print(f"❌ Erro na impressão: {e}")
                finally:
                    if os.path.exists(print_file_path):
                        os.unlink(print_file_path)
                
        except Exception as e:
            print(f"❌ Erro: {e}")
        finally:
            if os.path.exists(temp_file_path):
                os.unlink(temp_file_path)
        
        print("⏳ Aguardando 3 segundos...")
        time.sleep(3)

def test_zpl_with_form_feed():
    """Testa ZPL com form feed explícito"""
    print("\n🧪 Testando ZPL com form feed explícito...")
    
    # ZPL com form feed
    zpl_with_ff = """^XA
^FO50,50^A0N,30,30^FDFORM FEED TEST^FS
^XZ
^FF"""
    
    print(f"📄 ZPL com form feed: {zpl_with_ff}")
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as temp_file:
        temp_file.write(zpl_with_ff)
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
            print("✅ ZPL com form feed enviado!")
            
    except Exception as e:
        print(f"❌ Erro: {e}")
    finally:
        if os.path.exists(temp_file_path):
            os.unlink(temp_file_path)

def test_zpl_with_clear_buffer():
    """Testa ZPL com clear buffer"""
    print("\n🧪 Testando ZPL com clear buffer...")
    
    # ZPL com clear buffer
    zpl_with_clear = """^XA
^FO50,50^A0N,30,30^FDCLEAR BUFFER TEST^FS
^XZ
^CI28"""
    
    print(f"📄 ZPL com clear buffer: {zpl_with_clear}")
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as temp_file:
        temp_file.write(zpl_with_clear)
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
            print("✅ ZPL com clear buffer enviado!")
            
    except Exception as e:
        print(f"❌ Erro: {e}")
    finally:
        if os.path.exists(temp_file_path):
            os.unlink(temp_file_path)

def test_zpl_sequence():
    """Testa sequência completa de ZPL"""
    print("\n🧪 Testando sequência completa de ZPL...")
    
    # Sequência completa
    sequence = [
        "~HS",  # Host Status
        "^XA^MMD^XZ",  # Set Direct Mode
        "^XA^FO50,50^A0N,30,30^FDSEQUENCE TEST^FS^XZ",  # Print
        "^FF",  # Form Feed
        "~JA"   # Job Status
    ]
    
    for i, cmd in enumerate(sequence, 1):
        print(f"📄 Sequência {i}: {cmd}")
        
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
                print("✅ Comando da sequência enviado!")
                
        except Exception as e:
            print(f"❌ Erro: {e}")
        finally:
            if os.path.exists(temp_file_path):
                os.unlink(temp_file_path)
        
        print("⏳ Aguardando 2 segundos...")
        time.sleep(2)

if __name__ == "__main__":
    print("=== Teste de Impressão Forçada - Zebra ZD621R ===\n")
    
    # Teste 1: Comandos de impressão forçada
    test_force_print_commands()
    
    # Teste 2: Modos de impressão
    test_print_mode_commands()
    
    # Teste 3: Form feed
    test_zpl_with_form_feed()
    
    # Teste 4: Clear buffer
    test_zpl_with_clear_buffer()
    
    # Teste 5: Sequência completa
    test_zpl_sequence()
    
    print("\n✅ Todos os testes de impressão forçada concluídos!")
    print("🔍 Verifique se algum comando fez a impressora imprimir...")
    print("💡 Se ainda não imprimiu, pode ser necessário verificar as configurações do driver!")
