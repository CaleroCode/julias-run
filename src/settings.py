"""
settings.py - Configuración del juego Julia's Run

📚 PROPÓSITO EDUCATIVO:
Este archivo demuestra la importancia de la ORGANIZACIÓN DEL CÓDIGO.
En lugar de números "mágicos" dispersos por todo el código, 
centralizamos toda la configuración en un solo lugar.

🎯 CONCEPTOS QUE APRENDERÁS:
1. CONSTANTES: Variables que no cambian durante la ejecución
2. NOMBRES DESCRIPTIVOS: PLAYER_SPEED vs speed o s
3. ORGANIZACIÓN: Agrupación lógica por categorías
4. MANTENIMIENTO: Un solo lugar para cambiar configuraciones

💡 VENTAJAS DE ESTA ORGANIZACIÓN:
- ✅ Fácil ajustar velocidades y tamaños
- ✅ No hay números mágicos en el código
- ✅ Otros programadores entienden qué hace cada valor
- ✅ Cambios centralizados afectan todo el juego

🔍 EXPERIMENTO SUGERIDO:
Cambia algunos valores aquí y observa cómo afecta al juego:
- Aumenta PLAYER_SPEED para un juego más rápido
- Cambia OBSTACLE_SPEED para hacerlo más fácil/difícil
- Modifica colores para personalizar el aspecto visual

🤔 PREGUNTA CLAVE:
¿Por qué no poner estos valores directamente en entities.py?
Respuesta: Separación de responsabilidades y facilidad de mantenimiento.
"""

import pygame

# === CONFIGURACIÓN DE VENTANA ===
# 🔍 Mejora sugerida: Estos valores podrían leerse de un archivo de configuración
WINDOW_WIDTH = 1000      # Ancho de la ventana en píxeles
WINDOW_HEIGHT = 800     # Alto de la ventana en píxeles  
FPS = 60               # Cuadros por segundo - ¡Prueba cambiar a 30 o 120!

# === COLORES (formato RGB) ===
# 📚 Los colores se definen como tuplas de 3 valores (Red, Green, Blue)
# Cada valor va de 0 (ausencia) a 255 (máximo)
# 💡 Tip: Usa un color picker online para encontrar nuevos colores
BLACK = (0, 0, 0)          # Ausencia total de color
WHITE = (255, 255, 255)    # Máximo de todos los colores
RED = (255, 0, 0)          # Solo rojo al máximo
GREEN = (0, 255, 0)        # Solo verde al máximo
BLUE = (0, 0, 255)         # Solo azul al máximo
YELLOW = (255, 255, 0)     # Rojo + Verde = Amarillo
GRAY = (128, 128, 128)     # Valor medio de todos
LIGHT_BLUE = (173, 216, 230) # Combinación personalizada
PURPLE = (128, 0, 128)

# === CONFIGURACIÓN DEL JUGADOR ===
PLAYER_WIDTH = 120      # Ancho del sprite del jugador
PLAYER_HEIGHT = 140     # Alto del sprite del jugador
PLAYER_SPEED = 5       # Velocidad normal de movimiento (píxeles por frame)
PLAYER_LIVES = 3       # Número de vidas iniciales
PLAYER_COLOR = BLUE    # Color del rectángulo del jugador (placeholder)

# Posición inicial del jugador (centrado en la parte inferior)
PLAYER_START_X = WINDOW_WIDTH // 2 - PLAYER_WIDTH // 2
PLAYER_START_Y = WINDOW_HEIGHT - PLAYER_HEIGHT - 20

# === CONFIGURACIÓN DE CUCHILLOS ===
KNIFE_WIDTH = 100        # Ancho del cuchillo
KNIFE_HEIGHT = 130      # Alto del cuchillo
KNIFE_SPEED = 10       # Velocidad del cuchillo (píxeles por frame)
KNIFE_COLOR = YELLOW   # Color del cuchillo
KNIFE_COOLDOWN = 30    # Tiempo de cooldown en frames (0.5 segundos a 60 FPS)

# === CONFIGURACIÓN DE OBSTÁCULOS ===
OBSTACLE_WIDTH = 50    # Ancho del obstáculo
OBSTACLE_HEIGHT = 50   # Alto del obstáculo
OBSTACLE_SPEED = 3     # Velocidad de caída (píxeles por frame)
OBSTACLE_COLOR = RED   # Color del obstáculo
OBSTACLE_SPAWN_RATE = 60  # Frames entre spawn de obstáculos (1 segundo a 60 FPS)

# === CONFIGURACIÓN DE POWER-UPS ===
POWERUP_WIDTH = 150     # Ancho del power-up
POWERUP_HEIGHT = 120    # Alto del power-up
POWERUP_SPEED = 2      # Velocidad de caída (más lento que obstáculos)
POWERUP_SPAWN_RATE = 300  # Frames entre spawn de power-ups (5 segundos a 60 FPS)

# Colores de power-ups
VODKA_COLOR = PURPLE   # Vodka Boost - color morado
TEA_COLOR = GREEN      # Té Mágico - color verde
HONEY_COLOR = (255, 200,0) 

# Duración de efectos (en frames)
VODKA_DURATION = 180   # 3 segundos a 60 FPS
TEA_DURATION = 240     # 4 segundos a 60 FPS

# Multiplicadores de efectos
VODKA_SPEED_MULTIPLIER = 1.5  # El jugador se mueve 50% más rápido

# === CONFIGURACIÓN DE PUNTUACIÓN ===
POINTS_PER_OBSTACLE_AVOIDED = 1    # Puntos por esquivar obstáculo
POINTS_PER_OBSTACLE_DESTROYED = 5  # Puntos por destruir obstáculo con cuchillo
POINTS_PER_POWERUP = 10           # Puntos por recoger power-up

# === CONFIGURACIÓN DE ARCHIVOS ===
SCORE_FILE = "best_score.json"    # Archivo donde se guarda el récord

# === TECLAS DEL JUEGO ===
# Estas constantes se usan para hacer el código más legible
# En lugar de usar números mágicos, usamos nombres descriptivos
KEY_LEFT = pygame.K_LEFT
KEY_RIGHT = pygame.K_RIGHT
KEY_UP = pygame.K_UP
KEY_DOWN = pygame.K_DOWN
KEY_SPACE = pygame.K_SPACE
KEY_ENTER = pygame.K_RETURN
KEY_ESCAPE = pygame.K_ESCAPE
KEY_P = pygame.K_p

# === CONFIGURACIÓN DE ESTADOS DEL JUEGO ===
# Estos son los diferentes estados o pantallas del juego
STATE_MENU = "menu"
STATE_PLAYING = "playing"
STATE_GAME_OVER = "game_over"
STATE_PAUSED = "paused"  # ✅ IMPLEMENTADO: Estado de pausa

# === CONFIGURACIÓN DE FUENTES ===
FONT_SIZE_LARGE = 115   # Tamaño de fuente para títulos
FONT_SIZE_MEDIUM = 45  # Tamaño de fuente para texto normal
FONT_SIZE_SMALL = 20   # Tamaño de fuente para detalles

# ✅ IMPLEMENTADO: Configuración para barra de cooldown
COOLDOWN_BAR_WIDTH = 100   # Ancho de la barra de cooldown en píxeles
COOLDOWN_BAR_HEIGHT = 10   # Alto de la barra de cooldown en píxeles
COOLDOWN_BAR_X = 10        # Posición X de la barra de cooldown
COOLDOWN_BAR_Y = 100       # Posición Y de la barra de cooldown

# ✅ IMPLEMENTADO: Configuración para dificultad progresiva
DIFFICULTY_INCREASE_INTERVAL = 10  # Cada cuántos puntos aumenta la dificultad
MAX_OBSTACLE_SPEED = 8             # Velocidad máxima de obstáculos
SPEED_INCREASE_RATE = 0.5          # Cuánto aumenta la velocidad por nivel
MAX_SPAWN_RATE_REDUCTION = 30      # Máxima reducción en frames de spawn

# ✅ IMPLEMENTADO: Configuración de efectos visuales
PARTICLE_COUNT = 15                # Número de partículas en explosión
PARTICLE_LIFE = 30                 # Vida de partículas en frames
SCREEN_SHAKE_INTENSITY = 5         # Intensidad del screen shake
SCREEN_SHAKE_DURATION = 10         # Duración del screen shake en frames

# ✅ IMPLEMENTADO: Configuración de animaciones
SPRITE_ANIMATION_SPEED = 8         # Frames entre cambios de sprite
POWERUP_PULSE_SPEED = 4           # Velocidad del efecto de pulso en power-ups

# TODO 4: Añadir rutas de assets cuando estén disponibles
# SPRITE_JULIA = "assets/sprites/julia.png"
# SPRITE_git grep -n "Palabra que querais buscar" || true = "assets/sprites/knife.png"
# SPRITE_POWERUP = "assets/sprites/powerup.png"
SOUND_THROW = "assets/sounds/throw.wav"
SOUND_HIT = "assets/sounds/hit.wav"
SOUND_POWERUP = "assets/sounds/powerup.wav"

# === NOTAS EDUCATIVAS ===
"""
¿Por qué usar constantes?
1. Facilita el ajuste de valores sin buscar en todo el código
2. Evita errores por escribir mal un número
3. Hace el código más legible y mantenible
4. Permite experimentar con diferentes valores fácilmente

Ejemplo: Si queremos hacer el juego más difícil, solo cambiamos
OBSTACLE_SPEED de 3 a 4, en lugar de buscar todos los lugares
donde aparece el número 3 en el código.

Convenciones de nombres:
- MAYÚSCULAS_CON_GUIONES_BAJOS para constantes
- minúsculas_con_guiones_bajos para variables
- CamelCase para nombres de clases
"""