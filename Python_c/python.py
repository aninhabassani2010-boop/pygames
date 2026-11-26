import pygame
import os
import random
pygame.init()


screen_height = 600
screen_width = 990
screen = pygame.display.set_mode((screen_width, screen_height))

pygame.mixer.init()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

bg = os.path.join(BASE_DIR, "Assets", "Sound", "Fundo.mp3")
pygame.mixer.music.load(bg)

game_over_sound = pygame.mixer.Sound(os.path.join(BASE_DIR, "Assets", "Sound", "Dano.mp3"))

bite_83 = pygame.mixer.Sound(os.path.join(BASE_DIR, "Assets", "Sound", "Mordida.mp3"))



pygame.mixer.music.set_volume(0.6)  
pygame.mixer.music.play(-1)


Bones = pygame.image.load(os.path.join(BASE_DIR,"Assets/Other","bone.png"))

Running = [pygame.image.load(os.path.join(BASE_DIR,"Assets/Dog","DogRun1.png")), 
           pygame.image.load(os.path.join(BASE_DIR,"Assets/Dog","DogRun2.png"))]

Jumping = pygame.image.load(os.path.join(BASE_DIR,"Assets/Dog","Dogjump.png"))

Duking = [pygame.image.load(os.path.join(BASE_DIR,"Assets/Dog","DogDuck1.png")),
          pygame.image.load(os.path.join(BASE_DIR,"Assets/Dog","DogDuck2.png"))]

B_obstacle = [pygame.image.load(os.path.join(BASE_DIR,"Assets/Obstacle","Obstacle1.png")), 
              pygame.image.load(os.path.join(BASE_DIR,"Assets/Obstacle","Obstacle2.png")),
              pygame.image.load(os.path.join(BASE_DIR,"Assets/Obstacle","Obstacle3.png"))] 
            
S_obstacle = [pygame.image.load(os.path.join(BASE_DIR,"Assets/Obstacle","Obstacle4.png")),
              pygame.image.load(os.path.join(BASE_DIR,"Assets/Obstacle","Obstacle5.png")), 
              pygame.image.load(os.path.join(BASE_DIR,"Assets/Obstacle","Obstacle6.png"))]

Plane = [pygame.image.load(os.path.join(BASE_DIR,"Assets/Plane","Plane1.png")), 
         pygame.image.load(os.path.join(BASE_DIR,"Assets/Plane", "Plane2.png"))]
 
Cloud = pygame.image.load(os.path.join(BASE_DIR,"Assets/Other","Cloud.png"))
Bg = pygame.image.load(os.path.join(BASE_DIR,"Assets/Other","Track.png"))

#configuraçao
def sky(surface, top_color, bottom_color):
    width, height = surface.get_size()
    pixel_size = 8

    for y in range(0, height, pixel_size):
        ratio = y / height

        r = int(top_color[0] + (bottom_color[0] - top_color[0]) * ratio)
        g = int(top_color[1] + (bottom_color[1] - top_color[1]) * ratio)
        b = int(top_color[2] + (bottom_color[2] - top_color[2]) * ratio)

        pygame.draw.rect(
            surface,
            (r, g, b),
            (0, y, width, pixel_size)
        )

class CLOUD:
    def __init__(self):
        self.x = screen_width + random.randint(800, 1000)
        self.y = random.randint(50, 102)
        self.image = Cloud
        self.width = self.image.get_width()

    def update(self): 
        self.x -= game_speed
        if self.x < -self.width:
            self.x = screen_width + random.randint(2500, 3000)
            self.y = random.randint(50, 100)

    def draw(self, screen):   
        screen.blit(self.image, (self.x, self.y))
        
class Dog: 
    
    x_pos = 82
    y_pos = 310
    y_pos_duck = 342
    JUMP_VELOCI = 8.5
    
    def __init__(self):
        self.duck_img = Duking
        self.run_img = Running
        self.jump_img = Jumping
        
        self.dog_duck = False
        self.dog_run = True
        self.dog_jump = False
        
        self.step_index = 0
        self.jump_veloci = self.JUMP_VELOCI
        self.image = self.run_img[0]
        self.dog_rect = self.image.get_rect()
        self.dog_rect.x = self.x_pos
        self.dog_rect.y = self.y_pos
    
    def update(self, userinput):
        if self.dog_duck:
            self.duck()
        if self.dog_run:
            self.run()
        if self.dog_jump:
            self.jump()
      
        if self.step_index >= 10:
            self.step_index = 0
          
        if userinput[pygame.K_UP] and not self.dog_jump:      
            self.dog_duck = False
            self.dog_run = False
            self.dog_jump = True
        elif userinput[pygame.K_DOWN] and not self.dog_jump:
            self.dog_duck = True
            self.dog_run = False
            self.dog_jump = False
        elif not (self.dog_jump or userinput[pygame.K_DOWN]):
            self.dog_duck = False
            self.dog_run = True
            self.dog_jump = False
            
    def duck(self):
        self.image = self.duck_img[self.step_index // 5]
        self.dog_rect = self.image.get_rect()
        self.dog_rect.x = self.x_pos
        self.dog_rect.y = self.y_pos_duck
        self.step_index += 1
        
    def run(self):
        self.image = self.run_img[self.step_index // 5]
        self.dog_rect = self.image.get_rect()
        self.dog_rect.x = self.x_pos
        self.dog_rect.y = self.y_pos
        self.step_index += 1
    
    def jump(self):        
        self.image = self.jump_img
        if self.dog_jump:
            self.dog_rect.y -= self.jump_veloci * 4
            self.jump_veloci -= 0.8
        if self.jump_veloci < -self.JUMP_VELOCI:
            self.dog_jump = False
            self.jump_veloci = self.JUMP_VELOCI
    
    def draw(self, screen):
        screen.blit(self.image, (self.dog_rect.x, self.dog_rect.y))  

class bones:
        def __init__(self):
            self.image = Bones
            self.rect = self.image.get_rect()
            self.rect.x = screen_width + 350
            self.rect.y = random.randint(200,400)

        
        def update(self):
            self.rect.x -= game_speed
        
        def draw(self, screen):
            screen.blit(self.image, self.rect)

class Obstacles:
    def __init__(self, image, type):
        self.image = image
        self.type = type
        self.rect = self.image[self.type].get_rect()
        self.rect.x = screen_width
    
    def update(self):
        self.rect.x -= game_speed
        
    def draw(self, SCREEN):
        SCREEN.blit(self.image[self.type], self.rect)

class s_obstacle(Obstacles):
    def __init__(self, image):
        self.type = random.randint(0, 2)
        super().__init__(image, self.type)
        self.rect.y = 325
        
class b_obstacle(Obstacles):
    def __init__(self, image):
        self.type = random.randint(0, 2)
        super().__init__(image, self.type)
        self.rect.y = 310
        
class plane(Obstacles):
    def __init__(self, image):
        self.type = 0
        super().__init__(image, self.type)
        self.rect.y = 250
        self.index = 0
        
    def draw(self, SCREEN):
        if self.index >= 9:
            self.index = 0
        screen.blit(self.image[self.index // 5], self.rect)
        self.index += 1
    
def main():
    global game_speed, x_pos_bg, y_pos_bg, obstacles, death_count
    run = True
    clock = pygame.time.Clock()
    cloud = CLOUD()
    player = Dog()
    game_speed = 23
    x_pos_bg = 0
    y_pos_bg = 370
    obstacles = []
    death_count = 0
    bone_score = 0
    bone_items= []
    font = pygame.font.Font(None, 40)
    won=False
    obstacles_dodged = 0
    
    
    
    def background():
        global x_pos_bg, y_pos_bg
        image_width = Bg.get_width()
        screen.blit(Bg, (x_pos_bg, y_pos_bg))
        screen.blit(Bg, (x_pos_bg + image_width, y_pos_bg))
        
        if x_pos_bg <= -image_width:
            screen.blit(Bg, (image_width + x_pos_bg, y_pos_bg))
            x_pos_bg = 0
        x_pos_bg -= game_speed

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                
        sky(screen,(105, 160, 210),(255, 195, 155))
        
        userinput = pygame.key.get_pressed()
        background()
        cloud.draw(screen)
        cloud.update()
        player.draw(screen)
        player.update(userinput)
        
        if len(obstacles) == 0:
            rand_val = random.randint(0, 2)
            if rand_val == 0:
                obstacles.append(s_obstacle(S_obstacle))
            elif rand_val == 1:
                obstacles.append(b_obstacle(B_obstacle))
            elif rand_val == 2:
                obstacles.append(plane(Plane))


        for obstacle in obstacles[:]:
            obstacle.draw(screen)
            obstacle.update()
        
            
            if player.dog_rect.colliderect(obstacle.rect):
                pygame.mixer.music.stop()          
                game_over_sound.play()            
                pygame.time.delay(1500)               
                run = False  

            elif obstacle.rect.x < -obstacle.rect.width:
                for obstacle in obstacles[:]:
                    obstacles.remove(obstacle)
                    obstacles_dodged += 1

                if obstacles_dodged % 12 == 0:
                    bone_items.append(bones())
                
                
        for bone in bone_items[:]:
            bone.update()
            bone.draw(screen)

            if player.dog_rect.colliderect(bone.rect):
                bite_83.play()   
                bone_score += 1
                bone_items.remove(bone)

            elif bone.rect.x < -bone.rect.width:
                bone_items.remove(bone)
               
        if bone_score >= 10:
                        run = False
                        won = True
                     
        score_text = font.render(f"Ossos: {bone_score}/10",True,(255, 255, 255))
        screen.blit(score_text, (screen_width - score_text.get_width() - 20, 20))    
            
            
        clock.tick(30)
        pygame.display.update()


    def menu(deth_cont):
        run=True
        while run:
            screen.fill((255, 255, 255))
                   

if __name__ == "__main__":
    main()