#!/usr/bin/env python3
"""
Diagnóstico específico para problemas de gravação RFID
Zebra ZD621R
"""

import os
import subprocess
import tempfile
import time
import win32print

def test_rfid_status():
    """Testa status do RFID"""
    print("🔍 Testando status do RFID...")
    
    # Comando para verificar status do RFID
    rfid_status_zpl = """^XA
^RFS^FS
^XZ"""
    
    print(f"📄 ZPL Status RFID: {rfid_status_zpl}")
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as temp_file:
        temp_file.write(rfid_status_zpl)
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
            print("✅ Comando de status RFID enviado!")
            print("💡 Verifique a resposta da impressora para status do RFID")
            
    except Exception as e:
        print(f"❌ Erro: {e}")
    finally:
        if os.path.exists(temp_file_path):
            os.unlink(temp_file_path)

def test_rfid_read_only():
    """Testa apenas leitura RFID"""
    print("\n🧪 Testando leitura RFID...")
    
    # Comando apenas para ler RFID
    rfid_read_zpl = """^XA
^RFR,H,0,12,2^FS
^XZ"""
    
    print(f"📄 ZPL Leitura RFID: {rfid_read_zpl}")
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as temp_file:
        temp_file.write(rfid_read_zpl)
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
            print("✅ Comando de leitura RFID enviado!")
            
    except Exception as e:
        print(f"❌ Erro: {e}")
    finally:
        if os.path.exists(temp_file_path):
            os.unlink(temp_file_path)

def test_rfid_write_only():
    """Testa apenas gravação RFID"""
    print("\n🧪 Testando gravação RFID...")
    
    # Comando apenas para gravar RFID
    rfid_write_zpl = """^XA
^RFW,H,2,12,1^FDMUPA_TESTE_01^FS
^XZ"""
    
    print(f"📄 ZPL Gravação RFID: {rfid_write_zpl}")
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as temp_file:
        temp_file.write(rfid_write_zpl)
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
            print("✅ Comando de gravação RFID enviado!")
            
    except Exception as e:
        print(f"❌ Erro: {e}")
    finally:
        if os.path.exists(temp_file_path):
            os.unlink(temp_file_path)

def test_rfid_different_formats():
    """Testa diferentes formatos de comando RFID"""
    print("\n🧪 Testando diferentes formatos RFID...")
    
    # Diferentes formatos de comando RFID
    rfid_formats = [
        # Formato 1: Comando básico
        """^XA
^RFW,H,2,12,1^FDTESTE_01^FS
^XZ""",
        
        # Formato 2: Com leitura antes
        """^XA
^RFR,H,0,12,2^FS
^RFW,H,2,12,1^FDTESTE_02^FS
^XZ""",
        
        # Formato 3: Com configuração
        """^XA
^RFR,H,0,12,2^FS
^RFW,H,2,12,1^FDTESTE_03^FS
^RFR,H,0,12,2^FS
^XZ""",
        
        # Formato 4: Comando alternativo
        """^XA
^RFW,H,2,12,1^FDTESTE_04^FS
^RFR,H,0,12,2^FS
^XZ""",
        
        # Formato 5: Comando simples
        """^XA
^RFW,H,2,12,1^FDTESTE_05^FS
^XZ"""
    ]
    
    for i, zpl in enumerate(rfid_formats, 1):
        print(f"📄 Formato {i}: {zpl}")
        
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
                print("✅ Formato enviado!")
                
        except Exception as e:
            print(f"❌ Erro: {e}")
        finally:
            if os.path.exists(temp_file_path):
                os.unlink(temp_file_path)
        
        time.sleep(2)  # Aguardar entre comandos

def test_rfid_with_print():
    """Testa RFID com impressão para verificar se imprime mas não grava"""
    print("\n🧪 Testando RFID com impressão...")
    
    # RFID com impressão visível
    rfid_print_zpl = """^XA
^FO50,50^A0N,30,30^FDRFID TEST^FS
^FO50,100^A0N,25,25^FDGravando: MUPA_TESTE_01^FS
^RFW,H,2,12,1^FDMUPA_TESTE_01^FS
^FO50,150^A0N,25,25^FDComando RFID Enviado^FS
^XZ"""
    
    print(f"📄 ZPL RFID com impressão: {rfid_print_zpl}")
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as temp_file:
        temp_file.write(rfid_print_zpl)
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
            print("✅ RFID com impressão enviado!")
            print("🔍 Verifique se a etiqueta foi impressa mas o RFID não foi gravado")
            
    except Exception as e:
        print(f"❌ Erro: {e}")
    finally:
        if os.path.exists(temp_file_path):
            os.unlink(temp_file_path)

def test_rfid_verification():
    """Testa verificação de gravação RFID"""
    print("\n🧪 Testando verificação de gravação RFID...")
    
    # Sequência: gravar -> ler -> verificar
    verification_zpl = """^XA
^FO50,50^A0N,30,30^FDVERIFICACAO RFID^FS
^FO50,100^A0N,25,25^FD1. Gravando...^FS
^RFW,H,2,12,1^FDMUPA_TESTE_01^FS
^FO50,130^A0N,25,25^FD2. Lendo...^FS
^RFR,H,0,12,2^FS
^FO50,160^A0N,25,25^FD3. Verificando...^FS
^XZ"""
    
    print(f"📄 ZPL Verificação RFID: {verification_zpl}")
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as temp_file:
        temp_file.write(verification_zpl)
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
            print("✅ Verificação RFID enviada!")
            print("🔍 Verifique a resposta da impressora para confirmar gravação")
            
    except Exception as e:
        print(f"❌ Erro: {e}")
    finally:
        if os.path.exists(temp_file_path):
            os.unlink(temp_file_path)

def check_printer_rfid_capabilities():
    """Verifica capacidades RFID da impressora"""
    print("\n🔍 Verificando capacidades RFID da impressora...")
    
    try:
        printer_name = "ZDesigner ZD621R-203dpi ZPL"
        handle = win32print.OpenPrinter(printer_name)
        
        # Obter informações detalhadas
        info = win32print.GetPrinter(handle, 2)
        
        print(f"📋 Nome da impressora: {printer_name}")
        print(f"📋 Status: {info['Status']}")
        print(f"📋 Attributes: {info['Attributes']}")
        print(f"📋 Port: {info['pPortName']}")
        print(f"📋 Driver: {info['pDriverName']}")
        
        # Verificar se há jobs na fila
        print(f"📋 Jobs na fila: {info['cJobs']}")
        
        win32print.ClosePrinter(handle)
        
        print("\n💡 Verificações RFID:")
        print("1. Verifique se a impressora tem módulo RFID instalado")
        print("2. Verifique se há etiquetas RFID no rolo")
        print("3. Verifique se o módulo RFID está ligado")
        print("4. Verifique se há erros na tela da impressora")
        print("5. Verifique se o driver suporta comandos RFID")
        
    except Exception as e:
        print(f"❌ Erro ao verificar capacidades: {e}")

def main():
    """Função principal"""
    print("=== Diagnóstico RFID - Zebra ZD621R ===\n")
    
    # Verificar capacidades
    check_printer_rfid_capabilities()
    
    # Teste 1: Status RFID
    test_rfid_status()
    time.sleep(3)
    
    # Teste 2: Leitura RFID
    test_rfid_read_only()
    time.sleep(3)
    
    # Teste 3: Gravação RFID
    test_rfid_write_only()
    time.sleep(3)
    
    # Teste 4: Diferentes formatos
    test_rfid_different_formats()
    time.sleep(3)
    
    # Teste 5: RFID com impressão
    test_rfid_with_print()
    time.sleep(3)
    
    # Teste 6: Verificação
    test_rfid_verification()
    
    print("\n✅ Diagnóstico RFID concluído!")
    print("\n🔍 Próximos passos:")
    print("1. Verifique se alguma etiqueta foi impressa")
    print("2. Verifique se há resposta da impressora")
    print("3. Verifique se o módulo RFID está funcionando")
    print("4. Teste com ZebraDesigner para comparar")
    print("5. Verifique se há etiquetas RFID no rolo")

if __name__ == "__main__":
    main()
