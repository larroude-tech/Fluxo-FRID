#!/usr/bin/env node

const MupaRFIDIntegration = require('./backend/mupa-rfid-integration');

async function testMupaIntegration() {
    console.log('=== Teste de Integração MUPA RFID ===\n');

    const mupaIntegration = new MupaRFIDIntegration();

    try {
        // Teste 1: Status
        console.log('🔍 Verificando status...');
        const status = mupaIntegration.getStatus();
        console.log('📊 Status:', status);

        // Teste 2: Impressão de etiqueta
        console.log('\n🧪 Testando impressão de etiqueta...');
        const labelResult = await mupaIntegration.printLabel('MUPA_TESTE_01', {
            subtitle: 'Teste de Integração',
            showDate: true
        });
        console.log('📊 Resultado da etiqueta:', labelResult);

        // Aguardar um pouco
        await new Promise(resolve => setTimeout(resolve, 2000));

        // Teste 3: Gravação RFID
        console.log('\n🧪 Testando gravação RFID...');
        const rfidResult = await mupaIntegration.writeRFID('MUPA_TESTE_01');
        console.log('📊 Resultado do RFID:', rfidResult);

        // Aguardar um pouco
        await new Promise(resolve => setTimeout(resolve, 2000));

        // Teste 4: Comando combinado
        console.log('\n🧪 Testando comando combinado...');
        const combinedResult = await mupaIntegration.printAndWriteRFID('MUPA_TESTE_01', {
            subtitle: 'Teste Combinado',
            showDate: true,
            showBarcode: true
        });
        console.log('📊 Resultado combinado:', combinedResult);

        // Aguardar um pouco
        await new Promise(resolve => setTimeout(resolve, 2000));

        // Teste 5: Leitura RFID
        console.log('\n🧪 Testando leitura RFID...');
        const readResult = await mupaIntegration.readRFID();
        console.log('📊 Resultado da leitura:', readResult);

        // Teste 6: Teste completo
        console.log('\n🧪 Executando teste completo...');
        const fullTestResult = await mupaIntegration.testMupa('MUPA_TESTE_01');
        console.log('📊 Resultado do teste completo:', fullTestResult);

        console.log('\n✅ Todos os testes concluídos com sucesso!');

    } catch (error) {
        console.error('❌ Erro durante os testes:', error);
    }
}

// Executar teste se chamado diretamente
if (require.main === module) {
    testMupaIntegration();
}

module.exports = testMupaIntegration;
