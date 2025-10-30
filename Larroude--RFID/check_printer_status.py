#!/usr/bin/env python3

import win32print

def check_printer_status():
    printer_name = "ZDesigner ZD621R-203dpi ZPL"
    
    try:
        # Abrir impressora
        handle = win32print.OpenPrinter(printer_name)
        
        # Obter informações da impressora
        info = win32print.GetPrinter(handle, 2)
        
        print(f"📊 Status da Impressora: {printer_name}")
        print(f"Status: {info['Status']}")
        print(f"Attributes: {info['Attributes']}")
        print(f"Port: {info['pPortName']}")
        print(f"Driver: {info['pDriverName']}")
        
        # Verificar se está online
        if info['Status'] == 0:
            print("✅ Impressora está ONLINE")
        else:
            print(f"❌ Impressora está OFFLINE - Status: {info['Status']}")
        
        win32print.ClosePrinter(handle)
        
    except Exception as e:
        print(f"❌ Erro ao verificar status: {e}")

if __name__ == "__main__":
    check_printer_status()
