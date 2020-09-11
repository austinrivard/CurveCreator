import tkinter as tk
import numpy as np
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import style
style.use('ggplot')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from scipy.ndimage.filters import gaussian_filter1d
import os
import sys

def resource_path(relative_path):
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)

def quit_me():
    window.quit()
    window.destroy()

def init(): 
    line.set_data([], [])
    return line,

#drawing loop, start timer ticking every .1s
#each tick advances x a small amount on graph
#track y value of mouse during this and adjust y on graph
def start():
    global line, xdata, ydata
    while len(ax.lines) > 1:
        ax.lines.pop()
    line.set_data([],[])
    xdata, ydata = [], []
    ani = animation.FuncAnimation(fig, animate, init_func=init, interval=10, repeat=False, frames=101)
    canvas.draw()

def diff():
    ydata = ax.lines[-1].get_data()[1]
    ddx_ydata = [(ydata[1] - ydata[0]) * 10]
    for i in range(1,101):
        ddx_ydata.append((ydata[i] - ydata[i-1]) * 10)
    ysmoothed = gaussian_filter1d(ddx_ydata, sigma=2)
    ax.plot(xdata, ysmoothed, lw=2)
    canvas.draw()

def animate(i):
    global initial_y
    if i == 0:
      initial_y = (graph_frame.winfo_pointery() - graph_frame.winfo_rooty() - 300) * .1
      mouse_y = initial_y
    else:
      mouse_y = initial_y - (graph_frame.winfo_pointery() - graph_frame.winfo_rooty() - 300) * .1
    xdata.append(i * 0.1)
    ydata.append(mouse_y)
    ysmoothed = gaussian_filter1d(ydata, sigma=2)
    line.set_data(xdata, ysmoothed)
    return line,

window = tk.Tk()
window.wm_iconbitmap(resource_path('curveicon.ico'))
window.protocol("WM_DELETE_WINDOW", quit_me)
window.geometry('800x480')
window.resizable(False,False)
window.title('Curve Creator')

text_frame = tk.Frame(window, bg='white')
text_frame.grid(row=0, column=0,sticky=tk.NSEW)

text = tk.StringVar()
text.set('Click the button below then move your mouse up and down to control the curve\'s path.')
instructions = tk.Label(text_frame, font=14, width=20, bg='white', wraplength=160, textvariable=text)
instructions.grid(row=0, column=0, sticky=tk.S)
text_frame.grid_rowconfigure(0, weight=1)

fig = plt.figure() 
ax = plt.axes(xlim=(0,10), ylim=(-100, 100)) 
line, = ax.plot([], [], lw=2) 
xdata, ydata = [], []

graph_frame = tk.Frame(window)
graph_frame.grid(row=0, column=1, sticky=tk.NSEW)

canvas = FigureCanvasTkAgg(fig, graph_frame)
canvas.get_tk_widget().grid(row=0, column=0, sticky=tk.N)

initial_y = 0
start_button = tk.Button(text_frame, font=16, text='Start', command=start, pady=8, padx=28)
start_button.grid(row=1, column=0, sticky=tk.S)

diff_button = tk.Button(text_frame, font=16, text='Differentiate', command=diff, pady=8, padx=2)
diff_button.grid(row=2, column=0, sticky=tk.N)

text_frame.grid_rowconfigure(1, weight=1)
text_frame.grid_rowconfigure(2, weight=1)

window.mainloop()