#-------------------------------------------------------------------------------
# Name:         Jupiter 7
# Purpose:      Adaption and continuation using pygame of
#                http://www.codeskulptor.org/#user40_mTQSVmq0Q0_7.py
#
# Author:      Steven Ramsdell
#
# Created:     10/12/2015
# Copyright:   (c) Stevie 2015
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import pygame,os,sys,math,random
from pygame.locals import *
from functions import *

# Constants
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
HEIGHT = 500
WIDTH = 200
SIZE = (WIDTH, HEIGHT)
ROCKET_SPAWN = (100,450)

class UI:
    def __init__(self):

        #self.manager = StateManager(screen)
        self.score = 0
        self.lives = 3
        self.level = 0
        self.mob_group = set([])
        self.capsule_group = set([])
        self.game_started = False
        self.bullet_group = set([])
        #var name, image, image info, color, vel, class
        self.mob_dic = {"blue_ghost":[blue_ghost,ghost_image,ghost_info,"blue",[2 * random.choice([1,-1]),0],Ghost],
                        "red_ghost":[red_ghost,ghost_red_image,ghost_info,"red",[2 * random.choice([1,-1]),0],Ghost],
                        "green_ghost":[green_ghost,ghost_green_image,ghost_info,"green",[2 * random.choice([1,-1]),0],Ghost],
                        "red_bird":[red_bird,bird_image,bird_info,"red",[-2,0],Bird],
                        "blue_bird":[blue_bird,bird_blue_image,bird_info,"blue",[-2,0],Bird],
                        "green_bird":[green_bird,bird_green_image,bird_info,"green",[-2,0],Bird],
                        "green_wind":[green_wind,spirl_image,spirl_info,"green",[((random.randrange(2,3)/2))*random.choice([1,-1]), ((random.randrange(2,3)/2))*random.choice([1,-1])],Wind],
                        "red_wind":[red_wind,spirl_red_image,spirl_info,"red",[((random.randrange(2,3)/2))*random.choice([1,-1]), ((random.randrange(2,3)/2))*random.choice([1,-1])],Wind],
                        "blue_wind":[blue_wind,spirl_blue_image,spirl_info,"blue",[((random.randrange(2,3)/2))*random.choice([1,-1]), ((random.randrange(2,3)/2))*random.choice([1,-1])],Wind]

                       }
    def get_game_started(self):
        return self.game_started
    def alt_game_started(self,boo):
        self.game_started = boo
    def get_lives(self):
        return self.lives
    def get_score(self):
        return self.score
    def alt_score(self,num):
        self.score += num
    def alt_lives(self,num):
        self.lives += num
    def score_reset(self):
        self.score = 0
    def lives_reset(self):
        self.lives = 3

    def get_level(self):
        return self.level
    def alt_level(self,num):
        self.level += num

    def get_mob_group(self):

        return self.mob_group.copy()
    def mob_group_reset(self):
        self.mob_group = set([])
    def add_mob_group(self, mob):
        self.mob_group.add(mob)
    def get_mob_dic(self):
        return self.mob_dic
    def remove_mob_group(self,mob):
        self.mob_group.discard(mob)

    def get_bullet_group(self):

        return self.bullet_group.copy()
    def add_bullet_group(self,bull):
        self.bullet_group.add(bull)
    def remove_bullet_group(self,bull):
        self.bullet_group.discard(bull)

    def get_cap_group(self):

        return self.capsule_group.copy()
    def cap_group_reset(self):
        self.capsule_group = set([])
    def add_cap_group(self, cap):
        self.capsule_group.add(cap)
    def remove_cap_group(self,cap):
        self.capsule_group.discard(cap)

    def reset_game(self,rocket,manager,screen):
        rocket.reset()
        rocket.ammo_reset()

        self.lives_reset()
        self.mob_group_reset()
        self.cap_group_reset()
        self.score_reset()
        rocket.update_color_shield(None)
        self.game_started = False
        self.level = 0
        manager.current.change(StartScreen(screen))

# frame and canvas

screen = pygame.display.set_mode(SIZE)
pygame.display.set_caption("Jupiter 7")


def main():
    pygame.init()
    clock = pygame.time.Clock()
    manager = StateManager(screen)
    running = True
    if False:
        manager.change(PauseState(screen))
    while running:
        running = manager.state.event_handler(pygame.event.get())

        manager.update()
        manager.render(screen)
        clock.tick(60)
        #clock.tick_busy_loop(60)
        pygame.display.flip()

    pygame.quit()
    sys.exit()

def score_point(rocket):
    if rocket.get_position()[1] - rocket.get_radius() <= 0:
        #rocket.alt_vel(0,0)
        game.alt_score(1)

        rocket.reset()

def process_sprite_group(the_set1,canvas):

    the_set = set(the_set1)
    for obj in the_set:
        obj.update()
        obj.draw(canvas)

def process_bullet_group(the_set1,rocket,canvas):

    the_set = set(the_set1)
    for obj in the_set:
        obj.update(rocket)
        obj.draw(canvas,rocket)

def bullet_spawner():

    if my_rocket.get_ammo() > 0:
        a_bullet = Bullet(my_rocket.get_position(),(0,-5),0,0,aura_image,cap_info,None)
        game.add_bullet_group(a_bullet)
        my_rocket.alt_ammo(-1)

def mob_spawner():

    mob_dict = game.get_mob_dic()
    mob_list = mob_dict.keys()
    mob = random.choice(mob_list)

    if game.get_level() < game.get_score()+1:
        # pos, vel, ang, ang_vel, image, info,color, sound = None

        mob_dict[mob][0] = mob_dict[mob][5]([random.randrange(51,WIDTH-51),random.randrange(51,350)],mob_dict[mob][4],1, (random.randrange(5,15)/110.0)*random.choice([1,-1]),mob_dict[mob][1],mob_dict[mob][2],mob_dict[mob][3])

        game.add_mob_group(mob_dict[mob][0])
        game.alt_level(1)

def capsule_spawner():
    if game.get_level() < game.get_score()+1 and game.get_level() % 2 == 1:
        a_capsule = Capsule([random.randrange(51,WIDTH-51),random.randrange(100,350)],(1,0),0,0,cap_image,cap_info,random.choice(["red","green","blue"]))
        game.add_cap_group(a_capsule)

def rocket_mob_collide(rocket,mob):

    if rocket.get_radius() + mob.get_radius() >= dist(rocket.get_position(),mob.get_position()):
        if not rocket.color_shield(mob.get_color()):
            rocket.reset()
            game.alt_lives(-1)

def rocket_cap_collide(rocket,cap):
    # handles cap off frame as well
    if cap.get_position()[1] == -1 * cap.get_radius():
        game.remove_cap_group(cap)

    if rocket.get_radius() + cap.get_radius() >= dist(rocket.get_position(),cap.get_position()):

        rocket.update_color_shield(cap.get_color())
        game.remove_cap_group(cap)
        rocket.alt_ammo(1)

def bullet_mob_collide(bullet,mob):
    #handles bullet, mob off frame as well

    if bullet.get_position()[1] == -1 * bullet.get_radius():
        game.remove_bullet_group(bullet)
    if mob.get_position()[1] == -1 * mob.get_radius():
        game.remove_mob_group(mob)
    if bullet.get_radius() + mob.get_radius() >= dist(bullet.get_position(),mob.get_position()):
        game.remove_bullet_group(bullet)
        game.remove_mob_group(mob)


def bullets_mobs_collide(bullets,mobs):

    for mob in mobs:
        for bullet in bullets:
            bullet_mob_collide(bullet,mob)

def rocket_mobs_collide(rocket,mobs):
    for mob in mobs:
        rocket_mob_collide(rocket,mob)

def rocket_caps_collide(rocket,caps):
    for cap in caps:
        rocket_cap_collide(rocket,cap)

def start_again(manager):

    if game.get_lives() == 0:

        game.reset_game(my_rocket,manager,screen)


class StateManager:
    def __init__(self,screen):
        self.change(StartScreen(screen))

    def change(self,state):
        self.state = state
        self.state.current = self

    def render(self,screen):
        self.state.render(screen)

    def update(self):
        self.state.update()


class MasterState:
    def __init__(self,screen):
        self.screen = screen
    def quit(self,event):
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
            return False

def keydown(key):
    if key.type == pygame.KEYDOWN:
        if key.key == pygame.K_UP:

            my_rocket.start_thruster("up")

        if key.key == pygame.K_DOWN:
            my_rocket.move("down")
        if key.key == pygame.K_LEFT:
            my_rocket.move("left")
        if key.key == pygame.K_RIGHT:
            my_rocket.move("right")
        if key.key == pygame.K_SPACE:
            bullet_spawner()


def keyup(key):
    if key.type == pygame.KEYUP:
        if key.key == pygame.K_UP:
            my_rocket.stop_thruster("up")
        if key.key == pygame.K_DOWN:
            my_rocket.stop_move("down")
        if key.key == pygame.K_LEFT:
            my_rocket.stop_move("left")
        if key.key == pygame.K_RIGHT:
            my_rocket.stop_move("right")

class LevelOne(MasterState):
    def __init__(self,screen):
        MasterState.__init__(self,screen)
        self.background = background_image

        self.myfont = pygame.font.SysFont("fixedsys", 20)
##        self.liveslabel = self.myfont.render("Lives = " +str(game.get_lives()), 1,RED)
##        self.ammolabel = self.myfont.render("Ammo = "+str(my_rocket.get_ammo()),1,RED)
##        self.scorelabel = self.myfont.render("Score = "+str(game.get_score()),1,RED)
##        self.levellabel = self.myfont.render("Level = "+str(game.get_level()),1,RED)


    def update(self):
        my_rocket.update()

        self.liveslabel = self.myfont.render("Lives = " +str(game.get_lives()), 1,RED)
        self.ammolabel = self.myfont.render("Ammo = "+str(my_rocket.get_ammo()),1,RED)
        self.scorelabel = self.myfont.render("Score = "+str(game.get_score()),1,RED)
        self.levellabel = self.myfont.render("Level = "+str(game.get_level()),1,RED)
    def render(self,screen):

        screen.blit(self.background,(0,0))
        screen.blit(self.liveslabel,(5,480))
        screen.blit(self.scorelabel,(110,480))
        screen.blit(self.levellabel,(110,455))
        screen.blit(self.ammolabel,(5,455))
        my_rocket.draw(screen)

        #logic func updates and renders spawn, also processes colisions
        logic(screen,self)


    def event_handler(self,events):
        for event in events:
            self.quit(event)
            keydown(event)
            keyup(event)
            if event.type == pygame.USEREVENT+1:
                mob_spawner()

            if event.type == pygame.USEREVENT+2:
                capsule_spawner()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    self.current.change(PauseState(screen))
        return True

    
class Animation_1(MasterState):
    def __init__(self,screen):
        MasterState.__init__(self,screen)
        self.background = background_image
        self.font = pygame.font.SysFont("fixedsys",24)
        self.text = self.font.render("SPACE to start",1,RED)
        self.age = 0
        self.x = 0
        self.y = 100
        self.s = pygame.Surface(SIZE, pygame.SRCALPHA)
        self.trans = 0
        self.ass = 0
    def update(self):
        pass
    def render(self,screen):
        self.y += -4 +self.ass
        self.ass += -.2
        print self.y, self.trans
        if self.y <= -150 and self.trans >= 240:
            self.current.change(LevelOne(screen))
        if self.y <= -150:
            self.trans += 5

            if self.trans >= 240:
                self.trans = 245
                self.y = 500
                #self.ass = -10
        screen.blit(self.background,(0,0))
        screen.blit(self.text,(40,320))
        self.s.fill((0,0,0,self.trans))
        screen.blit(self.s, (0,0))
        self.age += 0.2
        current_index = (self.age % 4) // 1


        scroll = [150*(current_index+1),0,150,150]
        screen.blit(big_rocket_image,(self.x,self.y),area=scroll)


    def event_handler(self,events):
        for event in events:
            self.quit(event)
            keydown(event)
            keyup(event)
            #start = float("inf")
            if event.type == pygame.KEYDOWN:
                
                if event.key == pygame.K_SPACE:
                    #start = pygame.time.get_ticks()
                    #print start
                    #pygame.time.set_timer(USEREVENT+1,2000)
                    self.current.change(LevelOne(screen))
                if event.key == pygame.K_m:
                    self.current.change(InstructionState(screen))
##            if event.type == USEREVENT+1:
##                test()
##            #if start < pygame.time.get_ticks():
##                
##                self.current.change(LevelOne(screen))
                
        return True

class StartScreen(MasterState):
    def __init__(self, screen):
        MasterState.__init__(self, screen)
        self.background = background_image   
        
        self.font = pygame.font.SysFont("fixedsys",24)
        self.text = self.font.render("SPACE to start",1,RED)
        self.age = 0
    def update(self):
        pass
    def render(self,screen):
        screen.blit(self.background,(0,0))

        screen.blit(self.text,(40,320))
        self.age += 0.2
        current_index = (self.age % 4) // 1


        scroll = [150*(current_index+1),0,150,150]
        screen.blit(big_rocket_image,(0,100),area=scroll)

    def event_handler(self,events):
        
        for event in events:
            self.quit(event)
            keydown(event)
            keyup(event)
            
            if event.type == pygame.KEYDOWN:
                
                if event.key == pygame.K_SPACE:
                    self.current.change(Animation_1(screen))
                if event.key == pygame.K_m:
                    self.current.change(InstructionState(screen))
                
        return True


class PauseState(MasterState):
    def __init__(self,screen):
        MasterState.__init__(self,screen)
        self.background = background_image
        self.font = pygame.font.SysFont("fixedsys",24)
        self.text = self.font.render("Pause",1,RED)
        self.age = 0
    def update(self):
        pass
    def render(self,screen):
        screen.blit(self.background,(0,0))
        screen.blit(self.text,(40,320))

        #screen.blit(big_rocket_image,(0,100))
        #self.age += 0.2
        #current_index = (self.age % 4) // 1


        #scroll = [150*(current_index+1),0,150,150]
        #screen.blit(big_rocket_image,(0,100),area=scroll)


    def event_handler(self,events):
        for event in events:
            self.quit(event)
            keydown(event)
            keyup(event)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    self.current.change(LevelOne(screen))

        return True

class InstructionState(MasterState):
    def __init__(self,screen):
        MasterState.__init__(self,screen)
        self.background = background_image
        self.font = pygame.font.SysFont("fixedsys",18)
        self.text = self.font.render("test, press M to return",1,RED)
        self.age = 0
    def update(self):
        pass
    def render(self,screen):
        screen.blit(self.background,(0,0))
        screen.blit(self.text,(40,320))

        #screen.blit(big_rocket_image,(0,100))
        #self.age += 0.2
        #current_index = (self.age % 4) // 1


        #scroll = [150*(current_index+1),0,150,150]
        #screen.blit(big_rocket_image,(0,100),area=scroll)


    def event_handler(self,events):
        for event in events:
            self.quit(event)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_m:
                    self.current.change(StartScreen(screen))
        return True
#inits
the_ghost = Ghost([40,100],[1,1],0,0,ghost_image,ghost_info,"blue")
the_wind = Wind([40,150],[1,1],0,2,spirl_blue_image,spirl_info,"blue")
the_bird = Bird([40,150],[1,1],0,0,bird_blue_image,bird_info,"blue")

def logic(canvas,manager):

    process_sprite_group(game.get_cap_group(),canvas)
    rocket_caps_collide(my_rocket,game.get_cap_group())

    process_bullet_group(game.get_bullet_group(),my_rocket,canvas)
    bullets_mobs_collide(game.get_bullet_group(),game.get_mob_group())


    process_sprite_group(game.get_mob_group(),canvas)
    rocket_mobs_collide(my_rocket,game.get_mob_group())

    score_point(my_rocket)
    start_again(manager)

my_rocket = Rocket(list(ROCKET_SPAWN),[0,0],rocket_image,rocket_info)
red_bird=()
blue_bird=()
green_bird =()
red_ghost=()
blue_ghost=()
green_ghost =()
red_wind=()
blue_wind=()
green_wind =()
a_capsule = ()

game = UI()

pygame.time.set_timer(pygame.USEREVENT+1,100)
pygame.time.set_timer(pygame.USEREVENT+2,102)

if __name__ == '__main__':
    main()
