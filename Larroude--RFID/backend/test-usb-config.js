#!/usr/bin/env node

const USBPrinterConnection = require('./usb-printer-connection');

async function testDifferentConfigs() {
    console.log('=== Teste de Configurações USB - Impressora RFID ===\n');
    
    const usbConnection = new USBPrinterConnection();
    
    // Listar portas disponíveis
    console.log('🔍 Portas disponíveis:');
    const { printerPorts } = await usbConnection.listPorts();
    
    if (printerPorts.length === 0) {
        console.log('❌ Nenhuma porta detectada');
        return;
    }
    
    // Configurações para testar
    const configs = [
        { baudRate: 9600, dataBits: 8, stopBits: 1, parity: 'none' },
        { baudRate: 19200, dataBits: 8, stopBits: 1, parity: 'none' },
        { baudRate: 38400, dataBits: 8, stopBits: 1, parity: 'none' },
        { baudRate: 57600, dataBits: 8, stopBits: 1, parity: 'none' },
        { baudRate: 115200, dataBits: 8, stopBits: 1, parity: 'none' },
        { baudRate: 9600, dataBits: 7, stopBits: 1, parity: 'even' },
        { baudRate: 9600, dataBits: 7, stopBits: 1, parity: 'odd' },
        { baudRate: 9600, dataBits: 8, stopBits: 2, parity: 'none' }
    ];
    
    for (const port of printerPorts) {
        console.log(`\n🖨️ Testando porta: ${port.path}`);
        console.log('='.repeat(50));
        
        for (const config of configs) {
            try {
                console.log(`\n📡 Testando configuração: ${config.baudRate} baud, ${config.dataBits} bits, ${config.parity} parity, ${config.stopBits} stop bits`);
                
                // Tentar conectar
                await usbConnection.connect(port.path, config);
                console.log('✅ Conexão estabelecida');
                
                // Testar envio de comando simples
                const testZPL = '^XA^FO50,50^A0N,30,30^FDTeste^FS^XZ';
                await usbConnection.sendZPL(testZPL);
                console.log('✅ Comando ZPL enviado com sucesso');
                
                // Desconectar
                await usbConnection.disconnect();
                console.log('✅ Configuração FUNCIONOU!');
                
                // Se chegou até aqui, esta configuração funciona
                console.log(`\n🎉 CONFIGURAÇÃO IDEAL ENCONTRADA:`);
                console.log(`   Porta: ${port.path}`);
                console.log(`   Baud Rate: ${config.baudRate}`);
                console.log(`   Data Bits: ${config.dataBits}`);
                console.log(`   Parity: ${config.parity}`);
                console.log(`   Stop Bits: ${config.stopBits}`);
                
                return {
                    success: true,
                    port: port.path,
                    config: config
                };
                
            } catch (error) {
                console.log(`❌ Falhou: ${error.message}`);
                // Tentar desconectar se ainda estiver conectado
                try {
                    if (usbConnection.isConnected) {
                        await usbConnection.disconnect();
                    }
                } catch (disconnectError) {
                    // Ignorar erro de desconexão
                }
            }
        }
    }
    
    console.log('\n❌ Nenhuma configuração funcionou');
    return { success: false };
}

// Executar teste
testDifferentConfigs()
    .then(result => {
        if (result.success) {
            console.log('\n✅ Teste concluído com sucesso!');
            process.exit(0);
        } else {
            console.log('\n❌ Teste falhou');
            process.exit(1);
        }
    })
    .catch(error => {
        console.error('❌ Erro durante o teste:', error);
        process.exit(1);
    });
