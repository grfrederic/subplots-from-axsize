import pytest

from matplotlib.axes import Axes
from subplots_from_axsize import subplots_from_axsize


@pytest.mark.parametrize("axx", [0.1, [0.1, 0.2]])
@pytest.mark.parametrize("axy", [0.3, [0.5, 0.8]])
@pytest.mark.parametrize("squeeze", [True, False])
def test_shapes(axx, axy, squeeze):
    _fig, axs = subplots_from_axsize(axsize=(axx, axy), squeeze=squeeze)

    xlist = isinstance(axx, list)  # columns!
    ylist = isinstance(axy, list)  # rows!
    xlen = len(axx) if xlist else 1
    ylen = len(axy) if ylist else 1

    if not squeeze or (xlist and ylist):
        nrows, ncols = axs.shape
        assert nrows == ylen
        assert ncols == xlen

    elif xlist and not ylist:
        ncols, = axs.shape
        assert ncols == xlen

    elif not xlist and ylist:
        nrows, = axs.shape
        assert nrows == ylen

    else:
        assert isinstance(axs, Axes)


@pytest.mark.parametrize("axx", [0.1, [0.1, 0.2]])
@pytest.mark.parametrize("axy", [0.3, [0.5, 0.8]])
def test_sizes(axx, axy):
    fig, axs = subplots_from_axsize(axsize=(axx, axy), squeeze=False)
    fig.canvas.draw()  # otherwise ax positions / extents are not computed

    axx = axx if isinstance(axx, list) else [axx]
    axy = axy if isinstance(axy, list) else [axy]

    for row_idx, row in enumerate(axs):
        for col_idx, ax in enumerate(row):
            width = axx[col_idx]
            height = axy[row_idx]

            we = ax.get_window_extent()

            assert we.height / fig.dpi == pytest.approx(height)
            assert we.width / fig.dpi == pytest.approx(width)


@pytest.mark.parametrize("axx", [[0.1, 0.2], [0.3, 0.4, 0.5]])
@pytest.mark.parametrize("axy", [[0.5, 0.8], [0.6, 0.7, 0.8]])
def test_order(axx, axy):
    fig, axs = subplots_from_axsize(axsize=(axx, axy))
    fig.canvas.draw()  # otherwise ax positions / extents are not computed

    # upper right corner of the figure: first row, last col
    ax_ur = axs[0, -1]

    # lower left corner of the figure: last row, first col
    ax_ll = axs[-1, 0]

    assert ax_ur.get_window_extent().y0 > ax_ll.get_window_extent().y1
    assert ax_ur.get_window_extent().x0 > ax_ll.get_window_extent().x1
