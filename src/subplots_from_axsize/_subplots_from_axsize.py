"""Implementation of subplots_from_axsize()"""

from collections.abc import Iterable
from typing import Optional, Tuple, Union

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

    assert len(ns) < 2, (
        f"Inconsistent {row_or_col} count.\n"
        f"declared: {n}\n"
        f"ax sizes: {axs}\n"
        f"spaces: {ds}"
    )

    if len(ns) == 0:
        n = 1
    else:
        (n,) = ns
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
    ds = [start] + [l for pair in zip(axs, spaces + [end]) for l in pair]

    sizes = [ag.Size.Fixed(d) for d in ds]

    return sizes, sum(ds)


def _set_shares(axs, axis, share):
    if isinstance(share, bool):
        share = 'all' if share else 'none'

    assert axis in ['x', 'y']
    assert share in ['none', 'all', 'row', 'col']

    def set_share(ax, ax0):
        if axis == 'x':
            ax.sharex(ax0)
        else:
            ax.sharey(ax0)

    if share == 'none':
        return

    if share == 'all':
        ax0 = axs[0, 0]
        for ax in axs.ravel()[1:]:
            set_share(ax, ax0)

    if share == 'row':
        for row in axs:
            ax0 = row[0]
            for ax in row[1:]:
                set_share(ax, ax0)

    if share == 'col':
        for col in axs.T:
            ax0 = col[0]
            for ax in col[1:]:
                set_share(ax, ax0)


def subplots_from_axsize(
    nrows: Optional[int] = None,
    ncols: Optional[int] = None,
    axsize: Tuple[Union[float, list[float]], Union[float, list[float]]] = (4, 3),
    *,
    left: float = 0.6,
    bottom: float = 0.5,
    right: float = 0.2,
    top: float = 0.1,
    wspace: Union[float, list[float]] = 0.75,
    hspace: Union[float, list[float]] = 0.5,
    sharex: Union[bool, str] = False,
    sharey: Union[bool, str] = False,
    squeeze: bool = True,
    **fig_kw,
):
    """
    Similar to plt.subplots() but uses fixed sizes (inches) instead of fractions.
    This allows for more control over the final axes sizes.

    Parameters
    ----------
    nrows, ncols : int, optional, default: None
        Number of rows/columns of the subplot grid.

    axsize : tuple of sizes, default: (3, 4)
        Each size can be either a float or list of floats (inches).
        If either entry is a list, it will be used to determine `nrows`/`ncols`.

    left, bottom, right, top : floats, defaults: 0.6, 0.5, 0.2, 0.1
        Specify figure margins (in inches).

    wspace, hspace : sizes, defaults: 0.75, 0.5
        Each size can be either a float or list of floats (inches).
        `wspace` (`hspace`) specifies the distance(s) between columns (rows).
        If either entry is a list, it will be used to determine `nrows`/`ncols`.

    sharex, sharey : bool or {'none', 'all', 'row', 'col'}, default: False
        True is treated like 'all', False is treated like 'none'.
        Does _not_ turn off ticklabels.

    squeeze : bool, default: True
        If True, extra dimensions (with length 1) are removed from `axs`.
        If False, always returns an array of axes with shape ``(nrows, ncols)`.

    **fig_kw
        All additional kwargs passed to the `figure()` call.
        Should not contain `figsize` and any `_layout` kwargs.

    Returns
    -------
        fig, axs : same as plt.subplots()

    Examples
    --------
    Create a figure with two axes of size (3, 2):
    ```
    fig, axs = subplots_from_axsize(axsize=(3, 2), nrows=2)
    ```

    Create a figure with two axes, (3, 2) and (3, 1):
    ```
    fig, axs = subplots_from_axsize(axsize=(3, [2, 1]))
    ```

    """

    assert 'figsize' not in fig_kw
    assert 'tight_layout' not in fig_kw
    assert 'constrained_layout' not in fig_kw
    assert 'layout' not in fig_kw

    axx, axy = axsize

    # standardize types
    axx = _list_or_float(axx)
    axy = _list_or_float(axy)
    wspace = _list_or_float(wspace)
    hspace = _list_or_float(hspace)

    # make sure counts agree and convert to lists
    ncols, axx, wspace = _sync_counts(ncols, axx, wspace, "col")
    nrows, axy, hspace = _sync_counts(nrows, axy, hspace, "row")

    w_sizes, total_w = _make_sizes(left, axx, right, wspace)
    h_sizes, total_h = _make_sizes(top, axy, bottom, hspace)

    fig = plt.figure(figsize=(total_w, total_h), **fig_kw)

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

    _set_shares(axs, 'x', sharex)
    _set_shares(axs, 'y', sharey)

    if squeeze:
        axs = np.squeeze(axs)
        if len(axs.ravel()) == 1:
            axs = axs.ravel()[0]

    return fig, axs
