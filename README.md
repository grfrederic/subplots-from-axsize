## subplots_from_axsize
This package provides a single function, `subplots_from_axsize()`, which is based on matplotlib's `subplots()` and `adjust_subplots()` functions, but:
* `figsize` is replaced by `axsize`
* `left`, `bottom`, `right`, `top` use inches instead of fractions
* `wspace`, `hspace` use inches instead of fractions
* `axsize`, `wspace`, `hspace` can take lists as arguments (see example #2 below)

## getting started
The package is available on [PyPi](https://pypi.org/project/subplots-from-axsize/).

## example #1
```
import matplotlib.pyplot as plt
from subplots_from_axsize import subplots_from_axsize

fig, ax = subplots_from_axsize(
    axsize=(4, 3),
    left=0.9, bottom=0.5, top=0.3, right=0.2,
)

ax.set_xlabel('x label')
ax.set_ylabel('y label\nbut much\nmuch longer')
ax.set_title('important!')
fig.patch.set_facecolor('#ffbbff')
```
![image](https://github.com/grfrederic/subplots-from-axsize/assets/26434160/3fe370d5-0ff4-4387-b94e-3a266b97425d)

Since the default dpi in matplotlib is 100, the axis is exactly 400 by 300 pixels. The left margin, for example, is 0.9 × 100 = 90 pixels. Changing the margins does not change the axis size (you have my promise).

## example #2
Additionally, `subplots_from_axsize` makes it easy to create multiple axes.
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

The number of columns (or rows) is inferred automatically based on three arguments: `nrows` (if given), length of `axsize[0]` (if it is a list), length of `wspace` *+ 1* (if it is a list). If none of the conditions is met, the default is 1. If they disagree you get an error (xor create an Issue).

