import datetime
import errno
import os

import numpy as np
import pygame
import colorsys

# -----input of necessary information

class Mobius:
    dim = (200, 200)
    scale = 50
    pos = [0, 0]
    iteration = 10

    def __init__(self):
        self.u = 1.95
        self.v = 0.07
        self.t = self.u+1j*self.v

    def fA(self, z):
        try:
            return (self.t * z - 1j) / (-1j * z)
        except:
            return 0

    def fAi(self, z):
        try:
            return 1j / (1j * z + self.t)
        except:
            return 0

    def fB(self, z):
        return z + 2

    def fBi(self, z):
        return z - 2

    def printinfo(self):
        print()


Mclass = Mobius()
Mclass.printinfo()



def Vhalfplane(z):
    try:
        if z.imag > Mclass.u:
            w = (255, 205, 25)
        elif z.imag <= Mclass.v:
            w = (255, 69, 33)
        elif z.imag > Mclass.v and z.imag < Mclass.u:
            w = (0, 0, 0)
        else:
            w = (0, 0, 0)
    except:
        w = (0, 0, 0)
    return w

def tone(z):
    try:
        g = 0.2+abs(round(z.imag) - z.imag)/2
        if z.imag > Mclass.u:


            rgb_color = colorsys.hls_to_rgb(0.5, g, 1)
            w = (int(rgb_color[0] * 255), int(rgb_color[1] * 255), int(rgb_color[2] * 255))


        elif z.imag <= Mclass.v:

            rgb_color = colorsys.hls_to_rgb(0, g, 1)
            w = (int(rgb_color[0] * 255), int(rgb_color[1] * 255), int(rgb_color[2] * 255))

        elif z.imag > Mclass.v and z.imag < Mclass.u:
            w = (0, 0, 0)
        else:
            w = (0, 0, 0)
    except:
        w = (0, 0, 0)
    return w


def transf(z):
    '''P = 0.6 - 1j*0.8
    R = 1

    q = z - P
    h = np.tan(q)
    z = P + R**2*np.exp(1j*h)/abs(q)'''

    a = 1 + 0 * 1j
    a1 = 1 - Mclass.v + 1j * Mclass.u
    b = -1 + 1j * 0
    b1 = -1 - Mclass.v + 1j * Mclass.u

    for i in range(Mobius.iteration):
        if z.imag > 0 and z.imag < Mclass.u:
            zx = (z.real + 2 * 1000 - 1 + (Mclass.v * z.imag) / Mclass.u) % 2 - 1 - Mclass.v * z.imag / Mclass.u
            z = complex(zx, z.imag)
            M,K = 100, 100
            if z.real >= -Mclass.v/2:
                f = 1
            else:
                f = -1
            if z.imag < Mclass.u / 2+f*(1-np.exp(-abs(z.real+Mclass.v/2))):#Mclass.u / 2+f*K*Mclass.u*(1-np.exp(-M*abs(z.real+Mclass.v/2))):
                z = Mclass.fA(z)
                #z = Mclass.fB(z)

            else:
                z = Mclass.fAi(z)
                #z = Mclass.fBi(z)

            #if z.imag == Mclass.u / 2 + f * K * Mclass.u * (1 - np.exp(-M * abs(z.real + Mclass.v / 2))):
                #z = 0.5

    return z


def generate(background):
    x = np.arange(-(Mobius.dim[0] / 2), (Mobius.dim[0] / 2))
    y = np.arange(-(Mobius.dim[1] / 2), (Mobius.dim[1] / 2))
    xx, yy = np.meshgrid(x, y, sparse=True)
    z = (xx + 1j * yy) / Mclass.scale + (
            Mclass.pos[0] / Mclass.scale + 1j * Mclass.pos[1] / Mclass.scale)
    # z = Mclass.fA(z)
    ntransf = np.frompyfunc(transf, 1, 1)
    z = ntransf(z)
    nfun = np.frompyfunc(Vhalfplane, 1, 1)
    w = nfun(z)
    w = np.array([list(arr) for arr in w])
    w = np.flipud(np.fliplr(np.rot90(w)))
    pygame.surfarray.blit_array(background, w)
    pygame.display.update()
    pygame.display.flip()
    print('ok')


def start():
    date = datetime.datetime.now().strftime("%y-%m-%d-%H-%M")
    '''directory = "mob_" + date
    try:
        os.makedirs(directory)
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise

    file = open(os.path.join(directory, "functions_" + date + ".txt"), "w+")
    file.write("Title: " + "\n"
               + "Window size: " + "\n"
               + "Scale: " + "\n"
               + "Iterations: " + "\n"
               + "Method: " + "\n"
               + '*' * 50 + "\n"
               )'''

    counter = 0
    pygame.init()
    pygame.display.set_mode(Mclass.dim)
    background = pygame.display.get_surface()

    # background = background.convert()
    # screen.blit(background, (0, 0))
    mainloop = True
    generate(background)
    pygame.display.flip()
    pygame.image.save(background, str(counter)+str(date)+'.png')

    while mainloop:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                keys = pygame.key.get_pressed()
                if keys[pygame.K_a]:
                    #counter += 1
                    Mclass.v-=0.01
                    Mclass.t = complex(Mclass.u, Mclass.v)
                    generate(background)
                if keys[pygame.K_d]:
                    #counter += 1
                    Mclass.v+=0.01
                    Mclass.t = complex(Mclass.u, Mclass.v)
                    generate(background)
                if keys[pygame.K_w]:
                    #counter += 1
                    Mclass.u-=0.01
                    Mclass.t = complex(Mclass.u, Mclass.v)
                    generate(background)
                if keys[pygame.K_s]:
                    #counter += 1
                    Mclass.u+=0.01
                    Mclass.t = complex(Mclass.u, Mclass.v)
                    generate(background)
                if keys[pygame.K_i]:
                    #counter += 1
                    Mclass.iteration+=10

                    generate(background)
            if event.type == pygame.QUIT:
                mainloop = False


start()
