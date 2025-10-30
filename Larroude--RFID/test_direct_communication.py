#!/usr/bin/env python3
"""
Teste de comunicação direta com a impressora Zebra ZD621R
Verificando diferentes métodos de envio
"""

import os
import subprocess
import tempfile
import time
import win32print
import win32api

def test_direct_win32print():
    """Testa comunicação direta via win32print"""
    print("🧪 Testando comunicação direta via win32print...")
    
    try:
        printer_name = "ZDesigner ZD621R-203dpi ZPL"
        handle = win32print.OpenPrinter(printer_name)
        
        # ZPL simples
        zpl_data = "^XA^FO50,50^A0N,30,30^FDWIN32PRINT TEST^FS^XZ"
        
        print(f"📄 Enviando ZPL: {zpl_data}")
        
        # Iniciar documento
        doc_info = ("Teste Direto", None, "RAW")
        job_id = win32print.StartDocPrinter(handle, 1, doc_info)
        
        # Iniciar página
        win32print.StartPagePrinter(handle)
        
        # Enviar dados
        win32print.WritePrinter(handle, zpl_data.encode('ascii'))
        
        # Finalizar página
        win32print.EndPagePrinter(handle)
        
        # Finalizar documento
        win32print.EndDocPrinter(handle)
        
        print(f"✅ Job enviado com ID: {job_id}")
        
        # Verificar se o job foi criado
        info = win32print.GetPrinter(handle, 2)
        print(f"📋 Jobs na fila após envio: {info['cJobs']}")
        
        win32print.ClosePrinter(handle)
        
        return True
        
    except Exception as e:
        print(f"❌ Erro ao enviar job: {e}")
        return False

def test_copy_with_echo():
    """Testa envio via copy com echo"""
    print("\n🧪 Testando envio via copy com echo...")
    
    try:
        printer_name = "ZDesigner ZD621R-203dpi ZPL"
        
        # Comando echo direto
        command = f'echo "^XA^FO50,50^A0N,30,30^FDECHO TEST^FS^XZ" > temp.txt && copy temp.txt "{printer_name}" && del temp.txt'
        
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        
        print(f"📊 Resultado: {result.returncode}")
        print(f"📊 Saída: {result.stdout}")
        print(f"📊 Erro: {result.stderr}")
        
        if result.returncode == 0:
            print("✅ Comando echo enviado!")
            return True
        else:
            print("❌ Erro no comando echo")
            return False
            
    except Exception as e:
        print(f"❌ Erro: {e}")
        return False

def test_powershell_copy():
    """Testa envio via PowerShell copy"""
    print("\n🧪 Testando envio via PowerShell copy...")
    
    try:
        printer_name = "ZDesigner ZD621R-203dpi ZPL"
        
        # Comando PowerShell
        command = f'powershell "Set-Content -Path temp.txt -Value \'^XA^FO50,50^A0N,30,30^FDPOWERSHELL TEST^FS^XZ\' -Encoding ASCII; Copy-Item temp.txt \'{printer_name}\'; Remove-Item temp.txt"'
        
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        
        print(f"📊 Resultado: {result.returncode}")
        print(f"📊 Saída: {result.stdout}")
        print(f"📊 Erro: {result.stderr}")
        
        if result.returncode == 0:
            print("✅ Comando PowerShell enviado!")
            return True
        else:
            print("❌ Erro no comando PowerShell")
            return False
            
    except Exception as e:
        print(f"❌ Erro: {e}")
        return False

def test_raw_data():
    """Testa envio de dados RAW"""
    print("\n🧪 Testando envio de dados RAW...")
    
    try:
        printer_name = "ZDesigner ZD621R-203dpi ZPL"
        handle = win32print.OpenPrinter(printer_name)
        
        # Dados RAW simples
        raw_data = b"^XA^FO50,50^A0N,30,30^FDRAW DATA TEST^FS^XZ"
        
        print(f"📄 Enviando dados RAW: {raw_data}")
        
        # Iniciar documento
        doc_info = ("Teste RAW", None, "RAW")
        job_id = win32print.StartDocPrinter(handle, 1, doc_info)
        
        # Iniciar página
        win32print.StartPagePrinter(handle)
        
        # Enviar dados
        win32print.WritePrinter(handle, raw_data)
        
        # Finalizar página
        win32print.EndPagePrinter(handle)
        
        # Finalizar documento
        win32print.EndDocPrinter(handle)
        
        print(f"✅ Dados RAW enviados com ID: {job_id}")
        
        win32print.ClosePrinter(handle)
        
        return True
        
    except Exception as e:
        print(f"❌ Erro ao enviar dados RAW: {e}")
        return False

def test_printer_status_detailed():
    """Verifica status detalhado da impressora"""
    print("\n🔍 Verificando status detalhado da impressora...")
    
    try:
        printer_name = "ZDesigner ZD621R-203dpi ZPL"
        handle = win32print.OpenPrinter(printer_name)
        
        # Obter informações detalhadas
        info = win32print.GetPrinter(handle, 2)
        
        print(f"📋 Status: {info['Status']}")
        print(f"📋 Attributes: {info['Attributes']}")
        print(f"📋 Port: {info['pPortName']}")
        print(f"📋 Driver: {info['pDriverName']}")
        print(f"📋 Jobs: {info['cJobs']}")
        print(f"📋 Priority: {info['Priority']}")
        print(f"📋 DefaultPriority: {info['DefaultPriority']}")
        
        # Verificar flags de status
        status_flags = {
            0x00000001: "PAUSED",
            0x00000002: "ERROR",
            0x00000004: "PENDING_DELETION",
            0x00000008: "PAPER_JAM",
            0x00000010: "PAPER_OUT",
            0x00000020: "MANUAL_FEED",
            0x00000040: "PAPER_PROBLEM",
            0x00000080: "OFFLINE",
            0x00000100: "IO_ACTIVE",
            0x00000200: "BUSY",
            0x00000400: "PRINTING",
            0x00000800: "OUTPUT_BIN_FULL",
            0x00010000: "WARMING_UP",
            0x00020000: "TONER_LOW",
            0x00040000: "NO_TONER",
            0x00080000: "PAGE_PUNT",
            0x00100000: "USER_INTERVENTION",
            0x00200000: "OUT_OF_MEMORY",
            0x00400000: "DOOR_OPEN",
            0x00800000: "SERVER_UNKNOWN",
            0x01000000: "POWER_SAVE"
        }
        
        print("📋 Status flags ativos:")
        active_flags = []
        for flag, description in status_flags.items():
            if info['Status'] & flag:
                active_flags.append(description)
                print(f"  - {description}")
        
        if not active_flags:
            print("  - Nenhum flag ativo (impressora pronta)")
        
        win32print.ClosePrinter(handle)
        
        return info['Status'] == 0
        
    except Exception as e:
        print(f"❌ Erro ao verificar status: {e}")
        return False

def test_simple_text():
    """Testa envio de texto simples"""
    print("\n🧪 Testando envio de texto simples...")
    
    try:
        printer_name = "ZDesigner ZD621R-203dpi ZPL"
        handle = win32print.OpenPrinter(printer_name)
        
        # Texto simples
        text_data = "TESTE TEXTO SIMPLES\nLINHA 2\nLINHA 3\n"
        
        print(f"📄 Enviando texto: {text_data}")
        
        # Iniciar documento
        doc_info = ("Teste Texto", None, "TEXT")
        job_id = win32print.StartDocPrinter(handle, 1, doc_info)
        
        # Iniciar página
        win32print.StartPagePrinter(handle)
        
        # Enviar dados
        win32print.WritePrinter(handle, text_data.encode('ascii'))
        
        # Finalizar página
        win32print.EndPagePrinter(handle)
        
        # Finalizar documento
        win32print.EndDocPrinter(handle)
        
        print(f"✅ Texto enviado com ID: {job_id}")
        
        win32print.ClosePrinter(handle)
        
        return True
        
    except Exception as e:
        print(f"❌ Erro ao enviar texto: {e}")
        return False

def main():
    """Função principal"""
    print("=== Teste de Comunicação Direta - Zebra ZD621R ===\n")
    
    # Teste 1: Status detalhado
    status_ok = test_printer_status_detailed()
    
    if not status_ok:
        print("❌ Impressora não está pronta!")
        return
    
    # Teste 2: win32print direto
    test_direct_win32print()
    
    # Aguardar
    time.sleep(2)
    
    # Teste 3: Copy com echo
    test_copy_with_echo()
    
    # Aguardar
    time.sleep(2)
    
    # Teste 4: PowerShell copy
    test_powershell_copy()
    
    # Aguardar
    time.sleep(2)
    
    # Teste 5: Dados RAW
    test_raw_data()
    
    # Aguardar
    time.sleep(2)
    
    # Teste 6: Texto simples
    test_simple_text()
    
    print("\n✅ Todos os testes de comunicação direta concluídos!")
    print("🔍 Verifique se algum método fez a impressora imprimir...")
    print("💡 Se nenhum funcionou, pode ser um problema:")
    print("   - Físico (papel, porta, hardware)")
    print("   - Driver (configuração incorreta)")
    print("   - Impressora em modo de teste ou configuração")

if __name__ == "__main__":
    main()
