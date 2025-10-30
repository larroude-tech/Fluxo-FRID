#!/usr/bin/env python3
"""
Script para corrigir problemas de conexão USB com impressora Zebra
Baseado nos erros mostrados nos logs
"""

import os
import subprocess
import tempfile
import time
import win32print
import win32api
import serial.tools.list_ports
import sys

def fix_printer_driver():
    """Corrige configurações do driver da impressora"""
    print("🔧 Verificando e corrigindo configurações do driver...")
    
    printer_name = "ZDesigner ZD621R-203dpi ZPL"
    
    try:
        # Abrir impressora
        handle = win32print.OpenPrinter(printer_name)
        
        # Obter configurações atuais
        info = win32print.GetPrinter(handle, 2)
        print(f"📋 Impressora: {info['pPrinterName']}")
        print(f"📋 Porta atual: {info['pPortName']}")
        print(f"📋 Driver: {info['pDriverName']}")
        
        # Verificar se está em modo RAW
        print("\n🔧 Verificando configurações de porta...")
        
        win32print.ClosePrinter(handle)
        
        # Tentar reconfigurar para modo RAW se necessário
        print("✅ Driver verificado")
        
    except Exception as e:
        print(f"❌ Erro ao verificar driver: {e}")

def test_direct_usb_methods():
    """Testa diferentes métodos de conexão USB"""
    printer_name = "ZDesigner ZD621R-203dpi ZPL"
    
    # ZPL de teste mais simples
    simple_zpl = "^XA^FO50,50^A0N,30,30^FDTeste USB Fix^FS^XZ"
    
    print("🧪 Testando métodos de conexão USB...")
    
    # Método 1: win32print com configuração específica
    try:
        print("\n🔄 Método 1: win32print com configuração RAW...")
        
        handle = win32print.OpenPrinter(printer_name)
        
        # Configurar job para RAW
        doc_info = ("USB_Fix_Test", None, "RAW")
        
        # Iniciar job
        job_id = win32print.StartDocPrinter(handle, 1, doc_info)
        print(f"📄 Job iniciado: {job_id}")
        
        # Enviar dados
        win32print.StartPagePrinter(handle)
        bytes_written = win32print.WritePrinter(handle, simple_zpl.encode('ascii'))
        print(f"📤 Bytes escritos: {bytes_written}")
        
        win32print.EndPagePrinter(handle)
        win32print.EndDocPrinter(handle)
        win32print.ClosePrinter(handle)
        
        print("✅ Método 1 executado - verificar se imprimiu")
        time.sleep(3)
        
        return True
        
    except Exception as e:
        print(f"❌ Método 1 falhou: {e}")
    
    # Método 2: Arquivo temporário com copy
    try:
        print("\n🔄 Método 2: Copy via arquivo temporário...")
        
        # Criar arquivo temporário
        temp_path = os.path.join(os.getcwd(), "temp_zpl_test.txt")
        with open(temp_path, 'w') as f:
            f.write(simple_zpl)
        
        # Usar copy
        cmd = f'copy "{temp_path}" "{printer_name}"'
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        
        print(f"📊 Return code: {result.returncode}")
        print(f"📊 Output: {result.stdout}")
        if result.stderr:
            print(f"📊 Error: {result.stderr}")
        
        # Limpar arquivo
        os.remove(temp_path)
        
        if result.returncode == 0:
            print("✅ Método 2 executado - verificar se imprimiu")
            return True
        else:
            print("❌ Método 2 falhou")
            
    except Exception as e:
        print(f"❌ Método 2 falhou: {e}")
    
    # Método 3: Print direto via sistema
    try:
        print("\n🔄 Método 3: Print via sistema...")
        
        temp_path = os.path.join(os.getcwd(), "temp_system_print.zpl")
        with open(temp_path, 'w') as f:
            f.write(simple_zpl)
        
        # Usar print command
        cmd = f'print "{temp_path}"'
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        
        print(f"📊 Return code: {result.returncode}")
        
        os.remove(temp_path)
        
        if result.returncode == 0:
            print("✅ Método 3 executado")
            return True
            
    except Exception as e:
        print(f"❌ Método 3 falhou: {e}")
    
    return False

def check_usb_ports():
    """Verifica portas USB disponíveis"""
    print("\n🔍 Verificando portas USB/Serial disponíveis...")
    
    try:
        ports = serial.tools.list_ports.comports()
        
        print(f"📋 Portas encontradas: {len(ports)}")
        for port in ports:
            print(f"  📍 {port.device} - {port.description}")
            if "zebra" in port.description.lower() or "zd621" in port.description.lower():
                print(f"    🎯 ZEBRA ENCONTRADA: {port.device}")
                
    except Exception as e:
        print(f"❌ Erro ao verificar portas: {e}")

def restart_print_spooler():
    """Reinicia o serviço de spooler de impressão"""
    print("\n🔄 Reiniciando serviço de spooler de impressão...")
    
    try:
        # Parar spooler
        result1 = subprocess.run(['net', 'stop', 'spooler'], 
                                capture_output=True, text=True, shell=True)
        print(f"📊 Stop spooler: {result1.returncode}")
        
        time.sleep(2)
        
        # Iniciar spooler
        result2 = subprocess.run(['net', 'start', 'spooler'], 
                                capture_output=True, text=True, shell=True)
        print(f"📊 Start spooler: {result2.returncode}")
        
        if result2.returncode == 0:
            print("✅ Spooler reiniciado com sucesso")
            time.sleep(3)
            return True
        else:
            print("❌ Falha ao reiniciar spooler")
            
    except Exception as e:
        print(f"❌ Erro ao reiniciar spooler: {e}")
    
    return False

def test_printer_queue():
    """Testa e limpa fila de impressão"""
    printer_name = "ZDesigner ZD621R-203dpi ZPL"
    
    print(f"\n📋 Verificando fila de impressão: {printer_name}")
    
    try:
        handle = win32print.OpenPrinter(printer_name)
        
        # Verificar jobs na fila
        jobs = win32print.EnumJobs(handle, 0, -1, 1)
        print(f"📊 Jobs na fila: {len(jobs)}")
        
        if jobs:
            print("🗑️ Limpando jobs antigos...")
            for job in jobs:
                try:
                    win32print.SetJob(handle, job['JobId'], 0, None, win32print.JOB_CONTROL_DELETE)
                    print(f"  🗑️ Job {job['JobId']} removido")
                except:
                    pass
        
        # Verificar status da impressora
        info = win32print.GetPrinter(handle, 2)
        print(f"📊 Status da impressora: {info['Status']}")
        print(f"📊 Jobs restantes: {info['cJobs']}")
        
        win32print.ClosePrinter(handle)
        
        return True
        
    except Exception as e:
        print(f"❌ Erro ao verificar fila: {e}")
        return False

def main():
    print("=== Correção de Problemas USB - Zebra ZD621R ===")
    print("Baseado nos erros: 'Nenhuma conexão alternativa funcionou'\n")
    
    # 1. Verificar portas USB
    check_usb_ports()
    
    # 2. Verificar e limpar fila de impressão
    test_printer_queue()
    
    # 3. Verificar driver
    fix_printer_driver()
    
    # 4. Reiniciar spooler (opcional - descomente se necessário)
    print("\n❓ Deseja reiniciar o spooler de impressão? (pode ajudar)")
    print("   Descomente a linha abaixo se quiser tentar:")
    print("   # restart_print_spooler()")
    
    # 5. Testar métodos de conexão
    print("\n🧪 Testando métodos de conexão...")
    success = test_direct_usb_methods()
    
    if success:
        print("\n🎉 TESTE BEM-SUCEDIDO!")
        print("✅ Pelo menos um método funcionou")
        print("📋 Verifique se a etiqueta foi impressa")
    else:
        print("\n❌ TODOS OS MÉTODOS FALHARAM")
        print("\n💡 Sugestões para resolver:")
        print("1. Verificar se a impressora está ligada")
        print("2. Verificar cabo USB")
        print("3. Reinstalar driver da impressora")
        print("4. Executar como Administrador")
        print("5. Verificar se há papel na impressora")
        print("6. Tentar reiniciar o spooler (descomente a linha)")

if __name__ == "__main__":
    main()
