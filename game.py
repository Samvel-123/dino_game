from env import DinoGame
import pygame
if __name__ == "__main__":
    env = DinoGame()
    done = False
    obs, _ = env.reset()

    # Հրամաններ
    print("Սեղմեք SPACE կոճակը՝ թռիչք կատարելու համար։ Փակեք խաղի պատուհանը՝ դուրս գալու համար։")

    while not done:
        env.render()
        action = 0  # Բառարանական գործողություն՝ ոչինչ

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            # Թռիչք կատարելու գործողություն (SPACE կոճակ)
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                action = 1  # Թռիչք

        # Թարմացնում ենք վիճակը, վարձը և ստուգում ենք խաղի ավարտը
        obs, reward, done, truncated, info = env.step(action)

    env.close()