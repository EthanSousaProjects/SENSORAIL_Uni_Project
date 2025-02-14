import ipywidgets as widgets
from IPython.display import display
import matplotlib.pyplot as plt
def create_tabbed_figures(fig_list, fig_titles):
    outputs = []
    for i, fig in enumerate(fig_list):
        out = widgets.Output()
        with out:
            display(fig.canvas)
            fig.canvas.draw_idle()
        outputs.append(out)
    
    # Create a Tab widget with the outputs
    tab = widgets.Tab(children=outputs)
    
    # Set titles for each tab
    for i in range(len(outputs)):
        tab.set_title(i, fig_titles[i])

    plt.ion()

    return tab