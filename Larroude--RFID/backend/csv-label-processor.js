const { exec, spawn } = require('child_process');
const path = require('path');
const fs = require('fs');
const os = require('os');

/**
 * Utilitários RFID para conversão hexadecimal (mesmo do server.js)
 */
class RFIDUtils {
  /**
   * Converte string para hexadecimal
   */
  static stringToHex(str) {
    if (!str || typeof str !== 'string') {
      throw new Error('Dados inválidos para conversão hexadecimal');
    }
    
    let hex = '';
    for (let i = 0; i < str.length; i++) {
      const charCode = str.charCodeAt(i);
      const hexValue = charCode.toString(16).padStart(2, '0').toUpperCase();
      hex += hexValue;
    }
    
    console.log(`🔄 CSV RFID Hex: "${str}" → "${hex}"`);
    return hex;
  }

  /**
   * Gera dados RFID no formato ZebraDesigner (Barcode + PO + Sequencial + Zeros)
   */
  static generateZebraDesignerFormat(barcode, poNumber, sequence, targetLength = 24) {
    // Garantir que barcode tenha 12 caracteres
    const barcodeFormatted = String(barcode || '000000000000').substring(0, 12).padStart(12, '0');
    
    // PO sem letras (apenas números)
    const poFormatted = String(poNumber || '0000').replace(/[^0-9]/g, '');
    
    // Sequencial
    const seqFormatted = String(sequence || 1);
    
    // Montar dados base
    const baseData = `${barcodeFormatted}${poFormatted}${seqFormatted}`;
    
    // Completar com zeros até atingir o tamanho desejado
    const rfidData = baseData.padEnd(targetLength, '0');
    
    console.log(`📡 CSV RFID ZebraDesigner Format:`);
    console.log(`   Barcode: ${barcodeFormatted} (12 chars)`);
    console.log(`   PO: ${poFormatted}`);
    console.log(`   Sequencial: ${seqFormatted}`);
    console.log(`   Final: ${rfidData} (${rfidData.length} chars)`);
    
    return rfidData;
  }

  /**
   * Valida dados RFID
   */
  static validateRFIDData(data) {
    if (!data || typeof data !== 'string') {
      throw new Error('Dados RFID são obrigatórios e devem ser string');
    }
    
    if (data.length === 0) {
      throw new Error('Dados RFID não podem estar vazios');
    }
    
    if (data.length > 50) {
      throw new Error('Dados RFID muito longos (máximo 50 caracteres)');
    }
    
    // Verificar se contém apenas caracteres válidos (apenas números para formato ZebraDesigner)
    const validChars = /^[0-9]+$/;
    if (!validChars.test(data)) {
      throw new Error('Dados RFID devem conter apenas números (formato ZebraDesigner)');
    }
    
    return true;
  }
}

class CSVLabelProcessor {
    constructor() {
        this.csvPath = path.join(__dirname, '..', 'exemplo.csv');
        this.printerName = "ZDesigner ZD621R-203dpi ZPL";
    }

    /**
     * Carrega dados do arquivo CSV
     */
    loadCSVData() {
        try {
            const csvContent = fs.readFileSync(this.csvPath, 'utf8');
            const lines = csvContent.split('\n').filter(line => line.trim());
            
            if (lines.length < 2) {
                return [];
            }

            const headers = lines[0].split(',');
            const labels = [];

            for (let i = 1; i < lines.length; i++) {
                const values = lines[i].split(',');
                if (values.length >= 4) {
                    labels.push({
                        index: i,
                        style_name: values[0].trim(),
                        vpm: values[1].trim(),
                        color: values[2].trim(),
                        size: values[3].trim()
                    });
                }
            }

            return labels;
        } catch (error) {
            console.error('❌ Erro ao carregar CSV:', error);
            return [];
        }
    }

    /**
     * Gera ZPL para uma etiqueta específica baseado no layout da imagem com RFID hexadecimal
     */
    generateZPLForLabel(labelData, rfidData = null, sequence = 1) {
        const { style_name, vpm, color, size } = labelData;
        
        console.log(`📋 CSV: Gerando etiqueta para ${style_name}`);
        
        // Extrair PO e Local do VPM (formato: L458-JASM-11.0-SILV-1885)
        const vpmParts = vpm.split('-');
        const poNumber = vpmParts.length > 0 ? vpmParts[0].replace('L', '') : '0000';
        const localNumber = vpmParts.length > 4 ? vpmParts[4].substring(0, 3) : '000';
        
        // Gerar código de barras (usar VPM ou criar um baseado nos dados)
        const barcode = vpm.replace(/-/g, '').substring(0, 12);
        
        // Gerar dados RFID no formato ZebraDesigner (se não fornecido dados customizados)
        let rfidContent;
        if (rfidData) {
            // Se dados customizados foram fornecidos, usar como está (assumindo que já estão no formato correto)
            rfidContent = String(rfidData);
        } else {
            // Gerar no formato ZebraDesigner: Barcode + PO + Sequencial + Zeros
            rfidContent = RFIDUtils.generateZebraDesignerFormat(barcode, poNumber, sequence, 24);
        }
        
        console.log(`📡 CSV: Dados RFID finais: ${rfidContent}`);
        
        // Validar dados RFID (enviar como string direta, igual ZebraDesigner)
        RFIDUtils.validateRFIDData(rfidContent);
        
        console.log(`📡 CSV: RFID formato ZebraDesigner (string direta): ${rfidContent}`);
        
        // Carregar template oficial da Larroud
        const fs = require('fs');
        const path = require('path');
        const templatePath = path.join(__dirname, 'TEMPLATE_LARROUD_ORIGINAL.zpl');
        
        let larroudTemplate;
        try {
            larroudTemplate = fs.readFileSync(templatePath, 'utf8');
        } catch (error) {
            console.error('Erro ao carregar template oficial:', error);
            // Fallback para template simples se oficial não estiver disponível (ATUALIZADO COM HEX)
            larroudTemplate = `^XA
^FO50,50^A0N,35,35^FD{STYLE_NAME}^FS
^FO50,100^A0N,28,28^FDVPM: {VPM}^FS
^FO50,140^A0N,28,28^FDCOLOR: {COLOR}^FS
^FO50,180^A0N,28,28^FDSIZE: {SIZE}^FS
^FO50,240^BY2,3,40^BCN,40,Y,N,N^FD{BARCODE}^FS
^FO500,50^BQN,2,4^FD{RFID_DATA}^FS
^FO600,200^A0N,20,20^FD{PO_INFO}^FS
^FO600,230^A0N,16,16^FD{LOCAL_INFO}^FS
^RFW,H,2,12,1^FD{RFID_DATA_HEX}^FS
^XZ`;
        }

        // Substituir variáveis no template com dados hexadecimais para RFID
        const zpl = larroudTemplate
            .replace('{STYLE_NAME}', style_name)
            .replace('{VPM}', vpm)
            .replace('{COLOR}', color)
            .replace('{SIZE}', size)
            .replace('{QR_DATA}', vpm)
            .replace('{PO_INFO}', `PO${poNumber}`)
            .replace('{LOCAL_INFO}', `Local.${localNumber}`)
            .replace('{BARCODE}', barcode)
            .replace('{RFID_DATA_HEX}', rfidContent)     // USAR DADOS COMO STRING DIRETA (igual ZebraDesigner)
            .replace('{RFID_DATA}', rfidContent);        // Manter compatibilidade para QR codes

        console.log(`✅ CSV: ZPL gerado com RFID string direta`);

        return zpl;
    }

    /**
     * Executa script Python para impressão
     */
    async executePythonPrint(zplCommand) {
        return new Promise((resolve, reject) => {
            const pythonScript = `
import win32print
import time

def print_zpl():
    printer_name = "${this.printerName}"
    zpl_command = """${zplCommand.replace(/"/g, '\\"').replace(/\n/g, '\\n')}"""
    
    try:
        # Abrir impressora
        handle = win32print.OpenPrinter(printer_name)
        
        # Configurar para modo RAW
        doc_info = ("CSV_Label_Print", None, "RAW")
        
        # Iniciar job
        job_id = win32print.StartDocPrinter(handle, 1, doc_info)
        
        # Enviar dados
        win32print.StartPagePrinter(handle)
        bytes_written = win32print.WritePrinter(handle, zpl_command.encode('ascii'))
        win32print.EndPagePrinter(handle)
        win32print.EndDocPrinter(handle)
        
        win32print.ClosePrinter(handle)
        
        print("SUCCESS:Job_ID_" + str(job_id) + "_Bytes_" + str(bytes_written))
        
    except Exception as e:
        print("ERROR:" + str(e))

if __name__ == "__main__":
    print_zpl()
`;

            // Criar arquivo temporário do script Python
            const tempScriptPath = path.join(os.tmpdir(), `csv_print_${Date.now()}.py`);
            
            fs.writeFile(tempScriptPath, pythonScript, 'utf8', (err) => {
                if (err) {
                    reject(new Error(`Erro ao criar script Python: ${err.message}`));
                    return;
                }
                
                // Executar script Python
                const pythonProcess = spawn('python', [tempScriptPath], {
                    stdio: ['pipe', 'pipe', 'pipe']
                });
                
                let stdout = '';
                let stderr = '';
                
                pythonProcess.stdout.on('data', (data) => {
                    stdout += data.toString();
                });
                
                pythonProcess.stderr.on('data', (data) => {
                    stderr += data.toString();
                });
                
                pythonProcess.on('close', (code) => {
                    // Limpar arquivo temporário
                    fs.unlink(tempScriptPath, () => {});
                    
                    if (stdout.includes('SUCCESS:')) {
                        const jobInfo = stdout.replace('SUCCESS:', '').trim();
                        resolve({
                            success: true,
                            jobInfo: jobInfo,
                            code: code
                        });
                    } else if (stdout.includes('ERROR:')) {
                        const error = stdout.replace('ERROR:', '').trim();
                        reject(new Error(`Erro Python: ${error}`));
                    } else if (code === 0) {
                        resolve({
                            success: true,
                            jobInfo: 'Comando executado',
                            code: code
                        });
                    } else {
                        reject(new Error(`Processo Python falhou: código ${code}, stderr: ${stderr}`));
                    }
                });
                
                pythonProcess.on('error', (error) => {
                    // Limpar arquivo temporário
                    fs.unlink(tempScriptPath, () => {});
                    reject(new Error(`Erro ao executar Python: ${error.message}`));
                });
            });
        });
    }

    /**
     * Imprime uma etiqueta usando Python USB
     */
    async printLabel(zplData, labelInfo) {
        try {
            console.log(`🖨️ Imprimindo etiqueta: ${labelInfo.style_name}`);
            
            const result = await this.executePythonPrint(zplData);
            
            console.log(`✅ Etiqueta impressa com sucesso: ${result.jobInfo}`);
            
            return {
                success: true,
                message: `Etiqueta '${labelInfo.style_name}' enviada com sucesso`,
                label: labelInfo,
                jobInfo: result.jobInfo
            };
            
        } catch (error) {
            console.error(`❌ Erro ao imprimir etiqueta ${labelInfo.style_name}:`, error);
            throw new Error(`Erro ao imprimir etiqueta: ${error.message}`);
        }
    }

    /**
     * Imprime uma etiqueta específica por índice
     */
    async printSingleLabel(labelIndex, rfidData = null) {
        try {
            const labels = this.loadCSVData();
            
            if (labelIndex < 1 || labelIndex > labels.length) {
                throw new Error(`Índice inválido. Use um número entre 1 e ${labels.length}`);
            }

            const label = labels[labelIndex - 1];
            const zpl = this.generateZPLForLabel(label, rfidData);
            
            const result = await this.printLabel(zpl, label);
            return result;
            
        } catch (error) {
            throw new Error(`Erro ao imprimir etiqueta: ${error.message}`);
        }
    }

    /**
     * Imprime todas as etiquetas
     */
    async printAllLabels(rfidData = null) {
        try {
            const labels = this.loadCSVData();
            
            if (labels.length === 0) {
                throw new Error('Nenhuma etiqueta encontrada no CSV');
            }

            const results = [];
            let successCount = 0;

            for (let i = 0; i < labels.length; i++) {
                try {
                    const label = labels[i];
                    const zpl = this.generateZPLForLabel(label, rfidData);
                    
                    const result = await this.printLabel(zpl, label);
                    results.push(result);
                    successCount++;
                    
                    // Aguardar entre impressões
                    await new Promise(resolve => setTimeout(resolve, 2000));
                    
                } catch (error) {
                    results.push({
                        success: false,
                        error: error.message,
                        label: labels[i]
                    });
                }
            }

            return {
                success: true,
                message: `Processamento concluído: ${successCount}/${labels.length} etiquetas impressas`,
                total: labels.length,
                successCount,
                results
            };
            
        } catch (error) {
            throw new Error(`Erro ao imprimir todas as etiquetas: ${error.message}`);
        }
    }

    /**
     * Obtém informações do processador
     */
    getInfo() {
        const labels = this.loadCSVData();
        return {
            csvPath: this.csvPath,
            printerName: this.printerName,
            totalLabels: labels.length,
            labels: labels
        };
    }
}

module.exports = CSVLabelProcessor;
