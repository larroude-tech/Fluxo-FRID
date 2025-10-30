REM ===================================================
REM TEMPLATE ZPL QUE FUNCIONA SEM VOID
REM Baseado no diagnose_void_problem.py que funcionou
REM ===================================================

REM Formato mínimo e limpo que elimina o problema VOID
REM Testado e aprovado na impressora Zebra ZD621R

^XA
^FO50,50^A0N,35,35^FD{STYLE_NAME}^FS
^FO50,100^A0N,28,28^FDVPM: {VPM}^FS
^FO50,140^A0N,28,28^FDCOLOR: {COLOR}^FS
^FO50,180^A0N,28,28^FDSIZE: {SIZE}^FS
^FO50,240^BY2,3,40^BCN,40,Y,N,N^FD{BARCODE}^FS
^FO500,50^BQN,2,4^FD{RFID_DATA}^FS
^FO600,200^A0N,20,20^FD{PO_NUMBER}^FS
^FO600,230^A0N,16,16^FDLocal.{LOCAL}^FS
^RFW,H,2,12,1^FD{RFID_DATA}^FS
^XZ

REM ===================================================
REM CAMPOS SUBSTITUÍVEIS:
REM {STYLE_NAME} - Nome do produto
REM {VPM} - Código VPM completo
REM {COLOR} - Cor do produto
REM {SIZE} - Tamanho
REM {BARCODE} - Código de barras (VPM sem hífens)
REM {RFID_DATA} - Dados para gravação RFID
REM {PO_NUMBER} - Número do PO
REM {LOCAL} - Local/código da loja
REM ===================================================

REM CARACTERÍSTICAS IMPORTANTES:
REM - SEM comandos ^PW e ^LL (causavam VOID)
REM - SEM comandos ^CI, ^LH, ^MD, ^PR (desnecessários)
REM - SEM bordas e caixas (simplificado)
REM - Apenas comandos essenciais
REM - Layout limpo e funcional
REM ===================================================
