import numpy as np
import matplotlib.pyplot as plt
from scipy.special import comb

def bernstein_poly(i, n, t):
    # The Bernstein polynomial of n, i as a function of t
    return comb(n, i) * ( t**(n-i) ) * (1 - t)**i


def bezier_curve(points, nTimes=1000):

    nPoints = len(points)
    xPoints = np.array([p[0] for p in points])
    yPoints = np.array([p[1] for p in points])

    t = np.linspace(0.0, 1.0, nTimes)

    polynomial_array = np.array([bernstein_poly(i, nPoints-1, t) for i in range(0, nPoints)])

    xvals = np.dot(xPoints, polynomial_array)
    yvals = np.dot(yPoints, polynomial_array)

    return xvals, yvals


class BezierBuilder:
    def __init__(self, line):
        self.line = line
        self.xs = list(line.get_xdata())
        self.ys = list(line.get_ydata())
        self.cid = line.figure.canvas.mpl_connect('button_press_event', self)

    def __call__(self, event):
        if event.inaxes!=self.line.axes: return
        self.xs.append(event.xdata)
        self.ys.append(event.ydata)
        self.line.set_data(self.xs, self.ys)
        self.line.figure.canvas.draw()
        self.line.figure.canvas.flush_events()

        if len(self.xs) > 1:
            bx, by = bezier_curve(list(zip(self.xs, self.ys)))
            bezier_line.set_data(bx, by)
            self.line.figure.canvas.draw()
            self.line.figure.canvas.flush_events()

        ax.set_title(f'{len(self.xs)-1}º degree curve')
        self.line.figure.canvas.draw()



fig, ax = plt.subplots()
ax.set_title('click to create lines')
line, = ax.plot([0], [0])
bezier_line, = ax.plot([], [], 'r-') 
bezier_builder = BezierBuilder(line)
plt.show()
