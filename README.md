![Imagen5](https://user-images.githubusercontent.com/105141268/232054945-bc8f6d56-e457-4e68-b8b2-c1168dd49090.png)

Tanks es un emocionante minijuego para 2 a 4 jugadores. Conviértete en un tanque, dispárale a tus amigos y sobrevive en el campo de batalla. Avanza, rota y usa tu munición para ser el último en pie. ¡Demuestra tus habilidades y diviértete!


## Autor

Richard Rivero Cornejo - 55800

## Requerimietos

Para ejecutar el juego necesitas:

* **python** >= 3.10
* **arcade y numpy**
* pantalla y teclado

Instala arcade o numpy con pip:

```bash
  pip install arcade
  pip install numpy
```
    
## Controles

| Tecla | Pantalla | Efecto |
| :---: | :---: | :---: |
| ESC | todas | cierra el juego |
| ← | menú | 1 jugador menos |
| → | menú | 1 jugador más |
| Espacio o Enter | menu   | iniciar juego |
| Z | juego | jugador 1 |
| M | juego | jugador 2 |
| Q | juego | jugador 3 |
| P | juego | jugador 4 |
| Espacio o Enter | ganador  | vuelve al menú |

## Instrucciones de juego

Selecciona la cantidad de jugadores entre 2 y 4, preciona espacio/enter para empezar a jugar.

Cada jugador empieza girando en una esquina protegido por cajas empujables. Al precionar la tecla del jugador (Z,M,Q,P) el tanque **dispara un misil** que puede acabar con otro jugador u objetos repartidos aleatoriamente en el mapa. Inicias con munición completa (5 misiles) y cada 4 segundos se **recarga 1 misil** usado. Manteniendo presionada la tecla el tanque **avanza** en la dirección que apunte. Cada vez que se presiona la tecla de jugador el tanque **cambia la dirección de giro**.

![gameplay](https://user-images.githubusercontent.com/105141268/232059594-9bc0dabd-d164-473a-a3a0-cf91910c9fb9.png)

En el mapa hay cajas empujables, arbustos destruibles y rocas resistentes que obstruyen el camino o pueden usarse como defensa.

**¡¡¡ GANA EL ÚLTIMO QUE QUEDE EN PIE !!!**

## Herramientas usadas

* Visual Studio Code - programación
* GIMP - creación de los sprites
* Fontsgeek - descargar fuente *Franklin Gothic Heavy Regular*

## Estructura de carpetas

| Carpeta | Contenido |
| :---: | :--- |
| font | el archivo de la fuente *Franklin Gothic Heavy Regular* |
| gimp | archivos editables de imágenes para sprites |
| img | imágenes para sprites y texturas |
| sprites | lógica de los sprites |
| views | pantallas y lógica del juego |

| Archivo | Contenido |
| :---: | :--- |
| main | manejo de pantallas |
| conf | variables e importaciones comunes |

![Imagen6](https://user-images.githubusercontent.com/105141268/232056550-3a20b31b-c6f2-403e-9c2b-513a5b642b4a.png)
