#!/usr/bin/env node

const { SerialPort } = require('serialport');

async function diagnosePrinter() {
    console.log('=== Diagnóstico de Impressora USB ===\n');
    
    try {
        // Listar todas as portas
        console.log('🔍 Listando todas as portas seriais...');
        const ports = await SerialPort.list();
        
        console.log(`\n📋 Total de portas encontradas: ${ports.length}`);
        
        for (const port of ports) {
            console.log(`\n📡 Porta: ${port.path}`);
            console.log(`   Fabricante: ${port.manufacturer || 'Desconhecido'}`);
            console.log(`   Produto: ${port.productId || 'Desconhecido'}`);
            console.log(`   Vendor ID: ${port.vendorId || 'Desconhecido'}`);
            console.log(`   Serial Number: ${port.serialNumber || 'N/A'}`);
            console.log(`   PNP ID: ${port.pnpId || 'N/A'}`);
            console.log(`   Local Port: ${port.localName || 'N/A'}`);
            
            // Tentar abrir a porta para verificar se está disponível
            try {
                const testPort = new SerialPort({
                    path: port.path,
                    baudRate: 9600,
                    autoOpen: false
                });
                
                await new Promise((resolve, reject) => {
                    testPort.open((err) => {
                        if (err) {
                            console.log(`   ❌ Status: Não disponível (${err.message})`);
                            reject(err);
                        } else {
                            console.log(`   ✅ Status: Disponível`);
                            testPort.close();
                            resolve();
                        }
                    });
                });
                
            } catch (error) {
                // Erro já foi tratado acima
            }
        }
        
        // Testar comunicação básica na primeira porta disponível
        const availablePorts = ports.filter(port => {
            // Filtrar portas que parecem ser impressoras
            const manufacturer = port.manufacturer?.toLowerCase() || '';
            const productId = port.productId?.toLowerCase() || '';
            return manufacturer.includes('zebra') || 
                   manufacturer.includes('printer') ||
                   productId.includes('zebra') ||
                   port.path.includes('COM');
        });
        
        if (availablePorts.length > 0) {
            console.log(`\n🖨️ Testando comunicação na primeira porta disponível: ${availablePorts[0].path}`);
            
            const testPort = new SerialPort({
                path: availablePorts[0].path,
                baudRate: 9600,
                autoOpen: false
            });
            
            await new Promise((resolve, reject) => {
                testPort.open((err) => {
                    if (err) {
                        console.log(`❌ Não foi possível abrir a porta: ${err.message}`);
                        reject(err);
                        return;
                    }
                    
                    console.log('✅ Porta aberta com sucesso');
                    
                    // Enviar comando de status simples
                    const statusCommand = '~HS\r\n';
                    console.log(`📤 Enviando comando de status: ${statusCommand.trim()}`);
                    
                    testPort.write(statusCommand, (writeErr) => {
                        if (writeErr) {
                            console.log(`❌ Erro ao escrever: ${writeErr.message}`);
                            testPort.close();
                            reject(writeErr);
                            return;
                        }
                        
                        console.log('✅ Comando enviado, aguardando resposta...');
                        
                        // Configurar timeout para resposta
                        const timeout = setTimeout(() => {
                            console.log('⏰ Timeout - Nenhuma resposta recebida');
                            testPort.close();
                            resolve();
                        }, 3000);
                        
                        // Escutar por resposta
                        testPort.on('data', (data) => {
                            clearTimeout(timeout);
                            console.log(`📨 Resposta recebida: ${data.toString()}`);
                            testPort.close();
                            resolve();
                        });
                        
                        testPort.on('error', (error) => {
                            clearTimeout(timeout);
                            console.log(`❌ Erro na comunicação: ${error.message}`);
                            testPort.close();
                            reject(error);
                        });
                    });
                });
            });
            
        } else {
            console.log('\n❌ Nenhuma porta de impressora detectada');
        }
        
    } catch (error) {
        console.error('❌ Erro durante diagnóstico:', error);
    }
}

// Executar diagnóstico
diagnosePrinter()
    .then(() => {
        console.log('\n✅ Diagnóstico concluído');
        process.exit(0);
    })
    .catch(error => {
        console.error('❌ Erro no diagnóstico:', error);
        process.exit(1);
    });
