#!/usr/bin/env python3
"""
Teste final de diagnóstico para Zebra ZD621R
"""

import os
import subprocess
import tempfile
import time
import win32print

def test_printer_error_status():
    """Testa status de erro da impressora"""
    print("🔍 Verificando status de erro da impressora...")
    
    try:
        printer_name = "ZDesigner ZD621R-203dpi ZPL"
        handle = win32print.OpenPrinter(printer_name)
        
        # Obter informações detalhadas
        info = win32print.GetPrinter(handle, 2)
        
        print(f"📋 Status: {info['Status']}")
        print(f"📋 Attributes: {info['Attributes']}")
        
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
            0x00001000: "NOT_AVAILABLE",
            0x00002000: "WAITING",
            0x00004000: "PROCESSING",
            0x00008000: "INITIALIZING",
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
        for flag, description in status_flags.items():
            if info['Status'] & flag:
                print(f"  - {description}")
        
        if info['Status'] == 0:
            print("✅ Impressora está PRONTA")
        else:
            print(f"⚠️ Impressora com status: {info['Status']}")
            
        win32print.ClosePrinter(handle)
        
    except Exception as e:
        print(f"❌ Erro ao verificar status: {e}")

def test_zpl_with_paper_feed():
    """Testa ZPL com alimentação de papel"""
    print("\n🧪 Testando ZPL com alimentação de papel...")
    
    # ZPL com comandos de alimentação
    feed_zpl = """^XA
^FO50,50^A0N,30,30^FDPAPER FEED TEST^FS
^FO50,100^A0N,25,25^FDAlimentação de Papel^FS
^XZ
^FF"""
    
    print(f"📄 ZPL com alimentação: {feed_zpl}")
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as temp_file:
        temp_file.write(feed_zpl)
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
            print("✅ ZPL com alimentação enviado!")
            
    except Exception as e:
        print(f"❌ Erro: {e}")
    finally:
        if os.path.exists(temp_file_path):
            os.unlink(temp_file_path)

def test_zpl_with_tear_off():
    """Testa ZPL com modo tear-off"""
    print("\n🧪 Testando ZPL com modo tear-off...")
    
    # ZPL com modo tear-off
    tear_zpl = """^XA
^MMT
^FO50,50^A0N,30,30^FDTEAR OFF TEST^FS
^FO50,100^A0N,25,25^FDModo Tear-Off^FS
^XZ"""
    
    print(f"📄 ZPL tear-off: {tear_zpl}")
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as temp_file:
        temp_file.write(tear_zpl)
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
            print("✅ ZPL tear-off enviado!")
            
    except Exception as e:
        print(f"❌ Erro: {e}")
    finally:
        if os.path.exists(temp_file_path):
            os.unlink(temp_file_path)

def test_zpl_with_cutter():
    """Testa ZPL com modo cutter"""
    print("\n🧪 Testando ZPL com modo cutter...")
    
    # ZPL com modo cutter
    cutter_zpl = """^XA
^MMC
^FO50,50^A0N,30,30^FDCUTTER TEST^FS
^FO50,100^A0N,25,25^FDModo Cutter^FS
^XZ"""
    
    print(f"📄 ZPL cutter: {cutter_zpl}")
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as temp_file:
        temp_file.write(cutter_zpl)
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
            print("✅ ZPL cutter enviado!")
            
    except Exception as e:
        print(f"❌ Erro: {e}")
    finally:
        if os.path.exists(temp_file_path):
            os.unlink(temp_file_path)

def test_zpl_with_rewind():
    """Testa ZPL com modo rewind"""
    print("\n🧪 Testando ZPL com modo rewind...")
    
    # ZPL com modo rewind
    rewind_zpl = """^XA
^MMR
^FO50,50^A0N,30,30^FDREWIND TEST^FS
^FO50,100^A0N,25,25^FDModo Rewind^FS
^XZ"""
    
    print(f"📄 ZPL rewind: {rewind_zpl}")
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as temp_file:
        temp_file.write(rewind_zpl)
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
            print("✅ ZPL rewind enviado!")
            
    except Exception as e:
        print(f"❌ Erro: {e}")
    finally:
        if os.path.exists(temp_file_path):
            os.unlink(temp_file_path)

def test_zpl_with_peel_off():
    """Testa ZPL com modo peel-off"""
    print("\n🧪 Testando ZPL com modo peel-off...")
    
    # ZPL com modo peel-off
    peel_zpl = """^XA
^MMP
^FO50,50^A0N,30,30^FDPEEL OFF TEST^FS
^FO50,100^A0N,25,25^FDModo Peel-Off^FS
^XZ"""
    
    print(f"📄 ZPL peel-off: {peel_zpl}")
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as temp_file:
        temp_file.write(peel_zpl)
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
            print("✅ ZPL peel-off enviado!")
            
    except Exception as e:
        print(f"❌ Erro: {e}")
    finally:
        if os.path.exists(temp_file_path):
            os.unlink(temp_file_path)

def test_zpl_with_keep_back():
    """Testa ZPL com modo keep-back"""
    print("\n🧪 Testando ZPL com modo keep-back...")
    
    # ZPL com modo keep-back
    keep_zpl = """^XA
^MMK
^FO50,50^A0N,30,30^FDKEEP BACK TEST^FS
^FO50,100^A0N,25,25^FDModo Keep-Back^FS
^XZ"""
    
    print(f"📄 ZPL keep-back: {keep_zpl}")
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as temp_file:
        temp_file.write(keep_zpl)
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
            print("✅ ZPL keep-back enviado!")
            
    except Exception as e:
        print(f"❌ Erro: {e}")
    finally:
        if os.path.exists(temp_file_path):
            os.unlink(temp_file_path)

def final_diagnosis():
    """Diagnóstico final"""
    print("\n🔍 Diagnóstico Final:")
    print("=" * 50)
    print("✅ Comunicação: FUNCIONANDO")
    print("✅ Jobs: SENDO CRIADOS")
    print("✅ Processamento: FUNCIONANDO")
    print("❌ Impressão: NÃO ESTÁ IMPRIMINDO")
    print()
    print("💡 Possíveis causas:")
    print("1. 🔧 Impressora em modo PAUSE")
    print("2. 🔧 Sem papel ou papel travado")
    print("3. 🔧 Porta aberta")
    print("4. 🔧 Erro de hardware")
    print("5. 🔧 Configuração incorreta do driver")
    print("6. 🔧 Modo de impressão incorreto")
    print()
    print("🔧 Próximos passos:")
    print("1. Verificar se há papel na impressora")
    print("2. Verificar se a porta está fechada")
    print("3. Verificar se há erros na tela da impressora")
    print("4. Tentar imprimir via ZebraDesigner")
    print("5. Verificar configurações do driver")
    print("6. Reiniciar a impressora")

if __name__ == "__main__":
    print("=== Teste Final de Diagnóstico - Zebra ZD621R ===\n")
    
    # Teste 1: Status de erro
    test_printer_error_status()
    
    # Teste 2: Alimentação de papel
    test_zpl_with_paper_feed()
    
    # Teste 3: Tear-off
    test_zpl_with_tear_off()
    
    # Teste 4: Cutter
    test_zpl_with_cutter()
    
    # Teste 5: Rewind
    test_zpl_with_rewind()
    
    # Teste 6: Peel-off
    test_zpl_with_peel_off()
    
    # Teste 7: Keep-back
    test_zpl_with_keep_back()
    
    # Diagnóstico final
    final_diagnosis()
    
    print("\n✅ Teste final concluído!")
