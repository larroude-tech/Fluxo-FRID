#!/usr/bin/env python3
"""
Teste direto da impressão de etiquetas CSV usando o método que funciona
"""

import win32print
import time

def test_csv_print():
    """Testa impressão de etiqueta CSV"""
    print("🧪 Testando impressão de etiqueta CSV...")
    
    printer_name = "ZDesigner ZD621R-203dpi ZPL"
    
    # ZPL de exemplo baseado no formato CSV
    zpl_command = """CT~~CD,~CC^~CT~
^XA
~TA000
~JSN
^LT0
^MNW
^MTT
^PON
^PMN
^LH0,0
^JMA
^PR4,4
~SD15
^JUS
^LRN
^CI27
^PA0,1,1,0
^RS8,,,3
^XZ
^XA
^MMT
^PW831
^LL320
^LS0
^BY2,3,37^FT287,169^BCN,,Y,N
^FH\\^FD>;VPM123456>64^FS
^RFW,H,1,2,1^FD3000^FS
^RFW,H,2,12,1^FDVPM123456^FS
^FO50,50^A0N,30,30^FDTeste CSV^FS
^FO50,90^A0N,25,25^FDCor: PRETO^FS
^FO50,130^A0N,25,25^FDSize: 38^FS
^FO50,170^A0N,20,20^FDVPM: VPM123456^FS
^PQ1,0,1,Y
^XZ"""
    
    try:
        # Abrir impressora
        handle = win32print.OpenPrinter(printer_name)
        
        # Configurar para modo RAW
        doc_info = ("CSV_Test_Print", None, "RAW")
        
        # Iniciar job
        job_id = win32print.StartDocPrinter(handle, 1, doc_info)
        
        print(f"📄 Job iniciado: {job_id}")
        
        # Enviar dados
        win32print.StartPagePrinter(handle)
        bytes_written = win32print.WritePrinter(handle, zpl_command.encode('ascii'))
        win32print.EndPagePrinter(handle)
        win32print.EndDocPrinter(handle)
        
        print(f"📤 Bytes enviados: {bytes_written}")
        
        # Verificar status
        info = win32print.GetPrinter(handle, 2)
        print(f"📊 Jobs na fila: {info['cJobs']}")
        
        win32print.ClosePrinter(handle)
        
        print("✅ Etiqueta CSV enviada com sucesso!")
        print("🔍 Verifique se a etiqueta foi impressa com:")
        print("   - Texto: 'Teste CSV'")
        print("   - Cor: 'PRETO'")
        print("   - Tamanho: '38'")
        print("   - VPM: 'VPM123456'")
        print("   - Código de barras")
        print("   - Dados RFID gravados")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro ao imprimir etiqueta CSV: {e}")
        return False

if __name__ == "__main__":
    print("=== Teste de Impressão CSV - Zebra ZD621R ===")
    test_csv_print()
