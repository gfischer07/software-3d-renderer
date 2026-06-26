# import sys
# sys.setrecursionlimit(1000000)

import Render_3D
import pygame
import math
import Maths_3D as m
from pygame.locals import (
    QUIT,
    KEYDOWN,
    K_t,
    K_w,
    K_a,
    K_s,
    K_d,
    KEYUP,
    MOUSEMOTION,
    K_ESCAPE,
    K_LEFT,
    K_RIGHT,
    K_UP,
    K_DOWN,
    K_SPACE,
    K_LSHIFT,
    K_m,
)

zaxis = ((1, 0, 0, 0), 
         (0, math.cos(0.01), -math.sin(0.01), 0), 
         (0, math.sin(0.01), math.cos(0.01), 0), 
         (0, 0, 0, 1))
xaxis = ((math.cos(0.01), -math.sin(0.01), 0, 0), 
         (math.sin(0.01), math.cos(0.01), 0, 0), 
         (0, 0, 1, 0), 
         (0, 0, 0, 1))
move = ((1, 0, 0, 0),
        (0, 1, 0, 3.687397),
        (0, 0, 1, 0),
        (0, 0, 0, 1))


# defines the constants of the program
SCREEN_WIDTH = 960
SCREEN_HEIGHT = 540
MIDPOINT_WIDTH = SCREEN_WIDTH/2
MIDPOINT_HEIGHT = SCREEN_HEIGHT/2
FOV = 60
SENSITIVITY = 0.4
MOVESPEED = 0.1
NEAR_CLIP = 0.1
FAR_CLIP = 1000

pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.mouse.set_visible(False)

camera = Render_3D.Camera(screen, SCREEN_WIDTH, SCREEN_HEIGHT, FOV, SENSITIVITY, NEAR_CLIP, FAR_CLIP)
camera.ProjectionMatrix()
camera.ViewMatrix()

t1 = Render_3D.Triangle((-50, -1, -50), (-50, 0, -50), (50, 0, -50), (100, 255, 100))
t2 = Render_3D.Triangle((-50, -1, -50), (50, 0, -50), (50, -1, -50), (100, 255, 100))
t3 = Render_3D.Triangle((50, -1, -50), (50, 0, -50), (50, 0, 50), (100, 255, 100))
t4 = Render_3D.Triangle((50, -1, -50), (50, 0, 50), (50, -1, 50), (100, 255, 100))
t5 = Render_3D.Triangle((50, -1, 50), (50, 0, 50), (-50, 0, 50), (100, 255, 100))
t6 = Render_3D.Triangle((50, -1, 50), (-50, 0, 50), (-50, -1, 50), (100, 255, 100))
t7 = Render_3D.Triangle((-50, -1, 50), (-50, 0, 50), (-50, 0, -50), (100, 255, 100))
t8 = Render_3D.Triangle((-50, -1, 50), (-50, 0, -50), (-50, -1, -50), (100, 255, 100))
t9 = Render_3D.Triangle((-50, -1, -50), (50, -1, -50), (50, -1, 50), (100, 255, 100))
t10 = Render_3D.Triangle((-50, -1, -50), (50, -1, 50), (-50, -1, 50), (100, 255, 100))
t11 = Render_3D.Triangle((-50, 0, -50), (-50, 0, 50), (50, 0, 50), (100, 255, 100))
t12 = Render_3D.Triangle((-50, 0, -50), (50, 0, 50), (50, 0, -50), (100, 255, 100))
triangles = [t1, t2, t3, t4, t5, t6, t7, t8, t9, t10, t11, t12]
floor = Render_3D.Object(triangles, (100, 100, 255))
floor.CreateObject("3D/wardrobe.obj")
environment = Render_3D.Environment()
environment.AddObject(floor)

class Player():
    def __init__(self, camera):
        self.position = (0, 0, 0)
        self.facing = (0, 0, 1, 1)
        self.xmovement = 0
        self.zmovement = 0
        self.ymovement = 0
        self.pitch = 0
        self.camera = camera
        self.mesh = False
        self.jump = False
        self.sprint = False
        self.jumping = False
        self.falling = False
        self.t = 0
        self.movespeed = MOVESPEED
    
    def Update(self):
        # updates the position of the camera to the position of the player
        self.camera.SetPosition((self.position[0], self.position[1] + 5, self.position[2]), m.UnitVector(self.facing))

    def KeyPress(self, key):
        # sets the movement when a key is pressed
        if key == K_w:
            self.zmovement += 1
        elif key == K_s:
            self.zmovement -= 1
        elif key == K_d:
            self.xmovement += 1
        elif key == K_a:
            self.xmovement -= 1
        elif key == K_UP:
            self.ymovement += 1
        elif key == K_DOWN:
            self.ymovement -= 1
        elif key == K_SPACE:
            self.jump = True
        elif key == K_LSHIFT:
            self.sprint = True
        
        elif key == K_m:
            self.mesh = True

    def KeyRelease(self, key):
        # sets the movement when a key is pressed
        if key == K_w:
            self.zmovement -= 1
        elif key == K_s:
            self.zmovement += 1
        elif key == K_d:
            self.xmovement -= 1
        elif key == K_a:
            self.xmovement += 1
        elif key == K_UP:
            self.ymovement -= 1
        elif key == K_DOWN:
            self.ymovement += 1
        elif key == K_SPACE:
            self.jump = False
        elif key == K_LSHIFT:
            self.sprint = False

        elif key == K_m:
            self.mesh = False
    
    def Mouse(self):
        mouse_position = pygame.mouse.get_pos()
        mouserel = (mouse_position[0] - SCREEN_WIDTH/2, mouse_position[1] - MIDPOINT_HEIGHT)
        if mouserel[0] != 0:
            self.facing = m.MatrixMultiplier(m.RotationMatrixY(m.Radian(mouserel[0] * SENSITIVITY * camera.aspect)), self.facing)
        y = m.UnitVector(self.facing)[1]
        if mouserel[1] > 0 and y > -0.95:
            self.facing = m.MatrixMultiplier(m.RotationMatrixX(m.Radian(mouserel[1] * SENSITIVITY), self.facing[2], -self.facing[0]), self.facing)
        if mouserel[1] < 0 and y < 0.95:
            self.facing = m.MatrixMultiplier(m.RotationMatrixX(m.Radian(mouserel[1] * SENSITIVITY), self.facing[2], -self.facing[0]), self.facing)
        if mouserel != (0, 0): 
            pygame.mouse.set_pos(MIDPOINT_WIDTH, MIDPOINT_HEIGHT)
        self.Update()
    
    def Movement(self):
        # updates the player position
        u = m.UnitVector2x1((self.facing[0], self.facing[2]))
        # testz = ((self.position[0] + self.movespeed * self.zmovement * u[0]), (self.position[1]), (self.position[2] + self.movespeed * self.zmovement * u[1]))
        # if abs(testz[0]) < 50:
        #     self.position = (testz[0], self.position[1], self.position[2])
        # if abs(testz[2]) < 50:
        #     self.position = (self.position[0], self.position[1], testz[2])
        # testx = ((self.position[0] + self.movespeed * self.xmovement * u[1]), (self.position[1]), (self.position[2] + -self.movespeed * self.xmovement * u[0]))
        # if abs(testx[0]) < 50:
        #     self.position = (testx[0], self.position[1], self.position[2])
        # if abs(testx[2]) < 50:
        #     self.position = (self.position[0], self.position[1], testx[2])
        
        self.position = ((self.position[0] + self.movespeed * self.zmovement * u[0]), (self.position[1]), (self.position[2] + self.movespeed * self.zmovement * u[1]))
        self.position = ((self.position[0] + self.movespeed * self.xmovement * u[1]), (self.position[1]), (self.position[2] + -self.movespeed * self.xmovement * u[0]))

        self.position = (self.position[0], (self.position[1] + self.movespeed * self.ymovement), self.position[2])
        self.Update()
    
    def Jump(self):
        if self.t < 60 and self.jumping:
            if self.t == 0: self.startposition = self.position[1]
            self.t += 1
            self.position = (self.position[0], (60 * self.t - self.t**2) / 120 + self.startposition, self.position[2])
            self.Update()
        elif self.jumping:
            self.jumping = False
            self.t = 0
    
    def Checks(self):
        if self.jump: self.jumping = True
        if self.jumping: self.Jump()
        if self.sprint: self.movespeed = MOVESPEED * 2
        else: self.movespeed = MOVESPEED
        if abs(self.position[0]) > 50 or abs(self.position[2]) > 50: self.falling = True
        if self.falling: 
            self.position = (self.position[0], self.position[1] - self.movespeed * 5, self.position[2])
            self.Update()

def main():
    # creates the player
    player = Player(camera)

    # starts the game loop
    running = True
    while running == True:
        screen.fill((135, 206, 235))

        # updates the player and triangles
        if player.xmovement or player.zmovement or player.ymovement: player.Movement()

        player.Checks()

        if player.mesh: environment.RenderMesh(camera)
        else: environment.Render(camera)
        # floor.Transform(xaxis)
        # floor.Transform(zaxis)
        
        # checks for events
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            
            elif event.type == KEYDOWN:
                if event.key == K_t:
                    print(m.UnitVector(player.facing)[1])
                elif event.key == K_ESCAPE:
                    running = False
                else:
                    player.KeyPress(event.key)
            
            elif event.type == KEYUP:
                player.KeyRelease(event.key)
            
            elif event.type == MOUSEMOTION:
                player.Mouse()

        # sets the frame rate
        clock.tick(60)

        # updates the display
        pygame.display.flip()
            



main()