#!/usr/bin/env python3
"""
Debug: Comparar ZPL do sistema web vs Python direto
"""

import requests
import json
import win32print

def get_system_zpl():
    """Captura o ZPL que o sistema web está gerando"""
    print("🔍 Capturando ZPL do sistema web...")
    
    # Dados de teste idênticos ao teste Python
    test_data = {
        "STYLE_NAME": "TESTE SISTEMA WEB",
        "VPM": "L777-WEB-TEST-BLUE-8888",
        "COLOR": "AZUL SISTEMA",
        "SIZE": "9.5",
        "QTY": "1"
    }
    
    try:
        # Tentar capturar via API (se servidor estiver rodando)
        url = "http://localhost:3000/api/print-individual"
        response = requests.post(url, json={"data": [test_data], "quantity": 1})
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Sistema web respondeu")
            print(f"📊 Resultado: {result.get('message', 'N/A')}")
            return True
        else:
            print(f"❌ Erro HTTP: {response.status_code}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("⚠️ Servidor não está rodando")
        return False
    except Exception as e:
        print(f"❌ Erro: {e}")
        return False

def generate_python_zpl():
    """Gera ZPL usando mesma lógica do teste Python que funcionou"""
    print("\n🔧 Gerando ZPL com lógica Python que funciona...")
    
    # Dados idênticos
    test_data = {
        "STYLE_NAME": "TESTE PYTHON DIRETO",
        "VPM": "L777-PY-TEST-BLUE-8888", 
        "COLOR": "AZUL PYTHON",
        "SIZE": "9.5"
    }
    
    # ZPL que funcionou no teste Python (sem VOID)
    working_zpl = f"""CT~~CD,~CC^~CT~
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
^LL376
^LS0
^FPH,3^FT187,147^A0N,20,23^FH\^CI28^FDSTYLE NAME:^FS^CI27
^FPH,3^FT188,176^A0N,20,23^FH\^CI28^FDVPM:^FS^CI27
^FPH,3^FT187,204^A0N,20,23^FH\^CI28^FDCOLOR:^FS^CI27
^FPH,3^FT187,234^A0N,20,23^FH\^CI28^FDSIZE:^FS^CI27
^FO353,147^A0N,23,23^FH\^CI28^FD{test_data["STYLE_NAME"]}^FS^CI27
^FO353,175^A0N,23,23^FH\^CI28^FD{test_data["VPM"]}^FS^CI27
^FO353,204^A0N,23,23^FH\^CI28^FD{test_data["COLOR"]}^FS^CI27
^FO353,232^A0N,23,23^FH\^CI28^FD{test_data["SIZE"]}^FS^CI27
^FO31,80^GB640,280,3^FS
^FO177,81^GB0,275,3^FS
^CI28
^FT800,360^A0N,18,18^FB300,1,0,R^FDGRAVADO RFID: SUCESSO^FS
^CI27
^PQ1,0,1,Y
^XZ"""
    
    return working_zpl

def generate_system_template_zpl():
    """Gera ZPL usando o template do sistema"""
    print("\n🔧 Gerando ZPL usando template do sistema...")
    
    # Carregar template do sistema
    try:
        with open('backend/TEMPLATE_LARROUD_OFICIAL.zpl', 'r', encoding='utf-8') as f:
            template = f.read()
    except FileNotFoundError:
        print("❌ Template do sistema não encontrado!")
        return None
    
    # Dados de teste
    test_data = {
        "STYLE_NAME": "TESTE TEMPLATE SISTEMA",
        "VPM": "L777-TPL-TEST-BLUE-8888",
        "COLOR": "AZUL TEMPLATE",
        "SIZE": "9.5"
    }
    
    # Processar como o sistema faz
    vpm_parts = test_data["VPM"].split('-')
    po_number = f"PO{vpm_parts[0].replace('L', '')}" if len(vpm_parts) > 0 else "PO000"
    local_number = vpm_parts[4][:3] if len(vpm_parts) > 4 else "000"
    barcode = test_data["VPM"].replace('-', '')[:12]
    rfid_content = test_data["VPM"]
    rfid_status = "SUCESSO"
    
    # Substituir variáveis como o sistema faz
    system_zpl = template.replace('{STYLE_NAME}', test_data["STYLE_NAME"]) \
                        .replace('{VPM}', test_data["VPM"]) \
                        .replace('{COLOR}', test_data["COLOR"]) \
                        .replace('{SIZE}', test_data["SIZE"]) \
                        .replace('{PO_INFO}', po_number) \
                        .replace('{LOCAL_INFO}', f'Local.{local_number}') \
                        .replace('{BARCODE}', barcode) \
                        .replace('{RFID_DATA}', rfid_content) \
                        .replace('{QR_DATA_1}', rfid_content) \
                        .replace('{QR_DATA_2}', rfid_content) \
                        .replace('{QR_DATA_3}', rfid_content) \
                        .replace('{RFID_STATUS}', rfid_status)
    
    return system_zpl

def compare_and_test_zpl():
    """Compara e testa os dois ZPL"""
    print("\n🆚 Comparando ZPL Python vs Sistema...")
    
    # Gerar ambos os ZPL
    python_zpl = generate_python_zpl()
    system_zpl = generate_system_template_zpl()
    
    if not system_zpl:
        return False
    
    # Salvar para comparação
    with open('ZPL_PYTHON_FUNCIONA.zpl', 'w', encoding='ascii', errors='ignore') as f:
        f.write(python_zpl)
    
    with open('ZPL_SISTEMA_PROBLEMA.zpl', 'w', encoding='ascii', errors='ignore') as f:
        f.write(system_zpl)
    
    print("💾 Arquivos salvos para comparação:")
    print("   📄 ZPL_PYTHON_FUNCIONA.zpl - Funciona SEM VOID")
    print("   📄 ZPL_SISTEMA_PROBLEMA.zpl - Sistema atual")
    
    # Testar ambos na impressora
    printer_name = "ZDesigner ZD621R-203dpi ZPL"
    
    print("\n🖨️ Testando Python ZPL (que funciona)...")
    try:
        handle = win32print.OpenPrinter(printer_name)
        doc_info = ("Python_ZPL_Test", None, "RAW")
        job_id = win32print.StartDocPrinter(handle, 1, doc_info)
        
        win32print.StartPagePrinter(handle)
        bytes_written = win32print.WritePrinter(handle, python_zpl.encode('ascii', errors='ignore'))
        win32print.EndPagePrinter(handle)
        win32print.EndDocPrinter(handle)
        win32print.ClosePrinter(handle)
        
        print(f"✅ Python ZPL enviado: {bytes_written} bytes")
    except Exception as e:
        print(f"❌ Erro Python ZPL: {e}")
    
    print("\n🖨️ Testando Sistema ZPL...")
    try:
        handle = win32print.OpenPrinter(printer_name)
        doc_info = ("System_ZPL_Test", None, "RAW")
        job_id = win32print.StartDocPrinter(handle, 1, doc_info)
        
        win32print.StartPagePrinter(handle)
        bytes_written = win32print.WritePrinter(handle, system_zpl.encode('ascii', errors='ignore'))
        win32print.EndPagePrinter(handle)
        win32print.EndDocPrinter(handle)
        win32print.ClosePrinter(handle)
        
        print(f"✅ Sistema ZPL enviado: {bytes_written} bytes")
    except Exception as e:
        print(f"❌ Erro Sistema ZPL: {e}")
    
    return True

if __name__ == "__main__":
    print("=== DEBUG: SISTEMA WEB vs PYTHON DIRETO ===")
    print("Investigando por que Python funciona e sistema web não\n")
    
    # Testar sistema web
    system_working = get_system_zpl()
    
    # Comparar ZPL
    comparison_done = compare_and_test_zpl()
    
    print("\n" + "="*50)
    print("🎯 DIAGNÓSTICO:")
    print("✅ Python direto: SEM VOID")
    print("❌ Sistema web: COM VOID")
    print("\n🔍 PRÓXIMOS PASSOS:")
    print("1. Compare os arquivos ZPL gerados")
    print("2. Identifique diferenças entre eles")
    print("3. Ajuste o sistema para usar ZPL que funciona")
    print("4. Verifique as etiquetas físicas impressas")
    
    if comparison_done:
        print("\n📄 ARQUIVOS PARA ANÁLISE:")
        print("   ZPL_PYTHON_FUNCIONA.zpl - Use este como referência")
        print("   ZPL_SISTEMA_PROBLEMA.zpl - Identifique diferenças")
        print("\n🔧 CORREÇÃO:")
        print("   Vou ajustar o sistema para usar o ZPL que funciona")

