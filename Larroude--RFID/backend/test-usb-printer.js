#!/usr/bin/env node

const USBPrinterConnection = require('./usb-printer-connection');

async function main() {
    console.log('=== Teste de Conexão USB com Impressora RFID Zebra ZD621R ===\n');
    
    const usbConnection = new USBPrinterConnection();
    
    // Opções de teste
    const args = process.argv.slice(2);
    const command = args[0];
    
    switch (command) {
        case 'list':
            console.log('🔍 Listando portas seriais disponíveis...\n');
            try {
                const { allPorts, printerPorts } = await usbConnection.listPorts();
                console.log(`\n📊 Resumo:`);
                console.log(`   Total de portas: ${allPorts.length}`);
                console.log(`   Possíveis impressoras: ${printerPorts.length}`);
                
                if (printerPorts.length > 0) {
                    console.log('\n🖨️ Impressoras detectadas:');
                    printerPorts.forEach((printer, index) => {
                        console.log(`   ${index + 1}. ${printer.path} - ${printer.manufacturer || 'Desconhecido'}`);
                    });
                }
            } catch (error) {
                console.error('❌ Erro ao listar portas:', error.message);
            }
            break;
            
        case 'connect':
            const portPath = args[1];
            if (!portPath) {
                console.error('❌ Erro: Caminho da porta é obrigatório');
                console.log('Uso: node test-usb-printer.js connect <porta>');
                console.log('Exemplo: node test-usb-printer.js connect COM3');
                process.exit(1);
            }
            
            try {
                console.log(`🔌 Conectando à porta ${portPath}...`);
                await usbConnection.connect(portPath);
                
                console.log('\n🧪 Testando conectividade...');
                const testResult = await usbConnection.testConnection();
                
                if (testResult.success) {
                    console.log('✅ Teste de conectividade: OK');
                    console.log('✅ Comando de teste enviado com sucesso');
                } else {
                    console.log('❌ Teste de conectividade: FALHOU');
                    console.log(`   Erro: ${testResult.error}`);
                }
                
                // Desconectar
                await usbConnection.disconnect();
                
            } catch (error) {
                console.error('❌ Erro na conexão:', error.message);
            }
            break;
            
        case 'auto':
            try {
                console.log('🔍 Auto-detectando e conectando à impressora...\n');
                const result = await usbConnection.autoConnect();
                
                console.log('✅ Auto-conexão bem-sucedida!');
                console.log(`   Porta: ${result.port.path}`);
                console.log(`   Fabricante: ${result.port.manufacturer || 'Desconhecido'}`);
                console.log(`   Mensagem: ${result.message}`);
                
                console.log('\n🧪 Testando conectividade...');
                const testResult = await usbConnection.testConnection();
                
                if (testResult.success) {
                    console.log('✅ Teste de conectividade: OK');
                    console.log('✅ Comando de teste enviado com sucesso');
                } else {
                    console.log('❌ Teste de conectividade: FALHOU');
                    console.log(`   Erro: ${testResult.error}`);
                }
                
                // Desconectar
                await usbConnection.disconnect();
                
            } catch (error) {
                console.error('❌ Erro na auto-conexão:', error.message);
            }
            break;
            
        case 'test':
            const testPort = args[1];
            if (!testPort) {
                console.error('❌ Erro: Caminho da porta é obrigatório');
                console.log('Uso: node test-usb-printer.js test <porta>');
                process.exit(1);
            }
            
            try {
                console.log(`🔌 Conectando à porta ${testPort}...`);
                await usbConnection.connect(testPort);
                
                console.log('\n🧪 Executando teste completo...');
                const testResult = await usbConnection.testConnection();
                
                console.log('\n📊 Resultados do Teste:');
                console.log('='.repeat(50));
                
                if (testResult.success) {
                    console.log('✅ Status da Conexão: OK');
                    console.log(`   Porta: ${testResult.connectionInfo.portPath}`);
                    console.log('✅ Comando de Teste: OK');
                    console.log('✅ Impressora USB: FUNCIONANDO');
                } else {
                    console.log('❌ Status da Conexão: FALHOU');
                    console.log(`   Erro: ${testResult.error}`);
                }
                
                // Desconectar
                await usbConnection.disconnect();
                
            } catch (error) {
                console.error('❌ Erro no teste:', error.message);
            }
            break;
            
        case 'send':
            const sendPort = args[1];
            const zplCommand = args[2];
            
            if (!sendPort || !zplCommand) {
                console.error('❌ Erro: Porta e comando ZPL são obrigatórios');
                console.log('Uso: node test-usb-printer.js send <porta> <comando_zpl>');
                console.log('Exemplo: node test-usb-printer.js send COM3 "^XA^FO50,50^A0N,50,50^FDTeste^FS^XZ"');
                process.exit(1);
            }
            
            try {
                console.log(`🔌 Conectando à porta ${sendPort}...`);
                await usbConnection.connect(sendPort);
                
                console.log('\n📤 Enviando comando ZPL...');
                await usbConnection.sendZPL(zplCommand);
                console.log('✅ Comando ZPL enviado com sucesso!');
                
                // Desconectar
                await usbConnection.disconnect();
                
            } catch (error) {
                console.error('❌ Erro ao enviar ZPL:', error.message);
            }
            break;
            
        case 'help':
        default:
            console.log('📖 Uso do Testador de Impressora USB:');
            console.log('='.repeat(50));
            console.log('\nComandos disponíveis:');
            console.log('\n  list                        - Lista todas as portas seriais');
            console.log('  connect <porta>             - Conecta à porta específica');
            console.log('  auto                        - Auto-detecta e conecta à impressora');
            console.log('  test <porta>                - Testa conectividade completa');
            console.log('  send <porta> <zpl>          - Envia comando ZPL específico');
            console.log('  help                        - Mostra esta ajuda');
            
            console.log('\nExemplos:');
            console.log('  node test-usb-printer.js list');
            console.log('  node test-usb-printer.js connect COM3');
            console.log('  node test-usb-printer.js auto');
            console.log('  node test-usb-printer.js test COM3');
            console.log('  node test-usb-printer.js send COM3 "^XA^FO50,50^A0N,50,50^FDTeste^FS^XZ"');
            
            console.log('\n📋 Informações:');
            console.log('  - Baud rate padrão: 9600');
            console.log('  - Data bits: 8');
            console.log('  - Stop bits: 1');
            console.log('  - Parity: none');
            console.log('  - Timeout de conexão: 5 segundos');
            console.log('  - Timeout de envio: 10 segundos');
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
