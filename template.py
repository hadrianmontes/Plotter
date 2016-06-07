import matplotlib
matplotlib.use("Qt4Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import MaxNLocator

def stick_axes(fig):
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
        row, col = ind//ncols, ind%ncols
        axes[row][col] = ax
    # Se quita el interespaciado
    plt.subplots_adjust(hspace=0.001)
    plt.subplots_adjust(wspace=0.001)
    # Se eliminan las etiquetas que queden en los intersticios
    # Primero en x
    print(axes)
    if nrows > 1:
        for i in range(nrows-1):
            for j in range(ncols):
                axes[i][j].set_xticklabels([])
        # Se eliminan las etiquetas que solapan
        nbins = len(axes[-1][-1].get_xticklabels())
        for j in range(nrows):
            for i in range(ncols-1):
                axes[j][i].xaxis.set_major_locator(MaxNLocator(nbins=nbins, prune='upper'))
    # Ahora en y
    if ncols > 1:
        for j in range(ncols-1):
            for i in range(nrows):
                axes[i][j+1].set_yticklabels([])
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

#Fix the spacing between subplots
fig.tight_layout()
plt.show()
