"""
game_states.py - Estados del juego Julia's Run

Este archivo gestiona los diferentes estados o pantallas del juego:
- Menú principal
- Jugando
- Game Over
- Pausa (TODO)

Conceptos de programación cubiertos:
- Máquina de estados
- Gestión de eventos
- Renderizado condicional
- Flujo de control del programa

Referencias útiles:
- pygame.font: https://www.pygame.org/docs/ref/font.html
- pygame.event: https://www.pygame.org/docs/ref/event.html
"""

import pygame

pygame.mixer.pre_init(frequency=44100, size=-16, channels=2, buffer=512)
pygame.init()

from settings import *
class GameStateManager:
    """
    Esta clase gestiona los diferentes estados del juego.
    
    Un juego típicamente tiene varios estados o pantallas:
    - Menú principal
    - Gameplay
    - Game Over
    - Pausa
    
    Esta clase se encarga de cambiar entre estos estados y
    asegurarse de que solo uno esté activo a la vez.
    """
    
    def __init__(self):
        """Constructor del gestor de estados."""
        self.current_state = STATE_MENU
        self.next_state = None
        
        # Inicializar fuentes para texto
        pygame.font.init()
        self.font_large = pygame.font.Font(None, FONT_SIZE_LARGE)
        self.font_medium = pygame.font.Font(None, FONT_SIZE_MEDIUM)
        self.font_small = pygame.font.Font(None, FONT_SIZE_SMALL)
        
         # 🎵 Música de fondo
        pygame.mixer.music.load(MUSIC_BACKGROUND)
        pygame.mixer.music.set_volume(0.2)  # 0.0 - 1.0
        pygame.mixer.music.play(-1)         # -1 = bucle      
    
    def change_state(self, new_state):
        """
        Cambia a un nuevo estado.
        
        Args:
            new_state: El nuevo estado (ver constantes en settings.py)
        """
        self.next_state = new_state
    
    def update_state(self):
        """Actualiza el estado actual si hay un cambio pendiente."""
        if self.next_state:
            self.current_state = self.next_state
            self.next_state = None
    
    def get_current_state(self):
        """Obtiene el estado actual."""
        return self.current_state


import os
import pygame

class MenuState:
    """
    Estado del menú principal.
    
    Muestra el título del juego, instrucciones básicas y
    espera a que el jugador presione una tecla para empezar.
    """
    
    def __init__(self, state_manager):
        """
        Constructor del estado de menú.
        
        Args:
            state_manager: Referencia al gestor de estados
        """
        self.state_manager = state_manager

        # ====== FONDO ANIMADO ======
        self.bg_frames = []
        frames_path = "assets/sprites/animated"

        # Cargar todos los PNG de la carpeta como frames
        if os.path.isdir(frames_path):
            for filename in sorted(os.listdir(frames_path)):
                if filename.lower().endswith(".png"):
                    full_path = os.path.join(frames_path, filename)
                    img = pygame.image.load(full_path).convert()

                    # Escalar la imagen para cubrir toda la ventana (tipo 'cover')
                    bg_width, bg_height = img.get_size()
                    scale_factor = max(WINDOW_WIDTH / bg_width, WINDOW_HEIGHT / bg_height)
                    new_size = (int(bg_width * scale_factor), int(bg_height * scale_factor))
                    img = pygame.transform.scale(img, new_size)

                    self.bg_frames.append(img)

        # Índice y velocidad de animación
        self.bg_frame_index = 0
        self.bg_anim_speed = 150  # ms por frame (como tu GIF)
        # =============================

        # ====== LOGO DEL JUEGO ======
        # Asegúrate de que este archivo existe: assets/sprites/logo.png
        self.logo_image = pygame.image.load("assets/sprites/logo.png").convert_alpha()

        # Escalar el logo si es demasiado grande
        max_logo_width = int(WINDOW_WIDTH * 0.3)
        logo_w, logo_h = self.logo_image.get_size()
        if logo_w > max_logo_width:
            scale_factor = max_logo_width / logo_w
            new_size = (int(logo_w * scale_factor), int(logo_h * scale_factor))
            self.logo_image = pygame.transform.scale(self.logo_image, new_size)
        # ============================
    
    def handle_events(self, events):
        """
        Maneja los eventos del menú.
        
        Args:
            events: Lista de eventos de pygame
        """
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == KEY_SPACE or event.key == KEY_ENTER:
                    self.state_manager.change_state(STATE_PLAYING)
                elif event.key == KEY_ESCAPE:
                    return False  # Señal para salir del juego
        
        return True  # Continuar ejecutando
    
    def update(self):
        """Actualiza la lógica del menú (animación del fondo)."""
        if self.bg_frames:
            current_time = pygame.time.get_ticks()
            # Cambia de frame cada bg_anim_speed ms
            self.bg_frame_index = (current_time // self.bg_anim_speed) % len(self.bg_frames)
    
    def draw(self, screen):
        """
        Dibuja el menú principal.
        
        Args:
            screen: Superficie de pygame donde dibujar
        """
        # ====== DIBUJAR FONDO ANIMADO ======
        if self.bg_frames:
            background_image = self.bg_frames[self.bg_frame_index]
            bg_width, bg_height = background_image.get_size()
            bg_x = (WINDOW_WIDTH - bg_width) // 2
            bg_y = (WINDOW_HEIGHT - bg_height) // 2
            screen.blit(background_image, (bg_x, bg_y))
        else:
            # Fallback si no hay frames
            screen.fill(LIGHT_BLUE)
        # ===================================

        # ====== LOGO DEL JUEGO (en vez de texto) ======
        logo_rect = self.logo_image.get_rect(center=(WINDOW_WIDTH // 2, 150))
        screen.blit(self.logo_image, logo_rect)
        # ==============================================
        
        # ====== PANEL GLASS PARA CONTROLES ======
        instructions = [
            "Controles:",
            "¡Usa las flechas para mover a la rusa!",
            "La barra espaciadora para lanzar cuchillos",
            "¡Esquiva los cachopos!",
            "El vodka te dará velocidad, el té un escudo",
            "¡Pero cuidado con la miel!",
            "",
            "Presiona ESPACIO para comenzar",
            "ESC para salir"
        ]

        MARGIN_X = 50
        start_y = 280
        line_h = self.state_manager.font_small.get_linesize()
        padding_x = 16
        padding_y = 14

        panel_w = int(WINDOW_WIDTH * 0.31)  # ancho del panel (ajustable)
        panel_h = padding_y * 2 + line_h * len(instructions)
        panel_rect = pygame.Rect(MARGIN_X - padding_x, start_y - padding_y, panel_w, panel_h)

        # 1) "Falso blur" del fondo bajo el panel (downscale -> upscale)
        sub = screen.subsurface(panel_rect).copy()
        small = pygame.transform.smoothscale(sub, (max(1, panel_rect.w // 8), max(1, panel_rect.h // 8)))
        blurred = pygame.transform.smoothscale(small, (panel_rect.w, panel_rect.h))
        screen.blit(blurred, panel_rect.topleft)

        # 2) Capa translúcida blanca con esquinas redondeadas
        glass = pygame.Surface((panel_rect.w, panel_rect.h), pygame.SRCALPHA)
        pygame.draw.rect(glass, (255, 255, 255, 70), glass.get_rect(), border_radius=18)  # “vidrio” suave
        # 3) Borde sutil
        pygame.draw.rect(glass, (255, 255, 255, 120), glass.get_rect(), width=1, border_radius=18)
        # 4) Highlight superior (brillito)
        highlight = pygame.Surface((panel_rect.w, panel_rect.h // 3), pygame.SRCALPHA)
        pygame.draw.rect(highlight, (255, 255, 255, 60), highlight.get_rect(), border_radius=18)
        glass.blit(highlight, (0, 0))
        # 5) Sombra ligera (opcional)
        shadow = pygame.Surface((panel_rect.w + 12, panel_rect.h + 12), pygame.SRCALPHA)
        pygame.draw.rect(shadow, (0, 0, 0, 80), shadow.get_rect(), border_radius=22)
        screen.blit(shadow, (panel_rect.x - 6, panel_rect.y - 6))
        # 6) Blit final del panel glass
        screen.blit(glass, panel_rect.topleft)

        # 7) Título y líneas alineadas a la izquierda dentro del panel
        x_text = panel_rect.x + padding_x
        y_text = panel_rect.y + padding_y

        for i, instruction in enumerate(instructions):
            color = BLACK if instruction != "" else (0, 0, 0, 0)  # no dibujar texto en vacío
            if instruction:  # evita imprimir la línea vacía
                surf = self.state_manager.font_small.render(instruction, True, color)
                screen.blit(surf, (x_text, y_text + i * line_h))


class PlayingState:
    """
    Estado principal del juego.
    
    Este es el estado donde ocurre toda la acción:
    - El jugador se mueve y lanza cuchillos
    - Aparecen obstáculos y power-ups
    - Se detectan colisiones
    - Se actualiza la puntuación
    """
    
    def __init__(self, state_manager):
        """Constructor del estado de juego."""
        self.state_manager = state_manager
        
        # 🔊 Cargar sonidos una sola vez
        self.snd_throw = pygame.mixer.Sound(SOUND_THROW)
        self.snd_hit = pygame.mixer.Sound(SOUND_HIT)
        self.snd_powerup = pygame.mixer.Sound(SOUND_POWERUP)

        # Sube un poco volumen por si la música tapa los FX
        self.snd_throw.set_volume(1.0)
        self.snd_hit.set_volume(1.0)
        self.snd_powerup.set_volume(1.0)
    
    def handle_events(self, events, player, knife_cooldown):
        new_knives = []
        
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == KEY_SPACE:
                    if knife_cooldown.is_ready():
                        from entities import Knife  # Import local para evitar circular
                        new_knife = Knife(player.rect)
                        new_knives.append(new_knife)
                        knife_cooldown.start_cooldown()
                        # pygame.mixer.Sound(SOUND_THROW).play()
                        self.snd_throw.play()
                
                elif event.key == KEY_P:
                    self.state_manager.change_state(STATE_PAUSED)
                    print("Juego pausado")  # Debug
                
                elif event.key == KEY_ESCAPE:
                    return new_knives, False  # Salir del juego
        
        return new_knives, True  # Continuar jugando
    
    def update(self, player, obstacles, knives, powerups, effects, knife_cooldown):
        """
        Actualiza toda la lógica del juego.
        """
        # Timers
        knife_cooldown.update()
        effects.update(player)
        
        # Mover jugador
        keys = pygame.key.get_pressed()
        player.move(keys)
        
        # Obstáculos
        for obstacle in obstacles[:]:
            if not obstacle.update():
                obstacles.remove(obstacle)
                player.score += POINTS_PER_OBSTACLE_AVOIDED
        
        # Cuchillos
        for knife in knives[:]:
            if not knife.update():
                knives.remove(knife)
        
        # Power-ups
        for powerup in powerups[:]:
            if not powerup.update():
                powerups.remove(powerup)
        
        # Colisiones jugador-obstáculos
        for obstacle in obstacles[:]:
            if player.rect.colliderect(obstacle.rect):
                if player.take_damage():
                    obstacles.remove(obstacle)
                else:
                    return False  # Game Over
                        
        # Colisiones cuchillo-obstáculos
        for knife in knives[:]:
            for obstacle in obstacles[:]:
                if knife.rect.colliderect(obstacle.rect):
                    knives.remove(knife)
                    obstacles.remove(obstacle)
                    player.score += POINTS_PER_OBSTACLE_DESTROYED
                    
                    # 🔊 Sonido de impacto
                    self.snd_hit.play()
                    # Debug opcional:
                    # print("HIT sonido disparado")
                    break
        
        # Colisiones jugador-powerups (incluye apple aquí)
        for powerup in powerups[:]:
            if player.rect.colliderect(powerup.rect):
                powerups.remove(powerup)
                player.score += POINTS_PER_POWERUP

                # 🔊 Sonido de power-up
                self.snd_powerup.play()
                # Debug opcional:
                # print("POWERUP sonido disparado:", powerup.type)
                
                if powerup.type == 'vodka':
                    effects.activate_vodka_boost(player)
                elif powerup.type == 'tea':
                    effects.activate_tea_shield(player)
                elif powerup.type == 'honey':
                    player.honey_timer = max(player.honey_timer, 240)
                elif powerup.type == 'apple':
                    player.lives += 1
                    print(f"🍎 Manzana recogida! Vidas: {player.lives}")


        
        return True  # Jugador sigue vivo
    
    def draw(self, screen, player, obstacles, knives, powerups, effects, knife_cooldown):
        """
        Dibuja todo el estado del juego.
        """
        # Limpiar
        screen.fill(BLACK)
        
        # Entidades
        player.draw(screen)
        for obstacle in obstacles:
            obstacle.draw(screen)
        for knife in knives:
            knife.draw(screen)
        for powerup in powerups:
            powerup.draw(screen)
        
        # HUD
        self.draw_hud(screen, player, effects, knife_cooldown)
    
    def draw_hud(self, screen, player, effects, knife_cooldown):
        """
        HUD (puntuación, vidas, etc.)
        """
        score_text = self.state_manager.font_medium.render(f"Puntuación: {player.score}", True, WHITE)
        screen.blit(score_text, (10, 10))
        
        lives_text = self.state_manager.font_medium.render(f"Vidas: {player.lives}", True, WHITE)
        screen.blit(lives_text, (10, 40))
        
        if player.has_shield:
            shield_text = self.state_manager.font_small.render("🛡️ ESCUDO ACTIVO", True, TEA_COLOR)
            screen.blit(shield_text, (10, 70))
        
        knife_cooldown.draw_cooldown_bar(screen)
        effects.draw_active_effects(screen, self.state_manager.font_small)

class GameOverState:
    """
    Estado de Game Over.
    
    Muestra la puntuación final, el récord y permite
    reiniciar el juego o volver al menú.
    """
    
    def __init__(self, state_manager):
        """Constructor del estado de Game Over."""
        self.state_manager = state_manager
        self.final_score = 0
        self.best_score = 0
        self.is_new_record = False

        # ===== FONDO ESTÁTICO (fallback) =====
        self.game_over_bg = pygame.image.load("assets/sprites/gameover.png").convert()
        self.game_over_bg = pygame.transform.scale(self.game_over_bg, (WINDOW_WIDTH, WINDOW_HEIGHT))
        # =====================================

        # ===== FONDO ANIMADO (precargado) =====
        self.bg_frames = []
        frames_path = "assets/sprites/gameover_animated"

        if os.path.isdir(frames_path):
            for filename in sorted(os.listdir(frames_path)):
                if filename.lower().endswith(".png"):
                    full_path = os.path.join(frames_path, filename)
                    img = pygame.image.load(full_path).convert()

                    # === RECORTAR LA PARTE INFERIOR (donde está la firma) ===
                    w, h = img.get_size()
                    crop_bottom = 60  # píxeles a recortar desde abajo (ajusta este valor)
                    if crop_bottom < h:
                        crop_rect = pygame.Rect(0, 0, w, h - crop_bottom)
                        img = img.subsurface(crop_rect)
                    # ========================================================

                    # Escalar la imagen recortada al tamaño de la ventana
                    img = pygame.transform.scale(img, (WINDOW_WIDTH, WINDOW_HEIGHT))
                    self.bg_frames.append(img)

                self.bg_frame_index = 0
                self.bg_anim_speed = 150  # ms por frame
        # ======================================
    
    def set_scores(self, final_score, best_score):
        """Establece las puntuaciones para mostrar."""
        self.final_score = final_score
        self.best_score = best_score
        self.is_new_record = final_score > best_score
    
    def handle_events(self, events):
        """Maneja los eventos en la pantalla de Game Over."""
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == KEY_ENTER:
                    self.state_manager.change_state(STATE_PLAYING)
                elif event.key == KEY_ESCAPE:
                    return False  # Salir del juego
        return True
    
    def update(self):
        """Actualiza la lógica del Game Over (animación de fondo)."""
        if self.bg_frames:
            current_time = pygame.time.get_ticks()
            self.bg_frame_index = (current_time // self.bg_anim_speed) % len(self.bg_frames)
    
    def draw(self, screen):
        """Dibuja la pantalla de Game Over."""
        # Fondo (animado si hay frames, estático si no)
        if self.bg_frames:
            bg = self.bg_frames[self.bg_frame_index]
            screen.blit(bg, (0, 0))
        else:
            screen.blit(self.game_over_bg, (0, 0))

        # Overlay dramático
        overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 100))  # Negro con alpha 100
        screen.blit(overlay, (0, 0))

        # Título de Game Over
        game_over_text = self.state_manager.font_large.render("¡GAME OVER Y TAL!", True, RED)
        title_rect = game_over_text.get_rect(center=(WINDOW_WIDTH // 2, 150))
        screen.blit(game_over_text, title_rect)
        
        # Puntuación final
        score_text = self.state_manager.font_medium.render(
            f"Cachopo-Puntuación: {self.final_score}", True, WHITE
        )
        score_rect = score_text.get_rect(center=(WINDOW_WIDTH//2, 220))
        screen.blit(score_text, score_rect)
        
        # Récord
        if self.is_new_record:
            record_text = self.state_manager.font_medium.render("¡NUEVO RÉCORD!", True, YELLOW)
        else:
            record_text = self.state_manager.font_medium.render(
                f"Récord: {self.best_score}", True, GRAY
            )
        record_rect = record_text.get_rect(center=(WINDOW_WIDTH//2, 260))
        screen.blit(record_text, record_rect)
        
        # Instrucciones
        restart_text = self.state_manager.font_small.render(
            "Presiona ENTER para jugar de nuevo", True, BLACK
        )
        restart_rect = restart_text.get_rect(topleft=(50, 350))
        screen.blit(restart_text, restart_rect)

        exit_text = self.state_manager.font_small.render("ESC para salir", True, BLACK)
        exit_rect = exit_text.get_rect(topleft=(50, 380))
        screen.blit(exit_text, exit_rect)


# ✅ IMPLEMENTADO: Estado de pausa
class PausedState:
    """
    Estado cuando el juego está pausado.
    
    En este estado el juego se detiene pero se mantiene visible
    en el fondo con una indicación de pausa superpuesta.
    """
    
    def __init__(self, state_manager):
        """Constructor del estado de pausa."""
        self.state_manager = state_manager
        
        # ✅ IMPLEMENTADO: Efecto visual de pausa
        self.pulse_timer = 0  # Para efecto de pulso en el texto "PAUSED"
    
    def handle_events(self, events):
        """
        Maneja eventos en estado de pausa.
        
        Args:
            events: Lista de eventos de pygame
        """
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == KEY_P:
                    # Reanudar el juego
                    self.state_manager.change_state(STATE_PLAYING)
                    print("Juego reanudado")  # Debug
                elif event.key == KEY_ESCAPE:
                    # Volver al menú principal
                    self.state_manager.change_state(STATE_MENU)
                    print("Volviendo al menú desde pausa")  # Debug
        return True
    
    def update(self):
        """Actualizar efectos visuales de la pausa."""
        self.pulse_timer += 1
    
    def draw(self, screen, game_surface=None):
        """
        Dibuja la pantalla de pausa.
        
        Args:
            screen: Superficie donde dibujar
            game_surface: Superficie del juego de fondo (opcional)
        """
        
        # ✅ IMPLEMENTADO: Mostrar el juego de fondo con overlay de pausa
        if game_surface:
            # Dibujar el juego de fondo ligeramente oscurecido
            dark_surface = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
            dark_surface.fill((0, 0, 0))
            dark_surface.set_alpha(128)  # Semi-transparente
            
            screen.blit(game_surface, (0, 0))
            screen.blit(dark_surface, (0, 0))
        else:
            # Si no hay superficie de fondo, usar color sólido
            screen.fill((50, 50, 50))  # Gris oscuro
        
        # ✅ IMPLEMENTADO: Texto "PAUSED" con efecto de pulso
        pulse_factor = abs(pygame.math.Vector2(1, 0).rotate(self.pulse_timer * 3).x)
        pulse_size = int(FONT_SIZE_LARGE + pulse_factor * 10)
        
        try:
            pulse_font = pygame.font.Font(None, pulse_size)
        except:
            pulse_font = self.state_manager.font_large
        
        paused_text = pulse_font.render("PAUSED", True, YELLOW)
        paused_rect = paused_text.get_rect(center=(WINDOW_WIDTH//2, WINDOW_HEIGHT//2 - 50))
        
        # Sombra del texto para mejor legibilidad
        shadow_text = pulse_font.render("PAUSED", True, BLACK)
        shadow_rect = shadow_text.get_rect(center=(paused_rect.centerx + 3, paused_rect.centery + 3))
        screen.blit(shadow_text, shadow_rect)
        screen.blit(paused_text, paused_rect)
        
        # Instrucciones
        instructions = [
            "Presiona P para continuar",
            "ESC para volver al menú"
        ]
        
        y_offset = WINDOW_HEIGHT//2 + 20
        for instruction in instructions:
            text = self.state_manager.font_medium.render(instruction, True, WHITE)
            text_rect = text.get_rect(center=(WINDOW_WIDTH//2, y_offset))
            
            # Fondo semi-transparente para las instrucciones
            bg_rect = pygame.Rect(text_rect.x - 10, text_rect.y - 5,
                                text_rect.width + 20, text_rect.height + 10)
            pygame.draw.rect(screen, BLACK, bg_rect)
            pygame.draw.rect(screen, WHITE, bg_rect, 1)
            
            screen.blit(text, text_rect)
            y_offset += 40


# TODO 1: Estado de pausa
# class PausedState:
#     """Estado cuando el juego está pausado."""
#     
#     def __init__(self, state_manager):
#         self.state_manager = state_manager
#     
#     def handle_events(self, events):
#         for event in events:
#             if event.type == pygame.KEYDOWN:
#                 if event.key == KEY_P:
#                     self.state_manager.change_state(STATE_PLAYING)
#         return True
#     
#     def update(self):
#         pass
#     
#     def draw(self, screen):
#         # Dibujar "PAUSED" en el centro
#         pass

# === NOTAS EDUCATIVAS ===
"""
Conceptos importantes sobre máquinas de estados:

1. SEPARACIÓN DE RESPONSABILIDADES:
   Cada estado maneja solo su propia lógica, lo que hace
   el código más organizado y fácil de mantener.

2. TRANSICIONES DE ESTADO:
   Los estados pueden cambiar a otros estados según eventos
   (teclas presionadas, condiciones del juego, etc.).

3. GESTIÓN DE EVENTOS:
   Cada estado decide cómo responder a eventos de teclado
   y ratón de manera apropiada para su contexto.

4. RENDERIZADO CONDICIONAL:
   Solo se dibuja lo que es relevante para el estado actual,
   mejorando el rendimiento y la claridad visual.

5. FLUJO DEL PROGRAMA:
   La máquina de estados define cómo el usuario navega
   por las diferentes pantallas del juego.

Ejercicio para estudiantes:
- Implementar el estado de pausa (TODO 1)
- Añadir un estado de opciones o configuración
- Crear transiciones animadas entre estados
"""