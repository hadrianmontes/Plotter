import matplotlib
matplotlib.use("Qt4Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import MaxNLocator

def stick_axes(fig, stick_x=True, stick_y=True):
    """
    Stick the axes of a figure 'fig'. The subplots distribution is respected.
    """
    # Se leen los ejes de la figura
    l_axes = fig.axes
    # El número de columnas y filas
    nrows, ncols, _, _ = l_axes[0].get_subplotspec().get_geometry()
    # Se inicia una lista de ceros con la forma del grid
    axes = [[0 for j in range(ncols)] for i in range(nrows)]
    # Se sitúa cada eje en su sitio de la grid
    for ax in l_axes:
        _, _, ind, _ = ax.get_subplotspec().get_geometry()
        row, col = ind//ncols, ind % ncols
        axes[row][col] = ax
    # Se quita el interespaciado
    if stick_x:
        plt.subplots_adjust(hspace=0.001)
    if stick_y:
        plt.subplots_adjust(wspace=0.001)
    # Se eliminan las etiquetas que queden en los intersticios
    # Primero en x
    if nrows > 1:
        if stick_y:
            for i in range(nrows):
                for j in range(ncols-1):
                    axes[i][j+1].set_yticklabels([])
            # Se eliminan las etiquetas que solapan
            nbins = len(axes[-1][-1].get_xticklabels())
            for j in range(nrows):
                for i in range(ncols-1):
                    axes[j][i].xaxis.set_major_locator(MaxNLocator(nbins=nbins, prune='upper'))
                    axes[j][i+1].set_ylabel("")
    # Ahora en y
    if ncols > 1:
        if stick_x:
            for i in range(nrows-1):
                for j in range(ncols):
                    axes[i][j].set_xticklabels([])
            # Se eliminan las etiquetas que solapan
            nbins = len(axes[-1][0].get_xticklabels())
            for i in range(nrows-1):
                for j in range(ncols):
                    axes[i+1][j].yaxis.set_major_locator(MaxNLocator(nbins=nbins, prune='upper'))

def read_data(filename,xcolumn,ycolumn):
    f=open(filename,"r")
    x=[]
    y=[]
    for l in f:
        l=l.strip()
        if not (l.startswith("#") or l.startswith("@")):
            try:
                x.append(float(l.split()[xcolumn]))
                y.append(float(l.split()[ycolumn]))
            except:
                pass
    x=np.array(x)
    y=np.array(y)
    return x,y


# Create the figure where the plots will be done
fig=plt.figure()
$create_fig_and_axes

# Now set the parameters for each axis
$write_parameters_axes

# Now we load all the data sets
$load_data

# Now start to plot the data files for each axe
$plot_data

# Fix the spacing between subplots
fig.tight_layout()

# If wanted to stick the axis uncomment one of the following lines
# REmenber that if the y axis are sticked, the y labels of some of the axis
# will be removed, if it were necessary for any reason it is possible to rewrite
# them after theese lines

# TO stick all the axis
# stick_axes(fig)
# To stick the x axis only
# stick_axes(fig,stick_y=False)
# To stick the y axis only
# stick_axes(fig,stick_x=False)

plt.show()
