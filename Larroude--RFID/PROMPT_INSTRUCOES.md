# Prompt de Instruções - Sistema de Geração de Etiquetas RFID Larroudé

## Contexto do Projeto

Você está trabalhando no **Sistema de Geração de Etiquetas RFID da Larroudé**, um sistema completo para upload de dados de produtos via CSV/Excel e geração automática de etiquetas RFID em formato ZPL com QR codes e códigos de barras.

## REGRA FUNDAMENTAL - SEMPRE CONSULTE OS ARQUIVOS

**🚨 IMPORTANTE: Antes de fazer QUALQUER modificação no código, você DEVE:**

1. **SEMPRE** consultar os arquivos existentes do projeto
2. **SEMPRE** verificar a estrutura atual do código
3. **SEMPRE** entender o contexto antes de implementar mudanças
4. **NUNCA** assumir a estrutura do código sem verificar
5. **NUNCA** criar código que conflite com o existente

## Estrutura do Projeto

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

## Arquivos Principais para Consultar

### Frontend
- **`frontend/src/App.js`** - Componente principal da aplicação
- **`frontend/src/components/FileUpload.js`** - Upload de arquivos CSV/Excel
- **`frontend/src/components/PreviewSection.js`** - Geração e visualização de previews
- **`frontend/src/components/GenerateSection.js`** - Geração final das etiquetas
- **`frontend/src/components/components.css`** - Estilos dos componentes

### Backend
- **`backend/server.js`** - Servidor Express com todas as rotas
- **`backend/LAYOUT_LABEL.ZPL`** - Template das etiquetas ZPL
- **`backend/package.json`** - Dependências do backend

## Tecnologias Utilizadas

### Frontend
- React.js 18.x
- Axios para requisições HTTP
- Lucide React para ícones
- React Toastify para notificações
- CSS3 com design responsivo

### Backend
- Node.js com Express.js
- Multer para upload de arquivos
- XLSX para processamento de planilhas Excel
- CSV-Parser para arquivos CSV
- Sharp para processamento de imagens
- Puppeteer para geração de previews
- JSZip para compactação de arquivos

## Endpoints da API

### `POST /api/upload`
- **Função:** Upload e processamento de arquivos CSV/XLSX
- **Input:** FormData com arquivo
- **Output:** JSON com dados processados

### `POST /api/generate-preview`
- **Função:** Geração de previews das etiquetas
- **Input:** Dados dos produtos + quantidade de previews
- **Output:** Array de imagens base64

### `POST /api/generate-labels`
- **Função:** Geração final das etiquetas ZPL
- **Input:** Dados completos dos produtos
- **Output:** Arquivo ZIP para download

## Campos Obrigatórios dos Dados

- `STYLE_NAME`: Nome do produto/estilo
- `VPM`: Código VPM do produto
- `COLOR`: Cor do produto
- `SIZE`: Tamanho do produto
- `BARCODE`: Código de barras

## Instruções Específicas

### Antes de Modificar Qualquer Arquivo:

1. **Use `view_files` ou `search_codebase`** para examinar o arquivo atual
2. **Entenda a estrutura** e padrões existentes
3. **Verifique dependências** e imports
4. **Mantenha consistência** com o código existente
5. **Teste funcionalidades** relacionadas

### Para Modificações no Frontend:

1. **Sempre consulte `App.js`** para entender a estrutura de componentes
2. **Verifique `components.css`** para estilos existentes
3. **Mantenha padrões** de nomenclatura e estrutura
4. **Use React hooks** consistentemente (useState, useEffect)
5. **Mantenha tratamento de erros** com try-catch

### Para Modificações no Backend:

1. **Sempre consulte `server.js`** para entender rotas existentes
2. **Verifique middleware** e configurações CORS
3. **Mantenha padrões** de resposta da API
4. **Use async/await** consistentemente
5. **Implemente tratamento de erros** adequado

### Para Modificações de Estilo:

1. **Sempre consulte `components.css`** primeiro
2. **Mantenha nomenclatura** de classes existente
3. **Use variáveis CSS** quando disponíveis
4. **Teste responsividade** em diferentes tamanhos
5. **Mantenha consistência visual** com o design atual

## Fluxo de Desenvolvimento

### 1. Análise
- Consulte arquivos relevantes
- Entenda o contexto atual
- Identifique dependências

### 2. Planejamento
- Defina mudanças necessárias
- Considere impactos em outros componentes
- Planeje testes

### 3. Implementação
- Mantenha padrões existentes
- Implemente mudanças incrementalmente
- Teste cada modificação

### 4. Validação
- Teste funcionalidades afetadas
- Verifique console para erros
- Valide interface do usuário

## Comandos Úteis

### Para Executar o Projeto:
```bash
# Backend
cd backend
npm start

# Frontend
cd frontend
npm start
```

### Para Consultar Arquivos:
- Use `view_files` para ver conteúdo específico
- Use `search_codebase` para encontrar código relacionado
- Use `list_dir` para explorar estrutura de pastas

## Debugging

### Frontend:
- Verifique console do navegador (F12)
- Use React DevTools
- Verifique network tab para requisições

### Backend:
- Verifique logs do terminal
- Use console.log para debug
- Verifique arquivos em uploads/ e output/

## Padrões de Código

### JavaScript/React:
- Use arrow functions
- Use template literals
- Mantenha componentes funcionais
- Use hooks apropriadamente

### CSS:
- Use classes semânticas
- Mantenha hierarquia clara
- Use flexbox/grid para layout
- Implemente responsividade

## Tratamento de Erros

### Frontend:
```javascript
try {
  // código
} catch (error) {
  console.error('Erro:', error);
  toast.error('Mensagem para usuário');
}
```

### Backend:
```javascript
try {
  // código
} catch (error) {
  console.error('Erro:', error);
  res.status(500).json({ error: 'Mensagem de erro' });
}
```

## Lembre-se Sempre:

1. **CONSULTE OS ARQUIVOS** antes de qualquer modificação
2. **MANTENHA CONSISTÊNCIA** com o código existente
3. **TESTE FUNCIONALIDADES** após mudanças
4. **DOCUMENTE MUDANÇAS** importantes
5. **USE FERRAMENTAS** de análise de código disponíveis

---

**Este prompt deve ser usado como referência constante durante o desenvolvimento. Sempre consulte os arquivos do projeto antes de implementar qualquer mudança.**