"""
Lindenmayer system
"""

from matplotlib import pyplot as plt
import numpy as np


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

    def draw(self, ax):
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


def main():
    tree = System(
        {'0': 'L10', '1': 'L10', '[': 'P R+045', ']': 'p R-045'},
        '0',
        {'1': '11', '0': '1[0]0'}
    )

    koch = System(
        {'F': 'L10', '+': 'R+90', '-': 'R-90'},
        'F',
        {'F': 'F+F-F-F+F'}
    )

    sierpinski = System(
        {'A': 'L10', 'B': 'L10', '+': 'R+60', '-': 'R-60'}, 'A', {'A': 'B-A-B', 'B': 'A+B+A'}
    )

    plant = System(
        {'X': '0', 'F': 'L10', '+': 'R+25', '-': 'R-25', '[': 'P', ']': 'p'},
        'X',
        {'X': 'F+[[X]-X]-F[-FX]+X', 'F': 'FF'},
        60
    )

    hilbert = System(
        {'A': '0', 'B': '0', 'F': 'L10', '+': 'R+90', '-': 'R-90'},
        'A',
        {'A': '+BF-AFA-FB+', 'B': '-AF+BFB+FA-'},
        0
    )

    fig, ax = plt.subplots()
    ax.set_aspect('equal', adjustable='box')
    neco = System(
        {'A': '0', 'F': 'L10', '+': 'R+60', '-': 'R-60'},
        'A',
        {'A': 'F--F--F', 'F': 'F+F--F+F'}
    )

    game = hilbert

    for _ in range(3):
        game.iterate()
        # game.print()
    # game.reduce()
    # game.print()

    game.draw(ax)
    plt.show()


if __name__ == '__main__':
    main()
