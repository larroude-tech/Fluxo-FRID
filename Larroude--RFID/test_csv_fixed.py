#!/usr/bin/env python3
"""
Teste da correção do ZPL para eliminar o problema "VOID"
"""

import win32print
import time

def test_fixed_csv_zpl():
    """Testa o novo ZPL corrigido"""
    print("🧪 Testando ZPL CSV corrigido...")
    
    printer_name = "ZDesigner ZD621R-203dpi ZPL"
    
    # Dados de exemplo
    style_name = "TESTE CORRIGIDO"
    vpm = "TEST123456"
    color = "AZUL"
    size = "40"
    rfid_content = "RFID_TEST_DATA"
    
    # ZPL corrigido (sem comandos problemáticos)
    zpl_command = f"""^XA
^CI28
^LH0,0
^MD30
^PR5
^PW812
^LL406

^FO12,12^GB788,382,2,B,24^FS
^FO36,48^GB580,290,2,B,14^FS

^FO60,86^GB80,80,2,B,8^FS

^FO60,235^BQN,2,5^FD{rfid_content}^FS

^FO170,66^GB2,240,2^FS

^CF0,30
^FO190,78^FB400,2,0,L,0^FD{style_name}^FS
^CF0,26
^FO190,138^FB400,1,0,L,0^FDVPM: {vpm}^FS
^FO190,178^FB400,2,0,L,0^FDCOLOR: {color}^FS

^FO190,218^A0N,28,28^FDSIZE:^FS
^CF0,34
^FO260,218^FB330,1,0,L,0^FD{size}^FS

^BY2,3,60
^FO190,270^BCN,60,Y,N,N^FD{vpm}^FS

^FO654,60^BQN,2,6^FD{rfid_content}-TOP^FS

^FO642,184^GB150,66,2,B,16^FS
^CF0,24
^FO652,198^FB130,2,0,C,0^FDPO: {vpm[:8]}\\&Local.SP^FS

^FO654,285^BQN,2,6^FD{rfid_content}-BOT^FS

^RFW,H,1,2,1^FD3000^FS
^RFW,H,2,12,1^FD{rfid_content}^FS

^XZ"""
    
    try:
        # Abrir impressora
        handle = win32print.OpenPrinter(printer_name)
        
        # Configurar para modo RAW
        doc_info = ("CSV_Fixed_Test", None, "RAW")
        
        # Iniciar job
        job_id = win32print.StartDocPrinter(handle, 1, doc_info)
        
        print(f"📄 Job iniciado: {job_id}")
        
        # Enviar dados
        win32print.StartPagePrinter(handle)
        bytes_written = win32print.WritePrinter(handle, zpl_command.encode('ascii'))
        win32print.EndPagePrinter(handle)
        win32print.EndDocPrinter(handle)
        
        print(f"📤 Bytes enviados: {bytes_written}")
        
        win32print.ClosePrinter(handle)
        
        print("✅ Etiqueta CSV CORRIGIDA enviada!")
        print("🔍 Verifique se agora imprime:")
        print("   - ❌ SEM 'VOID'")
        print("   - ✅ Texto: 'TESTE CORRIGIDO'")
        print("   - ✅ VPM: 'TEST123456'")
        print("   - ✅ Cor: 'AZUL'")
        print("   - ✅ Tamanho: '40'")
        print("   - ✅ QR codes funcionais")
        print("   - ✅ Código de barras")
        print("   - ✅ Layout estruturado")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro ao imprimir etiqueta corrigida: {e}")
        return False

if __name__ == "__main__":
    print("=== Teste ZPL Corrigido - SEM VOID ===")
    test_fixed_csv_zpl()
