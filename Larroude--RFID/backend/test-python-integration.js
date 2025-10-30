#!/usr/bin/env node

const PythonZebraIntegration = require('./python-zebra-integration');

async function main() {
    console.log('=== Teste de Integração Python com Node.js ===\n');
    
    const pythonIntegration = new PythonZebraIntegration();
    
    // Opções de teste
    const args = process.argv.slice(2);
    const command = args[0];
    
    switch (command) {
        case 'detect':
            console.log('🔍 Testando detecção via Python...\n');
            try {
                const result = await pythonIntegration.detectPrinters();
                console.log('📊 Resultado da Detecção:');
                console.log(JSON.stringify(result, null, 2));
            } catch (error) {
                console.error('❌ Erro na detecção:', error.message);
            }
            break;
            
        case 'test':
            console.log('🧪 Testando conectividade via Python...\n');
            try {
                const result = await pythonIntegration.testConnection();
                console.log('📊 Resultado do Teste:');
                console.log(JSON.stringify(result, null, 2));
            } catch (error) {
                console.error('❌ Erro no teste:', error.message);
            }
            break;
            
        case 'full':
            console.log('🚀 Teste completo via Python...\n');
            try {
                const result = await pythonIntegration.fullTest();
                console.log('📊 Resultado do Teste Completo:');
                console.log(JSON.stringify(result, null, 2));
            } catch (error) {
                console.error('❌ Erro no teste completo:', error.message);
            }
            break;
            
        case 'send':
            const zplCommand = args[1];
            if (!zplCommand) {
                console.error('❌ Erro: Comando ZPL é obrigatório');
                console.log('Uso: node test-python-integration.js send <comando_zpl>');
                console.log('Exemplo: node test-python-integration.js send "^XA^FO50,50^A0N,30,30^FDTeste^FS^XZ"');
                process.exit(1);
            }
            
            console.log('📤 Enviando ZPL via Python...\n');
            try {
                const result = await pythonIntegration.sendZPL(zplCommand);
                console.log('📊 Resultado do Envio:');
                console.log(JSON.stringify(result, null, 2));
            } catch (error) {
                console.error('❌ Erro no envio:', error.message);
            }
            break;
            
        case 'status':
            console.log('📊 Status da Conexão Python:\n');
            try {
                const status = pythonIntegration.getStatus();
                console.log(JSON.stringify(status, null, 2));
            } catch (error) {
                console.error('❌ Erro ao obter status:', error.message);
            }
            break;
            
        case 'help':
        default:
            console.log('📖 Uso do Teste de Integração Python:');
            console.log('='.repeat(50));
            console.log('\nComandos disponíveis:');
            console.log('\n  detect                      - Detecta impressoras via Python');
            console.log('  test                        - Testa conectividade via Python');
            console.log('  full                        - Teste completo via Python');
            console.log('  send <zpl>                  - Envia ZPL via Python');
            console.log('  status                      - Mostra status da conexão');
            console.log('  help                        - Mostra esta ajuda');
            
            console.log('\nExemplos:');
            console.log('  node test-python-integration.js detect');
            console.log('  node test-python-integration.js test');
            console.log('  node test-python-integration.js full');
            console.log('  node test-python-integration.js send "^XA^FO50,50^A0N,30,30^FDTeste^FS^XZ"');
            console.log('  node test-python-integration.js status');
            
            console.log('\n📋 Informações:');
            console.log('  - Integração Node.js + Python');
            console.log('  - Comunicação via subprocesso');
            console.log('  - API JSON para troca de dados');
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
