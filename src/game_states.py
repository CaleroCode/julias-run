"""
game_states.py - Estados del juego Julia's Run

Este archivo gestiona los diferentes estados o pantallas del juego:
- Menú principal
- Jugando
- Game Over
- Pausa

Conceptos de programación cubiertos:
- Máquina de estados
- Gestión de eventos
- Renderizado condicional
- Flujo de control del programa

Referencias útiles:
- pygame.font: https://www.pygame.org/docs/ref/font.html
- pygame.event: https://www.pygame.org/docs/ref/event.html
"""

import os
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
        if self.next_state is not None:
            self.current_state = self.next_state
            self.next_state = None
    
    def get_current_state(self):
        """Obtiene el estado actual."""
        return self.current_state


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
        self.bg_anim_speed = 150  # ms por frame
        # =============================

        # ====== LOGO DEL JUEGO ======
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
                if event.key in (KEY_SPACE, KEY_ENTER):
                    self.state_manager.change_state(STATE_PLAYING)
                elif event.key == KEY_ESCAPE:
                    return False  # Señal para salir del juego
        
        return True  # Continuar ejecutando
    
    def update(self):
        """Actualiza la lógica del menú (animación del fondo)."""
        if self.bg_frames:
            current_time = pygame.time.get_ticks()
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
            screen.fill(LIGHT_BLUE)
        # ===================================

        # ====== LOGO DEL JUEGO ======
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

        panel_w = int(WINDOW_WIDTH * 0.31)
        panel_h = padding_y * 2 + line_h * len(instructions)
        panel_rect = pygame.Rect(MARGIN_X - padding_x, start_y - padding_y, panel_w, panel_h)

        # "Falso blur"
        sub = screen.subsurface(panel_rect).copy()
        small = pygame.transform.smoothscale(
            sub,
            (max(1, panel_rect.w // 8), max(1, panel_rect.h // 8))
        )
        blurred = pygame.transform.smoothscale(small, (panel_rect.w, panel_rect.h))
        screen.blit(blurred, panel_rect.topleft)

        # Vidrio
        glass = pygame.Surface((panel_rect.w, panel_rect.h), pygame.SRCALPHA)
        pygame.draw.rect(glass, (255, 255, 255, 70), glass.get_rect(), border_radius=18)
        pygame.draw.rect(glass, (255, 255, 255, 120), glass.get_rect(), width=1, border_radius=18)

        highlight = pygame.Surface((panel_rect.w, panel_rect.h // 3), pygame.SRCALPHA)
        pygame.draw.rect(highlight, (255, 255, 255, 60), highlight.get_rect(), border_radius=18)
        glass.blit(highlight, (0, 0))

        shadow = pygame.Surface((panel_rect.w + 12, panel_rect.h + 12), pygame.SRCALPHA)
        pygame.draw.rect(shadow, (0, 0, 0, 80), shadow.get_rect(), border_radius=22)
        screen.blit(shadow, (panel_rect.x - 6, panel_rect.y - 6))

        screen.blit(glass, panel_rect.topleft)

        x_text = panel_rect.x + padding_x
        y_text = panel_rect.y + padding_y

        for i, instruction in enumerate(instructions):
            if instruction:
                surf = self.state_manager.font_small.render(instruction, True, BLACK)
                screen.blit(surf, (x_text, y_text + i * line_h))


class PlayingState:
    """
    Estado principal del juego.
    
    Aquí ocurre toda la acción del gameplay.
    """
    
    def __init__(self, state_manager):
        """Constructor del estado de juego."""
        self.state_manager = state_manager
        
        # 🔊 Sonidos (protegidos con try/except para evitar crasheos)
        self.snd_throw = None
        self.snd_hit = None
        self.snd_powerup = None
        try:
            self.snd_throw = pygame.mixer.Sound(SOUND_THROW)
            self.snd_hit = pygame.mixer.Sound(SOUND_HIT)
            self.snd_powerup = pygame.mixer.Sound(SOUND_POWERUP)

            self.snd_throw.set_volume(0.3)
            self.snd_hit.set_volume(0.2)
            self.snd_powerup.set_volume(0.2)
        except Exception as e:
            print(f"[PlayingState] Error cargando sonidos: {e}")

        # ================= HUD PIXELART =================
        self.hud_bg_color = (20, 12, 40)     
        self.hud_border_color = (120, 200, 255)
        self.hud_text_color = (240, 240, 240)

        # Fuentes pixel (fallback a las del state_manager si falla)
        try:
            self.font_hud_medium = pygame.font.Font("assets/fonts/pixel.ttf", 18)
            self.font_hud_small = pygame.font.Font("assets/fonts/pixel.ttf", 12)
        except Exception as e:
            print(f"[HUD] No se pudo cargar fuente pixel, usando fuente por defecto: {e}")
            self.font_hud_medium = self.state_manager.font_medium
            self.font_hud_small = self.state_manager.font_small

        # Iconos de vidas y escudo (16x16)
        self.heart_icon = None
        self.shield_icon = None
        try:
            heart = pygame.image.load("assets/sprites/ui_heart.png").convert_alpha()
            shield = pygame.image.load("assets/sprites/ui_shield.png").convert_alpha()
            self.heart_icon = pygame.transform.scale(heart, (16, 16))
            self.shield_icon = pygame.transform.scale(shield, (16, 16))
        except Exception as e:
            print(f"[HUD] No se pudieron cargar iconos pixelart: {e}")
        # =================================================
        
        # 👉 NUEVO: sprite "¡AY!" al recibir daño (escalado pequeño)
        try:
            ay_raw = pygame.image.load("assets/sprites/ay.png").convert_alpha()
            # Escala a un tamaño más pequeño, ajusta (32, 32) si lo quieres aún más mini
            self.ay_image = pygame.transform.smoothscale(ay_raw, (2, 2))
        except Exception as e:
            print(f"[HUD] No se pudo cargar ay.png: {e}")
            self.ay_image = None


        # 👉 NUEVO: temporizador del sprite "¡AY!"
        self.ay_timer = 0
        # ====================================

        # ANTES: self.reset_game()
        # Esa lógica ahora vive en JuliasRunGame.reset_game(), así que aquí no se llama nada más.
    
    def handle_events(self, events, player, knife_cooldown):
        """
        Maneja los eventos durante el gameplay.
        
        Devuelve:
            (new_knives, continuar_jugando: bool)
        """
        new_knives = []
        
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == KEY_SPACE:
                    if knife_cooldown.is_ready():
                        from entities import Knife  # Import local para evitar circular
                        new_knife = Knife(player.rect)
                        new_knives.append(new_knife)
                        knife_cooldown.start_cooldown()
                        if self.snd_throw is not None:
                            self.snd_throw.play()
                
                elif event.key == KEY_P:
                    self.state_manager.change_state(STATE_PAUSED)
                    print("Juego pausado")
                
                elif event.key == KEY_ESCAPE:
                    # Salir del juego (el game loop en main.py interpretará este False)
                    return new_knives, False
        
        return new_knives, True  # Continuar jugando
    
    def update(self, player, obstacles, knives, powerups, effects, knife_cooldown):
        """
        Actualiza toda la lógica del juego.

        OJO: con tu nuevo main.py, probablemente ya no uses este método,
        porque la lógica está centralizada en JuliasRunGame.update_game_logic().
        Lo dejo funcional igualmente por si lo sigues usando en algún sitio.
        """
        # ================== debug colisiones / sonidos ==================
        # Si te molesta el spam en consola, comenta estas líneas:
        # print("----- FRAME UPDATE -----")
        # print("PLAYER:", player.rect)
        # print("   Obstáculos:", len(obstacles))
        # print("   Powerups:", len(powerups))
        # print("   Knives:", len(knives))
        # ===================================================

        # 👉 NUEVO: actualizar el temporizador del sprite "¡AY!"
        if self.ay_timer > 0:
            self.ay_timer -= 1
        
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
                # player.take_damage() devuelve True si sigue vivo, False si muere
                if player.take_damage():
                    obstacles.remove(obstacle)
                    # 👉 NUEVO: mostrar sprite "¡AY!" encima de la cabeza
                    self.ay_timer = 30  # ~0.5s a 60 FPS
                    if self.snd_hit is not None:
                        self.snd_hit.play()
                else:
                    # Última vida: también mostramos "¡AY!" justo antes del Game Over
                    self.ay_timer = 30
                    if self.snd_hit is not None:
                        self.snd_hit.play()
                    return False  # Game Over
                        
        # Colisiones cuchillo-obstáculos
        for knife in knives[:]:
            for obstacle in obstacles[:]:
                if knife.rect.colliderect(obstacle.rect):
                    print("COLISIÓN CUCHILLO-OBSTACULO!!")
                    knives.remove(knife)
                    obstacles.remove(obstacle)
                    player.score += POINTS_PER_OBSTACLE_DESTROYED
                    if self.snd_hit is not None:
                        self.snd_hit.play()
                    break
        
        # Colisiones jugador-powerups
        for powerup in powerups[:]:
            if player.rect.colliderect(powerup.rect):
                print(f"powerup recogido: {powerup.type}")
                powerups.remove(powerup)
                player.score += POINTS_PER_POWERUP
                if self.snd_powerup is not None:
                    self.snd_powerup.play()
                
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

        Igual que con update(), en tu nuevo main probablemente ya dibujas
        directamente desde JuliasRunGame.draw_game_content(), pero esta
        función se queda operativa por si aún la usas.
        """
        screen.fill(BLACK)
        
        # Jugador y entidades
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
        HUD estilo pixelart:
        - Barra superior morada
        - SCORE tipo arcade
        - Vidas con corazones
        - Escudo a la derecha
        """
        hud_height = 64

        # Barra superior
        pygame.draw.rect(screen, self.hud_bg_color, (0, 0, WINDOW_WIDTH, hud_height))
        pygame.draw.rect(screen, self.hud_border_color, (0, 0, WINDOW_WIDTH, hud_height), 2)

        padding_x = 10
        padding_y = 8

        # SCORE
        score_str = f"SCORE {player.score:06d}"
        score_text = self.font_hud_medium.render(score_str, True, self.hud_text_color)
        screen.blit(score_text, (padding_x, padding_y))

        # VIDAS
        lives_y = padding_y + 26
        lives_x = padding_x

        if self.heart_icon:
            for i in range(player.lives):
                icon_x = lives_x + i * (self.heart_icon.get_width() + 2)
                screen.blit(self.heart_icon, (icon_x, lives_y))

            lives_label = self.font_hud_small.render("LIVES", True, self.hud_text_color)
            screen.blit(
                lives_label,
                (
                    lives_x + player.lives * (self.heart_icon.get_width() + 6),
                    lives_y + 2,
                ),
            )
        else:
            lives_text = self.font_hud_small.render(f"LIVES: {player.lives}", True, self.hud_text_color)
            screen.blit(lives_text, (lives_x, lives_y))

        # ESCUDO
        if getattr(player, "has_shield", False):
            shield_panel_x = WINDOW_WIDTH - 160
            shield_panel_y = padding_y + 4

            panel_w = 140
            panel_h = 32
            panel_rect = pygame.Rect(shield_panel_x, shield_panel_y, panel_w, panel_h)
            pygame.draw.rect(screen, (30, 60, 90), panel_rect)
            pygame.draw.rect(screen, self.hud_border_color, panel_rect, 2)

            text_offset_x = 6
            if self.shield_icon:
                screen.blit(self.shield_icon, (shield_panel_x + 6, shield_panel_y + 8))
                text_offset_x = 26

            shield_text = self.font_hud_small.render("SHIELD ACTIVE", True, TEA_COLOR)
            screen.blit(shield_text, (shield_panel_x + text_offset_x, shield_panel_y + 8))

        # COOLDOWN CUCHILLO
        knife_cooldown.draw_cooldown_bar(screen)

        # EFECTOS ACTIVOS
        effects.draw_active_effects(screen, self.font_hud_small)


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

                    # === RECORTAR LA PARTE INFERIOR (firma) ===
                    w, h = img.get_size()
                    crop_bottom = 60
                    if crop_bottom < h:
                        crop_rect = pygame.Rect(0, 0, w, h - crop_bottom)
                        img = img.subsurface(crop_rect)
                    # ==========================================

                    img = pygame.transform.scale(img, (WINDOW_WIDTH, WINDOW_HEIGHT))
                    self.bg_frames.append(img)

        self.bg_frame_index = 0
        self.bg_anim_speed = 150  # ms por frame
        # ======================================

        # ===== LOGO ESPECÍFICO DE GAME OVER =====
        try:
            self.logo_image = pygame.image.load("assets/sprites/gameover_small.png").convert_alpha()
            # Escalar por si acaso es grande
            max_logo_width = int(WINDOW_WIDTH * 0.4)
            logo_w, logo_h = self.logo_image.get_size()
            if logo_w > max_logo_width:
                scale_factor = max_logo_width / logo_w
                new_size = (int(logo_w * scale_factor), int(logo_h * scale_factor))
                self.logo_image = pygame.transform.scale(self.logo_image, new_size)
        except Exception as e:
            print(f"[GAME OVER] No se pudo cargar gameover_small.png: {e}")
            self.logo_image = None
        # =========================================
    
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

        # ===== TEXTO ARRIBA A LA IZQUIERDA =====
        margin_left = 30
        current_y = 30

        # Puntuación final
        score_text = self.state_manager.font_medium.render(
            f"Cachopo-Puntuación: {self.final_score}", True, WHITE
        )
        screen.blit(score_text, (margin_left, current_y))
        current_y += 35
        
        # Récord
        if self.is_new_record:
            record_text = self.state_manager.font_medium.render("¡NUEVO RÉCORD!", True, YELLOW)
        else:
            record_text = self.state_manager.font_medium.render(
                f"Récord: {self.best_score}", True, GRAY
            )
        screen.blit(record_text, (margin_left, current_y))
        current_y += 50
        
        # Instrucciones (blanco, alineadas a la izquierda)
        restart_text = self.state_manager.font_small.render(
            "Presiona ENTER para jugar de nuevo", True, WHITE
        )
        screen.blit(restart_text, (margin_left, current_y))
        current_y += 25

        exit_text = self.state_manager.font_small.render(
            "ESC para salir", True, WHITE
        )
        screen.blit(exit_text, (margin_left, current_y))
        # =======================================

        # ===== LOGO A LA IZQUIERDA, CENTRADO VERTICALMENTE =====
        if self.logo_image:
            logo_rect = self.logo_image.get_rect()
            
            # margen desde la izquierda (ajusta si lo quieres más pegado o más separado)
            logo_margin_left = 40  

            # centrado vertical
            logo_rect.midleft = (logo_margin_left, WINDOW_HEIGHT // 2)

            screen.blit(self.logo_image, logo_rect)
        # =======================================================




class PausedState:
    """
    Estado cuando el juego está pausado.
    
    El juego se detiene pero se mantiene visible en el fondo.
    """
    
    def __init__(self, state_manager):
        """Constructor del estado de pausa."""
        self.state_manager = state_manager
        self.pulse_timer = 0  # Para efecto de pulso en el texto "PAUSED"
    
    def handle_events(self, events):
        """
        Maneja eventos en estado de pausa.
        """
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == KEY_P:
                    self.state_manager.change_state(STATE_PLAYING)
                    print("Juego reanudado")
                elif event.key == KEY_ESCAPE:
                    self.state_manager.change_state(STATE_MENU)
                    print("Volviendo al menú desde pausa")
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
        if game_surface:
            dark_surface = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
            dark_surface.fill((0, 0, 0))
            dark_surface.set_alpha(128)
            
            screen.blit(game_surface, (0, 0))
            screen.blit(dark_surface, (0, 0))
        else:
            screen.fill((50, 50, 50))
        
        pulse_factor = abs(pygame.math.Vector2(1, 0).rotate(self.pulse_timer * 3).x)
        pulse_size = int(FONT_SIZE_LARGE + pulse_factor * 10)
        
        try:
            pulse_font = pygame.font.Font(None, pulse_size)
        except Exception:
            pulse_font = self.state_manager.font_large
        
        paused_text = pulse_font.render("PAUSED", True, YELLOW)
        paused_rect = paused_text.get_rect(center=(WINDOW_WIDTH//2, WINDOW_HEIGHT//2 - 50))
        
        shadow_text = pulse_font.render("PAUSED", True, BLACK)
        shadow_rect = shadow_text.get_rect(center=(paused_rect.centerx + 3, paused_rect.centery + 3))
        screen.blit(shadow_text, shadow_rect)
        screen.blit(paused_text, paused_rect)
        
        instructions = [
            "Presiona P para continuar",
            "ESC para volver al menú"
        ]
        
        y_offset = WINDOW_HEIGHT//2 + 20
        for instruction in instructions:
            text = self.state_manager.font_medium.render(instruction, True, WHITE)
            text_rect = text.get_rect(center=(WINDOW_WIDTH//2, y_offset))
            
            bg_rect = pygame.Rect(
                text_rect.x - 10,
                text_rect.y - 5,
                text_rect.width + 20,
                text_rect.height + 10
            )
            pygame.draw.rect(screen, BLACK, bg_rect)
            pygame.draw.rect(screen, WHITE, bg_rect, 1)
            
            screen.blit(text, text_rect)
            y_offset += 40


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
"""
