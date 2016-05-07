import matplotlib
matplotlib.use("Qt4Agg")
import matplotlib.pyplot as plt
import numpy as np

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
