import pygame
import os
import random
pygame.init()

#global constants (width,height)
screen_height = 600
screen_width = 1100
screen = pygame.display.set_mode((screen_width, screen_height))

# add the images to the program

Running = [pygame.image.load(os.path.join("Assets/Dog","DogRun1.png")), 
           pygame.image.load(os.path.join("Assets/Dog","DogRun2.png"))]

Jumping = pygame.image.load(os.path.join("Assets/Dog","Dogjump.png"))

Duking = [pygame.image.load(os.path.join("Assets/Dog","DogDuck1.png")),
          pygame.image.load(os.path.join("Assets/Dog","DogDuck2.png"))]

Obstacle = [pygame.image.load(os.path.join("Assets/Obstacle","Obstacle1.png")), 
            pygame.image.load(os.path.join("Assets/Obstacle","Obstacle2.png")),
            pygame.image.load(os.path.join("Assets/Obstacle","Obstacle3.png")),
            pygame.image.load(os.path.join("Assets/Obstacle","Obstacle4.png")),
            pygame.image.load(os.path.join("Assets/Obstacle","Obstacle5.png")), 
            pygame.image.load(os.path.join("Assets/Obstacle","Obstacle5.png"))] 

Plane = [pygame.image.load(os.path.join("Assets/Plane","Plane1.png")), 
        pygame.image.load(os.path.join("Assets/Plane", "Plane2.png"))]
 

Cloud = pygame.image.load(os.path.join("Assets/Other","Cloud.png"))

Bg = pygame.image.load((os.path.join("Assets/Other","Track.png")))

class CLOUD:
    def __init__(self):
        self.x = screen_width + random.randint(800, 1000)
        self.y = random.randint(50, 100)
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
    y_pos = 312
    y_pos_duck = 342
    JUMP_VELOCI = 8.5
    
    def __init__ (self):
        
        self.duck_img = Duking
        self.run_img = Running
        self.jump_img = Jumping
        
        self.dog_duck= False
        self.dog_run= True
        self.dog_jump= False
        
        self.step_index =0
        self.jump_veloci = self.JUMP_VELOCI
        self.image = self.run_img[0]
        self.dog_rect = self.image.get_rect()
        self.dog_rect.x = self.x_pos
        self.dog_rect.y = self.y_pos
    
    def update(self,userinput):
        if self.dog_duck:
            self.duck()
        if self.dog_run:
            self.run()
        if self.dog_jump:
            self.jump()
      
        if self.step_index >=10:
          self.step_index = 0
          
        if userinput[pygame.K_UP] and not self.dog_jump:      
            self.dog_duck= False
            self.dog_run= False
            self.dog_jump= True
        elif userinput[pygame.K_DOWN] and not self.dog_jump:
            self.dog_duck= True
            self.dog_run= False
            self.dog_jump= False
        elif not (self.dog_jump or userinput[pygame.K_DOWN]):
            self.dog_duck= False
            self.dog_run= True
            self.dog_jump= False
            
    def duck(self):
        self.image = self.duck_img[self.step_index//5]
        self.dog_rect = self.image.get_rect()
        self.dog_rect.x = self.x_pos
        self.dog_rect.y = self.y_pos_duck
        self.step_index += 1
        
    def run(self):
        self.image = self.run_img[self.step_index//5]
        self.dog_rect = self.image.get_rect()
        self.dog_rect.x = self.x_pos
        self.dog_rect.y = self.y_pos
        self.step_index += 1
    
    def jump(self):        
      self.image = self.jump_img
      if self.dog_jump:
          self.dog_rect.y-= self.jump_veloci * 4
          self.jump_veloci -=0.8
      if self.jump_veloci < - self.JUMP_VELOCI:
          
          self.dog_jump = False
          self.jump_veloci = self.JUMP_VELOCI
    
    def draw(self, screen):
        screen.blit(self.image, (self.dog_rect.x, self.dog_rect.y))  

def main():
    global game_speed, x_pos_bg, y_pos_bg
    run = True
    clock = pygame.time.Clock()
    Cloud = CLOUD()
    player = Dog()
    game_speed=14
    x_pos_bg=0
    y_pos_bg=370
    
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
                run= False
        screen.fill((135, 206, 235))
        
        userinput = pygame.key.get_pressed()
        background()
        Cloud.draw(screen)
        Cloud.update()
        player.draw(screen)
        player.update(userinput)
        clock.tick(30)
        pygame.display.update()


main()

