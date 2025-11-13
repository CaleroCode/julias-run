# Yul's Run - Aprende POO con un Juego Real 🎮

![Pantalla de inicio](assets/sprites/inicio.png)

> Versión extendida y modificada del proyecto original (https://github.com/Anais-RV), con mejoras visuales, animaciones, HUD pixel-art y nuevos sistemas desarrollados hoy.

**Yul's Run** es un proyecto ideal para aprender **Programación Orientada a Objetos con Python y Pygame** trabajando sobre un juego real.  
En esta versión se han añadido mejoras gráficas, efectos modernos, arquitectura más limpia y muchos detalles nuevos para convertirlo en un proyecto profesional y didáctico a la vez.

---

# 🚀 Mejoras añadidas

Aquí está **TODO lo que se ha mejorado hoy**

---

## 🎬 Pantalla de carga mejorada
- Eliminado el fondo azul sólido.
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
- Eliminado el texto “Game Over”.
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
- `self.snd_throw` usado correctamente.
- Preparado para migrarlo a `self.snd_knife` si se desea mantener la lógica del nombre.

---

## 🪓 Gameplay
- Dificultad progresiva mejorada.
- Power-ups más visibles y limpitos.
- Efectos activos reubicados y alineados.
- Mejor lectura en general del HUD durante el juego.

---

## 🎮 Controles
- Flechas → Mover
- **ESPACIO** → Lanzar cuchillo
- **P** → Pausar
- **ESC** → Salir

---

# 🧩 Instalación

```bash
git clone -b dev https://github.com/CaleroCode/julias-run.git
cd julias-run
pip install pygame
make run
# o:
python src/main.py
