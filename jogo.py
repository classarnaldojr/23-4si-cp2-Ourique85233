import cv2

import numpy as np

cap = cv2.VideoCapture('pedra-papel-tesoura.mp4') #Captura do Vídeo

if not cap.isOpened():
    raise Exception("Vídeo não abriu")  # Expection se o Vídeo não abrir

while True:

    ret, frame = cap.read() #Ler o frame do vídeo

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)  # Filtro de Cinza

    blur = cv2.blur(hsv, (15, 15), 0)  # Blur na Imagem para ficar mais clara a detecção

    lh_1 = np.array([0, 20, 10])  # Range Mínimo para Escala do Filtro HSV
    hh_1 = np.array([18, 200, 200])  # Range Máximo para Escala do Filtro HSV

    lh_2 = np.array([0, 1, 1])  # Range Mínimo para Escala do Filtro HSV
    hh_2 = np.array([255, 150, 250])  # Range Máximo para Escala do Filtro HSV

    mask_1 = cv2.inRange(blur, lh_1, hh_1)  # Máscara 1

    mask_2 = cv2.inRange(blur, lh_2, hh_2)  # Máscara 2

    img = cv2.bitwise_or(mask_1, mask_2)  # Imagem filtrada (para calcular Massa do Objeto)

    contours, _ = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE) #Encontrar os Contornos da Imagem img_filtro

    img = cv2.cvtColor(img, cv2.COLOR_GRAY2RGB)

    cv2.drawContours(img, contours, -1, [255, 0, 0], 5) #Contornos Azuis na Imagem

    contorno_1 = contours[1] #Puxando Jogador 1

    contorno_2 = contours[0] #Puxando Jogador 2

    dict = cv2.moments(contorno_1) #Retirando Dicionário dos Contornos do Jogador 1
    dict2 = cv2.moments(contorno_2) #Retirando Dicionário dos Contornos do Jogador 2

    area1 = int(dict['m00']) #Área da mão do jogador 1
    area2 = int(dict2['m00'])#Área da mão do jogador 2

    if area1 < 58199:       #Definindo Tesoura como Área menor que 58200
        area1 = "Tesoura"

    elif area1 > 58200 and area1 < 71000:    #Definindo Pedra como Área entre 58200 e 7100
        area1 = "Pedra"

    elif area1 > 71000:     #Definindo Papel como Área maior que 71000
        area1 = "Papel"

    if area2 < 58199:
        area2 = "Tesoura"

    elif area2 > 58200 and area2 < 71000:
        area2 = "Pedra"

    elif area2 > 71000:
        area2 = "Papel"

    if area1 == "Pedra" and area2 == "Tesoura":
        area1 = "Tesoura"
        area2 = "Pedra"

    # SISTEMA DE PONTUAÇÕES

    if (area1 == "Tesoura" and area2 == "Papel"):

        resultado = "Player 1 Wins"

    elif (area1 == "Papel" and area2 == "Tesoura"):

        resultado = "Player 2 Wins"

    elif (area1 == "Pedra" and area2 == "Tesoura"):

        resultado = "Player 1 Wins"

    elif (area1 == "Tesoura" and area2 == "Pedra"):

        resultado = "Player 2 Wins!"

    elif (area1 == "Papel" and area2 == "Pedra"):

        resultado = "Player 1 Wins!"
    elif (area1 == "Pedra" and area2 == "Papel"):

        resultado = "Player 2 Wins"

    if area1 == area2:
        resultado = "Draw"

    #Inserindo Dados na Imagem

    #Jogador 1
    (cv2.putText(img,("Player 1 = " + str(area1)),(250, 250),cv2.FONT_HERSHEY_SIMPLEX,2, (255, 0, 0), 2, cv2.LINE_AA))

    #Jogador 2

    (cv2.putText(img,("Player 2 = " + str(area2)),(1050, 250),cv2.FONT_HERSHEY_SIMPLEX,2, (255, 0, 0), 2, cv2.LINE_AA))

    #Resultado
    (cv2.putText(img,str(resultado),(700, 120),cv2.FONT_HERSHEY_SIMPLEX,2,(255, 0, 0), 2, cv2.LINE_AA))

    img = cv2.resize(img, (1280, 1024))

    cv2.imshow("Imagem", img)

    if cv2.waitKey(1) & 0xFF == ord('p'):
        break

    if not ret:
        break

cap.release()

cv2.destroyAllWindows()