import numpy as np
from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import time
import pygame

pygame.init()
#win = pygame.display.set_mode((500, 500))
screen = pygame.display.set_mode((400, 400))

class var:
    def __init__(self):
        # coordinate of end effector
        self.x_endeff = 0.0
        self.y_endeff = 0.0
        self.z_endeff = 0.0

        # angles in joints
        self.theta1 = 0.0
        self.theta2 = 0.0
        self.theta3 = 0.0

class param:
    def __init__(self):
        # coordinates of base
        self.x_origin = 0.0
        self.y_origin = 0.0
        self.z_origin = 0.0

        # link lengths
        self.l1 = 7.0
        self.l2 = 5.0

        # increment
        self.inc = 0.5

        #plotting params
        fig = plt.figure()
        self.ax = fig.add_subplot( 111 , projection = '3d')
        self.ax.set_xlim3d(-13, 13)
        self.ax.set_ylim3d(-13, 13)
        self.ax.set_zlim3d(0, 13)

# function to calculate projection of distance of endeffector on x-y plane
def d_calc(var):
    xt = np.power((var.x_endeff),2)
    yt = np.power((var.y_endeff),2)
    d = np.power(xt+yt,0.5)
    return d

# function to find thetas
def theta_finder(var , param):
    var.theta1 = np.arctan2(var.y_endeff,var.x_endeff)
    d = d_calc(var)
    gamma = np.arctan2(var.z_endeff , d)
    b1 = param.l1*param.l1 + param.l2*param.l2 - d*d - var.z_endeff*var.z_endeff
    b2 = 2*param.l1*param.l2
    b = (b1/b2)
    b = max(-1,b)
    b = min(1,b)
    beta = np.arccos(b)
    a1 = param.l1*param.l1 - param.l2*param.l2 + d*d + var.z_endeff*var.z_endeff
    a2 = 2*param.l1*np.power((d*d + var.z_endeff*var.z_endeff),0.5)
    a = (a1/a2)
    a = max(-1,a)
    a = min(1,a)
    alpha = np.arccos(a)
    var.theta2 = gamma + alpha
    var.theta3 = beta - np.pi

# plotting functions
def plotter(var,param):
    z = param.l1*np.sin(var.theta2) + param.l2*np.sin(var.theta3+var.theta2)
    t = param.l1*np.cos(var.theta2) + param.l2*np.cos(var.theta3+var.theta2)
    x = t*np.cos(var.theta1)
    y = t*np.sin(var.theta1)
    zl = param.l1*np.sin(var.theta2)
    tl = param.l1*np.cos(var.theta2)
    xl = tl*np.cos(var.theta1)
    yl = tl*np.sin(var.theta1)
    param.ax.scatter([param.x_origin,xl,x],[param.y_origin,yl,y],[param.z_origin,zl,z],zdir = 'z',s=20,c='blue',depthshade=True)
    param.ax.plot([param.x_origin,xl],[param.y_origin,yl],[param.z_origin,zl],'red')
    param.ax.plot([xl,x],[yl,y],[zl,z],'red')

#check in workspace
def check_in_ws(x,y,var,param):
    rtemp = np.power((param.l1+param.l2),2) - np.power(var.z_endeff,2)
    r = np.power(rtemp,0.5)
    x_new = (x-200)*(r/200)
    y_new = (y-200)*(r/200)
    check = np.power((x_new*x_new + y_new*y_new),0.5)
    if check <= r:
        var.y_endeff = x_new
        var.z_endeff = - y_new
    else:
        print("out of workspace")

def main():
    Var = var()
    Param = param()
    Var.x_endeff = Param.l2
    Var.y_endeff = 0.0
    Var.z_endeff = Param.l1
    point = (0,0)

    while True:
        plt.cla()
        Param.ax.set_xlim3d(-13, 13)
        Param.ax.set_ylim3d(-13, 13)
        Param.ax.set_zlim3d(0, 13)
        # for stopping simulation with the esc key.
        plt.gcf().canvas.mpl_connect('key_release_event',lambda event: [exit(0) if event.key == 'escape' else None])
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        keys = pygame.key.get_pressed()
        if keys[pygame.K_q]:
            Var.x_endeff += Param.inc
        if keys[pygame.K_a]:
            Var.x_endeff -= Param.inc
        elif event.type == pygame.MOUSEMOTION:
            print event.pos
            point = event.pos
        screen.fill((0, 0, 0))
        pygame.display.flip()
        check_in_ws(point[0],point[1],Var,Param)
        theta_finder(Var,Param)
        plotter(Var,Param)
        plt.pause(0.001)
    plt.show()

def signal_handler(signal,frame):
    plt.close()
    sys.exit(0)

if __name__ == '__main__':
    main()
    signal.signal(signal.SIGINT,signal_handler)
