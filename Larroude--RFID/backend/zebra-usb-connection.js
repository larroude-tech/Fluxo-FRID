const { SerialPort } = require('serialport');
const { exec } = require('child_process');
const fs = require('fs');
const path = require('path');

class ZebraUSBConnection {
    constructor() {
        this.port = null;
        this.isConnected = false;
        this.connectionType = null;
    }

    /**
     * Detecta impressoras Zebra usando diferentes métodos
     */
    async detectPrinters() {
        console.log('🔍 Detectando impressoras Zebra...');
        
        const results = {
            serial: [],
            usb: [],
            network: [],
            windows: []
        };

        try {
            // 1. Tentar detectar via SerialPort
            console.log('📡 Verificando portas seriais...');
            const serialPorts = await SerialPort.list();
            results.serial = serialPorts.filter(port => {
                const manufacturer = port.manufacturer?.toLowerCase() || '';
                const productId = port.productId?.toLowerCase() || '';
                return manufacturer.includes('zebra') || productId.includes('zebra');
            });

            // 2. Tentar detectar via Windows Device Manager
            console.log('🖥️ Verificando dispositivos Windows...');
            const windowsDevices = await this.getWindowsDevices();
            results.windows = windowsDevices.filter(device => 
                device.toLowerCase().includes('zebra') || 
                device.toLowerCase().includes('zd621r')
            );

            // 3. Tentar detectar via USB (usando comando do sistema)
            console.log('🔌 Verificando dispositivos USB...');
            const usbDevices = await this.getUSBDevices();
            results.usb = usbDevices.filter(device => 
                device.toLowerCase().includes('zebra') || 
                device.toLowerCase().includes('zd621r')
            );

        } catch (error) {
            console.error('❌ Erro na detecção:', error.message);
        }

        return results;
    }

    /**
     * Obtém dispositivos do Windows Device Manager
     */
    async getWindowsDevices() {
        return new Promise((resolve, reject) => {
            exec('powershell "Get-PnpDevice | Where-Object {$_.FriendlyName -like \'*printer*\' -or $_.FriendlyName -like \'*zebra*\' -or $_.FriendlyName -like \'*usb*\'} | Select-Object FriendlyName"', (error, stdout, stderr) => {
                if (error) {
                    console.error('❌ Erro ao obter dispositivos Windows:', error);
                    resolve([]);
                    return;
                }
                
                const devices = stdout.split('\n')
                    .map(line => line.trim())
                    .filter(line => line.length > 0 && line !== 'FriendlyName' && line !== '----')
                    .filter(line => line.toLowerCase().includes('printer') || 
                                   line.toLowerCase().includes('zebra') ||
                                   line.toLowerCase().includes('usb'));
                
                resolve(devices);
            });
        });
    }

    /**
     * Obtém dispositivos USB
     */
    async getUSBDevices() {
        return new Promise((resolve, reject) => {
            exec('powershell "Get-WmiObject Win32_USBHub | Select-Object Name, DeviceID"', (error, stdout, stderr) => {
                if (error) {
                    console.error('❌ Erro ao obter dispositivos USB:', error);
                    resolve([]);
                    return;
                }
                
                const devices = stdout.split('\n')
                    .map(line => line.trim())
                    .filter(line => line.length > 0 && line !== 'Name' && line !== '----')
                    .filter(line => line.toLowerCase().includes('zebra') ||
                                   line.toLowerCase().includes('printer'));
                
                resolve(devices);
            });
        });
    }

    /**
     * Tenta conectar usando diferentes métodos
     */
    async connect(portPath = null, options = {}) {
        console.log('🔌 Tentando conectar à impressora Zebra...');

        // Se não foi especificada uma porta, tentar auto-detectar
        if (!portPath) {
            const detection = await this.detectPrinters();
            
            if (detection.serial.length > 0) {
                portPath = detection.serial[0].path;
                this.connectionType = 'serial';
            } else if (detection.windows.length > 0) {
                // Tentar usar o primeiro dispositivo Windows encontrado
                console.log('🖥️ Tentando conectar via dispositivo Windows...');
                return await this.connectViaWindows(detection.windows[0]);
            } else {
                throw new Error('Nenhuma impressora Zebra detectada');
            }
        }

        // Tentar conexão serial
        try {
            await this.connectSerial(portPath, options);
            return true;
        } catch (error) {
            console.log(`❌ Conexão serial falhou: ${error.message}`);
            
            // Tentar outras abordagens
            return await this.tryAlternativeConnections();
        }
    }

    /**
     * Conecta via porta serial
     */
    async connectSerial(portPath, options = {}) {
        const defaultOptions = {
            baudRate: 9600,
            dataBits: 8,
            stopBits: 1,
            parity: 'none',
            rtscts: true,
            timeout: 5000
        };

        const connectionOptions = { ...defaultOptions, ...options };

        return new Promise((resolve, reject) => {
            this.port = new SerialPort({
                path: portPath,
                ...connectionOptions
            });

            const timeout = setTimeout(() => {
                reject(new Error('Timeout de conexão serial'));
            }, connectionOptions.timeout);

            this.port.on('open', () => {
                console.log('✅ Conexão serial estabelecida');
                this.isConnected = true;
                this.connectionType = 'serial';
                clearTimeout(timeout);
                resolve(true);
            });

            this.port.on('error', (error) => {
                console.error('❌ Erro na conexão serial:', error);
                this.isConnected = false;
                clearTimeout(timeout);
                reject(error);
            });

            this.port.on('close', () => {
                console.log('🔌 Conexão serial fechada');
                this.isConnected = false;
            });
        });
    }

    /**
     * Tenta conectar via Windows
     */
    async connectViaWindows(deviceName) {
        console.log(`🖥️ Tentando conectar via Windows: ${deviceName}`);
        
        // Para impressoras Zebra, muitas vezes precisamos usar o driver do Windows
        // Vou tentar enviar um comando via arquivo temporário
        
        try {
            const tempFile = path.join(__dirname, 'temp_zpl.txt');
            const testZPL = '^XA^FO50,50^A0N,30,30^FDTeste Windows^FS^XZ';
            
            fs.writeFileSync(tempFile, testZPL);
            
            // Tentar usar o comando copy do Windows para enviar para a impressora
            const printerName = deviceName.replace(/"/g, '');
            
            return new Promise((resolve, reject) => {
                exec(`copy "${tempFile}" "${printerName}"`, (error, stdout, stderr) => {
                    fs.unlinkSync(tempFile); // Limpar arquivo temporário
                    
                    if (error) {
                        console.error('❌ Erro ao enviar via Windows:', error);
                        reject(error);
                    } else {
                        console.log('✅ Comando enviado via Windows');
                        this.isConnected = true;
                        this.connectionType = 'windows';
                        resolve(true);
                    }
                });
            });
            
        } catch (error) {
            console.error('❌ Erro na conexão Windows:', error);
            throw error;
        }
    }

    /**
     * Tenta conexões alternativas
     */
    async tryAlternativeConnections() {
        console.log('🔄 Tentando conexões alternativas...');
        
        // Tentar diferentes baud rates
        const baudRates = [9600, 19200, 38400, 57600, 115200];
        
        for (const baudRate of baudRates) {
            try {
                console.log(`📡 Tentando baud rate: ${baudRate}`);
                await this.connectSerial('COM1', { baudRate });
                return true;
            } catch (error) {
                console.log(`❌ Baud rate ${baudRate} falhou: ${error.message}`);
            }
        }
        
        throw new Error('Nenhuma conexão alternativa funcionou');
    }

    /**
     * Envia comando ZPL
     */
    async sendZPL(zplCommand) {
        if (!this.isConnected) {
            throw new Error('Impressora não está conectada');
        }

        try {
            console.log('📤 Enviando comando ZPL...');
            
            if (this.connectionType === 'serial') {
                return await this.sendZPLSerial(zplCommand);
            } else if (this.connectionType === 'windows') {
                return await this.sendZPLWindows(zplCommand);
            } else {
                throw new Error('Tipo de conexão não suportado');
            }
        } catch (error) {
            console.error('❌ Erro ao enviar ZPL:', error);
            throw error;
        }
    }

    /**
     * Envia ZPL via conexão serial
     */
    async sendZPLSerial(zplCommand) {
        return new Promise((resolve, reject) => {
            const timeout = setTimeout(() => {
                reject(new Error('Timeout ao enviar ZPL'));
            }, 10000);

            this.port.write(zplCommand, (error) => {
                clearTimeout(timeout);
                if (error) {
                    reject(error);
                } else {
                    console.log('✅ Comando ZPL enviado via serial');
                    resolve(true);
                }
            });
        });
    }

    /**
     * Envia ZPL via Windows
     */
    async sendZPLWindows(zplCommand) {
        const tempFile = path.join(__dirname, 'temp_zpl.txt');
        
        try {
            fs.writeFileSync(tempFile, zplCommand);
            
            return new Promise((resolve, reject) => {
                exec(`copy "${tempFile}" "Zebra ZD621R"`, (error, stdout, stderr) => {
                    fs.unlinkSync(tempFile);
                    
                    if (error) {
                        reject(error);
                    } else {
                        console.log('✅ Comando ZPL enviado via Windows');
                        resolve(true);
                    }
                });
            });
        } catch (error) {
            if (fs.existsSync(tempFile)) {
                fs.unlinkSync(tempFile);
            }
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
            }
            this.isConnected = false;
            console.log('🔌 Desconectado da impressora');
        } catch (error) {
            console.error('❌ Erro ao desconectar:', error);
            throw error;
        }
    }

    /**
     * Testa a conectividade
     */
    async testConnection() {
        try {
            console.log('🧪 Testando conectividade...');
            
            const testZPL = `^XA
^FO50,50^A0N,50,50^FDTeste Zebra USB^FS
^FO50,120^BY3^BCN,100,Y,N,N^FD123456789^FS
^FO50,250^A0N,30,30^FDUSB Test^FS
^FO50,290^A0N,30,30^FDData: ${new Date().toLocaleString('pt-BR')}^FS
^XZ`;

            await this.sendZPL(testZPL);
            
            return {
                success: true,
                connectionType: this.connectionType,
                timestamp: new Date().toISOString()
            };
        } catch (error) {
            return {
                success: false,
                error: error.message,
                timestamp: new Date().toISOString()
            };
        }
    }
}

module.exports = ZebraUSBConnection;
