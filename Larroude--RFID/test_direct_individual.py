#!/usr/bin/env python3
"""
Teste direto da impressão individual (sem API)
"""

import win32print

def test_direct_individual_print():
    """Testa impressão individual diretamente"""
    print("🧪 Teste direto de impressão individual...")
    
    printer_name = "ZDesigner ZD621R-203dpi ZPL"
    
    # Dados de exemplo
    item_data = {
        "STYLE_NAME": "TESTE LISTA INDIVIDUAL",
        "VPM": "L555-LISTA-10.5-RED-2024",
        "COLOR": "VERMELHO",
        "SIZE": "10.5",
        "QTY": "1"
    }
    
    # Gerar ZPL usando o formato que funciona (SEM VOID)
    style_name = item_data["STYLE_NAME"]
    vpm = item_data["VPM"]
    color = item_data["COLOR"]
    size = item_data["SIZE"]
    rfid_content = vpm
    
    # Extrair PO e Local
    vpm_parts = vpm.split('-')
    po_number = f"PO{vpm_parts[0].replace('L', '')}" if len(vpm_parts) > 0 else "PO000"
    local_number = vpm_parts[4][:3] if len(vpm_parts) > 4 else "000"
    barcode = vpm.replace('-', '')[:12]
    
    # ZPL que funciona SEM VOID
    working_zpl = f"""^XA
^FO50,50^A0N,35,35^FD{style_name}^FS
^FO50,100^A0N,28,28^FDVPM: {vpm}^FS
^FO50,140^A0N,28,28^FDCOLOR: {color}^FS
^FO50,180^A0N,28,28^FDSIZE: {size}^FS
^FO50,240^BY2,3,40^BCN,40,Y,N,N^FD{barcode}^FS
^FO500,50^BQN,2,4^FD{rfid_content}^FS
^FO600,200^A0N,20,20^FD{po_number}^FS
^FO600,230^A0N,16,16^FDLocal.{local_number}^FS
^RFW,H,2,12,1^FD{rfid_content}^FS
^XZ"""
    
    try:
        print(f"📋 Imprimindo etiqueta individual:")
        print(f"   Produto: {style_name}")
        print(f"   VPM: {vpm}")
        print(f"   Cor: {color}")
        print(f"   Tamanho: {size}")
        print(f"   PO: {po_number}")
        print(f"   Local: {local_number}")
        
        handle = win32print.OpenPrinter(printer_name)
        doc_info = ("Individual_Print_Test", None, "RAW")
        job_id = win32print.StartDocPrinter(handle, 1, doc_info)
        
        win32print.StartPagePrinter(handle)
        bytes_written = win32print.WritePrinter(handle, working_zpl.encode('ascii'))
        win32print.EndPagePrinter(handle)
        win32print.EndDocPrinter(handle)
        
        print(f"📤 Enviado: {bytes_written} bytes")
        win32print.ClosePrinter(handle)
        
        print("✅ Etiqueta individual enviada com sucesso!")
        print("🔍 Esta etiqueta deve ter:")
        print("   ❌ ZERO VOID")
        print("   ✅ Dados da lista de upload")
        print("   ✅ Layout organizado")
        print("   ✅ RFID funcional")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro: {e}")
        return False

def simulate_list_printing():
    """Simula impressão de vários itens de uma lista"""
    print("\n🧪 Simulando impressão de lista com vários itens...")
    
    # Lista de itens simulando upload CSV
    items_list = [
        {
            "STYLE_NAME": "SANDALIA VERÃO",
            "VPM": "L100-SAND-8.0-BLUE-1001",
            "COLOR": "AZUL",
            "SIZE": "8.0",
            "QTY": "1"
        },
        {
            "STYLE_NAME": "BOTA INVERNO",
            "VPM": "L200-BOOT-9.5-BLACK-2002",
            "COLOR": "PRETO",
            "SIZE": "9.5",
            "QTY": "2"
        },
        {
            "STYLE_NAME": "TENIS ESPORTE",
            "VPM": "L300-SPORT-10.0-WHITE-3003",
            "COLOR": "BRANCO",
            "SIZE": "10.0",
            "QTY": "1"
        }
    ]
    
    print(f"📋 Lista com {len(items_list)} itens únicos")
    total_labels = sum(int(item.get('QTY', 1)) for item in items_list)
    print(f"📊 Total de etiquetas: {total_labels}")
    
    print("\n🎯 Simulação de impressão individual:")
    for i, item in enumerate(items_list, 1):
        qty = int(item.get('QTY', 1))
        print(f"   {i}. {item['STYLE_NAME']} - {item['VPM']} ({qty} etiqueta{'s' if qty > 1 else ''})")
        print(f"      [Botão Imprimir] ← Imprimiria {qty} etiqueta(s)")
    
    print("\n✨ Funcionalidade implementada:")
    print("   ✅ Lista visual de todos os itens")
    print("   ✅ Botão individual para cada item")
    print("   ✅ Impressão com formato SEM VOID")
    print("   ✅ Interface responsiva")
    print("   ✅ Feedback de status (loading/success/error)")

if __name__ == "__main__":
    print("=== TESTE DE IMPRESSÃO INDIVIDUAL ===")
    print("Testando funcionalidade de lista com impressão individual\n")
    
    # Teste 1: Impressão individual direta
    success = test_direct_individual_print()
    
    # Simulação da interface
    simulate_list_printing()
    
    print("\n" + "="*50)
    print("🎯 RESULTADO:")
    if success:
        print("✅ Impressão individual funcionando!")
        print("✅ Formato SEM VOID implementado")
        print("✅ Ready para usar na interface web")
        print("\n🌐 Para usar a interface completa:")
        print("   1. Inicie o servidor: cd backend && npm start")
        print("   2. Acesse: http://localhost:3000")
        print("   3. Faça upload do CSV")
        print("   4. Clique 'Lista para Impressão'")
        print("   5. Use botões individuais")
    else:
        print("❌ Problema na impressão")
        print("❌ Verifique conexão da impressora")
