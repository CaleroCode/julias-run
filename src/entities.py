"""
entities.py - Entidades del juego Julia's Run

📚 PROPÓSITO EDUCATIVO:
Este archivo contiene todas las CLASES que representan los objetos del juego.
Es el ejemplo perfecto para entender Programación Orientada a Objetos (POO).

🧩 CONCEPTOS POO QUE VAS A VER:
1. CLASES: Player, Obstacle, PowerUp, Knife (moldes/plantillas)
2. OBJETOS: Cada enemigo específico, el jugador único (instancias)
3. ATRIBUTOS: self.lives, self.rect, self.speed (características)
4. MÉTODOS: update(), draw(), take_damage() (comportamientos)
5. ENCAPSULACIÓN: Todo lo del jugador está en la clase Player

🎯 CÓMO LEER ESTE ARCHIVO:
- Busca 'class' para encontrar las clases principales
- Dentro de cada clase, 'def __init__' es el constructor
- Los 'self.' son atributos (características del objeto)
- Los 'def nombre()' son métodos (acciones que puede hacer)

💡 PREGÚNTATE MIENTRAS LEES:
- ¿Qué características tiene esta entidad?
- ¿Qué acciones puede realizar?
- ¿Por qué está todo junto en una clase?
- ¿Cómo se relaciona con las otras clases?

🔍 MEJORAS SUGERIDAS PARA ALUMNADO:
- Añadir más tipos de power-ups
- Crear nuevos tipos de obstáculos
- Implementar animaciones más complejas
- Mejorar los efectos visuales
"""

import pygame
import random
import os
from settings import *

# === GESTIÓN DE SPRITES ===
"""
Este módulo incluye la carga y renderizado de sprites (imágenes) en lugar de rectángulos.

Conceptos importantes sobre sprites en pygame:
1. pygame.image.load() - Carga una imagen desde archivo
2. convert_alpha() - Optimiza la imagen para mejor rendimiento y soporte de transparencia
3. transform.scale() - Redimensiona la imagen al tamaño deseado
4. screen.blit() - Dibuja la imagen en la pantalla en una posición específica

Diferencias entre pygame.draw y blit:
- pygame.draw: Dibuja formas geométricas (rectángulos, círculos, líneas)
- screen.blit: Dibuja imágenes/sprites cargados desde archivos

¿Por qué usar convert_alpha()?
- Mejora significativamente el rendimiento al dibujar
- Preserva la transparencia del fondo (canal alpha)
- Adapta el formato de píxeles al de la pantalla

Gestión de errores:
- Siempre incluimos fallbacks en caso de que las imágenes no existan
- El juego debe funcionar correctamente aunque falten sprites
"""

def load_sprite_with_fallback(sprite_path, fallback_color, width, height):
    """
    Función auxiliar para cargar sprites con fallback seguro.
    
    Args:
        sprite_path: Ruta al archivo de imagen
        fallback_color: Color a usar si la imagen no se encuentra
        width, height: Dimensiones para escalar la imagen
    
    Returns:
        tuple: (imagen_cargada, es_fallback_boolean)
    """
    try:
        if os.path.exists(sprite_path):
            # Cargar imagen original
            image = pygame.image.load(sprite_path)
            
            # convert_alpha() optimiza la imagen y preserva transparencia
            image = image.convert_alpha()
            
            # Escalar al tamaño deseado - pygame.transform.scale()
            image = pygame.transform.scale(image, (width, height))
            
            return image, False  # Imagen cargada exitosamente
        else:
            # Crear sprite fallback si no existe la imagen
            return create_fallback_sprite(fallback_color, width, height), True
            
    except (pygame.error, FileNotFoundError, OSError) as e:
        print(f"⚠️ Error cargando sprite {sprite_path}: {e}")
        print(f"   Usando fallback de color {fallback_color}")
        return create_fallback_sprite(fallback_color, width, height), True

def create_fallback_sprite(color, width, height):
    """
    Crea un sprite de fallback (rectángulo de color) cuando la imagen no está disponible.
    
    Args:
        color: Color RGB del fallback
        width, height: Dimensiones del sprite
    
    Returns:
        pygame.Surface: Superficie con el color especificado
    """
    # Crear una superficie con transparencia
    surface = pygame.Surface((width, height), pygame.SRCALPHA)
    
    # Rellenar con el color especificado
    surface.fill(color)
    
    # Añadir un borde para distinguir que es un fallback
    # pygame.draw.rect(surface, WHITE, surface.get_rect(), 2)
    
    
    return surface

class Player:
    """
    🎮 CLASE PLAYER - Representa al personaje principal (Julia)
    
    📚 CONCEPTOS POO QUE APRENDERÁS:
    
    🏗️ ENCAPSULACIÓN:
    Todos los datos y comportamientos del jugador están dentro de esta clase.
    No hay variables globales sueltas, todo está organizado.
    
    📦 ATRIBUTOS (lo que "TIENE" o "ES" el jugador):
    - lives: ¿Cuántas vidas le quedan?
    - score: ¿Cuántos puntos ha conseguido?  
    - rect: ¿Dónde está en la pantalla?
    - speed: ¿Qué tan rápido se mueve?
    - has_shield: ¿Tiene protección activa?
    
    ⚡ MÉTODOS (lo que "HACE" el jugador):
    - move(): ¿Cómo se mueve con las teclas?
    - draw(): ¿Cómo se dibuja en pantalla?
    - take_damage(): ¿Qué pasa cuando le hacen daño?
    - restore_life(): Restaura vidas (p. ej. cuando recoge una manzana)
    
    🤔 PREGUNTA CLAVE:
    ¿Por qué usar una clase en lugar de variables sueltas?
    Respuesta: Organización, reutilización y mantenimiento del código.
    
    🔍 Mejora sugerida: Esta clase podría dividirse en componentes más pequeños
    (PlayerMovement, PlayerGraphics, PlayerState) para mejor organización.
    """
    
    def __init__(self):
        """
        🏗️ CONSTRUCTOR - Cómo se "construye" un jugador
        
        El método __init__ se ejecuta automáticamente cuando haces:
        player = Player()  # ¡Aquí se ejecuta este método!
        
        📦 Todos los self.algo son ATRIBUTOS del objeto que se está creando.
        """
        
        # 📍 POSICIÓN Y TAMAÑO - pygame.Rect es perfecto para colisiones
        self.rect = pygame.Rect(PLAYER_START_X, PLAYER_START_Y, PLAYER_WIDTH, PLAYER_HEIGHT)
        
        # 🎮 ESTADO DEL JUEGO
        self.lives = PLAYER_LIVES           # Empieza con vidas completas
        self.score = 0                      # Puntuación inicial
        self.speed = PLAYER_SPEED           # Velocidad de movimiento
        self.original_speed = self.speed    # Guardar velocidad base para restaurar
        self.has_shield = False             # Sin escudo al inicio
        self.honey_timer = 0                # Duración del efecto de ralentización
        
        # === CARGA DE SPRITE PARA JULIA ===
        sprite_path = SPRITE_JULIA
        self.sprite, self.using_fallback = load_sprite_with_fallback(
            sprite_path,
            PLAYER_COLOR,
            PLAYER_WIDTH,
            PLAYER_HEIGHT
        )

        
        # ✅ IMPLEMENTADO: Atributos para animaciones de sprites
        self.sprite_frame = 0          # Frame actual de animación
        self.animation_timer = 0       # Contador para cambio de frames
        self.facing_direction = 1      # 1 = derecha, -1 = izquierda
        
        # ✅ IMPLEMENTADO: Efectos visuales
        self.hit_flash_timer = 0       # Timer para efecto de parpadeo al recibir daño
        self.invulnerability_timer = 0 # Frames de invulnerabilidad después de recibir daño
        
        # --------------------------
        # NUEVO: Atributos para la inclinación/rotación visual al moverse
        # rotation_angle: ángulo actual (grados) aplicado al renderizado (visual only)
        # target_rotation: ángulo objetivo hacia el que se interpola
        # LEAN_ANGLE: ángulo máximo de inclinación en grados (ajustable)
        # ROTATION_SMOOTHING: factor de interpolación (0..1), mayor = más rápido
        # --------------------------
        self.rotation_angle = 0.0        # ángulo actual aplicado al dibujo (grados)
        self.target_rotation = 0.0       # ángulo objetivo hacia el que interpolar
        self.LEAN_ANGLE = 12.0           # ángulo máximo de inclinación en grados
        self.ROTATION_SMOOTHING = 0.18   # cuánto suaviza la interpolización (0..1). Más alto = más rápido

        # ✅ COMPATIBILIDAD: Flag de mezcla seguro para tintes (evita AttributeError en algunas builds de pygame)
        self.BLEND_TINT = getattr(pygame, "BLEND_ALPHA_SDL2",
                           getattr(pygame, "BLEND_RGBA_ADD", 0))

        # Debug info para desarrollo
        if self.using_fallback:
            print("🎮 Player: Usando rectángulo fallback (imagen no encontrada)")
        else:
            print("🎮 Player: Sprite cargado exitosamente desde", sprite_path)

    def set_sprite(self, sprite_path):
        """
        Cambia el sprite actual del jugador (para skins como el modo Navidad).
        """
        self.sprite, self.using_fallback = load_sprite_with_fallback(
            sprite_path,
            PLAYER_COLOR,
            PLAYER_WIDTH,
            PLAYER_HEIGHT
        )


    def move(self, keys_pressed):
        """
        ⚡ MÉTODO MOVE - Cómo se mueve el jugador
        
        📚 CONCEPTOS QUE VAS A VER:
        - Parámetros: keys_pressed (información externa que necesita el método)
        - self: Referencia al objeto actual (esta instancia específica de Player)
        - Modificación de atributos: self.rect.x, self.speed
        - Lógica condicional: if para detectar teclas presionadas
        
        🤔 PREGUNTA: ¿Por qué es un método y no una función suelta?
        Respuesta: Porque necesita acceso a los atributos del jugador (self.rect, self.speed)
        
        Args:
            keys_pressed: Diccionario con el estado de todas las teclas del teclado
        """
        
        # 🎬 ANIMACIÓN: Actualizar frame de sprite
        self.animation_timer += 1
        if self.animation_timer >= SPRITE_ANIMATION_SPEED:
            self.sprite_frame = (self.sprite_frame + 1) % 4  # 4 frames de animación
            self.animation_timer = 0
        
        # ⏰ EFECTOS TEMPORALES: Reducir timers
        if self.hit_flash_timer > 0:
            self.hit_flash_timer -= 1
        if self.invulnerability_timer > 0:
            self.invulnerability_timer -= 1

        # 🐝 EFECTO DE MIEL: Ralentizar temporalmente al jugador
        if self.honey_timer > 0:
            self.honey_timer -= 1
            if self.honey_timer == 0:
                self.speed = self.original_speed  # Restaurar velocidad original
        
        # 🏃 DETECCIÓN DE MOVIMIENTO (para animaciones)
        is_moving = False
        
        # ⬅️ MOVIMIENTO HORIZONTAL
        if keys_pressed[KEY_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed
            self.facing_direction = -1
            is_moving = True
            
        if keys_pressed[KEY_RIGHT] and self.rect.right < WINDOW_WIDTH:
            self.rect.x += self.speed
            self.facing_direction = 1
            is_moving = True
            
        # ⬆️⬇️ MOVIMIENTO VERTICAL
        if keys_pressed[KEY_UP] and self.rect.top > 0:
            self.rect.y -= self.speed
            is_moving = True
            
        if keys_pressed[KEY_DOWN] and self.rect.bottom < WINDOW_HEIGHT:
            self.rect.y += self.speed
            is_moving = True
        
        # ✅ IMPLEMENTADO: Resetear animación si no se mueve
        if not is_moving:
            self.sprite_frame = 0  # Frame estático cuando no se mueve

        # --------------------------
        # NUEVO: actualizar target_rotation según dirección horizontal actual
        # - Izquierda -> inclinar hacia la izquierda (positivo)
        # - Derecha  -> inclinar hacia la derecha (negativo)
        # - Ninguna  -> volver recto (0)
        # Esto solo afecta al render (rotación visual), no a colisiones.
        # --------------------------
        if keys_pressed[KEY_LEFT] and self.rect.left > 0:
            self.target_rotation = self.LEAN_ANGLE
        elif keys_pressed[KEY_RIGHT] and self.rect.right < WINDOW_WIDTH:
            self.target_rotation = -self.LEAN_ANGLE
        else:
            self.target_rotation = 0.0

        # Interpolar suavemente el ángulo actual hacia el objetivo
        # (puedes ajustar ROTATION_SMOOTHING para que sea más o menos suave)
        self.rotation_angle += (self.target_rotation - self.rotation_angle) * self.ROTATION_SMOOTHING
    
    def draw(self, screen):
        """
        Dibuja al jugador en la pantalla.
        
        Args:
            screen: Superficie de pygame donde dibujar
        """
        
        # ✅ IMPLEMENTADO: Efecto de parpadeo cuando recibe daño
        if self.hit_flash_timer > 0 and self.hit_flash_timer % 4 < 2:
            return  # No dibujar cada 2 frames para crear efecto de parpadeo
        
        # === RENDERIZADO DE SPRITE O FALLBACK ===
        if self.using_fallback:
            # Si usamos fallback, dibujar rectángulo mejorado
            # Color base del jugador
            color = PLAYER_COLOR
            
            # Si tiene escudo, cambiar color para indicarlo visualmente
            if self.has_shield:
                color = TEA_COLOR  # Verde cuando tiene escudo
                
                # ✅ IMPLEMENTADO: Efecto de pulso para el escudo
                pulse = abs((pygame.time.get_ticks() // 200) % 2)  # Cambia cada 200ms
                if pulse:
                    # Hacer el color más brillante
                    color = tuple(min(255, c + 50) for c in color)
            
            # -------------------------------------------------------------
            # NUEVO: Crear una superficie temporal con la representación del jugador
            # para poder rotarla sin modificar self.rect (la colisión queda igual).
            # -------------------------------------------------------------
            surf = pygame.Surface((self.rect.width, self.rect.height), pygame.SRCALPHA)
            
            # Dibujar el rectángulo del jugador en la superficie temporal
            pygame.draw.rect(surf, color, pygame.Rect(0, 0, self.rect.width, self.rect.height))
            
            # ✅ IMPLEMENTADO: Dibujar dirección con un pequeño indicador (en la surf)
            if self.facing_direction == 1:  # Derecha
                points = [(self.rect.width, self.rect.height // 2),
                         (self.rect.width - 8, self.rect.height // 2 - 4),
                         (self.rect.width - 8, self.rect.height // 2 + 4)]
            else:  # Izquierda
                points = [(0, self.rect.height // 2),
                         (8, self.rect.height // 2 - 4),
                         (8, self.rect.height // 2 + 4)]
            
            # pygame.draw.polygon(surf, WHITE, points)
            
            # -------------------------------------------------------------
            # NUEVO: Rotar la superficie según rotation_angle (rotación visual)
            # y mantener el centro en self.rect.center para que la colisión no cambie.
            # -------------------------------------------------------------
            rotated = pygame.transform.rotate(surf, self.rotation_angle)
            rotated_rect = rotated.get_rect(center=self.rect.center)
            screen.blit(rotated, rotated_rect.topleft)
            
            # ✅ IMPLEMENTADO: Borde adicional si es invulnerable (usando rotated_rect ahora)
            if self.invulnerability_timer > 0:
                border_rect = pygame.Rect(rotated_rect.x - 2, rotated_rect.y - 2, 
                                        rotated_rect.width + 4, rotated_rect.height + 4)
                pygame.draw.rect(screen, YELLOW, border_rect, 2)
        
        else:
            # === RENDERIZADO DE SPRITE REAL ===
            sprite_to_draw = self.sprite
            
            # Si está mirando hacia la izquierda, voltear el sprite
            if self.facing_direction == -1:
                sprite_to_draw = pygame.transform.flip(self.sprite, True, False)
            
            # Si tiene escudo, aplicar tinte verdoso
            if self.has_shield:
                # Crear una copia del sprite con tinte
                sprite_to_draw = sprite_to_draw.copy()
                
                # Crear superficie de tinte
                tint_surface = pygame.Surface(sprite_to_draw.get_size(), pygame.SRCALPHA)
                tint_surface.fill((*TEA_COLOR, 100))  # Verde semi-transparente
                
                # Aplicar tinte al sprite (con compatibilidad de flag)
                if self.BLEND_TINT:
                    sprite_to_draw.blit(tint_surface, (0, 0), special_flags=self.BLEND_TINT)
                else:
                    sprite_to_draw.blit(tint_surface, (0, 0))
            
            # -------------------------------------------------------------
            # NUEVO: Aplicar rotación suavizada al sprite real (solo visual)
            # - Se usa get_rect(center=self.rect.center) para que el sprite rotado
            #   mantenga el mismo centro visual que el rect original.
            # - Las colisiones siguen dependiendo de self.rect (sin rotar).
            # -------------------------------------------------------------
            rotated_sprite = pygame.transform.rotate(sprite_to_draw, self.rotation_angle)
            rotated_rect = rotated_sprite.get_rect(center=self.rect.center)
            screen.blit(rotated_sprite, rotated_rect.topleft)
            
            # ✅ IMPLEMENTADO: Borde adicional si es invulnerable (ahora usando rotated_rect)
            if self.invulnerability_timer > 0:
                border_rect = pygame.Rect(rotated_rect.x - 2, rotated_rect.y - 2, 
                                        rotated_rect.width + 4, rotated_rect.height + 4)
                pygame.draw.rect(screen, YELLOW, border_rect, 2)
    
    def take_damage(self):
        """
        El jugador recibe daño. Si tiene escudo, lo pierde.
        Si no tiene escudo, pierde una vida.
        
        Returns:
            bool: True si el jugador sigue vivo, False si se queda sin vidas
        """
        
        # ✅ IMPLEMENTADO: No recibir daño si está en período de invulnerabilidad
        if self.invulnerability_timer > 0:
            return True  # Aún invulnerable, no recibir daño
        
        if self.has_shield:
            # El escudo absorbe el daño
            self.has_shield = False
            # ✅ IMPLEMENTADO: Efecto visual al perder escudo
            self.hit_flash_timer = 20  # 20 frames de parpadeo
            print("¡Escudo perdido!")  # Mensaje educativo para debug
            return True
        else:
            # Pierde una vida
            self.lives -= 1
            # ✅ IMPLEMENTADO: Período de invulnerabilidad tras recibir daño
            self.invulnerability_timer = 60  # 1 segundo de invulnerabilidad
            self.hit_flash_timer = 30        # 30 frames de parpadeo
            print(f"¡Vida perdida! Vidas restantes: {self.lives}")  # Debug educativo
            return self.lives > 0
    
    def reset_position(self):
        """Vuelve al jugador a su posición inicial."""
        self.rect.x = PLAYER_START_X
        self.rect.y = PLAYER_START_Y

    def restore_life(self, amount=1):
        """
        🍎 Restaura vidas al jugador (para cuando recoge una manzana).
        
        - Limita la vida al máximo (PLAYER_LIVES).
        - Devuelve cuántas vidas se restauraron realmente.
        
        💡 Cómo usar (ejemplo de colisión):
            if player.rect.colliderect(apple.rect):
                player.restore_life(1)
        """
        prev = self.lives
        self.lives = min(self.lives + amount, PLAYER_LIVES)

        restored = self.lives - prev
        if restored > 0:
            # ✅ Feedback visual simple (pequeño flash)
            self.hit_flash_timer = 10

            # ✅ SFX opcional (no rompe si no existe el archivo o el mixer)
            try:
                from utils import play_sound
                play_sound('assets/sfx/apple_pick.wav', volume=0.8)
            except Exception:
                pass

        return restored


class Apple:
    """
    🍎 CLASE APPLE - Representa una manzana que el jugador puede recoger.

    Atributos:
        rect: Posición y tamaño de la manzana en la pantalla.
        sprite: Imagen o color de la manzana.
    """

    def __init__(self, x, y, width=13, height=13):
        """
        Inicializa la manzana en la posición dada.
        """
        self.rect = pygame.Rect(x, y, width, height)

        # Intentar cargar sprite
        sprite_path = os.path.join("assets", "sprites", "apple.png")
        try:
            self.sprite = pygame.image.load(sprite_path).convert_alpha()
            self.using_fallback = False
        except:
            self.sprite = None
            self.using_fallback = True
            print("🍎 Apple: Sprite no encontrado, usando rectángulo de fallback")

    def draw(self, screen):
        """Dibuja la manzana en la pantalla."""
        if self.using_fallback:
            pygame.draw.rect(screen, (255, 0, 0), self.rect)  # rojo como fallback
        else:
            screen.blit(self.sprite, self.rect.topleft)




class Obstacle:
    """
    🍖 CLASE OBSTACLE - Representa un cachopo (obstáculo) que cae
    
    📚 CONCEPTOS POO QUE APRENDERÁS:
    
    🎲 VARIEDAD EN OBJETOS:
    Aunque todos son "Obstacle", cada objeto puede ser diferente:
    - Unos son rápidos (fast)
    - Otros son grandes (big)  
    - Algunos son normales (normal)
    ¡Misma clase, comportamientos diferentes!
    
    🏗️ CONSTRUCTOR INTELIGENTE:
    El __init__ usa random.choice() para crear variedad automáticamente.
    Cada obstáculo que se crea es único y aleatorio.
    
    📦 ATRIBUTOS CLAVE:
    - rect: Posición y tamaño (fundamental para colisiones)
    - speed: Velocidad de caída (varía según el tipo)
    - obstacle_type: 'normal', 'fast' o 'big'
    - color: Color visual (diferente por tipo)
    
    ⚡ MÉTODOS PRINCIPALES:
    - update(): Se mueve hacia abajo cada frame
    - draw(): Se dibuja con efectos visuales
    
    🤔 PREGUNTA CLAVE:
    ¿Por qué no hacer 3 clases separadas (ObstaculoRapido, ObstaculoGrande)?
    Respuesta: Comparten mucho comportamiento común. Mejor usar tipos.
    
    🔍 Mejora sugerida: El método __init__ es largo. Se podría dividir en 
    métodos como _setup_fast_obstacle(), _setup_big_obstacle().
    """
    
    def __init__(self, difficulty_multiplier=1.0):
        """
        🏗️ CONSTRUCTOR - Crea un obstáculo aleatorio
        
        📚 CONCEPTOS IMPORTANTES:
        - Parámetros opcionales: difficulty_multiplier=1.0
        - random.choice(): Selección aleatoria de tipos
        - Lógica condicional: if/elif/else para comportamientos diferentes
        - Cálculos matemáticos: Ajustar velocidad según dificultad
        
        Args:
            difficulty_multiplier: Multiplicador de dificultad (por defecto 1.0)
        """
        
        # 📍 POSICIÓN INICIAL - Aparece arriba en X aleatoria
        start_x = random.randint(0, WINDOW_WIDTH - OBSTACLE_WIDTH)
        start_y = -OBSTACLE_HEIGHT  # Arriba de la pantalla (invisible al inicio)
        
        self.rect = pygame.Rect(start_x, start_y, OBSTACLE_WIDTH, OBSTACLE_HEIGHT)
        
        # 🎲 TIPO ALEATORIO - ¡Aquí está la magia de la variedad!
        self.obstacle_type = random.choice(['normal', 'fast', 'big'])
        
        # ⚙️ CONFIGURACIÓN SEGÚN TIPO - Cada tipo tiene características únicas
        if self.obstacle_type == 'fast':
            self.speed = int(OBSTACLE_SPEED * 1.5 * difficulty_multiplier)
            self.color = RED
            # Los rápidos son más pequeños (más difíciles de esquivar)
            self.rect.width = OBSTACLE_WIDTH - 5
            self.rect.height = OBSTACLE_HEIGHT - 5
            
        elif self.obstacle_type == 'big':
            self.speed = int(OBSTACLE_SPEED * 0.7 * difficulty_multiplier)
            # Los grandes son más lentos pero más difíciles de esquivar
            self.rect.width = OBSTACLE_WIDTH + 15
            self.rect.height = OBSTACLE_HEIGHT + 15
            self.color = (150, 0, 0)  # Rojo más oscuro
            
        else:  # 'normal'
            self.speed = int(OBSTACLE_SPEED * difficulty_multiplier)
            self.color = OBSTACLE_COLOR
        
        # === CARGA DE SPRITE PARA CACHOPO (OBSTÁCULO) ===
        # Intentar cargar sprite del cachopo
        sprite_path = os.path.join("assets", "sprites", "cachopo_pixelart.png")
        self.sprite, self.using_fallback = load_sprite_with_fallback(
            sprite_path, 
            self.color,  # Color fallback específico del tipo
            self.rect.width, 
            self.rect.height
        )
        
        # ✅ IMPLEMENTADO: Efectos visuales
        self.rotation = 0  # Para rotación visual
        self.pulse_timer = random.randint(0, 60)  # Para efecto de pulso
        
        # Debug info para desarrollo
        if self.using_fallback:
            print(f"🍖 Obstacle ({self.obstacle_type}): Usando rectángulo fallback")
        else:
            print(f"🍖 Obstacle ({self.obstacle_type}): Sprite cargado desde", sprite_path)
    
    def update(self):
        """
        Actualiza la posición del obstáculo (lo hace caer).
        
        Returns:
            bool: False si el obstáculo salió de la pantalla, True si sigue visible
        """
        
        self.rect.y += self.speed
        
        # ✅ IMPLEMENTADO: Actualizar efectos visuales
        self.rotation += 2  # Rotación lenta para efecto visual
        self.pulse_timer += 1
        
        # Retorna False si salió de la pantalla (por abajo)
        return self.rect.top < WINDOW_HEIGHT
    
    def draw(self, screen):
        """Dibuja el obstáculo en la pantalla sin efectos extra."""
        
        if self.using_fallback:
            # Solo un rectángulo liso del color correspondiente
            pygame.draw.rect(screen, self.color, self.rect)
        else:
            # Solo el sprite, sin líneas, ni bordes, ni indicadores
            screen.blit(self.sprite, self.rect)


class Knife:
    """
    Esta clase representa un cuchillo lanzado por el jugador.
    
    Los cuchillos se mueven hacia arriba y pueden destruir obstáculos.
    Desaparecen cuando salen de la pantalla por arriba.
    """
    
    def __init__(self, player_rect):
        """
        Constructor del cuchillo. Aparece en la posición del jugador.
        
        Args:
            player_rect: Rectángulo del jugador para saber dónde aparecer
        """
        
        # El cuchillo aparece en el centro superior del jugador
        start_x = player_rect.centerx - KNIFE_WIDTH // 2
        start_y = player_rect.top
        
        self.rect = pygame.Rect(start_x, start_y, KNIFE_WIDTH, KNIFE_HEIGHT)
        self.speed = KNIFE_SPEED
        
        # === CARGA DE SPRITE PARA CUCHILLO ===
        # Intentar cargar sprite del cuchillo
        sprite_path = os.path.join("assets", "sprites", "knife__pixelart.png")
        self.sprite, self.using_fallback = load_sprite_with_fallback(
            sprite_path, 
            KNIFE_COLOR,  # Color fallback
            KNIFE_WIDTH, 
            KNIFE_HEIGHT
        )
        
        # Efectos visuales para el cuchillo
        self.rotation = 0  # Para rotación durante el vuelo
        
        # Debug info para desarrollo
        if self.using_fallback:
            print("🔪 Knife: Usando rectángulo fallback (imagen no encontrada)")
        else:
            print("🔪 Knife: Sprite cargado exitosamente desde", sprite_path)
    
    def update(self):
        """
        Actualiza la posición del cuchillo (lo hace subir).
        
        Returns:
            bool: False si el cuchillo salió de la pantalla, True si sigue visible
        """
        
        self.rect.y -= self.speed
        
        # Efecto de rotación durante el vuelo
        self.rotation += 10  # Rotación rápida para efecto dinámico
        
        # Retorna False si salió de la pantalla (por arriba)
        return self.rect.bottom > 0
    
    def draw(self, screen):
        """Dibuja el cuchillo en la pantalla."""
        
        # === RENDERIZADO DE SPRITE O FALLBACK ===
        if self.using_fallback:
            # Dibujar rectángulo fallback
            pygame.draw.rect(screen, KNIFE_COLOR, self.rect)
            
            # Añadir una punta para que parezca más un cuchillo
            tip_points = [(self.rect.centerx, self.rect.top - 3),
                        (self.rect.left + 2, self.rect.top + 3),
                        (self.rect.right - 2, self.rect.top + 3)]
            pygame.draw.polygon(screen, KNIFE_COLOR, tip_points)
            
        else:
            # === RENDERIZADO DE SPRITE REAL ===
            sprite_to_draw = self.sprite
            
            # Aplicar rotación al sprite
            if self.rotation != 0:
                # Rotar sprite alrededor de su centro
                sprite_to_draw = pygame.transform.rotate(self.sprite, self.rotation)
                
                # Calcular nueva posición para que el centro se mantenga
                old_center = self.rect.center
                new_rect = sprite_to_draw.get_rect()
                new_rect.center = old_center
                
                # Dibujar sprite rotado
                screen.blit(sprite_to_draw, new_rect)
            else:
                # Dibujar sprite normal
                screen.blit(sprite_to_draw, self.rect)

class PowerUp:
    """
    Representa un power-up (vodka, tea, honey, apple, navidad).
    Caen desde arriba, con pequeños efectos visuales.
    """

    def __init__(self, powerup_type):
        # ----- Tamaño según tipo -----
        if powerup_type == 'tea':
            self.width, self.height = 100, 80
        elif powerup_type == 'navidad':
            self.width, self.height = 120, 120  # un pelín más grande para destacar
        else:
            self.width, self.height = POWERUP_WIDTH, POWERUP_HEIGHT

        # ----- Posición inicial -----
        start_x = random.randint(0, WINDOW_WIDTH - self.width)
        start_y = -self.height
        self.rect = pygame.Rect(start_x, start_y, self.width, self.height)

        self.type = powerup_type
        self.speed = POWERUP_SPEED

        # ----- Color/símbolo + sprite path -----
        if powerup_type == 'vodka':
            self.color = VODKA_COLOR
            self.symbol = "V"
            sprite_path = os.path.join("assets", "sprites", "vodka_pixelart.png")
            fallback_color = self.color

        elif powerup_type == 'tea':
            self.color = TEA_COLOR           # solo para texto
            self.symbol = "T"
            sprite_path = os.path.join("assets", "sprites", "tea_pixelart.png")
            fallback_color = self.color      # color del rect si no hay sprite

        elif powerup_type == 'honey':
            self.color = HONEY_COLOR
            self.symbol = "H"
            sprite_path = os.path.join("assets", "sprites", "honey_pixelart.png")
            fallback_color = self.color

        elif powerup_type == 'apple':
            self.color = (255, 0, 0)         # Rojo (fallback y texto)
            self.symbol = "A"
            sprite_path = os.path.join("assets", "sprites", "apple.png")
            fallback_color = self.color

        elif powerup_type == 'navidad':
            self.color = (255, 0, 0)
            self.symbol = "X"
            sprite_path = os.path.join("assets", "sprites", "navidad.png")
            fallback_color = self.color
            
        elif powerup_type == 'grinch':
            self.color = (0, 200, 0)
            self.symbol = "G"
            sprite_path = os.path.join("assets", "sprites", "grinch.png")
            fallback_color = self.color

        else:
            raise ValueError(f"Tipo de power-up desconocido: {powerup_type}")

        # ----- Cargar sprite (una sola vez) -----
        self.sprite, self.using_fallback = load_sprite_with_fallback(
            sprite_path,
            fallback_color,
            self.width,
            self.height
        )

        # ----- Efectos visuales -----
        self.pulse_timer = 0
        self.float_offset = 0.0
        self.sparkle_timer = 0
        self.original_y = start_y

        if self.using_fallback:
            print(f"🍺 PowerUp ({powerup_type}): Usando rectángulo fallback")
        else:
            print(f"🍺 PowerUp ({powerup_type}): Sprite cargado desde", sprite_path)

        # Compatibilidad de blend flag entre versiones de pygame
        self.BLEND_TINT = getattr(
            pygame, "BLEND_ALPHA_SDL2",
            getattr(pygame, "BLEND_RGBA_ADD", 0)
        )

    def apply_effect(self, player):
        """
        Aplica el efecto del power-up sobre el jugador.
        (Ahora mismo no la usamos porque la lógica está en main, pero la dejamos preparada)
        """
        if self.type == 'apple':
            max_lives = getattr(player, "max_lives", PLAYER_LIVES)
            if player.lives < max_lives:
                player.lives += 1
            print(f"🍎 Apple: vidas → {player.lives}/{max_lives}")

        elif self.type == 'vodka':
            # Aquí podrías llamar a powerup_effects.activate_vodka_boost(player)
            pass

        elif self.type == 'tea':
            player.has_shield = True

        elif self.type == 'honey':
            player.honey_timer = 180

    def update(self):
        """
        Actualiza posición y timers visuales.
        Returns:
            bool: True si sigue en pantalla, False si salió
        """
        self.rect.y += self.speed
        self.pulse_timer += 1
        self.sparkle_timer += 1

        # flotación ligera (usa int para evitar warnings)
        self.float_offset = (
            pygame.math.Vector2(1, 0).rotate(self.pulse_timer * 3).y * 2
        )
        return self.rect.top < WINDOW_HEIGHT

    def draw(self, screen):
        """
        Dibuja el power-up con efectos (pulso, brillo, etc.).
        (Sin tinte raro extra para el té, solo sprite normal + pulso).
        """
        # aplicar offset de flotación (rect independiente para el render)
        draw_rect = pygame.Rect(
            self.rect.x,
            int(self.rect.y + self.float_offset),
            self.rect.width,
            self.rect.height
        )

        if self.using_fallback:
            pulse_intensity = abs(
                pygame.math.Vector2(1, 0).rotate(self.pulse_timer * POWERUP_PULSE_SPEED).x
            )
            base_color = self.color
            pulse_color = tuple(
                int(c * (0.7 + 0.3 * pulse_intensity)) for c in base_color
            )

            pygame.draw.rect(screen, pulse_color, draw_rect)
            border_color = tuple(min(255, c + 50) for c in base_color)
            pygame.draw.rect(screen, border_color, draw_rect, 2)

            font = pygame.font.Font(None, 20)
            text = font.render(self.symbol, True, WHITE)
            screen.blit(text, text.get_rect(center=draw_rect.center))

        else:
            # pulso por escala
            pulse_intensity = abs(
                pygame.math.Vector2(1, 0).rotate(self.pulse_timer * POWERUP_PULSE_SPEED).x
            )
            scale_factor = 0.9 + 0.2 * pulse_intensity
            sprite_to_draw = self.sprite

            if scale_factor != 1.0:
                scaled_size = (
                    int(self.rect.width * scale_factor),
                    int(self.rect.height * scale_factor)
                )
                sprite_to_draw = pygame.transform.scale(self.sprite, scaled_size)
                scaled_rect = sprite_to_draw.get_rect(center=draw_rect.center)
                screen.blit(sprite_to_draw, scaled_rect)
            else:
                screen.blit(sprite_to_draw, draw_rect)

        # # brillo ocasional
        # if self.sparkle_timer % 30 < 5:
        #     sparkle_points = [
        #         (draw_rect.centerx, draw_rect.top - 3),
        #         (draw_rect.right + 3, draw_rect.centery),
        #         (draw_rect.centerx, draw_rect.bottom + 3),
        #         (draw_rect.left - 3, draw_rect.centery),
        #     ]
        #     for p in sparkle_points:
        #         pygame.draw.circle(screen, WHITE, p, 1)

    
    
    
    
class PowerUpEffect:
    """
    Esta clase gestiona los efectos temporales de los power-ups.
    
    Cuando el jugador recoge un power-up, se activa un efecto que dura
    un tiempo determinado. Esta clase maneja la duración y el estado
    de estos efectos.
    """
    
    def __init__(self):
        """Constructor del sistema de efectos de power-ups."""
        # Timers para cada tipo de power-up (en frames)
        self.vodka_timer = 0      # Frames restantes del efecto Vodka Boost
        self.tea_timer = 0        # Frames restantes del efecto Té Mágico
        
        # Estado original del jugador (para restaurar después)
        self.original_speed = PLAYER_SPEED
    
    def activate_vodka_boost(self, player):
        """
        Activa el efecto Vodka Boost (aumenta velocidad).
        
        Args:
            player: Instancia del jugador para modificar su velocidad
        """
        self.vodka_timer = VODKA_DURATION
        
        # Aumentar la velocidad del jugador
        player.speed = int(self.original_speed * VODKA_SPEED_MULTIPLIER)
        print("¡Vodka Boost activado! Velocidad aumentada.")  # Debug
    
    def activate_tea_shield(self, player):
        """
        Activa el efecto Té Mágico (escudo protector).
        
        Args:
            player: Instancia del jugador para darle el escudo
        """
        self.tea_timer = TEA_DURATION
        
        # Activar escudo
        player.has_shield = True
        print("¡Té Mágico activado! Escudo protector obtenido.")  # Debug
    
    def update(self, player):
        """
        Actualiza todos los efectos activos (llamar cada frame).
        
        Args:
            player: Instancia del jugador para modificar sus atributos
        """
        # Actualizar Vodka Boost
        if self.vodka_timer > 0:
            self.vodka_timer -= 1
            
            # Si el efecto termina, restaurar velocidad normal
            if self.vodka_timer == 0:
                player.speed = self.original_speed
                print("Vodka Boost terminado. Velocidad normal restaurada.")  # Debug
        
        # Actualizar Té Mágico
        if self.tea_timer > 0:
            self.tea_timer -= 1
            
            # Si el efecto termina, quitar escudo
            if self.tea_timer == 0:
                player.has_shield = False
                print("Té Mágico terminado. Escudo desactivado.")  # Debug
    
    def is_vodka_active(self):
        """Comprueba si el efecto Vodka Boost está activo."""
        return self.vodka_timer > 0
    
    def is_tea_active(self):
        """Comprueba si el efecto Té Mágico está activo."""
        return self.tea_timer > 0
    
    def get_vodka_time_left(self):
        """Obtiene el tiempo restante del Vodka Boost en segundos."""
        return self.vodka_timer / FPS
    
    def get_tea_time_left(self):
        """Obtiene el tiempo restante del Té Mágico en segundos."""
        return self.tea_timer / FPS
    
    # ✅ Método antiguo: efectos activos en la HUD (si algún día lo quieres usar otra vez)
    def draw_active_effects(self, screen, font):
        """
        Dibuja los efectos activos en la pantalla (HUD lateral).
        """
        y_offset = 140  # Posición inicial (debajo de la barra de cooldown)
        
        if self.is_vodka_active():
            time_left = f"⚡ Vodka Boost: {self.get_vodka_time_left():.1f}s"
            text = font.render(time_left, True, VODKA_COLOR)
            
            text_rect = text.get_rect()
            text_rect.x = 10
            text_rect.y = y_offset
            
            background_rect = pygame.Rect(text_rect.x - 2, text_rect.y - 2,
                                          text_rect.width + 4, text_rect.height + 4)
            pygame.draw.rect(screen, BLACK, background_rect)
            pygame.draw.rect(screen, VODKA_COLOR, background_rect, 1)
            
            screen.blit(text, text_rect)
            y_offset += 25
        
        if self.is_tea_active():
            time_left = f"🛡️ Té Mágico: {self.get_tea_time_left():.1f}s"
            text = font.render(time_left, True, TEA_COLOR)
            
            text_rect = text.get_rect()
            text_rect.x = 10
            text_rect.y = y_offset
            
            background_rect = pygame.Rect(text_rect.x - 2, text_rect.y - 2,
                                          text_rect.width + 4, text_rect.height + 4)
            pygame.draw.rect(screen, BLACK, background_rect)
            pygame.draw.rect(screen, TEA_COLOR, background_rect, 1)
            
            screen.blit(text, text_rect)
            y_offset += 25

    # ✅ NUEVO: mensajes debajo del jugador
    def draw_active_effects_near_player(self, screen, player, font):
        """
        Dibuja mensajes de efectos activos debajo del jugador.
        """
        messages = []

        # Vodka → velocidad
        if self.is_vodka_active():
            messages.append(("¡VELOCIDAD AUMENTADA!", VODKA_COLOR))

        # Té → escudo
        if self.is_tea_active() or getattr(player, "has_shield", False):
            messages.append(("¡ESCUDO ACTIVO!", TEA_COLOR))

        # Miel → más lento (usamos honey_timer del player)
        if getattr(player, "honey_timer", 0) > 0:
            messages.append(("¡TE MUEVES MÁS LENTO!", HONEY_COLOR))

        if not messages:
            return

        # Posición base: debajo del jugador
        base_x = player.rect.centerx
        base_y = player.rect.bottom + 10

        for i, (msg, color) in enumerate(messages):
            text_surf = font.render(msg, True, color)
            text_rect = text_surf.get_rect(
                midtop=(base_x, base_y + i * (text_surf.get_height() + 4))
            )

            # Fondo para legibilidad
            bg_rect = pygame.Rect(
                text_rect.x - 4,
                text_rect.y - 2,
                text_rect.width + 8,
                text_rect.height + 4,
            )
            pygame.draw.rect(screen, BLACK, bg_rect)
            pygame.draw.rect(screen, color, bg_rect, 1)

            screen.blit(text_surf, text_rect)


# ✅ IMPLEMENTADO: Clase Enemy para enemigos más complejos
class Enemy(Obstacle):
    """
    Enemigo que se mueve de forma más inteligente que un obstáculo simple.
    Hereda de Obstacle y puede seguir al jugador.
    """
    
    def __init__(self, player_x, difficulty_multiplier=1.0):
        """
        Constructor del enemigo.
        
        Args:
            player_x: Posición X del jugador para seguimiento
            difficulty_multiplier: Multiplicador de dificultad
        """
        super().__init__(difficulty_multiplier)  # Inicializa Obstacle
        
        # Guardar posición inicial generada por Obstacle
        old_center = self.rect.center
        
        # Intentar cargar sprite
        try:
            self.image = pygame.image.load("assets/sprites/calero.png").convert_alpha()
            # Escalar imagen a tamaño más pequeño (80x80)
            self.image = pygame.transform.scale(self.image, (80, 80))
        except Exception as e:
            print("⚠️ Error al cargar sprite de Enemy:", e)
            # Fallback: superficie simple si falla
            self.image = pygame.Surface((80, 80))
            self.image.fill((150, 0, 150))
        
        # Ajustar rect al tamaño de la imagen pero mantener posición inicial
        self.rect = self.image.get_rect()
        self.rect.center = old_center
        
        # Configuración específica del enemigo
        self.obstacle_type = 'enemy'
        self.target_x = player_x    # Posición objetivo (jugador)
        self.horizontal_speed = 1   # Velocidad de seguimiento horizontal

    def update(self, player_x):
        """
        Actualizar enemigo con seguimiento del jugador.
        
        Args:
            player_x: Posición X actual del jugador
        """
        # Actualizar posición vertical
        self.rect.y += self.speed
        
        # Seguimiento horizontal del jugador
        self.target_x = player_x
        if self.rect.centerx < self.target_x:
            self.rect.x += self.horizontal_speed
        elif self.rect.centerx > self.target_x:
            self.rect.x -= self.horizontal_speed
        
        # Mantener dentro de los límites de pantalla
        self.rect.left = max(0, self.rect.left)
        self.rect.right = min(WINDOW_WIDTH, self.rect.right)
        
        # Efectos visuales
        self.rotation += 3
        self.pulse_timer += 1
        
        return self.rect.top < WINDOW_HEIGHT
    
    def draw(self, screen):
        """Dibujar enemigo con sprite y efectos visuales."""
        
        # Dibujar sprite principal
        screen.blit(self.image, self.rect.topleft)
        
        # # Indicador de que es un enemigo (ojos)
        # eye_size = 3
        # left_eye = (self.rect.left + 6, self.rect.top + 6)
        # right_eye = (self.rect.right - 6, self.rect.top + 6)
        # pygame.draw.circle(screen, WHITE, left_eye, eye_size)
        # pygame.draw.circle(screen, WHITE, right_eye, eye_size)
        # pygame.draw.circle(screen, RED, left_eye, 1)
        # pygame.draw.circle(screen, RED, right_eye, 1)
        
        # Borde amenazante
        # pygame.draw.rect(screen, RED, self.rect, 2)



# ✅ IMPLEMENTADO: Clase Explosion para efectos visuales
class Explosion:
    """
    Efecto visual cuando se destruye un obstáculo.
    
    Esta clase demuestra cómo crear efectos temporales que se
    dibujan durante un tiempo limitado y luego desaparecen.
    """
    
    def __init__(self, x, y, color=YELLOW):
        """
        Constructor de la explosión.
        
        Args:
            x, y: Posición central de la explosión
            color: Color base de la explosión
        """
        self.x = x
        self.y = y
        self.color = color
        self.particles = []
        self.life = PARTICLE_LIFE  # Vida total del efecto
        
        # ✅ IMPLEMENTADO: Crear partículas individuales
        for _ in range(PARTICLE_COUNT):
            # Cada partícula tiene posición, velocidad y tamaño aleatorio
            angle = random.uniform(0, 2 * 3.14159)  # Ángulo aleatorio
            speed = random.uniform(2, 8)             # Velocidad aleatoria
            
            particle = {
                'x': x,
                'y': y,
                'vel_x': pygame.math.Vector2(speed, 0).rotate_rad(angle).x,
                'vel_y': pygame.math.Vector2(speed, 0).rotate_rad(angle).y,
                'size': random.randint(2, 5),
                'life': random.randint(15, PARTICLE_LIFE)
            }
            self.particles.append(particle)
    
    def update(self):
        """
        Actualizar todas las partículas de la explosión.
        
        Returns:
            bool: False si la explosión terminó, True si sigue activa
        """
        self.life -= 1
        
        # Actualizar cada partícula
        for particle in self.particles[:]:  # [:] para iterar copia segura
            particle['x'] += particle['vel_x']
            particle['y'] += particle['vel_y']
            particle['life'] -= 1
            
            # Aplicar gravedad y fricción
            particle['vel_y'] += 0.2  # Gravedad
            particle['vel_x'] *= 0.98  # Fricción
            
            # Eliminar partículas que expiraron
            if particle['life'] <= 0:
                self.particles.remove(particle)
        
        # La explosión termina cuando no quedan partículas o se acaba el tiempo
        return len(self.particles) > 0 and self.life > 0
    
    def draw(self, screen):
        """Dibujar todas las partículas de la explosión."""
        for particle in self.particles:
            # Color que se desvanece con el tiempo
            alpha_factor = particle['life'] / PARTICLE_LIFE
            particle_color = tuple(int(c * alpha_factor) for c in self.color)
            
            # Dibujar partícula como círculo
            pygame.draw.circle(screen, particle_color, 
                             (int(particle['x']), int(particle['y'])), 
                             particle['size'])


# ✅ IMPLEMENTADO: Clase para efectos de pantalla
class ScreenEffect:
    """
    Efectos que afectan a toda la pantalla como screen shake.
    """
    
    def __init__(self):
        """Constructor del sistema de efectos de pantalla."""
        self.shake_intensity = 0
        self.shake_duration = 0
        self.shake_offset_x = 0
        self.shake_offset_y = 0
    
    def start_screen_shake(self, intensity=SCREEN_SHAKE_INTENSITY, duration=SCREEN_SHAKE_DURATION):
        """
        Iniciar efecto de screen shake.
        
        Args:
            intensity: Intensidad del temblor
            duration: Duración en frames
        """
        self.shake_intensity = intensity
        self.shake_duration = duration
    
    def update(self):
        """Actualizar efectos de pantalla."""
        if self.shake_duration > 0:
            self.shake_duration -= 1
            
            # Calcular offset aleatorio para el shake
            if self.shake_duration > 0:
                self.shake_offset_x = random.randint(-self.shake_intensity, self.shake_intensity)
                self.shake_offset_y = random.randint(-self.shake_intensity, self.shake_intensity)
            else:
                self.shake_offset_x = 0
                self.shake_offset_y = 0
    
    def get_screen_offset(self):
        """
        Obtener el offset actual de la pantalla.
        
        Returns:
            tuple: (offset_x, offset_y) para aplicar a la cámara
        """
        return (self.shake_offset_x, self.shake_offset_y)


# TODO 8: Crear clase Enemy para enemigos más complejos
# class Enemy(Obstacle):
#     """Enemigo que se mueve de forma más inteligente que un obstáculo simple."""
#     pass

# TODO 9: Crear clase Explosion para efectos visuales
# class Explosion:
#     """Efecto visual cuando se destruye un obstáculo."""
#     pass

# === NOTAS EDUCATIVAS ===
"""
Conceptos importantes de POO demostrados aquí:

1. ENCAPSULACIÓN: Cada clase mantiene sus propios datos (atributos)
   y los métodos que operan sobre esos datos.

2. RESPONSABILIDAD ÚNICA: Cada clase tiene una responsabilidad clara:
   - Player: Gestionar al jugador
   - Obstacle: Gestionar obstáculos
   - Knife: Gestionar proyectiles
   - PowerUp: Gestionar power-ups

3. PYGAME.RECT: Usamos pygame.Rect para:
   - Posición (x, y)
   - Tamaño (width, height)
   - Detección de colisiones
   - Límites de pantalla

4. MÉTODOS COMUNES: Todas las entidades móviles tienen:
   - update(): Actualizar lógica
   - draw(): Dibujar en pantalla

5. CONSTRUCTOR (__init__): Inicializa el estado de cada objeto
   cuando se crea una nueva instancia.

Para estudiantes: Experimenten cambiando los valores en settings.py
y vean cómo afecta el comportamiento de estas clases.
"""