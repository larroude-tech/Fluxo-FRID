#!/usr/bin/env node

const RFIDPrinterTest = require('./rfid-printer-test');

async function main() {
    console.log('=== Teste de Comunicação com Impressora RFID Zebra ZD621R ===\n');
    
    const tester = new RFIDPrinterTest();
    
    // Opções de teste
    const args = process.argv.slice(2);
    const command = args[0];
    
    switch (command) {
        case 'discover':
            console.log('🔍 Descobrindo impressoras na rede...');
            const printers = await tester.discoverPrinters(10000); // 10 segundos
            console.log(`\n📋 Impressoras descobertas: ${printers.length}`);
            printers.forEach((printer, index) => {
                console.log(`${index + 1}. IP: ${printer.ip}:${printer.port}`);
                console.log(`   Resposta: ${printer.response.substring(0, 100)}...`);
                console.log(`   Timestamp: ${printer.timestamp}\n`);
            });
            break;
            
        case 'test':
            const ip = args[1];
            const port = args[2] || 9100;
            
            if (!ip) {
                console.error('❌ Erro: IP da impressora é obrigatório');
                console.log('Uso: node test-rfid-printer.js test <IP> [porta]');
                process.exit(1);
            }
            
            console.log(`🧪 Testando impressora ${ip}:${port}...\n`);
            const result = await tester.testSpecificPrinter(ip, port);
            
            console.log('📊 Resultados do Teste:');
            console.log('='.repeat(50));
            
            // Teste TCP
            console.log('\n🔌 Teste de Conectividade TCP:');
            if (result.tests.tcp.tcpConnected) {
                console.log('✅ Conectividade TCP: OK');
                console.log(`   Tempo de resposta: ${result.tests.tcp.responseTime}ms`);
            } else {
                console.log('❌ Conectividade TCP: FALHOU');
                console.log(`   Erro: ${result.tests.tcp.error}`);
            }
            
            // Teste ZPL
            console.log('\n🖨️  Teste de Envio ZPL:');
            if (result.tests.zpl?.zplSent) {
                console.log('✅ Envio ZPL: OK');
            } else {
                console.log('❌ Envio ZPL: FALHOU');
                console.log(`   Erro: ${result.tests.zpl?.error || 'Não testado'}`);
            }
            
            // Teste HTTP
            console.log('\n🌐 Teste de Status HTTP:');
            if (result.tests.http.httpStatus) {
                console.log('✅ Status HTTP: OK');
                console.log(`   Título: ${result.tests.http.statusData.title}`);
            } else {
                console.log('❌ Status HTTP: FALHOU');
                console.log(`   Erro: ${result.tests.http.error}`);
            }
            
            // Informações da impressora
            console.log('\n📋 Informações da Impressora:');
            console.log(`   Modelo: ${result.tests.info.model}`);
            console.log(`   Capacidades: ${result.tests.info.capabilities.join(', ')}`);
            console.log(`   Formatos suportados: ${result.tests.info.supportedFormats.join(', ')}`);
            console.log(`   Largura máxima: ${result.tests.info.maxPrintWidth}`);
            console.log(`   Resolução: ${result.tests.info.dpi}`);
            
            break;
            
        case 'full':
            console.log('🔍 Descobrindo impressoras...');
            const discovered = await tester.discoverPrinters(10000);
            
            if (discovered.length === 0) {
                console.log('❌ Nenhuma impressora descoberta automaticamente');
                console.log('💡 Use o comando "test" com um IP específico');
                break;
            }
            
            console.log(`\n🧪 Testando ${discovered.length} impressora(s) descoberta(s)...\n`);
            
            for (const printer of discovered) {
                console.log(`\n--- Testando ${printer.ip}:${printer.port} ---`);
                await tester.testSpecificPrinter(printer.ip, printer.port);
            }
            
            // Gerar relatório
            const reportPath = await tester.saveTestReport();
            console.log(`\n📄 Relatório salvo em: ${reportPath}`);
            
            // Mostrar resumo
            const report = tester.generateTestReport();
            console.log('\n📊 Resumo dos Testes:');
            console.log('='.repeat(30));
            console.log(`Total de impressoras: ${report.summary.totalPrinters}`);
            console.log(`Testadas: ${report.summary.testedPrinters}`);
            console.log(`Conexões TCP bem-sucedidas: ${report.summary.successfulConnections}`);
            console.log(`Envios ZPL bem-sucedidos: ${report.summary.successfulZPL}`);
            
            break;
            
        case 'help':
        default:
            console.log('📖 Uso do Testador de Impressoras RFID:');
            console.log('='.repeat(50));
            console.log('\nComandos disponíveis:');
            console.log('\n  discover                    - Descobre impressoras na rede');
            console.log('  test <IP> [porta]          - Testa impressora específica');
            console.log('  full                       - Descobre e testa todas as impressoras');
            console.log('  help                       - Mostra esta ajuda');
            
            console.log('\nExemplos:');
            console.log('  node test-rfid-printer.js discover');
            console.log('  node test-rfid-printer.js test 192.168.1.100');
            console.log('  node test-rfid-printer.js test 192.168.1.100 9100');
            console.log('  node test-rfid-printer.js full');
            
            console.log('\n📋 Informações:');
            console.log('  - Porta padrão: 9100');
            console.log('  - Timeout de descoberta: 10 segundos');
            console.log('  - Timeout de conexão: 5 segundos');
            console.log('  - Relatórios salvos em: backend/test-reports/');
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
