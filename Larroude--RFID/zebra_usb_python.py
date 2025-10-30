#!/usr/bin/env python3
"""
Script Python para comunicação com impressora Zebra ZD621R via USB
"""

import os
import sys
import time
import subprocess
import win32print
import win32api
import tempfile
from pathlib import Path

class ZebraUSBPrinter:
    def __init__(self):
        self.printer_name = None
        self.is_connected = False
        self.connection_type = None
    
    def detect_printers(self):
        """Detecta impressoras Zebra no sistema"""
        print("🔍 Detectando impressoras Zebra...")
        
        try:
            # Listar todas as impressoras do Windows
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
        """Conecta à impressora Zebra"""
        print("🔌 Conectando à impressora Zebra...")
        
        try:
            if not printer_name:
                # Auto-detect
                printers = self.detect_printers()
                if not printers:
                    raise Exception("Nenhuma impressora Zebra detectada")
                printer_name = printers[0]
            
            self.printer_name = printer_name
            self.is_connected = True
            self.connection_type = 'windows'
            
            print(f"✅ Conectado à: {printer_name}")
            return True
            
        except Exception as e:
            print(f"❌ Erro na conexão: {e}")
            return False
    
    def send_zpl(self, zpl_command):
        """Envia comando ZPL para a impressora"""
        if not self.is_connected:
            raise Exception("Impressora não está conectada")
        
        try:
            print("📤 Enviando comando ZPL...")
            
            # Criar arquivo temporário com o comando ZPL
            with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as temp_file:
                temp_file.write(zpl_command)
                temp_file_path = temp_file.name
            
            # Enviar para a impressora usando comando do Windows
            result = subprocess.run(
                ['copy', temp_file_path, self.printer_name],
                capture_output=True,
                text=True,
                shell=True
            )
            
            # Limpar arquivo temporário
            os.unlink(temp_file_path)
            
            if result.returncode == 0:
                print("✅ Comando ZPL enviado com sucesso!")
                return True
            else:
                raise Exception(f"Erro ao enviar: {result.stderr}")
                
        except Exception as e:
            print(f"❌ Erro ao enviar ZPL: {e}")
            return False
    
    def test_connection(self):
        """Testa a conectividade da impressora"""
        try:
            print("🧪 Testando conectividade...")
            
            test_zpl = f"""^XA
^FO50,50^A0N,50,50^FDTeste Python Zebra^FS
^FO50,120^BY3^BCN,100,Y,N,N^FD123456789^FS
^FO50,250^A0N,30,30^FDPython Test^FS
^FO50,290^A0N,30,30^FDData: {time.strftime('%d/%m/%Y %H:%M:%S')}^FS
^XZ"""
            
            success = self.send_zpl(test_zpl)
            
            if success:
                print("✅ Teste de conectividade: OK")
                return {
                    'success': True,
                    'connection_type': self.connection_type,
                    'printer_name': self.printer_name,
                    'timestamp': time.strftime('%Y-%m-%d %H:%M:%S')
                }
            else:
                return {
                    'success': False,
                    'error': 'Falha no envio do comando de teste',
                    'timestamp': time.strftime('%Y-%m-%d %H:%M:%S')
                }
                
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'timestamp': time.strftime('%Y-%m-%d %H:%M:%S')
            }
    
    def disconnect(self):
        """Desconecta da impressora"""
        self.is_connected = False
        self.printer_name = None
        self.connection_type = None
        print("🔌 Desconectado da impressora")

def main():
    """Função principal"""
    print("=== Teste de Conexão USB Zebra ZD621R (Python) ===\n")
    
    printer = ZebraUSBPrinter()
    
    if len(sys.argv) < 2:
        print("📖 Uso:")
        print("  python zebra_usb_python.py detect    - Detecta impressoras")
        print("  python zebra_usb_python.py connect   - Auto-conecta e testa")
        print("  python zebra_usb_python.py test      - Teste completo")
        print("  python zebra_usb_python.py send <zpl> - Envia comando ZPL")
        return
    
    command = sys.argv[1]
    
    if command == 'detect':
        printers = printer.detect_printers()
        print(f"\n📊 Total de impressoras Zebra encontradas: {len(printers)}")
        
    elif command == 'connect':
        if printer.connect():
            result = printer.test_connection()
            print(f"\n📊 Resultado: {result}")
            printer.disconnect()
        
    elif command == 'test':
        print("🧪 Executando teste completo...\n")
        
        # 1. Detectar
        printers = printer.detect_printers()
        if not printers:
            print("❌ Nenhuma impressora Zebra detectada")
            return
        
        print(f"✅ {len(printers)} impressora(s) encontrada(s)")
        
        # 2. Conectar
        if not printer.connect():
            print("❌ Falha na conexão")
            return
        
        # 3. Testar
        result = printer.test_connection()
        print(f"\n📊 Resultado do teste: {result}")
        
        # 4. Desconectar
        printer.disconnect()
        
    elif command == 'send':
        if len(sys.argv) < 3:
            print("❌ Erro: Comando ZPL é obrigatório")
            print("Uso: python zebra_usb_python.py send <comando_zpl>")
            return
        
        zpl_command = sys.argv[2]
        
        if printer.connect():
            success = printer.send_zpl(zpl_command)
            if success:
                print("✅ Comando ZPL enviado com sucesso!")
            printer.disconnect()
    
    else:
        print(f"❌ Comando desconhecido: {command}")

if __name__ == "__main__":
    main()
