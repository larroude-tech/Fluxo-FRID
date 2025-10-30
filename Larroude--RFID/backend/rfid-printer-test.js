const net = require('net');
const dgram = require('dgram');
const axios = require('axios');
const fs = require('fs');
const path = require('path');

class RFIDPrinterTest {
    constructor() {
        this.discoveredPrinters = [];
        this.testResults = [];
    }

    /**
     * Descobre impressoras Zebra na rede usando broadcast UDP
     */
    async discoverPrinters(timeout = 5000) {
        return new Promise((resolve) => {
            const socket = dgram.createSocket('udp4');
            const printers = [];
            
            socket.on('message', (msg, rinfo) => {
                try {
                    const response = msg.toString();
                    if (response.includes('Zebra') || response.includes('ZD621R')) {
                        printers.push({
                            ip: rinfo.address,
                            port: rinfo.port,
                            response: response,
                            timestamp: new Date().toISOString()
                        });
                    }
                } catch (error) {
                    console.error('Erro ao processar resposta da impressora:', error);
                }
            });

            socket.on('error', (err) => {
                console.error('Erro no socket UDP:', err);
            });

            // Enviar broadcast para descobrir impressoras
            const discoveryMessage = Buffer.from('~HS\r\n'); // Comando de status Zebra
            
            socket.bind(() => {
                socket.setBroadcast(true);
                
                // Enviar para broadcast
                socket.send(discoveryMessage, 0, discoveryMessage.length, 9100, '255.255.255.255');
                
                // Enviar para subnets comuns
                const commonSubnets = [
                    '192.168.1.255',
                    '192.168.0.255',
                    '10.0.0.255',
                    '172.16.0.255'
                ];
                
                commonSubnets.forEach(subnet => {
                    socket.send(discoveryMessage, 0, discoveryMessage.length, 9100, subnet);
                });
            });

            // Timeout para parar a busca
            setTimeout(() => {
                socket.close();
                this.discoveredPrinters = printers;
                resolve(printers);
            }, timeout);
        });
    }

    /**
     * Testa conectividade TCP com uma impressora específica
     */
    async testTCPConnection(ip, port = 9100, timeout = 5000) {
        return new Promise((resolve) => {
            const socket = new net.Socket();
            let connected = false;
            let testResult = {
                ip: ip,
                port: port,
                tcpConnected: false,
                responseTime: null,
                error: null,
                timestamp: new Date().toISOString()
            };

            const timer = setTimeout(() => {
                if (!connected) {
                    testResult.error = 'Timeout de conexão';
                    socket.destroy();
                    resolve(testResult);
                }
            }, timeout);

            socket.on('connect', () => {
                connected = true;
                testResult.tcpConnected = true;
                testResult.responseTime = Date.now();
                
                // Enviar comando de teste
                const testCommand = '~HS\r\n';
                socket.write(testCommand);
            });

            socket.on('data', (data) => {
                testResult.response = data.toString();
                socket.destroy();
            });

            socket.on('error', (err) => {
                testResult.error = err.message;
                resolve(testResult);
            });

            socket.on('close', () => {
                clearTimeout(timer);
                resolve(testResult);
            });

            socket.connect(port, ip);
        });
    }

    /**
     * Envia comando ZPL de teste para a impressora
     */
    async sendTestZPL(ip, port = 9100, timeout = 10000) {
        return new Promise((resolve) => {
            const socket = new net.Socket();
            let testResult = {
                ip: ip,
                port: port,
                zplSent: false,
                response: null,
                error: null,
                timestamp: new Date().toISOString()
            };

            const timer = setTimeout(() => {
                testResult.error = 'Timeout ao enviar ZPL';
                socket.destroy();
                resolve(testResult);
            }, timeout);

            // Comando ZPL de teste simples
            const testZPL = `^XA
^FO50,50^A0N,50,50^FDTeste RFID ZD621R^FS
^FO50,120^BY3^BCN,100,Y,N,N^FD123456789^FS
^FO50,250^A0N,30,30^FDIP: ${ip}^FS
^FO50,290^A0N,30,30^FDData: ${new Date().toLocaleString('pt-BR')}^FS
^XZ`;

            socket.on('connect', () => {
                socket.write(testZPL, (err) => {
                    if (err) {
                        testResult.error = err.message;
                    } else {
                        testResult.zplSent = true;
                    }
                    socket.destroy();
                });
            });

            socket.on('error', (err) => {
                testResult.error = err.message;
                resolve(testResult);
            });

            socket.on('close', () => {
                clearTimeout(timer);
                resolve(testResult);
            });

            socket.connect(port, ip);
        });
    }

    /**
     * Verifica status da impressora via HTTP (se suportado)
     */
    async checkPrinterStatus(ip, timeout = 5000) {
        const testResult = {
            ip: ip,
            httpStatus: false,
            statusData: null,
            error: null,
            timestamp: new Date().toISOString()
        };

        try {
            // Tentar acessar interface web da impressora
            const response = await axios.get(`http://${ip}`, { timeout });
            testResult.httpStatus = true;
            testResult.statusData = {
                status: response.status,
                headers: response.headers,
                title: response.data.includes('<title>') ? 
                    response.data.match(/<title>(.*?)<\/title>/)?.[1] : 'Interface Zebra'
            };
        } catch (error) {
            testResult.error = error.message;
        }

        return testResult;
    }

    /**
     * Executa teste completo de comunicação
     */
    async runFullTest(ip, port = 9100) {
        console.log(`Iniciando teste completo para impressora ${ip}:${port}`);
        
        const results = {
            ip: ip,
            port: port,
            timestamp: new Date().toISOString(),
            tests: {}
        };

        // Teste 1: Conectividade TCP
        console.log(`Testando conectividade TCP...`);
        results.tests.tcp = await this.testTCPConnection(ip, port);

        // Teste 2: Envio de ZPL
        if (results.tests.tcp.tcpConnected) {
            console.log(`Enviando comando ZPL de teste...`);
            results.tests.zpl = await this.sendTestZPL(ip, port);
        }

        // Teste 3: Status HTTP
        console.log(`Verificando status HTTP...`);
        results.tests.http = await this.checkPrinterStatus(ip);

        // Teste 4: Informações da impressora
        results.tests.info = {
            model: 'Zebra ZD621R',
            capabilities: ['RFID', 'ZPL', 'TCP/IP', 'USB'],
            supportedFormats: ['ZPL', 'EPL'],
            maxPrintWidth: '4 inches',
            maxPrintLength: 'unlimited',
            dpi: '203 dpi'
        };

        this.testResults.push(results);
        return results;
    }

    /**
     * Gera relatório de teste
     */
    generateTestReport() {
        const report = {
            timestamp: new Date().toISOString(),
            summary: {
                totalPrinters: this.discoveredPrinters.length,
                testedPrinters: this.testResults.length,
                successfulConnections: this.testResults.filter(r => r.tests.tcp?.tcpConnected).length,
                successfulZPL: this.testResults.filter(r => r.tests.zpl?.zplSent).length
            },
            discoveredPrinters: this.discoveredPrinters,
            testResults: this.testResults
        };

        return report;
    }

    /**
     * Salva relatório em arquivo
     */
    async saveTestReport(filename = null) {
        const report = this.generateTestReport();
        
        if (!filename) {
            const timestamp = new Date().toISOString().replace(/[:.]/g, '-');
            filename = `rfid-printer-test-${timestamp}.json`;
        }

        const filepath = path.join(__dirname, 'test-reports', filename);
        
        // Criar diretório se não existir
        const dir = path.dirname(filepath);
        if (!fs.existsSync(dir)) {
            fs.mkdirSync(dir, { recursive: true });
        }

        fs.writeFileSync(filepath, JSON.stringify(report, null, 2));
        return filepath;
    }

    /**
     * Testa impressora específica por IP
     */
    async testSpecificPrinter(ip, port = 9100) {
        console.log(`Testando impressora específica: ${ip}:${port}`);
        
        // Adicionar à lista de impressoras descobertas se não existir
        if (!this.discoveredPrinters.find(p => p.ip === ip)) {
            this.discoveredPrinters.push({
                ip: ip,
                port: port,
                response: 'Manual entry',
                timestamp: new Date().toISOString()
            });
        }

        return await this.runFullTest(ip, port);
    }

    /**
     * Lista impressoras descobertas
     */
    getDiscoveredPrinters() {
        return this.discoveredPrinters;
    }

    /**
     * Limpa resultados de teste
     */
    clearResults() {
        this.discoveredPrinters = [];
        this.testResults = [];
    }
}

module.exports = RFIDPrinterTest;
