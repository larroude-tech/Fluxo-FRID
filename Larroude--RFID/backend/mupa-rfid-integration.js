const { exec } = require('child_process');
const path = require('path');
const fs = require('fs');
const os = require('os');

class MupaRFIDIntegration {
    constructor() {
        this.printerName = "ZDesigner ZD621R-203dpi ZPL";
        this.isConnected = false;
    }

    /**
     * Converte string para hexadecimal
     * @param {string} str - String para converter
     * @returns {string} - String em formato hexadecimal
     */
    stringToHex(str) {
        if (!str || typeof str !== 'string') {
            throw new Error('Dados inválidos para conversão hexadecimal');
        }
        
        let hex = '';
        for (let i = 0; i < str.length; i++) {
            const charCode = str.charCodeAt(i);
            const hexValue = charCode.toString(16).padStart(2, '0').toUpperCase();
            hex += hexValue;
        }
        
        console.log(`🔄 Conversão: "${str}" → "${hex}"`);
        return hex;
    }

    /**
     * Valida dados RFID antes do envio
     * @param {string} data - Dados para validar
     * @returns {boolean} - True se válidos
     */
    validateRFIDData(data) {
        if (!data || typeof data !== 'string') {
            throw new Error('Dados RFID são obrigatórios e devem ser string');
        }
        
        if (data.length === 0) {
            throw new Error('Dados RFID não podem estar vazios');
        }
        
        if (data.length > 50) {
            throw new Error('Dados RFID muito longos (máximo 50 caracteres)');
        }
        
        // Verificar se contém apenas caracteres válidos (alfanuméricos)
        const validChars = /^[A-Za-z0-9]+$/;
        if (!validChars.test(data)) {
            throw new Error('Dados RFID contêm caracteres inválidos (apenas A-Z, a-z, 0-9 permitidos)');
        }
        
        console.log(`✅ Dados RFID validados: "${data}" (${data.length} caracteres)`);
        return true;
    }

    /**
     * Gera ZPL para impressão de etiqueta
     */
    generateLabelZPL(text, additionalInfo = {}) {
        const date = new Date().toLocaleString('pt-BR');
        const { subtitle = "Teste RFID", showDate = true, showBarcode = false } = additionalInfo;
        
        // Dimensões da etiqueta 100mm x 37mm (203 DPI)
        const widthDots = 800;
        const heightDots = 296;
        
        let zpl = `^XA
^PW${widthDots}
^LL${heightDots}
^FO${widthDots/2 - 150},50^A0N,50,50^FD${text}^FS
^FO${widthDots/2 - 100},120^A0N,30,30^FD${subtitle}^FS`;
        
        if (showDate) {
            zpl += `\n^FO${widthDots/2 - 80},160^A0N,25,25^FDData: ${date}^FS`;
        }
        
        if (showBarcode) {
            zpl += `\n^FO${widthDots/2 - 120},200^BY3^BCN,100,Y,N,N^FD${text}^FS`;
        }
        
        zpl += '\n^XZ';
        return zpl;
    }

    /**
     * Gera ZPL para gravação RFID com dados em hexadecimal
     */
    generateRFIDZPL(data) {
        // Validar dados antes de processar
        this.validateRFIDData(data);
        
        // Gerar ZPL com dados como string direta (igual ZebraDesigner)
        const zpl = `^XA
^RFR,H,0,12,2^FS
^RFW,H,2,12,1^FD${data}^FS
^XZ`;
        
        console.log(`📡 ZPL RFID gerado:`);
        console.log(`   Dados string direta: ${data}`);
        console.log(`   ZPL: ${zpl.replace(/\n/g, '\\n')}`);
        
        return zpl;
    }

    /**
     * Gera ZPL combinado (impressão + RFID) com dados hexadecimais
     */
    generateCombinedZPL(text, additionalInfo = {}) {
        // Validar dados RFID
        this.validateRFIDData(text);
        
        const date = new Date().toLocaleString('pt-BR');
        const { subtitle = "Teste RFID", showDate = true, showBarcode = false } = additionalInfo;
        
        // Dimensões da etiqueta 100mm x 37mm (203 DPI)
        const widthDots = 800;
        const heightDots = 296;
        
        let zpl = `^XA
^PW${widthDots}
^LL${heightDots}
^RFR,H,0,12,2^FS
^RFW,H,2,12,1^FD${text}^FS
^FO${widthDots/2 - 150},50^A0N,50,50^FD${text}^FS
^FO${widthDots/2 - 100},120^A0N,30,30^FD${subtitle}^FS`;
        
        if (showDate) {
            zpl += `\n^FO${widthDots/2 - 80},160^A0N,25,25^FDData: ${date}^FS`;
        }
        
        if (showBarcode) {
            zpl += `\n^FO${widthDots/2 - 120},200^BY3^BCN,100,Y,N,N^FD${text}^FS`;
        }
        
        zpl += `\n^XZ`;
        
        console.log(`📡 ZPL Combinado gerado:`);
        console.log(`   Dados string direta: ${text}`);
        
        return zpl;
    }

    /**
     * Gera ZPL para leitura RFID
     */
    generateReadRFIDZPL() {
        return `^XA
^RFR,H,0,12,2^FS
^XZ`;
    }

    /**
     * Envia ZPL para a impressora
     */
    async sendZPL(zpl) {
        return new Promise((resolve, reject) => {
            // Criar arquivo temporário
            const tempFile = path.join(os.tmpdir(), `mupa_${Date.now()}.txt`);
            
            fs.writeFile(tempFile, zpl, 'utf8', (err) => {
                if (err) {
                    reject(new Error(`Erro ao criar arquivo temporário: ${err.message}`));
                    return;
                }

                // Enviar para impressora
                const command = `copy "${tempFile}" "${this.printerName}"`;
                
                exec(command, (error, stdout, stderr) => {
                    // Limpar arquivo temporário
                    fs.unlink(tempFile, () => {});
                    
                    if (error) {
                        reject(new Error(`Erro ao enviar para impressora: ${error.message}`));
                        return;
                    }

                    resolve({
                        success: true,
                        message: 'Comando enviado com sucesso',
                        output: stdout
                    });
                });
            });
        });
    }

    /**
     * Imprime etiqueta com texto
     */
    async printLabel(text, additionalInfo = {}) {
        try {
            const zpl = this.generateLabelZPL(text, additionalInfo);
            const result = await this.sendZPL(zpl);
            
            return {
                success: true,
                message: `Etiqueta "${text}" enviada para impressão`,
                zpl: zpl,
                result: result
            };
        } catch (error) {
            return {
                success: false,
                error: error.message
            };
        }
    }

    /**
     * Grava dados no RFID com validação e conversão hexadecimal
     */
    async writeRFID(data) {
        try {
            console.log(`📡 Iniciando gravação RFID: "${data}"`);
            
            // Gerar ZPL com validação e conversão hexadecimal
            const zpl = this.generateRFIDZPL(data);
            const result = await this.sendZPL(zpl);
            
            return {
                success: true,
                message: `Dados "${data}" enviados para gravação RFID como string direta (formato ZebraDesigner)`,
                originalData: data,
                zpl: zpl,
                result: result
            };
        } catch (error) {
            console.error(`❌ Erro na gravação RFID: ${error.message}`);
            return {
                success: false,
                error: error.message,
                originalData: data
            };
        }
    }

    /**
     * Imprime etiqueta e grava RFID em um único comando com validação hexadecimal
     */
    async printAndWriteRFID(text, additionalInfo = {}) {
        try {
            console.log(`📡 Iniciando impressão + gravação RFID: "${text}"`);
            
            // Gerar ZPL combinado com validação e conversão hexadecimal
            const zpl = this.generateCombinedZPL(text, additionalInfo);
            const result = await this.sendZPL(zpl);
            
            return {
                success: true,
                message: `Etiqueta "${text}" impressa e RFID gravado como string direta (formato ZebraDesigner)`,
                originalData: text,
                zpl: zpl,
                result: result
            };
        } catch (error) {
            console.error(`❌ Erro na impressão + gravação RFID: ${error.message}`);
            return {
                success: false,
                error: error.message,
                originalData: text
            };
        }
    }

    /**
     * Lê dados do RFID
     */
    async readRFID() {
        try {
            const zpl = this.generateReadRFIDZPL();
            const result = await this.sendZPL(zpl);
            
            return {
                success: true,
                message: 'Comando de leitura RFID enviado',
                zpl: zpl,
                result: result
            };
        } catch (error) {
            return {
                success: false,
                error: error.message
            };
        }
    }

    /**
     * Teste completo MUPA
     */
    async testMupa(text = "MUPA_TESTE_01") {
        console.log(`🧪 Iniciando teste MUPA: ${text}`);
        
        const results = {
            label: null,
            rfid: null,
            combined: null,
            read: null
        };

        // Teste 1: Impressão da etiqueta
        console.log('📄 Testando impressão da etiqueta...');
        results.label = await this.printLabel(text, {
            subtitle: "Teste RFID",
            showDate: true
        });

        // Aguardar um pouco
        await new Promise(resolve => setTimeout(resolve, 1000));

        // Teste 2: Gravação RFID
        console.log('📄 Testando gravação RFID...');
        results.rfid = await this.writeRFID(text);

        // Aguardar um pouco
        await new Promise(resolve => setTimeout(resolve, 1000));

        // Teste 3: Comando combinado
        console.log('📄 Testando comando combinado...');
        results.combined = await this.printAndWriteRFID(text, {
            subtitle: "Teste RFID Avançado",
            showDate: true,
            showBarcode: true
        });

        // Aguardar um pouco
        await new Promise(resolve => setTimeout(resolve, 1000));

        // Teste 4: Leitura RFID
        console.log('📄 Testando leitura RFID...');
        results.read = await this.readRFID();

        return {
            success: true,
            message: 'Teste MUPA completo',
            results: results
        };
    }

    /**
     * Obtém status da conexão
     */
    getStatus() {
        return {
            connected: this.isConnected,
            printerName: this.printerName,
            timestamp: new Date().toISOString()
        };
    }
}

module.exports = MupaRFIDIntegration;
