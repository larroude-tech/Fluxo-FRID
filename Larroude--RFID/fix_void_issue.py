#!/usr/bin/env python3
"""
Script para resolver o problema VOID na impressora Zebra
"""

import win32print
import time

def check_printer_status():
    """Verifica status detalhado da impressora"""
    print("🔍 Verificando status da impressora...")
    
    printer_name = "ZDesigner ZD621R-203dpi ZPL"
    
    try:
        handle = win32print.OpenPrinter(printer_name)
        info = win32print.GetPrinter(handle, 2)
        
        print(f"📋 Status da impressora:")
        print(f"   Nome: {info['pPrinterName']}")
        print(f"   Porta: {info['pPortName']}")
        print(f"   Driver: {info['pDriverName']}")
        print(f"   Status: {info['Status']}")
        print(f"   Jobs na fila: {info['cJobs']}")
        print(f"   Atributos: {info['Attributes']}")
        
        win32print.ClosePrinter(handle)
        
        return True
        
    except Exception as e:
        print(f"❌ Erro ao verificar status: {e}")
        return False

def calibrate_printer():
    """Envia comandos de calibração"""
    print("\n🔧 Enviando comandos de calibração...")
    
    printer_name = "ZDesigner ZD621R-203dpi ZPL"
    
    # Sequência de comandos de calibração
    calibration_commands = [
        # Reset completo
        "~JA\n",
        
        # Calibração automática
        "^XA\n^JUS\n^XZ\n",
        
        # Configurar modo ZPL
        "^XA\n^SZ\n^XZ\n",
        
        # Calibração de mídia
        "^XA\n^MNN\n^XZ\n",
        
        # Configurar densidade de impressão
        "^XA\n^MD15\n^XZ\n",
        
        # Configurar velocidade
        "^XA\n^PR4\n^XZ\n"
    ]
    
    try:
        handle = win32print.OpenPrinter(printer_name)
        
        for i, command in enumerate(calibration_commands, 1):
            print(f"   Enviando comando {i}/6...")
            
            doc_info = (f"Calibration_{i}", None, "RAW")
            job_id = win32print.StartDocPrinter(handle, 1, doc_info)
            
            win32print.StartPagePrinter(handle)
            win32print.WritePrinter(handle, command.encode('ascii'))
            win32print.EndPagePrinter(handle)
            win32print.EndDocPrinter(handle)
            
            time.sleep(2)  # Aguardar entre comandos
        
        win32print.ClosePrinter(handle)
        
        print("✅ Calibração concluída!")
        print("⏳ Aguardando 10 segundos para a impressora processar...")
        time.sleep(10)
        
        return True
        
    except Exception as e:
        print(f"❌ Erro na calibração: {e}")
        return False

def test_simple_label():
    """Teste com etiqueta super simples"""
    print("\n🧪 Testando etiqueta super simples...")
    
    printer_name = "ZDesigner ZD621R-203dpi ZPL"
    
    # ZPL mais simples possível
    simple_zpl = """^XA
^FO100,100^A0N,50,50^FDTESTE SIMPLES^FS
^FO100,200^A0N,30,30^FDSEM VOID^FS
^XZ"""
    
    try:
        handle = win32print.OpenPrinter(printer_name)
        doc_info = ("Simple_Test", None, "RAW")
        job_id = win32print.StartDocPrinter(handle, 1, doc_info)
        
        print(f"📄 Job iniciado: {job_id}")
        
        win32print.StartPagePrinter(handle)
        bytes_written = win32print.WritePrinter(handle, simple_zpl.encode('ascii'))
        win32print.EndPagePrinter(handle)
        win32print.EndDocPrinter(handle)
        
        print(f"📤 Bytes enviados: {bytes_written}")
        win32print.ClosePrinter(handle)
        
        print("✅ Etiqueta simples enviada!")
        print("🔍 Verifique se imprimiu SEM VOID")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro: {e}")
        return False

def clear_printer_memory():
    """Limpa memória da impressora"""
    print("\n🗑️ Limpando memória da impressora...")
    
    printer_name = "ZDesigner ZD621R-203dpi ZPL"
    
    # Comandos para limpar memória
    clear_commands = """^XA
^IDR:*.*^FS
^XZ

^XA
^IDR:*.ZPL^FS
^XZ

~JA"""
    
    try:
        handle = win32print.OpenPrinter(printer_name)
        doc_info = ("Clear_Memory", None, "RAW")
        job_id = win32print.StartDocPrinter(handle, 1, doc_info)
        
        win32print.StartPagePrinter(handle)
        bytes_written = win32print.WritePrinter(handle, clear_commands.encode('ascii'))
        win32print.EndPagePrinter(handle)
        win32print.EndDocPrinter(handle)
        
        print(f"📤 Comandos de limpeza enviados: {bytes_written} bytes")
        win32print.ClosePrinter(handle)
        
        print("✅ Memória limpa!")
        time.sleep(5)
        
        return True
        
    except Exception as e:
        print(f"❌ Erro na limpeza: {e}")
        return False

def main():
    print("=== CORREÇÃO DO PROBLEMA VOID ===")
    print("Zebra ZD621R - Diagnóstico e Correção\n")
    
    # 1. Verificar status
    check_printer_status()
    
    # 2. Limpar memória
    clear_printer_memory()
    
    # 3. Calibrar impressora
    calibrate_printer()
    
    # 4. Teste simples
    test_simple_label()
    
    print("\n" + "="*50)
    print("🎯 PRÓXIMOS PASSOS:")
    print("1. Verifique se a etiqueta simples imprimiu SEM VOID")
    print("2. Se ainda aparecer VOID:")
    print("   - Verifique se as etiquetas são compatíveis")
    print("   - Calibre manualmente na impressora")
    print("   - Atualize o firmware da impressora")
    print("   - Verifique configurações do driver")
    print("\n3. Se funcionou, teste novamente o sistema CSV")

if __name__ == "__main__":
    main()
