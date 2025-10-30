const sharp = require('sharp');

/**
 * Processa código ZPL e converte para imagem PNG usando Sharp
 * @param {string} zplCode - Código ZPL para processar
 * @returns {Promise<string>} - Base64 da imagem PNG gerada
 */
async function processZPLToImage(zplCode) {
  try {
    console.log('Processando ZPL usando template definido pelo usuário...');
    
    // Extrair dados do ZPL (já processado com ^FD)
    const styleName = extractZPLField(zplCode, 1) || 'N/A';
    const vpn = extractZPLField(zplCode, 2) || 'N/A';
    const color = extractZPLField(zplCode, 3) || 'N/A';
    const size = extractZPLField(zplCode, 4) || 'N/A';
    const barcode = extractZPLField(zplCode, 5) || 'N/A';
    const poLocal = extractZPLField(zplCode, 6) || 'N/A';
    
    // Criar SVG baseado no layout ZPL definido pelo usuário
    const svg = createLabelSVG({
      styleName,
      vpn,
      color,
      size,
      barcode,
      poLocal
    });
    
    // Converter SVG para PNG usando Sharp
    const pngBuffer = await sharp(Buffer.from(svg))
      .png()
      .resize(812, 406)
      .toBuffer();
    
    const base64Image = pngBuffer.toString('base64');
    console.log('ZPL processado com sucesso usando template definido');
    
    return base64Image;
    
  } catch (error) {
    console.log('Erro ao processar ZPL:', error.message);
    throw error;
  }
}

/**
 * Extrai campo do ZPL baseado no ^FD (dados já processados)
 */
function extractZPLField(zplCode, fieldNumber) {
  // Mapear os campos baseado na ordem esperada
  const fieldPatterns = {
    1: /\^FDSTYLE NAME:\s*([^\^]+)\^FS/i,
    2: /\^FDVPN:\s*([^\^]+)\^FS/i,
    3: /\^FDCOLOR:\s*([^\^]+)\^FS/i,
    4: /\^FD([^\^]+)\^FS.*SIZE/i, // Campo SIZE (sem prefixo)
    5: /\^FD(\d+)\^FS.*BC/i, // Barcode (números)
    6: /\^FD(PO[^\^]+)\^FS/i // PO/Local
  };
  
  const pattern = fieldPatterns[fieldNumber];
  if (!pattern) return null;
  
  const match = zplCode.match(pattern);
  return match ? match[1].trim() : null;
}

/**
 * Cria SVG baseado no layout ZPL definido pelo usuário
 */
function createLabelSVG(data) {
  // Escapar caracteres especiais XML
  const escapeXML = (str) => {
    return str.replace(/&/g, '&amp;')
              .replace(/</g, '&lt;')
              .replace(/>/g, '&gt;')
              .replace(/"/g, '&quot;')
              .replace(/'/g, '&#39;');
  };

  return `<svg width="812" height="406" xmlns="http://www.w3.org/2000/svg">
    <!-- Fundo branco -->
    <rect width="812" height="406" fill="white"/>
    
    <!-- Moldura externa arredondada -->
    <rect x="12" y="12" width="788" height="382" fill="none" stroke="black" stroke-width="2" rx="24"/>
    
    <!-- Moldura interna -->
    <rect x="36" y="48" width="580" height="290" fill="none" stroke="black" stroke-width="2" rx="14"/>
    
    <!-- Ícone do produto (canto superior esquerdo) -->
    <rect x="60" y="86" width="80" height="80" fill="none" stroke="black" stroke-width="2" rx="8"/>
    <text x="100" y="135" text-anchor="middle" font-family="Arial" font-size="32" fill="black">👟</text>
    
    <!-- Divisor vertical entre ícone e textos -->
    <line x1="170" y1="66" x2="170" y2="306" stroke="black" stroke-width="2"/>
    
    <!-- Informações principais -->
    <text x="190" y="100" font-family="Arial" font-size="18" font-weight="bold" fill="black">${escapeXML(data.styleName)}</text>
    <text x="190" y="130" font-family="Arial" font-size="16" fill="black">VPN: ${escapeXML(data.vpn)}</text>
    <text x="190" y="160" font-family="Arial" font-size="16" fill="black">COLOR: ${escapeXML(data.color)}</text>
    
    <!-- SIZE em destaque -->
    <text x="190" y="190" font-family="Arial" font-size="16" fill="black">SIZE:</text>
    <text x="260" y="190" font-family="Arial" font-size="20" font-weight="bold" fill="black">${escapeXML(data.size)}</text>
    
    <!-- Código de barras -->
    <rect x="190" y="220" width="300" height="40" fill="white" stroke="black" stroke-width="1"/>
    <text x="340" y="245" text-anchor="middle" font-family="monospace" font-size="12" fill="black">${escapeXML(data.barcode)}</text>
    
    <!-- QR Code esquerdo -->
    <rect x="60" y="235" width="80" height="80" fill="white" stroke="black" stroke-width="2"/>
    <text x="100" y="280" text-anchor="middle" font-family="Arial" font-size="12" fill="black">QR</text>
    
    <!-- Coluna direita: QR TOP -->
    <rect x="654" y="60" width="80" height="80" fill="white" stroke="black" stroke-width="2"/>
    <text x="694" y="105" text-anchor="middle" font-family="Arial" font-size="12" fill="black">QR</text>
    
    <!-- Cápsula PO/Local -->
    <rect x="642" y="184" width="150" height="66" fill="none" stroke="black" stroke-width="2" rx="16"/>
    <text x="717" y="210" text-anchor="middle" font-family="Arial" font-size="14" font-weight="bold" fill="black">PO/Local</text>
    <text x="717" y="230" text-anchor="middle" font-family="Arial" font-size="12" fill="black">${escapeXML(data.poLocal)}</text>
    
    <!-- QR BOTTOM -->
    <rect x="654" y="285" width="80" height="80" fill="white" stroke="black" stroke-width="2"/>
    <text x="694" y="330" text-anchor="middle" font-family="Arial" font-size="12" fill="black">QR</text>
    
  </svg>`;
}

module.exports = {
  processZPLToImage
};
