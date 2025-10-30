#!/usr/bin/env python3
"""
Verificação e ajuste de configurações do driver da impressora Zebra ZD621R
"""

import os
import subprocess
import win32print
import win32api
import tempfile

def check_printer_settings():
    """Verifica configurações detalhadas da impressora"""
    print("🔍 Verificando configurações da impressora...")
    
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
        print(f"📋 StartTime: {info['StartTime']}")
        print(f"📋 UntilTime: {info['UntilTime']}")
        print(f"📋 Jobs: {info['cJobs']}")
        
        # Verificar se está pronto
        if info['Status'] == 0:
            print("✅ Impressora está PRONTA")
        else:
            print(f"⚠️ Impressora com status: {info['Status']}")
            
        win32print.ClosePrinter(handle)
        
    except Exception as e:
        print(f"❌ Erro ao verificar configurações: {e}")

def check_printer_ports():
    """Verifica portas disponíveis"""
    print("\n🔍 Verificando portas disponíveis...")
    
    try:
        result = subprocess.run(
            ['powershell', 'Get-PrinterPort | Select-Object Name, Description, PrinterHostAddress'],
            capture_output=True,
            text=True,
            shell=True
        )
        
        if result.returncode == 0:
            print("📋 Portas disponíveis:")
            print(result.stdout)
        else:
            print("❌ Erro ao obter portas")
            
    except Exception as e:
        print(f"❌ Erro: {e}")

def check_printer_drivers():
    """Verifica drivers disponíveis"""
    print("\n🔍 Verificando drivers disponíveis...")
    
    try:
        result = subprocess.run(
            ['powershell', 'Get-PrinterDriver | Where-Object {$_.Name -like "*Zebra*" -or $_.Name -like "*ZDesigner*"} | Select-Object Name, DriverVersion'],
            capture_output=True,
            text=True,
            shell=True
        )
        
        if result.returncode == 0:
            print("📋 Drivers Zebra encontrados:")
            print(result.stdout)
        else:
            print("❌ Erro ao obter drivers")
            
    except Exception as e:
        print(f"❌ Erro: {e}")

def test_direct_port_communication():
    """Testa comunicação direta com a porta"""
    print("\n🔍 Testando comunicação direta com a porta...")
    
    try:
        # Tentar comunicação direta via PowerShell
        test_commands = [
            'Get-Printer -Name "ZDesigner ZD621R-203dpi ZPL" | Format-List',
            'Get-Printer -Name "ZDesigner ZD621R-203dpi ZPL" | Get-PrinterProperty -PropertyName PrinterStatus',
            'Get-Printer -Name "ZDesigner ZD621R-203dpi ZPL" | Get-PrinterProperty -PropertyName PrinterState'
        ]
        
        for cmd in test_commands:
            print(f"📄 Executando: {cmd}")
            
            result = subprocess.run(
                ['powershell', cmd],
                capture_output=True,
                text=True,
                shell=True
            )
            
            if result.returncode == 0:
                print("📊 Resultado:")
                print(result.stdout)
            else:
                print(f"❌ Erro: {result.stderr}")
                
    except Exception as e:
        print(f"❌ Erro: {e}")

def test_zpl_with_different_encoding():
    """Testa ZPL com diferentes codificações"""
    print("\n🧪 Testando ZPL com diferentes codificações...")
    
    # Testar diferentes codificações
    encodings = ['ascii', 'utf-8', 'cp437', 'iso-8859-1']
    
    for encoding in encodings:
        print(f"📄 Testando encoding: {encoding}")
        
        # ZPL simples
        zpl = "^XA^FO50,50^A0N,30,30^FDENCODING TEST^FS^XZ"
        
        with tempfile.NamedTemporaryFile(mode='wb', suffix='.txt', delete=False) as temp_file:
            temp_file.write(zpl.encode(encoding))
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
                print("✅ ZPL enviado com sucesso!")
                
        except Exception as e:
            print(f"❌ Erro: {e}")
        finally:
            if os.path.exists(temp_file_path):
                os.unlink(temp_file_path)

def test_zpl_with_binary_mode():
    """Testa ZPL em modo binário"""
    print("\n🧪 Testando ZPL em modo binário...")
    
    # ZPL com caracteres de controle binários
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

def suggest_solutions():
    """Sugere soluções baseadas nos testes"""
    print("\n💡 Sugestões de Solução:")
    print("=" * 50)
    print("1. 🔧 Verificar configurações do driver:")
    print("   - Abrir 'Impressoras e Scanners' no Windows")
    print("   - Clicar com botão direito na impressora")
    print("   - Selecionar 'Propriedades da impressora'")
    print("   - Verificar se está em modo 'ZPL' ou 'RAW'")
    print()
    print("2. 🔧 Verificar configurações de porta:")
    print("   - Verificar se a porta USB está correta")
    print("   - Tentar reconectar o cabo USB")
    print()
    print("3. 🔧 Reinstalar driver:")
    print("   - Baixar driver mais recente da Zebra")
    print("   - Desinstalar driver atual")
    print("   - Instalar novo driver")
    print()
    print("4. 🔧 Testar com software ZebraDesigner:")
    print("   - Se ZebraDesigner funciona, copiar configurações")
    print("   - Verificar se há diferenças nas configurações")
    print()
    print("5. 🔧 Verificar se impressora está em modo ZPL:")
    print("   - Algumas impressoras precisam ser configuradas")
    print("   - Verificar manual da impressora")
    print()

if __name__ == "__main__":
    print("=== Verificação de Configurações - Zebra ZD621R ===\n")
    
    # Verificar configurações
    check_printer_settings()
    
    # Verificar portas
    check_printer_ports()
    
    # Verificar drivers
    check_printer_drivers()
    
    # Testar comunicação direta
    test_direct_port_communication()
    
    # Testar diferentes codificações
    test_zpl_with_different_encoding()
    
    # Testar modo binário
    test_zpl_with_binary_mode()
    
    # Sugerir soluções
    suggest_solutions()
    
    print("✅ Verificação concluída!")
