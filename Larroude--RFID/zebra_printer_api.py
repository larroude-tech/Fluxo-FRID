#!/usr/bin/env python3
"""
API Python para comunicação com impressora Zebra ZD621R
Pode ser chamada como subprocesso pelo Node.js
"""

import os
import sys
import json
import time
import subprocess
import win32print
import tempfile
from pathlib import Path

class ZebraPrinterAPI:
    def __init__(self):
        self.printer_name = None
        self.is_connected = False
    
    def detect_printers(self):
        """Detecta impressoras Zebra e retorna JSON"""
        try:
            printers = win32print.EnumPrinters(win32print.PRINTER_ENUM_LOCAL | win32print.PRINTER_ENUM_CONNECTIONS)
            
            zebra_printers = []
            for printer in printers:
                printer_name = printer[2]
                if 'zebra' in printer_name.lower() or 'zd621r' in printer_name.lower():
                    zebra_printers.append({
                        'name': printer_name,
                        'type': 'windows',
                        'status': 'available'
                    })
            
            return {
                'success': True,
                'printers': zebra_printers,
                'count': len(zebra_printers),
                'timestamp': time.strftime('%Y-%m-%d %H:%M:%S')
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'printers': [],
                'count': 0,
                'timestamp': time.strftime('%Y-%m-%d %H:%M:%S')
            }
    
    def connect(self, printer_name=None):
        """Conecta à impressora"""
        try:
            if not printer_name:
                result = self.detect_printers()
                if not result['success'] or result['count'] == 0:
                    raise Exception("Nenhuma impressora Zebra detectada")
                printer_name = result['printers'][0]['name']
            
            self.printer_name = printer_name
            self.is_connected = True
            
            return {
                'success': True,
                'printer_name': printer_name,
                'connection_type': 'windows',
                'timestamp': time.strftime('%Y-%m-%d %H:%M:%S')
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'timestamp': time.strftime('%Y-%m-%d %H:%M:%S')
            }
    
    def send_zpl(self, zpl_command):
        """Envia comando ZPL"""
        if not self.is_connected:
            return {
                'success': False,
                'error': 'Impressora não está conectada',
                'timestamp': time.strftime('%Y-%m-%d %H:%M:%S')
            }
        
        try:
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
                return {
                    'success': True,
                    'message': 'Comando ZPL enviado com sucesso',
                    'timestamp': time.strftime('%Y-%m-%d %H:%M:%S')
                }
            else:
                return {
                    'success': False,
                    'error': f"Erro ao enviar: {result.stderr}",
                    'timestamp': time.strftime('%Y-%m-%d %H:%M:%S')
                }
                
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'timestamp': time.strftime('%Y-%m-%d %H:%M:%S')
            }
    
    def test_connection(self):
        """Testa conectividade"""
        try:
            test_zpl = f"""^XA
^FO50,50^A0N,50,50^FDTeste Python API^FS
^FO50,120^BY3^BCN,100,Y,N,N^FD123456789^FS
^FO50,250^A0N,30,30^FDPython API^FS
^FO50,290^A0N,30,30^FDData: {time.strftime('%d/%m/%Y %H:%M:%S')}^FS
^XZ"""
            
            result = self.send_zpl(test_zpl)
            
            if result['success']:
                return {
                    'success': True,
                    'connection_type': 'windows',
                    'printer_name': self.printer_name,
                    'test_result': 'OK',
                    'timestamp': time.strftime('%Y-%m-%d %H:%M:%S')
                }
            else:
                return result
                
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
        return {
            'success': True,
            'message': 'Desconectado da impressora',
            'timestamp': time.strftime('%Y-%m-%d %H:%M:%S')
        }

def main():
    """Função principal - API mode"""
    if len(sys.argv) < 2:
        print(json.dumps({
            'success': False,
            'error': 'Comando não especificado',
            'available_commands': ['detect', 'connect', 'send_zpl', 'test', 'disconnect']
        }))
        return
    
    command = sys.argv[1]
    printer = ZebraPrinterAPI()
    
    if command == 'detect':
        result = printer.detect_printers()
        print(json.dumps(result))
        
    elif command == 'connect':
        printer_name = sys.argv[2] if len(sys.argv) > 2 else None
        result = printer.connect(printer_name)
        print(json.dumps(result))
        
    elif command == 'send_zpl':
        if len(sys.argv) < 3:
            print(json.dumps({
                'success': False,
                'error': 'Comando ZPL não especificado'
            }))
            return
        
        zpl_command = sys.argv[2]
        result = printer.send_zpl(zpl_command)
        print(json.dumps(result))
        
    elif command == 'test':
        # Primeiro conectar
        connect_result = printer.connect()
        if not connect_result['success']:
            print(json.dumps(connect_result))
            return
        
        # Depois testar
        test_result = printer.test_connection()
        print(json.dumps(test_result))
        
        # Desconectar
        printer.disconnect()
        
    elif command == 'disconnect':
        result = printer.disconnect()
        print(json.dumps(result))
        
    else:
        print(json.dumps({
            'success': False,
            'error': f'Comando desconhecido: {command}',
            'available_commands': ['detect', 'connect', 'send_zpl', 'test', 'disconnect']
        }))

if __name__ == "__main__":
    main()
