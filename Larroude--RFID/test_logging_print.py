#!/usr/bin/env python3
"""
Teste de Impressão com Logs Detalhados - Zebra ZD621R
"""

import subprocess
import tempfile
import os
import time
import win32print
import logging
from datetime import datetime

# Configurar logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('printer_debug.log', mode='w'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

def log_printer_status():
    """Log do status da impressora"""
    logger.info("=== VERIFICAÇÃO DE STATUS DA IMPRESSORA ===")
    
    try:
        printer_name = "ZDesigner ZD621R-203dpi ZPL"
        handle = win32print.OpenPrinter(printer_name)
        
        # Obter informações da impressora
        info = win32print.GetPrinter(handle, 2)
        
        logger.info(f"📊 Nome da Impressora: {info['pPrinterName']}")
        logger.info(f"📊 Porta: {info['pPortName']}")
        logger.info(f"📊 Driver: {info['pDriverName']}")
        logger.info(f"📊 Status: {info['Status']}")
        logger.info(f"📊 Attributes: {info['Attributes']}")
        logger.info(f"📊 Jobs: {info['cJobs']}")
        
        # Verificar se está online
        if info['Status'] == 0:
            logger.info("✅ Impressora está ONLINE")
        else:
            logger.warning(f"⚠️ Impressora com status: {info['Status']}")
            
        win32print.ClosePrinter(handle)
        
    except Exception as e:
        logger.error(f"❌ Erro ao verificar status: {e}")

def log_job_details():
    """Log detalhado dos jobs de impressão"""
    logger.info("=== DETALHES DOS JOBS DE IMPRESSÃO ===")
    
    try:
        printer_name = "ZDesigner ZD621R-203dpi ZPL"
        handle = win32print.OpenPrinter(printer_name)
        
        # Listar jobs
        jobs = win32print.EnumJobs(handle, 0, 10)
        
        if jobs:
            logger.info(f"📋 Jobs encontrados: {len(jobs)}")
            for i, job in enumerate(jobs):
                logger.info(f"📋 Job {i+1}:")
                logger.info(f"   - ID: {job['JobId']}")
                logger.info(f"   - Status: {job['Status']}")
                logger.info(f"   - Páginas: {job['TotalPages']}")
                logger.info(f"   - Bytes: {job['TotalBytes']}")
                logger.info(f"   - Data: {job['Submitted']}")
        else:
            logger.info("📋 Nenhum job encontrado")
            
        win32print.ClosePrinter(handle)
        
    except Exception as e:
        logger.error(f"❌ Erro ao verificar jobs: {e}")

def test_print_with_logs(zpl_data, test_name):
    """Testa impressão com logs detalhados"""
    logger.info(f"=== TESTE: {test_name} ===")
    logger.info(f"📄 ZPL: {zpl_data}")
    
    # Log antes da impressão
    logger.info("🔄 Iniciando processo de impressão...")
    
    # Criar arquivo temporário
    temp_file_path = None
    try:
        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as temp_file:
            temp_file.write(zpl_data)
            temp_file_path = temp_file.name
            
        logger.info(f"📁 Arquivo temporário criado: {temp_file_path}")
        
        # Verificar se arquivo foi criado
        if os.path.exists(temp_file_path):
            file_size = os.path.getsize(temp_file_path)
            logger.info(f"📁 Tamanho do arquivo: {file_size} bytes")
            
            with open(temp_file_path, 'r') as f:
                content = f.read()
                logger.info(f"📄 Conteúdo do arquivo: {repr(content)}")
        
        printer_name = "ZDesigner ZD621R-203dpi ZPL"
        logger.info(f"🖨️ Enviando para impressora: {printer_name}")
        
        # Log do comando
        command = f'copy "{temp_file_path}" "{printer_name}"'
        logger.info(f"🔧 Comando: {command}")
        
        # Executar comando
        start_time = time.time()
        result = subprocess.run(
            ['copy', temp_file_path, printer_name],
            capture_output=True,
            text=True,
            shell=True
        )
        end_time = time.time()
        
        # Log dos resultados
        logger.info(f"⏱️ Tempo de execução: {end_time - start_time:.2f} segundos")
        logger.info(f"📊 Return code: {result.returncode}")
        logger.info(f"📊 stdout: {repr(result.stdout)}")
        logger.info(f"📊 stderr: {repr(result.stderr)}")
        
        if result.returncode == 0:
            logger.info("✅ Comando executado com sucesso!")
        else:
            logger.error(f"❌ Erro na execução: {result.stderr}")
            
    except Exception as e:
        logger.error(f"❌ Erro durante impressão: {e}")
        import traceback
        logger.error(f"📋 Traceback: {traceback.format_exc()}")
        
    finally:
        # Limpar arquivo temporário
        if temp_file_path and os.path.exists(temp_file_path):
            try:
                os.unlink(temp_file_path)
                logger.info(f"🗑️ Arquivo temporário removido: {temp_file_path}")
            except Exception as e:
                logger.error(f"❌ Erro ao remover arquivo: {e}")

def test_different_methods():
    """Testa diferentes métodos de impressão"""
    logger.info("=== TESTANDO DIFERENTES MÉTODOS ===")
    
    # Teste 1: ZPL simples
    zpl1 = """^XA
^FO50,50^A0N,30,30^FDTESTE LOG 1^FS
^FO50,100^A0N,25,25^FD21/08/2025^FS
^XZ"""
    test_print_with_logs(zpl1, "ZPL Simples")
    
    time.sleep(2)
    
    # Teste 2: Texto simples
    text2 = "TESTE LOG 2\n21/08/2025\n"
    test_print_with_logs(text2, "Texto Simples")
    
    time.sleep(2)
    
    # Teste 3: ZPL com RFID
    zpl3 = """^XA
^RU
^RFW,H^FDTESTE_LOG_3^FS
^FO50,50^A0N,30,30^FDTESTE LOG 3^FS
^FO50,100^A0N,25,25^FDRFID TEST^FS
^XZ"""
    test_print_with_logs(zpl3, "ZPL com RFID")

def main():
    """Função principal"""
    logger.info("🚀 INICIANDO TESTE DE IMPRESSÃO COM LOGS")
    logger.info(f"📅 Data/Hora: {datetime.now()}")
    
    # Verificar status inicial
    log_printer_status()
    log_job_details()
    
    # Testar impressão
    test_different_methods()
    
    # Verificar status final
    time.sleep(3)
    logger.info("=== VERIFICAÇÃO FINAL ===")
    log_printer_status()
    log_job_details()
    
    logger.info("✅ Teste concluído! Verifique o arquivo printer_debug.log")

if __name__ == "__main__":
    main()

