# Sistema de Geração de Etiquetas RFID - Larroudé

## Visão Geral do Projeto

Este é um sistema completo para geração de etiquetas RFID desenvolvido para a empresa Larroudé. O sistema permite o upload de arquivos CSV/Excel contendo dados de produtos e gera etiquetas personalizadas em formato ZPL (Zebra Programming Language) com códigos de barras e QR codes.

## Arquitetura do Sistema

### Stack Tecnológica

**Frontend:**
- React.js 18.x
- Axios para requisições HTTP
- Lucide React para ícones
- React Toastify para notificações
- CSS3 com design responsivo

**Backend:**
- Node.js com Express.js
- Multer para upload de arquivos
- XLSX para processamento de planilhas Excel
- CSV-Parser para arquivos CSV
- Sharp para processamento de imagens ZPL
- Canvas e JSBarcode para códigos de barras
- QRCode para geração de QR codes
- Node-ZPL para processamento de templates
- Archiver para compactação de arquivos
- CORS habilitado

### Estrutura de Diretórios

```
Larroudé-RFID/
├── frontend/                 # Aplicação React
│   ├── src/
│   │   ├── components/       # Componentes React
│   │   │   ├── FileUpload.js
│   │   │   ├── PreviewSection.js
│   │   │   ├── GenerateSection.js
│   │   │   └── components.css
│   │   ├── App.js
│   │   └── index.js
│   └── package.json
├── backend/                  # Servidor Node.js
│   ├── server.js            # Servidor principal
│   ├── LAYOUT_LABEL.ZPL     # Template ZPL
│   ├── uploads/             # Arquivos enviados
│   ├── output/              # Arquivos gerados
│   └── package.json
└── README.md
```

## Funcionalidades Principais

### 1. Upload e Processamento de Arquivos

**Formatos Suportados:**
- CSV (Comma Separated Values)
- XLSX (Excel)

**Campos Obrigatórios:**
- `STYLE NAME`: Nome do produto/estilo
- `VPN/VPM`: Código VPN/VPM do produto
- `COLOR`: Cor do produto
- `SIZE`: Tamanho do produto
- `Barcode`: Código de barras
- `REF`: Referência do produto
- `QTY`: Quantidade de etiquetas
- `QR1`: Primeiro QR code
- `QR2`: Segundo QR code
- `PO/Local`: Purchase Order/Local

**Validações Implementadas:**
- Verificação de campos obrigatórios
- Validação de formato de arquivo
- Sanitização de dados
- Verificação de duplicatas

### 2. Geração de Previews

**Tecnologia:**
- Sharp para processamento de imagens ZPL
- Canvas API para geração de códigos de barras
- QRCode para geração de QR codes
- SVG para renderização de layout

**Características:**
- Preview em tempo real das etiquetas
- Processamento ZPL com Field Numbers (^FN)
- Dimensões 4x2 polegadas (812x406 dots)
- Escape automático de caracteres XML
- Layout otimizado para impressoras Zebra

### 3. Geração de Etiquetas ZPL

**Template ZPL:**
- Layout personalizado para impressoras Zebra
- Sistema de Field Numbers (^FN) para campos dinâmicos
- Códigos de barras Code 128
- QR Codes duplos com dados do produto
- Dimensões 4x2 polegadas (812x406 dots)
- Moldura externa e cápsula PO/Local

**Processo de Geração:**
1. Leitura do template ZPL com ^FN
2. Processamento de Field Numbers
3. Geração de códigos de barras e QR codes
4. Escape de caracteres XML especiais
5. Criação de arquivo ZIP com todas as etiquetas

## Detalhes Técnicos

### Componentes Frontend

#### FileUpload.js
```javascript
// Responsável por:
- Upload de arquivos via drag & drop ou seleção
- Validação de formato de arquivo
- Exibição de preview dos dados
- Comunicação com backend via axios
```

#### PreviewSection.js
```javascript
// Funcionalidades:
- Geração de previews das etiquetas
- Modal para visualização ampliada
- Download individual de previews
- Grid responsivo de previews
- Event handlers para interação
```

#### GenerateSection.js
```javascript
// Características:
- Geração final das etiquetas ZPL
- Download do arquivo ZIP
- Indicadores de progresso
- Validação antes da geração
```

### Endpoints Backend

#### POST /api/upload
```javascript
// Funcionalidade: Upload e processamento de arquivos
// Input: FormData com arquivo CSV/XLSX
// Output: JSON com dados processados
// Validações: Formato, campos obrigatórios, estrutura
```

#### POST /api/generate-preview
```javascript
// Funcionalidade: Geração de previews das etiquetas
// Input: Dados dos produtos + quantidade de previews
// Output: Array de imagens base64
// Tecnologia: Puppeteer + Sharp
```

#### POST /api/generate-labels
```javascript
// Funcionalidade: Geração final das etiquetas ZPL
// Input: Dados completos dos produtos
// Output: Arquivo ZIP para download
// Processo: Template ZPL + substituição de variáveis
```

### Lógica de Processamento

#### Processamento de Dados
```javascript
1. Upload do arquivo
2. Detecção automática do formato (CSV/XLSX)
3. Parsing dos dados
4. Validação de campos obrigatórios
5. Sanitização e normalização
6. Retorno dos dados estruturados
```

#### Geração de Previews
```javascript
1. Recebimento dos dados do produto
2. Processamento do template ZPL com ^FN
3. Geração de SVG com layout da etiqueta
4. Conversão ZPL para PNG via Sharp
5. Escape de caracteres XML especiais
6. Retorno em base64
```

#### Geração de Etiquetas ZPL
```javascript
1. Leitura do template LAYOUT_LABEL.ZPL
2. Para cada produto:
   - Processamento de Field Numbers (^FN1-^FN10)
   - Mapeamento de campos: STYLE NAME, VPN/VPM, COLOR, SIZE, etc.
   - Geração de códigos de barras e QR codes
   - Escape de caracteres XML (&, <, >, ", ')
3. Criação de arquivo .zpl individual
4. Compactação em ZIP
5. Disponibilização para download
```

### Tratamento de Erros

**Frontend:**
- Try-catch em todas as requisições
- Notificações toast para feedback
- Estados de loading e erro
- Validação de formulários

**Backend:**
- Middleware de tratamento de erros
- Logs detalhados
- Validação de entrada
- Respostas HTTP padronizadas

### Segurança

**Medidas Implementadas:**
- Validação de tipos de arquivo
- Sanitização de dados de entrada
- Limitação de tamanho de upload
- CORS configurado
- Limpeza de arquivos temporários

## Fluxo de Uso

1. **Upload de Dados:**
   - Usuário faz upload de arquivo CSV/XLSX
   - Sistema valida e processa os dados
   - Exibe preview dos dados na interface

2. **Geração de Previews:**
   - Usuário seleciona quantidade de previews
   - Sistema gera imagens das etiquetas
   - Usuário pode visualizar em modal ampliado

3. **Geração Final:**
   - Usuário confirma geração de todas as etiquetas
   - Sistema cria arquivos ZPL
   - Download automático do ZIP

## Configurações e Variáveis

### Portas
- Frontend: http://localhost:3000
- Backend: http://localhost:3002

### Limites
- Tamanho máximo de arquivo: 10MB
- Formatos aceitos: .csv, .xlsx
- Máximo de previews: 20 etiquetas

### Template ZPL
O arquivo `LAYOUT_LABEL.ZPL` contém o layout base das etiquetas com Field Numbers:
- `^FN1`: STYLE NAME (Nome do produto)
- `^FN2`: VPN/VPM (Código VPN/VPM)
- `^FN3`: COLOR (Cor)
- `^FN4`: SIZE (Tamanho)
- `^FN5`: Barcode (Código de barras)
- `^FN6`: REF (Referência)
- `^FN7`: QR1 (Primeiro QR code)
- `^FN8`: QR2 (Segundo QR code)
- `^FN9`: PO/Local (Purchase Order/Local)
- `^FN10`: Ícone do produto

## Dependências Principais

### Frontend
```json
{
  "react": "^18.x",
  "axios": "^1.x",
  "lucide-react": "^0.x",
  "react-toastify": "^9.x"
}
```

### Backend
```json
{
  "express": "^4.x",
  "multer": "^1.x",
  "xlsx": "^0.x",
  "sharp": "^0.x",
  "canvas": "^2.x",
  "jsbarcode": "^3.x",
  "qrcode": "^1.x",
  "node-zpl": "^1.x",
  "archiver": "^6.x",
  "cors": "^2.x",
  "axios": "^1.x"
}
```

## Instalação e Execução

### Pré-requisitos
- Node.js 16+ (recomendado 18+)
- NPM ou Yarn
- Git (para clonagem do repositório)

### Dependências do Sistema

**Windows:**
```powershell
# Instalar Visual Studio Build Tools (para Canvas)
# Baixar de: https://visualstudio.microsoft.com/visual-cpp-build-tools/

# Ou via Chocolatey
choco install visualstudio2019buildtools
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt-get install build-essential libcairo2-dev libpango1.0-dev libjpeg-dev libgif-dev librsvg2-dev
```

**macOS:**
```bash
# Instalar Xcode Command Line Tools
xcode-select --install
```

### Instalação

```bash
# 1. Clonar o repositório
git clone <repository-url>
cd Larroudé-RFID

# 2. Instalar dependências do backend
cd backend
npm install

# 3. Instalar dependências do frontend
cd ../frontend
npm install
```

### Execução

**Método 1 - Terminais Separados:**
```bash
# Terminal 1 - Backend
cd backend
npm start
# Servidor rodando em http://localhost:3002

# Terminal 2 - Frontend
cd frontend
npm start
# Aplicação rodando em http://localhost:3000
```

**Método 2 - PowerShell (Windows):**
```powershell
# Iniciar backend
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd backend; npm start"

# Iniciar frontend
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd frontend; npm start"
```

### Verificação da Instalação

```bash
# Testar backend
curl http://localhost:3002/api/health

# Ou no navegador
# http://localhost:3000
```

## Considerações de Performance

- Processamento assíncrono de arquivos grandes
- Otimização de imagens com Sharp
- Limpeza automática de arquivos temporários
- Compressão de arquivos de saída
- Cache de previews quando possível
- Processamento ZPL nativo sem dependências externas

## Troubleshooting

### Problemas Comuns

**Erro "Dados inválidos" na API:**
- Verifique se todos os campos obrigatórios estão presentes
- Confirme que o formato do arquivo está correto (CSV/XLSX)
- Valide se os nomes das colunas correspondem exatamente aos esperados

**Falha na geração de previews:**
- Verifique se o servidor backend está rodando na porta 3002
- Confirme se não há caracteres especiais não tratados nos dados
- Verifique os logs do servidor para erros específicos

**Problemas de dependências:**
- Execute `npm install` novamente em ambos os diretórios
- Para problemas com Canvas: instale as dependências do sistema operacional
- Para Sharp: certifique-se de que a versão é compatível com seu Node.js

**Arquivos ZPL corrompidos:**
- Verifique se o template LAYOUT_LABEL.ZPL está íntegro
- Confirme se não há caracteres especiais não escapados
- Valide se os Field Numbers (^FN1-^FN10) estão corretos

### Logs e Debug

**Backend:**
```bash
# Verificar logs do servidor
tail -f backend/logs/server.log

# Executar em modo debug
DEBUG=* npm start
```

**Frontend:**
```bash
# Verificar console do navegador
# Abrir DevTools (F12) > Console

# Verificar requisições de rede
# DevTools > Network tab
```

## Melhorias Recentes Implementadas

### v2.0 - Sistema ZPL Aprimorado
- **Migração para Sharp**: Substituição do Puppeteer por Sharp para melhor performance
- **Sistema Field Numbers**: Implementação de ^FN para templates ZPL mais robustos
- **Escape XML**: Tratamento automático de caracteres especiais (&, <, >, ", ')
- **Layout Otimizado**: Dimensões 4x2 polegadas com posicionamento preciso
- **Duplos QR Codes**: Suporte a dois QR codes por etiqueta
- **Moldura e Cápsula**: Design visual aprimorado com moldura externa
- **Estabilidade**: Correção de dependências nativas e processamento mais confiável

## Melhorias Futuras

- Autenticação de usuários
- Histórico de gerações
- Templates personalizáveis via interface
- Integração com banco de dados
- API para integração com outros sistemas
- Suporte a mais formatos de arquivo
- Impressão direta via rede
- Editor visual de templates ZPL

Este sistema foi desenvolvido especificamente para atender às necessidades da Larroudé na geração automatizada de etiquetas RFID, proporcionando uma interface intuitiva e um processo eficiente de criação de etiquetas personalizadas.