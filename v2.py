"""
Lindenmayer system
"""

from matplotlib import pyplot as plt
import numpy as np
from matplotlib import animation


class System:
    def __init__(self, alphabet: dict, axiom: str, rules: dict, rot: int=90):
        self.alphabet = alphabet
        self.axiom = axiom
        self.rules = rules
        self.current = axiom
        self.iterations = 0
        self.start = np.array([0, 0])
        self.pos = self.start
        self.rot = rot

    def iterate(self):
        new = ''
        for c in self.current:
            if c in self.rules.keys():
                new += self.rules[c]
            else:
                new += c
        self.current = new
        self.iterations += 1

    def reduce(self):
        orig = len(self.current)
        red = [c for c in self.alphabet.keys() if self.alphabet[c] == '0']
        # red += ['+-', '-+']
        for r in red:
            self.current = self.current.replace(r, '')
        new = len(self.current)
        print(f'Reduced from {orig} to {new}, which is {1-new/orig:.2%} reduction.')

    def print(self):
        print('Iteration: ', self.iterations)
        print('\t', self.current)

    def draw(self):
        pos = self.pos
        rot = self.rot
        pos_save = []
        rot_save = []
        # print(self.current)
        for c in self.current:
            do = self.alphabet[c].split(' ')
            # print(c, do)
            for d in do:
                if d == 'P':
                    # print('P')
                    pos_save.append(pos)
                    rot_save.append(rot)
                elif d == 'p':
                    # print('p')
                    pos = pos_save[-1]
                    rot = rot_save[-1]
                    pos_save = pos_save[:-1]
                    rot_save = rot_save[:-1]
                elif d[0] == 'R':
                    # print('R')
                    rot += int(d[1:])
                    # print(rot)
                elif d[0] == 'L':
                    # print('L')
                    ln = int(d[1:])
                    newpos = np.array([pos[0] + ln*np.cos(rot*np.pi/180), pos[1] + ln*np.sin(rot*np.pi/180)])
                    # line = mlines.Line2D([pos[0], newpos[0]], [pos[1], newpos[1]])
                    plt.plot([pos[0], newpos[0]], [pos[1], newpos[1]], 'b')
                    pos = newpos


def update(frame):
    plt.cla()
    ax = plt.gca()
    plt.axis('off')
    ax.set_aspect('equal', adjustable='box')

    angle = int(10+frame/(N_FRAMES*0.8)*15)
    if angle > 25:
        angle = 25
    print(frame, angle)
    plant = System(
        {'X': '0', 'F': 'L10', '+': f'R+{angle}', '-': f'R-{angle}', '[': 'P', ']': 'p'},
        'X',
        {'X': 'F+[[X]-X]-F[-FX]+X', 'F': 'FF'},
        60
    )

    game = plant
    for i in range(5):
        game.iterate()

    game.draw()


def main():
    fig, ax = plt.subplots()

    ani = animation.FuncAnimation(fig=fig, func=update, frames=N_FRAMES, interval=100 / 3)
    ani.save('hilbert.mp4', writer='ffmpeg', dpi=300),
    # plt.show()


if __name__ == '__main__':
    N_FRAMES = 120
    main()
