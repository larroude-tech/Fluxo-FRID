const { SerialPort } = require('serialport');
const { ReadlineParser } = require('@serialport/parser-readline');

class USBPrinterConnection {
    constructor() {
        this.port = null;
        this.parser = null;
        this.isConnected = false;
        this.portInfo = null;
    }

    /**
     * Lista todas as portas seriais disponíveis
     */
    async listPorts() {
        try {
            const ports = await SerialPort.list();
            console.log('🔍 Portas seriais disponíveis:');
            
            const printerPorts = ports.filter(port => {
                // Filtrar portas que podem ser impressoras Zebra
                const manufacturer = port.manufacturer?.toLowerCase() || '';
                const productId = port.productId?.toLowerCase() || '';
                const vendorId = port.vendorId?.toLowerCase() || '';
                
                return manufacturer.includes('zebra') || 
                       manufacturer.includes('zd621r') ||
                       productId.includes('zebra') ||
                       vendorId.includes('0483') || // Zebra vendor ID comum
                       port.path.includes('COM'); // Portas COM no Windows
            });

            ports.forEach(port => {
                const isPrinter = printerPorts.includes(port);
                console.log(`${isPrinter ? '🖨️ ' : '📡 '} ${port.path}`);
                console.log(`   Fabricante: ${port.manufacturer || 'Desconhecido'}`);
                console.log(`   Produto: ${port.productId || 'Desconhecido'}`);
                console.log(`   Vendor ID: ${port.vendorId || 'Desconhecido'}`);
                console.log(`   Serial Number: ${port.serialNumber || 'N/A'}`);
                console.log('');
            });

            return {
                allPorts: ports,
                printerPorts: printerPorts
            };
        } catch (error) {
            console.error('❌ Erro ao listar portas:', error);
            throw error;
        }
    }

    /**
     * Conecta à impressora via USB
     */
    async connect(portPath, options = {}) {
        try {
            const defaultOptions = {
                baudRate: 9600,
                dataBits: 8,
                stopBits: 1,
                parity: 'none',
                rtscts: true,
                timeout: 5000
            };

            const connectionOptions = { ...defaultOptions, ...options };

            console.log(`🔌 Conectando à porta ${portPath}...`);
            console.log(`   Configuração: ${connectionOptions.baudRate} baud, ${connectionOptions.dataBits} bits, ${connectionOptions.parity} parity`);

            this.port = new SerialPort({
                path: portPath,
                ...connectionOptions
            });

            this.parser = this.port.pipe(new ReadlineParser({ delimiter: '\r\n' }));

            return new Promise((resolve, reject) => {
                const timeout = setTimeout(() => {
                    reject(new Error('Timeout de conexão'));
                }, connectionOptions.timeout);

                this.port.on('open', () => {
                    console.log('✅ Conexão USB estabelecida');
                    this.isConnected = true;
                    clearTimeout(timeout);
                    resolve(true);
                });

                this.port.on('error', (error) => {
                    console.error('❌ Erro na conexão USB:', error);
                    this.isConnected = false;
                    clearTimeout(timeout);
                    reject(error);
                });

                this.port.on('close', () => {
                    console.log('🔌 Conexão USB fechada');
                    this.isConnected = false;
                });

                this.parser.on('data', (data) => {
                    console.log(`📨 Resposta da impressora: ${data}`);
                });
            });

        } catch (error) {
            console.error('❌ Erro ao conectar via USB:', error);
            throw error;
        }
    }

    /**
     * Desconecta da impressora
     */
    async disconnect() {
        try {
            if (this.port && this.isConnected) {
                await this.port.close();
                this.isConnected = false;
                console.log('🔌 Desconectado da impressora USB');
            }
        } catch (error) {
            console.error('❌ Erro ao desconectar:', error);
            throw error;
        }
    }

    /**
     * Envia comando ZPL para a impressora
     */
    async sendZPL(zplCommand) {
        if (!this.port || !this.isConnected) {
            throw new Error('Impressora não está conectada');
        }

        try {
            console.log('📤 Enviando comando ZPL via USB...');
            console.log(`Comando: ${zplCommand.substring(0, 100)}...`);

            return new Promise((resolve, reject) => {
                const timeout = setTimeout(() => {
                    reject(new Error('Timeout ao enviar ZPL'));
                }, 10000);

                this.port.write(zplCommand, (error) => {
                    clearTimeout(timeout);
                    if (error) {
                        console.error('❌ Erro ao enviar ZPL:', error);
                        reject(error);
                    } else {
                        console.log('✅ Comando ZPL enviado com sucesso');
                        resolve(true);
                    }
                });
            });

        } catch (error) {
            console.error('❌ Erro ao enviar ZPL via USB:', error);
            throw error;
        }
    }

    /**
     * Envia comando de teste simples
     */
    async sendTestCommand() {
        const testZPL = `^XA
^FO50,50^A0N,50,50^FDTeste USB ZD621R^FS
^FO50,120^BY3^BCN,100,Y,N,N^FD123456789^FS
^FO50,250^A0N,30,30^FDUSB Test^FS
^FO50,290^A0N,30,30^FDData: ${new Date().toLocaleString('pt-BR')}^FS
^XZ`;

        return await this.sendZPL(testZPL);
    }

    /**
     * Obtém informações da conexão
     */
    getConnectionInfo() {
        return {
            isConnected: this.isConnected,
            portPath: this.port?.path || null,
            portInfo: this.portInfo,
            timestamp: new Date().toISOString()
        };
    }

    /**
     * Testa a conectividade da impressora
     */
    async testConnection() {
        try {
            console.log('🧪 Testando conectividade USB...');
            
            const result = {
                success: false,
                connectionInfo: null,
                testCommand: false,
                error: null,
                timestamp: new Date().toISOString()
            };

            // Verificar se está conectado
            if (!this.isConnected) {
                result.error = 'Impressora não está conectada';
                return result;
            }

            result.connectionInfo = this.getConnectionInfo();

            // Enviar comando de teste
            try {
                await this.sendTestCommand();
                result.testCommand = true;
                result.success = true;
            } catch (error) {
                result.error = error.message;
            }

            return result;

        } catch (error) {
            console.error('❌ Erro no teste de conectividade:', error);
            throw error;
        }
    }

    /**
     * Auto-detecta e conecta à impressora Zebra
     */
    async autoConnect() {
        try {
            console.log('🔍 Auto-detectando impressora Zebra...');
            
            const { printerPorts } = await this.listPorts();
            
            if (printerPorts.length === 0) {
                throw new Error('Nenhuma impressora Zebra detectada');
            }

            // Tentar conectar na primeira impressora encontrada
            const firstPrinter = printerPorts[0];
            console.log(`🖨️ Tentando conectar em: ${firstPrinter.path}`);
            
            this.portInfo = firstPrinter;
            await this.connect(firstPrinter.path);
            
            return {
                success: true,
                port: firstPrinter,
                message: 'Conectado automaticamente à impressora Zebra'
            };

        } catch (error) {
            console.error('❌ Erro na auto-conexão:', error);
            throw error;
        }
    }
}

module.exports = USBPrinterConnection;
