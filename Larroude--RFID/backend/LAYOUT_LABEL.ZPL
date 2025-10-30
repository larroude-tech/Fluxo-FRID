^XA
^CI28
^LH0,0
^MD30
^PR5
^PW812           ; 4.00" (203 dpi)
^LL406           ; 2.00"

^DFR:LAYOUT_LABEL.ZPL^FS

^FX --- Molduras ---
^FO12,12^GB788,382,2,B,24^FS                  ; externa arredondada
^FO36,48^GB580,290,2,B,14^FS                  ; interna (não invade coluna direita)

^FX --- Ícone do produto (opcional .GRF) ---
^FO60,86^GB80,80,2,B,8^FS
; ^FO64,90^XGPROD.GRF,1,1^FS

^FX --- QR ESQUERDO (dentro da caixa) ---
^FO60,235^BQN,2,5^FN7^FS                      ; conteúdo via FN7 (tamanho 5)

^FX --- Divisor vertical entre ícone e textos ---
^FO170,66^GB2,240,2^FS

^FX --- Textos com FB (sem extrapolar) ---
^CF0,30
^FO190,78 ^FB400,2,0,L,0^FN1^FS               ; STYLE NAME: ...
^CF0,26
^FO190,138^FB400,1,0,L,0^FN2^FS               ; VPN/VPM: ...
^FO190,178^FB400,2,0,L,0^FN3^FS               ; COLOR: ... (quebra se longo)

^FO190,218^A0N,28,28^FDSIZE:^FS               ; rótulo SIZE
^FO260,218^CF0,34^FB330,1,0,L,0^FN4^FS        ; valor SIZE em destaque

^FX --- Código de barras (Code128) ---
^BY2,3,60
^FO190,270^BCN,60,Y,N,N^FN5^FS

^FX --- Coluna direita: QR TOP, cápsula PO/Local, QR BOTTOM ---
^FO654,60 ^BQN,2,6^FN9^FS                     ; QR TOP (tamanho 6)

^FO642,184^GB150,66,2,B,16^FS                 ; cápsula arredondada
^CF0,24
^FO652,198^FB130,2,0,C,0^FN6^FS               ; 1ª linha PO / 2ª linha Local.xxx

^FO654,285^BQN,2,6^FN8^FS                     ; QR BOTTOM (tamanho 6)

^XZ
