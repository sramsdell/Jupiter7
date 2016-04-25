import pygame,sys,os,math,random

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

#classes

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

big_rocket_info = ImageInfo((150/2,150/2),(150,150),75)
big_rocket_image = pygame.image.load(os.path.join("images","big_rocket.png"))

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
    def __init__(self, pos, vel, ang, ang_vel, image, info,color, sound = None, screen_size = (200, 500)):
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
        self.width = screen_size[0]
        self.height = screen_size[1]
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
        if self.pos[0] + self.radius >= self.width -(self.radius*2) or self.pos[0] +( self.radius * 2) <= self.width - self.width:
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
        self.pos[0] = self.pos[0] % (self.width +(self.radius))

class Wind(Sprite):
    def __init__(self, pos, vel, ang, ang_vel, image, info, color , sound = None):
        Sprite.__init__(self, pos, vel, ang, ang_vel, image, info, color , sound = None)
    def draw(self,canvas):
        self.age += self.angle_vel
        the_age = int(self.age % 359)

        canvas.blit(rot_center(self.image,the_age),self.pos)

    def update(self):
        self.angle += self.angle_vel
        self.pos[0] += self.vel[0]
        if self.pos[0] + (self.radius*2) >= self.width or self.pos[0]  <= self.width - self.width:
            self.vel[0] *= -1
        self.pos[1] += self.vel[1]

        if self.pos[1] + self.radius >= self.height-100 or self.pos[1] - self.radius <= self.height-self.height:
            self.vel[1] *= -1


class Rocket:
    def __init__(self, pos, vel,image, info, screen_size = (200, 500)):
        self.pos = [pos[0],pos[1]]
        self.vel = [vel[0],vel[1]]
        self.thrust = False
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        self.age = 0
        self.color = None
        self.ammo = 0
        self.spawn = pos
        self.width = screen_size[0]
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

        if self.pos[1] + self.vel[1] <= self.spawn[1]:

            if self.pos[0] + self.vel[0] >= 0  and self.pos[0] + self.vel[0] <= self.width - (self.radius*2):
                self.pos[0] += self.vel[0]
                self.pos[1] += self.vel[1]
    def alt_vel(self,x,y):
        self.vel = [x,y]
    def reset(self):
        ##need to research later why setting vel to 0 didn't stop "sticking, auto vel bugs"
        ## solution was to include key up handlers in the other states
        #self.vel = [0,0]
        self.pos = list(self.spawn)



    def ammo_reset(self):
        self.ammo = 0

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
        if self.pos[0] + self.radius >= self.width or self.pos[0] - self.radius <= self.width - self.width:
            self.vel[0] *= -1
