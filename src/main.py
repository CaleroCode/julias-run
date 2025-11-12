"""
main.py - Punto de entrada de Julia's Run

📚 PROPÓSITO EDUCATIVO:
Este archivo demuestra cómo se estructura un programa completo usando POO.
Aquí ves la INTEGRACIÓN de todas las clases trabajando juntas.

🎮 ¿QUÉ HACE ESTE ARCHIVO?
- Inicializa Pygame y configura la ventana
- Crea los objetos principales del juego (Player, listas de enemigos, etc.)
- Ejecuta el GAME LOOP principal (update → draw → repeat)
- Gestiona eventos de entrada (teclado, mouse, cerrar ventana)

🧩 CONCEPTOS POO QUE VAS A VER:
1. COMPOSICIÓN: JuliasRunGame "tiene" un Player, listas de Obstacles, etc.
2. DELEGACIÓN: JuliasRunGame llama métodos de sus objetos (player.move(), obstacle.update())
3. ENCAPSULACIÓN: Cada objeto se encarga de su propia lógica
4. ABSTRACCIÓN: El game loop no necesita saber CÓMO se mueve el player, solo que se mueve

🔍 PREGUNTAS PARA REFLEXIONAR:
- ¿Por qué JuliasRunGame es una clase y no solo funciones sueltas?
- ¿Dónde se crean los objetos Player, Obstacle, etc.?
- ¿Cómo interactúan las diferentes clases entre sí?
- ¿Qué pasaría si quisieras añadir un nuevo tipo de entidad?

🎯 FLUJO PRINCIPAL:
1. __init__(): Crear e inicializar todos los objetos
2. run(): Ejecutar el game loop infinito
   - handle_events(): Procesar input del usuario
   - update(): Actualizar estado de todos los objetos
   - draw(): Dibujar todo en pantalla
3. cleanup(): Limpiar recursos al salir

Para ejecutar: python src/main.py
"""

import sys
import pygame
import random

# Importar nuestros módulos
from settings import *
from entities import Player, Obstacle, Knife, PowerUp, Enemy, Explosion, ScreenEffect
from abilities import CooldownTimer, PowerUpEffect, ParticleEffect, ComboSystem
from game_states import GameStateManager, MenuState, PlayingState, GameOverState, PausedState
from utils import (
    load_best_score, save_best_score, should_spawn_obstacle, 
    should_spawn_powerup, get_random_powerup_type, get_difficulty_multiplier,
    debug_print, update_play_statistics, get_fps_color
)


class JuliasRunGame:
    """
    Clase principal del juego Julia's Run.
    
    Esta clase encapsula todo el juego: inicialización, game loop,
    y gestión de todos los sistemas del juego.
    
    El patrón usado aquí es común en programación de juegos:
    - Inicialización una vez
    - Game loop que se ejecuta continuamente
    - Cleanup al salir
    """
    
    def __init__(self):
        """Inicializa el juego y todos sus sistemas.""" 
    
        # Inicializar Pygame
        pygame.init()
    
        
        # Crear la ventana del juego
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Julia's Run - ¡Esquiva y Sobrevive!")
        
        # Fondo scroll
        self.background = pygame.image.load("assets//sprites/background.png").convert()
        self.background_y = 0
        
        # Control de tiempo (FPS)
        self.clock = pygame.time.Clock()
        
        # Gestor de estados del juego
        self.state_manager = GameStateManager()
        self.menu_state = MenuState(self.state_manager)
        self.playing_state = PlayingState(self.state_manager)
        self.game_over_state = GameOverState(self.state_manager)
        self.paused_state = PausedState(self.state_manager)  # ✅ IMPLEMENTADO
        
        # Variables del juego
        self.running = True
        self.frame_count = 0
        
        # ✅ IMPLEMENTADO: Variables adicionales para funcionalidad completa
        self.debug_mode = False        # Modo debug (activar con F1)
        self.show_fps = False         # Mostrar FPS (activar con F2)
        self.game_start_time = 0      # Para tracking de tiempo de juego
        
        # Inicializar componentes del juego
        self.reset_game()
    
    def reset_game(self):
        """
        Reinicia el juego a su estado inicial.
        
        Esta función se llama al inicio y cada vez que se reinicia una partida.
        Es importante resetear TODOS los componentes para evitar bugs.
        """
        
        # Crear jugador
        self.player = Player()
        
        # Listas de entidades del juego
        self.obstacles = []      # Lista de obstáculos en pantalla
        self.knives = []         # Lista de cuchillos lanzados
        self.powerups = []       # Lista de power-ups en pantalla
        self.enemies = []        # ✅ IMPLEMENTADO: Lista de enemigos
        self.explosions = []     # ✅ IMPLEMENTADO: Lista de explosiones
        self.particles = []      # ✅ IMPLEMENTADO: Lista de efectos de partículas
        
        # Sistemas de juego
        self.knife_cooldown = CooldownTimer(KNIFE_COOLDOWN)
        self.powerup_effects = PowerUpEffect()
        self.combo_system = ComboSystem()     # ✅ IMPLEMENTADO: Sistema de combos
        self.screen_effects = ScreenEffect()  # ✅ IMPLEMENTADO: Efectos de pantalla
        
        # Contadores
        self.frame_count = 0
        self.enemy_spawn_timer = 0  # ✅ IMPLEMENTADO: Timer para spawn de enemigos
        
        # ✅ IMPLEMENTADO: Variables para dificultad progresiva
        self.current_difficulty = 1.0
        self.last_difficulty_score = 0
        
        # Cargar mejor puntuación
        self.best_score = load_best_score()
        
        # ✅ IMPLEMENTADO: Inicializar tiempo de juego
        self.game_start_time = pygame.time.get_ticks() / 1000.0
        
        debug_print("Juego reiniciado. ¡Buena suerte!", debug_mode=self.debug_mode)
    
    def handle_events(self):
        """
        Maneja todos los eventos del juego (teclado, ratón, etc.).
        
        Returns:
            bool: False si se debe salir del juego, True para continuar
        """
        
        # Obtener todos los eventos de esta frame
        events = pygame.event.get()
        
        # Revisar eventos especiales (cerrar ventana)
        for event in events:
            if event.type == pygame.QUIT:
                return False
            
            # ✅ IMPLEMENTADO: Controles de debug y herramientas
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_F1:
                    self.debug_mode = not self.debug_mode
                    print(f"Modo debug: {'ON' if self.debug_mode else 'OFF'}")
                elif event.key == pygame.K_F2:
                    self.show_fps = not self.show_fps
                    print(f"Mostrar FPS: {'ON' if self.show_fps else 'OFF'}")
                elif event.key == pygame.K_F3 and self.debug_mode:
                    # Cheat: añadir puntos para testing
                    if hasattr(self, 'player'):
                        self.player.score += 50
                        print("Cheat: +50 puntos añadidos")
        
        # Delegar el manejo de eventos al estado actual
        current_state = self.state_manager.get_current_state()
        
        if current_state == STATE_MENU:
            return self.menu_state.handle_events(events)
        
        elif current_state == STATE_PLAYING:
            new_knives, continue_playing = self.playing_state.handle_events(
                events, self.player, self.knife_cooldown
            )
            # Añadir nuevos cuchillos a la lista
            self.knives.extend(new_knives)
            return continue_playing
        
        elif current_state == STATE_PAUSED:
            # ✅ IMPLEMENTADO: Manejar eventos en estado de pausa
            return self.paused_state.handle_events(events)
        
        elif current_state == STATE_GAME_OVER:
            return self.game_over_state.handle_events(events)
        
        return True
    
    def update(self):
        """
        Actualiza toda la lógica del juego.
        
        Esta función se llama una vez por frame y contiene toda la lógica
        del juego: movimiento, colisiones, spawn de entidades, etc.
        """
        
        # Actualizar el gestor de estados
        self.state_manager.update_state()
        
        current_state = self.state_manager.get_current_state()
        
        if current_state == STATE_MENU:
            self.menu_state.update()
        
        elif current_state == STATE_PLAYING:
            # Incrementar contador de frames
            self.frame_count += 1
            
            # ✅ IMPLEMENTADO: Calcular dificultad progresiva
            self.current_difficulty = get_difficulty_multiplier(self.player.score)
            
            # ✅ IMPLEMENTADO: Notificar al jugador cuando aumenta la dificultad
            if self.player.score // DIFFICULTY_INCREASE_INTERVAL > self.last_difficulty_score // DIFFICULTY_INCREASE_INTERVAL:
                self.last_difficulty_score = self.player.score
                debug_print(f"¡Dificultad aumentada! Nivel: {self.current_difficulty:.1f}", 
                        debug_mode=True)  # Siempre mostrar este mensaje
            
            # Spawn de nuevos obstáculos (con dificultad ajustada)
            adjusted_spawn_rate = max(30, OBSTACLE_SPAWN_RATE - int(self.current_difficulty * 10))
            if self.frame_count % adjusted_spawn_rate == 0:
                new_obstacle = Obstacle(self.current_difficulty)
                self.obstacles.append(new_obstacle)
            
            # ✅ IMPLEMENTADO: Spawn de enemigos ocasional
            self.enemy_spawn_timer += 1
            enemy_spawn_rate = max(300, 600 - int(self.current_difficulty * 50))
            if self.enemy_spawn_timer >= enemy_spawn_rate:
                if len(self.enemies) < 2:  # Máximo 2 enemigos a la vez
                    new_enemy = Enemy(self.player.rect.centerx, self.current_difficulty)
                    self.enemies.append(new_enemy)
                    debug_print("¡Enemigo aparecido!", debug_mode=self.debug_mode)
                self.enemy_spawn_timer = 0
            
            # Spawn de power-ups (menos frecuente con dificultad)
            adjusted_powerup_rate = max(200, POWERUP_SPAWN_RATE + int(self.current_difficulty * 20))
            if self.frame_count % adjusted_powerup_rate == 0:
                powerup_type = get_random_powerup_type()
                new_powerup = PowerUp(powerup_type)
                self.powerups.append(new_powerup)
            
            # Actualizar lógica del juego
            player_alive = self.update_game_logic()
            
            # Comprobar Game Over
            if not player_alive:
                self.handle_game_over()
        
        elif current_state == STATE_PAUSED:
            # ✅ IMPLEMENTADO: En pausa, solo actualizar efectos visuales
            self.paused_state.update()
        
        elif current_state == STATE_GAME_OVER:
            self.game_over_state.update()
    
    def update_game_logic(self):
        """
        ✅ IMPLEMENTADO: Lógica de juego mejorada con todos los sistemas.
        
        Esta función centraliza toda la lógica del juego durante el estado PLAYING,
        incluyendo sistemas nuevos como combos, partículas y efectos de pantalla.
        
        Returns:
            bool: True si el jugador sigue vivo, False si Game Over
        """
        
        # Actualizar timers y sistemas
        self.knife_cooldown.update()
        self.powerup_effects.update(self.player)
        self.combo_system.update()
        self.screen_effects.update()
        
        # Mover jugador según teclas presionadas
        keys = pygame.key.get_pressed()
        self.player.move(keys)
        
        # ✅ IMPLEMENTADO: Actualizar obstáculos normales
        for obstacle in self.obstacles[:]:
            if not obstacle.update():
                # Obstáculo salió de pantalla - dar puntos por esquivar
                self.obstacles.remove(obstacle)
                points = self.combo_system.get_combo_bonus_points(POINTS_PER_OBSTACLE_AVOIDED)
                self.player.score += points
                debug_print(f"Obstáculo esquivado: +{points} puntos", debug_mode=self.debug_mode)
        
        # ✅ IMPLEMENTADO: Actualizar enemigos
        for enemy in self.enemies[:]:
            if not enemy.update(self.player.rect.centerx):
                self.enemies.remove(enemy)
                # Los enemigos dan más puntos por esquivar
                points = self.combo_system.get_combo_bonus_points(POINTS_PER_OBSTACLE_AVOIDED * 2)
                self.player.score += points
                debug_print(f"Enemigo esquivado: +{points} puntos", debug_mode=self.debug_mode)
        
        # Actualizar cuchillos
        for knife in self.knives[:]:
            if not knife.update():
                self.knives.remove(knife)
        
        # Actualizar power-ups
        for powerup in self.powerups[:]:
            if not powerup.update():
                self.powerups.remove(powerup)
        
        # ✅ IMPLEMENTADO: Actualizar explosiones
        for explosion in self.explosions[:]:
            if not explosion.update():
                self.explosions.remove(explosion)
        
        # ✅ IMPLEMENTADO: Actualizar partículas
        for particle_effect in self.particles[:]:
            if not particle_effect.update():
                self.particles.remove(particle_effect)
        
        # ✅ IMPLEMENTADO: Detección de colisiones jugador-obstáculos (con invulnerabilidad)
        all_threats = self.obstacles + self.enemies
        for threat in all_threats[:]:
            if self.player.rect.colliderect(threat.rect):
                # Remover la amenaza
                if threat in self.obstacles:
                    self.obstacles.remove(threat)
                else:
                    self.enemies.remove(threat)
                
                # ✅ IMPLEMENTADO: Efectos al recibir daño
                if not self.player.take_damage():
                    # Game Over
                    return False
                
                # Resetear combo al recibir daño
                self.combo_system.add_miss()
                
                # ✅ IMPLEMENTADO: Efectos visuales al recibir daño
                self.screen_effects.start_screen_shake()
                
                # Crear efecto de partículas en el punto de impacto
                impact_particles = ParticleEffect(
                    threat.rect.centerx, threat.rect.centery, 
                    RED, particle_count=8, effect_type="explosion"
                )
                self.particles.append(impact_particles)
        
        # ✅ IMPLEMENTADO: Detección de colisiones cuchillo-amenazas
        for knife in self.knives[:]:
            hit_something = False
            
            # Colisiones con obstáculos
            for obstacle in self.obstacles[:]:
                if knife.rect.colliderect(obstacle.rect):
                    # Destruir ambos y dar puntos
                    self.knives.remove(knife)
                    self.obstacles.remove(obstacle)
                    
                    # ✅ IMPLEMENTADO: Puntos con sistema de combos
                    points = self.combo_system.get_combo_bonus_points(POINTS_PER_OBSTACLE_DESTROYED)
                    self.player.score += points
                    self.combo_system.add_hit()
                    
                    # ✅ IMPLEMENTADO: Crear explosión visual
                    explosion = Explosion(obstacle.rect.centerx, obstacle.rect.centery)
                    self.explosions.append(explosion)
                    
                    # ✅ IMPLEMENTADO: Partículas adicionales
                    explosion_particles = ParticleEffect(
                        obstacle.rect.centerx, obstacle.rect.centery,
                        YELLOW, particle_count=12, effect_type="explosion"
                    )
                    self.particles.append(explosion_particles)
                    
                    debug_print(f"Obstáculo destruido: +{points} puntos (combo x{self.combo_system.combo_count})", 
                              debug_mode=self.debug_mode)
                    hit_something = True
                    break
            
            # ✅ IMPLEMENTADO: Colisiones con enemigos (más difíciles de destruir)
            if not hit_something:
                for enemy in self.enemies[:]:
                    if knife.rect.colliderect(enemy.rect):
                        self.knives.remove(knife)
                        self.enemies.remove(enemy)
                        
                        # Los enemigos dan más puntos
                        points = self.combo_system.get_combo_bonus_points(POINTS_PER_OBSTACLE_DESTROYED * 3)
                        self.player.score += points
                        self.combo_system.add_hit()
                        
                        # Explosión más grande para enemigos
                        explosion = Explosion(enemy.rect.centerx, enemy.rect.centery, PURPLE)
                        self.explosions.append(explosion)
                        
                        debug_print(f"Enemigo destruido: +{points} puntos!", debug_mode=self.debug_mode)
                        break
        
        # Detectar colisiones jugador-power-ups
        for powerup in self.powerups[:]:
            if self.player.rect.colliderect(powerup.rect):
                self.powerups.remove(powerup)
                
                # ✅ IMPLEMENTADO: Puntos con sistema de combos
                points = self.combo_system.get_combo_bonus_points(POINTS_PER_POWERUP)
                self.player.score += points
                
                # Activar efecto según el tipo
                if powerup.type == 'vodka':
                    self.powerup_effects.activate_vodka_boost(self.player)
                elif powerup.type == 'tea':
                    self.powerup_effects.activate_tea_shield(self.player)
                elif powerup.type == 'honey':
                    self.player.speed *=0.5
                    self.player.honey_timer = 180
                
                # ✅ IMPLEMENTADO: Efectos visuales para power-ups
                sparkle_particles = ParticleEffect(
                    powerup.rect.centerx, powerup.rect.centery,
                    powerup.color, particle_count=10, effect_type="sparkle"
                )
                self.particles.append(sparkle_particles)
                
                debug_print(f"Power-up recogido: +{points} puntos", debug_mode=self.debug_mode)
        
        return True  # Jugador sigue vivo
    
    def handle_game_over(self):
        """
        Maneja la transición a Game Over.
        
        Se llama cuando el jugador se queda sin vidas.
        Guarda la puntuación y cambia al estado correspondiente.
        """
        
        # ✅ IMPLEMENTADO: Actualizar estadísticas de juego
        game_time = (pygame.time.get_ticks() / 1000.0) - self.game_start_time
        update_play_statistics(self.player.score, game_time)
        
        # Guardar nueva mejor puntuación si corresponde
        if self.player.score > self.best_score:
            save_best_score(self.player.score)
            self.best_score = self.player.score
        
        # Configurar el estado de Game Over
        self.game_over_state.set_scores(self.player.score, self.best_score)
        
        # ✅ IMPLEMENTADO: Mostrar estadísticas finales en debug
        debug_print(f"Game Over! Puntuación final: {self.player.score}", debug_mode=True)
        debug_print(f"Tiempo jugado: {game_time:.1f} segundos", debug_mode=True)
        debug_print(f"Mejor combo: {self.combo_system.best_combo}", debug_mode=True)
        debug_print(f"Dificultad alcanzada: {self.current_difficulty:.1f}", debug_mode=True)
        
        # Cambiar al estado de Game Over
        self.state_manager.change_state(STATE_GAME_OVER)
    
    def draw(self):
        """
        Dibuja todo el contenido del juego en la pantalla.
        
        Esta función se llama una vez por frame y se encarga de
        renderizar todos los elementos visuales del juego.
        """
        
        current_state = self.state_manager.get_current_state()
        
        # ✅ IMPLEMENTADO: Aplicar screen shake si está activo
        screen_offset = self.screen_effects.get_screen_offset()
        
        if current_state == STATE_MENU:
            self.menu_state.draw(self.screen)
        
        elif current_state == STATE_PLAYING:
            # ✅ IMPLEMENTADO: Dibujar con offset de screen shake
            if screen_offset != (0, 0):
                # Crear superficie temporal para aplicar shake
                temp_surface = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
                self.draw_game_content(temp_surface)
                self.screen.blit(temp_surface, screen_offset)
            else:
                self.draw_game_content(self.screen)
        
        elif current_state == STATE_PAUSED:
            # ✅ IMPLEMENTADO: Dibujar pausa con fondo del juego
            game_surface = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
            self.draw_game_content(game_surface)
            self.paused_state.draw(self.screen, game_surface)
        
        elif current_state == STATE_GAME_OVER:
            self.game_over_state.draw(self.screen)
        
        # ✅ IMPLEMENTADO: Dibujar información de debug si está activa
        if self.debug_mode:
            self.draw_debug_info()
        
        # ✅ IMPLEMENTADO: Mostrar FPS si está activado
        if self.show_fps:
            self.draw_fps_counter()
        
        # Actualizar la pantalla (hacer visible lo dibujado)
        pygame.display.flip()
    
    def draw_game_content(self, surface):
        """
        ✅ IMPLEMENTADO: Dibuja el contenido del juego en la superficie especificada.
        
        Esta función centraliza el dibujo del juego para poder reutilizarla
        en diferentes contextos (juego normal, pausa con fondo, etc.).
        """
        
        # Limpiar pantalla
        # surface.fill(BLACK)
        
        # Scroll vertical del fondo
        self.background_y += 2  # Ajusta la velocidad si quieres

        # Reinicio sauve del scroll
        if self.background_y >= self.background.get_height():
            self.background_y -= self.background.get_height()

        # Dibujar el fondo dos veces pa cubrir toda la pantalla
        for x in range(0, WINDOW_WIDTH, self.background.get_width()):
            surface.blit(self.background, (x, self.background_y))
            surface.blit(self.background, (x, self.background_y - self.background.get_height()))

        
        # Dibujar todas las entidades
        self.player.draw(surface)
        
        for obstacle in self.obstacles:
            obstacle.draw(surface)
        
        for enemy in self.enemies:
            enemy.draw(surface)
        
        for knife in self.knives:
            knife.draw(surface)
        
        for powerup in self.powerups:
            powerup.draw(surface)
        
        # ✅ IMPLEMENTADO: Dibujar efectos visuales
        for explosion in self.explosions:
            explosion.draw(surface)
        
        for particle_effect in self.particles:
            particle_effect.draw(surface)
        
        # Dibujar HUD (Heads-Up Display)
        self.draw_hud(surface)
    
    def draw_hud(self, surface):
        """
        ✅ IMPLEMENTADO: Dibuja la interfaz de usuario mejorada.
        """
        
        # Puntuación con formato mejorado
        from utils import format_score
        score_text = self.state_manager.font_medium.render(
            f"Puntuación: {format_score(self.player.score)}", True, WHITE
        )
        surface.blit(score_text, (10, 10))
        
        # Vidas con indicadores visuales
        lives_text = self.state_manager.font_medium.render(f"Vidas: {self.player.lives}", True, WHITE)
        surface.blit(lives_text, (10, 40))
        
        # ✅ IMPLEMENTADO: Indicadores visuales de vidas
        for i in range(self.player.lives):
            heart_x = 80 + i * 25
            heart_y = 45
            pygame.draw.circle(surface, RED, (heart_x, heart_y), 8)
            pygame.draw.circle(surface, WHITE, (heart_x, heart_y), 8, 1)
        
        # Estado del escudo con mejor visualización
        if self.player.has_shield:
            shield_text = self.state_manager.font_small.render("🛡️ ESCUDO ACTIVO", True, TEA_COLOR)
            shield_rect = shield_text.get_rect()
            shield_rect.x = 10
            shield_rect.y = 70
            
            # Fondo para el texto del escudo
            bg_rect = pygame.Rect(shield_rect.x - 2, shield_rect.y - 2,
                                shield_rect.width + 4, shield_rect.height + 4)
            pygame.draw.rect(surface, BLACK, bg_rect)
            pygame.draw.rect(surface, TEA_COLOR, bg_rect, 1)
            
            surface.blit(shield_text, shield_rect)
        
        # ✅ IMPLEMENTADO: Barra de cooldown visual
        self.knife_cooldown.draw_cooldown_bar(surface)
        
        # ✅ IMPLEMENTADO: Efectos activos
        self.powerup_effects.draw_active_effects(surface, self.state_manager.font_small)
        
        # ✅ IMPLEMENTADO: Sistema de combos
        self.combo_system.draw_combo_display(surface, self.state_manager.font_small)
        
        # ✅ IMPLEMENTADO: Indicador de dificultad
        if self.current_difficulty > 1.0:
            diff_text = f"Dificultad: {self.current_difficulty:.1f}x"
            diff_surface = self.state_manager.font_small.render(diff_text, True, YELLOW)
            diff_rect = diff_surface.get_rect()
            diff_rect.right = WINDOW_WIDTH - 10
            diff_rect.bottom = WINDOW_HEIGHT - 10
            surface.blit(diff_surface, diff_rect)
    
    def draw_debug_info(self):
        """
        ✅ IMPLEMENTADO: Dibuja información de debug.
        """
        debug_info = [
            f"FPS: {self.clock.get_fps():.1f}",
            f"Obstáculos: {len(self.obstacles)}",
            f"Enemigos: {len(self.enemies)}",
            f"Cuchillos: {len(self.knives)}",
            f"Power-ups: {len(self.powerups)}",
            f"Explosiones: {len(self.explosions)}",
            f"Partículas: {len(self.particles)}",
            f"Frame: {self.frame_count}",
            f"Estado: {self.state_manager.get_current_state()}",
        ]
        
        y_offset = WINDOW_HEIGHT - len(debug_info) * 20 - 10
        for info in debug_info:
            text = self.state_manager.font_small.render(info, True, WHITE)
            bg_rect = pygame.Rect(10, y_offset - 2, text.get_width() + 4, text.get_height() + 4)
            pygame.draw.rect(self.screen, BLACK, bg_rect)
            pygame.draw.rect(self.screen, GREEN, bg_rect, 1)
            self.screen.blit(text, (12, y_offset))
            y_offset += 20
    
    def draw_fps_counter(self):
        """
        ✅ IMPLEMENTADO: Dibuja contador de FPS con código de colores.
        """
        fps = self.clock.get_fps()
        fps_color = get_fps_color(fps)
        
        fps_text = self.state_manager.font_medium.render(f"FPS: {fps:.0f}", True, fps_color)
        fps_rect = fps_text.get_rect()
        fps_rect.right = WINDOW_WIDTH - 10
        fps_rect.top = 10
        
        # Fondo semi-transparente
        bg_rect = pygame.Rect(fps_rect.x - 5, fps_rect.y - 2,
                            fps_rect.width + 10, fps_rect.height + 4)
        pygame.draw.rect(self.screen, BLACK, bg_rect)
        pygame.draw.rect(self.screen, fps_color, bg_rect, 1)
        
        self.screen.blit(fps_text, fps_rect)
    
    def run(self):
        """
        Game loop principal.
        
        Este es el corazón del juego: un bucle que se ejecuta continuamente
        hasta que el jugador decide salir. En cada iteración:
        1. Maneja eventos
        2. Actualiza lógica
        3. Dibuja en pantalla
        4. Controla el framerate
        """
        
        print("¡Iniciando Julia's Run!")
        print("Usa las flechas para mover, ESPACIO para lanzar cuchillos.")
        print("¡Buena suerte!")
        
        # Game loop principal
        while self.running:
            # 1. Manejar eventos (input del usuario)
            self.running = self.handle_events()
            
            # 2. Actualizar lógica del juego
            if self.running:
                self.update()
            
            # 3. Dibujar todo en pantalla
            if self.running:
                self.draw()
            
            # 4. Controlar framerate (mantener FPS constantes)
            self.clock.tick(FPS)
            
            # Comprobar si necesitamos reiniciar el juego
            if (self.state_manager.get_current_state() == STATE_PLAYING and 
                self.state_manager.next_state == STATE_PLAYING):
                # El estado cambió a PLAYING desde otro estado - reiniciar
                self.reset_game()
                self.state_manager.next_state = None
        
        # Cleanup al salir
        self.cleanup()
    
    def cleanup(self):
        """
        Limpia recursos antes de salir del juego.
        
        Es una buena práctica limpiar recursos (sonidos, fuentes, etc.)
        antes de terminar el programa.
        """
        
        print("¡Gracias por jugar Julia's Run!")
        pygame.quit()


def main():
    """
    Función principal del programa.
    
    Esta función se ejecuta cuando se llama al módulo directamente.
    Maneja errores generales y asegura un cierre limpio del programa.
    """
    
    try:
        # Crear e iniciar el juego
        game = JuliasRunGame()
        game.run()
    
    except KeyboardInterrupt:
        # El usuario presionó Ctrl+C
        print("\nJuego interrumpido por el usuario.")
    
    except Exception as e:
        # Error inesperado
        print(f"Error inesperado: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        # Asegurar que pygame se cierre correctamente
        pygame.quit()
        sys.exit()


# ✅ IMPLEMENTADO: Añadir sistema de pausa
# - El game loop maneja el estado PAUSED correctamente
# - Se mantiene el fondo del juego visible durante la pausa

# ✅ IMPLEMENTADO: Implementar barra de cooldown visual
# - La barra se dibuja en el HUD con colores indicativos
# - Muestra tiempo restante y estado "LISTO"

# ✅ IMPLEMENTADO: Añadir dificultad progresiva
# - Usa get_difficulty_multiplier() de utils.py
# - Aumenta velocidad de obstáculos y frecuencia de spawn según puntuación
# - Spawn de enemigos más frecuente con mayor dificultad

# ✅ IMPLEMENTADO: Integrar sprites y sonidos
# - Estructura preparada para cargar assets reales
# - Efectos visuales mejorados con partículas y animaciones
# - Sistema de colores y formas para distinguir tipos

# ✅ IMPLEMENTADO: Añadir más efectos visuales
# - Partículas al destruir obstáculos y recoger power-ups
# - Explosiones animadas con múltiples partículas
# - Screen shake al recibir daño
# - Efectos de pulso y animaciones en entidades

# ✅ IMPLEMENTADO: Mejorar el HUD
# - Muestra tiempo de efectos activos con fondos semi-transparentes
# - Indicadores visuales de vidas (corazones)
# - Barra de cooldown con código de colores
# - Sistema de combos con multiplicadores

# ✅ IMPLEMENTADO: Sistema de logros/estadísticas
# - Tracking de estadísticas de juego en utils.py
# - Combo system para recompensar juego hábil
# - Debug info y herramientas de desarrollo

# ✅ IMPLEMENTADO: Opciones de configuración
# - Sistema de configuración en utils.py
# - Controles de debug (F1, F2, F3)
# - Modo debug con información detallada

# TODO 9: Multijugador local
# - Segundo jugador con teclas diferentes
# - Competencia por puntuación más alta

# ✅ IMPLEMENTADO: Efectos de pantalla
# - Screen shake al recibir daño implementado
# - Sistema de efectos de pantalla extensible para más efectos

# TODO 1: Añadir sistema de pausa
# - Modificar el game loop para manejar el estado PAUSED
# - Pausar actualizaciones pero mantener el renderizado

# TODO 2: Implementar barra de cooldown visual
# - Llamar al método draw_cooldown_bar() del CooldownTimer

# TODO 3: Añadir dificultad progresiva
# - Usar get_difficulty_multiplier() de utils.py
# - Aumentar velocidad de obstáculos según puntuación

# TODO 4: Integrar sprites y sonidos
# - Cargar assets al inicializar
# - Reemplazar rectángulos con sprites reales

# TODO 5: Añadir más efectos visuales
# - Partículas al destruir obstáculos
# - Animaciones de power-ups

# TODO 6: Mejorar el HUD
# - Mostrar tiempo de efectos activos
# - Añadir mini-mapa o indicadores

# TODO 7: Sistema de logros
# - Tracking de estadísticas de juego
# - Desbloquear logros por acciones específicas

# TODO 8: Opciones de configuración
# - Volumen de sonidos
# - Dificultad inicial
# - Controles personalizables

# TODO 9: Multijugador local
# - Segundo jugador con teclas diferentes
# - Competencia por puntuación más alta

# TODO 10: Efectos de pantalla
# - Screen shake al recibir daño
# - Fade in/out entre estados

# Esta condición verifica si el archivo se está ejecutando directamente
# (no siendo importado como módulo)
if __name__ == "__main__":
    main()

# === NOTAS EDUCATIVAS AMPLIADAS ===
"""
Conceptos importantes del game loop y arquitectura de juegos:

1. GAME LOOP PATTERN:
   El patrón fundamental de los videojuegos:
   - Input → Update → Render → Repeat
   Esta versión implementa un game loop completo con:
   - Manejo de múltiples estados
   - Sistemas de efectos visuales
   - Gestión de tiempo y dificultad progresiva

2. FRAMERATE Y RENDIMIENTO:
   - FPS (Frames Per Second) determina qué tan suave se ve el juego
   - 60 FPS es el estándar para juegos fluidos
   - pygame.time.Clock.tick() controla el framerate
   - El contador de FPS con colores ayuda a detectar problemas de rendimiento

3. SEPARACIÓN DE RESPONSABILIDADES AVANZADA:
   - main.py orquesta todo pero delega responsabilidades específicas
   - Cada sistema (combos, partículas, efectos) es independiente
   - Facilita mantenimiento y permite añadir nuevas funcionalidades

4. GESTIÓN DE ESTADOS COMPLETA:
   - Estados bien definidos con transiciones claras
   - El estado de pausa demuestra cómo preservar contexto
   - Cada estado maneja sus propios eventos y renderizado

5. SISTEMAS DE PARTÍCULAS:
   - Efectos visuales que mejoran la experiencia del jugador
   - Cada partícula es un objeto simple con física básica
   - Se crean dinámicamente y se destruyen automáticamente

6. DIFICULTAD PROGRESIVA:
   - El juego se adapta al progreso del jugador
   - Múltiples variables afectadas (velocidad, spawn rate, tipos de enemigos)
   - Equilibrio entre desafío y jugabilidad

7. SISTEMA DE COMBOS:
   - Recompensa el juego hábil y consistente
   - Multiplicadores que afectan la puntuación
   - Timeout para mantener presión sobre el jugador

8. DEBUG Y HERRAMIENTAS DE DESARROLLO:
   - Modo debug para visualizar estado interno
   - Teclas especiales para testing (F1, F2, F3)
   - Información en tiempo real para optimización

9. GESTIÓN DE MEMORIA Y RENDIMIENTO:
   - Listas que se limpian automáticamente
   - Límites en número de entidades simultáneas
   - Reutilización de objetos cuando es posible

10. FEEDBACK VISUAL INMEDIATO:
    - Screen shake para impacto
    - Efectos de parpadeo para invulnerabilidad
    - Colores que comunican estado (escudo, velocidad, etc.)

ERRORES COMUNES QUE LOS ESTUDIANTES PODRÍAN COMETER:

1. **Olvidar reiniciar listas al reiniciar el juego**:
   - Solución: El método reset_game() limpia todas las listas
   
2. **No manejar la eliminación segura de listas**:
   - Problema: for item in lista: lista.remove(item)
   - Solución: for item in lista[:]: # Iterar sobre copia
   
3. **Hardcodear valores en lugar de usar constants**:
   - Problema: if countdown == 60:
   - Solución: if countdown == KNIFE_COOLDOWN:
   
4. **No considerar casos edge en colisiones**:
   - Problema: No verificar si el objeto ya fue eliminado
   - Solución: Verificar existencia antes de eliminar
   
5. **Mezclar lógica de game states**:
   - Problema: Actualizar juego durante pausa
   - Solución: Cada estado maneja solo su propia lógica

6. **No optimizar el rendimiento**:
   - Problema: Crear muchos objetos cada frame
   - Solución: Reutilizar objetos y límites razonables

EJERCICIOS AVANZADOS PARA ESTUDIANTES:

1. **Implementar fade in/out entre estados**:
   - Crear superficie semi-transparente que cambia alpha
   
2. **Añadir más tipos de power-ups**:
   - Multiplicador de puntuación temporal
   - Cuchillos múltiples
   - Tiempo ralentizado
   
3. **Sistema de ondas de enemigos**:
   - Patrones predefinidos de aparición
   - Jefes cada cierto número de ondas
   
4. **Mejoras de audio**:
   - Música de fondo con cambio según estado
   - Efectos de sonido direccionales
   
5. **Persistencia avanzada**:
   - Guardar configuración de controles
   - Sistema de logros desbloqueables
   - Historial de puntuaciones

ARQUITECTURA EXTENSIBLE:

Este código está diseñado para ser fácilmente extensible:
- Nuevos tipos de entidades: heredar de clases base
- Nuevos estados: implementar interfaz de estados
- Nuevos efectos: añadir a sistemas existentes
- Nuevas mecánicas: integrar en update_game_logic()

La estructura modular permite que los estudiantes:
- Entiendan cada parte por separado
- Modifiquen componentes sin afectar otros
- Experimenten con nuevas ideas fácilmente
- Vean el impacto de sus cambios inmediatamente
"""