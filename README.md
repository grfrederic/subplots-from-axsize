## subplots_from_axsize
Alternative for matplotlib's subplots() (and adjust_subplots()) which uses exact measurements rather than fractions.
* `axsize` instead of `figsize`
* `left`, `bottom`, `right`, `top` use inches instead of fractions
* `wspace`, `hspace` use inches instead of fractions
* 'axsize', 'wspace', 'hspace' can take lists as arguments (see example #2 below)

## getting started
The package is available on [PyPi](https://pypi.org/project/subplots-from-axsize/).

## example #1
```
import matplotlib.pyplot as plt
from subplots_from_axsize import subplots_from_axsize

fig, ax = subplots_from_axsize()

ax.set_xlabel('x label')
ax.set_ylabel('y label')
fig.patch.set_facecolor('#ffbbff')
```
![image](https://github.com/grfrederic/subplots-from-axsize/assets/26434160/f3440071-22e7-4e9c-a985-5aad3f52f3f7)

## example #2
```
import matplotlib.pyplot as plt
from subplots_from_axsize import subplots_from_axsize

fig, axs = subplots_from_axsize(
    axsize=([1, 3], 1),
    hspace=[0.5, 1.0],
    left=0.4, bottom=0.3,
)
fig.patch.set_facecolor('#ffbbff')
```
![image](https://github.com/grfrederic/subplots-from-axsize/assets/26434160/fdadf3af-60e2-4423-8632-fbabc117c319)

