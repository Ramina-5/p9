from nicegui import ui
import plotly.graph_objects as go
import numpy as np

# Limits for the sliders
MAX_FREQ = 5.0
MAX_AMP = 5.0


class State:
    """Holds the parameters of the sinusoid."""

    def __init__(self):
        self.frequency = 1.0
        self.amplitude = 1.0
        self.phase = 0.0  


def make_figure(state: State) -> go.Figure:
    """ plot of y = amplitude * sin(2*pi*frequency*x + phase)."""
    x = np.linspace(0, 2, 500)
    y = state.amplitude * np.sin(2 * np.pi * state.frequency * x + state.phase)
    fig = go.Figure(go.Scatter(x=x, y=y, mode="lines"))
    # Fixed y-axis, so that a change of amplitude is visible
    fig.update_yaxes(range=[-MAX_AMP * 1.1, MAX_AMP * 1.1], title="y")
    fig.update_xaxes(title="x")
    fig.update_layout(margin=dict(l=40, r=20, t=20, b=40), autosize=True)
    return fig


def app():
    # Remove NiceGUI's default padding/gap and let children fill the width
    ui.query(".nicegui-content").style(
        "padding: 0; gap: 0; align-items: stretch; overflow: hidden;"
    )

    state = State()

    # ---- callbacks (they use `plot` and `info`, defined below) ----
    def refresh():
        plot.update_figure(make_figure(state))
        info.set_text(
            f"Frequency: {state.frequency:.1f} | Amplitude: {state.amplitude:.1f}"
        )

    def on_frequency(e):
        state.frequency = e.value
        refresh()

    def on_amplitude(e):
        state.amplitude = e.value
        refresh()

    # ---- layout: header / (sidebar + content) / footer ----

    with ui.element("div").style(
        "display: flex; flex-direction: column; width: 100%; height: 100vh;"
    ):
        # Header
        with ui.element("header").style(
            "padding: 1rem; background: #dcdcdc; flex-shrink: 0;"
        ):
            ui.label("Sinusoid").classes("text-xl")

        # Main area (takes all the remaining height)
        with ui.element("div").style(
            "display: flex; flex: 1; min-height: 0; width: 100%;"
        ):
            # Sidebar: controls
            with ui.element("div").style(
                "width: 30%; max-width: 20rem; flex-shrink: 0; "
                "padding: 1rem; background: #ececec; overflow-y: auto;"
            ):
                ui.label("Options").classes("text-xl")

                ui.label("Frequency")
                ui.slider(
                    min=0.5,
                    max=MAX_FREQ,
                    step=0.1,
                    value=state.frequency,
                    on_change=on_frequency,
                ).props("label-always switch-label-side color=green")

                ui.label("Amplitude").style("margin-top: 1.5rem;")
                # "reverse" puts the maximum at the top (default is at the bottom)
                ui.slider(
                    min=0.1,
                    max=MAX_AMP,
                    step=0.1,
                    value=state.amplitude,
                    on_change=on_amplitude,
                ).props("vertical reverse label-always").style(
                    "height: 12rem; margin: 0.5rem 1rem;"
                )

            # Content: the plot
            with ui.element("div").style(
                "flex: 1; min-width: 0; padding: 1rem; background: #ffffff; "
                "display: flex;"
            ):
                plot = ui.plotly(make_figure(state)).style(
                    "width: 100%; height: 100%; min-height: 300px;"
                )

        # Footer
        with ui.element("footer").style(
            "padding: 1rem; background: #dcdcdc; flex-shrink: 0;"
        ):
            info = ui.label("Parameter info").classes("text-xl")

    refresh()


app()
ui.run(title="Sinusoid")