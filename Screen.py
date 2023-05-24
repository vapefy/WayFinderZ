import pygame, sys, os
from pygame.locals import *
import time
from Level import Level
pygame.mixer.init()
import os, pygame.mixer
pygame.font.init()

class Screen:   
    def __init__(self):
        self.FRAME_RATE = 30

        self.x_offset = 0
        self.y_offset = 0

        self.level = Level()
        self.calcGridOffsets()

        self.current_level = 1
        self.lives = 5
        
        self.animation_offset_x = 0
        self.animation_offset_y = 0

        self.stop_moving = False
        self.restart = False

        #Pygame und Display initialisieren
        pygame.init()
        self.screen = pygame.display.set_mode((640, 480))
        pygame.display.set_caption("WayFinderZ")
        pygame.mouse.set_visible(0)
        pygame.display.init()

        #Font initialisieren
        self.font = pygame.font.Font(os.path.join(r"data\fonts","impact.ttf"), 36)

        #Sounds initialisieren
        self.intro_sound = pygame.mixer.Sound(os.path.join("data\sounds","Intro.ogg"))
        self.enter_sound = pygame.mixer.Sound(os.path.join("data\sounds","LevelWon.mp3"))
        self.hit_wall_sound = pygame.mixer.Sound(os.path.join("data\sounds","WallHit.mp3"))
        self.game_over_sound = pygame.mixer.Sound(os.path.join("data\sounds","GameOver.mp3"))
        self.fall_sound = pygame.mixer.Sound(os.path.join("data\sounds","Fall.mp3"))
        self.game_intro_sound = pygame.mixer.Sound(os.path.join("data\sounds","Logo.ogg"))

        #Images initialisieren
        self.ball_1 = pygame.image.load(os.path.join("data\images","Ball.png")).convert_alpha()
        self.you_lose_image = pygame.image.load(os.path.join("data\images","YouLose.png")).convert_alpha()
        self.menu_image = pygame.image.load(os.path.join("data\images","Menu.png")).convert_alpha()
        self.block = pygame.image.load(os.path.join("data\images","Block.png")).convert_alpha()
        self.block1 = pygame.image.load(os.path.join("data\images","Block.png")).convert_alpha()
        self.block2 = pygame.image.load(os.path.join("data\images","Block.png")).convert_alpha()
        self.arrow1 = pygame.image.load(os.path.join("data\images","arrow1.png")).convert_alpha()
        self.arrow2 = pygame.image.load(os.path.join("data\images","arrow2.png")).convert_alpha()
        self.horizontal_block = pygame.image.load(os.path.join("data\images","Horizblock.gif")).convert_alpha()
        self.vertical_block = pygame.image.load(os.path.join("data\images","Vertblock.gif")).convert_alpha()
        self.floor_block = pygame.image.load(os.path.join("data\images","Floor.png")).convert_alpha()
        self.hole_block = pygame.image.load(os.path.join("data\images","feuer.png")).convert_alpha()
        self.start_block = pygame.image.load(os.path.join("data\images","Start.png")).convert()
        self.finish_block = pygame.image.load(os.path.join("data\images","Ziel.png")).convert_alpha()
        self.black_screen = pygame.image.load(os.path.join("data\images","Blank.png")).convert_alpha()
        self.you_win_image = pygame.image.load(os.path.join("data\images","YouWin.png")).convert_alpha()
        self.instructions = pygame.image.load(os.path.join("data\images","instructions.png")).convert_alpha()


    #Menü wird gerendert. Es gibt mehrere button positions. 
    def displayMainMenu(self):
        button_position = 1
        not_done = True
        while (not_done):

            #Wenn die Auswahl auf die jeweilige Position ist, werden zwei Pfeile an die jeweiligen Stellen gerendert.

            if button_position == 1:
                self.screen.blit(self.black_screen, (0,0))
                self.screen.blit(self.menu_image, (0, 0))
                self.screen.blit(self.arrow1, (138, 272))
                self.screen.blit(self.arrow2, (473, 272))
                pygame.display.flip()
            if button_position == 2:
                self.screen.blit(self.black_screen, (0,0))
                self.screen.blit(self.menu_image, (0, 0))
                self.screen.blit(self.arrow1, (210, 325))
                self.screen.blit(self.arrow2, (400, 325))
                pygame.display.flip()
            if button_position == 3:
                self.screen.blit(self.black_screen, (0,0))
                self.screen.blit(self.menu_image, (0, 0))
                self.screen.blit(self.arrow1, (135, 375))
                self.screen.blit(self.arrow2, (480, 375))
                pygame.display.flip()
            if button_position == 4:
                self.screen.blit(self.black_screen, (0,0))
                self.screen.blit(self.menu_image, (0, 0))
                self.screen.blit(self.arrow1, (140, 425))
                self.screen.blit(self.arrow2, (470, 425))
                pygame.display.flip()

            
            #Steuerung der Pfeile an die jeweiligen Positionen.

            for event in pygame.event.get():
                if (event.type == KEYDOWN):
                    if (event.key == K_DOWN) and button_position == 3:
                        button_position = 4
                    if (event.key == K_DOWN) and button_position == 2:
                        button_position = 3
                    if (event.key == K_DOWN) and button_position == 1:
                        button_position = 2
                    if (event.key == K_UP) and button_position == 2:
                        button_position = 1
                    if (event.key == K_UP) and button_position == 3:
                        button_position = 2
                    if (event.key == K_UP) and button_position == 4:
                        button_position = 3               
                    if (event.key == K_RETURN) and button_position == 1:
                        #Wenn die Position auf "Spiel starten" ist, bricht er aus der while schleife raus.
                        return
                    if (event.key == K_RETURN) and button_position == 2:
                        pygame.quit()
                        sys.exit()            
                    if (event.key == K_RETURN) and button_position == 3:
                        self.screen = pygame.display.set_mode((640, 480), FULLSCREEN)
                    if (event.key == K_RETURN) and button_position == 4:
                        self.screen = pygame.display.set_mode((640, 480))

    def drawLevel(self):
        self.screen.blit(self.black_screen, (0, 0))
        self.drawUI()
        for ym in range(0, len(self.getLevelObject().getLevelArray()), 1):
            for xm in range(0, len(self.getLevelObject().getLevelArray()[0]), 1):
                if self.getLevelObject().getLevelArray()[ym][xm] == 0:
                    self.screen.blit(self.floor_block, (xm * 32 + self.x_offset, ym * 32 + self.y_offset))
                if self.getLevelObject().getLevelArray()[ym][xm] == 1:
                    self.screen.blit(self.block, (xm * 32 + self.x_offset, ym * 32 + self.y_offset))
                if self.getLevelObject().getLevelArray()[ym][xm] == 2:
                    self.screen.blit(self.hole_block, (xm * 32 + self.x_offset, ym * 32 + self.y_offset))
                if self.getLevelObject().getLevelArray()[ym][xm] == 3:
                    self.screen.blit(self.start_block, (xm * 32 + self.x_offset, ym * 32 + self.y_offset))
                if self.getLevelObject().getLevelArray()[ym][xm] == 4:
                    self.screen.blit(self.finish_block, (xm * 32 + self.x_offset, ym * 32 + self.y_offset))
                if self.getLevelObject().getLevelArray()[ym][xm] == 5:
                    self.screen.blit(self.horizontal_block, (xm * 32 + self.x_offset, ym * 32 + self.y_offset))
                if self.getLevelObject().getLevelArray()[ym][xm] == 6:
                    self.screen.blit(self.vertical_block, (xm * 32 + self.x_offset, ym * 32 + self.y_offset))
        self.screen.blit(self.ball_1, ((self.getLevelObject().getBallX() * 32) + self.animation_offset_x + self.x_offset, (self.getLevelObject().getBallY()* 32) + self.animation_offset_y + self.y_offset))
        

    def update(self):
        self.drawLevel() #Level wird gerendert, je nach dem welches.
        
        pygame.display.flip()

        for event in pygame.event.get():                    
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
			
            if(event.type == KEYDOWN):            
                if (event.key == K_ESCAPE):
                    pygame.quit()
                    sys.exit()
                if(event.key == K_RIGHT):
                    self.moveRight()
                      
                if (event.key == K_LEFT):
                    self.moveLeft()                 
                      
                if (event.key == K_DOWN):
                    self.moveDown()
                         
                if (event.key == K_UP):
                    self.moveUp()

        self.stop_moving = False



    def moveDown(self):
        self.animation_offset_y = 0
        if((self.getLevelObject().getLevelArray()[(self.getLevelObject().getBallY() + 1)][(self.getLevelObject().getBallX())] == 2) or (self.getLevelObject().getLevelArray()[(self.getLevelObject().getBallY() + 1)][(self.getLevelObject().getBallX())] == 6)):
            self.die()
        if((self.getLevelObject().getLevelArray()[(self.getLevelObject().getBallY() + 1)][(self.getLevelObject().getBallX())] == 1) or (self.getLevelObject().getLevelArray()[(self.getLevelObject().getBallY() + 1)][(self.getLevelObject().getBallX())] == 5)):
            self.hit_wall_sound.play() #Wenn eine Wand erreicht wird, spielt er einen Sound.
        if((self.getLevelObject().getLevelArray()[(self.getLevelObject().getBallY() + 1)][(self.getLevelObject().getBallX())] == 0) or (self.getLevelObject().getLevelArray()[(self.getLevelObject().getBallY() + 1)][(self.getLevelObject().getBallX())] == 3)):
            if(self.stop_moving != True):
                for i in range(0, 4, 1):
                    self.animation_offset_y+=8
                    self.drawLevel()
                    time.sleep(0.025)
                    pygame.display.flip()
                self.getLevelObject().setBallY(self.getLevelObject().getBallY() + 1)
                self.moveDown()
        if((self.getLevelObject().getLevelArray()[(self.getLevelObject().getBallY() + 1)][(self.getLevelObject().getBallX())] == 4)):
            self.winLevel()
            
    def moveUp(self):
        self.animation_offset_y = 0
        if((self.getLevelObject().getLevelArray()[(self.getLevelObject().getBallY() - 1)][(self.getLevelObject().getBallX())] == 2) or (self.getLevelObject().getLevelArray()[(self.getLevelObject().getBallY() - 1)][(self.getLevelObject().getBallX())] == 6)):
            self.die()
        if((self.getLevelObject().getLevelArray()[(self.getLevelObject().getBallY() - 1)][(self.getLevelObject().getBallX())] == 1) or (self.getLevelObject().getLevelArray()[(self.getLevelObject().getBallY() - 1)][(self.getLevelObject().getBallX())] == 5)):
            self.hit_wall_sound.play()
        if((self.getLevelObject().getLevelArray()[(self.getLevelObject().getBallY() - 1)][(self.getLevelObject().getBallX())] == 0) or (self.getLevelObject().getLevelArray()[(self.getLevelObject().getBallY() - 1)][(self.getLevelObject().getBallX())] == 3)):
            if(self.stop_moving != True):
                for i in range(0, 4, 1):
                    self.animation_offset_y-=8
                    self.drawLevel()
                    time.sleep(0.025)
                    pygame.display.flip()
                self.getLevelObject().setBallY(self.getLevelObject().getBallY() - 1)
                self.moveUp()
        if((self.getLevelObject().getLevelArray()[(self.getLevelObject().getBallY() - 1)][(self.getLevelObject().getBallX())] == 4)):
            self.winLevel()

    def moveRight(self):
        self.animation_offset_x = 0
        if((self.getLevelObject().getLevelArray()[(self.getLevelObject().getBallY())][(self.getLevelObject().getBallX() + 1)] == 2) or (self.getLevelObject().getLevelArray()[(self.getLevelObject().getBallY())][(self.getLevelObject().getBallX() + 1)] == 5)):
            self.die()
        if((self.getLevelObject().getLevelArray()[(self.getLevelObject().getBallY())][(self.getLevelObject().getBallX() + 1)] == 1) or (self.getLevelObject().getLevelArray()[(self.getLevelObject().getBallY())][(self.getLevelObject().getBallX() + 1)] == 6)):
            self.hit_wall_sound.play()
        if((self.getLevelObject().getLevelArray()[(self.getLevelObject().getBallY())][(self.getLevelObject().getBallX() + 1)] == 0) or (self.getLevelObject().getLevelArray()[(self.getLevelObject().getBallY())][(self.getLevelObject().getBallX() + 1)] == 3)):
            if(self.stop_moving != True):
                for i in range(0, 4, 1):
                    self.animation_offset_x+=8
                    self.drawLevel()
                    time.sleep(0.025)
                    pygame.display.flip()
                self.getLevelObject().setBallX(self.getLevelObject().getBallX() + 1)
                self.moveRight()
        if((self.getLevelObject().getLevelArray()[(self.getLevelObject().getBallY())][(self.getLevelObject().getBallX() + 1)] == 4)):
            self.winLevel()

    def moveLeft(self):
        self.animation_offset_x = 0
        if((self.getLevelObject().getLevelArray()[(self.getLevelObject().getBallY())][(self.getLevelObject().getBallX() - 1)] == 2) or (self.getLevelObject().getLevelArray()[(self.getLevelObject().getBallY())][(self.getLevelObject().getBallX() - 1)] == 5)):
            self.die()
        if((self.getLevelObject().getLevelArray()[(self.getLevelObject().getBallY())][(self.getLevelObject().getBallX() - 1)] == 1) or (self.getLevelObject().getLevelArray()[(self.getLevelObject().getBallY())][(self.getLevelObject().getBallX() - 1)] == 6)):
            self.hit_wall_sound.play()
        if((self.getLevelObject().getLevelArray()[(self.getLevelObject().getBallY())][(self.getLevelObject().getBallX() - 1)] == 0) or (self.getLevelObject().getLevelArray()[(self.getLevelObject().getBallY())][(self.getLevelObject().getBallX() - 1)] == 3)):
            if(self.stop_moving != True):
                for i in range(0, 4, 1):
                    self.animation_offset_x-=8
                    self.drawLevel()
                    time.sleep(0.025)
                    pygame.display.flip()
                self.getLevelObject().setBallX(self.getLevelObject().getBallX() - 1)
                self.moveLeft()
        if((self.getLevelObject().getLevelArray()[(self.getLevelObject().getBallY())][(self.getLevelObject().getBallX() - 1)] == 4)):
            self.winLevel()

    def getLevelObject(self):
        return self.level

    def die(self):
        self.stop_moving = True
        self.fall_sound.play()
        self.lives-=1

        if(self.lives == 0):
            self.gameOver()
        else:
            self.getLevelObject().loadLevel(self.current_level)

    def gameOver(self):
        self.drawUI()
        pygame.display.flip()
        time.sleep(0.5)
        self.game_over_sound.play()
        self.screen.blit(self.black_screen, (0, 0))
        self.screen.blit(self.you_lose_image, (0, 170))
        pygame.display.flip()
        time.sleep(3)
        self.restart = True

    def calcGridOffsets(self):
        self.x_offset = (320 - (((len(self.getLevelObject().getLevelArray())) * 32)/2))
        self.y_offset = (240 - (((len(self.getLevelObject().getLevelArray()[0])) * 32)/2))

    def winLevel(self):
        self.enter_sound.play()
        self.current_level+=1
        if(self.current_level == 10):
            self.block = pygame.image.load(os.path.join("data","Block2.gif"))
        elif(self.current_level == 20):
            self.block = pygame.image.load(os.path.join("data","Block3.gif"))
        elif(self.current_level == 31):
            self.win()
            self.restart = True
        self.getLevelObject().loadLevel(self.current_level)
        self.calcGridOffsets()
        self.stop_moving = True

    def win(self):
        for i in range(0, 5, 1):
            time.sleep(0.5)
            self.screen.blit(self.black_screen, (0, 0))
            pygame.display.flip()
            time.sleep(0.5)
            self.screen.blit(self.you_win_image, (0, 170))
            pygame.display.flip()

    def playIntro(self):
        notDone = True
        self.game_intro_sound.play()
        for event in pygame.event.get():
            while notDone:
                for introy in range(-300, 60, 1):
                    self.screen.blit(self.intro_image, (0, introy))
                    pygame.display.flip()
                    time.sleep(.008)
                self.screen.blit(self.intro_image_2, (0, introy))
                pygame.display.flip()
                notDone = False
            time.sleep(1.5)

    def showInstructions(self):
        notDone = True
        self.screen.blit(self.instructions, (0, 0))
        pygame.display.flip()
        while notDone:
            for event in pygame.event.get():                    
                if (event.type == KEYDOWN):            
                    notDone = False

    def drawUI(self):
        level_text = self.font.render("Level " + str(self.current_level) +"/30", 1, (250, 250, 250))
        lives_text = self.font.render("Leben: " + str(self.lives), 1, (250, 250, 250))
        self.screen.blit(level_text, (240, 20))
        self.screen.blit(lives_text, (260, 420))

    def setLives(self, _lives):
        self.lives = _lives

    def setCurrentLevel(self, _level):
        self.current_level = _level

    def getRestartStatus(self):
        return self.restart

    def setRestartStatus(self):
        self.restart = False

    
    def main(self):    
        while(True):
            test = Screen()
            test.setRestartStatus()
            test.displayMainMenu()
            test.showInstructions()
            test.setLives(5)
            test.setCurrentLevel(1)
            while(test.getRestartStatus() == False):
                test.update()
                time.sleep(1/test.FRAME_RATE)
