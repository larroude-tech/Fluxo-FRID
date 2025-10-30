const { spawn, exec } = require('child_process');
const path = require('path');
const fs = require('fs');

class PythonUSBIntegration {
    constructor() {
        this.printerName = "ZDesigner ZD621R-203dpi ZPL";
        this.isConnected = false;
        this.lastTestResult = null;
    }

    /**
     * Executa script Python e retorna resultado
     */
    async executePythonScript(scriptContent, args = []) {
        return new Promise((resolve, reject) => {
            // Criar arquivo temporário do script
            const tempScriptPath = path.join(__dirname, `temp_script_${Date.now()}.py`);
            
            try {
                fs.writeFileSync(tempScriptPath, scriptContent, 'utf8');
                
                // Executar script Python
                const pythonProcess = spawn('python', [tempScriptPath, ...args], {
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
                    try {
                        fs.unlinkSync(tempScriptPath);
                    } catch (e) {
                        // Ignorar erro de limpeza
                    }
                    
                    if (code === 0) {
                        resolve({
                            success: true,
                            output: stdout,
                            error: stderr,
                            code: code
                        });
                    } else {
                        reject({
                            success: false,
                            output: stdout,
                            error: stderr,
                            code: code
                        });
                    }
                });
                
                pythonProcess.on('error', (error) => {
                    // Limpar arquivo temporário
                    try {
                        fs.unlinkSync(tempScriptPath);
                    } catch (e) {
                        // Ignorar erro de limpeza
                    }
                    
                    reject({
                        success: false,
                        error: error.message,
                        code: -1
                    });
                });
                
            } catch (error) {
                reject({
                    success: false,
                    error: error.message,
                    code: -1
                });
            }
        });
    }

    /**
     * Testa conexão com a impressora
     */
    async testConnection() {
        console.log('🧪 Testando conexão USB via Python...');
        
        const pythonScript = `
import win32print
import time

def test_usb_connection():
    printer_name = "${this.printerName}"
    
    try:
        # Verificar se impressora existe
        handle = win32print.OpenPrinter(printer_name)
        
        # Obter informações
        info = win32print.GetPrinter(handle, 2)
        
        result = {
            "success": True,
            "printer_name": info['pPrinterName'],
            "port": info['pPortName'],
            "driver": info['pDriverName'],
            "status": info['Status'],
            "jobs_in_queue": info['cJobs'],
            "online": info['Status'] == 0
        }
        
        win32print.ClosePrinter(handle)
        
        print("SUCCESS:" + str(result).replace("'", '"').replace('True', 'true').replace('False', 'false'))
        
    except Exception as e:
        error_result = {
            "success": False,
            "error": str(e)
        }
        print("ERROR:" + str(error_result).replace("'", '"').replace('True', 'true').replace('False', 'false'))

if __name__ == "__main__":
    test_usb_connection()
`;

        try {
            const result = await this.executePythonScript(pythonScript);
            
            // Parsear resultado
            const lines = result.output.split('\n');
            let testResult = null;
            
            for (const line of lines) {
                if (line.startsWith('SUCCESS:')) {
                    testResult = JSON.parse(line.replace('SUCCESS:', ''));
                    this.isConnected = testResult.online;
                    break;
                } else if (line.startsWith('ERROR:')) {
                    testResult = JSON.parse(line.replace('ERROR:', ''));
                    this.isConnected = false;
                    break;
                }
            }
            
            this.lastTestResult = testResult;
            
            console.log('✅ Teste de conexão USB concluído:', testResult);
            
            return {
                success: true,
                result: testResult,
                timestamp: new Date().toISOString()
            };
            
        } catch (error) {
            console.error('❌ Erro no teste de conexão USB:', error);
            
            this.isConnected = false;
            this.lastTestResult = { success: false, error: error.error || error.message };
            
            return {
                success: false,
                error: error.error || error.message,
                timestamp: new Date().toISOString()
            };
        }
    }

    /**
     * Envia comando ZPL para a impressora
     */
    async sendZPL(zplCommand, encoding = 'ascii', copies = 1) {
        console.log(`📤 Enviando ZPL via Python USB (${copies} cópia${copies > 1 ? 's' : ''})...`);
        
        const pythonScript = `
import win32print
import time

def send_zpl_command():
    printer_name = "${this.printerName}"
    copies = ${copies}
    zpl_command = """${zplCommand.replace(/"/g, '\\"')}"""
    
    # Ajustar comando ^PQ para número de cópias
    if copies > 1:
        # Substituir ^PQ1,0,1,Y por ^PQ{copies},0,1,Y
        import re
        zpl_command = re.sub(r'\\^PQ\\d+,0,1,Y', f'^PQ{copies},0,1,Y', zpl_command)
        # Se não encontrar ^PQ, adicionar antes de ^XZ
        if '^PQ' not in zpl_command:
            zpl_command = zpl_command.replace('^XZ', f'^PQ{copies},0,1,Y\\n^XZ')
    
    try:
        # Abrir impressora
        handle = win32print.OpenPrinter(printer_name)
        
        # Configurar para modo RAW
        doc_info = ("Python_ZPL_Job", None, "RAW")
        
        # Iniciar job
        job_id = win32print.StartDocPrinter(handle, 1, doc_info)
        
        # Enviar dados
        win32print.StartPagePrinter(handle)
        bytes_written = win32print.WritePrinter(handle, zpl_command.encode('${encoding}', errors='ignore'))
        win32print.EndPagePrinter(handle)
        win32print.EndDocPrinter(handle)
        
        # Verificar status
        info = win32print.GetPrinter(handle, 2)
        
        win32print.ClosePrinter(handle)
        
        result = {
            "success": True,
            "job_id": job_id,
            "bytes_written": bytes_written,
            "jobs_in_queue": info['cJobs'],
            "printer_status": info['Status'],
            "copies_sent": copies
        }
        
        print("SUCCESS:" + str(result).replace("'", '"').replace('True', 'true').replace('False', 'false'))
        
    except Exception as e:
        error_result = {
            "success": False,
            "error": str(e)
        }
        print("ERROR:" + str(error_result).replace("'", '"').replace('True', 'true').replace('False', 'false'))

if __name__ == "__main__":
    send_zpl_command()
`;

        try {
            const result = await this.executePythonScript(pythonScript);
            
            // Parsear resultado
            const lines = result.output.split('\n');
            let sendResult = null;
            
            for (const line of lines) {
                if (line.startsWith('SUCCESS:')) {
                    sendResult = JSON.parse(line.replace('SUCCESS:', ''));
                    break;
                } else if (line.startsWith('ERROR:')) {
                    sendResult = JSON.parse(line.replace('ERROR:', ''));
                    break;
                }
            }
            
            console.log('✅ ZPL enviado via Python USB:', sendResult);
            
            return {
                success: sendResult?.success || false,
                result: sendResult,
                timestamp: new Date().toISOString()
            };
            
        } catch (error) {
            console.error('❌ Erro ao enviar ZPL via Python USB:', error);
            
            return {
                success: false,
                error: error.error || error.message,
                timestamp: new Date().toISOString()
            };
        }
    }

    /**
     * Lista impressoras disponíveis
     */
    async listPrinters() {
        console.log('🔍 Listando impressoras via Python...');
        
        const pythonScript = `
import win32print

def list_printers():
    try:
        printers = win32print.EnumPrinters(win32print.PRINTER_ENUM_LOCAL | win32print.PRINTER_ENUM_CONNECTIONS)
        
        printer_list = []
        for printer in printers:
            printer_info = {
                "name": printer[2],
                "server": printer[1] or "",
                "description": printer[0] or ""
            }
            printer_list.append(printer_info)
        
        result = {
            "success": True,
            "printers": printer_list,
            "count": len(printer_list)
        }
        
        print("SUCCESS:" + str(result).replace("'", '"').replace('True', 'true').replace('False', 'false'))
        
    except Exception as e:
        error_result = {
            "success": False,
            "error": str(e)
        }
        print("ERROR:" + str(error_result).replace("'", '"').replace('True', 'true').replace('False', 'false'))

if __name__ == "__main__":
    list_printers()
`;

        try {
            const result = await this.executePythonScript(pythonScript);
            
            // Parsear resultado
            const lines = result.output.split('\n');
            let listResult = null;
            
            for (const line of lines) {
                if (line.startsWith('SUCCESS:')) {
                    listResult = JSON.parse(line.replace('SUCCESS:', ''));
                    break;
                } else if (line.startsWith('ERROR:')) {
                    listResult = JSON.parse(line.replace('ERROR:', ''));
                    break;
                }
            }
            
            console.log('✅ Impressoras listadas via Python:', listResult);
            
            return {
                success: true,
                result: listResult,
                timestamp: new Date().toISOString()
            };
            
        } catch (error) {
            console.error('❌ Erro ao listar impressoras via Python:', error);
            
            return {
                success: false,
                error: error.error || error.message,
                timestamp: new Date().toISOString()
            };
        }
    }

    /**
     * Envia ZPL de teste
     */
    async sendTestZPL() {
        const testZPL = `^XA
^FO50,50^A0N,40,40^FDTeste USB Python^FS
^FO50,100^A0N,25,25^FDData: ${new Date().toLocaleString('pt-BR')}^FS
^FO50,130^A0N,25,25^FDPython Integration^FS
^FO50,160^A0N,20,20^FDImpressora: ${this.printerName}^FS
^XZ`;

        return await this.sendZPL(testZPL);
    }

    /**
     * Obtém status da integração
     */
    getStatus() {
        return {
            printerName: this.printerName,
            isConnected: this.isConnected,
            lastTestResult: this.lastTestResult,
            timestamp: new Date().toISOString()
        };
    }

    /**
     * Executa teste completo
     */
    async fullTest() {
        console.log('🚀 Executando teste completo Python USB...');
        
        try {
            // 1. Listar impressoras
            const listResult = await this.listPrinters();
            
            // 2. Testar conexão
            const connectionResult = await this.testConnection();
            
            // 3. Enviar ZPL de teste se conectado
            let zplResult = null;
            if (this.isConnected) {
                zplResult = await this.sendTestZPL();
            }
            
            const fullResult = {
                success: true,
                list: listResult,
                connection: connectionResult,
                zplTest: zplResult,
                summary: {
                    printersFound: listResult.result?.count || 0,
                    connectionSuccess: this.isConnected,
                    zplSent: zplResult?.success || false
                },
                timestamp: new Date().toISOString()
            };
            
            console.log('✅ Teste completo Python USB concluído');
            return fullResult;
            
        } catch (error) {
            console.error('❌ Erro no teste completo Python USB:', error);
            
            return {
                success: false,
                error: error.message,
                timestamp: new Date().toISOString()
            };
        }
    }
}

module.exports = PythonUSBIntegration;
