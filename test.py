""""
hand_p1 = [3,6,6]

for i, carta1 in enumerate(hand_p1):
    print(i)
    print(carta1)
    for j, carta2 in enumerate(hand_p1[i+1:], start=i+1):
        if i==1: 
            break
        print(j)
        print(carta2)
        if carta1 == carta2:
            print("test")
            print(carta1, carta2)
"""
"""""
hand_p1 = [(6, 2), (6, 2), (7, 2)]
puntos_envido = 0

for i, carta1 in enumerate(hand_p1):
    for j, carta2 in enumerate(hand_p1[i+1:], start=i+1):
        if carta1[1] == carta2[1]:
            puntos_envido += carta1[0] + carta2[0] + 20
            print(f"Se encontraron dos cartas con palos iguales: {carta1} y {carta2} (Palo: {carta1[1]})")

print(f"Puntos de envido acumulados: {puntos_envido}")
"""
hand_p1 = [(12, 2), (12, 3), (12, 3)]
hand_p2 = [(2, 1), (12, 1), (12, 0)]

def calculate_envido(hand_p1, hand_p2):
    puntos_envido_p1 = 0
    puntos_envido_p2 = 0                                           # No hay flor, los 2 valores mas grandes de la mano se usan en el envido
    if hand_p1[0][1] == hand_p1[1][1]:                              # Verificar si se repiten palos haciendo todas las combinaciones posibles y verificar si alguna carta es 10
        if hand_p1[0][0] >= 10 and hand_p1[1][0] < 10:              # Se podria optimizar muchisimo este codigo para no usar muchos if anidados, pero no supe otra forma para hacerlo mejor
            puntos_envido_p1 = 20 + hand_p1[1][0]
        elif hand_p1[1][0] >= 10 and hand_p1[0][0] < 10:
            puntos_envido_p1 = 20 + hand_p1[0][0]
        elif hand_p1[0][0] >= 10 and hand_p1[1][0] >= 10:
            puntos_envido_p1 = 20
        else:
            puntos_envido_p1 = hand_p1[0][0]+hand_p1[1][0] + 20

    elif hand_p1[0][1] == hand_p1[2][1]:
        if hand_p1[0][0] >= 10 and hand_p1[2][0] < 10:
            puntos_envido_p1 = 20 + hand_p1[2][0]
        elif hand_p1[2][0] >= 10 and hand_p1[0][0] < 10:
            puntos_envido_p1 = 20 + hand_p1[0][0]
        elif hand_p1[0][0] >= 10 and hand_p1[2][0] >= 10:
            puntos_envido_p1 = 20
        else:
            puntos_envido_p1 = hand_p1[0][0]+hand_p1[2][0] + 20
    
    elif hand_p1[1][1] == hand_p1[2][1]:
        if hand_p1[1][0] >= 10 and hand_p1[2][0] < 10:
            puntos_envido_p1 = 20 + hand_p1[2][0]
        elif hand_p1[2][0] >= 10 and hand_p1[1][0] < 10:
            puntos_envido_p1 = 20 + hand_p1[1][0]
        elif hand_p1[1][0] >= 10 and hand_p1[2][0] >= 10:
            puntos_envido_p1 = 20
        else:
            puntos_envido_p1 = hand_p1[1][0]+hand_p1[2][0] + 20
    else:
        valores = [carta[0] for carta in hand_p1]
        for i in valores:
            valores.sort(reverse=True)                     
            puntos_envido_p1 = valores[0]

    if hand_p1[0][1] == hand_p1[1][1] == hand_p1[2][1]:         # Verificar si 3 palos son iguales                                    
            valores = [carta[0] for carta in hand_p1]
            for i in range(3):
                if valores[i] >= 10:
                    valores.pop(i)       # Crear una lista auxiliar con la mano
            valores.sort(reverse=True)                     # Ordenar la lista de forma descendente, para que los 2 valores mas grandes queden en posicion [0] y [1]
            puntos_envido_p1 = valores[0]+valores[1]+20
    
    if hand_p2[0][1] == hand_p2[1][1]:                              # P2
        if hand_p2[0][0] >= 10 and hand_p2[1][0] < 10:               
            puntos_envido_p2 = 20 + hand_p2[1][0]
        elif hand_p2[1][0] >= 10 and hand_p2[0][0] < 10:
            puntos_envido_p2 = 20 + hand_p2[0][0]
        elif hand_p2[0][0] >= 10 and hand_p2[1][0] >= 10:
            puntos_envido_p2 = 20
        else:
            puntos_envido_p2 = hand_p2[0][0]+hand_p2[1][0] + 20

    elif hand_p2[0][1] == hand_p2[2][1]:
        if hand_p2[0][0] >= 10 and hand_p2[2][0] < 10:
            puntos_envido_p2 = 20 + hand_p2[2][0]
        elif hand_p2[2][0] >= 10 and hand_p2[0][0] < 10:
            puntos_envido_p2 = 20 + hand_p2[0][0]
        elif hand_p2[0][0] >= 10 and hand_p2[2][0] >= 10:
            puntos_envido_p2 = 20
        else:
            puntos_envido_p2 = hand_p2[0][0]+hand_p2[2][0] + 20
    
    elif hand_p2[1][1] == hand_p2[2][1]:
        if hand_p2[1][0] >= 10 and hand_p2[2][0] < 10:
            puntos_envido_p2 = 20 + hand_p2[2][0]
        elif hand_p2[2][0] >= 10 and hand_p2[1][0] < 10:
            puntos_envido_p2 = 20 + hand_p2[1][0]
        elif hand_p2[1][0] >= 10 and hand_p2[2][0] >= 10:
            puntos_envido_p2 = 20
        else:
            puntos_envido_p2 = hand_p2[1][0]+hand_p2[2][0] + 20
    else:
        valores = [carta[0] for carta in hand_p2]
        for i in valores:
            valores.sort(reverse=True)                     
            puntos_envido_p2 = valores[0]

    if hand_p2[0][1] == hand_p2[1][1] == hand_p2[2][1]:                                           
            valores = [carta[0] for carta in hand_p2]
            for i in range(3):
                if valores[i] >= 10:
                    valores.pop(i)       
            valores.sort(reverse=True)                     
            puntos_envido_p2 = valores[0]+valores[1]+20
    
    #for i in range(len(hand_p1)):                                       
    #    for j, carta in enumerate(hand_p1[i+1:], start=i+1): 
    #        if hand_p1[i][1] == carta[1]:   
    #            aux = hand_p1[i][0] + carta[0] + 20                                                
    #            if hand_p1[i][0] >= 10:                         
    #                puntos_envido_p1 = 20 + carta[0]
    #                found = True
    #if not found:
    #     puntos_envido_p1 = aux
    
    
    #for i in range(len(hand_p2)):                                     
    #    for j, carta in enumerate(hand_p2[i+1:], start=i+1): 
    #        if hand_p2[i][1] == carta[1]:                       
    #            if hand_p2[i][0] >= 10:                         
    #                puntos_envido_p2 += 20 + carta[0]
    #            else:
    #                puntos_envido_p2 += hand_p2[i][0] + carta[0] + 20
    #if hand_p2[0][1] == hand_p2[1][1] == hand_p2[2][1]:                                         
    #        valores = [carta[0] for carta in hand_p2]       
    #        valores.sort(reverse=True)                    
    #        puntos_envido_p2 = valores[0]+valores[1]+20

    print(f"Envido jugador 1: {puntos_envido_p1}")
    print(f"Puntos jugador 2: {puntos_envido_p2}")

calculate_envido(hand_p1, hand_p2)
