"""Implementation of subplots_from_axsize()"""

from collections.abc import Iterable

import matplotlib.pyplot as plt
import mpl_toolkits.axes_grid1 as ag
import numpy as np


def _list_or_float(x):
    if isinstance(x, Iterable):
        return list(x)
    else:
        return float(x)


def _sync_counts(n, axs, ds, row_or_col):
    # nrows, axy, hs, "row"
    # ncols, axx, ws, "col"

    n1 = int(n) if n is not None else None
    n2 = len(axs) if isinstance(axs, list) else None
    n3 = len(ds) + 1 if isinstance(ds, list) else None

    ns = {n1, n2, n3} - {None}

    assert len(ns) < 2, f"Inconsistent {row_or_col} count.\n{n = }, {axs = }, {ds = }"

    if len(ns) == 0:
        n = 1
    else:
        n, = ns
        assert isinstance(n, int)

    if not isinstance(axs, list):
        assert isinstance(axs, float)
        axs = n * [axs]

    if not isinstance(ds, list):
        assert isinstance(ds, float)
        ds = (n - 1) * [ds]

    return n, axs, ds


def _make_sizes(start, axs, end, spaces):
    n = len(axs)
    assert len(spaces) == n - 1

    # interleave ax sizes and spaces
    ds = [start] + [
        l
        for pair in zip(axs, spaces + [end])  # same lengths!
        for l in pair
    ]

    sizes = [ag.Size.Fixed(d) for d in ds]

    return sizes, sum(ds)


def subplots_from_axsize(
    axsize=(3, 2),
    nrows=None,
    ncols=None,
    top=0.1,
    bottom=0.5,
    left=0.5,
    right=0.1,
    hspace=0.5,
    wspace=0.5,
    squeeze=True,
):
    """
    Similar to plt.subplots() but uses fixed instead of relative sizes.
    This allows for more control over the final axes sizes.

    Examples:
    fig, axs = subplots_from_axsize(axsize=(3, 2), nrows=2) creates a figure with two axes of size (3, 2)
    fig, axs = subplots_from_axsize(axsize=(3, [2, 1])) creates a figure with two axes: (3, 2) and (3, 1)
    """
    axx, axy = axsize

    # standardize types
    axx = _list_or_float(axx)
    axy = _list_or_float(axy)
    hspace = _list_or_float(hspace)
    wspace = _list_or_float(wspace)

    # make sure counts agree and convert to lists
    ncols, axx, wspace = _sync_counts(ncols, axx, wspace, "col")
    nrows, axy, hspace = _sync_counts(nrows, axy, hspace, "row")

    w_sizes, total_w = _make_sizes(left, axx, right, wspace)
    h_sizes, total_h = _make_sizes(top, axy, bottom, hspace)

    fig = plt.figure(figsize=(total_w, total_h))

    divider = ag.Divider(fig, (0, 0, 1, 1), w_sizes, h_sizes[::-1], aspect=False)
    axs = np.array(
        [
            [
                fig.add_axes(
                    divider.get_position(),
                    axes_locator=divider.new_locator(nx=2 * col + 1, ny=2 * row + 1),
                )
                for col in range(ncols)
            ]
            for row in range(nrows - 1, -1, -1)
        ]
    )

    if squeeze:
        axs = np.squeeze(axs)
        if len(axs.ravel()) == 1:
            axs = axs.ravel()[0]

    return fig, axs
