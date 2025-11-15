# Julia's Run (Yul's Run) - Aprende POO con un Juego Real 🎮

![Pantalla de inicio](assets/sprites/inicio.png)

> Versión extendida y modificada del proyecto original ([repo de Anais-RV](https://github.com/Anais-RV)), con mejoras visuales, animaciones, HUD pixel-art y nuevos sistemas desarrollados y ampliados.

**Julia's Run / Yul's Run** es un proyecto ideal para aprender **Programación Orientada a Objetos con Python y Pygame** trabajando sobre un juego real.  
En esta versión se han añadido mejoras gráficas, efectos modernos, arquitectura más limpia y muchos detalles nuevos para convertirlo en un proyecto profesional y didáctico a la vez.

---

# 🚀 Mejoras añadidas

Aquí está **TODO lo que se ha mejorado** sobre la base original:

---

## 🎬 Pantalla de carga mejorada
- Eliminado el fondo sólido.
- Añadido overlay **semi-transparente** para no romper la estética.
- `loading.png` ahora aparece **escalado** y centrado correctamente.
- Evita pantallazos negros iniciales.

---

## 🎨 HUD estilo pixel-art completamente nuevo
- Sustituido el HUD original por uno **retro arcade**.
- Fondo semitransparente tipo *glass*.
- Bordes pixelados y consistentes.
- Score formateado como `SCORE 000120`.
- Corazones de vida colocados junto al texto **LIVES**, no desperdigados.
- Eliminados los círculos rojos de fallback.
- Escudo reubicado y armonizado con el HUD.

---

## 💥 Game Over rediseñado
- Eliminado el texto “Game Over” plano.
- Ahora usa el sprite **`gameover_small.png`** como logotipo.
- Logo alineado **a la izquierda y centrado verticalmente**, para no tapar la animación del fondo.
- Todo el texto del Game Over ahora está **alineado a la izquierda**.
- Instrucciones (`ENTER para jugar de nuevo`, `ESC para salir`) ahora en **blanco**.
- Puntuación y récord movidos a la **esquina superior izquierda**.

---

## 🌟 Animaciones y efectos visuales mejorados
- Fondos animados en menú y Game Over funcionando con escala *cover*.
- Screen shake al recibir daño.
- Efectos de pulso en modo pausa.
- Partículas mejoradas:
  - Colisiones
  - Power-ups
  - Explosiones
- Explosiones con más frames y mejor sincronización.

---

## 🔊 Sistema de sonido ordenado
- Sonido del cuchillo renombrado y reorganizado.
- `self.snd_throw` (y otros efectos) usados de forma consistente.
- Preparado para seguir ampliando el sistema de audio.

---

## 🪓 Gameplay
- Dificultad progresiva mejorada (a más puntuación, más locura).
- Power-ups más visibles y limpios.
- Efectos activos reubicados y alineados.
- Mejor lectura en general del HUD durante el juego.
- Sistema de **combos** que premia jugar bien (más puntos por racha).

---

## 🎄 Versión Navideña, Grinch y Shurikens

Se ha añadido una mini “expansión” temática con nuevos power-ups:

### 🎅 Modo Navidad (Sombrero navideño)
- Nuevo power-up: **sombrero navideño**.
- Al recogerlo:
  - El juego cambia a un **modo navideño**:  
    - Fondo nevado
    - Sprite navideño de Julia
    - Música de fondo especial de Navidad
- Ideal para romper el hielo en las partidas de diciembre.  

### 💚 El Grinch (vuelta a la normalidad)
- Nuevo power-up: **Grinch**.
- Si lo coges mientras estás en modo Navidad:
  - Se **desactiva el modo navideño**.
  - Vuelven el fondo normal, el sprite original y la música estándar.
- Básicamente: el Grinch te roba la Navidad… pero te devuelve el juego original. 😈🎁  

### 🌀 Shurikens protectores (nuevo power-up)
- Nuevo power-up: **Shuriken**.
- Al recogerlo:
  - Aparecen **varios shurikens orbitando alrededor de Julia**.
  - Durante ~**10 segundos** destruyen todo lo que tocan:
    - Cachopos / obstáculos
    - Enemigos
  - Cada impacto da puntos extra y genera explosiones y partículas.
- Es un escudo ofensivo: no solo te protege, sino que limpia la pantalla.

---

## 🎮 Controles

- Flechas → Mover
- **ESPACIO** → Lanzar cuchillo
- **P** → Pausar
- **ESC** → Salir
- **F1** → Activar/desactivar modo debug
- **F2** → Mostrar/ocultar contador de FPS
- **F3 (en debug)** → Añadir puntos para pruebas

---

# 🧩 Instalación

```bash
git clone -b dev https://github.com/CaleroCode/julias-run.git
cd julias-run
pip install pygame
make run
# o:
python src/main.py
