@echo off
echo ========================================
echo   Teste de Impressora RFID Zebra ZD621R
echo ========================================
echo.

echo Iniciando servidor backend...
cd backend
start "Backend RFID Test" cmd /k "npm start"

echo Aguardando 3 segundos para o backend inicializar...
timeout /t 3 /nobreak > nul

echo Iniciando frontend...
cd ../frontend
start "Frontend RFID Test" cmd /k "npm start"

echo.
echo ========================================
echo   Servidores iniciados!
echo ========================================
echo.
echo Backend: http://localhost:3002
echo Frontend: http://localhost:3000
echo.
echo Para testar via linha de comando:
echo   cd backend
echo   node test-rfid-printer.js help
echo.
echo Pressione qualquer tecla para sair...
pause > nul
