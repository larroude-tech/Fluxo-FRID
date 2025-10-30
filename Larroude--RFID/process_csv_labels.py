#!/usr/bin/env python3
"""
Processador de etiquetas CSV - Zebra ZD621R
Usa o ZPL fornecido pelo usuário para gerar etiquetas a partir do arquivo exemplo.csv
ATUALIZADO: Agora com conversão hexadecimal para RFID
"""

import os
import subprocess
import tempfile
import time
import csv
import win32print

def string_to_hex(text):
    """Converte string para hexadecimal (mesmo algoritmo do Node.js)"""
    if not text:
        raise ValueError("Texto não pode estar vazio")
    
    hex_result = ""
    for char in text:
        char_code = ord(char)
        hex_value = format(char_code, '02X')
        hex_result += hex_value
    
    return hex_result

def validate_rfid_data(data):
    """Valida dados RFID"""
    if not data or not isinstance(data, str):
        raise ValueError("Dados RFID são obrigatórios e devem ser string")
    
    if len(data) == 0:
        raise ValueError("Dados RFID não podem estar vazios")
    
    if len(data) > 50:
        raise ValueError("Dados RFID muito longos (máximo 50 caracteres)")
    
    # Verificar se contém apenas caracteres válidos (alfanuméricos)
    import re
    if not re.match(r'^[A-Za-z0-9]+$', data):
        raise ValueError("Dados RFID contêm caracteres inválidos (apenas A-Z, a-z, 0-9 permitidos)")
    
    return True

def load_csv_data():
    """Carrega dados do arquivo exemplo.csv"""
    print("📂 Carregando dados do arquivo exemplo.csv...")
    
    labels = []
    try:
        with open('exemplo.csv', 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                labels.append({
                    'style_name': row['STYLE_NAME'],
                    'vpm': row['VPM'],
                    'color': row['COLOR'],
                    'size': row['SIZE']
                })
        
        print(f"✅ {len(labels)} etiquetas carregadas do CSV")
        return labels
        
    except Exception as e:
        print(f"❌ Erro ao carregar CSV: {e}")
        return []

def generate_zebra_designer_format(barcode, po_number, sequence, target_length=24):
    """Gera dados RFID no formato ZebraDesigner (Barcode + PO + Sequencial + Zeros)"""
    # Garantir que barcode tenha 12 caracteres
    barcode_formatted = str(barcode or '000000000000')[:12].zfill(12)
    
    # PO sem letras (apenas números)
    po_formatted = ''.join(filter(str.isdigit, str(po_number or '0000')))
    
    # Sequencial
    seq_formatted = str(sequence or 1)
    
    # Montar dados base
    base_data = f"{barcode_formatted}{po_formatted}{seq_formatted}"
    
    # Completar com zeros até atingir o tamanho desejado
    rfid_data = base_data.ljust(target_length, '0')
    
    print(f"📡 Python CSV RFID ZebraDesigner Format:")
    print(f"   Barcode: {barcode_formatted} (12 chars)")
    print(f"   PO: {po_formatted}")
    print(f"   Sequencial: {seq_formatted}")
    print(f"   Final: {rfid_data} ({len(rfid_data)} chars)")
    
    return rfid_data

def generate_zpl_for_label(label_data, rfid_data=None, sequence=1):
    """Gera ZPL para uma etiqueta específica usando o formato fornecido com RFID hexadecimal"""
    
    # Dados da etiqueta
    style_name = label_data['style_name']
    vpm = label_data['vpm']
    color = label_data['color']
    size = label_data['size']
    
    print(f"📋 Python CSV: Gerando etiqueta para {style_name}")
    
    # Extrair PO do VPM (formato: L458-JASM-11.0-SILV-1885)
    vpm_parts = vpm.split('-')
    po_number = vpm_parts[0].replace('L', '') if vpm_parts else '0000'
    
    # Gerar código de barras
    barcode = vpm.replace('-', '')[:12]
    
    # Gerar dados RFID no formato ZebraDesigner (se não fornecido dados customizados)
    if rfid_data:
        # Se dados customizados foram fornecidos, usar como está
        rfid_content = str(rfid_data)
    else:
        # Gerar no formato ZebraDesigner: Barcode + PO + Sequencial + Zeros
        rfid_content = generate_zebra_designer_format(barcode, po_number, sequence, 24)
    
    print(f"📡 Python CSV: Dados RFID finais: {rfid_content}")
    
    # Validar dados RFID (enviar como string direta, igual ZebraDesigner)
    validate_rfid_data(rfid_content)
    
    print(f"📡 Python CSV: RFID string direta (formato ZebraDesigner): {rfid_content}")
    
    # ZPL base fornecido pelo usuário
    zpl = f"""CT~~CD,~CC^~CT~
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
^FH\\^FD>;{vpm}>64^FS
^RFW,H,1,2,1^FD3000^FS
^RFW,H,2,12,1^FD{rfid_content}^FS
^FO50,50^A0N,30,30^FD{style_name}^FS
^FO50,90^A0N,25,25^FD{color}^FS
^FO50,130^A0N,25,25^FDSize: {size}^FS
^FO50,170^A0N,20,20^FDVPM: {vpm}^FS
^PQ1,0,1,Y
^XZ"""
    
    return zpl

def print_label(zpl_data, label_info):
    """Imprime uma etiqueta usando o ZPL fornecido"""
    print(f"🖨️ Imprimindo etiqueta: {label_info['style_name']}")
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as temp_file:
        temp_file.write(zpl_data)
        temp_file_path = temp_file.name
    
    try:
        printer_name = "ZDesigner ZD621R-203dpi ZPL"
        
        result = subprocess.run(
            ['copy', temp_file_path, printer_name],
            capture_output=True,
            text=True,
            shell=True
        )
        
        if result.returncode == 0:
            print(f"✅ Etiqueta '{label_info['style_name']}' enviada!")
            return True
        else:
            print(f"❌ Erro ao imprimir '{label_info['style_name']}': {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ Erro: {e}")
        return False
    finally:
        if os.path.exists(temp_file_path):
            os.unlink(temp_file_path)

def print_all_labels():
    """Imprime todas as etiquetas do CSV"""
    print("=== Processamento de Etiquetas CSV ===\n")
    
    # Carregar dados
    labels = load_csv_data()
    
    if not labels:
        print("❌ Nenhuma etiqueta encontrada no CSV")
        return
    
    print(f"\n📋 Etiquetas encontradas ({len(labels)}):")
    for i, label in enumerate(labels, 1):
        print(f"  {i}. {label['style_name']} - {label['color']} - Size {label['size']}")
    
    print(f"\n🖨️ Iniciando impressão de {len(labels)} etiquetas...")
    
    success_count = 0
    for i, label in enumerate(labels, 1):
        print(f"\n--- Etiqueta {i}/{len(labels)} ---")
        
        # Gerar ZPL para esta etiqueta
        zpl = generate_zpl_for_label(label)
        
        # Imprimir etiqueta
        if print_label(zpl, label):
            success_count += 1
        
        # Aguardar entre impressões
        time.sleep(2)
    
    print(f"\n✅ Processamento concluído!")
    print(f"📊 Etiquetas impressas: {success_count}/{len(labels)}")

def print_single_label(label_index):
    """Imprime uma etiqueta específica por índice"""
    print(f"=== Impressão de Etiqueta Específica ===\n")
    
    # Carregar dados
    labels = load_csv_data()
    
    if not labels:
        print("❌ Nenhuma etiqueta encontrada no CSV")
        return
    
    if label_index < 1 or label_index > len(labels):
        print(f"❌ Índice inválido. Use um número entre 1 e {len(labels)}")
        return
    
    # Selecionar etiqueta
    label = labels[label_index - 1]
    print(f"🖨️ Imprimindo etiqueta {label_index}: {label['style_name']}")
    
    # Gerar ZPL
    zpl = generate_zpl_for_label(label)
    
    # Imprimir
    if print_label(zpl, label):
        print(f"✅ Etiqueta '{label['style_name']}' impressa com sucesso!")
    else:
        print(f"❌ Falha ao imprimir etiqueta '{label['style_name']}'")

def list_labels():
    """Lista todas as etiquetas disponíveis"""
    print("=== Lista de Etiquetas Disponíveis ===\n")
    
    # Carregar dados
    labels = load_csv_data()
    
    if not labels:
        print("❌ Nenhuma etiqueta encontrada no CSV")
        return
    
    print(f"📋 Total de etiquetas: {len(labels)}\n")
    
    for i, label in enumerate(labels, 1):
        print(f"{i:2d}. {label['style_name']}")
        print(f"    VPM: {label['vpm']}")
        print(f"    Cor: {label['color']}")
        print(f"    Tamanho: {label['size']}")
        print()

def main():
    """Função principal"""
    import sys
    
    if len(sys.argv) < 2:
        print("📖 Uso do Processador de Etiquetas CSV:")
        print("  python process_csv_labels.py list                    - Lista todas as etiquetas")
        print("  python process_csv_labels.py print-all               - Imprime todas as etiquetas")
        print("  python process_csv_labels.py print <número>          - Imprime etiqueta específica")
        print()
        print("Exemplos:")
        print("  python process_csv_labels.py list")
        print("  python process_csv_labels.py print-all")
        print("  python process_csv_labels.py print 1")
        return
    
    command = sys.argv[1]
    
    if command == "list":
        list_labels()
    elif command == "print-all":
        print_all_labels()
    elif command == "print":
        if len(sys.argv) < 3:
            print("❌ Especifique o número da etiqueta")
            print("Exemplo: python process_csv_labels.py print 1")
            return
        
        try:
            label_index = int(sys.argv[2])
            print_single_label(label_index)
        except ValueError:
            print("❌ Número da etiqueta deve ser um número inteiro")
    else:
        print(f"❌ Comando desconhecido: {command}")

if __name__ == "__main__":
    main()
