#!/usr/bin/env node

const ZebraUSBConnection = require('./zebra-usb-connection');

async function main() {
    console.log('=== Teste de Conexão USB Zebra ZD621R ===\n');
    
    const zebraConnection = new ZebraUSBConnection();
    
    // Opções de teste
    const args = process.argv.slice(2);
    const command = args[0];
    
    switch (command) {
        case 'detect':
            console.log('🔍 Detectando impressoras Zebra...\n');
            try {
                const detection = await zebraConnection.detectPrinters();
                
                console.log('📊 Resultados da Detecção:');
                console.log('='.repeat(50));
                
                console.log(`\n📡 Portas Seriais: ${detection.serial.length}`);
                detection.serial.forEach((port, index) => {
                    console.log(`   ${index + 1}. ${port.path} - ${port.manufacturer || 'Desconhecido'}`);
                });
                
                console.log(`\n🖥️ Dispositivos Windows: ${detection.windows.length}`);
                detection.windows.forEach((device, index) => {
                    console.log(`   ${index + 1}. ${device}`);
                });
                
                console.log(`\n🔌 Dispositivos USB: ${detection.usb.length}`);
                detection.usb.forEach((device, index) => {
                    console.log(`   ${index + 1}. ${device}`);
                });
                
                const total = detection.serial.length + detection.windows.length + detection.usb.length;
                console.log(`\n📈 Total de dispositivos encontrados: ${total}`);
                
            } catch (error) {
                console.error('❌ Erro na detecção:', error.message);
            }
            break;
            
        case 'connect':
            const portPath = args[1];
            try {
                console.log('🔌 Tentando conectar à impressora...');
                await zebraConnection.connect(portPath);
                
                console.log('\n🧪 Testando conectividade...');
                const testResult = await zebraConnection.testConnection();
                
                if (testResult.success) {
                    console.log('✅ Teste de conectividade: OK');
                    console.log(`   Tipo de conexão: ${testResult.connectionType}`);
                    console.log('✅ Comando de teste enviado com sucesso');
                } else {
                    console.log('❌ Teste de conectividade: FALHOU');
                    console.log(`   Erro: ${testResult.error}`);
                }
                
                // Desconectar
                await zebraConnection.disconnect();
                
            } catch (error) {
                console.error('❌ Erro na conexão:', error.message);
            }
            break;
            
        case 'auto':
            try {
                console.log('🔍 Auto-detectando e conectando à impressora...\n');
                await zebraConnection.connect();
                
                console.log('\n🧪 Testando conectividade...');
                const testResult = await zebraConnection.testConnection();
                
                if (testResult.success) {
                    console.log('✅ Auto-conexão bem-sucedida!');
                    console.log(`   Tipo de conexão: ${testResult.connectionType}`);
                    console.log('✅ Comando de teste enviado com sucesso');
                } else {
                    console.log('❌ Auto-conexão falhou');
                    console.log(`   Erro: ${testResult.error}`);
                }
                
                // Desconectar
                await zebraConnection.disconnect();
                
            } catch (error) {
                console.error('❌ Erro na auto-conexão:', error.message);
            }
            break;
            
        case 'test':
            try {
                console.log('🧪 Executando teste completo...\n');
                
                // 1. Detectar impressoras
                console.log('1️⃣ Detectando impressoras...');
                const detection = await zebraConnection.detectPrinters();
                const totalDevices = detection.serial.length + detection.windows.length + detection.usb.length;
                
                if (totalDevices === 0) {
                    console.log('❌ Nenhuma impressora Zebra detectada');
                    return;
                }
                
                console.log(`✅ ${totalDevices} dispositivo(s) encontrado(s)`);
                
                // 2. Tentar conectar
                console.log('\n2️⃣ Tentando conectar...');
                await zebraConnection.connect();
                
                // 3. Testar conectividade
                console.log('\n3️⃣ Testando conectividade...');
                const testResult = await zebraConnection.testConnection();
                
                console.log('\n📊 Resultados do Teste:');
                console.log('='.repeat(50));
                
                if (testResult.success) {
                    console.log('✅ Status da Conexão: OK');
                    console.log(`   Tipo: ${testResult.connectionType}`);
                    console.log('✅ Comando de Teste: OK');
                    console.log('✅ Impressora Zebra: FUNCIONANDO');
                } else {
                    console.log('❌ Status da Conexão: FALHOU');
                    console.log(`   Erro: ${testResult.error}`);
                }
                
                // Desconectar
                await zebraConnection.disconnect();
                
            } catch (error) {
                console.error('❌ Erro no teste:', error.message);
            }
            break;
            
        case 'send':
            const zplCommand = args[1];
            
            if (!zplCommand) {
                console.error('❌ Erro: Comando ZPL é obrigatório');
                console.log('Uso: node test-zebra-usb.js send <comando_zpl>');
                console.log('Exemplo: node test-zebra-usb.js send "^XA^FO50,50^A0N,50,50^FDTeste^FS^XZ"');
                process.exit(1);
            }
            
            try {
                console.log('🔌 Conectando à impressora...');
                await zebraConnection.connect();
                
                console.log('\n📤 Enviando comando ZPL...');
                await zebraConnection.sendZPL(zplCommand);
                console.log('✅ Comando ZPL enviado com sucesso!');
                
                // Desconectar
                await zebraConnection.disconnect();
                
            } catch (error) {
                console.error('❌ Erro ao enviar ZPL:', error.message);
            }
            break;
            
        case 'help':
        default:
            console.log('📖 Uso do Testador de Impressora Zebra USB:');
            console.log('='.repeat(50));
            console.log('\nComandos disponíveis:');
            console.log('\n  detect                      - Detecta impressoras Zebra');
            console.log('  connect [porta]             - Conecta à porta específica');
            console.log('  auto                        - Auto-detecta e conecta');
            console.log('  test                        - Teste completo');
            console.log('  send <zpl>                  - Envia comando ZPL');
            console.log('  help                        - Mostra esta ajuda');
            
            console.log('\nExemplos:');
            console.log('  node test-zebra-usb.js detect');
            console.log('  node test-zebra-usb.js connect COM3');
            console.log('  node test-zebra-usb.js auto');
            console.log('  node test-zebra-usb.js test');
            console.log('  node test-zebra-usb.js send "^XA^FO50,50^A0N,50,50^FDTeste^FS^XZ"');
            
            console.log('\n📋 Informações:');
            console.log('  - Suporta conexão serial e Windows');
            console.log('  - Auto-detecção de dispositivos');
            console.log('  - Múltiplas tentativas de conexão');
            console.log('  - Compatível com Zebra ZD621R');
            break;
    }
}

// Tratamento de erros
process.on('unhandledRejection', (reason, promise) => {
    console.error('❌ Erro não tratado:', reason);
    process.exit(1);
});

process.on('uncaughtException', (error) => {
    console.error('❌ Exceção não capturada:', error);
    process.exit(1);
});

// Executar se chamado diretamente
if (require.main === module) {
    main().catch(error => {
        console.error('❌ Erro durante execução:', error);
        process.exit(1);
    });
}

module.exports = main;
