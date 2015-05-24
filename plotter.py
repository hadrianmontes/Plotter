#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: Hadrian Montes
The MIT License (MIT)

Copyright (c) 2015 Hadrián Montes

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""
from Tkinter import *
import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg,NavigationToolbar2TkAgg
from matplotlib.figure import Figure
import tkMessageBox,tkFileDialog
import sys
class plotter(Frame):
    def __init__(self,mainframe):
        #Initiate t a blank figure
        self.figure_created=False #A bool to represent if the figure was created or not
        self.mainframe=mainframe#Asign a variable ofr the aminframe
        self.fig=Figure()#This is a dummy figure thta will be overwrited but it will grant the space for the real one
        self.canvas=FigureCanvasTkAgg(self.fig,master=mainframe)#The canvas where all the plots will be made
        self.canvas.show()
        self.canvas.get_tk_widget().grid(column=5,row=0,rowspan=12)#Create the widget that will mange the pots
        #Create the number of columns and rows
        ttk.Label(mainframe,text="Set number of columns  ").grid(column=0,row=0)
        self.total_columns=IntVar()#The variable that will store the number of total columns
        self.total_columns.set(1)#We give it an initial value
        self.box_total_columns=ttk.Combobox(mainframe,textvariable=self.total_columns,state="readonly",width=3)#Combobox with the 
        self.box_total_columns['values']=range(1,10)#Possible values for the total number of columns in the main figure
        self.box_total_columns.grid(column=1,row=0)
        ttk.Label(mainframe,text="  Set number of rows  ").grid(column=2,row=0)#The same taht with the columns but with the rows
        self.total_rows=IntVar()
        self.total_rows.set(1)
        self.box_total_rows=ttk.Combobox(mainframe,textvariable=self.total_rows,state="readonly",width=3)
        self.box_total_rows['values']=range(1,10)
        self.box_total_rows.grid(column=3,row=0)
        
        #Create the figure with the subplots
        ttk.Button(mainframe,command=self.init_program,text="Create").grid(column=4,row=0)#This button will initiate all the features

        #The next lines will allow to change between the subplots
        ttk.Label(mainframe,text="Select Column  ").grid(column=0,row=1)
        self.current_column=IntVar() #The variable storing the current Column
        #The next lines will setup the combobox for making this change
        self.box_current_column=ttk.Combobox(mainframe,textvariable=self.current_column,state="readonly",width=3)
        self.box_current_column["values"]=["--"]
        self.box_current_column.grid(column=1,row=1)
        ttk.Label(mainframe,text="  Select Row  ").grid(column=2,row=1)
        self.current_row=IntVar()#The variable storing th current row
        self.box_current_row=ttk.Combobox(mainframe,textvariable=self.current_row,state="readonly",width=3)
        self.box_current_row["values"]=["--"]
        self.box_current_row.grid(column=3,row=1)
        self.box_current_row.bind("<<ComboboxSelected>>",self.change_subplot)#Now we make that when you choose one column or a row
        self.box_current_column.bind("<<ComboboxSelected>>",self.change_subplot)#the prgram will auto load the presets for that subplot


        #Open File
        ttk.Button(mainframe,text="Open file",command=self.open_file).grid(column=0,row=3)
        self.filename=StringVar()#Variable to store the path to the data file
        self.entry_filename=ttk.Entry(mainframe,textvar=self.filename,width=30).grid(column=1,row=3,columnspan=3,sticky=E)
        
        #Options for the plot
        #The label for the legend
        self.label=StringVar()#Variable storing the label 
        ttk.Label(mainframe,text="Label").grid(column=0,row=4)
        ttk.Entry(mainframe,textvar=self.label,width=30).grid(column=1,row=4,columnspan=3,sticky=E)#Entry to enter the label
        #Combobox for selecting the maker
        self.marker=StringVar()#Variable storing the marker configuration
        self.marker.set("None")#The preset value for the marker (no marker on the points)
        ttk.Label(mainframe,text="Marker").grid(column=0,row=5)
        combo_marker=ttk.Combobox(mainframe,textvariable=self.marker,state="readonly",width=5)
        combo_marker["values"]=["None",".",",","o","+","*",'x',"custom"]#Since there quite a lot of markers i only preload the 
        combo_marker.grid(column=1,row=5)#esentials, but with the option custom it's posible to use wichever matplotlib supports
        self.marker_custom=StringVar()#Variable storing the marker type
        ttk.Entry(mainframe,textvar=self.marker_custom,width=5).grid(column=2,row=5,sticky=E)#Entry for the option of the custom 
        ttk.Button(mainframe,text="Custom Marker",command=self.set_custom_marker).grid(column=4,row=5)#Button to aply the custom config
        #Combobox for the line Style
        self.linestyle=StringVar()#Variable storing the linestyle configuration
        self.linestyle.set("-")#Preset value for the linestyle (solid line)
        ttk.Label(mainframe,text="Line Style").grid(column=0,row=6)
        combo_linestyle=ttk.Combobox(mainframe,textvariable=self.linestyle,state="readonly",width=5)
        combo_linestyle["values"]=["None","-","--","-.",":"]#Those are all the posible options for the linestyle
        combo_linestyle.grid(column=1,row=6)
        
        #Change the axis labels
        ttk.Label(mainframe,text="X axis Label").grid(column=0,row=7,columnspan=2)
        ttk.Label(mainframe,text="Y axis Label").grid(column=2,row=7,columnspan=2)
        self.x_label=StringVar()#Variable storing the label for the x axis
        self.y_label=StringVar()#Variable storing the label for the y axis
        ttk.Entry(mainframe,textvar=self.x_label).grid(column=0,row=8,columnspan=2)
        ttk.Entry(mainframe,textvar=self.y_label).grid(column=2,row=8,columnspan=2)
        ttk.Button(mainframe,text="Update Labels",command=self.update_labels).grid(column=4,row=8)#This button aplies the labels in the axis

        #Make the plot
        ttk.Button(mainframe,text="Plot",command=self.make_plot).grid(column=0,row=11)
        #Save the figure
        ttk.Button(mainframe,text="Save",command=self.save_plot).grid(column=1,row=11)
        #Options of subplots
        #Reset one of the subplots
        ttk.Button(mainframe,text="Reset Subplot",command=self.reset_subplot).grid(column=4,row=1)
        # Export a configuration file of the plots, this will allow to redo the figure
        ttk.Button(mainframe,text="Export",command=self.export_logfile).grid(column=2,row=11)
        # Import a configuration file of the plots, this will allow to redo a previous exported figure using the logfile
        ttk.Button(mainframe,text="import",command=self.read_logfile).grid(column=3,row=11)
    def init_program(self,*args):
        #This functions set all the presets for the program to work
        self.create_subplots()#First we create the subplots required by self.total_rows/columns
        self.current_column.set(1)#We set the focus on the
        self.current_row.set(1)#(1,1) subplot (remember that we start to count in 1 ,not 0.
        self.change_subplot()#Aply the changes in the focus of the subplot

    def create_subplots(self,*args):
        #This function will create the subplot axes, and the needed variables
        self.fig=Figure()#This will replace the figure in the main routine (its necesary to change the size of the figure without closing
        #the program
        self.canvas=FigureCanvasTkAgg(self.fig,master=self.mainframe)#We have to redefine the canvas
        self.canvas.show()
        self.canvas.get_tk_widget().grid(column=5,row=0,rowspan=12)
        self.axes=[[]]#This variable will store the axes of each subplots. Th axe os a subplot is what allow to make the plot in that subplot
        self.file_index=[[]]#This will save wich data files were plotted in each subplot, its necessary in order to write the logfile
        self.label_index=[[]]#This variable store the labels for making the logfile
        self.marker_index=[[]]#This one store the marker for each data set
        self.linestyle_index=[[]]#This one stores line style
        self.xlabel_index=[[]]#This will save the labels used for the x axis
        self.ylabel_index=[[]]#This will save the labels used for the y axis
        #Now we will append an axe inside self.axes for each subplot, it will be stored so it is accesible with [row][column]
        #We need to append also a list for each subplot in the other variables
        for j in range(self.total_columns.get()):#First we make a lopp throw the first row
            self.axes[0].append(self.fig.add_subplot(self.total_rows.get(),self.total_columns.get(),j+1))#Append an axe subplot in each column
            self.file_index[0].append([])#Append a list for each column
            self.label_index[0].append([])
            self.marker_index[0].append([])
            self.linestyle_index[0].append([])
            self.xlabel_index[0].append("")#Append a blank string for each column
            self.ylabel_index[0].append("")#Append a blank string for each column
        if (self.total_rows.get()-1)!=0:#If we have more than one row we repeat the previous steps for each row
            for i in range(1,self.total_rows.get()):
                self.axes.append([])#We need to append a list for each row here
                self.file_index.append([])#also in this one 
                self.label_index.append([])#And this one
                self.marker_index.append([])#and this one 
                self.linestyle_index.append([])#and this one
                self.xlabel_index.append([])
                self.ylabel_index.append([])
                for j in range(self.total_columns.get()):#The next steps are the same than in the previous loop
                    self.axes[i].append(self.fig.add_subplot(self.total_rows.get(),self.total_columns.get(),1+j+self.total_columns.get()*i))
                    self.file_index[i].append([])
                    self.label_index[i].append([])
                    self.marker_index[i].append([])
                    self.linestyle_index[i].append([])
                    self.xlabel_index[i].append("")
                    self.ylabel_index[i].append("")
        self.fig.tight_layout()#We let maplotlib to optimize the space around the subplots
        self.canvas.draw()#We dray the changes, now the main figure is divided in the subplots
        self.box_current_column["values"]=range(1,self.total_columns.get()+1)#Update the possible values in the combobox
        self.box_current_row["values"]=range(1,self.total_rows.get()+1)#of the columns and rows to make the change posiible
        self.figure_created=True#We save that we have created a figure with subplots

    def change_subplot(self,*args):#This function will set the focus on the proper subplot
        self.current_axe=self.axes[self.current_row.get()-1][self.current_column.get()-1]#We marke as the current axe the one we have chosen
        self.label.set("")#Reset the values of the labels 
        self.x_label.set(self.xlabel_index[self.current_row.get()-1][self.current_column.get()-1])#This set the correct x label
        self.y_label.set(self.ylabel_index[self.current_row.get()-1][self.current_column.get()-1])#This set the correct ylabel
    def save_plot(self,*args):
        self.fig.savefig(tkFileDialog.asksaveasfilename(filetypes=(('Portable Document Format','*.pdf' ),
                                                                   ('Portable Network Graphics','*.png'),
                                                                                       ('All files','*.*'))))

    def update_labels(self,*args):
        self.current_axe.set_xlabel(self.x_label.get())
        self.current_axe.set_ylabel(self.y_label.get())
        self.xlabel_index[self.current_row.get()-1][self.current_column.get()-1]=self.x_label.get()
        self.ylabel_index[self.current_row.get()-1][self.current_column.get()-1]=self.y_label.get()
        self.fig.tight_layout()
        self.canvas.draw()
    def reset_subplot(self,*args):
        self.current_axe.clear()
        self.canvas.draw()
    def set_custom_marker(self,*args):
        self.marker.set(self.marker_custom.get())
    def open_file(self,*args):
        self.filename.set(tkFileDialog.askopenfilename())
        self.label.set("")
    def make_plot(self,*args):
        self.file_index[self.current_row.get()-1][self.current_column.get()-1].append(self.filename.get())
        self.label_index[self.current_row.get()-1][self.current_column.get()-1].append(self.label.get())
        self.marker_index[self.current_row.get()-1][self.current_column.get()-1].append(self.marker.get())
        self.linestyle_index[self.current_row.get()-1][self.current_column.get()-1].append(self.linestyle.get())
        f=open(self.filename.get())
        x=[]
        y=[]
        for l in f:
            try:
                x.append(float(l.split()[0]))
                y.append(float(l.split()[1]))
            except:
                pass
        self.current_axe.plot(x,y,marker=self.marker.get(),linestyle=self.linestyle.get(),label=self.label.get())
        self.current_axe.legend(loc="best")
        self.fig.tight_layout()
        self.canvas.draw()
    
    def export_logfile(self,*args):
        filename=(tkFileDialog.asksaveasfilename())
        f=open(filename,'w+')
        f.write("Total Rows "+str(self.total_rows.get())+" Total Columns "+str(self.total_columns.get())+"\n")
        for i in range(self.total_rows.get()):
            for j in range(self.total_columns.get()):
                f.write('row= ')
                f.write(str(i+1))
                f.write(' column= ')
                f.write(str(j+1))
                f.write('\n')
                f.write("xlabel "+self.xlabel_index[i][j]+"\n")
                f.write("ylabel "+self.ylabel_index[i][j]+"\n")
                for k in range(len(self.file_index[i][j])):
                    f.write('file ')
                    f.write(str(k+1))
                    f.write('\n')
                    f.write('Marker '+self.marker_index[i][j][k]+'\n')
                    f.write('Linestyle '+self.linestyle_index[i][j][k]+'\n')
                    f.write('Label '+self.label_index[i][j][k]+'\n')
                    f.write('Data '+self.file_index[i][j][k]+'\n')
                    
    def read_logfile(self,*args):
        filename=(tkFileDialog.askopenfilename())
        self.load_logfile(filename)
    def load_logfile(self,filename):
        f=open(filename,'r')
        for l in f:
            if l.startswith("Total Row"):
                total_rows=int(l.split()[2])
                total_columns=int(l.split()[5])
                if not (total_rows<=self.total_rows.get() & total_columns<=self.total_columns.get() & self.figure_created):
                    self.total_rows.set(total_rows)
                    self.total_columns.set(total_columns)
                    self.create_subplots()
            elif l.startswith("row"):
                self.current_row.set(int(l.split()[1]))
                self.current_column.set(int(l.split()[3]))
                self.change_subplot()
            elif l.startswith("xlabel"):
                xlabel=""
                if len(l.split())>2:
                    for palabra in l.split()[1:-1]:
                        xlabel+=palabra+" "
                    xlabel+=l.split()[-1]
                elif len(l.split())==2:
                    xlabel=l.split()[1]
                self.x_label.set(xlabel)
                self.update_labels()
            elif l.startswith("ylabel"):
                ylabel=""
                if len(l.split())>2:
                    for palabra in l.split()[1:-1]:
                        ylabel+=palabra+" "
                    ylabel+=l.split()[-1]
                elif len(l.split())==2:
                    ylabel=l.split()[1]
                self.y_label.set(ylabel)
                self.update_labels()
            elif l.startswith("Marker"):
                self.marker.set(l.split()[1])
            elif l.startswith("Linestyle"):
                self.linestyle.set(l.split()[1])
            elif l.startswith("Label"):
                label=""
                if len(l.split())>2:
                    for palabra in l.split()[1:-1]:
                        label=label+palabra+" "
                    label=label+l.split()[-1]
                elif len(l.split())==2:
                    label=l.split()[1]
                self.label.set(label)
            elif l.startswith("Data"):
                filename2=""
                if len(l.split())>2:
                    for palabra in l.split()[1:-1]:
                        filename2=filename2+palabra+" "
                    filename2=filename2+l.split()[-1]
                elif len(l.split())==2:
                    filename2=l.split()[1]
                self.filename.set(filename2)
                self.make_plot()
        f.close()
root=Tk()
root.title("Plotter")
plotprog=plotter(root)
if len(sys.argv)==3: #Anhadimos la posibilidad de hacer la grafica usando un logfile desde la terminal
    plotprog.load_logfile(sys.argv[1])#Archivo de entrada sys.argv[1]
    plotprog.fig.savefig(sys.argv[2])#archivo de salida sys.argv[2]
else:
    root.mainloop()#Si no ejecutamos el programa de forma normal
