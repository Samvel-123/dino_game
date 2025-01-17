import numpy as np
import gymnasium as gym
from gymnasium import spaces
import pygame


# Կոնստանտներ
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 400
DINO_WIDTH, DINO_HEIGHT = 40, 40
OBSTACLE_WIDTH, OBSTACLE_HEIGHT = 20, 40
GROUND_HEIGHT = 300
FONT_SIZE = 24
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
FPS = 60

class DinoGame(gym.Env):
    def __init__(self):
        super(DinoGame, self).__init__()

        # Գործողությունների տարածք: 0 = ոչինչ, 1 = թռիչք
        self.action_space = spaces.Discrete(2)

        # Հսկողության տարածք: 4 տարր՝ 
        # 1. Դինոյի Y դիրք, 2. Դինոյի ուղղահայաց արագություն,
        # 3. Խոչընդոտի X դիրք, 4. Խոչընդոտի արագություն
        self.observation_space = spaces.Box(low=0, high=np.array([SCREEN_HEIGHT, 100, SCREEN_WIDTH, SCREEN_WIDTH]), shape=(4,), dtype=np.float32)

        # Pygame կազմաձևում
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Google Dino Game")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont(None, FONT_SIZE)

    def reset(self, seed=None, options=None):
        super().reset(seed=seed)

        # Սկզբնական վիճակի սահմանում՝ Դինոյի և խոչընդոտի համար
        self.dino_y = GROUND_HEIGHT - DINO_HEIGHT
        self.dino_velocity = 0
        self.is_jumping = False
        self.obstacle_x = SCREEN_WIDTH
        self.obstacle_speed = 5  # Սկզբում դանդաղ արագություն
        self.reward = 0

        # Վերադարձնում ենք սկզբնական վիճակը՝ [Դինո Y, Դինո արագություն, Խոչընդոտ X, Խոչընդոտի արագություն]
        self.state = np.array([self.dino_y, self.dino_velocity, self.obstacle_x, self.obstacle_speed], dtype=np.float32)
        return self.state, {}

    def step(self, action):
        """ Դինո խաղի մեկ քայլ կատարելը:
            self: DinoGame միջավայր
            action: int գործողություն՝ 0-ը նշանակում է ոչինչ, 1-ը նշանակում է թռիչք
        """
        
        # Թռիչքի լոգիկա
        if action == 1 and not self.is_jumping:
            self.is_jumping = True
            self.dino_velocity = -18   # Սկզբնական թռիչքի արագություն

        # Արթմենության և թռիչքի համաժամանակը
        if self.is_jumping:
            self.dino_y += self.dino_velocity
            self.dino_velocity += 1  # Գրավիտացիայի ազդեցություն
            if self.dino_y >= GROUND_HEIGHT - DINO_HEIGHT:
                self.dino_y = GROUND_HEIGHT - DINO_HEIGHT
                self.is_jumping = False

        # Եթե score-ը փոքր է 2, արագությունը քիչ է, հետո ավելանում է 2-8-ի սահմաններում
        if self.reward < 2:
            self.obstacle_speed = 5  # Դանդաղ արագություն
        elif 2 <= self.reward <= 8:
            # Արագությունն ավելանում է ավելի արագ, մինչև score 8
            self.obstacle_speed = 5 + (self.reward - 2) * 2  # Արագության ավելացում 2 անգամ ավելանում է
        else:
            # Երբ score-ը 8-ից մեծ է, արագությունը կպահանջվի նույնը
            self.obstacle_speed = 21  # Արագությունը մնա նույնը score 8-ից հետո

        # Խոչընդոտի թարմացում
        self.obstacle_x -= self.obstacle_speed
        if self.obstacle_x < 0:
            self.obstacle_x = SCREEN_WIDTH
            self.reward += 1

        # Հանդիպման ստուգում (проверка столкновения)
        done = False
        if (self.dino_y + DINO_HEIGHT > GROUND_HEIGHT - OBSTACLE_HEIGHT and
            self.obstacle_x < 50 + DINO_WIDTH and
            self.obstacle_x + OBSTACLE_WIDTH > 50):
            done = True

        # Թարմացնում ենք վիճակը՝ [Դինո Y, Դինո արագություն, Խոչընդոտ X, Խոչընդոտի արագություն]
        self.state = np.array([self.dino_y, self.dino_velocity, self.obstacle_x, self.obstacle_speed], dtype=np.float32)
        reward = 1 if not done else -100  # Վարձը՝ -100 հանդիպման համար, մյուս դեպքում 1 յուրաքանչյուր քայլի համար

        return self.state, reward, done, False, {}

    def render(self, mode="human"):
        self.screen.fill(WHITE)

        # Գծում ենք գետը, Դինոյին և խոչընդոտը
        pygame.draw.line(self.screen, BLACK, (0, GROUND_HEIGHT), (SCREEN_WIDTH, GROUND_HEIGHT), 2)
        pygame.draw.rect(self.screen, BLACK, (50, self.dino_y, DINO_WIDTH, DINO_HEIGHT))  # Դինո
        pygame.draw.rect(self.screen, RED, (self.obstacle_x, GROUND_HEIGHT - OBSTACLE_HEIGHT, OBSTACLE_WIDTH, OBSTACLE_HEIGHT))  # Խոչընդոտ
        score_text = self.font.render(f"Score: {self.reward}", True, BLACK)

        self.screen.blit(score_text, (10, 10))

        pygame.display.flip()
        self.clock.tick(FPS)

        return self.screen

    def close(self):
        pygame.quit()

     