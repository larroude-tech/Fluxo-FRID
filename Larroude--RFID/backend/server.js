const express = require('express');
const cors = require('cors');
const multer = require('multer');
const path = require('path');
const fs = require('fs');
const XLSX = require('xlsx');
const QRCode = require('qrcode');
const JsBarcode = require('jsbarcode');
const { PDFDocument, rgb } = require('pdf-lib');
const archiver = require('archiver');
const sharp = require('sharp');
const axios = require('axios');
const { Label } = require('node-zpl');

/**
 * Utilitários RFID para conversão hexadecimal
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
    
    console.log(`🔄 RFID Hex: "${str}" → "${hex}"`);
    return hex;
  }

  /**
   * Gera dados RFID no formato ZebraDesigner (Barcode + PO + Sequencial + Zeros)
   * Exemplo funcionou: 197416145132046412345678
   * Formato: [Barcode 12 chars] + [PO sem letras] + [Sequencial] + [Zeros para completar]
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
    
    console.log(`📡 RFID ZebraDesigner Format:`);
    console.log(`   Barcode: ${barcodeFormatted} (12 chars)`);
    console.log(`   PO: ${poFormatted}`);
    console.log(`   Sequencial: ${seqFormatted}`);
    console.log(`   Base: ${baseData} (${baseData.length} chars)`);
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

const app = express();
const PORT = process.env.PORT || 3002;

// Middleware
app.use(cors());
app.use(express.json({ limit: '50mb' }));
app.use(express.urlencoded({ limit: '50mb', extended: true }));
app.use(express.static('public'));

// ConfiguraÃ§Ã£o do multer para upload de arquivos
const storage = multer.diskStorage({
  destination: (req, file, cb) => {
    const uploadDir = 'uploads';
    if (!fs.existsSync(uploadDir)) {
      fs.mkdirSync(uploadDir);
    }
    cb(null, uploadDir);
  },
  filename: (req, file, cb) => {
    cb(null, Date.now() + '-' + file.originalname);
  }
});

const upload = multer({ 
  storage: storage,
  fileFilter: (req, file, cb) => {
    const allowedTypes = ['.xlsx', '.xls', '.csv'];
    const fileExt = path.extname(file.originalname).toLowerCase();
    if (allowedTypes.includes(fileExt)) {
      cb(null, true);
    } else {
      cb(new Error('Apenas arquivos Excel (.xlsx, .xls) ou CSV sÃ£o permitidos'));
    }
  }
});

// Rotas
app.get('/', (req, res) => {
  res.json({ message: 'Servidor LarroudÃ© RFID funcionando!' });
});

// Upload e processamento do arquivo Excel
app.post('/api/upload-excel', upload.single('excel'), async (req, res) => {
  try {
    if (!req.file) {
      return res.status(400).json({ error: 'Nenhum arquivo foi enviado' });
    }

    let data;
    const fileExt = path.extname(req.file.path).toLowerCase();
    
    if (fileExt === '.csv') {
      // Ler arquivo CSV
      const csvContent = fs.readFileSync(req.file.path, 'utf8');
      const lines = csvContent.split('\n').filter(line => line.trim());
      
      if (lines.length < 2) {
        return res.status(400).json({ error: 'Arquivo CSV deve ter pelo menos cabeÃ§alho e uma linha de dados' });
      }
      
      const headers = lines[0].split(',').map(h => h.trim());
      data = [];
      
      for (let i = 1; i < lines.length; i++) {
        const values = lines[i].split(',').map(v => v.trim());
        const row = {};
        headers.forEach((header, index) => {
          row[header] = values[index] || '';
        });
        data.push(row);
      }
    } else {
      // Ler arquivo Excel - processar apenas abas de etiquetas (excluir Sheet1 que Ã© banco de dados)
      const workbook = XLSX.readFile(req.file.path);
      data = [];
      
      // Iterar por todas as abas do arquivo, excluindo Sheet1
      for (const sheetName of workbook.SheetNames) {
        // Pular a aba Sheet1 pois Ã© o banco de dados de referÃªncia
        if (sheetName.toLowerCase() === 'sheet1') {
          continue;
        }
        
        const worksheet = workbook.Sheets[sheetName];
        const sheetData = XLSX.utils.sheet_to_json(worksheet);
        
        if (sheetData.length > 0) {
          // Adicionar dados da aba atual ao array principal
          data = data.concat(sheetData);
        }
      }
    }

    // Validar se o arquivo tem as colunas necessÃ¡rias
    const requiredColumns = ['NAME', 'DESCRIPTION', 'SKU', 'BARCODE', 'REF'];
    const alternativeColumns = ['Variant SKU', 'UPC']; // Formato alternativo
    
    if (data.length === 0) {
      return res.status(400).json({ error: 'Arquivo estÃ¡ vazio' });
    }
    
    // Separar dados por formato
    const standardData = [];
    const alternativeData = [];
    
    data.forEach(row => {
      const hasRequiredColumns = requiredColumns.every(col => col in row);
      const hasAlternativeColumns = alternativeColumns.every(col => col in row);
      
      if (hasRequiredColumns) {
        standardData.push(row);
      } else if (hasAlternativeColumns) {
        // Mapear formato alternativo para padrÃ£o
        const sku = row['Variant SKU'] || '';
        const skuParts = sku.split('-');
        const style = skuParts[1] || '';
        
        alternativeData.push({
          NAME: style,
          DESCRIPTION: `Produto ${style}`,
          SKU: sku,
          BARCODE: row['UPC'] || '',
          REF: sku.split('-')[0] || '',
          QTY: 1
        });
      }
    });
    
    // Combinar todos os dados processados
    data = [...standardData, ...alternativeData];
    
    if (data.length === 0) {
      return res.status(400).json({ 
        error: `Nenhuma aba com colunas vÃ¡lidas encontrada. Esperado: ${requiredColumns.join(', ')} ou ${alternativeColumns.join(', ')}` 
      });
    }
    
    // Processar dados com os novos campos
    data = data.map(row => {
      // Extrair cor e tamanho do SKU (formato: L264-HANA-5.0-WHIT-1120)
      const sku = row.SKU || '';
      const skuParts = sku.split('-');
      const size = skuParts.length >= 3 ? skuParts[2] : '';
      const colorCode = skuParts.length >= 4 ? skuParts[3] : '';
      
      // Mapear cÃ³digos de cor para nomes
      const colorMap = {
        'WHIT': 'WHITE',
        'BLCK': 'BLACK',
        'BRWN': 'BROWN',
        'NAVY': 'NAVY',
        'NUDE': 'NUDE',
        'SILV': 'SILVER',
        'GOLD': 'GOLD',
        'BEIG': 'BEIGE'
      };
      
      const color = colorMap[colorCode] || row.DESCRIPTION?.split(' ').pop() || colorCode || 'N/A';
      
      // Extrair PO do VPM/SKU (exemplo: L264-HANA-5.0-WHIT-1120 -> PO264)
      const vpm = row.SKU || '';
      const vpmParts = vpm.split('-');
      let poNumber = '';
      if (vpmParts.length > 0) {
        // Remover 'L' do início e extrair número do PO
        const firstPart = vpmParts[0].replace(/^L/, '');
        poNumber = firstPart || '0000';
      }

      return {
        STYLE_NAME: row.NAME || '',
        VPM: vpm,
        COLOR: color,
        SIZE: size || 'N/A',
        BARCODE: row.BARCODE || '',
        DESCRIPTION: row.DESCRIPTION || '',
        REF: row.REF || '',
        QTY: parseInt(row.QTY) || 1,
        PO: poNumber // Armazenar PO extraído
      };
    });

    // Limpar arquivo temporÃ¡rio
    fs.unlinkSync(req.file.path);

    res.json({
      message: 'Arquivo processado com sucesso',
      data: data,
      totalRecords: data.length
    });

  } catch (error) {
    console.error('Erro ao processar arquivo:', error);
    res.status(500).json({ error: 'Erro interno do servidor' });
  }
});

// Gerar preview das etiquetas
app.post('/api/generate-preview', async (req, res) => {
  try {
    const { data } = req.body;
    
    if (!data || !Array.isArray(data)) {
      return res.status(400).json({ error: 'Dados invÃ¡lidos' });
    }

    const previews = [];
    
    // Expandir dados baseado no campo QTY para calcular total de etiquetas
    let totalLabels = 0;
    for (const item of data) {
      const qty = parseInt(item.QTY) || 1;
      totalLabels += qty;
    }

    console.log(`Gerando previews para ${totalLabels} etiquetas de ${data.length} itens`);

    // Gerar previews para TODAS as etiquetas (sem limitaÃ§Ã£o)
    for (const item of data) {
      const qty = parseInt(item.QTY) || 1;
      
      for (let i = 0; i < qty; i++) {
        const preview = await generateLabelPreview(item);
        previews.push({
          ...preview,
          itemIndex: data.indexOf(item),
          copyNumber: i + 1,
          totalCopies: qty
        });
      }
    }

    console.log(`Previews gerados: ${previews.length}`);

    res.json({
      previews: previews,
      totalItems: data.length,
      totalLabels: totalLabels,
      previewCount: previews.length
    });

  } catch (error) {
    console.error('Erro ao gerar preview:', error);
    res.status(500).json({ error: 'Erro ao gerar preview' });
  }
});

// Imprimir etiqueta individual via Python USB (SEM VOID)
app.post('/api/print-individual', async (req, res) => {
  try {
    const { data, quantity } = req.body;
    
    if (!data || !Array.isArray(data) || data.length === 0) {
      return res.status(400).json({ error: 'Dados inválidos para impressão' });
    }

    const requestedQty = quantity || data.length;
    console.log(`🖨️ Imprimindo ${requestedQty} etiqueta(s) individual via Python USB...`);
    
    // Usar o módulo Python USB que funciona sem VOID
    const results = [];
    
    // Processar cada item com numeração sequencial
    let totalEtiquetasProcessadas = 0;
    for (const item of data) {
      const itemQty = parseInt(item.QTY) || 1;
      
      // Para cada item, gerar as etiquetas com numeração sequencial
      for (let seq = 1; seq <= itemQty; seq++) {
        totalEtiquetasProcessadas++;
        
        try {
          // Dados básicos do item
          const styleName = String(item.STYLE_NAME || 'N/A');
          const vpm = String(item.VPM || 'N/A');
          const color = String(item.COLOR || 'N/A');
          const size = String(item.SIZE || 'N/A');
          
          // Usar PO já extraído do upload, ou extrair do VPM como fallback
          const poNumber = item.PO || (vpm.split('-')[0] || '').replace('L', '') || '0000';
          const poFormatted = `PO${poNumber}`;
          
          // Gerar barcode sequencial: barcode + PO(sem letras) + sequencial
          const barcodeSource = String(item.BARCODE || vpm.replace(/-/g, '') || '00000000');
          const baseBarcode = barcodeSource.substring(0, 12); // Usar barcode completo para RFID
          const sequentialBarcode = `${barcodeSource.substring(0, 8)}${poNumber}${seq}`;
          
          // Dados para RFID: formato ZebraDesigner que funcionou (24 chars com zeros)
          // Exemplo: 197416145132046412345678
          const rfidContent = RFIDUtils.generateZebraDesignerFormat(baseBarcode, poNumber, seq, 24);
          
          // Extrair Local do VPM
          const vpmParts = vpm.split('-');
          const localNumber = vpmParts.length > 4 ? vpmParts[4].substring(0, 3) : '000';
        
        // Carregar template oficial da Larroud
        const fs = require('fs');
        const path = require('path');
        const templatePath = path.join(__dirname, 'TEMPLATE_LARROUD_ORIGINAL.zpl');
        let larroudTemplate;
        
        try {
          larroudTemplate = fs.readFileSync(templatePath, 'utf8');
        } catch (error) {
          console.error('Erro ao carregar template:', error);
          throw new Error('Template oficial não encontrado');
        }

          // Validar dados RFID (enviar como string direta, igual ZebraDesigner)
          RFIDUtils.validateRFIDData(rfidContent);
          
          console.log(`📡 RFID formato ZebraDesigner (string direta): ${rfidContent}`);
          
          // Substituir variáveis no template com dados sequenciais
          const workingZPL = larroudTemplate
            .replace('{STYLE_NAME}', styleName)
            .replace('{VPM}', vpm)
            .replace('{COLOR}', color)
            .replace('{SIZE}', size)
            .replace('{QR_DATA}', vpm)
            .replace('{PO_INFO}', poFormatted)
            .replace('{LOCAL_INFO}', `Local.${localNumber}`)
            .replace('{BARCODE}', sequentialBarcode) // Usar barcode sequencial
            .replace('{RFID_DATA_HEX}', rfidContent); // Enviar dados RFID como string direta (igual ZebraDesigner)

          // Imprimir cada etiqueta individual (1 cópia por vez para manter sequência)
          const printResult = await pythonUSBIntegration.sendZPL(workingZPL, 'ascii', 1);
          
          results.push({
            item: `${styleName} (${seq}/${itemQty})`,
            barcode: sequentialBarcode,
            rfid: rfidContent,
            success: printResult.success,
            message: printResult.success ? `Etiqueta ${seq} impressa com sucesso` : printResult.error,
            details: printResult.result
          });
          
          console.log(`✅ Etiqueta ${styleName} ${seq}/${itemQty} processada:`, printResult.success ? 'OK' : printResult.error);
          console.log(`   📊 Barcode: ${sequentialBarcode}`);
          console.log(`   📡 RFID String Direta: ${rfidContent}`);
          
        } catch (error) {
          console.error(`❌ Erro ao processar ${item.STYLE_NAME} ${seq}/${itemQty}:`, error);
          results.push({
            item: `${item.STYLE_NAME || 'Desconhecido'} (${seq}/${itemQty})`,
            success: false,
            message: error.message
          });
        }
      } // Fim do loop de sequência
    } // Fim do loop de itens
    
    const successCount = results.filter(r => r.success).length;
    
    res.json({
      message: `${successCount}/${results.length} etiquetas sequenciais impressas com sucesso`,
      results: results,
      totalItems: data.length,
      totalEtiquetas: totalEtiquetasProcessadas,
      successCount: successCount,
      timestamp: new Date().toISOString(),
      info: "Sistema com PO na RFID e barcode sequencial ativo"
    });

  } catch (error) {
    console.error('Erro na impressão individual:', error);
    res.status(500).json({ error: 'Erro interno do servidor' });
  }
});

// Gerar todas as etiquetas
app.post('/api/generate-labels', async (req, res) => {
  try {
    const { data } = req.body;
    
    if (!data || !Array.isArray(data)) {
      return res.status(400).json({ error: 'Dados invÃ¡lidos' });
    }

    const outputDir = 'output';
    if (!fs.existsSync(outputDir)) {
      fs.mkdirSync(outputDir);
    }

    const timestamp = Date.now();
    const zipFileName = `etiquetas-${timestamp}.zip`;
    const zipPath = path.join(outputDir, zipFileName);

    const output = fs.createWriteStream(zipPath);
    const archive = archiver('zip', { zlib: { level: 9 } });

    archive.pipe(output);

    let labelCounter = 1;
    let totalLabelsGenerated = 0;

    for (let i = 0; i < data.length; i++) {
      const item = data[i];
      const qty = parseInt(item.QTY) || 1;
      
      for (let copy = 1; copy <= qty; copy++) {
        try {
          const labelZPL = generateLabelZPL(item);
          const fileName = `etiqueta-${labelCounter}-${item.VPM || 'sem-vpm'}-copia-${copy}.zpl`;
          archive.append(Buffer.from(labelZPL, 'utf8'), { name: fileName });
          labelCounter++;
          totalLabelsGenerated++;
        } catch (error) {
          console.error(`Erro ao gerar etiqueta ${labelCounter}:`, error);
          throw error;
        }
      }
    }

    await archive.finalize();

    output.on('close', () => {
      res.json({
        message: 'Etiquetas ZPL geradas com sucesso',
        downloadUrl: `/api/download/${zipFileName}`,
        totalItems: data.length,
        totalLabels: totalLabelsGenerated
      });
    });

  } catch (error) {
    console.error('Erro ao gerar etiquetas ZPL:', error);
    res.status(500).json({ error: 'Erro ao gerar etiquetas ZPL' });
  }
});

// Download do arquivo ZIP
app.get('/api/download/:filename', (req, res) => {
  const filename = req.params.filename;
  const filePath = path.join('output', filename);
  
  if (fs.existsSync(filePath)) {
    res.download(filePath, (err) => {
      if (err) {
        console.error('Erro no download:', err);
      } else {
        // Limpar arquivo apÃ³s download
        setTimeout(() => {
          if (fs.existsSync(filePath)) {
            fs.unlinkSync(filePath);
          }
        }, 60000); // Remove apÃ³s 1 minuto
      }
    });
  } else {
    res.status(404).json({ error: 'Arquivo nÃ£o encontrado' });
  }
});

// FunÃ§Ã£o para gerar preview da etiqueta
async function generateLabelPreview(item) {
  try {
    // Importar o processador ZPL local
    const { processZPLToImage } = require("./zpl-processor");
    const fs = require('fs');
    const path = require('path');
    
    // Extrair dados do item
    const styleName = String(item.STYLE_NAME || item.NAME || "N/A");
    const vpm = String(item.VPM || item.SKU || "N/A");
    const color = String(item.COLOR || "N/A");
    const size = String(item.SIZE || "N/A");
    const barcode = String(item.BARCODE || item.VPM || "N/A");
    const ref = String(item.REF || "N/A");
    const qty = String(item.QTY || "1");

    // Gerar conteúdo dos QR codes conforme especificação
    const qrLeft = `LA,ESQ-QR-CONTENT`;
    const qrRightTop = `LA,DIR-QR-TOP`;
    const qrRightBottom = `LA,DIR-QR-BOTTOM`;
    const poLocal = `PO${ref}\\&Local.437`; // Formato: PO0656\&Local.437

    // Ler o template ZPL do arquivo
    const templatePath = path.join(__dirname, 'LAYOUT_LABEL.ZPL');
    let zplTemplate;
    
    try {
      zplTemplate = fs.readFileSync(templatePath, 'utf8');
    } catch (fileError) {
      console.error("Erro ao ler template ZPL:", fileError.message);
      throw new Error("Template ZPL não encontrado");
    }

    // Extrair apenas a definição do formato (primeira seção ^XA...^XZ)
    const templateMatch = zplTemplate.match(/\^XA[\s\S]*?\^XZ/);
    if (!templateMatch) {
      throw new Error("Template ZPL inválido");
    }
    
    let baseTemplate = templateMatch[0];
    
    // Substituir os ^FN placeholders com os dados reais
    baseTemplate = baseTemplate.replace(/\^FN1\^FS/g, `^FDSTYLE NAME: ${styleName}^FS`);
    baseTemplate = baseTemplate.replace(/\^FN2\^FS/g, `^FDVPN: ${vpm}^FS`);
    baseTemplate = baseTemplate.replace(/\^FN3\^FS/g, `^FDCOLOR: ${color}^FS`);
    baseTemplate = baseTemplate.replace(/\^FN4\^FS/g, `^FD${size}^FS`);
    baseTemplate = baseTemplate.replace(/\^FN5\^FS/g, `^FD${barcode}^FS`);
    baseTemplate = baseTemplate.replace(/\^FN6\^FS/g, `^FD${poLocal}^FS`);
    baseTemplate = baseTemplate.replace(/\^FN7\^FS/g, `^FD${qrLeft}^FS`);
    baseTemplate = baseTemplate.replace(/\^FN8\^FS/g, `^FD${qrRightBottom}^FS`);
    baseTemplate = baseTemplate.replace(/\^FN9\^FS/g, `^FD${qrRightTop}^FS`);

    // O ZPL final é o template com os dados substituídos
    const zplCode = baseTemplate;

    console.log("ZPL gerado para preview usando template ^FN:", zplCode.substring(0, 200) + "...");

    // Usar processador ZPL local
    const base64Image = await processZPLToImage(zplCode);
    
    return {
      id: item.VPM || item.SKU || Math.random().toString(36).substr(2, 9),
      styleName: styleName,
      vpm: vpm,
      color: color,
      size: size,
      barcode: barcode,
      ref: ref,
      qty: item.QTY || 1,
      preview: `data:image/png;base64,${base64Image}`
    };

  } catch (error) {
    console.error("Erro ao gerar preview:", error.message);
    throw error;
  }
}

// FunÃ§Ã£o para gerar ZPL da etiqueta usando sistema de templates ^FN
function generateLabelZPL(item) {
  // Gerar cÃ³digo ZPL inline (sem templates externos)
  // DimensÃµes: 4.0" x 2.0" (203 DPI) conforme especificaÃ§Ã£o
  
  const styleName = String(item.STYLE_NAME || item.NAME || 'N/A');
  const vpm = String(item.VPM || item.SKU || 'N/A');
  const color = String(item.COLOR || 'N/A');
  const size = String(item.SIZE || 'N/A');
  const barcode = String(item.BARCODE || item.VPM || 'N/A');
  const ref = String(item.REF || 'N/A');
  const qty = String(item.QTY || '1');
  
  // Gerar conteÃºdo conforme layout otimizado
  const poLocal = `${ref}\&Local.SP`; // PO na 1Âª linha e Local.xxx na 2Âª
  const qrLeft = `LA,ESQ-${vpm}-QTY:${qty}`; // QR esquerdo
  const qrTop = `LA,DIR-QR-TOP-${vpm}`; // QR superior direito
  const qrBottom = `LA,DIR-QR-BOTTOM-${vpm}`; // QR inferior direito
  
  // ZPL inline baseado no template LAYOUT_LABEL.ZPL
  const zplCode = `^XA
^CI28
^LH0,0
^MD30
^PR5
^PW812
^LL406

^FO10,10^GB792,386,2,B,0^FS

^FO20,20^GB50,50,2,B,0^FS
^FO25,25^A0N,16,16^FDðŸ‘ ^FS

^FO720,20^GB70,50,2,B,0^FS
^FO725,25^A0N,12,12^FDPO: ^FS
^FO725,40^A0N,12,12^FD${ref}^FS

^FO20,80^A0N,18,18^FD${styleName}^FS

^FO20,105^A0N,14,14^FDVPM:^FS
^FO70,105^A0N,14,14^FD${vpm}^FS

^FO20,125^A0N,14,14^FDCOLOR:^FS
^FO90,125^A0N,14,14^FD${color}^FS
^FO400,125^A0N,14,14^FDSIZE:^FS
^FO450,125^A0N,14,14^FD${size}^FS

^FO200,160^BY2,2,40^BCN,40,Y,N,N^FD${barcode}^FS

^FO20,220^BQN,2,3^FD${qrLeft}^FS

^FO650,220^BQN,2,3^FD${qrTop}^FS

^FO720,370^A0N,12,12^FD${ref}^FS
^XZ`;
  
  return zplCode;
}

async function generateLabelPDF(item) {
  const pdfDoc = await PDFDocument.create();
  // Tamanho baseado na proporÃ§Ã£o da imagem (aproximadamente 4:1)
  const page = pdfDoc.addPage([566, 142]); // 10cm x 2.5cm em pontos (72 DPI)
  
  const { width, height } = page.getSize();
  
  // Borda externa
  page.drawRectangle({
    x: 5,
    y: 5,
    width: width - 10,
    height: height - 10,
    borderColor: rgb(0, 0, 0),
    borderWidth: 1
  });
  
  // Ãrea principal da etiqueta
  page.drawRectangle({
    x: 10,
    y: 10,
    width: width - 120, // Deixa espaÃ§o para QR codes laterais
    height: height - 20,
    borderColor: rgb(0, 0, 0),
    borderWidth: 1
  });
  
  // QR Code removido - deixando espaÃ§o em branco conforme solicitado
  
  // InformaÃ§Ãµes do produto
  page.drawText(`NAME: ${String(item.STYLE_NAME || 'N/A')}`, {
    x: 65,
    y: height - 25,
    size: 10,
    color: rgb(0, 0, 0)
  });
  
  page.drawText(`SKU: ${String(item.VPM || 'N/A')}`, {
    x: 65,
    y: height - 40,
    size: 10,
    color: rgb(0, 0, 0)
  });
  
  page.drawText(`COLOR: ${String(item.COLOR || 'N/A')}`, {
    x: 65,
    y: height - 55,
    size: 10,
    color: rgb(0, 0, 0)
  });
  
  page.drawText(`SIZE: ${String(item.SIZE || 'N/A')}`, {
    x: 65,
    y: height - 70,
    size: 10,
    color: rgb(0, 0, 0)
  });
  
  // CÃ³digo de barras
  const barcodeWidth = 200;
  const barcodeHeight = 25;
  const barcodeX = 65;
  const barcodeY = 25;
  
  // Simular cÃ³digo de barras CODE128 usando BARCODE
  for (let i = 0; i < 50; i++) {
    const barWidth = Math.random() > 0.5 ? 2 : 1;
    const x = barcodeX + (i * 4);
    if (x < barcodeX + barcodeWidth) {
      page.drawRectangle({
        x: x,
        y: barcodeY,
        width: barWidth,
        height: barcodeHeight,
        color: rgb(0, 0, 0)
      });
    }
  }
  
  // Texto do cÃ³digo de barras usando BARCODE
  page.drawText(String(item.BARCODE || item.VPM || 'N/A'), {
    x: barcodeX + 50,
    y: barcodeY - 15,
    size: 8,
    color: rgb(0, 0, 0)
  });
  
  // QR Code grande removido - deixando espaÃ§o em branco conforme solicitado
  
  // CÃ³digo REF no canto inferior direito
  page.drawRectangle({
    x: width - 105,
    y: 15,
    width: 90,
    height: 35,
    borderColor: rgb(0, 0, 0),
    borderWidth: 1
  });
  
  page.drawText('REF:', {
    x: width - 95,
    y: 40,
    size: 10,
    color: rgb(0, 0, 0)
  });
  
  page.drawText(String(item.REF || 'N/A'), {
    x: width - 95,
    y: 25,
    size: 8,
    color: rgb(0, 0, 0)
  });
  
  // QR Code pequeno removido - deixando espaÃ§o em branco conforme solicitado
  
  return await pdfDoc.save();
}

// Importar módulo de teste de impressora RFID
const RFIDPrinterTest = require('./rfid-printer-test');

// Importar módulo de conexão USB
const USBPrinterConnection = require('./usb-printer-connection');
// Importar módulo de conexão Zebra USB
const ZebraUSBConnection = require('./zebra-usb-connection');
// Importar módulo de integração Python
const PythonZebraIntegration = require('./python-zebra-integration');
// Importar módulo de integração Python USB
const PythonUSBIntegration = require('./python-usb-integration');

// Importar módulo de integração MUPA RFID
const MupaRFIDIntegration = require('./mupa-rfid-integration');

// Instância global do testador
const rfidTester = new RFIDPrinterTest();

// Instância global da conexão USB
const usbConnection = new USBPrinterConnection();

// Instância global da conexão Zebra USB
const zebraUSBConnection = new ZebraUSBConnection();

// Instância global da integração Python
const pythonZebraIntegration = new PythonZebraIntegration();

// Instância global da integração Python USB
const pythonUSBIntegration = new PythonUSBIntegration();

// Instância global da integração MUPA RFID
const mupaRFIDIntegration = new MupaRFIDIntegration();

// Endpoints para teste de impressora RFID
app.get('/api/rfid/status', (req, res) => {
  res.json({ 
    status: 'online',
    service: 'RFID Printer Test Service',
    version: '1.0.0',
    timestamp: new Date().toISOString()
  });
});

// Descobrir impressoras na rede
app.post('/api/rfid/discover', async (req, res) => {
  try {
    const { timeout = 10000 } = req.body;
    console.log('🔍 Iniciando descoberta de impressoras RFID...');
    
    const printers = await rfidTester.discoverPrinters(timeout);
    
    res.json({
      success: true,
      printers: printers,
      count: printers.length,
      timestamp: new Date().toISOString()
    });
  } catch (error) {
    console.error('Erro na descoberta de impressoras:', error);
    res.status(500).json({
      success: false,
      error: error.message,
      timestamp: new Date().toISOString()
    });
  }
});

// Testar impressora específica
app.post('/api/rfid/test', async (req, res) => {
  try {
    const { ip, port = 9100 } = req.body;
    
    if (!ip) {
      return res.status(400).json({
        success: false,
        error: 'IP da impressora é obrigatório',
        timestamp: new Date().toISOString()
      });
    }
    
    console.log(`🧪 Testando impressora RFID ${ip}:${port}...`);
    
    const result = await rfidTester.testSpecificPrinter(ip, port);
    
    res.json({
      success: true,
      result: result,
      timestamp: new Date().toISOString()
    });
  } catch (error) {
    console.error('Erro no teste de impressora:', error);
    res.status(500).json({
      success: false,
      error: error.message,
      timestamp: new Date().toISOString()
    });
  }
});

// Executar teste completo (descoberta + teste)
app.post('/api/rfid/full-test', async (req, res) => {
  try {
    const { timeout = 10000 } = req.body;
    console.log('🚀 Iniciando teste completo de impressoras RFID...');
    
    // Descobrir impressoras
    const discovered = await rfidTester.discoverPrinters(timeout);
    
    if (discovered.length === 0) {
      return res.json({
        success: true,
        message: 'Nenhuma impressora descoberta automaticamente',
        discovered: [],
        tested: [],
        timestamp: new Date().toISOString()
      });
    }
    
    // Testar cada impressora descoberta
    const testResults = [];
    for (const printer of discovered) {
      console.log(`Testando ${printer.ip}:${printer.port}...`);
      const result = await rfidTester.testSpecificPrinter(printer.ip, printer.port);
      testResults.push(result);
    }
    
    // Gerar relatório
    const reportPath = await rfidTester.saveTestReport();
    
    res.json({
      success: true,
      discovered: discovered,
      tested: testResults,
      reportPath: reportPath,
      summary: rfidTester.generateTestReport().summary,
      timestamp: new Date().toISOString()
    });
  } catch (error) {
    console.error('Erro no teste completo:', error);
    res.status(500).json({
      success: false,
      error: error.message,
      timestamp: new Date().toISOString()
    });
  }
});

// Obter relatório de testes
app.get('/api/rfid/report', (req, res) => {
  try {
    const report = rfidTester.generateTestReport();
    res.json({
      success: true,
      report: report,
      timestamp: new Date().toISOString()
    });
  } catch (error) {
    console.error('Erro ao gerar relatório:', error);
    res.status(500).json({
      success: false,
      error: error.message,
      timestamp: new Date().toISOString()
    });
  }
});

// Limpar resultados de teste
app.post('/api/rfid/clear', (req, res) => {
  try {
    rfidTester.clearResults();
    res.json({
      success: true,
      message: 'Resultados de teste limpos',
      timestamp: new Date().toISOString()
    });
  } catch (error) {
    console.error('Erro ao limpar resultados:', error);
    res.status(500).json({
      success: false,
      error: error.message,
      timestamp: new Date().toISOString()
    });
  }
});

// ========================================
// ENDPOINTS PARA TESTE DE IMPRESSORA USB
// ========================================

// Status do serviço USB
app.get('/api/usb/status', (req, res) => {
  res.json({ 
    status: 'online',
    service: 'USB Printer Test Service',
    version: '1.0.0',
    timestamp: new Date().toISOString()
  });
});

// Detectar impressoras USB
app.post('/api/usb/detect', async (req, res) => {
  try {
    console.log('🔍 Detectando impressoras USB...');
    
    const detection = await zebraUSBConnection.detectPrinters();
    
    res.json({
      success: true,
      detection: detection,
      total: detection.serial.length + detection.windows.length + detection.usb.length,
      timestamp: new Date().toISOString()
    });
  } catch (error) {
    console.error('Erro na detecção USB:', error);
    res.status(500).json({
      success: false,
      error: error.message,
      timestamp: new Date().toISOString()
    });
  }
});

// Conectar e testar impressora USB
app.post('/api/usb/connect', async (req, res) => {
  try {
    const { portPath } = req.body;
    console.log('🔌 Conectando à impressora USB...');
    
    await zebraUSBConnection.connect(portPath);
    
    const testResult = await zebraUSBConnection.testConnection();
    
    // Desconectar após o teste
    await zebraUSBConnection.disconnect();
    
    res.json({
      success: true,
      result: testResult,
      timestamp: new Date().toISOString()
    });
  } catch (error) {
    console.error('Erro na conexão USB:', error);
    res.status(500).json({
      success: false,
      error: error.message,
      timestamp: new Date().toISOString()
    });
  }
});

// Auto-conectar e testar
app.post('/api/usb/auto-connect', async (req, res) => {
  try {
    console.log('🔍 Auto-conectando à impressora USB...');
    
    await zebraUSBConnection.connect();
    
    const testResult = await zebraUSBConnection.testConnection();
    
    // Desconectar após o teste
    await zebraUSBConnection.disconnect();
    
    res.json({
      success: true,
      result: testResult,
      timestamp: new Date().toISOString()
    });
  } catch (error) {
    console.error('Erro na auto-conexão USB:', error);
    res.status(500).json({
      success: false,
      error: error.message,
      timestamp: new Date().toISOString()
    });
  }
});

// Teste completo USB
app.post('/api/usb/full-test', async (req, res) => {
  try {
    console.log('🧪 Executando teste completo USB...');
    
    // 1. Detectar impressoras
    const detection = await zebraUSBConnection.detectPrinters();
    const totalDevices = detection.serial.length + detection.windows.length + detection.usb.length;
    
    if (totalDevices === 0) {
      return res.json({
        success: true,
        message: 'Nenhuma impressora USB detectada',
        detection: detection,
        testResult: null,
        timestamp: new Date().toISOString()
      });
    }
    
    // 2. Tentar conectar
    await zebraUSBConnection.connect();
    
    // 3. Testar conectividade
    const testResult = await zebraUSBConnection.testConnection();
    
    // 4. Desconectar
    await zebraUSBConnection.disconnect();
    
    res.json({
      success: true,
      detection: detection,
      testResult: testResult,
      timestamp: new Date().toISOString()
    });
  } catch (error) {
    console.error('Erro no teste completo USB:', error);
    res.status(500).json({
      success: false,
      error: error.message,
      timestamp: new Date().toISOString()
    });
  }
});

// Enviar comando ZPL via USB
app.post('/api/usb/send-zpl', async (req, res) => {
  try {
    const { zplCommand } = req.body;
    
    if (!zplCommand) {
      return res.status(400).json({
        success: false,
        error: 'Comando ZPL é obrigatório',
        timestamp: new Date().toISOString()
      });
    }
    
    console.log('📤 Enviando comando ZPL via USB...');
    
    await zebraUSBConnection.connect();
    await zebraUSBConnection.sendZPL(zplCommand);
    await zebraUSBConnection.disconnect();
    
    res.json({
      success: true,
      message: 'Comando ZPL enviado com sucesso',
      timestamp: new Date().toISOString()
    });
  } catch (error) {
    console.error('Erro ao enviar ZPL via USB:', error);
    res.status(500).json({
      success: false,
      error: error.message,
      timestamp: new Date().toISOString()
    });
  }
});

// ========================================
// ENDPOINTS PARA INTEGRAÇÃO PYTHON
// ========================================

// Status do serviço Python
app.get('/api/python/status', (req, res) => {
  res.json({ 
    status: 'online',
    service: 'Python Zebra Integration Service',
    version: '1.0.0',
    timestamp: new Date().toISOString()
  });
});

// Detectar impressoras via Python
app.post('/api/python/detect', async (req, res) => {
  try {
    console.log('🔍 Detectando impressoras via Python...');
    
    const result = await pythonZebraIntegration.detectPrinters();
    
    res.json({
      success: true,
      result: result,
      timestamp: new Date().toISOString()
    });
  } catch (error) {
    console.error('Erro na detecção Python:', error);
    res.status(500).json({
      success: false,
      error: error.message,
      timestamp: new Date().toISOString()
    });
  }
});

// Conectar via Python
app.post('/api/python/connect', async (req, res) => {
  try {
    const { printerName } = req.body;
    console.log('🔌 Conectando via Python...');
    
    const result = await pythonZebraIntegration.connect(printerName);
    
    res.json({
      success: true,
      result: result,
      timestamp: new Date().toISOString()
    });
  } catch (error) {
    console.error('Erro na conexão Python:', error);
    res.status(500).json({
      success: false,
      error: error.message,
      timestamp: new Date().toISOString()
    });
  }
});

// Teste completo via Python
app.post('/api/python/full-test', async (req, res) => {
  try {
    console.log('🧪 Executando teste completo via Python...');
    
    const result = await pythonZebraIntegration.fullTest();
    
    res.json({
      success: true,
      result: result,
      timestamp: new Date().toISOString()
    });
  } catch (error) {
    console.error('Erro no teste completo Python:', error);
    res.status(500).json({
      success: false,
      error: error.message,
      timestamp: new Date().toISOString()
    });
  }
});

// Enviar ZPL via Python
app.post('/api/python/send-zpl', async (req, res) => {
  try {
    const { zplCommand } = req.body;
    
    if (!zplCommand) {
      return res.status(400).json({
        success: false,
        error: 'Comando ZPL é obrigatório',
        timestamp: new Date().toISOString()
      });
    }
    
    console.log('📤 Enviando ZPL via Python...');
    
    const result = await pythonZebraIntegration.sendZPL(zplCommand);
    
    res.json({
      success: true,
      result: result,
      timestamp: new Date().toISOString()
    });
  } catch (error) {
    console.error('Erro ao enviar ZPL via Python:', error);
    res.status(500).json({
      success: false,
      error: error.message,
      timestamp: new Date().toISOString()
    });
  }
});

// Testar conectividade via Python
app.post('/api/python/test', async (req, res) => {
  try {
    console.log('🧪 Testando conectividade via Python...');
    
    const result = await pythonZebraIntegration.testConnection();
    
    res.json({
      success: true,
      result: result,
      timestamp: new Date().toISOString()
    });
  } catch (error) {
    console.error('Erro no teste Python:', error);
    res.status(500).json({
      success: false,
      error: error.message,
      timestamp: new Date().toISOString()
    });
  }
});

// Desconectar via Python
app.post('/api/python/disconnect', async (req, res) => {
  try {
    console.log('🔌 Desconectando via Python...');
    
    const result = await pythonZebraIntegration.disconnect();
    
    res.json({
      success: true,
      result: result,
      timestamp: new Date().toISOString()
    });
  } catch (error) {
    console.error('Erro na desconexão Python:', error);
    res.status(500).json({
      success: false,
      error: error.message,
      timestamp: new Date().toISOString()
    });
  }
});

// Obter status da conexão Python
app.get('/api/python/connection-status', (req, res) => {
  try {
    const status = pythonZebraIntegration.getStatus();
    
    res.json({
      success: true,
      status: status,
      timestamp: new Date().toISOString()
    });
  } catch (error) {
    console.error('Erro ao obter status Python:', error);
    res.status(500).json({
      success: false,
      error: error.message,
      timestamp: new Date().toISOString()
    });
  }
});

// ========================================
// ENDPOINTS PARA PYTHON USB INTEGRATION
// ========================================

// Status do serviço Python USB
app.get('/api/python-usb/status', (req, res) => {
  res.json({ 
    status: 'online',
    service: 'Python USB Integration Service',
    version: '1.0.0',
    timestamp: new Date().toISOString()
  });
});

// Listar impressoras via Python USB
app.post('/api/python-usb/list', async (req, res) => {
  try {
    console.log('🔍 Listando impressoras via Python USB...');
    
    const result = await pythonUSBIntegration.listPrinters();
    
    res.json({
      success: true,
      result: result,
      timestamp: new Date().toISOString()
    });
  } catch (error) {
    console.error('Erro ao listar impressoras Python USB:', error);
    res.status(500).json({
      success: false,
      error: error.message,
      timestamp: new Date().toISOString()
    });
  }
});

// Testar conexão via Python USB
app.post('/api/python-usb/test', async (req, res) => {
  try {
    console.log('🧪 Testando conexão Python USB...');
    
    const result = await pythonUSBIntegration.testConnection();
    
    res.json({
      success: true,
      result: result,
      timestamp: new Date().toISOString()
    });
  } catch (error) {
    console.error('Erro no teste Python USB:', error);
    res.status(500).json({
      success: false,
      error: error.message,
      timestamp: new Date().toISOString()
    });
  }
});

// Enviar ZPL via Python USB
app.post('/api/python-usb/send-zpl', async (req, res) => {
  try {
    const { zplCommand } = req.body;
    
    if (!zplCommand) {
      return res.status(400).json({
        success: false,
        error: 'Comando ZPL é obrigatório',
        timestamp: new Date().toISOString()
      });
    }
    
    console.log('📤 Enviando ZPL via Python USB...');
    
    const result = await pythonUSBIntegration.sendZPL(zplCommand);
    
    res.json({
      success: true,
      result: result,
      timestamp: new Date().toISOString()
    });
  } catch (error) {
    console.error('Erro ao enviar ZPL Python USB:', error);
    res.status(500).json({
      success: false,
      error: error.message,
      timestamp: new Date().toISOString()
    });
  }
});

// Teste completo via Python USB
app.post('/api/python-usb/full-test', async (req, res) => {
  try {
    console.log('🚀 Executando teste completo Python USB...');
    
    const result = await pythonUSBIntegration.fullTest();
    
    res.json({
      success: true,
      result: result,
      timestamp: new Date().toISOString()
    });
  } catch (error) {
    console.error('Erro no teste completo Python USB:', error);
    res.status(500).json({
      success: false,
      error: error.message,
      timestamp: new Date().toISOString()
    });
  }
});

// Obter status da integração Python USB
app.get('/api/python-usb/info', (req, res) => {
  try {
    const status = pythonUSBIntegration.getStatus();
    
    res.json({
      success: true,
      status: status,
      timestamp: new Date().toISOString()
    });
  } catch (error) {
    console.error('Erro ao obter status Python USB:', error);
    res.status(500).json({
      success: false,
      error: error.message,
      timestamp: new Date().toISOString()
    });
  }
});

// ===== ENDPOINTS USB =====

// Status do serviço USB
app.get('/api/usb/status', (req, res) => {
  res.json({ 
    status: 'online',
    service: 'USB Printer Connection Service',
    version: '1.0.0',
    timestamp: new Date().toISOString()
  });
});

// Listar portas seriais disponíveis
app.get('/api/usb/ports', async (req, res) => {
  try {
    console.log('🔍 Listando portas seriais...');
    const { allPorts, printerPorts } = await usbConnection.listPorts();
    
    res.json({
      success: true,
      allPorts: allPorts,
      printerPorts: printerPorts,
      count: allPorts.length,
      printerCount: printerPorts.length,
      timestamp: new Date().toISOString()
    });
  } catch (error) {
    console.error('Erro ao listar portas:', error);
    res.status(500).json({
      success: false,
      error: error.message,
      timestamp: new Date().toISOString()
    });
  }
});

// Conectar à impressora via USB
app.post('/api/usb/connect', async (req, res) => {
  try {
    const { portPath, options = {} } = req.body;
    
    if (!portPath) {
      return res.status(400).json({
        success: false,
        error: 'Caminho da porta é obrigatório',
        timestamp: new Date().toISOString()
      });
    }
    
    console.log(`🔌 Conectando à porta USB ${portPath}...`);
    await usbConnection.connect(portPath, options);
    
    res.json({
      success: true,
      message: 'Conectado à impressora USB',
      connectionInfo: usbConnection.getConnectionInfo(),
      timestamp: new Date().toISOString()
    });
  } catch (error) {
    console.error('Erro na conexão USB:', error);
    res.status(500).json({
      success: false,
      error: error.message,
      timestamp: new Date().toISOString()
    });
  }
});

// Auto-conectar à impressora
app.post('/api/usb/auto-connect', async (req, res) => {
  try {
    console.log('🔍 Auto-detectando impressora USB...');
    const result = await usbConnection.autoConnect();
    
    res.json({
      success: true,
      result: result,
      connectionInfo: usbConnection.getConnectionInfo(),
      timestamp: new Date().toISOString()
    });
  } catch (error) {
    console.error('Erro na auto-conexão USB:', error);
    res.status(500).json({
      success: false,
      error: error.message,
      timestamp: new Date().toISOString()
    });
  }
});

// Desconectar da impressora
app.post('/api/usb/disconnect', async (req, res) => {
  try {
    await usbConnection.disconnect();
    
    res.json({
      success: true,
      message: 'Desconectado da impressora USB',
      timestamp: new Date().toISOString()
    });
  } catch (error) {
    console.error('Erro ao desconectar USB:', error);
    res.status(500).json({
      success: false,
      error: error.message,
      timestamp: new Date().toISOString()
    });
  }
});

// Testar conectividade USB
app.post('/api/usb/test', async (req, res) => {
  try {
    const { portPath } = req.body;
    
    if (portPath) {
      // Conectar à porta específica primeiro
      await usbConnection.connect(portPath);
    }
    
    console.log('🧪 Testando conectividade USB...');
    const testResult = await usbConnection.testConnection();
    
    res.json({
      success: true,
      result: testResult,
      timestamp: new Date().toISOString()
    });
  } catch (error) {
    console.error('Erro no teste USB:', error);
    res.status(500).json({
      success: false,
      error: error.message,
      timestamp: new Date().toISOString()
    });
  }
});

// Enviar comando ZPL via USB
app.post('/api/usb/send-zpl', async (req, res) => {
  try {
    const { zplCommand, portPath } = req.body;
    
    if (!zplCommand) {
      return res.status(400).json({
        success: false,
        error: 'Comando ZPL é obrigatório',
        timestamp: new Date().toISOString()
      });
    }
    
    // Se não estiver conectado, tentar conectar
    if (!usbConnection.isConnected && portPath) {
      await usbConnection.connect(portPath);
    }
    
    console.log('📤 Enviando comando ZPL via USB...');
    await usbConnection.sendZPL(zplCommand);
    
    res.json({
      success: true,
      message: 'Comando ZPL enviado com sucesso',
      timestamp: new Date().toISOString()
    });
  } catch (error) {
    console.error('Erro ao enviar ZPL via USB:', error);
    res.status(500).json({
      success: false,
      error: error.message,
      timestamp: new Date().toISOString()
    });
  }
});

// ========================================
// ROTA UNIFICADA PARA ENVIO DIRETO DE ZPL
// ========================================

// Enviar ZPL direto para impressora (rota unificada)
app.post('/api/send-zpl-direct', async (req, res) => {
  try {
    const { 
      zplCommand, 
      method = 'python-usb', // Padrão: python-usb (mais confiável)
      copies = 1,
      encoding = 'utf-8',
      portPath = null,
      validateZPL = true
    } = req.body;
    
    // Validação básica
    if (!zplCommand) {
      return res.status(400).json({
        success: false,
        error: 'Comando ZPL é obrigatório',
        timestamp: new Date().toISOString()
      });
    }

    // Validação do ZPL se solicitada (COM PREVENÇÃO DE VOID)
    if (validateZPL) {
      if (!zplCommand.startsWith('^XA') || !zplCommand.includes('^XZ')) {
        return res.status(400).json({
          success: false,
          error: 'Comando ZPL inválido: deve começar com ^XA e terminar com ^XZ',
          example: '^XA\n^FO50,50^A0N,30,30^FDTeste^FS\n^XZ',
          timestamp: new Date().toISOString()
        });
      }

      // VERIFICAÇÃO CRÍTICA: Detectar comandos perigosos
      const dangerousCommands = ['^RFW', '^RFR', '^RFI', '^RFT', '^RFU'];
      const foundDangerous = dangerousCommands.filter(cmd => zplCommand.includes(cmd));
      
      if (foundDangerous.length > 0) {
        console.log(`🚨 BLOQUEADO: Comandos perigosos detectados: ${foundDangerous.join(', ')}`);
        return res.status(400).json({
          success: false,
          error: 'COMANDOS RFID BLOQUEADOS - RISCO DE VOID!',
          dangerousCommands: foundDangerous,
          message: 'Para sua segurança, comandos RFID foram bloqueados para evitar VOID',
          suggestion: 'Use apenas comandos de impressão visual (texto, código de barras, QR code)',
          safeExample: '^XA\n^FO50,50^A0N,30,30^FDTeste Seguro^FS\n^FO50,80^BCN,60,Y,N,N\n^FD123456^FS\n^XZ',
          timestamp: new Date().toISOString()
        });
      }
    }

    console.log(`📤 Enviando ZPL direto para impressora via ${method}...`);
    console.log(`📋 Comando ZPL (${zplCommand.length} chars):`);
    console.log(zplCommand.substring(0, 200) + (zplCommand.length > 200 ? '...' : ''));
    
    let result;
    let methodUsed = method;

    // Tentar diferentes métodos de envio
    try {
      switch (method) {
        case 'python-usb':
          console.log('🐍 Usando Python USB (recomendado)');
          result = await pythonUSBIntegration.sendZPL(zplCommand, encoding, copies);
          break;
          
        case 'python':
          console.log('🐍 Usando Python padrão');
          result = await pythonZebraIntegration.sendZPL(zplCommand);
          break;
          
        case 'usb-direct':
          console.log('🔌 Usando conexão USB direta');
          if (portPath) {
            if (!usbConnection.isConnected) {
              await usbConnection.connect(portPath);
            }
          }
          await usbConnection.sendZPL(zplCommand);
          result = { success: true, message: 'Enviado via USB direto' };
          break;
          
        case 'zebra-usb':
          console.log('🦓 Usando Zebra USB');
          await zebraUSBConnection.connect();
          await zebraUSBConnection.sendZPL(zplCommand);
          await zebraUSBConnection.disconnect();
          result = { success: true, message: 'Enviado via Zebra USB' };
          break;
          
        default:
          throw new Error(`Método '${method}' não suportado. Use: python-usb, python, usb-direct, zebra-usb`);
      }
      
    } catch (primaryError) {
      console.warn(`⚠️ Método ${method} falhou: ${primaryError.message}`);
      
      // Fallback automático para python-usb se outro método falhar
      if (method !== 'python-usb') {
        console.log('🔄 Tentando fallback para python-usb...');
        try {
          result = await pythonUSBIntegration.sendZPL(zplCommand, encoding, copies);
          methodUsed = 'python-usb (fallback)';
          console.log('✅ Fallback bem-sucedido!');
        } catch (fallbackError) {
          throw new Error(`Método ${method} falhou: ${primaryError.message}. Fallback também falhou: ${fallbackError.message}`);
        }
      } else {
        throw primaryError;
      }
    }

    console.log(`✅ ZPL enviado com sucesso via ${methodUsed}`);
    
    res.json({
      success: true,
      message: 'ZPL enviado para impressora com sucesso',
      method: methodUsed,
      zplLength: zplCommand.length,
      copies: copies,
      result: result,
      timestamp: new Date().toISOString()
    });
    
  } catch (error) {
    console.error('❌ Erro ao enviar ZPL direto:', error);
    res.status(500).json({
      success: false,
      error: error.message,
      method: req.body.method || 'python-usb',
      timestamp: new Date().toISOString(),
      troubleshooting: {
        checkPrinter: 'Verifique se a impressora está conectada e ligada',
        checkUSB: 'Confirme se o cabo USB está conectado',
        checkDrivers: 'Verifique se os drivers da impressora estão instalados',
        tryDifferentMethod: 'Tente um método diferente (python-usb, python, usb-direct, zebra-usb)'
      }
    });
  }
});

// Validar comando ZPL com prevenção de VOID
app.post('/api/validate-zpl', (req, res) => {
  try {
    const { zplCommand, allowRFID = false } = req.body;
    
    if (!zplCommand) {
      return res.status(400).json({
        success: false,
        error: 'Comando ZPL é obrigatório'
      });
    }

    const validation = {
      hasStart: zplCommand.includes('^XA'),
      hasEnd: zplCommand.includes('^XZ'),
      length: zplCommand.length,
      lines: zplCommand.split('\n').length,
      commands: [],
      dangerousCommands: [],
      safetyLevel: 'UNKNOWN',
      voidRisk: 'LOW'
    };

    // Comandos perigosos que podem causar VOID
    const dangerousCommands = ['^RFW', '^RFR', '^RFI', '^RFT', '^RFU'];
    
    // Extrair comandos ZPL
    const zplCommands = zplCommand.match(/\^[A-Z]{1,3}[^A-Z^]*/g) || [];
    validation.commands = zplCommands.map(cmd => cmd.substring(0, 10));

    // Verificar comandos perigosos
    validation.dangerousCommands = validation.commands.filter(cmd => 
      dangerousCommands.some(dangerous => cmd.startsWith(dangerous))
    );

    // Determinar nível de segurança
    if (validation.dangerousCommands.length > 0) {
      validation.safetyLevel = 'DANGEROUS';
      validation.voidRisk = 'HIGH';
      
      if (!allowRFID) {
        validation.isValid = false;
        validation.errors = validation.errors || [];
        validation.errors.push('COMANDOS RFID DETECTADOS - RISCO DE VOID!');
        validation.errors.push(`Comandos perigosos: ${validation.dangerousCommands.join(', ')}`);
        validation.errors.push('Use allowRFID=true apenas se tiver certeza absoluta');
      }
    } else {
      validation.safetyLevel = 'SAFE';
      validation.voidRisk = 'NONE';
    }

    // Validação básica
    validation.isValid = validation.hasStart && validation.hasEnd && (allowRFID || validation.dangerousCommands.length === 0);
    
    if (!validation.isValid) {
      validation.errors = validation.errors || [];
      if (!validation.hasStart) validation.errors.push('Comando deve começar com ^XA');
      if (!validation.hasEnd) validation.errors.push('Comando deve terminar com ^XZ');
    }

    const riskLevel = validation.voidRisk === 'HIGH' ? '🚨 ALTO RISCO' : 
                     validation.voidRisk === 'LOW' ? '⚠️ BAIXO RISCO' : '✅ SEM RISCO';
    
    console.log(`🔍 Validação ZPL: ${validation.isValid ? 'VÁLIDO' : 'INVÁLIDO'}`);
    console.log(`🛡️ Nível de Segurança: ${validation.safetyLevel}`);
    console.log(`⚠️ Risco de VOID: ${riskLevel}`);
    
    if (validation.dangerousCommands.length > 0) {
      console.log(`🚫 Comandos perigosos detectados: ${validation.dangerousCommands.join(', ')}`);
    }
    
    res.json({
      success: true,
      validation: validation,
      timestamp: new Date().toISOString()
    });
    
  } catch (error) {
    console.error('Erro na validação ZPL:', error);
    res.status(500).json({
      success: false,
      error: error.message,
      timestamp: new Date().toISOString()
    });
  }
});

// Obter exemplos de comandos ZPL
app.get('/api/zpl-examples', (req, res) => {
  const examples = {
    basic: {
      name: 'Texto Simples SEGURO',
      description: 'Imprime texto simples - SEM RISCO DE VOID',
      zpl: '^XA\n^FO50,50^A0N,30,30^FDTeste Seguro^FS\n^FO50,80^A0N,20,20^FDSem comandos RFID^FS\n^XZ',
      safety: 'SAFE'
    },
    barcode: {
      name: 'Código de Barras SEGURO',
      description: 'Código de barras Code 128 - SEM RISCO DE VOID',
      zpl: '^XA\n^FO50,50^BY2\n^BCN,80,Y,N,N\n^FD123456789012^FS\n^FO50,150^A0N,20,20^FDCódigo: 123456789012^FS\n^XZ',
      safety: 'SAFE'
    },
    qrcode: {
      name: 'QR Code SEGURO',
      description: 'QR Code com dados - SEM RISCO DE VOID',
      zpl: '^XA\n^FO50,50^BQN,2,4\n^FDMM,A789643610064|0464|001^FS\n^FO200,50^A0N,18,18^FDQR Code^FS\n^FO200,80^A0N,16,16^FDDados: 789643610064^FS\n^XZ',
      safety: 'SAFE'
    },
    complete: {
      name: 'Etiqueta Completa SEGURA',
      description: 'Etiqueta visual completa - SEM COMANDOS RFID',
      zpl: '^XA\n^CI28\n^FO50,30^A0N,25,25^FDProduto: Tênis Esportivo^FS\n^FO50,60^A0N,20,20^FDPO: 0464 | SEQ: 001^FS\n^FO50,90^A0N,18,18^FDCor: BLUE | Tam: 42^FS\n^FO50,120^BY2\n^BCN,60,Y,N,N\n^FD789643610064^FS\n^FO200,120^BQN,2,3\n^FDMM,A789643610064|0464|001^FS\n^FO50,200^A0N,16,16^FDLARROUD - SEM RFID^FS\n^XZ',
      safety: 'SAFE'
    },
    emergency: {
      name: 'PARADA DE EMERGÊNCIA',
      description: 'Cancela jobs e limpa buffer da impressora',
      zpl: '^XA\n^FX === PARADA DE EMERGÊNCIA ===\n~JA\n^JUS\n^FO50,50^A0N,25,25^FDEMERGÊNCIA EXECUTADA^FS\n^FO50,80^A0N,20,20^FDJobs cancelados^FS\n^FO50,110^A0N,20,20^FDBuffer limpo^FS\n^XZ',
      safety: 'EMERGENCY'
    }
  };

  res.json({
    success: true,
    examples: examples,
    usage: 'Use POST /api/send-zpl-direct com o campo zplCommand',
    timestamp: new Date().toISOString()
  });
});

// ========================================
// INTERFACE WEB PARA TESTE DE ZPL
// ========================================

// Página de teste ZPL
app.get('/zpl-tester', (req, res) => {
  const htmlPage = `
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ZPL Tester - Sistema Larroud RFID</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { 
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: #f8fafc; 
            color: #1f2937;
            line-height: 1.6;
        }
        .container { 
            max-width: 1200px; 
            margin: 0 auto; 
            padding: 20px; 
        }
        .header {
            background: linear-gradient(135deg, #3b82f6, #1e40af);
            color: white;
            padding: 24px;
            border-radius: 12px;
            margin-bottom: 24px;
            text-align: center;
        }
        .header h1 { font-size: 28px; margin-bottom: 8px; }
        .header p { opacity: 0.9; }
        
        .main-content {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 24px;
        }
        
        .zpl-panel {
            background: white;
            border-radius: 12px;
            padding: 24px;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
        }
        
        .panel-title {
            font-size: 18px;
            font-weight: 600;
            margin-bottom: 16px;
            color: #374151;
            display: flex;
            align-items: center;
            gap: 8px;
        }
        
        .zpl-textarea {
            width: 100%;
            height: 300px;
            font-family: 'Courier New', monospace;
            font-size: 14px;
            border: 2px solid #e5e7eb;
            border-radius: 8px;
            padding: 12px;
            resize: vertical;
            background: #f9fafb;
        }
        
        .zpl-textarea:focus {
            outline: none;
            border-color: #3b82f6;
            background: white;
        }
        
        .examples-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 12px;
            margin-bottom: 16px;
        }
        
        .example-btn {
            background: #f3f4f6;
            border: 1px solid #d1d5db;
            border-radius: 8px;
            padding: 12px;
            cursor: pointer;
            transition: all 0.2s ease;
            text-align: left;
        }
        
        .example-btn:hover {
            background: #e5e7eb;
            border-color: #3b82f6;
        }
        
        .example-btn.active {
            background: #dbeafe;
            border-color: #3b82f6;
            color: #1e40af;
        }
        
        .example-title {
            font-weight: 600;
            font-size: 14px;
            margin-bottom: 4px;
        }
        
        .example-desc {
            font-size: 12px;
            color: #6b7280;
        }
        
        .controls {
            display: flex;
            gap: 12px;
            margin-top: 16px;
            flex-wrap: wrap;
        }
        
        .btn {
            padding: 10px 16px;
            border: none;
            border-radius: 8px;
            font-size: 14px;
            font-weight: 500;
            cursor: pointer;
            transition: all 0.2s ease;
            display: flex;
            align-items: center;
            gap: 6px;
        }
        
        .btn-primary {
            background: #3b82f6;
            color: white;
        }
        
        .btn-primary:hover {
            background: #2563eb;
        }
        
        .btn-secondary {
            background: #6b7280;
            color: white;
        }
        
        .btn-secondary:hover {
            background: #4b5563;
        }
        
        .btn-success {
            background: #10b981;
            color: white;
        }
        
        .btn-success:hover {
            background: #059669;
        }
        
        .btn:disabled {
            background: #d1d5db;
            color: #9ca3af;
            cursor: not-allowed;
        }
        
        .method-select {
            padding: 8px 12px;
            border: 2px solid #e5e7eb;
            border-radius: 6px;
            font-size: 14px;
            background: white;
        }
        
        .result-panel {
            grid-column: 1 / -1;
            background: white;
            border-radius: 12px;
            padding: 24px;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
            margin-top: 24px;
        }
        
        .result-content {
            background: #1f2937;
            color: #e5e7eb;
            padding: 16px;
            border-radius: 8px;
            font-family: 'Courier New', monospace;
            font-size: 14px;
            white-space: pre-wrap;
            max-height: 400px;
            overflow-y: auto;
        }
        
        .status-indicator {
            display: inline-block;
            padding: 4px 8px;
            border-radius: 4px;
            font-size: 12px;
            font-weight: 600;
            margin-left: 8px;
        }
        
        .status-success {
            background: #dcfce7;
            color: #166534;
        }
        
        .status-error {
            background: #fee2e2;
            color: #dc2626;
        }
        
        .status-warning {
            background: #fef3c7;
            color: #d97706;
        }
        
        .spinner {
            display: inline-block;
            width: 16px;
            height: 16px;
            border: 2px solid rgba(255, 255, 255, 0.3);
            border-top: 2px solid white;
            border-radius: 50%;
            animation: spin 1s linear infinite;
        }
        
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
        
        @media (max-width: 768px) {
            .main-content {
                grid-template-columns: 1fr;
            }
            
            .examples-grid {
                grid-template-columns: 1fr;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🧪 ZPL Tester</h1>
            <p>Sistema Larroud RFID - Teste comandos ZPL diretamente na impressora</p>
        </div>
        
        <div class="main-content">
            <div class="zpl-panel">
                <h2 class="panel-title">📋 Exemplos ZPL</h2>
                
                <div class="examples-grid" id="examples-grid">
                    <!-- Exemplos serão carregados aqui -->
                </div>
                
                <div class="controls">
                    <button class="btn btn-secondary" onclick="loadExamples()">
                        🔄 Recarregar Exemplos
                    </button>
                    <button class="btn btn-secondary" onclick="clearEditor()">
                        🗑️ Limpar Editor
                    </button>
                </div>
            </div>
            
            <div class="zpl-panel">
                <h2 class="panel-title">✏️ Editor ZPL</h2>
                
                <textarea 
                    id="zpl-editor" 
                    class="zpl-textarea" 
                    placeholder="Cole seu comando ZPL aqui ou selecione um exemplo...&#10;&#10;Exemplo:&#10;^XA&#10;^FO50,50^A0N,30,30^FDHello World^FS&#10;^XZ"
                ></textarea>
                
                <div class="controls">
                    <select id="method-select" class="method-select">
                        <option value="python-usb">🐍 Python USB (Recomendado)</option>
                        <option value="python">🐍 Python Padrão</option>
                        <option value="usb-direct">🔌 USB Direto</option>
                        <option value="zebra-usb">🦓 Zebra USB</option>
                    </select>
                    
                    <button class="btn btn-primary" onclick="validateZPL()" id="validate-btn">
                        🔍 Validar ZPL
                    </button>
                    
                    <button class="btn btn-success" onclick="sendZPL()" id="send-btn">
                        📤 Enviar para Impressora
                    </button>
                </div>
            </div>
        </div>
        
        <div class="result-panel" id="result-panel" style="display: none;">
            <h2 class="panel-title">
                📊 Resultado
                <span id="status-indicator" class="status-indicator"></span>
            </h2>
            <div class="result-content" id="result-content"></div>
        </div>
    </div>

    <script>
        let examples = {};
        
        // Carregar exemplos
        async function loadExamples() {
            try {
                const response = await fetch('/api/zpl-examples');
                const data = await response.json();
                examples = data.examples;
                renderExamples();
            } catch (error) {
                showResult('Erro ao carregar exemplos: ' + error.message, 'error');
            }
        }
        
        // Renderizar exemplos
        function renderExamples() {
            const grid = document.getElementById('examples-grid');
            grid.innerHTML = '';
            
            Object.keys(examples).forEach(key => {
                const example = examples[key];
                const btn = document.createElement('div');
                btn.className = 'example-btn';
                btn.onclick = () => selectExample(key, btn);
                btn.innerHTML = \`
                    <div class="example-title">\${example.name}</div>
                    <div class="example-desc">\${example.description}</div>
                \`;
                grid.appendChild(btn);
            });
        }
        
        // Selecionar exemplo
        function selectExample(key, btnElement) {
            // Remover seleção anterior
            document.querySelectorAll('.example-btn').forEach(btn => 
                btn.classList.remove('active')
            );
            
            // Marcar como ativo
            btnElement.classList.add('active');
            
            // Carregar no editor
            document.getElementById('zpl-editor').value = examples[key].zpl;
        }
        
        // Limpar editor
        function clearEditor() {
            document.getElementById('zpl-editor').value = '';
            document.querySelectorAll('.example-btn').forEach(btn => 
                btn.classList.remove('active')
            );
        }
        
        // Validar ZPL
        async function validateZPL() {
            const zplCommand = document.getElementById('zpl-editor').value.trim();
            
            if (!zplCommand) {
                showResult('Por favor, insira um comando ZPL', 'warning');
                return;
            }
            
            const btn = document.getElementById('validate-btn');
            btn.disabled = true;
            btn.innerHTML = '<span class="spinner"></span> Validando...';
            
            try {
                const response = await fetch('/api/validate-zpl', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ zplCommand })
                });
                
                const data = await response.json();
                
                if (data.success) {
                    const validation = data.validation;
                    let result = \`✅ VALIDAÇÃO ZPL\\n\`;
                    result += \`═══════════════════\\n\`;
                    result += \`Status: \${validation.isValid ? 'VÁLIDO' : 'INVÁLIDO'}\\n\`;
                    result += \`Tamanho: \${validation.length} caracteres\\n\`;
                    result += \`Linhas: \${validation.lines}\\n\`;
                    result += \`Comandos: \${validation.commands.length}\\n\`;
                    
                    if (validation.commands.length > 0) {
                        result += \`\\nComandos encontrados:\\n\`;
                        result += validation.commands.slice(0, 10).join(', ');
                        if (validation.commands.length > 10) {
                            result += \` ... e mais \${validation.commands.length - 10}\`;
                        }
                    }
                    
                    if (!validation.isValid && validation.errors) {
                        result += \`\\n\\n❌ ERROS:\\n\`;
                        validation.errors.forEach(error => {
                            result += \`• \${error}\\n\`;
                        });
                    }
                    
                    showResult(result, validation.isValid ? 'success' : 'error');
                } else {
                    showResult('Erro na validação: ' + data.error, 'error');
                }
                
            } catch (error) {
                showResult('Erro na validação: ' + error.message, 'error');
            } finally {
                btn.disabled = false;
                btn.innerHTML = '🔍 Validar ZPL';
            }
        }
        
        // Enviar ZPL
        async function sendZPL() {
            const zplCommand = document.getElementById('zpl-editor').value.trim();
            const method = document.getElementById('method-select').value;
            
            if (!zplCommand) {
                showResult('Por favor, insira um comando ZPL', 'warning');
                return;
            }
            
            const btn = document.getElementById('send-btn');
            btn.disabled = true;
            btn.innerHTML = '<span class="spinner"></span> Enviando...';
            
            try {
                const response = await fetch('/api/send-zpl-direct', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ 
                        zplCommand, 
                        method, 
                        copies: 1,
                        validateZPL: true 
                    })
                });
                
                const data = await response.json();
                
                if (data.success) {
                    let result = \`✅ ZPL ENVIADO COM SUCESSO\\n\`;
                    result += \`═══════════════════════════\\n\`;
                    result += \`Método: \${data.method}\\n\`;
                    result += \`Tamanho: \${data.zplLength} chars\\n\`;
                    result += \`Cópias: \${data.copies}\\n\`;
                    result += \`Timestamp: \${new Date(data.timestamp).toLocaleString()}\\n\`;
                    
                    if (data.result && data.result.result) {
                        const printerResult = data.result.result;
                        result += \`\\n🖨️ INFORMAÇÕES DA IMPRESSORA:\\n\`;
                        result += \`Job ID: \${printerResult.job_id || 'N/A'}\\n\`;
                        result += \`Bytes enviados: \${printerResult.bytes_written || 'N/A'}\\n\`;
                        result += \`Jobs na fila: \${printerResult.jobs_in_queue || 'N/A'}\\n\`;
                        result += \`Status: \${printerResult.printer_status || 'N/A'}\\n\`;
                    }
                    
                    result += \`\\n🎯 Verifique se a etiqueta foi impressa!\\n\`;
                    
                    showResult(result, 'success');
                } else {
                    let result = \`❌ ERRO NO ENVIO\\n\`;
                    result += \`═══════════════════\\n\`;
                    result += \`Erro: \${data.error}\\n\`;
                    result += \`Método: \${data.method}\\n\`;
                    
                    if (data.troubleshooting) {
                        result += \`\\n🛠️ DICAS DE SOLUÇÃO:\\n\`;
                        Object.values(data.troubleshooting).forEach(tip => {
                            result += \`• \${tip}\\n\`;
                        });
                    }
                    
                    showResult(result, 'error');
                }
                
            } catch (error) {
                showResult('Erro na comunicação: ' + error.message, 'error');
            } finally {
                btn.disabled = false;
                btn.innerHTML = '📤 Enviar para Impressora';
            }
        }
        
        // Mostrar resultado
        function showResult(content, type) {
            const panel = document.getElementById('result-panel');
            const indicator = document.getElementById('status-indicator');
            const resultContent = document.getElementById('result-content');
            
            panel.style.display = 'block';
            resultContent.textContent = content;
            
            indicator.className = 'status-indicator status-' + type;
            indicator.textContent = {
                'success': 'SUCESSO',
                'error': 'ERRO',
                'warning': 'AVISO'
            }[type] || 'INFO';
            
            // Scroll para o resultado
            panel.scrollIntoView({ behavior: 'smooth' });
        }
        
        // Carregar exemplos ao inicializar
        loadExamples();
    </script>
</body>
</html>`;

  res.send(htmlPage);
});

// Rota para testar ZPL específico (API)
app.post('/api/test-zpl', async (req, res) => {
  try {
    const { 
      zplCommand, 
      testName = 'Teste Personalizado',
      description = 'ZPL enviado via API de teste',
      method = 'python-usb',
      copies = 1,
      analyze = true
    } = req.body;
    
    if (!zplCommand) {
      return res.status(400).json({
        success: false,
        error: 'Comando ZPL é obrigatório',
        timestamp: new Date().toISOString()
      });
    }

    console.log(`🧪 Teste ZPL: ${testName}`);
    console.log(`📋 Descrição: ${description}`);
    console.log(`📏 Tamanho: ${zplCommand.length} chars`);

    const results = {
      testInfo: {
        name: testName,
        description: description,
        timestamp: new Date().toISOString(),
        zplLength: zplCommand.length,
        method: method,
        copies: copies
      },
      validation: null,
      analysis: null,
      sendResult: null
    };

    // 1. Validar ZPL
    try {
      const validateResponse = await fetch(`http://localhost:${PORT}/api/validate-zpl`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ zplCommand })
      });
      
      if (validateResponse.ok) {
        const validateData = await validateResponse.json();
        results.validation = validateData.validation;
        console.log(`🔍 Validação: ${validateData.validation.isValid ? 'VÁLIDO' : 'INVÁLIDO'}`);
      }
    } catch (error) {
      console.warn('Erro na validação:', error.message);
    }

    // 2. Análise do conteúdo (se solicitada)
    if (analyze) {
      results.analysis = analyzeZPLContent(zplCommand);
      console.log(`🔍 Análise: ${Object.keys(results.analysis.elements).length} tipos de elementos`);
    }

    // 3. Enviar para impressora
    try {
      const sendResponse = await fetch(`http://localhost:${PORT}/api/send-zpl-direct`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ 
          zplCommand, 
          method, 
          copies,
          validateZPL: false // Já validamos acima
        })
      });
      
      const sendData = await sendResponse.json();
      results.sendResult = sendData;
      
      if (sendData.success) {
        console.log(`✅ ZPL enviado com sucesso via ${sendData.method}`);
      } else {
        console.log(`❌ Erro no envio: ${sendData.error}`);
      }
      
    } catch (error) {
      results.sendResult = {
        success: false,
        error: error.message
      };
      console.error('Erro no envio:', error.message);
    }

    // Determinar status geral
    const overallSuccess = results.sendResult && results.sendResult.success;
    const hasValidation = results.validation && results.validation.isValid;

    res.json({
      success: overallSuccess,
      message: overallSuccess ? 'ZPL testado e enviado com sucesso' : 'Teste completado com erros',
      results: results,
      summary: {
        validated: hasValidation,
        sent: overallSuccess,
        analyzed: analyze,
        elements: results.analysis ? Object.keys(results.analysis.elements).length : 0
      },
      timestamp: new Date().toISOString()
    });

  } catch (error) {
    console.error('Erro no teste ZPL:', error);
    res.status(500).json({
      success: false,
      error: error.message,
      timestamp: new Date().toISOString()
    });
  }
});

// Função auxiliar para análise de conteúdo ZPL
function analyzeZPLContent(zpl) {
  const lines = zpl.split('\\n');
  const analysis = {
    elements: {
      texts: [],
      barcodes: [],
      rfid: [],
      positioning: [],
      formatting: []
    },
    statistics: {
      totalLines: lines.length,
      commandLines: 0,
      commentLines: 0,
      emptyLines: 0
    }
  };

  lines.forEach(line => {
    const trimmed = line.trim();
    
    if (!trimmed) {
      analysis.statistics.emptyLines++;
      return;
    }
    
    if (trimmed.startsWith('^FX')) {
      analysis.statistics.commentLines++;
      return;
    }
    
    if (trimmed.startsWith('^')) {
      analysis.statistics.commandLines++;
    }

    // Analisar elementos específicos
    if (trimmed.includes('^FD') && !trimmed.includes('^BC')) {
      const content = trimmed.split('^FD')[1]?.split('^FS')[0] || '';
      if (content) {
        analysis.elements.texts.push(`Texto: ${content.substring(0, 50)}${content.length > 50 ? '...' : ''}`);
      }
    }
    
    if (trimmed.includes('^BC') || trimmed.includes('^BY')) {
      analysis.elements.barcodes.push('Código de barras detectado');
    }
    
    if (trimmed.includes('^RFW') || trimmed.includes('^RFR')) {
      analysis.elements.rfid.push('Comando RFID detectado');
    }
    
    if (trimmed.includes('^FO')) {
      const coords = trimmed.replace(/.*\\^FO/, '').split('^')[0];
      analysis.elements.positioning.push(`Posição: ${coords}`);
    }
    
    if (trimmed.includes('^CI') || trimmed.includes('^RS')) {
      analysis.elements.formatting.push(`Formatação: ${trimmed.substring(0, 20)}`);
    }
  });

  return analysis;
}

// Obter informações da conexão USB
app.get('/api/usb/info', (req, res) => {
  try {
    const connectionInfo = usbConnection.getConnectionInfo();
    
    res.json({
      success: true,
      connectionInfo: connectionInfo,
      timestamp: new Date().toISOString()
    });
  } catch (error) {
    console.error('Erro ao obter informações USB:', error);
    res.status(500).json({
      success: false,
      error: error.message,
      timestamp: new Date().toISOString()
    });
  }
});

// ========================================
// ENDPOINTS PARA INTEGRAÇÃO MUPA RFID
// ========================================

// Status do serviço MUPA
app.get('/api/mupa/status', (req, res) => {
  res.json({ 
    status: 'online',
    service: 'MUPA RFID Integration Service',
    version: '1.0.0',
    timestamp: new Date().toISOString()
  });
});

// Imprimir etiqueta
app.post('/api/mupa/print-label', async (req, res) => {
  try {
    const { text, additionalInfo = {} } = req.body;
    
    if (!text) {
      return res.status(400).json({
        success: false,
        error: 'Texto da etiqueta é obrigatório',
        timestamp: new Date().toISOString()
      });
    }
    
    console.log(`📄 Imprimindo etiqueta: ${text}`);
    
    const result = await mupaRFIDIntegration.printLabel(text, additionalInfo);
    
    res.json({
      success: true,
      result: result,
      timestamp: new Date().toISOString()
    });
  } catch (error) {
    console.error('Erro ao imprimir etiqueta:', error);
    res.status(500).json({
      success: false,
      error: error.message,
      timestamp: new Date().toISOString()
    });
  }
});

// Gravar dados no RFID
app.post('/api/mupa/write-rfid', async (req, res) => {
  try {
    const { data } = req.body;
    
    if (!data) {
      return res.status(400).json({
        success: false,
        error: 'Dados para gravação RFID são obrigatórios',
        timestamp: new Date().toISOString()
      });
    }
    
    console.log(`📄 Gravando RFID: ${data}`);
    
    const result = await mupaRFIDIntegration.writeRFID(data);
    
    res.json({
      success: true,
      result: result,
      timestamp: new Date().toISOString()
    });
  } catch (error) {
    console.error('Erro ao gravar RFID:', error);
    res.status(500).json({
      success: false,
      error: error.message,
      timestamp: new Date().toISOString()
    });
  }
});

// Imprimir etiqueta e gravar RFID em um único comando
app.post('/api/mupa/print-and-write', async (req, res) => {
  try {
    const { text, additionalInfo = {} } = req.body;
    
    if (!text) {
      return res.status(400).json({
        success: false,
        error: 'Texto para impressão e gravação RFID é obrigatório',
        timestamp: new Date().toISOString()
      });
    }
    
    console.log(`📄 Imprimindo e gravando RFID: ${text}`);
    
    const result = await mupaRFIDIntegration.printAndWriteRFID(text, additionalInfo);
    
    res.json({
      success: true,
      result: result,
      timestamp: new Date().toISOString()
    });
  } catch (error) {
    console.error('Erro ao imprimir e gravar RFID:', error);
    res.status(500).json({
      success: false,
      error: error.message,
      timestamp: new Date().toISOString()
    });
  }
});

// Ler dados do RFID
app.post('/api/mupa/read-rfid', async (req, res) => {
  try {
    console.log('📄 Lendo dados do RFID...');
    
    const result = await mupaRFIDIntegration.readRFID();
    
    res.json({
      success: true,
      result: result,
      timestamp: new Date().toISOString()
    });
  } catch (error) {
    console.error('Erro ao ler RFID:', error);
    res.status(500).json({
      success: false,
      error: error.message,
      timestamp: new Date().toISOString()
    });
  }
});

// Teste completo MUPA
app.post('/api/mupa/test', async (req, res) => {
  try {
    const { text = "MUPA_TESTE_01" } = req.body;
    
    console.log(`🧪 Executando teste completo MUPA: ${text}`);
    
    const result = await mupaRFIDIntegration.testMupa(text);
    
    res.json({
      success: true,
      result: result,
      timestamp: new Date().toISOString()
    });
  } catch (error) {
    console.error('Erro no teste MUPA:', error);
    res.status(500).json({
      success: false,
      error: error.message,
      timestamp: new Date().toISOString()
    });
  }
});

// Obter status da integração MUPA
app.get('/api/mupa/info', (req, res) => {
  try {
    const status = mupaRFIDIntegration.getStatus();
    
    res.json({
      success: true,
      status: status,
      timestamp: new Date().toISOString()
    });
  } catch (error) {
    console.error('Erro ao obter informações MUPA:', error);
    res.status(500).json({
      success: false,
      error: error.message,
      timestamp: new Date().toISOString()
    });
  }
});

// ========================================
// ENDPOINTS PARA PROCESSAMENTO CSV
// ========================================

// Importar módulo de processamento CSV
const CSVLabelProcessor = require('./csv-label-processor');
const csvLabelProcessor = new CSVLabelProcessor();

// Listar etiquetas do CSV
app.get('/api/csv/labels', (req, res) => {
  try {
    const info = csvLabelProcessor.getInfo();
    
    res.json({
      success: true,
      message: 'Etiquetas carregadas do CSV',
      data: info,
      timestamp: new Date().toISOString()
    });
  } catch (error) {
    console.error('❌ Erro ao carregar etiquetas CSV:', error);
    res.status(500).json({
      success: false,
      error: error.message,
      timestamp: new Date().toISOString()
    });
  }
});

// Imprimir etiqueta específica do CSV
app.post('/api/csv/print-label', async (req, res) => {
  try {
    const { labelIndex, rfidData } = req.body;
    
    if (!labelIndex) {
      return res.status(400).json({
        success: false,
        error: 'Índice da etiqueta é obrigatório',
        timestamp: new Date().toISOString()
      });
    }
    
    console.log(`🖨️ Imprimindo etiqueta ${labelIndex} do CSV...`);
    
    const result = await csvLabelProcessor.printSingleLabel(labelIndex, rfidData);
    
    res.json({
      success: true,
      message: 'Etiqueta enviada para impressão',
      data: result,
      timestamp: new Date().toISOString()
    });
  } catch (error) {
    console.error('❌ Erro ao imprimir etiqueta CSV:', error);
    res.status(500).json({
      success: false,
      error: error.message,
      timestamp: new Date().toISOString()
    });
  }
});

// Imprimir todas as etiquetas do CSV
app.post('/api/csv/print-all', async (req, res) => {
  try {
    const { rfidData } = req.body;
    
    console.log('🖨️ Imprimindo todas as etiquetas do CSV...');
    
    const result = await csvLabelProcessor.printAllLabels(rfidData);
    
    res.json({
      success: true,
      message: 'Todas as etiquetas enviadas para impressão',
      data: result,
      timestamp: new Date().toISOString()
    });
  } catch (error) {
    console.error('❌ Erro ao imprimir todas as etiquetas CSV:', error);
    res.status(500).json({
      success: false,
      error: error.message,
      timestamp: new Date().toISOString()
    });
  }
});

// Obter informações do processador CSV
app.get('/api/csv/info', (req, res) => {
  try {
    const info = csvLabelProcessor.getInfo();
    
    res.json({
      success: true,
      message: 'Informações do processador CSV',
      data: info,
      timestamp: new Date().toISOString()
    });
  } catch (error) {
    console.error('❌ Erro ao obter informações CSV:', error);
    res.status(500).json({
      success: false,
      error: error.message,
      timestamp: new Date().toISOString()
    });
  }
});

// Tratamento de erros
app.use((error, req, res, next) => {
  console.error('Erro:', error);
  res.status(500).json({ error: 'Erro interno do servidor' });
});

app.listen(PORT, () => {
  console.log(`Servidor rodando na porta ${PORT}`);
});

module.exports = app;