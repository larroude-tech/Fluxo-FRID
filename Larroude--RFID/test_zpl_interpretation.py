#!/usr/bin/env python3
"""
Teste de interpretação ZPL para Zebra ZD621R
Verificando diferentes formatos e comandos
"""

import os
import subprocess
import tempfile
import time
import win32print

def test_basic_zpl():
    """Testa ZPL básico"""
    print("🧪 Testando ZPL básico...")
    
    zpl = "^XA^FO50,50^A0N,30,30^FDBASIC TEST^FS^XZ"
    
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
        
        if result.returncode == 0:
            print("✅ ZPL básico enviado!")
            
    except Exception as e:
        print(f"❌ Erro: {e}")
    finally:
        if os.path.exists(temp_file_path):
            os.unlink(temp_file_path)

def test_zpl_with_crlf():
    """Testa ZPL com quebras de linha CR+LF"""
    print("\n🧪 Testando ZPL com CR+LF...")
    
    zpl = "^XA\r\n^FO50,50^A0N,30,30^FDCRLF TEST^FS\r\n^XZ\r\n"
    
    with tempfile.NamedTemporaryFile(mode='wb', suffix='.txt', delete=False) as temp_file:
        temp_file.write(zpl.encode('ascii'))
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
            print("✅ ZPL com CR+LF enviado!")
            
    except Exception as e:
        print(f"❌ Erro: {e}")
    finally:
        if os.path.exists(temp_file_path):
            os.unlink(temp_file_path)

def test_zpl_with_lf():
    """Testa ZPL com quebras de linha LF"""
    print("\n🧪 Testando ZPL com LF...")
    
    zpl = "^XA\n^FO50,50^A0N,30,30^FDLF TEST^FS\n^XZ\n"
    
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
        
        if result.returncode == 0:
            print("✅ ZPL com LF enviado!")
            
    except Exception as e:
        print(f"❌ Erro: {e}")
    finally:
        if os.path.exists(temp_file_path):
            os.unlink(temp_file_path)

def test_zpl_with_spaces():
    """Testa ZPL com espaços extras"""
    print("\n🧪 Testando ZPL com espaços...")
    
    zpl = "  ^XA  \n  ^FO50,50^A0N,30,30^FDSPACES TEST^FS  \n  ^XZ  \n"
    
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
        
        if result.returncode == 0:
            print("✅ ZPL com espaços enviado!")
            
    except Exception as e:
        print(f"❌ Erro: {e}")
    finally:
        if os.path.exists(temp_file_path):
            os.unlink(temp_file_path)

def test_zpl_with_encoding():
    """Testa ZPL com diferentes codificações"""
    print("\n🧪 Testando ZPL com diferentes codificações...")
    
    encodings = ['ascii', 'utf-8', 'cp437', 'iso-8859-1']
    
    for encoding in encodings:
        print(f"📄 Testando encoding: {encoding}")
        
        zpl = f"^XA^FO50,50^A0N,30,30^FD{encoding.upper()} TEST^FS^XZ"
        
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
            
            if result.returncode == 0:
                print("✅ ZPL enviado!")
                
        except Exception as e:
            print(f"❌ Erro: {e}")
        finally:
            if os.path.exists(temp_file_path):
                os.unlink(temp_file_path)
        
        time.sleep(1)

def test_zpl_with_binary():
    """Testa ZPL em modo binário"""
    print("\n🧪 Testando ZPL em modo binário...")
    
    zpl_binary = b"^XA\r\n^FO50,50^A0N,30,30^FDBINARY TEST^FS\r\n^XZ\r\n"
    
    with tempfile.NamedTemporaryFile(mode='wb', suffix='.bin', delete=False) as temp_file:
        temp_file.write(zpl_binary)
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
            print("✅ ZPL binário enviado!")
            
    except Exception as e:
        print(f"❌ Erro: {e}")
    finally:
        if os.path.exists(temp_file_path):
            os.unlink(temp_file_path)

def test_zpl_with_win32print():
    """Testa ZPL via win32print"""
    print("\n🧪 Testando ZPL via win32print...")
    
    try:
        printer_name = "ZDesigner ZD621R-203dpi ZPL"
        handle = win32print.OpenPrinter(printer_name)
        
        # ZPL simples
        zpl_data = "^XA^FO50,50^A0N,30,30^FDWIN32PRINT ZPL^FS^XZ"
        
        print(f"📄 Enviando ZPL: {zpl_data}")
        
        # Iniciar documento
        doc_info = ("Teste ZPL", None, "RAW")
        job_id = win32print.StartDocPrinter(handle, 1, doc_info)
        
        # Iniciar página
        win32print.StartPagePrinter(handle)
        
        # Enviar dados
        win32print.WritePrinter(handle, zpl_data.encode('ascii'))
        
        # Finalizar página
        win32print.EndPagePrinter(handle)
        
        # Finalizar documento
        win32print.EndDocPrinter(handle)
        
        print(f"✅ ZPL via win32print enviado com ID: {job_id}")
        
        win32print.ClosePrinter(handle)
        
    except Exception as e:
        print(f"❌ Erro: {e}")

def test_zpl_with_echo():
    """Testa ZPL via echo"""
    print("\n🧪 Testando ZPL via echo...")
    
    try:
        printer_name = "ZDesigner ZD621R-203dpi ZPL"
        
        # Comando echo
        command = f'echo "^XA^FO50,50^A0N,30,30^FDECHO ZPL TEST^FS^XZ" > temp_echo.txt && copy temp_echo.txt "{printer_name}" && del temp_echo.txt'
        
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        
        print(f"📊 Resultado: {result.returncode}")
        print(f"📊 Saída: {result.stdout}")
        
        if result.returncode == 0:
            print("✅ ZPL via echo enviado!")
            
    except Exception as e:
        print(f"❌ Erro: {e}")

def test_zpl_with_powershell():
    """Testa ZPL via PowerShell"""
    print("\n🧪 Testando ZPL via PowerShell...")
    
    try:
        printer_name = "ZDesigner ZD621R-203dpi ZPL"
        
        # Comando PowerShell
        command = f'powershell "Set-Content -Path temp_ps.txt -Value \'^XA^FO50,50^A0N,30,30^FDPOWERSHELL ZPL TEST^FS^XZ\' -Encoding ASCII; Copy-Item temp_ps.txt \'{printer_name}\'; Remove-Item temp_ps.txt"'
        
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        
        print(f"📊 Resultado: {result.returncode}")
        print(f"📊 Saída: {result.stdout}")
        
        if result.returncode == 0:
            print("✅ ZPL via PowerShell enviado!")
            
    except Exception as e:
        print(f"❌ Erro: {e}")

def main():
    """Função principal"""
    print("=== Teste de Interpretação ZPL - Zebra ZD621R ===\n")
    
    # Teste 1: ZPL básico
    test_basic_zpl()
    time.sleep(2)
    
    # Teste 2: ZPL com CR+LF
    test_zpl_with_crlf()
    time.sleep(2)
    
    # Teste 3: ZPL com LF
    test_zpl_with_lf()
    time.sleep(2)
    
    # Teste 4: ZPL com espaços
    test_zpl_with_spaces()
    time.sleep(2)
    
    # Teste 5: ZPL com diferentes codificações
    test_zpl_with_encoding()
    time.sleep(2)
    
    # Teste 6: ZPL binário
    test_zpl_with_binary()
    time.sleep(2)
    
    # Teste 7: ZPL via win32print
    test_zpl_with_win32print()
    time.sleep(2)
    
    # Teste 8: ZPL via echo
    test_zpl_with_echo()
    time.sleep(2)
    
    # Teste 9: ZPL via PowerShell
    test_zpl_with_powershell()
    
    print("\n✅ Todos os testes de interpretação ZPL concluídos!")
    print("🔍 Verifique se algum formato fez a impressora imprimir...")
    print("💡 Se nenhum funcionou, o problema pode ser:")
    print("   - Driver não está interpretando ZPL corretamente")
    print("   - Impressora em modo de configuração")
    print("   - Problema físico (papel, hardware)")

if __name__ == "__main__":
    main()
