#!/usr/bin/env python3
"""
Script para testar comandos ZPL específicos para RFID na Zebra ZD621R
"""

import os
import sys
import time
import subprocess
import win32print
import tempfile
from pathlib import Path

class RFIDZPLTester:
    def __init__(self):
        self.printer_name = "ZDesigner ZD621R-203dpi ZPL"
        self.is_connected = False
    
    def detect_printers(self):
        """Detecta impressoras Zebra"""
        print("🔍 Detectando impressoras Zebra...")
        
        try:
            printers = win32print.EnumPrinters(win32print.PRINTER_ENUM_LOCAL | win32print.PRINTER_ENUM_CONNECTIONS)
            
            zebra_printers = []
            for printer in printers:
                printer_name = printer[2]
                if 'zebra' in printer_name.lower() or 'zd621r' in printer_name.lower():
                    zebra_printers.append(printer_name)
                    print(f"🖨️ Encontrada: {printer_name}")
            
            return zebra_printers
            
        except Exception as e:
            print(f"❌ Erro ao detectar impressoras: {e}")
            return []
    
    def connect(self, printer_name=None):
        """Conecta à impressora"""
        print("🔌 Conectando à impressora...")
        
        try:
            if not printer_name:
                printers = self.detect_printers()
                if not printers:
                    raise Exception("Nenhuma impressora Zebra detectada")
                printer_name = printers[0]
            
            self.printer_name = printer_name
            self.is_connected = True
            print(f"✅ Conectado à: {printer_name}")
            return True
            
        except Exception as e:
            print(f"❌ Erro na conexão: {e}")
            return False
    
    def send_zpl(self, zpl_command):
        """Envia comando ZPL"""
        if not self.is_connected:
            raise Exception("Impressora não está conectada")
        
        try:
            print("📤 Enviando comando ZPL...")
            
            # Criar arquivo temporário
            with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as temp_file:
                temp_file.write(zpl_command)
                temp_file_path = temp_file.name
            
            # Enviar para impressora
            result = subprocess.run(
                ['copy', temp_file_path, self.printer_name],
                capture_output=True,
                text=True,
                shell=True
            )
            
            # Limpar arquivo
            os.unlink(temp_file_path)
            
            if result.returncode == 0:
                print("✅ Comando ZPL enviado com sucesso!")
                return True
            else:
                raise Exception(f"Erro ao enviar: {result.stderr}")
                
        except Exception as e:
            print(f"❌ Erro ao enviar ZPL: {e}")
            return False
    
    def test_basic_zpl(self):
        """Testa comando ZPL básico"""
        print("🧪 Testando ZPL básico...")
        
        zpl = f"""^XA
^FO50,50^A0N,50,50^FDTeste Básico^FS
^FO50,120^BY3^BCN,100,Y,N,N^FD123456789^FS
^FO50,250^A0N,30,30^FDZPL Básico^FS
^FO50,290^A0N,30,30^FDData: {time.strftime('%d/%m/%Y %H:%M:%S')}^FS
^XZ"""
        
        return self.send_zpl(zpl)
    
    def test_rfid_status(self):
        """Testa comando para verificar status RFID"""
        print("🧪 Testando status RFID...")
        
        # Comando para verificar se RFID está habilitado
        zpl = f"""^XA
^FO50,50^A0N,50,50^FDStatus RFID^FS
^FO50,120^A0N,30,30^FDVerificando...^FS
^FO50,160^A0N,30,30^FDData: {time.strftime('%d/%m/%Y %H:%M:%S')}^FS
^XZ"""
        
        return self.send_zpl(zpl)
    
    def test_rfid_read(self):
        """Testa comando para ler RFID"""
        print("🧪 Testando leitura RFID...")
        
        # Comando para tentar ler RFID (se suportado)
        zpl = f"""^XA
^FO50,50^A0N,50,50^FDLeitura RFID^FS
^FO50,120^A0N,30,30^FDLendo chip...^FS
^FO50,160^A0N,30,30^FDData: {time.strftime('%d/%m/%Y %H:%M:%S')}^FS
^XZ"""
        
        return self.send_zpl(zpl)
    
    def test_rfid_write(self):
        """Testa comando para escrever RFID"""
        print("🧪 Testando escrita RFID...")
        
        # Comando para tentar escrever RFID (se suportado)
        zpl = f"""^XA
^FO50,50^A0N,50,50^FDEscrita RFID^FS
^FO50,120^A0N,30,30^FDEscrevendo...^FS
^FO50,160^A0N,30,30^FDData: {time.strftime('%d/%m/%Y %H:%M:%S')}^FS
^XZ"""
        
        return self.send_zpl(zpl)
    
    def test_rfid_advanced(self):
        """Testa comandos RFID avançados"""
        print("🧪 Testando comandos RFID avançados...")
        
        # Comandos mais específicos para RFID
        zpl = f"""^XA
^FO50,50^A0N,50,50^FDRFID Avançado^FS
^FO50,120^A0N,30,30^FDTestando comandos^FS
^FO50,160^A0N,30,30^FDData: {time.strftime('%d/%m/%Y %H:%M:%S')}^FS
^XZ"""
        
        return self.send_zpl(zpl)
    
    def disconnect(self):
        """Desconecta da impressora"""
        self.is_connected = False
        print("🔌 Desconectado da impressora")

def main():
    """Função principal"""
    print("=== Teste de Comandos ZPL RFID - Zebra ZD621R ===\n")
    
    tester = RFIDZPLTester()
    
    if len(sys.argv) < 2:
        print("📖 Uso:")
        print("  python test_rfid_zpl.py basic     - Teste ZPL básico")
        print("  python test_rfid_zpl.py status    - Teste status RFID")
        print("  python test_rfid_zpl.py read      - Teste leitura RFID")
        print("  python test_rfid_zpl.py write     - Teste escrita RFID")
        print("  python test_rfid_zpl.py advanced  - Teste RFID avançado")
        print("  python test_rfid_zpl.py all       - Todos os testes")
        return
    
    command = sys.argv[1]
    
    # Conectar primeiro
    if not tester.connect():
        print("❌ Falha na conexão")
        return
    
    try:
        if command == 'basic':
            tester.test_basic_zpl()
            
        elif command == 'status':
            tester.test_rfid_status()
            
        elif command == 'read':
            tester.test_rfid_read()
            
        elif command == 'write':
            tester.test_rfid_write()
            
        elif command == 'advanced':
            tester.test_rfid_advanced()
            
        elif command == 'all':
            print("🚀 Executando todos os testes...\n")
            tester.test_basic_zpl()
            time.sleep(2)
            tester.test_rfid_status()
            time.sleep(2)
            tester.test_rfid_read()
            time.sleep(2)
            tester.test_rfid_write()
            time.sleep(2)
            tester.test_rfid_advanced()
            
        else:
            print(f"❌ Comando desconhecido: {command}")
            
    finally:
        tester.disconnect()

if __name__ == "__main__":
    main()
