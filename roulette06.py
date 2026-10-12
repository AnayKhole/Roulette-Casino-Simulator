import pygame
import math
import random
import time

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 1000, 700
CENTER_X, CENTER_Y = WIDTH // 2, HEIGHT // 2 - 50
WHEEL_RADIUS = 200
INNER_RADIUS = 30

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (220, 20, 20)
GREEN = (0, 150, 0)
GOLD = (255, 215, 0)
GRAY = (128, 128, 128)
DARK_GRAY = (64, 64, 64)
BLUE = (0, 100, 200)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)
LIGHT_BLUE = (173, 216, 230)
DARK_BLUE = (0, 0, 139)

# Roulette numbers and colors (European style)
NUMBERS = [0, 32, 15, 19, 4, 21, 2, 25, 17, 34, 6, 27, 13, 36, 11, 30, 8, 23, 10, 5, 24, 16, 33, 1, 20, 14, 31, 9, 22, 18, 29, 7, 28, 12, 35, 3, 26]
RED_NUMBERS = [1, 3, 5, 7, 9, 12, 14, 16, 18, 19, 21, 23, 25, 27, 30, 32, 34, 36]
BLACK_NUMBERS = [2, 4, 6, 8, 10, 11, 13, 15, 17, 20, 22, 24, 26, 28, 29, 31, 33, 35]

class BankSystem:
    def __init__(self):
        self.showing = False
        self.loan_amount = 1000
        self.loan_offer = 0
        self.loan_percentage = 0
        self.win_rate = 0.0
        self.message = ""
        self.show_offer = False
        self.special_loan_mode = False
        self.interest_rate = 0
        self.outstanding_debt = 0  # Track total debt with interest
        
    def calculate_win_rate(self, game_history):
        if len(game_history) < 3:  # Need at least 3 games for loan
            return 0.0
        
        # Look at last 10 games maximum
        recent_games = game_history[-10:]
        wins = sum(1 for result in recent_games if result)
        return (wins / len(recent_games)) * 100
    
    def request_loan(self, amount, game_history):
        self.loan_amount = amount
        self.win_rate = self.calculate_win_rate(game_history)
        
        if len(game_history) < 3:
            self.message = "You need at least 3 games played to qualify for a loan."
            self.show_offer = False
            self.special_loan_mode = False
            return False
        
        # Special high-risk loan for poor performers (50% or lower win rate)
        if self.win_rate <= 50:
            self.special_loan_mode = True
            self.interest_rate = max(25, 75 - int(self.win_rate))  # 25% to 75% interest based on how bad win rate is
            self.loan_offer = amount  # Give them exactly what they ask for
            self.message = f"⚠️ HIGH-RISK LOAN AVAILABLE ⚠️\nWin rate: {self.win_rate:.1f}% - You qualify for our special high-risk lending program!"
            self.show_offer = True
            return True
        
        # Standard loan logic for good performers (above 50%)
        if self.win_rate < 60:
            self.message = f"Loan DENIED. Win rate: {self.win_rate:.1f}% (minimum 60% required for standard loans)"
            self.show_offer = False
            self.special_loan_mode = False
            return False
        
        # Standard loan for good performers
        self.special_loan_mode = False
        self.loan_percentage = min(int(self.win_rate), 90)  # Cap at 90%
        self.loan_offer = int((self.loan_percentage / 100) * amount)
        self.interest_rate = 5  # Low interest for good performers
        
        self.message = f"Win rate: {self.win_rate:.1f}% - Since there's some risk involved with loaning you money, you will be given a lower amount."
        self.show_offer = True
        return True
    
    def draw(self, screen, font, big_font):
        if not self.showing:
            return
        
        # Draw semi-transparent overlay
        overlay = pygame.Surface((WIDTH, HEIGHT))
        overlay.set_alpha(128)
        overlay.fill(BLACK)
        screen.blit(overlay, (0, 0))
        
        # Draw bank panel background (now on top of overlay)
        panel_rect = pygame.Rect(150, 150, 700, 400)
        pygame.draw.rect(screen, DARK_BLUE, panel_rect)
        pygame.draw.rect(screen, GOLD, panel_rect, 3)
        
        # Bank title
        title_text = big_font.render("🏦 CASINO BANK 🏦", True, GOLD)
        title_rect = title_text.get_rect(center=(panel_rect.centerx, panel_rect.y + 40))
        screen.blit(title_text, title_rect)
        
        # Loan amount input area
        input_label = font.render("Loan Amount: $", True, WHITE)
        screen.blit(input_label, (panel_rect.x + 50, panel_rect.y + 100))
        
        # Loan amount display
        amount_text = font.render(str(self.loan_amount), True, WHITE)
        amount_rect = pygame.Rect(panel_rect.x + 180, panel_rect.y + 95, 100, 30)
        pygame.draw.rect(screen, WHITE, amount_rect, 2)
        screen.blit(amount_text, (amount_rect.x + 5, amount_rect.y + 5))
        
        # +/- buttons for loan amount
        minus_btn = pygame.Rect(panel_rect.x + 300, panel_rect.y + 95, 30, 30)
        plus_btn = pygame.Rect(panel_rect.x + 340, panel_rect.y + 95, 30, 30)
        pygame.draw.rect(screen, RED, minus_btn)
        pygame.draw.rect(screen, GREEN, plus_btn)
        
        minus_text = font.render("-", True, WHITE)
        plus_text = font.render("+", True, WHITE)
        screen.blit(minus_text, (minus_btn.centerx - 5, minus_btn.centery - 8))
        screen.blit(plus_text, (plus_btn.centerx - 5, plus_btn.centery - 8))
        
        # Request loan button
        request_btn = pygame.Rect(panel_rect.x + 400, panel_rect.y + 95, 120, 30)
        pygame.draw.rect(screen, BLUE, request_btn)
        pygame.draw.rect(screen, WHITE, request_btn, 2)
        request_text = font.render("Request Loan", True, WHITE)
        request_rect = request_text.get_rect(center=request_btn.center)
        screen.blit(request_text, request_rect)
        
        # Message area
        if self.message:
            # Word wrap the message
            words = self.message.split()
            lines = []
            current_line = ""
            
            for word in words:
                test_line = current_line + (" " if current_line else "") + word
                if font.size(test_line)[0] < 600:  # Max width
                    current_line = test_line
                else:
                    if current_line:
                        lines.append(current_line)
                    current_line = word
            if current_line:
                lines.append(current_line)
            
            # Display message lines
            for i, line in enumerate(lines):
                msg_text = font.render(line, True, WHITE)
                screen.blit(msg_text, (panel_rect.x + 50, panel_rect.y + 160 + i * 25))
        
        # Show offer if available
        if self.show_offer:
            offer_y = panel_rect.y + 260
            
            if self.special_loan_mode:
                # Special high-risk loan display
                offer_text1 = font.render(f"🔥 HIGH-RISK LOAN: ${self.loan_offer} (FULL AMOUNT!)", True, ORANGE)
                screen.blit(offer_text1, (panel_rect.x + 50, offer_y))
                
                interest_text = font.render(f"⚠️ Interest Rate: {self.interest_rate}% (Added to your debt immediately)", True, RED)
                screen.blit(interest_text, (panel_rect.x + 50, offer_y + 25))
                
                debt_amount = int(self.loan_offer * (1 + self.interest_rate / 100))
                debt_text = font.render(f"Total Debt if Accepted: ${debt_amount}", True, YELLOW)
                screen.blit(debt_text, (panel_rect.x + 50, offer_y + 50))
                
                # Warning text
                warning_text = font.render("⚠️ WARNING: This loan must be repaid with interest!", True, RED)
                screen.blit(warning_text, (panel_rect.x + 50, offer_y + 75))
            else:
                # Standard loan display
                offer_text1 = font.render(f"Approved Amount: ${self.loan_offer} ({self.loan_percentage}% of ${self.loan_amount})", True, GREEN)
                screen.blit(offer_text1, (panel_rect.x + 50, offer_y))
                
                interest_text = font.render(f"Interest Rate: {self.interest_rate}%", True, WHITE)
                screen.blit(interest_text, (panel_rect.x + 50, offer_y + 25))
            
            # Accept/Decline buttons (adjust position for special loan)
            button_y_offset = 100 if self.special_loan_mode else 40
            accept_btn = pygame.Rect(panel_rect.x + 200, offer_y + button_y_offset, 100, 35)
            decline_btn = pygame.Rect(panel_rect.x + 320, offer_y + button_y_offset, 100, 35)
            
            accept_color = ORANGE if self.special_loan_mode else GREEN
            pygame.draw.rect(screen, accept_color, accept_btn)
            pygame.draw.rect(screen, RED, decline_btn)
            pygame.draw.rect(screen, WHITE, accept_btn, 2)
            pygame.draw.rect(screen, WHITE, decline_btn, 2)
            
            accept_text = font.render("ACCEPT", True, WHITE)
            decline_text = font.render("DECLINE", True, WHITE)
            
            accept_rect = accept_text.get_rect(center=accept_btn.center)
            decline_rect = decline_text.get_rect(center=decline_btn.center)
            
            screen.blit(accept_text, accept_rect)
            screen.blit(decline_text, decline_rect)
        
        # Close button
        close_btn = pygame.Rect(panel_rect.x + panel_rect.width - 80, panel_rect.y + 20, 60, 30)
        pygame.draw.rect(screen, RED, close_btn)
        pygame.draw.rect(screen, WHITE, close_btn, 2)
        close_text = font.render("CLOSE", True, WHITE)
        close_rect = close_text.get_rect(center=close_btn.center)
        screen.blit(close_text, close_rect)
        
    def handle_click(self, pos):
        if not self.showing:
            return None
        
        x, y = pos
        panel_rect = pygame.Rect(150, 150, 700, 400)
        
        # Close button
        close_btn = pygame.Rect(panel_rect.x + panel_rect.width - 80, panel_rect.y + 20, 60, 30)
        if close_btn.collidepoint(pos):
            self.showing = False
            return "close"
        
        # Loan amount adjustment buttons
        minus_btn = pygame.Rect(panel_rect.x + 300, panel_rect.y + 95, 30, 30)
        plus_btn = pygame.Rect(panel_rect.x + 340, panel_rect.y + 95, 30, 30)
        
        if minus_btn.collidepoint(pos) and self.loan_amount > 100:
            self.loan_amount -= 100
            return "adjust"
        
        if plus_btn.collidepoint(pos) and self.loan_amount < 10000:
            self.loan_amount += 100
            return "adjust"
        
        # Request loan button
        request_btn = pygame.Rect(panel_rect.x + 400, panel_rect.y + 95, 120, 30)
        if request_btn.collidepoint(pos):
            return "request"
        
        # Accept/Decline buttons (only if offer is showing)
        if self.show_offer:
            offer_y = panel_rect.y + 260
            button_y_offset = 100 if self.special_loan_mode else 40
            accept_btn = pygame.Rect(panel_rect.x + 200, offer_y + button_y_offset, 100, 35)
            decline_btn = pygame.Rect(panel_rect.x + 320, offer_y + button_y_offset, 100, 35)
            
            if accept_btn.collidepoint(pos):
                return "accept"
            
            if decline_btn.collidepoint(pos):
                self.show_offer = False
                self.special_loan_mode = False
                self.message = "Loan declined."
                return "decline"
        
        return None

class RouletteWheel:
    def __init__(self):
        self.angle = 0
        self.spinning = False
        self.spin_speed = 0
        self.spin_decay = 0.995
        self.min_spin_speed = 0.5
        self.result = None
        
        # Ball animation
        self.ball_angle = 0
        self.ball_speed = 0
        self.ball_radius = WHEEL_RADIUS - 15  # Ball moves on outer rim
        self.ball_spinning = False
        
        # Smooth animation variables
        self.target_angle = 0
        self.angle_velocity = 0
        self.smoothing = 0.1
        
    def spin(self, force_duration=None):
        if not self.spinning:
            self.spinning = True
            self.ball_spinning = True
            
            if force_duration:
                # Adjust spin speed to achieve desired duration
                self.spin_speed = random.uniform(15, 25) * force_duration
                self.ball_speed = random.uniform(20, 30) * force_duration  # Ball moves faster than wheel
                self.spin_decay = 0.992 + (force_duration - 1.0) * 0.002
            else:
                self.spin_speed = random.uniform(18, 28)  # Smoother speed range
                self.ball_speed = random.uniform(25, 35)  # Ball starts faster
                self.spin_decay = 0.995
                
            self.result = None
            
    def update(self):
        if self.spinning:
            # Smooth wheel rotation
            self.target_angle += self.spin_speed
            self.angle += (self.target_angle - self.angle) * self.smoothing
            
            # Ball animation (moves in opposite direction, faster)
            if self.ball_spinning:
                self.ball_angle -= self.ball_speed * 1.2  # Opposite direction, faster
                self.ball_speed *= 0.998  # Ball slows down faster than wheel
                
                # Ball stops first
                if self.ball_speed < 0.5:
                    self.ball_spinning = False
            
            # Wheel continues spinning
            self.spin_speed *= self.spin_decay
            
            # Wheel stops when very slow
            if self.spin_speed < 0.3:
                self.spinning = False
                self.ball_spinning = False
                self.spin_speed = 0
                self.ball_speed = 0
                
                # Calculate result based on where ball stopped
                if hasattr(self, 'force_win_number'):
                    target_number = self.force_win_number
                    target_index = NUMBERS.index(target_number)
                    segment_size = 360 / len(NUMBERS)
                    # Position ball to land on target number
                    self.ball_angle = -(target_index * segment_size) + random.uniform(-5, 5)  # Small random offset for realism
                    self.result = target_number
                    delattr(self, 'force_win_number')
                else:
                    # Normal result calculation based on ball position
                    segment_size = 360 / len(NUMBERS)
                    # Convert ball angle to segment index
                    ball_segment = int((-self.ball_angle) % 360 / segment_size) % len(NUMBERS)
                    self.result = NUMBERS[ball_segment]
                
    def draw(self, screen, font):
        # Draw wheel segments with smooth rotation
        segment_angle = 360 / len(NUMBERS)
        
        for i, number in enumerate(NUMBERS):
            start_angle = i * segment_angle + self.angle
            end_angle = (i + 1) * segment_angle + self.angle
            
            # Determine color
            if number == 0:
                color = GREEN
            elif number in RED_NUMBERS:
                color = RED
            else:
                color = BLACK
                
            # Add pulsing effect to winning number
            if hasattr(self, 'winning_pulse') and number == self.result and not self.spinning:
                pulse_factor = 1 + 0.1 * math.sin(self.winning_pulse * 8)
                pulse_radius = int(WHEEL_RADIUS * pulse_factor)
            else:
                pulse_radius = WHEEL_RADIUS
                
            # Draw segment
            points = [
                (CENTER_X, CENTER_Y),
                (CENTER_X + pulse_radius * math.cos(math.radians(start_angle)),
                 CENTER_Y + pulse_radius * math.sin(math.radians(start_angle))),
                (CENTER_X + pulse_radius * math.cos(math.radians(end_angle)),
                 CENTER_Y + pulse_radius * math.sin(math.radians(end_angle)))
            ]
            pygame.draw.polygon(screen, color, points)
            pygame.draw.polygon(screen, WHITE, points, 2)
            
            # Draw numbers
            text_angle = start_angle + segment_angle / 2
            text_radius = pulse_radius - 30
            text_x = CENTER_X + text_radius * math.cos(math.radians(text_angle))
            text_y = CENTER_Y + text_radius * math.sin(math.radians(text_angle))
            
            text_color = WHITE if color != WHITE else BLACK
            text_surface = font.render(str(number), True, text_color)
            text_rect = text_surface.get_rect(center=(text_x, text_y))
            screen.blit(text_surface, text_rect)
        
        # Draw ball
        ball_x = CENTER_X + self.ball_radius * math.cos(math.radians(self.ball_angle))
        ball_y = CENTER_Y + self.ball_radius * math.sin(math.radians(self.ball_angle))
        
        # Ball with glow effect
        if self.ball_spinning:
            # Moving ball - white with motion blur effect
            pygame.draw.circle(screen, WHITE, (int(ball_x), int(ball_y)), 8)
            pygame.draw.circle(screen, LIGHT_BLUE, (int(ball_x), int(ball_y)), 6)
        else:
            # Stationary ball - brighter
            pygame.draw.circle(screen, WHITE, (int(ball_x), int(ball_y)), 10)
            pygame.draw.circle(screen, YELLOW, (int(ball_x), int(ball_y)), 7)
            pygame.draw.circle(screen, BLACK, (int(ball_x), int(ball_y)), 10, 2)
        
        # Draw center circle with breathing animation
        time_factor = time.time() * 3  # Speed of breathing
        breath_size = INNER_RADIUS + int(5 * math.sin(time_factor))
        pygame.draw.circle(screen, YELLOW, (CENTER_X, CENTER_Y), breath_size)
        pygame.draw.circle(screen, BLACK, (CENTER_X, CENTER_Y), breath_size, 3)
        
        # Draw pointer (ball indicator) - Now pointing down into the wheel
        pointer_points = [
            (CENTER_X, CENTER_Y - WHEEL_RADIUS + 5),  # Point now points down
            (CENTER_X - 10, CENTER_Y - WHEEL_RADIUS - 15),
            (CENTER_X + 10, CENTER_Y - WHEEL_RADIUS - 15)
        ]
        pygame.draw.polygon(screen, GOLD, pointer_points)
        pygame.draw.polygon(screen, BLACK, pointer_points, 2)

    def get_segment_at_angle(self, click_angle):
        """Get the number segment at a given angle relative to the wheel"""
        segment_size = 360 / len(NUMBERS)
        
        # Convert click angle to wheel-relative angle
        wheel_relative_angle = (click_angle - self.angle) % 360
        
        # The pointer is at the top (270 degrees in screen coordinates, but 0 in wheel coordinates)
        # We need to find which segment the pointer would hit if it were at this angle
        pointer_relative_angle = (270 - wheel_relative_angle) % 360
        
        # Convert to segment index
        segment = int(pointer_relative_angle / segment_size)
        segment = segment % len(NUMBERS)  # Ensure we stay within bounds
        
        return NUMBERS[segment]

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Roulette Wheel with Bank")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 24)
        self.big_font = pygame.font.Font(None, 36)
        self.huge_font = pygame.font.Font(None, 48)
        
        self.wheel = RouletteWheel()
        self.bank = BankSystem()
        self.balance = 10000
        self.bet_amount = 100
        self.current_bet = None
        self.bet_type = None
        self.last_result = None
        self.message = "Place your bet!"
        self.message_timer = 0
        
        # Game history for bank system (True = win, False = loss)
        self.game_history = []
        
        # Cheat system - click yellow center 4 times to activate
        self.cheat_clicks = 0
        self.cheat_active = False
        self.cheat_indicator_timer = 0
        
        # Text input for bet amount
        self.text_input_active = False
        self.text_input_value = ""
        
    def get_clicked_segment(self, click_angle):
        """More accurate method to determine which segment was clicked"""
        segment_size = 360 / len(NUMBERS)
        
        # Convert screen angle to wheel angle (accounting for current rotation)
        # Screen angles: 0° = right, 90° = down, 180° = left, 270° = up
        # We need to map this to our wheel coordinate system
        wheel_angle = (self.wheel.angle + click_angle) % 360
        
        # Find which segment this corresponds to
        # The wheel segments start from 0° and go clockwise
        segment_index = int(wheel_angle / segment_size) % len(NUMBERS)
        
        return NUMBERS[segment_index]

    def get_current_pointer_segment(self):
        """Get the segment that the pointer is currently pointing to"""
        segment_size = 360 / len(NUMBERS)
        # Pointer is at top, so we need to find which segment is at 270 degrees (top)
        adjusted_angle = (360 - (self.wheel.angle % 360) + (segment_size / 2)) % 360
        segment = int(adjusted_angle // segment_size)
        return segment % len(NUMBERS)
        
    def draw_hazard_symbol(self, screen, x, y, size=20):
        """Draw a triangular hazard warning symbol"""
        # Outer yellow triangle
        points = [
            (x, y - size),  # Top point
            (x - size * 0.866, y + size * 0.5),  # Bottom left
            (x + size * 0.866, y + size * 0.5)   # Bottom right
        ]
        pygame.draw.polygon(screen, YELLOW, points)
        pygame.draw.polygon(screen, BLACK, points, 2)
        
        # Inner exclamation mark
        # Vertical line
        pygame.draw.line(screen, BLACK, (x, y - size * 0.6), (x, y - size * 0.1), 3)
        # Dot
        pygame.draw.circle(screen, BLACK, (x, y + size * 0.2), 2)
        
    def handle_bet(self, bet_type, bet_value=None):
        if self.wheel.spinning:
            print("Cannot bet while wheel is spinning!")
            return
        if self.balance < self.bet_amount:
            print(f"Insufficient funds! Balance: ${self.balance}, Bet: ${self.bet_amount}")
            return
            
        self.current_bet = bet_value if bet_value is not None else bet_type
        self.bet_type = bet_type
        self.balance -= self.bet_amount
        self.message = f"Bet placed: ${self.bet_amount} on {bet_type}"
        if bet_value is not None:
            self.message += f" {bet_value}"
        self.message_timer = time.time()
        print(f"BET SUCCESSFULLY PLACED: {bet_type}, Balance now: ${self.balance}")
        
        # Activate cheat if active and set winning number for ALL bet types
        if self.cheat_active:
            # Handle ALL bet types to guarantee wins
            if self.bet_type == "Red":
                self.wheel.force_win_number = random.choice(RED_NUMBERS)
            elif self.bet_type == "Black":
                self.wheel.force_win_number = random.choice(BLACK_NUMBERS)
            elif self.bet_type == "Even":
                evens = [n for n in range(2, 37, 2)]
                self.wheel.force_win_number = random.choice(evens)
            elif self.bet_type == "Odd":
                odds = [n for n in range(1, 37, 2)]
                self.wheel.force_win_number = random.choice(odds)
            elif self.bet_type == "Low":
                self.wheel.force_win_number = random.choice(range(1, 19))
            elif self.bet_type == "High":
                self.wheel.force_win_number = random.choice(range(19, 37))
            elif self.bet_type == "Number":
                # For number bets, force the exact number they bet on
                self.wheel.force_win_number = self.current_bet
            elif self.bet_type == "Column":
                # Add column support if needed
                column_numbers = []
                if self.current_bet == 1:
                    column_numbers = [1, 4, 7, 10, 13, 16, 19, 22, 25, 28, 31, 34]
                elif self.current_bet == 2:
                    column_numbers = [2, 5, 8, 11, 14, 17, 20, 23, 26, 29, 32, 35]
                elif self.current_bet == 3:
                    column_numbers = [3, 6, 9, 12, 15, 18, 21, 24, 27, 30, 33, 36]
                if column_numbers:
                    self.wheel.force_win_number = random.choice(column_numbers)
            elif self.bet_type == "Dozen":
                # Add dozen support if needed
                if self.current_bet == 1:
                    self.wheel.force_win_number = random.choice(range(1, 13))
                elif self.current_bet == 2:
                    self.wheel.force_win_number = random.choice(range(13, 25))
                elif self.current_bet == 3:
                    self.wheel.force_win_number = random.choice(range(25, 37))
                    
            print(f"CHEAT ACTIVATED: Forcing win number {getattr(self.wheel, 'force_win_number', 'None')} for bet {self.bet_type}")
            
            # Set cheat duration for smooth animation
            target_index = NUMBERS.index(getattr(self.wheel, 'force_win_number', NUMBERS[0]))
            current_pointer_segment = self.get_current_pointer_segment()
            
            # Calculate distance to target
            distance = (target_index - current_pointer_segment) % len(NUMBERS)
            
            # Adjust spin duration based on distance
            if distance <= len(NUMBERS) // 4:
                self.wheel.cheat_duration = 0.8
            elif distance >= 3 * len(NUMBERS) // 4:
                self.wheel.cheat_duration = 1.3
            else:
                self.wheel.cheat_duration = 1.0
        
    def calculate_payout(self):
        if self.current_bet is None:
            return 0
            
        result = self.wheel.result
        
        # Normal payout calculations (cheat is now handled by forcing the wheel result)
        if self.bet_type == "Number" and self.current_bet == result:
            return self.bet_amount * 36  # 35:1 + original bet
        elif self.bet_type == "Red" and result in RED_NUMBERS:
            return self.bet_amount * 2  # 1:1 + original bet
        elif self.bet_type == "Black" and result in BLACK_NUMBERS:
            return self.bet_amount * 2
        elif self.bet_type == "Even" and result != 0 and result % 2 == 0:
            return self.bet_amount * 2
        elif self.bet_type == "Odd" and result % 2 == 1:
            return self.bet_amount * 2
        elif self.bet_type == "Low" and 1 <= result <= 18:
            return self.bet_amount * 2
        elif self.bet_type == "High" and 19 <= result <= 36:
            return self.bet_amount * 2
            
        return 0
        
    def draw_ui(self):
        # Background
        self.screen.fill(DARK_GRAY)
        
        # Title
        title = self.huge_font.render("ROULETTE", True, GOLD)
        title_rect = title.get_rect(center=(WIDTH // 2, 30))
        self.screen.blit(title, title_rect)
        
        # Balance with hazard symbol and debt indicator
        balance_text = self.big_font.render(f"Balance: ${self.balance}", True, WHITE)
        self.screen.blit(balance_text, (20, 20))
        
        # Show outstanding debt if any
        if self.bank.outstanding_debt > 0:
            debt_text = self.font.render(f"Debt: ${self.bank.outstanding_debt}", True, RED)
            self.screen.blit(debt_text, (20, 50))
        
        # Draw hazard symbol with pulsing animation
        hazard_x = 20 + balance_text.get_width() + 15
        hazard_y = 35
        pulse_time = time.time() * 4  # Faster pulse for hazard
        pulse_size = 15 + int(3 * math.sin(pulse_time))
        self.draw_hazard_symbol(self.screen, hazard_x, hazard_y, pulse_size)
        
        # Bank button - only show when balance is low, with pulsing animation
        if self.balance < self.bet_amount:
            bank_btn = pygame.Rect(WIDTH - 120, 20, 100, 35)
            pulse_time = time.time() * 2
            pulse_intensity = 0.3 + 0.2 * math.sin(pulse_time)
            bank_color = tuple(int(c * pulse_intensity + LIGHT_BLUE[i] * (1 - pulse_intensity)) for i, c in enumerate([255, 255, 255]))
            
            pygame.draw.rect(self.screen, bank_color, bank_btn)
            pygame.draw.rect(self.screen, DARK_BLUE, bank_btn, 2)
            bank_text = self.font.render("🏦 BANK", True, DARK_BLUE)
            bank_rect = bank_text.get_rect(center=bank_btn.center)
            self.screen.blit(bank_text, bank_rect)
        
        # Bet amount with text input
        bet_text = self.font.render(f"Bet Amount: $", True, WHITE)
        self.screen.blit(bet_text, (20, 60))
        
        # Text input box for bet amount
        input_rect = pygame.Rect(135, 58, 100, 25)
        input_color = WHITE if self.text_input_active else GRAY
        pygame.draw.rect(self.screen, input_color, input_rect, 2)
        
        # Display current bet amount or input value
        display_value = self.text_input_value if self.text_input_active else str(self.bet_amount)
        input_text = self.font.render(display_value, True, WHITE)
        self.screen.blit(input_text, (input_rect.x + 5, input_rect.y + 3))
        
        # Show cursor if text input is active
        if self.text_input_active:
            cursor_x = input_rect.x + 5 + self.font.size(display_value)[0]
            pygame.draw.line(self.screen, WHITE, (cursor_x, input_rect.y + 3), (cursor_x, input_rect.y + 22), 1)
        
        # Apply button for text input
        if self.text_input_active and self.text_input_value:
            apply_btn = pygame.Rect(245, 58, 60, 25)
            pygame.draw.rect(self.screen, GREEN, apply_btn)
            pygame.draw.rect(self.screen, WHITE, apply_btn, 2)
            apply_text = self.font.render("Apply", True, WHITE)
            apply_rect = apply_text.get_rect(center=apply_btn.center)
            self.screen.blit(apply_text, apply_rect)
        
        # Controls
        controls_y = HEIGHT - 200
        
        # Bet amount controls (+ and - buttons)
        pygame.draw.rect(self.screen, BLUE, (20, controls_y, 60, 30))
        pygame.draw.rect(self.screen, BLUE, (90, controls_y, 60, 30))
        minus_text = self.font.render("-", True, WHITE)
        plus_text = self.font.render("+", True, WHITE)
        self.screen.blit(minus_text, (45, controls_y + 8))
        self.screen.blit(plus_text, (115, controls_y + 8))
        
        # Betting buttons - Make them bigger and easier to click
        button_width = 90
        button_height = 35
        button_y = controls_y + 40
        
        buttons = [
            ("Red", RED, 20),
            ("Black", BLACK, 120),
            ("Even", BLUE, 220),
            ("Odd", BLUE, 320),
            ("Low", BLUE, 420),
            ("High", BLUE, 520)
        ]
        
        for text, color, x in buttons:
            pygame.draw.rect(self.screen, color, (x, button_y, button_width, button_height))
            pygame.draw.rect(self.screen, WHITE, (x, button_y, button_width, button_height), 2)
            btn_text = self.font.render(text, True, WHITE)
            text_rect = btn_text.get_rect(center=(x + button_width // 2, button_y + button_height // 2))
            self.screen.blit(btn_text, text_rect)
        
        # Spin button
        spin_color = GREEN if not self.wheel.spinning else GRAY
        pygame.draw.rect(self.screen, spin_color, (WIDTH // 2 - 50, button_y + 50, 100, 40))
        pygame.draw.rect(self.screen, WHITE, (WIDTH // 2 - 50, button_y + 50, 100, 40), 2)
        spin_text = self.big_font.render("SPIN", True, WHITE)
        spin_rect = spin_text.get_rect(center=(WIDTH // 2, button_y + 70))
        self.screen.blit(spin_text, spin_rect)
        
        # Messages
        if time.time() - self.message_timer < 3:
            msg_text = self.font.render(self.message, True, WHITE)
            self.screen.blit(msg_text, (20, HEIGHT - 60))
            
        # Last result
        if self.last_result is not None:
            result_color = GREEN if self.last_result == 0 else (RED if self.last_result in RED_NUMBERS else BLACK)
            result_text = self.big_font.render(f"Last Result: {self.last_result}", True, result_color)
            self.screen.blit(result_text, (WIDTH - 200, 20))
            
        # Very subtle cheat indicator with pulsing animation
        if self.cheat_active and time.time() - self.cheat_indicator_timer < 2:
            pulse_time = time.time() * 6
            alpha = int(128 + 127 * math.sin(pulse_time))
            cheat_color = (*GOLD, alpha) if len(GOLD) == 3 else GOLD
            cheat_text = self.font.render("✦", True, GOLD)  # Changed to a subtle star symbol
            self.screen.blit(cheat_text, (WIDTH - 30, HEIGHT - 30))
            
        # Add winning pulse timer update
        if hasattr(self.wheel, 'winning_pulse'):
            self.wheel.winning_pulse += 0.1
            if self.wheel.winning_pulse > 20:  # Stop pulsing after a while
                delattr(self.wheel, 'winning_pulse')
        
        # Win rate display (for debugging bank system)
        if len(self.game_history) > 0:
            wins = sum(1 for result in self.game_history[-10:] if result)
            games = len(self.game_history[-10:])
            win_rate = (wins / games) * 100
            rate_text = self.font.render(f"Win Rate (last 10): {win_rate:.1f}%", True, GRAY)
            self.screen.blit(rate_text, (20, HEIGHT - 30))
            
    def handle_click(self, pos):
        x, y = pos
        
        # Handle bank system clicks first (bank is drawn last so it's on top)
        if self.bank.showing:
            bank_action = self.bank.handle_click(pos)
            if bank_action == "request":
                success = self.bank.request_loan(self.bank.loan_amount, self.game_history)
                return
            elif bank_action == "accept":
                # Calculate total debt with interest
                if self.bank.special_loan_mode:
                    debt_with_interest = int(self.bank.loan_offer * (1 + self.bank.interest_rate / 100))
                    self.bank.outstanding_debt += debt_with_interest
                    self.balance += self.bank.loan_offer
                    self.message = f"HIGH-RISK LOAN APPROVED! ${self.bank.loan_offer} added. Total debt: ${self.bank.outstanding_debt}"
                else:
                    debt_with_interest = int(self.bank.loan_offer * (1 + self.bank.interest_rate / 100))
                    self.bank.outstanding_debt += debt_with_interest
                    self.balance += self.bank.loan_offer
                    self.message = f"Loan approved! ${self.bank.loan_offer} added. Debt: ${self.bank.outstanding_debt}"
                
                self.message_timer = time.time()
                self.bank.showing = False
                return
            elif bank_action:
                return  # Other bank actions handled
        
        controls_y = HEIGHT - 200
        button_y = controls_y + 40
        
        # Bank button
        if self.balance < self.bet_amount:
            bank_btn = pygame.Rect(WIDTH - 120, 20, 100, 35)
            if bank_btn.collidepoint(pos):
                self.bank.showing = True
                self.bank.show_offer = False  # Reset offer display
                return
        
        # Text input box for bet amount
        input_rect = pygame.Rect(135, 58, 100, 25)
        if input_rect.collidepoint(pos):
            self.text_input_active = True
            self.text_input_value = str(self.bet_amount)
            return
        
        # Apply button for text input
        if self.text_input_active and self.text_input_value:
            apply_btn = pygame.Rect(245, 58, 60, 25)
            if apply_btn.collidepoint(pos):
                try:
                    new_amount = int(self.text_input_value)
                    if new_amount > 0:
                        self.bet_amount = new_amount
                        self.text_input_active = False
                        self.text_input_value = ""
                        print(f"Bet amount set to: ${self.bet_amount}")
                except ValueError:
                    print("Invalid bet amount entered")
                return
        
        # Click elsewhere to deactivate text input
        if self.text_input_active:
            self.text_input_active = False
            self.text_input_value = ""
        
        # Check if clicking on the wheel center (for cheat activation)
        wheel_distance = math.sqrt((x - CENTER_X)**2 + (y - CENTER_Y)**2)
        if wheel_distance <= INNER_RADIUS:  # Clicked on yellow center
            self.cheat_clicks += 1
            if self.cheat_clicks >= 4:
                self.cheat_active = True
                self.cheat_indicator_timer = time.time()
                self.cheat_clicks = 0  # Reset counter
                print("CHEAT MODE ACTIVATED! (very quietly)")
        
        # Bet amount controls (+ and - buttons)
        if controls_y <= y <= controls_y + 30:
            if 20 <= x <= 80 and self.bet_amount > 5:
                self.bet_amount -= 5
                print(f"Bet amount decreased to: ${self.bet_amount}")
            elif 90 <= x <= 150:
                self.bet_amount += 5
                print(f"Bet amount increased to: ${self.bet_amount}")
                
        # Betting buttons - Updated click areas to match new button sizes
        if button_y <= y <= button_y + 35:  # Updated height
            if 20 <= x <= 110:  # Red button
                self.handle_bet("Red")
                print("Red bet placed!")
            elif 120 <= x <= 210:  # Black button
                self.handle_bet("Black")
                print("Black bet placed!")
            elif 220 <= x <= 310:  # Even button
                self.handle_bet("Even")
                print("Even bet placed!")
            elif 320 <= x <= 410:  # Odd button
                self.handle_bet("Odd")
                print("Odd bet placed!")
            elif 420 <= x <= 510:  # Low button
                self.handle_bet("Low")
                print("Low bet placed!")
            elif 520 <= x <= 610:  # High button
                self.handle_bet("High")
                print("High bet placed!")
                
        # Spin button
        if (button_y + 50 <= y <= button_y + 90 and 
            WIDTH // 2 - 50 <= x <= WIDTH // 2 + 50):
            print(f"Spin button clicked! Current bet: {self.current_bet}, Spinning: {self.wheel.spinning}")
            if not self.wheel.spinning and self.current_bet is not None:
                # Use cheat duration if available
                duration = getattr(self.wheel, 'cheat_duration', None)
                self.wheel.spin(duration)
                if duration:
                    delattr(self.wheel, 'cheat_duration')  # Clean up
                print("Wheel is now spinning!")
            else:
                if self.wheel.spinning:
                    print("Wheel is already spinning!")
                if self.current_bet is None:
                    print("No bet placed yet!")
    
    def handle_keypress(self, event):
        """Handle keyboard input for text input"""
        if self.text_input_active:
            if event.key == pygame.K_RETURN:
                # Apply the bet amount
                try:
                    new_amount = int(self.text_input_value)
                    if new_amount > 0:
                        self.bet_amount = new_amount
                        self.text_input_active = False
                        self.text_input_value = ""
                        print(f"Bet amount set to: ${self.bet_amount}")
                except ValueError:
                    print("Invalid bet amount entered")
            elif event.key == pygame.K_ESCAPE:
                # Cancel text input
                self.text_input_active = False
                self.text_input_value = ""
            elif event.key == pygame.K_BACKSPACE:
                # Remove last character
                self.text_input_value = self.text_input_value[:-1]
            elif event.unicode.isdigit() and len(self.text_input_value) < 8:
                # Add digit (limit to 8 characters)
                self.text_input_value += event.unicode
            
    def run(self):
        running = True
        
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.handle_click(event.pos)
                elif event.type == pygame.KEYDOWN:
                    self.handle_keypress(event)
                    
            # Update wheel
            was_spinning = self.wheel.spinning
            self.wheel.update()
            
            # Check if spin just finished
            if was_spinning and not self.wheel.spinning and self.wheel.result is not None:
                payout = self.calculate_payout()
                self.balance += payout
                self.last_result = self.wheel.result
                
                # Record game result for bank system
                won = payout > 0
                self.game_history.append(won)
                
                # Add winning pulse animation for winning number
                if won and payout > self.bet_amount:
                    self.wheel.winning_pulse = 0
                
                # Auto-repay debt if player has money and debt exists
                if self.balance > 0 and self.bank.outstanding_debt > 0:
                    repayment = min(self.balance, self.bank.outstanding_debt)
                    self.balance -= repayment
                    self.bank.outstanding_debt -= repayment
                    debt_repay_msg = f" (${repayment} auto-repaid toward debt)"
                else:
                    debt_repay_msg = ""
                
                if payout > 0:
                    self.message = f"You won ${payout}!{debt_repay_msg}"
                else:
                    self.message = f"You lost. Result: {self.wheel.result}{debt_repay_msg}"
                    
                self.message_timer = time.time()
                self.current_bet = None
                self.bet_type = None
                
                # Deactivate cheat after one use (moved here so it happens after the spin)
                if self.cheat_active:
                    print("Cheat used! Deactivating...")
                    self.cheat_active = False
                    self.cheat_clicks = 0
                
            # Draw everything (wheel first, then UI, then bank on top)
            self.draw_ui()
            self.wheel.draw(self.screen, self.font)
            
            # Draw bank system LAST so it appears on top
            self.bank.draw(self.screen, self.font, self.big_font)
            
            pygame.display.flip()
            self.clock.tick(60)
            
        pygame.quit()

if __name__ == "__main__":
    game = Game()
    game.run()