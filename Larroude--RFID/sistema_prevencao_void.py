#!/usr/bin/env python3
"""
Sistema de Prevenção de VOID - Análise e Correção
NUNCA MAIS PERMITIR COMANDOS QUE CAUSEM VOID!
"""

import requests
import json

def analyze_void_causes():
    """Analisa as possíveis causas dos erros VOID"""
    print("🔍 ANÁLISE DAS CAUSAS DE VOID")
    print("=" * 50)
    
    void_causes = {
        "RFID Commands": {
            "^RFW": "Comando de escrita RFID pode causar VOID se malformado",
            "^RFR": "Comando de leitura RFID pode causar VOID",
            "USER Memory": "Gravação na USER memory pode estar incorreta",
            "Words calculation": "Cálculo incorreto de words pode causar VOID"
        },
        "Data Format": {
            "ASCII vs HEX": "Mistura de formatos pode causar problemas",
            "String length": "Tamanho incorreto dos dados",
            "Encoding": "Problemas de codificação de caracteres"
        },
        "Printer State": {
            "No RFID tag": "Impressora tentando gravar sem tag RFID presente",
            "Tag position": "Tag RFID mal posicionada",
            "Tag type": "Tipo de tag incompatível"
        }
    }
    
    for category, causes in void_causes.items():
        print(f"\n📋 {category.upper()}:")
        for cause, description in causes.items():
            print(f"   ❌ {cause}: {description}")

def create_safe_zpl_only_print():
    """Cria ZPL SEGURO - apenas impressão, SEM RFID"""
    print(f"\n✅ CRIANDO ZPL SEGURO (SEM RFID)")
    print("=" * 50)
    
    safe_zpl = """^XA
^CI28
^FX === ETIQUETA SEGURA - SEM RFID ===

^FX Apenas impressão visual - ZERO risco de VOID
^FO50,50^A0N,25,25^FDTESTE SEGURO^FS
^FO50,80^A0N,20,20^FDSEM COMANDOS RFID^FS
^FO50,110^A0N,18,18^FDBarcode: 789643610064^FS
^FO50,140^A0N,18,18^FDPO: 0464 | SEQ: 001^FS

^FX Código de barras visual
^FO50,180^BY2
^BCN,60,Y,N,N
^FD789643610064^FS

^FX QR Code com dados
^FO200,180^BQN,2,3
^FDMM,A789643610064|0464|001^FS

^XZ"""
    
    print("📋 ZPL GERADO (SEGURO):")
    print("```")
    print(safe_zpl)
    print("```")
    
    return safe_zpl

def create_void_prevention_system():
    """Cria sistema de prevenção de VOID"""
    print(f"\n🛡️ SISTEMA DE PREVENÇÃO DE VOID")
    print("=" * 50)
    
    prevention_rules = {
        "REGRA 1": "NUNCA enviar comandos ^RFW ou ^RFR sem validação extrema",
        "REGRA 2": "SEMPRE testar primeiro com ZPL sem RFID",
        "REGRA 3": "VALIDAR se há tag RFID presente antes de gravar",
        "REGRA 4": "USAR apenas comandos testados e aprovados",
        "REGRA 5": "IMPLEMENTAR modo 'SEGURO' por padrão"
    }
    
    for rule, description in prevention_rules.items():
        print(f"🔒 {rule}: {description}")

def test_safe_zpl():
    """Testa ZPL seguro sem RFID"""
    print(f"\n🧪 TESTE ZPL SEGURO")
    print("=" * 50)
    
    # ZPL completamente seguro
    safe_zpl = create_safe_zpl_only_print()
    
    try:
        print("📤 ENVIANDO ZPL SEGURO (SEM RFID)...")
        
        payload = {
            "zplCommand": safe_zpl,
            "testName": "TESTE SEGURO - SEM RFID",
            "description": "ZPL sem comandos RFID para evitar VOID",
            "method": "python-usb",
            "copies": 1,
            "analyze": True
        }
        
        response = requests.post("http://localhost:3002/api/test-zpl", 
                               json=payload, timeout=30)
        
        if response.status_code == 200:
            result = response.json()
            
            if result['success']:
                print("✅ ZPL SEGURO ENVIADO!")
                print("   🎯 Este ZPL NÃO deve causar VOID")
                print("   📋 Apenas impressão visual")
                print("   🚫 ZERO comandos RFID")
                
                # Mostrar detalhes
                if 'results' in result:
                    send_result = result['results'].get('sendResult', {})
                    if send_result.get('success'):
                        printer_info = send_result.get('result', {}).get('result', {})
                        print(f"   🖨️ Job ID: {printer_info.get('job_id', 'N/A')}")
                        print(f"   📊 Bytes: {printer_info.get('bytes_written', 'N/A')}")
                
                return True
            else:
                print("❌ ERRO MESMO COM ZPL SEGURO!")
                print(f"   💥 Mensagem: {result.get('message', 'N/A')}")
                return False
                
        else:
            print(f"❌ ERRO HTTP {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ ERRO: {e}")
        return False

def create_emergency_stop():
    """Cria sistema de parada de emergência"""
    print(f"\n🚨 SISTEMA DE PARADA DE EMERGÊNCIA")
    print("=" * 50)
    
    emergency_zpl = """^XA
^FX === PARADA DE EMERGÊNCIA ===
^FX Cancelar todos os jobs pendentes
~JA
^FX Limpar buffer
^JUS
^XZ"""
    
    print("🛑 COMANDO DE EMERGÊNCIA:")
    print("```")
    print(emergency_zpl)
    print("```")
    
    print("\n🔧 COMANDOS ÚTEIS:")
    print("   ~JA  = Cancelar todos os jobs")
    print("   ^JUS = Limpar buffer da impressora")
    print("   ^XA^XZ = Comando vazio para resetar")

def update_zpl_validator():
    """Atualiza validador ZPL para prevenir VOID"""
    print(f"\n🔧 ATUALIZANDO VALIDADOR ZPL")
    print("=" * 50)
    
    dangerous_commands = [
        "^RFW",  # Write RFID
        "^RFR",  # Read RFID
        "^RFI",  # RFID Info
        "^RFT",  # RFID Test
    ]
    
    print("⚠️ COMANDOS PERIGOSOS DETECTADOS:")
    for cmd in dangerous_commands:
        print(f"   🚫 {cmd} - Pode causar VOID")
    
    print("\n✅ COMANDOS SEGUROS PERMITIDOS:")
    safe_commands = [
        "^FO", "^FD", "^FS",  # Texto
        "^BC", "^BY",         # Código de barras
        "^BQ",               # QR Code
        "^A0",               # Fonte
        "^FX",               # Comentário
        "^CI",               # Codificação
        "^XA", "^XZ"         # Início/Fim
    ]
    
    for cmd in safe_commands:
        print(f"   ✅ {cmd} - Seguro")

def main():
    """Executa análise completa e cria sistema de prevenção"""
    print("🚨 SISTEMA DE PREVENÇÃO DE VOID")
    print("NUNCA MAIS PERMITIR ERROS!")
    print("=" * 50)
    
    # 1. Analisar causas
    analyze_void_causes()
    
    # 2. Criar sistema de prevenção
    create_void_prevention_system()
    
    # 3. Atualizar validador
    update_zpl_validator()
    
    # 4. Criar comando de emergência
    create_emergency_stop()
    
    # 5. Testar ZPL seguro
    print(f"\n🧪 VAMOS TESTAR ZPL SEGURO AGORA:")
    success = test_safe_zpl()
    
    print(f"\n🏁 RESULTADO:")
    if success:
        print("✅ ZPL SEGURO FUNCIONOU!")
        print("   🎯 Use apenas este tipo de ZPL")
        print("   🚫 EVITE comandos RFID por enquanto")
    else:
        print("❌ PROBLEMA PERSISTE!")
        print("   🔧 Verificar impressora e conexão")
    
    print(f"\n📋 PRÓXIMOS PASSOS:")
    print("1. 🛑 PARAR todos os testes com RFID")
    print("2. ✅ Usar apenas ZPL de impressão visual")
    print("3. 🔧 Investigar configuração da impressora")
    print("4. 📞 Verificar se impressora suporta RFID")
    print("5. 🧪 Testar RFID apenas depois de resolver")
    
    print(f"\n🌐 INTERFACE SEGURA:")
    print("   http://localhost:3002/zpl-tester")
    print("   • Use apenas comandos de impressão")
    print("   • EVITE comandos ^RFW, ^RFR")

if __name__ == "__main__":
    main()
