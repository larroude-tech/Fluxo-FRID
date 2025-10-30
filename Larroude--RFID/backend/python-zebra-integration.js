const { exec } = require('child_process');
const path = require('path');

class PythonZebraIntegration {
    constructor() {
        this.pythonScriptPath = path.join(__dirname, '..', 'zebra_printer_api.py');
        this.isConnected = false;
        this.printerName = null;
    }

    /**
     * Executa comando Python e retorna resultado JSON
     */
    async executePythonCommand(command, args = []) {
        return new Promise((resolve, reject) => {
            const fullCommand = `python "${this.pythonScriptPath}" ${command} ${args.join(' ')}`;
            
            console.log(`🐍 Executando: ${fullCommand}`);
            
            exec(fullCommand, (error, stdout, stderr) => {
                if (error) {
                    console.error('❌ Erro ao executar Python:', error);
                    reject(error);
                    return;
                }
                
                if (stderr) {
                    console.warn('⚠️ Aviso Python:', stderr);
                }
                
                try {
                    const result = JSON.parse(stdout.trim());
                    resolve(result);
                } catch (parseError) {
                    console.error('❌ Erro ao parsear JSON:', parseError);
                    console.error('Saída Python:', stdout);
                    reject(new Error('Resposta inválida do Python'));
                }
            });
        });
    }

    /**
     * Detecta impressoras Zebra
     */
    async detectPrinters() {
        try {
            console.log('🔍 Detectando impressoras via Python...');
            const result = await this.executePythonCommand('detect');
            
            if (result.success) {
                console.log(`✅ ${result.count} impressora(s) detectada(s) via Python`);
            } else {
                console.error('❌ Falha na detecção Python:', result.error);
            }
            
            return result;
        } catch (error) {
            console.error('❌ Erro na detecção Python:', error);
            return {
                success: false,
                error: error.message,
                printers: [],
                count: 0,
                timestamp: new Date().toISOString()
            };
        }
    }

    /**
     * Conecta à impressora Zebra
     */
    async connect(printerName = null) {
        try {
            console.log('🔌 Conectando via Python...');
            
            const args = printerName ? [printerName] : [];
            const result = await this.executePythonCommand('connect', args);
            
            if (result.success) {
                this.isConnected = true;
                this.printerName = result.printer_name;
                console.log(`✅ Conectado via Python: ${result.printer_name}`);
            } else {
                console.error('❌ Falha na conexão Python:', result.error);
            }
            
            return result;
        } catch (error) {
            console.error('❌ Erro na conexão Python:', error);
            return {
                success: false,
                error: error.message,
                timestamp: new Date().toISOString()
            };
        }
    }

    /**
     * Envia comando ZPL
     */
    async sendZPL(zplCommand) {
        try {
            if (!this.isConnected) {
                throw new Error('Impressora não está conectada');
            }
            
            console.log('📤 Enviando ZPL via Python...');
            const result = await this.executePythonCommand('send_zpl', [zplCommand]);
            
            if (result.success) {
                console.log('✅ ZPL enviado com sucesso via Python');
            } else {
                console.error('❌ Falha no envio ZPL Python:', result.error);
            }
            
            return result;
        } catch (error) {
            console.error('❌ Erro no envio ZPL Python:', error);
            return {
                success: false,
                error: error.message,
                timestamp: new Date().toISOString()
            };
        }
    }

    /**
     * Testa conectividade
     */
    async testConnection() {
        try {
            console.log('🧪 Testando conectividade via Python...');
            const result = await this.executePythonCommand('test');
            
            if (result.success) {
                console.log('✅ Teste de conectividade Python: OK');
                this.isConnected = true;
                this.printerName = result.printer_name;
            } else {
                console.error('❌ Falha no teste Python:', result.error);
                this.isConnected = false;
            }
            
            return result;
        } catch (error) {
            console.error('❌ Erro no teste Python:', error);
            this.isConnected = false;
            return {
                success: false,
                error: error.message,
                timestamp: new Date().toISOString()
            };
        }
    }

    /**
     * Desconecta da impressora
     */
    async disconnect() {
        try {
            console.log('🔌 Desconectando via Python...');
            const result = await this.executePythonCommand('disconnect');
            
            this.isConnected = false;
            this.printerName = null;
            
            if (result.success) {
                console.log('✅ Desconectado via Python');
            }
            
            return result;
        } catch (error) {
            console.error('❌ Erro na desconexão Python:', error);
            this.isConnected = false;
            this.printerName = null;
            return {
                success: false,
                error: error.message,
                timestamp: new Date().toISOString()
            };
        }
    }

    /**
     * Executa teste completo
     */
    async fullTest() {
        try {
            console.log('🚀 Executando teste completo via Python...');
            
            // 1. Detectar
            const detection = await this.detectPrinters();
            if (!detection.success || detection.count === 0) {
                return {
                    success: false,
                    error: 'Nenhuma impressora Zebra detectada',
                    detection: detection,
                    timestamp: new Date().toISOString()
                };
            }
            
            // 2. Testar conectividade (inclui conexão e teste)
            const testResult = await this.testConnection();
            
            return {
                success: testResult.success,
                detection: detection,
                testResult: testResult,
                timestamp: new Date().toISOString()
            };
            
        } catch (error) {
            console.error('❌ Erro no teste completo Python:', error);
            return {
                success: false,
                error: error.message,
                timestamp: new Date().toISOString()
            };
        }
    }

    /**
     * Obtém status da conexão
     */
    getStatus() {
        return {
            isConnected: this.isConnected,
            printerName: this.printerName,
            connectionType: 'python-windows',
            timestamp: new Date().toISOString()
        };
    }
}

module.exports = PythonZebraIntegration;
