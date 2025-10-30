#!/usr/bin/env python3
"""
Salva ZPL para comparação com ZebraDesigner
"""

def save_current_system_zpl():
    """Salva o ZPL que o sistema atual está gerando"""
    print("💾 Salvando ZPL do sistema atual...")
    
    # Simular dados como o sistema faz
    item_data = {
        "STYLE_NAME": "SANDALIA LARROUD",
        "VPM": "L456-SAND-9.0-BROWN-1234",
        "COLOR": "MARROM",
        "SIZE": "9.0"
    }
    
    # Carregar template como o sistema faz
    try:
        with open('backend/TEMPLATE_LARROUD_OFICIAL.zpl', 'r', encoding='utf-8') as f:
            template = f.read()
    except FileNotFoundError:
        print("❌ Template não encontrado!")
        return
    
    # Processar dados como o sistema faz
    style_name = item_data["STYLE_NAME"]
    vpm = item_data["VPM"]
    color = item_data["COLOR"]
    size = item_data["SIZE"]
    rfid_content = vpm
    
    # Extrair PO e Local como o sistema faz
    vpm_parts = vpm.split('-')
    po_number = f"PO{vpm_parts[0].replace('L', '')}" if len(vpm_parts) > 0 else "PO000"
    local_number = vpm_parts[4][:3] if len(vpm_parts) > 4 else "000"
    barcode = vpm.replace('-', '')[:12]
    
    # Substituir variáveis como o sistema faz
    system_zpl = template.replace('{STYLE_NAME}', style_name) \
                        .replace('{VPM}', vpm) \
                        .replace('{COLOR}', color) \
                        .replace('{SIZE}', size) \
                        .replace('{PO_INFO}', po_number) \
                        .replace('{LOCAL_INFO}', f'Local.{local_number}') \
                        .replace('{BARCODE}', barcode) \
                        .replace('{RFID_DATA}', rfid_content) \
                        .replace('{QR_DATA_1}', rfid_content) \
                        .replace('{QR_DATA_2}', rfid_content) \
                        .replace('{QR_DATA_3}', rfid_content)
    
    # Salvar em arquivo
    with open('ZPL_SISTEMA_ATUAL.zpl', 'w', encoding='ascii', errors='ignore') as f:
        f.write(system_zpl)
    
    print("✅ ZPL do sistema salvo em: ZPL_SISTEMA_ATUAL.zpl")
    
    # Também salvar o template original para comparação
    try:
        with open('modelo_zpl_larroude.prn', 'r', encoding='utf-8') as f:
            original = f.read()
        
        with open('ZPL_ORIGINAL_LARROUD.zpl', 'w', encoding='ascii', errors='ignore') as f:
            f.write(original)
        
        print("✅ ZPL original salvo em: ZPL_ORIGINAL_LARROUD.zpl")
    except FileNotFoundError:
        print("⚠️ Arquivo original modelo_zpl_larroude.prn não encontrado")
    
    return system_zpl

def create_test_variants():
    """Cria variantes do ZPL para teste"""
    print("\n🧪 Criando variantes para teste...")
    
    base_data = {
        "STYLE_NAME": "TESTE VARIANTE",
        "VPM": "L777-VAR-8.5-GREEN-9999",
        "COLOR": "VERDE",
        "SIZE": "8.5"
    }
    
    # Variante 1: Sem comandos de configuração complexos
    variant1 = f"""^XA
^PW831
^LL376
^FO187,147^A0N,20,23^FDSTYLE NAME:^FS
^FO188,176^A0N,20,23^FDVPM:^FS
^FO187,204^A0N,20,23^FDCOLOR:^FS
^FO187,234^A0N,20,23^FDSIZE:^FS
^FO353,147^A0N,23,23^FD{base_data["STYLE_NAME"]}^FS
^FO353,175^A0N,23,23^FD{base_data["VPM"]}^FS
^FO353,204^A0N,23,23^FD{base_data["COLOR"]}^FS
^FO353,232^A0N,23,23^FD{base_data["SIZE"]}^FS
^FO31,80^GB640,280,3^FS
^FO177,81^GB0,275,3^FS
^XZ"""
    
    # Variante 2: Com QR codes mas sem RFID
    variant2 = f"""^XA
^PW831
^LL376
^FO187,147^A0N,20,23^FDSTYLE NAME:^FS
^FO353,147^A0N,23,23^FD{base_data["STYLE_NAME"]}^FS
^FO353,175^A0N,23,23^FD{base_data["VPM"]}^FS
^FO737,167^BQN,2,3^FDLA,{base_data["VPM"]}^FS
^FO31,80^GB640,280,3^FS
^XZ"""
    
    # Variante 3: Só texto, sem gráficos
    variant3 = f"""^XA
^FO100,100^A0N,30,30^FD{base_data["STYLE_NAME"]}^FS
^FO100,150^A0N,25,25^FD{base_data["VPM"]}^FS
^FO100,200^A0N,25,25^FD{base_data["COLOR"]} - {base_data["SIZE"]}^FS
^XZ"""
    
    variants = [
        ("VARIANTE_1_SEM_CONFIG.zpl", variant1),
        ("VARIANTE_2_QR_SEM_RFID.zpl", variant2),
        ("VARIANTE_3_SO_TEXTO.zpl", variant3)
    ]
    
    for filename, zpl_content in variants:
        with open(filename, 'w', encoding='ascii', errors='ignore') as f:
            f.write(zpl_content)
        print(f"✅ Criado: {filename}")

if __name__ == "__main__":
    print("=== COMPARAÇÃO DE ZPL ===")
    print("Salvando arquivos para comparar com ZebraDesigner\n")
    
    # Salvar ZPL do sistema atual
    save_current_system_zpl()
    
    # Criar variantes para teste
    create_test_variants()
    
    print("\n" + "="*50)
    print("📁 ARQUIVOS CRIADOS:")
    print("   📄 ZPL_SISTEMA_ATUAL.zpl - O que nosso sistema gera")
    print("   📄 ZPL_ORIGINAL_LARROUD.zpl - Template original")
    print("   📄 VARIANTE_1_SEM_CONFIG.zpl - Sem configs complexos")
    print("   📄 VARIANTE_2_QR_SEM_RFID.zpl - QR sem RFID")
    print("   📄 VARIANTE_3_SO_TEXTO.zpl - Apenas texto")
    
    print("\n🎯 PRÓXIMOS PASSOS:")
    print("1. Abra estes arquivos no ZebraDesigner")
    print("2. Veja qual NÃO gera VOID no designer")
    print("3. Compare com as etiquetas físicas impressas")
    print("4. Me informe qual formato funciona")
    print("5. Vou ajustar o sistema para usar o formato correto")
