#!/usr/bin/env python3
"""
Comparação detalhada entre ZPL atual e ZPL fornecido
"""

def compare_zpl():
    """Compara os dois ZPLs linha por linha"""
    
    # ZPL atual do sistema
    current_zpl = """CT~~CD,~CC^~CT~
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
^PR2,2
~SD15
^JUS
^LRN
^CI27
^PA0,1,1,0
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
^FT737,167^BQN,2,3
^FH\^FDLA,{QR_DATA}^FS
^FT739,355^BQN,2,3
^FH\^FDLA,{QR_DATA}^FS
^FT77,355^BQN,2,3
^FH\^FDLA,{QR_DATA}^FS
^FO31,80^GB640,280,3^FS
^FO177,81^GB0,275,3^FS
^FT353,147^A0N,23,23^FH\^CI28^FD{STYLE_NAME}^FS^CI27
^FT353,175^A0N,23,23^FH\^CI28^FD{VPM}^FS^CI27
^FT353,204^A0N,23,23^FH\^CI28^FD{COLOR}^FS^CI27
^FT353,232^A0N,23,23^FH\^CI28^FD{SIZE}^FS^CI27
^FT701,220^A0N,16,15^FB130,1,4,C^FH\^CI28^FD{PO_INFO}^FS^CI27
^FT680,238^A0N,16,15^FB151,1,4,C^FH\^CI28^FD{LOCAL_INFO}^FS^CI27
^BY2,2,39^FT222,308^BEN,,Y,N
^FH\^FD{BARCODE}^FS
^RFW,H^FD{RFID_DATA}^FS
^PQ1,0,1,Y
^XZ"""

    # ZPL fornecido pelo usuário
    provided_zpl = """CT~~CD,~CC^~CT~
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
^PR2,2
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
^FT737,167^BQN,2,3
^FH\^FDLA,123456789012^FS
^FT739,355^BQN,2,3
^FH\^FDLA,123456789012^FS
^FT77,355^BQN,2,3
^FH\^FDLA,123456789012^FS
^FO31,80^GB640,280,3^FS
^FO177,81^GB0,275,3^FS
^FT353,147^A0N,23,23^FH\^CI28^FDtxt_style_name^FS^CI27
^FT353,175^A0N,23,23^FH\^CI28^FDtxt_VPM^FS^CI27
^FT353,204^A0N,23,23^FH\^CI28^FDtxt_color^FS^CI27
^FT353,232^A0N,23,23^FH\^CI28^FDtxt_size^FS^CI27
^FT701,220^A0N,16,15^FB130,1,4,C^FH\^CI28^FDPO_infoped\5C&^FS^CI27
^FT680,238^A0N,16,15^FB151,1,4,C^FH\^CI28^FDinfoLoca\5C&^FS^CI27
^BY2,2,39^FT222,308^BEN,,Y,N
^FH\^FD1234567897899^FS
^RFW,H,2,9,1^FD197416145132046401^FS
^PQ1,0,1,Y
^XZ"""

    print("=== COMPARAÇÃO DETALHADA DOS ZPLs ===\n")
    
    current_lines = current_zpl.strip().split('\n')
    provided_lines = provided_zpl.strip().split('\n')
    
    max_lines = max(len(current_lines), len(provided_lines))
    
    print("📊 DIFERENÇAS ENCONTRADAS:\n")
    
    differences = []
    
    for i in range(max_lines):
        current = current_lines[i] if i < len(current_lines) else ""
        provided = provided_lines[i] if i < len(provided_lines) else ""
        
        if current != provided:
            differences.append({
                'line': i + 1,
                'current': current,
                'provided': provided,
                'description': get_difference_description(current, provided)
            })
    
    if differences:
        for diff in differences:
            print(f"📍 LINHA {diff['line']}:")
            print(f"   ATUAL:     {diff['current']}")
            print(f"   FORNECIDO: {diff['provided']}")
            print(f"   DIFERENÇA: {diff['description']}")
            print()
    else:
        print("✅ ZPLs são idênticos!")
    
    return differences

def get_difference_description(current, provided):
    """Descreve a diferença entre as linhas"""
    
    if not current and provided:
        return f"Linha ausente no atual: '{provided}'"
    elif current and not provided:
        return f"Linha extra no atual: '{current}'"
    elif '^RS8,,,3' in provided:
        return "Comando ^RS8,,,3 ausente no template atual"
    elif '{QR_DATA}' in current and '123456789012' in provided:
        return "QR Code: template usa {QR_DATA}, fornecido usa valor fixo"
    elif '{STYLE_NAME}' in current and 'txt_style_name' in provided:
        return "Style Name: template usa {STYLE_NAME}, fornecido usa texto fixo"
    elif '{VPM}' in current and 'txt_VPM' in provided:
        return "VPM: template usa {VPM}, fornecido usa texto fixo"
    elif '{COLOR}' in current and 'txt_color' in provided:
        return "Color: template usa {COLOR}, fornecido usa texto fixo"
    elif '{SIZE}' in current and 'txt_size' in provided:
        return "Size: template usa {SIZE}, fornecido usa texto fixo"
    elif '{PO_INFO}' in current and 'PO_infoped' in provided:
        return "PO Info: template usa {PO_INFO}, fornecido tem texto diferente"
    elif '{LOCAL_INFO}' in current and 'infoLoca' in provided:
        return "Local Info: template usa {LOCAL_INFO}, fornecido tem texto diferente"
    elif '{BARCODE}' in current and '1234567897899' in provided:
        return "Barcode: template usa {BARCODE}, fornecido usa valor fixo"
    elif '^RFW,H^FD{RFID_DATA}^FS' in current and '^RFW,H,2,9,1^FD197416145132046401^FS' in provided:
        return "RFID: template usa formato simples, fornecido tem parâmetros específicos"
    else:
        return "Conteúdo diferente"

def show_key_differences():
    """Mostra as principais diferenças"""
    print("🔍 PRINCIPAIS DIFERENÇAS:\n")
    
    print("1. 📡 COMANDO ^RS8,,,3:")
    print("   • ATUAL: Ausente")
    print("   • FORNECIDO: ^RS8,,,3")
    print("   • FUNÇÃO: Configuração de RFID")
    print()
    
    print("2. 🏷️ DADOS DINÂMICOS vs FIXOS:")
    print("   • ATUAL: Usa placeholders {STYLE_NAME}, {VPM}, etc.")
    print("   • FORNECIDO: Usa valores fixos txt_style_name, txt_VPM, etc.")
    print("   • VANTAGEM ATUAL: Dados dinâmicos do CSV")
    print()
    
    print("3. 📊 QR CODES:")
    print("   • ATUAL: {QR_DATA} (dinâmico)")
    print("   • FORNECIDO: 123456789012 (fixo)")
    print("   • VANTAGEM ATUAL: QR único por produto")
    print()
    
    print("4. 📡 COMANDO RFID:")
    print("   • ATUAL: ^RFW,H^FD{RFID_DATA}^FS")
    print("   • FORNECIDO: ^RFW,H,2,9,1^FD197416145132046401^FS")
    print("   • DIFERENÇA: Parâmetros adicionais no fornecido")
    print()
    
    print("5. 🔢 BARCODE:")
    print("   • ATUAL: {BARCODE} (sequencial dinâmico)")
    print("   • FORNECIDO: 1234567897899 (fixo)")
    print("   • VANTAGEM ATUAL: Barcode único sequencial")

def show_recommendations():
    """Mostra recomendações"""
    print("\n💡 RECOMENDAÇÕES:\n")
    
    print("✅ MANTER NO SISTEMA ATUAL:")
    print("   • Dados dinâmicos ({STYLE_NAME}, {VPM}, etc.)")
    print("   • QR Code dinâmico ({QR_DATA})")
    print("   • Barcode sequencial ({BARCODE})")
    print("   • Sistema de placeholders funcional")
    print()
    
    print("🔧 CONSIDERAR ADICIONAR:")
    print("   • ^RS8,,,3 (se necessário para RFID)")
    print("   • Parâmetros específicos no comando ^RFW")
    print("   • Ajustes nos textos fixos se necessário")
    print()
    
    print("⚠️ NÃO RECOMENDADO:")
    print("   • Substituir dados dinâmicos por fixos")
    print("   • Perder funcionalidade de placeholders")
    print("   • Usar valores hardcoded")

def show_rfid_command_difference():
    """Mostra diferença específica no comando RFID"""
    print("\n📡 DIFERENÇA NO COMANDO RFID:\n")
    
    print("🔍 ATUAL:")
    print("   ^RFW,H^FD{RFID_DATA}^FS")
    print("   • H: Formato hexadecimal")
    print("   • {RFID_DATA}: Dados dinâmicos")
    print("   • Formato simples")
    print()
    
    print("🔍 FORNECIDO:")
    print("   ^RFW,H,2,9,1^FD197416145132046401^FS")
    print("   • H: Formato hexadecimal")
    print("   • 2: Parâmetro adicional")
    print("   • 9: Parâmetro adicional")
    print("   • 1: Parâmetro adicional")
    print("   • 197416145132046401: Dados fixos")
    print()
    
    print("💡 POSSÍVEL SOLUÇÃO:")
    print("   Usar: ^RFW,H,2,9,1^FD{RFID_DATA}^FS")
    print("   • Manter parâmetros específicos")
    print("   • Manter dados dinâmicos")
    print("   • Melhor dos dois mundos")

if __name__ == "__main__":
    # Comparar ZPLs
    differences = compare_zpl()
    
    # Mostrar principais diferenças
    show_key_differences()
    
    # Mostrar diferença específica do RFID
    show_rfid_command_difference()
    
    # Mostrar recomendações
    show_recommendations()
    
    print("\n" + "="*60)
    print("🎯 RESUMO:")
    print(f"   📊 {len(differences)} diferenças encontradas")
    print("   🏆 Sistema atual: Dados dinâmicos (MELHOR)")
    print("   📝 ZPL fornecido: Dados fixos para teste")
    print("   💡 Recomendação: Manter atual + ajustar RFID")
    
    print("\n🔧 COMPARAÇÃO COMPLETA! 🔧")


