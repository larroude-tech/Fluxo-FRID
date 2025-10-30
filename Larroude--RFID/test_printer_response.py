#!/usr/bin/env python3
"""
Teste para verificar se a impressora está respondendo aos comandos
"""

import os
import subprocess
import tempfile
import time
import win32print

def test_printer_jobs():
    """Verifica se há jobs na fila da impressora"""
    print("🔍 Verificando jobs na fila da impressora...")
    
    try:
        printer_name = "ZDesigner ZD621R-203dpi ZPL"
        handle = win32print.OpenPrinter(printer_name)
        
        # Obter informações da impressora
        info = win32print.GetPrinter(handle, 2)
        
        print(f"📋 Jobs na fila: {info['cJobs']}")
        print(f"📋 Status: {info['Status']}")
        
        if info['cJobs'] > 0:
            print("⚠️ Há jobs na fila da impressora!")
        else:
            print("✅ Nenhum job na fila")
            
        win32print.ClosePrinter(handle)
        
    except Exception as e:
        print(f"❌ Erro ao verificar jobs: {e}")

def test_printer_with_job():
    """Testa enviando um job real para a impressora"""
    print("\n🧪 Testando envio de job real...")
    
    try:
        printer_name = "ZDesigner ZD621R-203dpi ZPL"
        handle = win32print.OpenPrinter(printer_name)
        
        # ZPL simples
        zpl_data = "^XA^FO50,50^A0N,30,30^FDJOB TEST^FS^XZ"
        
        print(f"📄 Enviando ZPL: {zpl_data}")
        
        # Iniciar documento
        doc_info = ("Teste Job", None, "RAW")
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
        
    except Exception as e:
        print(f"❌ Erro ao enviar job: {e}")

def test_printer_status_after_command():
    """Testa status da impressora após enviar comando"""
    print("\n🧪 Testando status após comando...")
    
    # Comando ZPL
    zpl = "^XA^FO50,50^A0N,30,30^FDSTATUS TEST^FS^XZ"
    
    print(f"📄 Enviando: {zpl}")
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as temp_file:
        temp_file.write(zpl)
        temp_file_path = temp_file.name
    
    try:
        printer_name = "ZDesigner ZD621R-203dpi ZPL"
        
        # Verificar status antes
        handle = win32print.OpenPrinter(printer_name)
        info_before = win32print.GetPrinter(handle, 2)
        print(f"📋 Status antes: {info_before['Status']}")
        print(f"📋 Jobs antes: {info_before['cJobs']}")
        win32print.ClosePrinter(handle)
        
        # Enviar comando
        result = subprocess.run(
            ['copy', temp_file_path, printer_name],
            capture_output=True,
            text=True,
            shell=True
        )
        
        print(f"📊 Resultado copy: {result.returncode}")
        
        # Aguardar um pouco
        time.sleep(2)
        
        # Verificar status depois
        handle = win32print.OpenPrinter(printer_name)
        info_after = win32print.GetPrinter(handle, 2)
        print(f"📋 Status depois: {info_after['Status']}")
        print(f"📋 Jobs depois: {info_after['cJobs']}")
        win32print.ClosePrinter(handle)
        
        # Comparar
        if info_after['cJobs'] > info_before['cJobs']:
            print("✅ Job foi adicionado à fila!")
        else:
            print("⚠️ Nenhum job foi adicionado à fila")
            
    except Exception as e:
        print(f"❌ Erro: {e}")
    finally:
        if os.path.exists(temp_file_path):
            os.unlink(temp_file_path)

def test_printer_with_different_datatypes():
    """Testa com diferentes tipos de dados"""
    print("\n🧪 Testando com diferentes tipos de dados...")
    
    datatypes = [
        ("RAW", "^XA^FO50,50^A0N,30,30^FDRAW TEST^FS^XZ"),
        ("TEXT", "TEXT TEST\nLINHA 2\nLINHA 3"),
        ("EMF", "^XA^FO50,50^A0N,30,30^FDEMF TEST^FS^XZ"),
        ("XPS", "^XA^FO50,50^A0N,30,30^FDXPS TEST^FS^XZ"),
    ]
    
    for datatype, content in datatypes:
        print(f"📄 Testando datatype: {datatype}")
        print(f"📄 Conteúdo: {content}")
        
        try:
            printer_name = "ZDesigner ZD621R-203dpi ZPL"
            handle = win32print.OpenPrinter(printer_name)
            
            # Enviar com datatype específico
            doc_info = (f"Teste {datatype}", None, datatype)
            job_id = win32print.StartDocPrinter(handle, 1, doc_info)
            win32print.StartPagePrinter(handle)
            win32print.WritePrinter(handle, content.encode('ascii'))
            win32print.EndPagePrinter(handle)
            win32print.EndDocPrinter(handle)
            
            print(f"✅ Job {datatype} enviado com ID: {job_id}")
            
            # Verificar jobs
            info = win32print.GetPrinter(handle, 2)
            print(f"📋 Jobs na fila: {info['cJobs']}")
            
            win32print.ClosePrinter(handle)
            
        except Exception as e:
            print(f"❌ Erro com {datatype}: {e}")
        
        time.sleep(1)

def test_printer_clear_queue():
    """Testa limpar a fila da impressora"""
    print("\n🧪 Testando limpeza da fila...")
    
    try:
        printer_name = "ZDesigner ZD621R-203dpi ZPL"
        handle = win32print.OpenPrinter(printer_name)
        
        # Verificar jobs antes
        info_before = win32print.GetPrinter(handle, 2)
        print(f"📋 Jobs antes da limpeza: {info_before['cJobs']}")
        
        if info_before['cJobs'] > 0:
            # Limpar fila
            win32print.SetPrinter(handle, 2, info_before, 0)
            print("✅ Fila limpa!")
            
            # Verificar jobs depois
            info_after = win32print.GetPrinter(handle, 2)
            print(f"📋 Jobs depois da limpeza: {info_after['cJobs']}")
        else:
            print("✅ Fila já estava vazia")
            
        win32print.ClosePrinter(handle)
        
    except Exception as e:
        print(f"❌ Erro ao limpar fila: {e}")

def test_printer_manual_print():
    """Testa impressão manual"""
    print("\n🧪 Testando impressão manual...")
    
    # ZPL simples
    zpl = "^XA^FO50,50^A0N,30,30^FDMANUAL TEST^FS^XZ"
    
    print(f"📄 ZPL: {zpl}")
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as temp_file:
        temp_file.write(zpl)
        temp_file_path = temp_file.name
    
    try:
        printer_name = "ZDesigner ZD621R-203dpi ZPL"
        
        # Enviar via copy
        result = subprocess.run(
            ['copy', temp_file_path, printer_name],
            capture_output=True,
            text=True,
            shell=True
        )
        
        print(f"📊 Resultado: {result.returncode}")
        
        if result.returncode == 0:
            print("✅ Comando enviado!")
            print("🔍 Verifique se a impressora imprimiu...")
            print("💡 Se não imprimiu, pode ser necessário:")
            print("   - Verificar se há papel na impressora")
            print("   - Verificar se a impressora está ligada")
            print("   - Verificar se há algum erro na tela da impressora")
            print("   - Tentar imprimir via ZebraDesigner para comparar")
            
    except Exception as e:
        print(f"❌ Erro: {e}")
    finally:
        if os.path.exists(temp_file_path):
            os.unlink(temp_file_path)

if __name__ == "__main__":
    print("=== Teste de Resposta da Impressora - Zebra ZD621R ===\n")
    
    # Teste 1: Verificar jobs
    test_printer_jobs()
    
    # Teste 2: Job real
    test_printer_with_job()
    
    # Teste 3: Status após comando
    test_printer_status_after_command()
    
    # Teste 4: Diferentes datatypes
    test_printer_with_different_datatypes()
    
    # Teste 5: Limpar fila
    test_printer_clear_queue()
    
    # Teste 6: Impressão manual
    test_printer_manual_print()
    
    print("\n✅ Todos os testes de resposta concluídos!")
