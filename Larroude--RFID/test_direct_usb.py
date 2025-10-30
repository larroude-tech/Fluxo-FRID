#!/usr/bin/env python3
"""
Teste de comunicação direta via USB com a impressora Zebra ZD621R
"""

import os
import subprocess
import tempfile
import time
import serial
import serial.tools.list_ports

def test_serial_ports():
    """Testa portas seriais disponíveis"""
    print("🔍 Verificando portas seriais disponíveis...")
    
    ports = serial.tools.list_ports.comports()
    
    if not ports:
        print("❌ Nenhuma porta serial encontrada")
        return []
    
    print("📋 Portas seriais encontradas:")
    for port in ports:
        print(f"  - {port.device}: {port.description}")
        if 'zebra' in port.description.lower() or 'usb' in port.description.lower():
            print(f"    ⭐ Possível porta da impressora!")
    
    return [port.device for port in ports]

def test_direct_usb_communication():
    """Testa comunicação direta via USB"""
    print("\n🧪 Testando comunicação direta via USB...")
    
    # Tentar comunicação direta via PowerShell
    usb_commands = [
        'Get-WmiObject Win32_USBHub | Where-Object {$_.Name -like "*Zebra*" -or $_.Name -like "*USB*"} | Select-Object Name, DeviceID',
        'Get-PnpDevice | Where-Object {$_.FriendlyName -like "*Zebra*" -or $_.FriendlyName -like "*USB*"} | Select-Object FriendlyName, InstanceId',
        'Get-WmiObject Win32_SerialPort | Select-Object Name, DeviceID, Description'
    ]
    
    for cmd in usb_commands:
        print(f"📄 Executando: {cmd}")
        
        try:
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

def test_zpl_with_raw_mode():
    """Testa ZPL em modo RAW direto"""
    print("\n🧪 Testando ZPL em modo RAW direto...")
    
    # ZPL com caracteres de controle específicos
    raw_zpl = b"\x02^XA^FO50,50^A0N,30,30^FDRAW MODE^FS^XZ\x03"
    
    print(f"📄 ZPL RAW: {repr(raw_zpl)}")
    
    with tempfile.NamedTemporaryFile(mode='wb', suffix='.raw', delete=False) as temp_file:
        temp_file.write(raw_zpl)
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
            print("✅ ZPL RAW enviado!")
            
    except Exception as e:
        print(f"❌ Erro: {e}")
    finally:
        if os.path.exists(temp_file_path):
            os.unlink(temp_file_path)

def test_zpl_with_stx_etx():
    """Testa ZPL com STX/ETX (Start/End of Text)"""
    print("\n🧪 Testando ZPL com STX/ETX...")
    
    # ZPL com STX (0x02) e ETX (0x03)
    stx_etx_zpl = b"\x02^XA^FO50,50^A0N,30,30^FDSTX ETX TEST^FS^XZ\x03"
    
    print(f"📄 ZPL STX/ETX: {repr(stx_etx_zpl)}")
    
    with tempfile.NamedTemporaryFile(mode='wb', suffix='.stx', delete=False) as temp_file:
        temp_file.write(stx_etx_zpl)
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
            print("✅ ZPL STX/ETX enviado!")
            
    except Exception as e:
        print(f"❌ Erro: {e}")
    finally:
        if os.path.exists(temp_file_path):
            os.unlink(temp_file_path)

def test_zpl_with_escape_sequences():
    """Testa ZPL com sequências de escape"""
    print("\n🧪 Testando ZPL com sequências de escape...")
    
    # ZPL com diferentes sequências de escape
    escape_sequences = [
        b"\x1B^XA^FO50,50^A0N,30,30^FDESC TEST^FS^XZ",  # ESC
        b"\x1D^XA^FO50,50^A0N,30,30^FDGS TEST^FS^XZ",   # GS
        b"\x1C^XA^FO50,50^A0N,30,30^FDFS TEST^FS^XZ",   # FS
    ]
    
    for i, seq in enumerate(escape_sequences, 1):
        print(f"📄 Sequência {i}: {repr(seq)}")
        
        with tempfile.NamedTemporaryFile(mode='wb', suffix='.esc', delete=False) as temp_file:
            temp_file.write(seq)
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
                print("✅ Sequência de escape enviada!")
                
        except Exception as e:
            print(f"❌ Erro: {e}")
        finally:
            if os.path.exists(temp_file_path):
                os.unlink(temp_file_path)

def test_zpl_with_printer_commands():
    """Testa comandos específicos da impressora"""
    print("\n🧪 Testando comandos específicos da impressora...")
    
    # Comandos específicos da Zebra
    printer_commands = [
        b"~HS",  # Host Status
        b"~JA",  # Print Job Status
        b"~HI",  # Host Information
        b"~HS~JA~HI",  # Todos os status
    ]
    
    for cmd in printer_commands:
        print(f"📄 Comando: {repr(cmd)}")
        
        with tempfile.NamedTemporaryFile(mode='wb', suffix='.cmd', delete=False) as temp_file:
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
                print("✅ Comando da impressora enviado!")
                
        except Exception as e:
            print(f"❌ Erro: {e}")
        finally:
            if os.path.exists(temp_file_path):
                os.unlink(temp_file_path)
        
        time.sleep(1)  # Aguardar entre comandos

def test_zpl_with_network_style():
    """Testa ZPL como se fosse comunicação de rede"""
    print("\n🧪 Testando ZPL estilo comunicação de rede...")
    
    # ZPL com quebras de linha de rede
    network_zpl = b"^XA\r\n^FO50,50^A0N,30,30^FDNETWORK TEST^FS\r\n^XZ\r\n"
    
    print(f"📄 ZPL Network: {repr(network_zpl)}")
    
    with tempfile.NamedTemporaryFile(mode='wb', suffix='.net', delete=False) as temp_file:
        temp_file.write(network_zpl)
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
            print("✅ ZPL Network enviado!")
            
    except Exception as e:
        print(f"❌ Erro: {e}")
    finally:
        if os.path.exists(temp_file_path):
            os.unlink(temp_file_path)

if __name__ == "__main__":
    print("=== Teste de Comunicação Direta USB - Zebra ZD621R ===\n")
    
    # Teste 1: Portas seriais
    test_serial_ports()
    
    # Teste 2: Comunicação USB
    test_direct_usb_communication()
    
    # Teste 3: ZPL RAW
    test_zpl_with_raw_mode()
    
    # Teste 4: STX/ETX
    test_zpl_with_stx_etx()
    
    # Teste 5: Sequências de escape
    test_zpl_with_escape_sequences()
    
    # Teste 6: Comandos da impressora
    test_zpl_with_printer_commands()
    
    # Teste 7: Estilo rede
    test_zpl_with_network_style()
    
    print("\n✅ Todos os testes de comunicação direta concluídos!")
    print("🔍 Verifique se algum comando fez a impressora imprimir...")
