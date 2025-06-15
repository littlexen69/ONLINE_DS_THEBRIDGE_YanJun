from utils import crea_tablero,disparar,colocar_barcos,LADO_TABLERO
import random

def main():
    mi_tablero = crea_tablero()
    su_tablero = crea_tablero()
    colocar_barcos(mi_tablero)
    colocar_barcos(su_tablero)
    print("Mi tablero:")
    print(mi_tablero)
    mi_vista_su_tablero = crea_tablero()

    while "O" in mi_tablero or "O" in su_tablero:

        if "O" not in mi_tablero:
            print("El oponente ha hundido todos tus barcos. ¡Has perdido!")
            break
        else:
            print("Turno del oponente:")
            while True:
                fila = random.randint(0, LADO_TABLERO - 1)
                col = random.randint(0, LADO_TABLERO - 1)
                if mi_tablero[fila, col] == "X":
                    continue
                elif mi_tablero[fila, col] == "A":
                    continue
                else:
                    print("Disparando a:", (fila, col))
                    disparar(mi_tablero, (fila, col))
                    print("Mi tablero actualizado:")
                    print(mi_tablero)
                    break
            
        if "O" not in su_tablero:
            print("¡Has hundido todos los barcos del oponente!")
            break
        else:
            print("Turno del jugador:", flush=True)
            while True:
                while True:
                    fila = input("Introduce la fila (0-9): ").strip()
                    col = input("Introduce la columna (0-9): ").strip()
                    try:
                        fila = int(fila)
                        col = int(col)
                        break
                    except ValueError:
                        print("Inserte un número entero", flush=True)
                if fila < 0 or fila >= LADO_TABLERO or col < 0 or col >= LADO_TABLERO:
                    print("Coordenadas inválidas. Inténtalo de nuevo.", flush=True)
                    continue
                elif su_tablero[fila, col] == "X":
                    print("Ya has disparado a esa coordenada. Inténtalo de nuevo.", flush=True) 
                    continue              
                elif su_tablero[fila, col] == "A":
                    print("Ya has disparado a esa coordenada y ha sido agua. Inténtalo de nuevo.", flush=True)  
                    continue
                else:
                    print("Disparando a:", (fila, col))
                    disparar(su_tablero, (fila, col))
                    if su_tablero[fila, col] == "X":
                        mi_vista_su_tablero[fila, col] = "X"
                    elif su_tablero[fila, col] == "A":
                        mi_vista_su_tablero[fila, col] = "A"
                    else:
                        mi_vista_su_tablero[fila, col] = "O"
                    print("Tablero del oponente actualizado:")
                    print(mi_vista_su_tablero)
                    break

if __name__ == "__main__":
    main()