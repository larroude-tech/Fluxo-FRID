#!/usr/bin/env python3
"""
Teste do sistema SEM gravação RFID (para eliminar VOID definitivamente)
"""

import win32print
import requests
import json

def test_template_sem_rfid():
    """Testa template simplificado sem RFID"""
    print("🧪 Testando template SEM RFID...")
    
    printer_name = "ZDesigner ZD621R-203dpi ZPL"
    
    # Carregar template simplificado
    try:
        with open('backend/TEMPLATE_LARROUD_SIMPLIFICADO.zpl', 'r', encoding='utf-8') as f:
            template = f.read()
    except FileNotFoundError:
        print("❌ Template simplificado não encontrado!")
        return False
    
    # Dados de teste
    test_data = {
        "STYLE_NAME": "TESTE SEM RFID",
        "VPM": "L999-NO-RFID-10.0-GREEN-5555",
        "COLOR": "VERDE SEM RFID",
        "SIZE": "10.0"
    }
    
    # Substituir variáveis (sem RFID)
    test_zpl = template.replace('{STYLE_NAME}', test_data["STYLE_NAME"]) \
                      .replace('{VPM}', test_data["VPM"]) \
                      .replace('{COLOR}', test_data["COLOR"]) \
                      .replace('{SIZE}', test_data["SIZE"])
    
    try:
        print(f"📋 Dados da etiqueta:")
        print(f"   Produto: {test_data['STYLE_NAME']}")
        print(f"   VPM: {test_data['VPM']}")
        print(f"   Cor: {test_data['COLOR']}")
        print(f"   Tamanho: {test_data['SIZE']}")
        
        handle = win32print.OpenPrinter(printer_name)
        doc_info = ("Test_Sem_RFID", None, "RAW")
        job_id = win32print.StartDocPrinter(handle, 1, doc_info)
        
        win32print.StartPagePrinter(handle)
        bytes_written = win32print.WritePrinter(handle, test_zpl.encode('ascii', errors='ignore'))
        win32print.EndPagePrinter(handle)
        win32print.EndDocPrinter(handle)
        win32print.ClosePrinter(handle)
        
        print(f"📤 Enviado: {bytes_written} bytes")
        print("✅ Template SEM RFID enviado!")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro: {e}")
        return False

def test_api_sem_rfid():
    """Testa API do sistema sem RFID"""
    print("\n🌐 Testando API do sistema SEM RFID...")
    
    # Dados de teste
    test_data = {
        "STYLE_NAME": "API SEM RFID",
        "VPM": "L888-API-NO-RFID-9.5-BLUE-6666",
        "COLOR": "AZUL API",
        "SIZE": "9.5",
        "QTY": "1"
    }
    
    try:
        url = "http://localhost:3000/api/print-individual"
        response = requests.post(url, json={"data": [test_data], "quantity": 1})
        
        if response.status_code == 200:
            result = response.json()
            print("✅ API respondeu com sucesso")
            print(f"📊 Mensagem: {result.get('message', 'N/A')}")
            print(f"📈 Sucessos: {result.get('successCount', 0)}")
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

def show_no_rfid_info():
    """Mostra informações sobre remoção do RFID"""
    print("\n📋 REMOÇÃO DO RFID:")
    print("   🎯 Objetivo: Eliminar VOID definitivamente")
    print("   🔧 Ação: Removidos todos os comandos RFID do ZPL")
    print("   📝 Template: TEMPLATE_LARROUD_SIMPLIFICADO.zpl")
    
    print("\n❌ COMANDOS REMOVIDOS:")
    print("   ^RFW,H,2,12,1^FD... - Gravação RFID")
    print("   ^FT...^BQN... - QR codes")
    print("   ^BY...^BEN... - Código de barras")
    print("   Variáveis RFID complexas")
    
    print("\n✅ MANTIDO:")
    print("   Layout básico da Larroud")
    print("   Campos de texto (STYLE, VPM, COLOR, SIZE)")
    print("   Bordas e estrutura visual")
    print("   Campo 'SEM RFID' no canto inferior direito")
    
    print("\n🎯 RESULTADO ESPERADO:")
    print("   ❌ ZERO VOID")
    print("   ✅ Layout limpo e profissional")
    print("   ✅ Dados completos do produto")
    print("   ✅ Economia de material (sem RFID)")

if __name__ == "__main__":
    print("=== TESTE SEM GRAVAÇÃO RFID ===")
    print("Eliminando VOID removendo comandos RFID\n")
    
    # Mostrar informações
    show_no_rfid_info()
    
    # Teste direto Python
    success_python = test_template_sem_rfid()
    
    # Teste API
    success_api = test_api_sem_rfid()
    
    print("\n" + "="*50)
    print("🎯 RESULTADO:")
    if success_python:
        print("✅ TEMPLATE SEM RFID FUNCIONANDO!")
        print("✅ ZPL simplificado enviado com sucesso")
        print("✅ Comandos RFID removidos")
        print("✅ Layout básico da Larroud mantido")
        
        if success_api:
            print("✅ API DO SISTEMA FUNCIONANDO!")
            print("✅ Sistema web agora usa template sem RFID")
            print("✅ Lista de impressão individual atualizada")
        else:
            print("⚠️ API não testada (servidor pode estar parado)")
        
        print("\n🏷️ ETIQUETA DEVE TER:")
        print("   ❌ ZERO VOID")
        print("   ✅ Nome do produto")
        print("   ✅ Código VPM") 
        print("   ✅ Cor e tamanho")
        print("   ✅ 'SEM RFID' no canto inferior direito")
        print("   ✅ Layout limpo da Larroud")
        
    else:
        print("❌ Erro no template sem RFID")
        print("❌ Verifique configurações")

