import cv2
import dlib
import numpy as np
import pyautogui as autogui

autogui.FAILSAFE = False
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor('shape_predictor_68_face_landmarks.dat')
cap = cv2.VideoCapture(0)
frist = True
#coloca os parametros inicias de posicção
old_pos = [0,0]
while True:
        # Pega a imagem da camera
        ret, image = cap.read()
        # Converte para a escala cinza
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        # Detecta a cara
        rects = detector(gray, 1)
        for rect in rects:
            #Pega as posições das landmarks
            shape = predictor(gray, rect)
            # Converte para um array NumPy
            shape_np = np.zeros((4, 2), dtype="int")
            ins = [30,48,54,50]
            z = 0
            for i in range(0,4):
                shape_np[i] = [ (shape.part(ins[z]).x), (shape.part(ins[z]).y) ]
                z += 1
            shape = shape_np
            # Mostra na tela os landmarks
            for i, (x, y) in enumerate(shape):
            # Coloca os pontos 
                cv2.circle(image, (x, y), 1, (0, 0, 255), -1)
            #fazendo o detector do movimento:
            """ Aqui vai detectar as atuais posições da cara """
            pos = shape[0].tolist()
            posx = pos[0]
            posy = pos[1]
            
            dify = (posy - old_pos[1]) 
            difx = (posx - old_pos[0]) 

            mouse_pos = list(autogui.position())
            movx = mouse_pos[0]
            movy = mouse_pos[1]

            old_x = old_pos[0]
            old_y = old_pos[1]

            if dify > 10 or dify < -10 :
                old_x = pos[0]
                movy = ( posy + dify * 5 )
            
            if difx > 10 or difx < -10 :
                movx = ( posx + difx * -20)
                old_y = pos[1] 
            autogui.moveTo(movx,movy,duration = 0.1)
            """Aqui vai ser onde eu irei localizar a posição das pontas da boca"""
            # definindo a padrão
            if frist == True :
                pose = shape[1].tolist()
                posd = shape[2].tolist()
                difv = shape[3][1] - posy
                difh = posd[0] - pose[0]
                frist = False
            else:
                apose = shape[1].tolist()
                aposd = shape[2].tolist()
                adifv = shape[3][1] - posy
                adifh = aposd[0] - apose[0]

                if adifh > (difh + 10) :
                    autogui.click(button='left')
                if adifv > (difv + 5) :
                    autogui.click(button='right')
                
            """ Aqui vai ser a parte referente a mudar a posição """
            old_pos = [old_x , old_y]
        # Display the image
        cv2.imshow('Mouse', image)

        # Press the escape button to terminate the code
        if cv2.waitKey(10) == 27:
            break
cap.release()