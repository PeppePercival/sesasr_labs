import sympy as sp
import numpy as np
sp.init_printing(use_latex='mathjax')
from sympy import symbols, Matrix, latex

def range_and_bearing():
    x, mx, y, my, theta = symbols('x mx y my theta')
    
    hx = Matrix([[sp.sqrt((mx-x)**2+(my-y)**2)],[sp.atan2(my-y,mx-x)-theta]])
    eval_hx = sp.lambdify((mx, x, my, y, theta), hx, 'numpy')

    Ht = Matrix([[(x-mx)/(sp.sqrt((mx-x)**2+(my-y)**2)), (y-my)/(sp.sqrt((mx-x)**2+(my-y)**2)), 0],[-(y-my)/(sp.sqrt((mx-x)**2+(my-y)**2)), (x-mx)/(sp.sqrt((mx-x)**2+(my-y)**2)), -1]])
    eval_Ht = sp.lambdify((mx, x, my, y), Ht, 'numpy')

    return eval_hx, Ht, eval_Ht




def z_landmark(x, lmark, eval_hx, std_rng=0.5, std_brg=0.5):
    mx = lmark[0]
    my = lmark[1]
    xx = x[0,0]
    yy = x[1,0]
    theta = x[2,0]
    z = eval_hx(mx, xx, my, yy, theta)

    # filter z for a more realistic sensor simulation (add a max range distance and a FOV)
    fov = np.deg2rad(45)
    if z[0, 0] < 8.0 and abs(z[1, 0])<fov:
        return z + np.array([[np.random.randn() * std_rng**2, np.random.randn() * std_brg]]).T
        
    return None


def residual(a, b):
    y = a - b
    y[1] = y[1] % (2 * np.pi)  # force in range [0, 2 pi)
    if y[1] > np.pi:  # move to [-pi, pi)
        y[1] -= 2 * np.pi
    return y