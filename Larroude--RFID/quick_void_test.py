#!/usr/bin/env python3
"""
Teste rápido para encontrar a causa do VOID
"""

import win32print
import time

def test_printer_settings():
    """Verifica configurações da impressora"""
    print("🔍 Verificando configurações da impressora...")
    
    printer_name = "ZDesigner ZD621R-203dpi ZPL"
    
    try:
        handle = win32print.OpenPrinter(printer_name)
        info = win32print.GetPrinter(handle, 2)
        
        print(f"📋 Impressora: {info['pPrinterName']}")
        print(f"📋 Porta: {info['pPortName']}")
        print(f"📋 Driver: {info['pDriverName']}")
        print(f"📋 Status: {info['Status']}")
        print(f"📋 Atributos: {info['Attributes']}")
        
        # Verificar configurações específicas
        try:
            # Tentar obter configurações do driver
            driver_info = win32print.GetPrinter(handle, 8)
            print(f"📋 Configurações do driver disponíveis")
        except:
            print("📋 Configurações do driver não acessíveis")
        
        win32print.ClosePrinter(handle)
        
    except Exception as e:
        print(f"❌ Erro ao verificar configurações: {e}")

def test_media_calibration():
    """Força calibração de mídia"""
    print("\n🔧 Forçando calibração de mídia...")
    
    printer_name = "ZDesigner ZD621R-203dpi ZPL"
    
    # Comandos específicos para calibração de mídia
    calibration_zpl = """~JA

^XA
^JUS
^XZ

^XA
^JUF
^XZ

^XA
^MNN
^MD15
^PR4
^XZ"""
    
    try:
        handle = win32print.OpenPrinter(printer_name)
        doc_info = ("Media_Calibration", None, "RAW")
        job_id = win32print.StartDocPrinter(handle, 1, doc_info)
        
        win32print.StartPagePrinter(handle)
        bytes_written = win32print.WritePrinter(handle, calibration_zpl.encode('ascii'))
        win32print.EndPagePrinter(handle)
        win32print.EndDocPrinter(handle)
        
        print(f"✅ Calibração enviada: {bytes_written} bytes")
        win32print.ClosePrinter(handle)
        
        print("⏳ Aguardando calibração (10s)...")
        time.sleep(10)
        
    except Exception as e:
        print(f"❌ Erro na calibração: {e}")

def test_ultra_simple():
    """Teste ultra simples - só texto"""
    print("\n🧪 Teste ultra simples...")
    
    printer_name = "ZDesigner ZD621R-203dpi ZPL"
    
    ultra_simple = """^XA
^FO100,100^A0N,50,50^FDOK^FS
^XZ"""
    
    try:
        handle = win32print.OpenPrinter(printer_name)
        doc_info = ("Ultra_Simple", None, "RAW")
        job_id = win32print.StartDocPrinter(handle, 1, doc_info)
        
        win32print.StartPagePrinter(handle)
        bytes_written = win32print.WritePrinter(handle, ultra_simple.encode('ascii'))
        win32print.EndPagePrinter(handle)
        win32print.EndDocPrinter(handle)
        
        print(f"✅ Ultra simples enviado: {bytes_written} bytes")
        win32print.ClosePrinter(handle)
        
    except Exception as e:
        print(f"❌ Erro: {e}")

def test_alternative_approach():
    """Testa abordagem alternativa com configurações específicas"""
    print("\n🔄 Teste com configurações específicas...")
    
    printer_name = "ZDesigner ZD621R-203dpi ZPL"
    
    # ZPL com configurações muito específicas
    specific_zpl = """^XA
^MMT
^PW812
^LL0406
^LS0
^FT50,100^A0N,50,50^FH\\^FDTESTE ESPECIFICO^FS
^FT50,200^A0N,30,30^FH\\^FDSEM VOID^FS
^PQ1,0,1,Y
^XZ"""
    
    try:
        handle = win32print.OpenPrinter(printer_name)
        doc_info = ("Specific_Config", None, "RAW")
        job_id = win32print.StartDocPrinter(handle, 1, doc_info)
        
        win32print.StartPagePrinter(handle)
        bytes_written = win32print.WritePrinter(handle, specific_zpl.encode('ascii'))
        win32print.EndPagePrinter(handle)
        win32print.EndDocPrinter(handle)
        
        print(f"✅ Configurações específicas enviadas: {bytes_written} bytes")
        win32print.ClosePrinter(handle)
        
    except Exception as e:
        print(f"❌ Erro: {e}")

def check_void_causes():
    """Verifica possíveis causas do VOID"""
    print("\n🔍 Analisando possíveis causas do VOID...")
    
    print("📋 POSSÍVEIS CAUSAS DO VOID:")
    print("1. 🏷️ Tipo de etiqueta incorreto:")
    print("   - Térmica direta vs Transferência térmica")
    print("   - Tamanho incompatível")
    print("   - Etiquetas de baixa qualidade")
    
    print("\n2. ⚙️ Configurações da impressora:")
    print("   - Densidade muito alta ou baixa")
    print("   - Velocidade inadequada")
    print("   - Calibração incorreta")
    
    print("\n3. 🔧 Problemas técnicos:")
    print("   - Cabeça de impressão suja")
    print("   - Sensor de etiqueta desalinhado")
    print("   - Firmware desatualizado")
    
    print("\n4. 💾 Driver/Software:")
    print("   - Driver incorreto")
    print("   - Configurações do Windows")
    print("   - Modo de impressão")

def main():
    print("=== DIAGNÓSTICO RÁPIDO DO VOID ===\n")
    
    # 1. Verificar configurações
    test_printer_settings()
    
    # 2. Calibrar mídia
    test_media_calibration()
    
    # 3. Teste ultra simples
    test_ultra_simple()
    
    # 4. Aguardar um pouco
    print("\n⏳ Aguardando 5 segundos...")
    time.sleep(5)
    
    # 5. Teste com configurações específicas
    test_alternative_approach()
    
    # 6. Mostrar possíveis causas
    check_void_causes()
    
    print("\n" + "="*60)
    print("🎯 PRÓXIMOS PASSOS:")
    print("1. Verifique as etiquetas que acabaram de imprimir")
    print("2. Se ainda aparecer VOID:")
    print("   → Acesse o painel da impressora")
    print("   → Menu → Calibrate → Auto Calibrate")
    print("   → Ou tente etiquetas de outro fornecedor")
    print("3. Se alguma etiqueta saiu sem VOID:")
    print("   → Use esse formato no sistema")

if __name__ == "__main__":
    main()
