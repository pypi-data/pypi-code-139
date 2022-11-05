import sympy
from sympy.plotting.plot import Plot
from matplotlib import animation, pyplot

if pyplot.isinteractive():
    pyplot.ioff()


def make_plot(expr) -> Plot:
    if not 0 < len(expr.free_symbols) < 3:
        raise ValueError("The number of free_symbols in the expression is greater than 4 or less than 1")

    elif len(expr.free_symbols) == 1:
        x = expr.free_symbols.pop()
        return sympy.plotting.plot(expr, (x, -3, 3), show=False, backend="matplotlib", title=sympy.pretty(expr))

    else:
        x, y = expr.free_symbols
        return sympy.plotting.plot3d(
            expr, (x, -2, 2), (y, -2, 2), show=False, backend="matplotlib", title=sympy.pretty(expr))


# todo: support custom spaces | image size ?
def save_plot_image(expr, outfile: str = "output.png") -> str:
    make_plot(expr).save(outfile)
    return outfile


def save_plot_video(expr, outfile: str = "output.mp4") -> str:
    if len(expr.free_symbols) != 2:
        raise ValueError("The number of free_symbols in the expression must be 2")

    plot3d = make_plot(expr)

    backend = plot3d.backend(plot3d)
    backend.process_series()

    def animate(i):
        backend.ax[0].view_init(elev=30, azim=i * 2)
        return backend.fig,

    anim = animation.FuncAnimation(backend.fig, animate, frames=180, interval=20, blit=True)
    anim.save(outfile, fps=25, extra_args=['-vcodec', 'libx264'])

    return outfile
