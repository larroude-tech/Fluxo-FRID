#!/usr/bin/env python3
"""
Teste específico para imprimir MUPA_TESTE_01 na etiqueta e gravar no RFID
"""

import os
import subprocess
import tempfile
import time
import win32print

def test_print_mupa_label():
    """Testa impressão da etiqueta MUPA_TESTE_01"""
    print("🧪 Testando impressão da etiqueta MUPA_TESTE_01...")
    
    # ZPL para imprimir MUPA_TESTE_01 na etiqueta
    mupa_zpl = """^XA
^FO50,50^A0N,50,50^FDMUPA_TESTE_01^FS
^FO50,120^A0N,30,30^FDTeste RFID^FS
^FO50,160^A0N,25,25^FDData: {date}^FS
^XZ""".format(date=time.strftime('%d/%m/%Y %H:%M:%S'))
    
    print(f"📄 ZPL da etiqueta: {mupa_zpl}")
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as temp_file:
        temp_file.write(mupa_zpl)
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
            print("✅ Etiqueta MUPA_TESTE_01 enviada para impressão!")
            
    except Exception as e:
        print(f"❌ Erro: {e}")
    finally:
        if os.path.exists(temp_file_path):
            os.unlink(temp_file_path)

def test_rfid_write_mupa():
    """Testa gravação de MUPA_TESTE_01 no RFID"""
    print("\n🧪 Testando gravação de MUPA_TESTE_01 no RFID...")
    
    # ZPL para gravar no RFID
    rfid_zpl = """^XA
^RFR,H,0,12,2^FS
^RFW,H,2,12,1^FD{data}^FS
^XZ""".format(data="MUPA_TESTE_01")
    
    print(f"📄 ZPL RFID: {rfid_zpl}")
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as temp_file:
        temp_file.write(rfid_zpl)
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
            print("✅ Comando RFID enviado!")
            
    except Exception as e:
        print(f"❌ Erro: {e}")
    finally:
        if os.path.exists(temp_file_path):
            os.unlink(temp_file_path)

def test_combined_mupa_rfid():
    """Testa impressão e RFID em um único comando"""
    print("\n🧪 Testando impressão + RFID em um único comando...")
    
    # ZPL combinado: imprimir etiqueta + gravar RFID
    combined_zpl = """^XA
^RFR,H,0,12,2^FS
^RFW,H,2,12,1^FDMUPA_TESTE_01^FS
^FO50,50^A0N,50,50^FDMUPA_TESTE_01^FS
^FO50,120^A0N,30,30^FDTeste RFID^FS
^FO50,160^A0N,25,25^FDData: {date}^FS
^XZ""".format(date=time.strftime('%d/%m/%Y %H:%M:%S'))
    
    print(f"📄 ZPL Combinado: {combined_zpl}")
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as temp_file:
        temp_file.write(combined_zpl)
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
            print("✅ Comando combinado enviado!")
            print("🔍 Verifique se:")
            print("   - A etiqueta foi impressa com 'MUPA_TESTE_01'")
            print("   - O RFID foi gravado com 'MUPA_TESTE_01'")
            
    except Exception as e:
        print(f"❌ Erro: {e}")
    finally:
        if os.path.exists(temp_file_path):
            os.unlink(temp_file_path)

def test_rfid_read_verify():
    """Testa leitura do RFID para verificar se foi gravado"""
    print("\n🧪 Testando leitura do RFID para verificação...")
    
    # ZPL para ler o RFID
    read_zpl = """^XA
^RFR,H,0,12,2^FS
^XZ"""
    
    print(f"📄 ZPL Leitura RFID: {read_zpl}")
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as temp_file:
        temp_file.write(read_zpl)
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
            print("💡 Verifique a resposta da impressora para confirmar o valor lido")
            
    except Exception as e:
        print(f"❌ Erro: {e}")
    finally:
        if os.path.exists(temp_file_path):
            os.unlink(temp_file_path)

def test_advanced_rfid_commands():
    """Testa comandos RFID avançados"""
    print("\n🧪 Testando comandos RFID avançados...")
    
    # Comandos RFID avançados
    advanced_commands = [
        # Comando de status RFID
        """^XA
^RFS^FS
^XZ""",
        
        # Comando de configuração RFID
        """^XA
^RFR,H,0,12,2^FS
^RFW,H,2,12,1^FDMUPA_TESTE_01^FS
^XZ""",
        
        # Comando de impressão + RFID com formatação
        """^XA
^RFR,H,0,12,2^FS
^RFW,H,2,12,1^FDMUPA_TESTE_01^FS
^FO50,50^A0N,50,50^FDMUPA_TESTE_01^FS
^FO50,120^A0N,30,30^FDTeste RFID Avançado^FS
^FO50,160^A0N,25,25^FDData: {date}^FS
^FO50,200^BY3^BCN,100,Y,N,N^FDMUPA_TESTE_01^FS
^XZ""".format(date=time.strftime('%d/%m/%Y %H:%M:%S'))
    ]
    
    for i, cmd in enumerate(advanced_commands, 1):
        print(f"📄 Comando RFID Avançado {i}: {cmd}")
        
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
                print("✅ Comando RFID avançado enviado!")
                
        except Exception as e:
            print(f"❌ Erro: {e}")
        finally:
            if os.path.exists(temp_file_path):
                os.unlink(temp_file_path)
        
        time.sleep(2)  # Aguardar entre comandos

if __name__ == "__main__":
    print("=== Teste MUPA_TESTE_01 - Zebra ZD621R ===\n")
    
    # Teste 1: Impressão da etiqueta
    test_print_mupa_label()
    
    # Teste 2: Gravação RFID
    test_rfid_write_mupa()
    
    # Teste 3: Comando combinado
    test_combined_mupa_rfid()
    
    # Teste 4: Leitura RFID
    test_rfid_read_verify()
    
    # Teste 5: Comandos RFID avançados
    test_advanced_rfid_commands()
    
    print("\n✅ Todos os testes MUPA_TESTE_01 concluídos!")
    print("🔍 Verifique se:")
    print("   - A etiqueta foi impressa corretamente")
    print("   - O RFID foi gravado com 'MUPA_TESTE_01'")
    print("   - A leitura do RFID retorna o valor correto")
