#!/usr/bin/env python3
"""
Teste direto de conexão USB com a impressora Zebra ZD621R
Porta identificada: Port_#0001.Hub_#0001
"""

import os
import subprocess
import tempfile
import time
import win32print
import win32api
from pathlib import Path

def list_all_printers():
    """Lista todas as impressoras disponíveis no sistema"""
    print("🖨️ Listando todas as impressoras disponíveis...")
    
    try:
        printers = win32print.EnumPrinters(win32print.PRINTER_ENUM_LOCAL | win32print.PRINTER_ENUM_CONNECTIONS)
        
        print(f"📋 Encontradas {len(printers)} impressoras:")
        for i, printer in enumerate(printers):
            print(f"  {i+1}. {printer[2]}")
            
        return [printer[2] for printer in printers]
        
    except Exception as e:
        print(f"❌ Erro ao listar impressoras: {e}")
        return []

def test_printer_by_name(printer_name):
    """Testa impressora pelo nome exato"""
    print(f"\n🧪 Testando impressora: {printer_name}")
    
    # ZPL de teste simples
    test_zpl = f"""^XA
^FO50,50^A0N,40,40^FDTeste USB Direto^FS
^FO50,100^A0N,25,25^FDImpressora: {printer_name[:30]}^FS
^FO50,130^A0N,25,25^FDData: {time.strftime('%d/%m/%Y %H:%M:%S')}^FS
^FO50,160^A0N,20,20^FDPorta USB: Port_#0001.Hub_#0001^FS
^XZ"""
    
    print(f"📄 ZPL enviado:")
    print(test_zpl)
    
    try:
        # Método 1: Via win32print (RAW)
        print("\n🔄 Tentativa 1: Usando win32print (RAW)...")
        
        handle = win32print.OpenPrinter(printer_name)
        
        # Configurar para modo RAW
        doc_info = ("Teste USB Direto", None, "RAW")
        job_id = win32print.StartDocPrinter(handle, 1, doc_info)
        
        win32print.StartPagePrinter(handle)
        win32print.WritePrinter(handle, test_zpl.encode('ascii'))
        win32print.EndPagePrinter(handle)
        win32print.EndDocPrinter(handle)
        
        # Verificar status do job
        time.sleep(2)
        info = win32print.GetPrinter(handle, 2)
        print(f"✅ Job ID: {job_id}")
        print(f"📊 Jobs na fila: {info['cJobs']}")
        print(f"📊 Status: {info['Status']}")
        
        win32print.ClosePrinter(handle)
        
        return True
        
    except Exception as e:
        print(f"❌ Erro no método win32print: {e}")
        
    try:
        # Método 2: Via arquivo temporário e copy
        print("\n🔄 Tentativa 2: Usando copy para impressora...")
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.zpl', delete=False) as temp_file:
            temp_file.write(test_zpl)
            temp_file_path = temp_file.name
        
        # Usar copy para enviar arquivo
        result = subprocess.run(
            ['copy', temp_file_path, printer_name],
            capture_output=True,
            text=True,
            shell=True
        )
        
        print(f"📊 Return code: {result.returncode}")
        print(f"📊 Stdout: {result.stdout}")
        if result.stderr:
            print(f"📊 Stderr: {result.stderr}")
        
        # Limpar arquivo temporário
        os.unlink(temp_file_path)
        
        if result.returncode == 0:
            print("✅ Arquivo enviado via copy!")
            return True
        else:
            print("❌ Falha no envio via copy")
            
    except Exception as e:
        print(f"❌ Erro no método copy: {e}")
        
    return False

def test_zebra_specific_names():
    """Testa nomes específicos da Zebra"""
    zebra_names = [
        "Zebra Technologies ZTC ZD621R-203dpi ZPL",
        "ZDesigner ZD621R-203dpi ZPL", 
        "Zebra ZD621R",
        "ZD621R-203dpi ZPL"
    ]
    
    print("\n🔍 Testando nomes específicos da Zebra...")
    
    for name in zebra_names:
        print(f"\n🧪 Tentando: {name}")
        try:
            # Verificar se a impressora existe
            handle = win32print.OpenPrinter(name)
            win32print.ClosePrinter(handle)
            print(f"✅ Impressora encontrada: {name}")
            
            # Testar envio
            if test_printer_by_name(name):
                print(f"🎉 SUCESSO com: {name}")
                return name
            else:
                print(f"❌ Falha no envio para: {name}")
                
        except Exception as e:
            print(f"❌ Impressora não encontrada: {name} - {e}")
    
    return None

def check_printer_status(printer_name):
    """Verifica status detalhado da impressora"""
    print(f"\n📊 Verificando status de: {printer_name}")
    
    try:
        handle = win32print.OpenPrinter(printer_name)
        
        # Obter informações da impressora
        info = win32print.GetPrinter(handle, 2)
        
        print(f"📋 Nome: {info['pPrinterName']}")
        print(f"📋 Porta: {info['pPortName']}")
        print(f"📋 Driver: {info['pDriverName']}")
        print(f"📋 Status: {info['Status']}")
        print(f"📋 Jobs na fila: {info['cJobs']}")
        print(f"📋 Comentário: {info.get('pComment', 'N/A')}")
        print(f"📋 Local: {info.get('pLocation', 'N/A')}")
        
        # Verificar se está online
        if info['Status'] == 0:
            print("✅ Impressora está ONLINE")
        else:
            print(f"⚠️ Impressora com status: {info['Status']}")
            
        win32print.ClosePrinter(handle)
        return True
        
    except Exception as e:
        print(f"❌ Erro ao verificar status: {e}")
        return False

def main():
    print("=== Teste de Conexão USB Direta - Zebra ZD621R ===")
    print("Porta USB identificada: Port_#0001.Hub_#0001\n")
    
    # 1. Listar todas as impressoras
    printers = list_all_printers()
    
    if not printers:
        print("❌ Nenhuma impressora encontrada!")
        return
    
    # 2. Tentar nomes específicos da Zebra
    success_printer = test_zebra_specific_names()
    
    if success_printer:
        print(f"\n🎉 TESTE BEM-SUCEDIDO!")
        print(f"✅ Impressora funcionando: {success_printer}")
        check_printer_status(success_printer)
    else:
        print(f"\n❌ TESTE FALHOU!")
        print("💡 Tentativas com todas as impressoras encontradas:")
        
        # 3. Tentar com todas as impressoras encontradas
        for printer in printers:
            if "zebra" in printer.lower() or "zd621" in printer.lower() or "zpl" in printer.lower():
                print(f"\n🧪 Tentando impressora: {printer}")
                check_printer_status(printer)
                if test_printer_by_name(printer):
                    print(f"🎉 SUCESSO com: {printer}")
                    break
        else:
            print("\n❌ Nenhuma impressora Zebra funcionou")
            print("\n💡 Sugestões:")
            print("1. Verificar se o driver está instalado corretamente")
            print("2. Verificar se a impressora está ligada")
            print("3. Tentar reinstalar o driver da impressora")
            print("4. Verificar configurações de porta no Windows")

if __name__ == "__main__":
    main()
