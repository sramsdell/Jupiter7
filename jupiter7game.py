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


# Constants
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
HEIGHT = 500
WIDTH = 200
SIZE = (WIDTH, HEIGHT)
ROCKET_SPAWN = (100,450)

class Game_State:
    def __init__(self):

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

    def reset_game(self,rocket):
        rocket.reset()
        self.lives_reset()
        self.mob_group_reset()
        self.cap_group_reset()
        self.score_reset()
        rocket.update_color_shield(None)
        self.game_started = False
        self.level = 0

#helper functions
def rot_center(image, angle):
    """rotate an image while keeping its center and size"""
    orig_rect = image.get_rect()
    rot_image = pygame.transform.rotate(image, angle)
    rot_rect = orig_rect.copy()
    rot_rect.center = rot_image.get_rect().center
    rot_image = rot_image.subsurface(rot_rect).copy()
    return rot_image

def angle_to_vector(ang):
    return [math.cos(ang), math.sin(ang)]

def dist(p,q):
    return math.sqrt((p[0] - q[0]) ** 2+(p[1] - q[1]) ** 2)

# frame and canvas

screen = pygame.display.set_mode(SIZE)
pygame.display.set_caption("Jupiter 7")


class ImageInfo:
    def __init__(self, center, size, radius = 0, animated = False,lifespan = None):
        self.center = center
        self.size = size
        self.radius = radius
        if lifespan:
            self.lifespan = lifespan
        else:
            self.lifespan = float('inf')
        self.animated = animated

    def get_center(self):
        return self.center

    def get_size(self):
        return self.size

    def get_radius(self):
        return self.radius

    def get_lifespan(self):
        return self.lifespan

    def get_animated(self):
        return self.animated


##center, size, radius = 0, animated = False, lifespan = None
rocket_info = ImageInfo((64/4,64/4),(64/2,64/2),32/2)
rocket_image = pygame.image.load(os.path.join("images","small_rocket.png"))

aura_info = ImageInfo((64/4,64/4),(64/2,64/2),32/2)
aura_image = pygame.image.load(os.path.join("images","aura2.png"))

expl_info = ImageInfo((64/4,64/4),(64/2,64/2),32/2)
expl_image = pygame.image.load(os.path.join("images","test_expl.png"))

cap_info = ImageInfo((64/4,64/4),(64/2,64/2),32/2)
cap_image = pygame.image.load(os.path.join("images","cap2.png"))

spirl_info = ImageInfo((50/2,50/2),(50,50),23)
spirl_image = pygame.image.load(os.path.join("images","spirl.png"))
spirl_red_image = pygame.image.load(os.path.join("images","red_wind.png"))
spirl_blue_image = pygame.image.load(os.path.join("images","blue_wind.png"))

ghost_info = ImageInfo((16,32/2),(32,32),7,True)
ghost_image = pygame.image.load(os.path.join("images","ghost.png"))
ghost_red_image = pygame.image.load(os.path.join("images","red_ghost.png"))
ghost_green_image = pygame.image.load(os.path.join("images","green_ghost.png"))

background_info = ImageInfo((100,250),(200,500))
background_image = pygame.image.load(os.path.join("images","backround.png"))
background_face_image = 7
background_2_image = pygame.image.load(os.path.join("images","backround2.png"))
splash_image = pygame.image.load(os.path.join("images","splashscreen.png"))

bird_info = ImageInfo((32/2,32/2),(32,32),13,True)
bird_image = pygame.image.load(os.path.join("images","the_bird.png"))
bird_blue_image = pygame.image.load(os.path.join("images","blue_bird.png"))
bird_green_image = pygame.image.load(os.path.join("images","green_bird.png"))

class Sprite:
    def __init__(self, pos, vel, ang, ang_vel, image, info,color, sound = None):
        self.color = str(color)
        self.pos = [pos[0],pos[1]]
        self.vel = [vel[0],vel[1]]
        self.angle = ang
        self.angle_vel = ang_vel
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        self.lifespan = info.get_lifespan()
        self.animated = info.get_animated()
        self.age = 0
        if sound:
            sound.rewind()
            sound.play()
    def get_radius(self):
        return self.radius

    def get_position(self):
        return self.pos

    def get_color(self):
        return self.color

class Ghost(Sprite):
    def __init__(self, pos, vel, ang, ang_vel, image, info, color , sound = None):
        Sprite.__init__(self, pos, vel, ang, ang_vel, image, info, color , sound = None)
    def draw(self,canvas):

        self.age += 0.05
        current_index = int((self.age % 4) // 1)

        ##rec= left,top,width,height
        scroll = [self.image_size[0]*current_index,0,self.image_size[0],self.image_size[1]]
        canvas.blit(self.image,self.pos,area=scroll)

    def update(self):
        self.pos[0] += self.vel[0]
        self.pos[1] += math.cos(.1*self.pos[0])*2
        if self.pos[0] + self.radius >= WIDTH or self.pos[0] - self.radius <= WIDTH - WIDTH:
            self.vel[0] *= -1

class Bird(Sprite):
    def __init__(self, pos, vel, ang, ang_vel, image, info, color , sound = None):
        Sprite.__init__(self, pos, vel, ang, ang_vel, image, info, color , sound = None)
    def draw(self,canvas):
        current_index = int((self.age % 2) // 1)


        scroll = [self.image_size[0]*current_index,0,self.image_size[0],self.image_size[1]]
        canvas.blit(self.image,self.pos,area=scroll)

        self.age += 0.07
    def update(self):
        self.pos[0] += self.vel[0]
        self.pos[0] = self.pos[0] % WIDTH

class Wind(Sprite):
    def __init__(self, pos, vel, ang, ang_vel, image, info, color , sound = None):
        Sprite.__init__(self, pos, vel, ang, ang_vel, image, info, color , sound = None)
    def draw(self,canvas):
        self.age +=self.angle_vel
        the_age = int(self.age % 359)

        canvas.blit(rot_center(self.image,the_age),self.pos)

    def update(self):
        self.angle += self.angle_vel
        self.pos[0] += self.vel[0]
        if self.pos[0] + self.radius >= WIDTH or self.pos[0] - self.radius <= WIDTH - WIDTH:
            self.vel[0] *= -1
        self.pos[1] += self.vel[1]

        if self.pos[1] + self.radius >= HEIGHT-100 or self.pos[1] - self.radius <= HEIGHT-HEIGHT:
            self.vel[1] *= -1


class Rocket:
    def __init__(self, pos, vel,image, info):
        self.pos = [pos[0],pos[1]]
        self.vel = [vel[0],vel[1]]
        self.thrust = False
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        self.age = 0
        self.color = "red"
        self.ammo = 3

    def color_shield(self, mob_color):
        if mob_color == self.color:
            return True
    def update_color_shield(self,cap_color):
        self.color = cap_color

    def get_ammo(self):
        return self.ammo
    def alt_ammo(self,count):
        self.ammo += count

    def get_radius(self):
        return self.radius
    def get_position(self):
        return self.pos
    def draw(self,canvas):

        if self.color == "blue":
            canvas.blit(aura_image,self.pos,area=[0,0,32,32])
        if self.color == "green":
            canvas.blit(aura_image,self.pos,area=[64,0,32,32])
        if self.color == "red":
            canvas.blit(aura_image,self.pos,area=[32,0,32,32])

        if self.thrust:
            current_index = (self.age % 4) // 1


            scroll = [self.image_size[0]*(current_index+1),0,self.image_size[0],self.image_size[1]]
            canvas.blit(self.image,self.pos,area=scroll)

            self.age += 0.2
        else:

            canvas.blit(self.image,self.pos,[0,0,32,32])
            ##canvas.draw_image(self.image,self.image_center,self.image_size,self.pos,self.image_size,0)

    def start_thruster(self,key):
        if key == "up":

            self.vel[1] += -2
            self.thrust = True
    def stop_thruster(self,key):
        if key == "up":
            self.vel[1] += 2
            self.thrust = False
    def move(self,key):
        if key == "down":
            self.vel[1] += 2

        if key == "left":
            self.vel[0] -= 1
        if key == "right":
            self.vel[0] += 1
    def stop_move(self,key):
        if key == "down":
            self.vel[1] -= 2
        if key == "left":
            self.vel[0] += 1
        if key == "right":
            self.vel[0] -= 1
    def update(self):

        if self.pos[1] + self.vel[1] <= ROCKET_SPAWN[1]:

            if self.pos[0] + self.vel[0] >= 0 + self.radius and self.pos[0] + self.vel[0] <= WIDTH - self.radius:
                self.pos[0] += self.vel[0]
                self.pos[1] += self.vel[1]

    def reset(self):
        self.pos[0] = ROCKET_SPAWN[0]
        self.pos[1] = ROCKET_SPAWN[1]


class Bullet(Sprite):
    def __init__(self, pos, vel, ang, ang_vel, image, info, color , sound = None):
        Sprite.__init__(self, pos, vel, ang, ang_vel, image, info, color , sound = None)



    def draw(self,canvas,rocket):
        if rocket.color == "blue":
            canvas.blit(aura_image,self.pos,area=[0,0,32,32])
        if rocket.color == "green":
            canvas.blit(aura_image,self.pos,area=[64,0,32,32])
        if rocket.color == "red":
            canvas.blit(aura_image,self.pos,area=[32,0,32,32])

    def update(self,rocket):
        if rocket.color != None:

            self.pos[0] += self.vel[0]
            self.pos[1] += self.vel[1]

class Capsule(Sprite):
    def __init__(self, pos, vel, ang, ang_vel, image, info, color , sound = None):
        Sprite.__init__(self, pos, vel, ang, ang_vel, image, info, color , sound = None)
    def draw(self,canvas):
        if self.color == "blue":
            canvas.blit(aura_image,self.pos,area=[0,0,32,32])
        if self.color == "red":
            canvas.blit(aura_image,self.pos,area=[32,0,32,32])
        if self.color == "green":
            canvas.blit(aura_image,self.pos,area=[64,0,32,32])
        canvas.blit(self.image,self.pos,area=[0,0,32,32])

    def update(self):
        self.pos[0] += self.vel[0]
        self.pos[1] += math.cos(.1*self.pos[0])*2
        if self.pos[0] + self.radius >= WIDTH or self.pos[0] - self.radius <= WIDTH - WIDTH:
            self.vel[0] *= -1


def main():
    pygame.init()
    clock = pygame.time.Clock()
    manager = StateManager(screen)
    running = True

    while running:
        running = manager.state.event_handler(pygame.event.get())

        manager.update()
        manager.render(screen)
        clock.tick(60)
        pygame.display.flip()

    pygame.quit()
    sys.exit()

def score_point(rocket):
    if rocket.get_position()[1] - rocket.get_radius() <= 0:
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

def start_again():

    if game.get_lives() == 0:
        game.reset_game(my_rocket)

class StateManager:
    def __init__(self,screen):
        self.change(SplashState(screen))

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
            print "up"
            my_rocket.start_thruster("up")
            #game.alt_game_started(True)
        if key.key == pygame.K_DOWN:
            my_rocket.move("down")
        if key.key == pygame.K_LEFT:
            my_rocket.move("left")
        if key.key == pygame.K_RIGHT:
            my_rocket.move("right")
        if key.key == pygame.K_SPACE:
            bullet_spawner()
            game.alt_game_started(True)

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

class SplashState(MasterState):
    def __init__(self,screen):
        MasterState.__init__(self,screen)
        self.background = pygame.image.load(os.path.join("images","splashscreen.png"))

        self.myfont = pygame.font.SysFont("monospace", 15)
        self.label = self.myfont.render("wheres the ghost!", 1, (255,255,0))

    def update(self):
        my_rocket.update()
    def render(self,screen):

        screen.blit(self.background,(0,0))
        screen.blit(self.label,(100,300))
        my_rocket.draw(screen)

        #logic func updates and renders spawn, also processes colisions
        logic(screen)
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
                if event.key == pygame.K_a:
                    self.current.change(StateTwo(screen))
        return True


class StateTwo(MasterState):
    def __init__(self,screen):
        MasterState.__init__(self,screen)
        self.background = pygame.image.load(os.path.join("images","backround.png"))
        self.font = pygame.font.SysFont("monospace",24)
        self.text = self.font.render("fuckyeah",1,(0,0,0))
    def update(self):
        pass
    def render(self,screen):
        screen.blit(self.background,(0,0))
        screen.blit(self.text,(50,300))
    def event_handler(self,events):
        for event in events:
            self.quit(event)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    self.current.change(SplashState(screen))
        return True


#inits
the_ghost = Ghost([40,100],[1,1],0,0,ghost_image,ghost_info,"blue")
the_wind = Wind([40,150],[1,1],0,2,spirl_blue_image,spirl_info,"blue")
the_bird = Bird([40,150],[1,1],0,0,bird_blue_image,bird_info,"blue")

def logic(canvas):

    process_sprite_group(game.get_cap_group(),canvas)
    rocket_caps_collide(my_rocket,game.get_cap_group())

    process_bullet_group(game.get_bullet_group(),my_rocket,canvas)
    bullets_mobs_collide(game.get_bullet_group(),game.get_mob_group())


    process_sprite_group(game.get_mob_group(),canvas)
    rocket_mobs_collide(my_rocket,game.get_mob_group())

    score_point(my_rocket)
    start_again()

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

game = Game_State()

##timer = simplegui.create_timer(10.0, mob_spawner)
##timer2 = simplegui.create_timer(10.0, capsule_spawner)
##timer2.start()
##timer.start()



pygame.time.set_timer(pygame.USEREVENT+1,100)
pygame.time.set_timer(pygame.USEREVENT+2,102)

if __name__ == '__main__':
    main()
