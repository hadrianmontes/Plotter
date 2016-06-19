class create_script:
    def __init__(self,in_buffer,salida):
        self.f=in_buffer.readlines()
        g=open("template.py","r")
        self.h=open(salida,"w")
        for l in g:
            if not l.startswith(r"$"):
                self.h.write(l)
            else:
                l=l.strip()
                eval("self."+l[1:]+"()")
        self.h.close()
        return

    def create_fig_and_axes(self):
        f=self.f
        for l in f:
            l.strip()
            if l.startswith("Total"):
                n_rows=int(l.split()[2])
                self.n_rows=n_rows
                n_columns=int(l.split()[5])
                self.n_columns=n_columns
                break
        for i in range(n_rows):
            for j in range(n_columns):
                self.h.write("axes_"+str(i+1)+"_"+str(j+1)+"=fig.add_subplot("+str(n_rows)
                             +","+str(n_columns)+","+str(j+i*(n_columns)+1)+")\n")

    def write_parameters_axes(self):
        current_row=None
        current_column=None
        for l in self.f:
            l=l.strip()
            if l.startswith("row"):
                    current_row=l.split()[1]
                    current_column=l.split()[3]

            elif l.startswith("xlabel"):
                if len(l.split())>1:
                    self.h.write("axes_"+current_row+"_"+current_column
                                 +".set_xlabel('"+l[7:]+"')\n")

            elif l.startswith("ylabel"):
                if len(l.split())>1:
                    self.h.write("axes_"+current_row+"_"+current_column
                                 +".set_ylabel('"+l[7:]+"')\n")

            elif l.startswith("xlimits"):
                if len(l.split())==3:
                    self.h.write("axes_"+current_row+"_"+current_column
                                 +".set_xlim(["+l.split()[1]+","
                                 +l.split()[2]+"])\n")

            elif l.startswith("ylimits"):
                if len(l.split())==3:
                    self.h.write("axes_"+current_row+"_"+current_column
                                 +".set_ylim(["+l.split()[1]+","
                                 +l.split()[2]+"])\n")

    def load_data(self):
        current_row=None
        current_column=None
        current_file=None
        xcolumn='0'
        ycolumn='1'
        for l in self.f:
            l=l.strip()
            if l.startswith("row"):
                current_row=l.split()[1]
                current_column=l.split()[3]
            elif l.startswith('file'):
                current_file=l.split()[1]
            elif l.startswith("Data"):
                self.h.write("data_"+current_row+"_"+current_column+"_"
                             +current_file+"=read_data('"+l[5:]+"',"
                             +xcolumn+","+ycolumn+")\n")
            elif l.startswith("Xcolumn"):
                xcolumn=l.split()[1]
            elif l.startswith("Ycolumn"):
                ycolumn=l.split()[1]

    def plot_data(self):
        current_row=None
        current_column=None
        current_file=None
        marker=""
        linestyle=""
        color=""
        label=""
        for l in self.f:
            l=l.strip()
            if l.startswith('row'):
                if current_file:
                    self.write_plot_line(current_row,current_column,current_file,marker,linestyle,color,label)
                current_row=l.split()[1]
                current_column=l.split()[3]
                marker=""
                linestyle=""
                color=""
                label=""
                current_file=l.split()[1]
            elif l.startswith('file'):
                current_file=l.split()[1]
            elif l.startswith("Color") and len(l.split())==2:
                color=l.split()[1]
            elif l.startswith("Marker") and len(l.split())==2:
                marker=l.split()[1]
            elif l.startswith("Linestyle") and len(l.split())==2:
                linestyle=l.split()[1]
            elif l.startswith("Label") and len(l.split())>=2:
                label=l[6:]
        if current_file:
            self.write_plot_line(current_row,current_column,current_file,marker,linestyle,color,label)
            return

    def write_plot_line(self,current_row,current_column,current_file,marker,linestyle,color,label):
        self.h.write("axes_"+current_row+"_"+current_column
                     +".plot(data_"+current_row+"_"
                     +current_column+"_"+current_file+"[0],"
                     +"data_"+current_row+"_"+current_column
                     +"_"+current_file+"[1],"+"linestyle='"
                     +linestyle+"',marker='"+marker+"',label='"
                     +label)
        if color:
            self.h.write("',color='"+color)
        self.h.write("')\n")
        return
if __name__=="__main__":
    a=create_script(open("test.save"),"test_out.py")
