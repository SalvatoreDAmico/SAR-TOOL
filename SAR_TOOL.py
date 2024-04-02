"""
SAR-TOOL 1.0

@author: Salvatore D'Amico and Francesco Guglielmino (INGV R0MA2, INGV OE)
email: salvatore.damico2@ingv.it






SAR-TOOLS is a open-source software: you can redistribute it and/or modify it under the terms of the GNU 
Affero General Public License as published by the Free Software Foundation, either version 3 of the License, 
or (at your option) any later version.
This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even 
the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU Affero General Public License for more details: <https://www.gnu.org/licenses/>
"""

# LIBRARIES ##########################################################################################################################################################
import os
import customtkinter
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import rasterio
from tkinter import (END,Tk,filedialog, messagebox, scrolledtext)
import tkinter as tk
##########################################################################################################################################################

# Set the initial mode
mode = 'dark'
color = 'blue'
customtkinter.set_appearance_mode(mode)
customtkinter.set_default_color_theme(color)

def change_mode():
    global mode
    if mode == 'dark':
        mode = 'light'
        output_text.configure(background="white", foreground="black")
    else:
        mode = 'dark'
        output_text.configure(background="black", foreground="white")
    customtkinter.set_appearance_mode(mode)

# Global variables for file import and cell size
global import_file
global cellsize

# Button variables
button1 = None
button2 = None
button3 = None
button4 = None
button5 = None
button6 = None
button7 = None
button8 = None
button9 = None
button10 = None
button11 = None
button12 = None
button12_2 = None
button13 = None
button14 = None

def clear_terminal():
    output_text.delete('1.0', tk.END)

def clear_all():
    for widget in center_frame.winfo_children():
        widget.destroy()

def clear_all_2():
    for widget in right_frame.winfo_children():
        widget.destroy()

def clear_frames():
    clear_all()
    clear_all_2()

def display_buttons():
    global button1, button2, button3
    clear_frames()
    title2_tools = customtkinter.CTkLabel(right_frame, text="Tools")
    title2_tools.pack()

    button1 = customtkinter.CTkButton(right_frame, text="GDAL info", command=gdalinfo, width=20, height=3)
    button2 = customtkinter.CTkButton(right_frame, text="Create an ENVI file", command=hdr, width=20, height=3)
    button3 = customtkinter.CTkButton(right_frame, text="Phase to Displacement Conversion", command=CONVERSION, width=20, height=3)
    button1.pack(pady=10)
    button2.pack(pady=10)
    button3.pack(pady=10)

def display_buttons_elaboration():
    global button4, button5, button6, button7, button8
    clear_frames()
    title2_tools = customtkinter.CTkLabel(right_frame, text="Tools")
    title2_tools.pack()

    button4 = customtkinter.CTkButton(right_frame, text="Convert to .TIFF file", command=TIFF_CREATION, width=20, height=3)
    button4.pack(pady=10)
    button5 = customtkinter.CTkButton(right_frame, text="Reprojection (Lat/Long to UTM)", command=utm, width=20, height=3)
    button5.pack(pady=10)
    button6 = customtkinter.CTkButton(right_frame, text="Crop Raster file", command=CROP, width=20, height=3)
    button6.pack(pady=10)
    button7 = customtkinter.CTkButton(right_frame, text="Intersection Raster files", command=INTERSECTION, width=20, height=3)
    button7.pack(pady=10)
    button8 = customtkinter.CTkButton(right_frame, text="Change Pixel Size and Resolution for multiple Raster files", command=same_res_pix, width=20, height=3)
    button8.pack(pady=10)

def display_buttons_visualization():
    global button9, button10, button11
    clear_frames()
    title2_tools = customtkinter.CTkLabel(right_frame, text="Tools")
    title2_tools.pack()

    button10 = customtkinter.CTkButton(right_frame, text="Show an image", command=show_image, width=20, height=3)
    button10.pack(pady=10)
    #button11 = customtkinter.CTkButton(right_frame, text="Show interferometric SAR data", command=sar, width=20, height=3)
    #button11.pack(pady=10)
    #button9 = customtkinter.CTkButton(right_frame, text="Create a Vector Displacement Map", command=displacement_map, width=20, height=3)
    #button9.pack(pady=10)

def display_buttons_sistem():
    global button12, button12_2
    clear_frames()
    title2_tools = customtkinter.CTkLabel(right_frame, text="Tools")
    title2_tools.pack()

    #button12 = customtkinter.CTkButton(right_frame, text="S I S T E M", command=RUN_SISTEM, width=20, height=3)
    #button12.pack(pady=10)
    #button12_2 = customtkinter.CTkButton(right_frame, text="loop SISTEM", command=LOOP_SISTEM, width=20, height=3)
    #button12_2.pack(pady=10)

def display_buttons_synthetic_model():
    global button13, button14, button15
    clear_frames()
    title2_tools = customtkinter.CTkLabel(right_frame, text="Tools")
    title2_tools.pack()

    button13 = customtkinter.CTkButton(right_frame, text="Mogi Model", command=Synthetic_Model, width=20, height=3)
    button13.pack(pady=10)
    button14 = customtkinter.CTkButton(right_frame, text="Generate random Points", command=gps_random, width=20, height=3)
    button14.pack(pady=10)
    button15 = customtkinter.CTkButton(right_frame, text="Generate evenly spaced points", command=equally_spaced_gps, width=20, height=3)
    button15.pack(pady=10)

def get_screen_size():
    root = tk.Tk()
    root.update_idletasks()
    width = root.winfo_screenwidth()
    height = root.winfo_screenheight()
    root.destroy()
    return width, height

# Get screen size using the new function
screen_width, screen_height = get_screen_size()

# ROOT ######################################################################################################################################

from tkinter import scrolledtext
import sys
root = customtkinter.CTk()
from PIL import Image, ImageTk
import ctypes
root.title("S A R - T O O L")

# Calculate the width and height ratios based on screen resolution
width_ratio = screen_width / 1920
height_ratio = screen_height / 1080

# Calculate the adjusted dimensions for the root window
adjusted_width = int(1100 * width_ratio)
adjusted_height = int(950 * height_ratio)
root.geometry(f"{adjusted_width}x{adjusted_height}")
# Create three frames, one for each column
left_frame = customtkinter.CTkFrame(root)
center_frame = customtkinter.CTkFrame(root)
basso_dx_frame = customtkinter.CTkFrame(root)
right_frame = customtkinter.CTkFrame(root)

# titles frame
title_tools=customtkinter.CTkLabel(left_frame, text="Categories")
title_tools.pack()

# Add the frames to the main window
left_frame.grid(row=0, column=0,rowspan=2, sticky="nsew")
center_frame.grid(row=0, column=2, sticky="nsew", rowspan=4)
right_frame.grid(row=0, column=1, sticky="nsew", rowspan=2)
basso_dx_frame.grid(row=1, column=0, sticky="nsew", rowspan=1)
basso_dx_frame.grid(row=2, column=0, columnspan=2, sticky="nsew")
# Create a text widget to display the output
output_text = scrolledtext.ScrolledText(root, width=30, height=40, font=("Courier", int(12 * width_ratio)))
output_text.grid(row=0, column=3, sticky="nsew", padx=int(20 * width_ratio), pady=int(20 * height_ratio), rowspan=4)

# Define the rows and columns to expand properly
root.grid_rowconfigure(0, weight=1)
root.grid_rowconfigure(1, weight=1)
root.grid_rowconfigure(2, weight=1)
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)
root.grid_columnconfigure(2, weight=5)
root.grid_columnconfigure(3, weight=5)
# Set the weights of the rows
root.rowconfigure(0, weight=1)

# Function to update the output text
def update_output_text(message):
    output_text.insert(tk.END, message + '\n')
    output_text.see(tk.END)  # Auto-scroll to the bottom
# Redirect standard output and standard error to the text widget
class StdoutRedirector:
    def __init__(self, text_widget):
        self.text_widget = text_widget

    def write(self, message):
        update_output_text(message)

class StderrRedirector:
    def __init__(self, text_widget):
        self.text_widget = text_widget

    def write(self, message):
        update_output_text(message)

# Create instances of the redirectors and set them as the new standard output and error
stdout_redirector = StdoutRedirector(output_text)
stderr_redirector = StderrRedirector(output_text)
sys.stdout = stdout_redirector
sys.stderr = stderr_redirector
# Redirect print statements to the text widget
def redirect_print(*args, **kwargs):
    message = ' '.join(map(str, args)) + ' '.join(f'{key}={value}' for key, value in kwargs.items())
    update_output_text(message)

# Replace the default print function with our custom redirect_print
print = redirect_print

# Set the background color to black
output_text.configure(background="black", foreground="white")


### FUNCTIONS########################################################################################################################################################
from tkinter import filedialog, Toplevel, Message, messagebox
from osgeo import gdal

def gdalinfo():
    '''
    The gdalinfo() function opens a file dialog where the user can select a file. Once the file is selected,
    the gdal.Info() method is used to obtain information about the file and display it in a message box.
    '''

    # Open a file dialog to select a file
    infopath = filedialog.askopenfilename(title="Select a Raster File...")

    # Check if a file was selected or the dialog was canceled
    if not infopath:
        return

    try:
        # Open the selected file
        dataset = gdal.Open(infopath, gdal.GA_ReadOnly)

        if dataset is None:
            raise Exception("Failed to open the raster file.")

        # Retrieve raster information
        info = gdal.Info(dataset, deserialize=True)
        print("____________________________________________________")
        print("GDAL INFORMATIONS:")
        print(info)
        # Close the dataset
        dataset = None
        print("____________________________________________________")
        

    except Exception as e:
        messagebox.showerror("Error", f"Error retrieving information: {str(e)}")

def hdr():

    '''
    This function creates a GUI window using the Tkinter library in Python. 
    It creates a series of labels and text boxes to allow the user to input various parameters for a .hdr file. 
    
    Each of these parameters is assigned a label and a text box, 
    with a label indicating the name of the parameter and the text box allowing the user to enter the value for that parameter. 
    The values are stored in variables, such as data1, data2, and so on, which are of type tk.IntVar or tk.StringVar.
    
    Subsequently, a function named getInput is defined.
    This function receives input from the text boxes and creates a header file for an ENVI file format.
    The header file parameters are stored in a list named params.
    
    Next, the user is prompted to select a file using the filedialog.askopenfilename method, 
    which opens a file selection window and returns the path of the selected file. 
    The path is stored in hdrpath. The file name is then appended with ".hdr" to create the header file name.
    
    Finally, the header file is created using a with statement that opens the file in write mode ('w') 
    and writes the parameters from the params list to the file, one per line. 
    The file is saved in the same directory as the selected file with the ".hdr" extension.
    
    A label named path_output is also created to display the path of the created header file 
    and is packed into the GUI window. 
    The content of the label is also printed to the console.
    '''
    
    #.HDR FILE PARAMETERS #########################################################################################################################
    
    # samples
    label1=customtkinter.CTkLabel(center_frame, text="samples:")
    label1.pack()
    data1=customtkinter.IntVar()
    textbox1=customtkinter.CTkEntry(center_frame, textvariable=data1)
    textbox1.pack()

    #lines
    label2=customtkinter.CTkLabel(center_frame, text="lines:")
    label2.pack()
    data2=customtkinter.IntVar()
    textbox2=customtkinter.CTkEntry(center_frame, textvariable=data2)
    textbox2.pack()

    #bands
    label3=customtkinter.CTkLabel(center_frame, text="bands:")
    label3.pack()
    data3=customtkinter.IntVar()
    textbox3=customtkinter.CTkEntry(center_frame, textvariable=data3)
    textbox3.pack()

    #interleave
    label4=customtkinter.CTkLabel(center_frame, text="interleave:")
    label4.pack()
    data4=customtkinter.StringVar()
    textbox4=customtkinter.CTkEntry(center_frame, textvariable=data4)
    textbox4.pack()

    #data type
    label5=customtkinter.CTkLabel(center_frame, text="data type:")
    label5.pack()
    data5=customtkinter.IntVar()
    textbox5=customtkinter.CTkEntry(center_frame, textvariable=data5)
    textbox5.pack()

    #byte order
    label6=customtkinter.CTkLabel(center_frame, text="byte order:")
    label6.pack()
    data6=customtkinter.IntVar()
    textbox6=customtkinter.CTkEntry(center_frame, textvariable=data6)
    textbox6.pack()

    #x min
    label9=customtkinter.CTkLabel(center_frame, text="Longitude min:")
    label9.pack()
    data9=customtkinter.IntVar()
    textbox9=customtkinter.CTkEntry(center_frame, textvariable=data9)
    textbox9.pack()
    #y max
    label10=customtkinter.CTkLabel(center_frame, text="Latitude max:")
    label10.pack()
    data10=customtkinter.IntVar()
    textbox10=customtkinter.CTkEntry(center_frame, textvariable=data10)
    textbox10.pack()
    #x size
    label11=customtkinter.CTkLabel(center_frame,text="x size:")
    label11.pack()
    data11=customtkinter.IntVar()
    textbox11=customtkinter.CTkEntry(center_frame, textvariable=data11)
    textbox11.pack()
    #y size
    label12=customtkinter.CTkLabel(center_frame,text="y size:")
    label12.pack()
    data12=customtkinter.IntVar()
    textbox12=customtkinter.CTkEntry(center_frame, textvariable=data12)
    textbox12.pack()
    #format

    
    # Function to acquire parameters, create a list, and export them to a .hdr file
    def getInput():
        a=textbox1.get()
        b=textbox2.get()
        c=textbox3.get()
        d=textbox4.get()
        e=textbox5.get()
        f=textbox6.get()

        i=textbox9.get()
        l=textbox10.get()
        m=textbox11.get()
        n=textbox12.get()
    

        global params
        params = [
            "ENVI",
            "samples = "+a,
            "lines = "+" "+b,
            "bands = "+" "+c,
            "interleave = "+" "+d,
            "data type = "+" "+e,
            "byte order = "+" "+f,
            "map info = "+" "+"{Geographic Lat/Lon, 0.5000, 0.5000"+", "+i+", "+l+", "+m+", "+n+", "+"WGS-84, units=Degrees}"
            ]
        
        hdrpath=filedialog.askopenfilename(title="Select a file..", filetypes=(("all files","*.*"),("text files",".txt")))
        hdrpath_output=customtkinter.CTkLabel(center_frame, text=hdrpath)
        
        with open(hdrpath+".hdr", 'w') as fp:
            for item in params:
                fp.write("%s\n" % item)
                
            path_output=customtkinter.CTkLabel(center_frame, text=fp)
            path_output.pack()
            print(path_output)

    button_hdr2 = customtkinter.CTkButton(center_frame, text="Save and export data to an ENVI file", 
                                        bg="orange", command=getInput)
    button_hdr2.pack(pady=10)


from osgeo.gdal import deprecation_warn
from osgeo_utils.gdal_calc import *  # noqa
from osgeo_utils.gdal_calc import main as gdal_calc_main

# The deprecation_warn function can be directly called in your code if necessary
deprecation_warn("gdal_calc")

def CONVERSION():
    '''
    In the window, there are several input fields for the user to enter information, including a formula for calculation, a format, and a NoData value.
    
    Once the user enters the information and clicks the "Submit" button, the code uses the filedialog module 
    to open a file dialog window to allow the user to select a file to use as input. 
    The code then opens another file dialog window to allow the user to select a directory where the output file will be saved. 
    The code then opens a third file dialog window to allow the user to enter the name of the output file.
    
    The information entered by the user in the text boxes, as well as the selected input and output files, 
    are used to create a gdal_calc.py command which is then executed using the os.system method. 
    The command performs a calculation using the GDAL library, using the input file, the formula entered by the user, 
    the format entered by the user, and the NoData value entered by the user. The output of the calculation is saved in the specified output file.
    '''

    title_gdalcalc=customtkinter.CTkLabel(center_frame, text="Phase to Displacement:")
    title_gdalcalc.pack()
    #formula

    formula_label=customtkinter.CTkLabel(center_frame,text="Enter calculation formula (use A as variable):")
    formula_label.pack()
    data_formula=customtkinter.IntVar()
    textbox_formula=customtkinter.CTkEntry(center_frame, textvariable=data_formula)
    textbox_formula.pack()

    # Format
    format_label=customtkinter.CTkLabel(center_frame,text="Enter the format (ex: ENVI):")
    format_label.pack()
    data_format=customtkinter.IntVar()
    textbox_format=customtkinter.CTkEntry(center_frame, textvariable=data_format)
    textbox_format.pack()

    # NoData
    nodata_label=customtkinter.CTkLabel(center_frame,text="NoData Value (ex: -9999):")
    nodata_label.pack()
    data_nodata=customtkinter.IntVar()
    textbox_nodata=customtkinter.CTkEntry(center_frame, textvariable=data_nodata)
    textbox_nodata.pack()

    def gdalcalc():
        from tkinter import messagebox
        from tkinter import filedialog
    
        # Select file
        A = filedialog.askopenfilename(filetypes=[("all files", "*.*"), ("ENVI file", ".BIL"), ("ENVI file", ".hdr"), ("GAMMA file", ".geo"), ("GEOTIFF", ".TIF"), ("GEOTIFF", ".TIFF")])
        if not A:  # Ensure the user has selected a file
            return
        
        # Select save location
        directory_calc = filedialog.askdirectory(title="Select the save folder..")
        if not directory_calc:  # Ensure the user has selected a folder
            return
        
        # Define output
        name_file_calc = filedialog.asksaveasfilename(filetypes=[("all files", "*.*"), ("GEO files", ".geo"), ("GEOTIFF files", ".geotiff"), ("GAMMA files", ".gamma")])
        if not name_file_calc:  # Ensure the user has provided a file name
            return
    
        formula = textbox_formula.get()
        nodatavalue = textbox_nodata.get()
        format = textbox_format.get()
    
        # Prepare arguments as list
        args = [
            'dummy',  # gdal_calc_main expects the script name as the first argument; can be any string
            '-A', A,
            '--outfile', name_file_calc,
            '--calc', formula,
            '--format', format,
            '--NoDataValue', nodatavalue,
            '--overwrite'
        ]
    
        # Execute gdal_calc_main with prepared arguments
        try:
            gdal_calc_main(args)
            messagebox.showinfo("Success", "Processing completed successfully.")
        except Exception as e:
            messagebox.showerror("Error", str(e))
            
    button_gdalcalc = customtkinter.CTkButton(center_frame, text="Insert",  command=gdalcalc)
    button_gdalcalc.pack()

def TIFF_CREATION():
    print("With this tool, you can convert your data into raster images with the .tif format.")
    print("1. Start by selecting the files you want to convert.")
    print("2. Choose the save folder.")

    filetypes = [
        ("All Files", ".*"),
        ("ASCII Files", "*.asc"),
        ("JPEG Files", "*.jpg"),
        ("PNG Files", "*.png")
    ]

    filenames = filedialog.askopenfilenames(filetypes=filetypes) 
    if not filenames:
        tk.messagebox.showerror("Error", "You must select files to continue.")
        return
    
    directory = filedialog.askdirectory(title="Select the save folder..")
    if not directory:
        tk.messagebox.showerror("Error", "You must select a save folder to continue.")
        return

    for filename in filenames:
        input_translate = str(filename)
        file_base_name = os.path.splitext(os.path.basename(filename))[0]
        
        output_translate = os.path.join(directory, f"{file_base_name}.tif")
        
        try:
            translate_options = gdal.TranslateOptions(gdal.ParseCommandLine("-co COMPRESS=DEFLATE -co NUM_THREADS=ALL_CPUS"))
            gdal.Translate(output_translate, input_translate, options=translate_options)
            print("Your file is saved in:", output_translate)
        except Exception as e:
            print(f"Error converting {input_translate}: {str(e)}")
            print("_________________________________________________________________________________")

def utm():

    '''
    In the utm function, you have defined a GUI using the Tkinter library. The GUI contains a label "Conversion Lat/Lon -> UTM/m:", 
    an entry for the EPSG code, and a "Submit" button. When the button is clicked, the warp function is executed.
    
    The warp function first opens a file dialog window to allow the user to select the input file. 
    Then, it opens another dialog window to allow the user to select the output directory. 
    Afterwards, it opens a Save As dialog window to allow the user to specify the output file name.
    
    Next, the warp function extracts the EPSG code entered by the user and converts it into a string. 
    Then, it combines the EPSG string with the string "-t_srs EPSG:" to create the string that will be used as an argument for the gdal.WarpOptions function.
    
    Finally, the function uses the gdal.Warp function to perform the file conversion and saves the result in the specified output directory 
    with the specified name.
    '''
    print("With this tool, you can reproject your data into a different reference coordinate system.\n 1. Start by selecting the file you want to convert; \n 2. Choose the save folder; \n 3. Enter the name for your new file (you don't need to specify the format)")
    epsg=customtkinter.CTkLabel(center_frame,text="EPSG:")
    epsg.pack()
    data_epsg=customtkinter.IntVar()
    epsg_box=customtkinter.CTkEntry(center_frame, textvariable=data_epsg)
    epsg_box.pack()
        

    def warp():  
        
        
        filename = filedialog.askopenfilename() 
        input_warp=str(filename)

        directory=filedialog.askdirectory(title="Select the save folder..")
        input2=str(directory)

        name_file=filedialog.asksaveasfilename()
        formato=".tif"
        input2_1=os.path.basename(str(name_file))

        output=os.path.join(os.path.normpath(input2),input2_1)
        output_warp=str(output+formato)

        epsg=epsg_box.get()
        epsg=str(epsg)
        epsg="-t_srs"+" "+"EPSG:"+epsg

        warp_options = gdal.WarpOptions(gdal.ParseCommandLine(epsg))
        warp=gdal.Warp (output_warp, input_warp, options=warp_options)
        print("Your EPSG code is:", epsg)
        print("Your file is saved in:", output_warp)

        del warp
    button_gdalwarp = customtkinter.CTkButton(center_frame, text="Insert",command=warp)
    button_gdalwarp.pack()

def CROP():
    '''
    GUI that allows cropping an image using the GDAL library. The GUI is created using the tkinter library in Python.
    
    The GUI has a title label that describes the process for cropping an image and four labels and text boxes 
    to enter the values for the top left and bottom right corners of the crop area. 
    The values for the top left and bottom right corners are obtained by opening the image in an image viewer, 
    positioning the mouse over the top left corner and noting the x-min and y-max values, then positioning the mouse over the bottom right corner 
    and noting the x-max and y-min values.
    
    The code then has a "Crop" button, which opens a file dialog window to select the image to be cropped, 
    a directory dialog window to select the output directory for the cropped image, and a save file dialog 
    to enter the name of the output image. The input image and output directories are joined to create the output path. 
    The format of the output image is set to ".tif".
    
    The values entered in the four text boxes are used to create the "crop_command" string, 
    which is the GDAL command line option for cropping. The option is created by concatenating the values entered in the text boxes in the correct format. 
    The "crop_command" string is then passed to the GDAL WarpOptions function to create the crop options. 
    The GDAL Warp function is then called with the output path, input path, and crop options to perform the cropping. 
    Finally, the result of the cropping is deleted to free up memory.
    '''
    title_crop=customtkinter.CTkLabel(center_frame, text="Crop an image:\n To crop:\n - •	Go to the Visualization category and click on the Show an Image tool\n - go to the top left corner and mark the values (x min, y max)\n - go to the bottom left corner right and mark the values (x max, y min)")
    title_crop.pack() 
    crop1=customtkinter.CTkLabel(center_frame,text="LONGITUDE min:")
    crop1.pack() 
    cropdata1=customtkinter.IntVar()
    croptextbox1=customtkinter.CTkEntry(center_frame, textvariable=cropdata1)
    croptextbox1.pack() 
    #lines
    crop2=customtkinter.CTkLabel(center_frame,text="LATITUDE max:")
    crop2.pack() 
    cropdata2=customtkinter.IntVar()
    croptextbox2=customtkinter.CTkEntry(center_frame, textvariable=cropdata2)
    croptextbox2.pack() 
    #bands
    crop3=customtkinter.CTkLabel(center_frame,text="LONGITUDE max:")
    crop3.pack() 
    cropdata3=customtkinter.IntVar()
    croptextbox3=customtkinter.CTkEntry(center_frame, textvariable=cropdata3)
    croptextbox3.pack() 
    #interleave
    crop4=customtkinter.CTkLabel(center_frame,text="LATITUDE min:")
    crop4.pack() 
    cropdata4=customtkinter.IntVar()
    croptextbox4=customtkinter.CTkEntry(center_frame, textvariable=cropdata4)
    croptextbox4.pack() 
        


    def crop():
        filename = filedialog.askopenfilename() # show an "Open" dialog box and return the path to the selected file
        input_crop=str(filename)

        directory=filedialog.askdirectory(title="Select the save folder..")
        input2=str(directory)
        print(input2)

        name_file=filedialog.asksaveasfilename()
        formato=".tif"
        input2_1=os.path.basename(str(name_file))
        print(input2_1)

        output=os.path.join(os.path.normpath(input2),input2_1)
        output_crop=str(output+formato)
        print(output_crop)

        h_sx_corner=croptextbox1.get()
        l_sx_corner=croptextbox2.get()
        h_dx_corner=croptextbox3.get()
        l_dx_corner=croptextbox4.get()
        

        h_s_c=str(h_sx_corner)
        l_s_c=str(l_sx_corner)
        h_d_c=str(h_dx_corner)
        l_d_c=str(l_dx_corner)
        crop_tot=h_s_c+" "+l_s_c+" "+h_d_c+" "+l_d_c
        comando_crop="-te"+" "+crop_tot
        print(comando_crop)

        #"-te 473000 4147000 525000 4192000"
        crop_options = gdal.WarpOptions(gdal.ParseCommandLine(comando_crop))
        crop=gdal.Warp (output_crop, input_crop, options=crop_options)
        crop= None
        del crop

    button_crop = customtkinter.CTkButton(center_frame, text="Insert",command=crop)
    button_crop.pack()

def INTERSECTION():
    '''
    This function automates geospatial operations on raster images using Python's GDAL and OGR libraries, facilitating tasks like creating shapefiles from raster extents, intersecting rasters, and cropping rasters with a shapefile. Users interact through a GUI to select images and directories for input and output, enhancing usability. Key operations include:

    1. **Generating Shapefiles**: For each raster in a designated folder, the script generates a corresponding shapefile that outlines the raster's extent.
    2. **Performing Intersection**: Users select two raster images to intersect, creating a shapefile that represents their overlapping area.
    3. **Repeating Intersection**: The script allows for another pair of rasters to be intersected, demonstrating the process's repeatability.
    4. **Cropping Rasters**: Users can crop selected rasters to the bounds of a chosen shapefile, useful for focusing on specific areas.

    '''
    import os
    from osgeo import gdal, ogr

    # Set the directory where the images are located
    image_dir = filedialog.askdirectory(title="Select the folder where your rasters are located")
    
    if not image_dir:  # This checks if image_dir is an empty string
        messagebox.showerror("Error", "You have not selected any folder containing your rasters.")
        return  # Exit the function

    # Set the directory where you want to save the shapefiles
    shapefile_dir = filedialog.askdirectory(title="Select the shapefiles save folder")
    
    if not image_dir:  # This checks if image_dir is an empty string
        messagebox.showerror("Error", "You have not selected any folder.")
        return  # Exit the function

    # Get a list of all the image files in the directory
    image_files = [f for f in os.listdir(image_dir) if f.endswith('.jpg') or f.endswith('.png') or f.endswith('.tif')]

    # Loop through the image files
    for image_file in image_files:
        # Open the image file
        image_ds = gdal.Open(os.path.join(image_dir, image_file))
        
        # Create a shapefile for the image
        shapefile_driver = ogr.GetDriverByName('ESRI Shapefile')
        shapefile_ds = shapefile_driver.CreateDataSource(os.path.join(shapefile_dir, image_file.split('.')[0] + '.shp'))
        shapefile_layer = shapefile_ds.CreateLayer('layer', image_ds.GetSpatialRef(), ogr.wkbPolygon)
        
        # Create a field in the shapefile for the image file name
        field_defn = ogr.FieldDefn('image_file', ogr.OFTString)
        shapefile_layer.CreateField(field_defn)
        
        # Create a feature for the image in the shapefile
        feature = ogr.Feature(shapefile_layer.GetLayerDefn())
        feature.SetField('image_file', image_file)
        
        # Get the image extent and set it as the geometry for the feature
        image_extent = image_ds.GetGeoTransform()
        min_x = image_extent[0]
        max_y = image_extent[3]
        max_x = min_x + image_extent[1] * image_ds.RasterXSize
        min_y = max_y + image_extent[5] * image_ds.RasterYSize
        ring = ogr.Geometry(ogr.wkbLinearRing)
        ring.AddPoint(min_x, min_y)
        ring.AddPoint(max_x, min_y)
        ring.AddPoint(max_x, max_y)
        ring.AddPoint(min_x, max_y)
        ring.AddPoint(min_x, min_y)
        poly = ogr.Geometry(ogr.wkbPolygon)
        poly.AddGeometry(ring)
        feature.SetGeometry(poly)
        
        # Add the feature to the shapefile layer
        shapefile_layer.CreateFeature(feature)
        
        # Clean up
        feature.Destroy()
        shapefile_ds.Destroy()
        image_ds = None

    #creation shp intersection
    master=filedialog.askopenfilename(title="Select MASTER",filetypes=(("all files","*.*"),("GEO files",".geo"),("GEOTIFF files",".geotiff"),("GAMMA files",".gamma"))) # show an "Open" dialog box and return the path to the selected file
    input_master=str(master)
    print(input_master)

    slave=filedialog.askopenfilename(title="Select SLAVE",filetypes=(("all files","*.*"),("GEO files",".geo"),("GEOTIFF files",".geotiff"),("GAMMA files",".gamma"))) # show an "Open" dialog box and return the path to the selected file
    input_slave=str(slave)
    print(input_slave)

    output_intersezione_shp=filedialog.askdirectory()
    input3=str(output_intersezione_shp)
    print(input3)    
    
    import subprocess

    comando_inters = ["ogr2ogr", "-overwrite", "-clipsrc", input_master, f"{input3}/intersection.shp", input_slave]
    
    try:
        subprocess.check_call(comando_inters)
        print("Success.")
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")

    #comando_inters="ogr2ogr -clipsrc"+" "+input_master+" "+input3+"/"+"intersection.shp"+" "+input_slave
    #os.system(comando_inters)

    master_2=filedialog.askopenfilename(title="Select MASTER",filetypes=(("all files","*.*"),("GEO files",".geo"),("GEOTIFF files",".geotiff"),("GAMMA files",".gamma"))) # show an "Open" dialog box and return the path to the selected file
    input_master_2=str(master_2)
    print(input_master_2)

    slave_2=filedialog.askopenfilename(title="Select SLAVE",filetypes=(("all files","*.*"),("GEO files",".geo"),("GEOTIFF files",".geotiff"),("GAMMA files",".gamma"))) # show an "Open" dialog box and return the path to the selected file
    input_slave_2=str(slave_2)
    print(input_slave_2)

    output_intersezione_shp=filedialog.askdirectory()
    input3=str(output_intersezione_shp)
    print(input3)    

    comando_inters="ogr2ogr -clipsrc"+" "+input_master_2+" "+input3+"/"+"intersection.shp"+" "+input_slave_2
    os.system(comando_inters)

    # Select the shapefile for cropping
    cropper_shp = filedialog.askopenfilename(title="Select the shapefile for cropping", filetypes=(("Shapefile", "*.shp"), ("All Files", "*.*")))
    input_shp = str(cropper_shp)
    print(input_shp)

    # Select the input images to be cropped
    input_images = filedialog.askopenfilenames(title="Select the input images to be cropped", filetypes=(("All Files", "*.*"), ("GeoTIFF Files", "*.tif")))
    input_tifs = list(input_images)
    print(input_tifs)

    # Select the output directory for the cropped images
    output_dir = filedialog.askdirectory(title="Select the output directory for the cropped images")
    if not output_dir:
        messagebox.showerror("Error", "No output directory selected.")
        exit()
        
    output_tifs = []

    # Loop through the input TIFF files and execute gdalwarp command for cropping
    for input_tif in input_tifs:
        input_filename = os.path.splitext(os.path.basename(input_tif))[0]
        output_tif = os.path.join(output_dir, input_filename + "_cropped.tif")
    
        comando_crop = ["gdalwarp", "-cutline", input_shp, "-crop_to_cutline", input_tif, output_tif]
    
        try:
            subprocess.check_call(comando_crop)
            print(f"Cropped image created: {output_tif}")
        except subprocess.CalledProcessError as e:
            print(f"Error cropping image {input_tif}: {e}")

    print(output_tifs)

def same_res_pix():
    '''
    The GUI window contains two input fields for entering two pixel values and a button 
    for executing a specific function when clicked.
    
    The function begins by creating a GUI window using the Tk() method. 
    Then, two labels named "pixel:" and two corresponding text boxes are created 
    using the Label() and Entry() methods, respectively. The text boxes are used to input the two pixel values, 
    which are stored in IntVar variables named pixeldata_a and pixeldata_b.
    
    The next step involves defining the pixel_same() function, which is executed when the "Submit" button is clicked. 
    The function starts by using the askopenfilename() method of the filedialog module to display an "Open" dialog window 
    to select a .shp file and stores its path in the shp_input variable. The same process is repeated 
    to select a save folder and two image files, storing their paths 
    in the save_folder, input_img, and name_file_px variables, respectively.
    
    Subsequently, the function retrieves the two pixel values from the text boxes using the get() method 
    and stores them as strings in the pixel_1 and pixel_2 variables. The values are concatenated to form a single string pixel_tot
    with the format pix_1 + " " + pix_2. The command string is then created as "-tr" + " " + pixel_tot.
    
    Finally, the function creates an intersection string containing the command to perform a GDAL warp operation 
    using the gdalwarp function. The command includes the -cutline and -tr options with the paths of the .shp file, the image file, 
    and the save file. The os.system() method is then used to execute the command as a shell command.
    
    After defining the pixel_same() function, the "Submit" button is created using the Button() method, 
    with the command option set to pixel_same, so that the function is executed when the button is clicked. 
    Finally, the mainloop() method is called to display the GUI window and wait for user input.

    
    '''

    pixel_a=customtkinter.CTkLabel(center_frame,text="pixel:")
    pixel_a.pack()
    pixeldata_a=customtkinter.IntVar()
    pixeltextboxa=customtkinter.CTkEntry(center_frame, textvariable=pixeldata_a)
    pixeltextboxa.pack()

    pixelb=customtkinter.CTkLabel(center_frame,text="pixel:")
    pixelb.pack()
    pixeldata_b=customtkinter.IntVar()
    pixeltextboxb=customtkinter.CTkEntry(center_frame, textvariable=pixeldata_b)
    pixeltextboxb.pack()



    def pixel_same():
        shp_input = filedialog.askopenfilename(title="Select .shp", filetypes=(("all files", "*.*"), ("GEO files", ".geo"), ("GEOTIFF files", ".geotiff"), ("GAMMA files", ".gamma")))
        input1 = str(shp_input)
        print(input1)

        save_folder = filedialog.askdirectory()
        input4 = str(save_folder)
        print(input4)

        img_inputs = filedialog.askopenfilenames(title="Select .shp", filetypes=(("all files", "*.*"), ("GEO files", ".geo"), ("GEOTIFF files", ".geotiff"), ("GAMMA files", ".gamma")))
        img_inputs = list(img_inputs)
        print(img_inputs)

        name_file_px = filedialog.asksaveasfilename(filetypes=(("all files", "*.*"), ("GEO files", ".geo"), ("GEOTIFF files", ".geotiff"), ("GAMMA files", ".gamma")))
        output_px = str(name_file_px)
        print(output_px)

        pixel_1 = pixeltextboxa.get()
        pixel_2 = pixeltextboxb.get()

        pix_1 = str(pixel_1)
        pix_2 = str(pixel_2)
        pixel_tot = pix_1 + " " + pix_2
        comando = "-tr" + " " + pixel_tot
        print(comando)

        for img_input in img_inputs:
            intersection = "gdalwarp -cutline" + " " + shp_input + " " + comando + " " + img_input + " " + name_file_px
            os.system(intersection)
    
    button_pixelsame = customtkinter.CTkButton(center_frame, text="Insert", command=pixel_same)
    button_pixelsame.pack()

def same_res_pix():


    pixel_a=customtkinter.CTkLabel(center_frame,text="pixel:")
    pixel_a.pack()
    pixeldata_a=customtkinter.IntVar()
    pixeltextboxa=customtkinter.CTkEntry(center_frame, textvariable=pixeldata_a)
    pixeltextboxa.pack()

    pixelb=customtkinter.CTkLabel(center_frame,text="pixel:")
    pixelb.pack()
    pixeldata_b=customtkinter.IntVar()
    pixeltextboxb=customtkinter.CTkEntry(center_frame, textvariable=pixeldata_b)
    pixeltextboxb.pack()



    def pixel_same():
        shp_input = filedialog.askopenfilename(title="Select .shp", filetypes=(("all files", "*.*"), ("GEO files", ".geo"), ("GEOTIFF files", ".geotiff"), ("GAMMA files", ".gamma")))
        input1 = str(shp_input)
        print(input1)

        save_folder = filedialog.askdirectory()
        input4 = str(save_folder)
        print(input4)

        img_inputs = filedialog.askopenfilenames(title="Select .shp", filetypes=(("all files", "*.*"), ("GEO files", ".geo"), ("GEOTIFF files", ".geotiff"), ("GAMMA files", ".gamma")))
        img_inputs = list(img_inputs)
        print(img_inputs)

        name_file_px = filedialog.asksaveasfilename(filetypes=(("all files", "*.*"), ("GEO files", ".geo"), ("GEOTIFF files", ".geotiff"), ("GAMMA files", ".gamma")))
        output_px = str(name_file_px)
        print(output_px)

        pixel_1 = pixeltextboxa.get()
        pixel_2 = pixeltextboxb.get()

        pix_1 = str(pixel_1)
        pix_2 = str(pixel_2)
        pixel_tot = pix_1 + " " + pix_2
        comando = "-tr" + " " + pixel_tot
        print(comando)

        for img_input in img_inputs:
            intersection = "gdalwarp -cutline" + " " + shp_input + " " + comando + " " + img_input + " " + name_file_px
            os.system(intersection)
    
    button_pixelsame = customtkinter.CTkButton(center_frame, text="Insert", command=pixel_same)
    button_pixelsame.pack()

def pixel():

    titolo_px=customtkinter.CTkLabel(center_frame, text="Set pixel size:")
    titolo_px.pack()
    pixel1=customtkinter.CTkLabel(center_frame,text="pixel:")
    pixel1.pack()
    pixeldata1=customtkinter.IntVar()
    pixeltextbox1=customtkinter.CTkEntry(center_frame, textvariable=pixeldata1)
    pixeltextbox1.pack()

    pixel2=customtkinter.CTkLabel(center_frame,text="pixel:")
    pixel2.pack()
    pixeldata2=customtkinter.IntVar()
    pixeltextbox2=customtkinter.CTkEntry(center_frame, textvariable=pixeldata2)
    pixeltextbox2.pack()

    def is_supported_file(filename):
        try:
            gdal.Open(filename)
            return True
        except:
            return False

    def pixel2():
        filenames = filedialog.askopenfilenames()  # Allow user to select multiple files
        input_files = filenames.split() if isinstance(filenames, str) else filenames

        directory = filedialog.askdirectory(title="Select the save folder")
        output_folder = str(directory)

        for filename in input_files:
            if is_supported_file(filename):
                input_pixel = str(filename)

                # Extract the base filename without the extension
                base_filename = os.path.splitext(os.path.basename(filename))[0]

                # Add the "_px" suffix to the base filename for the output file
                output_filename = base_filename + "_px.tif"

                output = os.path.join(os.path.normpath(output_folder), output_filename)
                output_pixel = str(output)

                pixel_a = pixeltextbox1.get()
                pixel_b = pixeltextbox2.get()

                pix_a = str(pixel_a)
                pix_b = str(pixel_b)
                pixel_tot = pix_a + " " + pix_b
                comando = "-tr" + " " + pixel_tot

                pixel_options = gdal.WarpOptions(gdal.ParseCommandLine(comando))
                try:
                    pixel = gdal.Warp(output_pixel, input_pixel, options=pixel_options)
                    del pixel
                except:
                    # Skip the problematic file without printing an error message
                    pass
        print("Processing completed.")

    button_crop = customtkinter.CTkButton(center_frame,text="Insert", command=pixel2)
    button_crop.pack()

def show_image():
    from tkinter import messagebox
    from osgeo import gdal

    # Get a list of supported image formats
    supported_formats = [driver.GetMetadataItem(gdal.DMD_EXTENSION) for i in range(gdal.GetDriverCount()) for driver in [gdal.GetDriver(i)] if driver.GetMetadataItem(gdal.DCAP_RASTER)]

    # Remove empty strings from the list
    supported_formats = [fmt for fmt in supported_formats if fmt]

    # Print the supported formats
    print("Supported image formats:", ', '.join(supported_formats))
    print("_________________________________________________________________________")
    # Prompt the user to select an image file
    root = tk.Tk()
    root.withdraw()

    # Prompt per la selezione del file immagine
    filetypes = [("All files", "*.*")]
    image_directory = filedialog.askopenfilename(title="Select an Image File", filetypes=filetypes)
    if not image_directory:
        messagebox.showerror("Error", "No file selected.")
        return

    # Prova ad aprire l'immagine selezionata
    try:
        with rasterio.open(image_directory) as dataset:
            # Leggi il primo canale dell'immagine
            image_data = dataset.read(1)
            # Visualizza l'immagine
            fig, ax = plt.subplots(1, figsize=(12, 12))
            im = ax.imshow(image_data, cmap='gray')
            ax.set_title(os.path.basename(image_directory))
            ax.set_xlabel('Column')
            ax.set_ylabel('Row')
            plt.colorbar(im, ax=ax)
            plt.show()
    except Exception as e:
        messagebox.showerror("Error", f"Could not open file:\n{e}")


## SYNTHETIC MOGI MODEL
def Synthetic_Model():
    '''
    This function uses a graphical user interface (GUI) to input parameters for simulating volcanic activity through a synthetic Mogi model. 

    Collecting Input Parameters: The GUI prompts the user to input various parameters, including cell size, latitude and longitude boundaries, maximum elevation, radius, exponent for elevation calculation, depth, and others related to the Mogi source and displacement model.
    
    Simulating Volcano Topography and Displacement: Based on the input parameters, the script calculates a digital elevation model (DEM) of a volcano and the displacement fields using the Mogi model. This includes calculating displacements in the east-west, north-south, and vertical directions, as well as constructing a Jacobian matrix to describe the displacement gradient.
    
    Saving Results: The script saves the DEM and displacement fields as ESRI ASC files, and also generates several plots. These include the DEM, displacement components, Jacobian matrix components, line-of-sight (LOS) displacements for ascending and descending satellite passes, and a 3D plot of the DEM with the Mogi source indicated.
    
    Visualization: Matplotlib is used to create visual representations of the DEM, displacement fields, and the effects of the Mogi source at a specified depth. These visualizations are saved as images.
    
    '''

    import customtkinter
    from tkinter import messagebox, filedialog
    import numpy as np
    import matplotlib.pyplot as plt

    def simulate_volcano(cellsize, min_lat, max_lat, min_lon, max_lon, max_elevation, radius, exponent, depth, poisson, mu, P, a, i_angle, az_angle_max, az_angle_min):
        try:
            # Define the dimensions of the DEM
            width = max_lon - min_lon
            height = max_lat - min_lat
        
            # Adjust the width and height to ensure that the number of columns and rows are evenly divisible by the desired cell size
            cols = int(width / cellsize)
            rows = int(height / cellsize)
            width = cols * cellsize
            height = rows * cellsize
        
            # Calculate the cell size
            cellsize_x = cellsize
            cellsize_y = cellsize
        
            # Define the center of the volcano
            center_row = rows // 2
            center_col = cols // 2
        
            # Create a meshgrid of x and y coordinates
            x, y = np.meshgrid(np.linspace(min_lon + cellsize_x / 2, max_lon - cellsize_x / 2, cols),
                               np.linspace(min_lat + cellsize_y / 2, max_lat - cellsize_y / 2, rows))
            
            # Calculate the distance of each cell from the center of the volcano
            distance = np.sqrt((x - (min_lon + center_col * cellsize_x))**2 + (y - (min_lat + center_row * cellsize_y))**2)
        
            # Calculate the elevation values based on distance from the center of the volcano
            elevation = max_elevation * np.exp(-(distance / radius)**exponent)
             
            
            # Print the calculated values for verification
            #print(f'Calculated elevation at grid center (should be close to max_elevation): {elevation[center_row, center_col]}')
        
            # This output will verify if the elevation at the center is calculated correctly (close to the max_elevation).
        
            # Calculate the center of the grid for the Mogi source
            center_lon = (min_lon + max_lon) / 2
            center_lat = (min_lat + max_lat) / 2
        
            # Position of Mogi Source
            xo = center_lon
            yo = center_lat
            zo = depth
        
            # Calculate the distance from the source
            r = np.sqrt(((x - xo) ** 2) + ((y - yo) ** 2) + ((zo) ** 2))
            c = pow(a, 3) * P * (1 - poisson) / mu
            dx = x - xo
            dy = y - yo
            #Calculate the displacements
            Uxo=((a**3)*P*((1-poisson)/mu))*((x-xo)/r**3) 
            Uyo=((a**3)*P*((1-poisson)/mu))*((y-yo)/r**3)
            Uzo=((a**3)*P*((1-poisson)/mu))*((zo)/r**3)       
        
            J11 = c / pow(r, 3) - c * (3 * dx * dx / pow(r, 5))
            J12 = c * (-3 * dx * dy / pow(r, 5))
            J13 = c * (-3 * x * (zo) / pow(r, 5))
            J21 = J12
            J22 = c / pow(r, 3) - c * (3 * dy * dy / pow(r, 5))
            J23 = c * (-3 * dy * (zo) / pow(r, 5))
            J31 = c * (-3 * (zo) * dx / pow(r, 5))
            J32 = c * (-3 * (zo) * dy / pow(r, 5))
            J33 = c * (-3 * (zo) * (zo) / pow(r, 5))
        
            # Prepare the ESRI ASC file header
            header = f'ncols {cols}\n' \
                     f'nrows {rows}\n' \
                     f'xllcorner {min_lon}\n' \
                     f'yllcorner {min_lat}\n' \
                     f'cellsize {cellsize_x}\n' \
                     f'NODATA_value -9999\n'
        
            # File paths
            asc_file_path = filedialog.askdirectory()
            
            # Prima controlla se l'utente ha effettivamente scelto una directory
            if not asc_file_path:  # Se la stringa è vuota o None
                messagebox.showerror("Error", "Per favore, select a directory to save the files.")
                return  # Interrompe l'esecuzione della funzione
            
            # Poi aggiungi il separatore di percorso se necessario
            if not asc_file_path.endswith('\\'):
                asc_file_path += '\\'

            # Save the DEM as an ESRI ASC file
            # Save the x, y, and elevation datasets as separate ASC files
            x_asc_filename = asc_file_path + 'x_values.asc'
            y_asc_filename = asc_file_path + 'y_values.asc'
            elevation_asc_filename = asc_file_path + 'elevation.asc'
            asc_filename = asc_file_path + 'dem.asc'
        
            with open(x_asc_filename, 'w') as x_asc_file:
                # Write the header information
                x_asc_file.write(f'ncols {cols}\n')
                x_asc_file.write(f'nrows {rows}\n')
                x_asc_file.write(f'xllcorner {min_lon}\n')
                x_asc_file.write(f'yllcorner {min_lat}\n')
                x_asc_file.write(f'cellsize {cellsize_x}\n')
                x_asc_file.write(f'NODATA_value -9999\n')
        
                # Write the x data in row-major order (starting from the top-left corner)
                for row in range(rows - 1, -1, -1):
                    for col in range(cols):
                        x_asc_file.write(f'{x[row, col]} ')
                    x_asc_file.write('\n')
        
            with open(y_asc_filename, 'w') as y_asc_file:
                # Write the header information
                y_asc_file.write(f'ncols {cols}\n')
                y_asc_file.write(f'nrows {rows}\n')
                y_asc_file.write(f'xllcorner {min_lon}\n')
                y_asc_file.write(f'yllcorner {min_lat}\n')
                y_asc_file.write(f'cellsize {cellsize_x}\n')
                y_asc_file.write(f'NODATA_value -9999\n')
        
                # Write the y data in row-major order (starting from the top-left corner)
                for row in range(rows - 1, -1, -1):
                    for col in range(cols):
                        y_asc_file.write(f'{y[row, col]} ')
                    y_asc_file.write('\n')
        
            with open(elevation_asc_filename, 'w') as elevation_asc_file:
                # Write the header information
                elevation_asc_file.write(f'ncols {cols}\n')
                elevation_asc_file.write(f'nrows {rows}\n')
                elevation_asc_file.write(f'xllcorner {min_lon}\n')
                elevation_asc_file.write(f'yllcorner {min_lat}\n')
                elevation_asc_file.write(f'cellsize {cellsize_x}\n')
                elevation_asc_file.write(f'NODATA_value -9999\n')
        
                # Write the elevation data in row-major order (starting from the top-left corner)
                for row in range(rows - 1, -1, -1):
                    for col in range(cols):
                        elevation_asc_file.write(f'{elevation[row, col]} ')
                    elevation_asc_file.write('\n')
        
        
            with open(asc_filename, 'w') as asc_file:
                # Write the header information
                asc_file.write(f'ncols {cols}\n')
                asc_file.write(f'nrows {rows}\n')
                asc_file.write(f'xllcorner {min_lon}\n')
                asc_file.write(f'yllcorner {min_lat}\n')
                asc_file.write(f'cellsize {cellsize_x}\n')
                asc_file.write(f'NODATA_value -9999\n')
        
                # Write the elevation data in row-major order (starting from the top-left corner)
                for row in range(rows - 1, -1, -1):
                    for col in range(cols):
                        asc_file.write(f'{elevation[row, col]} ')
                    asc_file.write('\n')
                    
            # Save the displacement and Jacobian matrices as ESRI ASC files
            np.savetxt(asc_file_path + 'east_displacement.asc', Uxo, fmt='%.8f', comments='', header=header)
            np.savetxt(asc_file_path + 'north_displacement.asc', Uyo, fmt='%.8f', comments='', header=header)
            np.savetxt(asc_file_path + 'vertical_displacement.asc', Uzo, fmt='%.8f', comments='', header=header)
            np.savetxt(asc_file_path + 'J11.asc', J11, fmt='%.8f', comments='', header=header)
            np.savetxt(asc_file_path + 'J12.asc', J12, fmt='%.8f', comments='', header=header)
            np.savetxt(asc_file_path + 'J21.asc', J21, fmt='%.8f', comments='', header=header)
            np.savetxt(asc_file_path + 'J22.asc', J22, fmt='%.8f', comments='', header=header)
            np.savetxt(asc_file_path + 'J31.asc', J31, fmt='%.8f', comments='', header=header)
            np.savetxt(asc_file_path + 'J32.asc', J32, fmt='%.8f', comments='', header=header)
            np.savetxt(asc_file_path + 'J33.asc', J33, fmt='%.8f', comments='', header=header)
        
        
            lia = np.ones((rows, cols))
            i_angle = np.deg2rad(i_angle) 
            az_angle = np.deg2rad([az_angle_max, az_angle_min])
            lia = lia * i_angle
            S = lia
            Nsar = 1
        
            #print("i_angle",i_angle)
            #print("az_angle", az_angle)
            SS = np.zeros((Nsar, 3))
            for i in range(Nsar):
                SS[i,:] = [np.cos(az_angle[i])*np.sin(S[i, 0]), 
                            np.sin(az_angle[i])*np.sin(S[i, 1]), 
                            np.cos(S[i, 2])]
                
            sx = SS[:, 0]
            sy = SS[:, 1]
            sz = SS[:, 2]
        
            Ascending_LOS = ((Uxo * sx) + (Uyo * sy) + (Uzo * sz))
        
        
            # Calculate the Line Of Sight 2 (LOS)
        
            SS_descending = np.zeros((Nsar, 3))
            for i in range(Nsar):
                SS_descending[i, :] = [-np.cos(az_angle[i]) * np.sin(S[i, 0]),
                                    np.sin(az_angle[i]) * np.sin(S[i, 1]),
                                    np.cos(S[i, 2])]
        
            sx_descending = SS_descending[:, 0]
            sy_descending = SS_descending[:, 1]
            sz_descending = SS_descending[:, 2]
        
            Descending_LOS = ((Uxo * sx_descending) + (Uyo * sy_descending) + (Uzo * sz_descending))
        
            # Save the LOS data as text files
            np.savetxt(asc_file_path + 'Ascending_LOS.asc', Ascending_LOS, fmt='%.8f', comments='', header=header)
            np.savetxt(asc_file_path + 'Descending_LOS.asc', Descending_LOS, fmt='%.8f', comments='', header=header)
        
        
        
        
            # Plotting the Digital Elevation Model (DEM)
            fig = plt.figure(figsize=(10, 7))
            ax = fig.add_subplot(111)
        
            # Plotting the elevation data
            dem_plot = ax.imshow(elevation, cmap='terrain', extent=[min_lon, max_lon, min_lat, max_lat])
        
            # Adding a color bar
            cbar = fig.colorbar(dem_plot, ax=ax)
            cbar.set_label('Elevation (m)', labelpad=15)
        
            # Setting the title and axes labels
            ax.set_title('Digital Elevation Model (DEM)')
            ax.set_xlabel('Longitude')
            ax.set_ylabel('Latitude')
            plt.savefig(asc_file_path + 'DEM.png')


            # Define the colormap
            cmap = 'jet'
        
            # Plotting the displacement components: Uxo, Uyo, Uzo
            fig, axs = plt.subplots(1, 3, figsize=(18, 6))
        
            # West-East displacement (Uxo)
            im1 = axs[0].imshow(Uxo, cmap=cmap, extent=[min_lon, max_lon, min_lat, max_lat], origin='lower')
            axs[0].set_title('WEST-EAST displacement (Uxo)')
            cbar1 = fig.colorbar(im1, ax=axs[0])
            cbar1.set_label('displacement (mm)', labelpad=10)
        
            # North-South displacement (Uyo)
            im2 = axs[1].imshow(Uyo, cmap=cmap, extent=[min_lon, max_lon, min_lat, max_lat], origin='lower')
            axs[1].set_title('NORTH-SOUTH displacement (Uyo)')
            cbar2 = fig.colorbar(im2, ax=axs[1])
            cbar2.set_label('displacement (mm)', labelpad=10)
        
            # Vertical displacement (Uzo)
            im3 = axs[2].imshow(Uzo, cmap=cmap, extent=[min_lon, max_lon, min_lat, max_lat], origin='lower')
            axs[2].set_title('VERTICAL displacement (Uzo)')
            cbar3 = fig.colorbar(im3, ax=axs[2])
            cbar3.set_label('displacement (mm)', labelpad=10)
        
            # Adjust layout and show plot
            plt.tight_layout()
            plt.savefig(asc_file_path + 'Displacement_Components.png')
        
        
            # Plotting configurations
            fig, axs = plt.subplots(3, 3, figsize=(15, 15))
        
            # J11 component
            axs[0, 0].imshow(J11, cmap=cmap, extent=[min_lon, max_lon, min_lat, max_lat])
            axs[0, 0].set_title('J11')
            fig.colorbar(axs[0, 0].images[0], ax=axs[0, 0], orientation='vertical')
        
            # J12 component
            axs[0, 1].imshow(J12, cmap=cmap, extent=[min_lon, max_lon, min_lat, max_lat])
            axs[0, 1].set_title('J12')
            fig.colorbar(axs[0, 1].images[0], ax=axs[0, 1], orientation='vertical')
        
            # J13 component - not calculated in the provided code, assuming zero for visualization
            J13 = np.zeros_like(J11)
            axs[0, 2].imshow(J13, cmap=cmap, extent=[min_lon, max_lon, min_lat, max_lat])
            axs[0, 2].set_title('J13')
            fig.colorbar(axs[0, 2].images[0], ax=axs[0, 2], orientation='vertical')
        
            # J21 component
            axs[1, 0].imshow(J21, cmap=cmap, extent=[min_lon, max_lon, min_lat, max_lat])
            axs[1, 0].set_title('J21')
            fig.colorbar(axs[1, 0].images[0], ax=axs[1, 0], orientation='vertical')
        
            # J22 component
            axs[1, 1].imshow(J22, cmap=cmap, extent=[min_lon, max_lon, min_lat, max_lat])
            axs[1, 1].set_title('J22')
            fig.colorbar(axs[1, 1].images[0], ax=axs[1, 1], orientation='vertical')
        
            # J23 component - not calculated in the provided code, assuming zero for visualization
            J23 = np.zeros_like(J22)
            axs[1, 2].imshow(J23, cmap=cmap, extent=[min_lon, max_lon, min_lat, max_lat])
            axs[1, 2].set_title('J23')
            fig.colorbar(axs[1, 2].images[0], ax=axs[1, 2], orientation='vertical')
        
            # J31 component
            axs[2, 0].imshow(J31, cmap=cmap, extent=[min_lon, max_lon, min_lat, max_lat])
            axs[2, 0].set_title('J31')
            fig.colorbar(axs[2, 0].images[0], ax=axs[2, 0], orientation='vertical')
        
            # J32 component
            axs[2, 1].imshow(J32, cmap=cmap, extent=[min_lon, max_lon, min_lat, max_lat])
            axs[2, 1].set_title('J32')
            fig.colorbar(axs[2, 1].images[0], ax=axs[2, 1], orientation='vertical')
        
            # J33 component
            axs[2, 2].imshow(J33, cmap=cmap, extent=[min_lon, max_lon, min_lat, max_lat])
            axs[2, 2].set_title('J33')
            fig.colorbar(axs[2, 2].images[0], ax=axs[2, 2], orientation='vertical')
        
            # Adjust layout
            plt.tight_layout()
            plt.savefig(asc_file_path + 'Jacobian_Components.png')
        
            # Now plot the LOS displacements for ascending and descending passes
            fig, axs = plt.subplots(1, 2, figsize=(12, 6))
        
            # Ascending LOS
            axs[0].imshow(Ascending_LOS, cmap=cmap, extent=[min_lon, max_lon, min_lat, max_lat])
            axs[0].set_title('Ascending LOS')
            cbar3 = fig.colorbar(axs[0].images[0], ax=axs[0])
            cbar3.set_label('displacement (mm)', labelpad=10)
        
            # Descending LOS
            axs[1].imshow(Descending_LOS, cmap=cmap, extent=[min_lon, max_lon, min_lat, max_lat])
            axs[1].set_title('Descending LOS')
        
        
            cbar4 = fig.colorbar(axs[1].images[0], ax=axs[1])
            cbar4.set_label('displacement (mm)', labelpad=10)
        
            # Adjust layout and show plot
            plt.tight_layout()
            plt.savefig(asc_file_path + 'LOS.png')
        
            # Create a 3D plot
            fig = plt.figure(figsize=(14, 10))
            ax = fig.add_subplot(111, projection='3d')
        
            # Plot the surface
            surf = ax.plot_surface(x, y, elevation, cmap='terrain', alpha=0.7)
        
            # Add a color bar which maps values to colors.
            cbar = fig.colorbar(surf, shrink=0.5, aspect=5)
            cbar.set_label('Elevation (m)', labelpad=15)
        
            # Add the Mogi source as a red dot at the desired depth
            ax.scatter(center_lon, center_lat, -depth, color='r', s=50, label='Mogi Source')
        
            # Set labels and title
            ax.set_xlabel('Longitude')
            ax.set_ylabel('Latitude')
            ax.set_zlabel('Elevation (m)')
            ax.set_title('3D View of the DEM with Mogi Source')
        
            # Add legend
            ax.legend()
        
            # Show the plot
            plt.savefig(asc_file_path + '3D_DEM.png')
            
            return True  # Se tutto va bene, restituiamo True
        except Exception as e:
            print(f"An error occurred: {e}")
            return False  # Se c'è un'eccezione, restituiamo False
        
        
    # Function to be called when "Run Simulation" button is clicked
    def run_simulation():
        # Retrieve values from entries
        cellsize = float(cellsize_entry.get())
        min_lat = float(min_lat_entry.get())
        max_lat = float(max_lat_entry.get())
        min_lon = float(min_lon_entry.get())
        max_lon = float(max_lon_entry.get())
        max_elevation = float(max_elevation_entry.get())
        radius = float(radius_entry.get())
        exponent = float(exponent_entry.get())
        mogi_source_row = float(mogi_source_row_entry.get())
        mogi_source_col = float(mogi_source_col_entry.get())
        depth = float(depth_entry.get())  # Ensure the value is positive as needed
        poisson = float(poisson_entry.get())
        mu = float(mu_entry.get())
        P = float(P_entry.get())
        a = float(a_entry.get())
        i_angle = float(i_angle_entry.get())
        az_angle_max = float(az_angle_max_entry.get())
        az_angle_min = float(az_angle_min_entry.get())
        
        
        # Do something with the values, e.g. print them
        print("Cellsize:", cellsize)
        #print("Columns:", cols)
        print("Minimum latitude:", min_lat)
        print("Maximum latitude:", max_lat)
        print("Minimum longitude:", min_lon)
        print("Maximum longitude:", max_lon)
        print("Maximum elevation:", max_elevation)
        print("Radius:", radius)
        print("Exponent:", exponent)
        print("Position of Mogi Source (rows):",mogi_source_row)
        print("Position of Mogi Source (columns):",mogi_source_col)
        print("Depth (no insert minus):",depth)
        print("Poisson Ratio:", poisson)
        print("Modulus of Rigidity:", mu)
        print("Pressure Variation of the Source:",P)
        print("Radial size of the source:",a)
        print("Inclination Angle:",i_angle)
        print("Ascending Azimuth Angle value:",az_angle_max)
        print("Descending Azimuth Angle value:", az_angle_min)
        
        # Here you would call your actual simulation function with the parameters
        # For example: run_your_simulation_function(cellsize, min_lat, max_lat, ...)
        # Then call the simulation function with these values
        success = simulate_volcano(cellsize, min_lat, max_lat, min_lon, max_lon, max_elevation, radius, exponent, depth, poisson, mu, P, a, i_angle, az_angle_max, az_angle_min)

        # You can then check the success and report back to the user
        if success:
            messagebox.showinfo("Simulation", "Simulation completed successfully!")
        else:
            messagebox.showerror("Simulation", "There was an error during the simulation.")

    # Create the main window
    root = customtkinter.CTk()
    root.title("Input Parameters for Simulation")

    # Set up the layout with grid
    content_frame = customtkinter.CTkFrame(root)
    content_frame.pack(padx=20, pady=20)

    # Define a function to create label-entry pairs
    def create_label_entry(frame, text, row):
        label = customtkinter.CTkLabel(frame, text=text)
        label.grid(row=row, column=0, pady=10, sticky='w')
        entry = customtkinter.CTkEntry(frame, width=200)
        entry.grid(row=row, column=1, pady=10, sticky='w')
        return entry

    # Create labels and entry widgets for each parameter using customtkinter
    cellsize_entry = create_label_entry(content_frame, "Cell Size:", 0)
    min_lat_entry = create_label_entry(content_frame, "Minimum Latitude (UTM meters):", 1)
    max_lat_entry = create_label_entry(content_frame, "Maximum Latitude (UTM meters):", 2)
    min_lon_entry = create_label_entry(content_frame, "Minimum Longitude (UTM meters):", 3)
    max_lon_entry = create_label_entry(content_frame, "Maximum Longitude (UTM meters):", 4)
    max_elevation_entry = create_label_entry(content_frame, "Maximum Elevation (meters):", 5)
    radius_entry = create_label_entry(content_frame, "Radius (meters):", 6)
    exponent_entry = create_label_entry(content_frame, "Exponent:", 7)
    mogi_source_row_entry = create_label_entry(content_frame, "Mogi Source Row:", 8)
    mogi_source_col_entry = create_label_entry(content_frame, "Mogi Source Column:", 9)
    depth_entry = create_label_entry(content_frame, "Depth (meters):", 10)
    poisson_entry = create_label_entry(content_frame, "Poisson Ratio:", 11)
    mu_entry = create_label_entry(content_frame, "Modulus of Rigidity (Pa):", 12)
    P_entry = create_label_entry(content_frame, "Pressure Variation (Pa):", 13)
    a_entry = create_label_entry(content_frame, "Radial Size of the Source (meters):", 14)
    i_angle_entry = create_label_entry(content_frame, "Inclination Angle (degrees):", 15)
    az_angle_max_entry = create_label_entry(content_frame, "Ascending Azimuth Angle (degrees):", 16)
    az_angle_min_entry = create_label_entry(content_frame, "Descending Azimuth Angle (degrees):", 17)

    # Create a button that will run the simulation when pressed
    run_button = customtkinter.CTkButton(content_frame, text="Run Simulation", command=run_simulation)
    run_button.grid(row=18, column=0, columnspan=2, pady=20)

    # Start the user interface loop
    root.mainloop()


import numpy as np
from tkinter import Tk, filedialog, END
import customtkinter as ctk
import numpy as np
from tkinter import filedialog, Label, Listbox, Tk
import customtkinter as ctk  # Assicurati che customtkinter sia installato

# Define the function to browse for a file
def equally_spaced_gps():
    
    # La funzione suggerisce numeri accettabili di punti GPS in base alle dimensioni della griglia
    def suggest_gps_points(ncols, nrows, max_points=100):
        total_points = ncols * nrows
        suggested_points = []
        for i in range(1, max_points + 1):
            if total_points % i == 0:
                suggested_points.append(i)
        return suggested_points
    
    # Define functions
    def browse_dem_file():
        file_path = filedialog.askopenfilename(filetypes=[('ESRI ASC files', '*.asc')])
        if file_path:
            entry_dem.delete(0, END)
            entry_dem.insert(0, file_path)
    
    def browse_uxm_file():
        file_path = filedialog.askopenfilename(filetypes=[('ESRI ASC files', '*.asc')])
        if file_path:
            entry_uxm.delete(0, END)
            entry_uxm.insert(0, file_path)
    
    def browse_uym_file():
        file_path = filedialog.askopenfilename(filetypes=[('ESRI ASC files', '*.asc')])
        if file_path:
            entry_uym.delete(0, END)
            entry_uym.insert(0, file_path)
    
    def browse_uzm_file():
        file_path = filedialog.askopenfilename(filetypes=[('ESRI ASC files', '*.asc')])
        if file_path:
            entry_uzm.delete(0, END)
            entry_uzm.insert(0, file_path)
    
    def calculate_dem_components():
        dem_file = entry_dem.get()
        uxm_file = entry_uxm.get()
        uym_file = entry_uym.get()
        uzm_file = entry_uzm.get()
        sampling_step = int(entry_s.get())  # Passo di campionamento
        errx_value = float(entry_errx.get())
        erry_value = float(entry_erry.get())
        errz_value = float(entry_errz.get())
    
        # Read DEM data from the ASC file
        with open(dem_file, 'r') as f:
            ncols = int(f.readline().split()[1])
            nrows = int(f.readline().split()[1])
            xllcorner = float(f.readline().split()[1])
            yllcorner = float(f.readline().split()[1])
            cellsize = float(f.readline().split()[1])
            nodata_value = float(f.readline().split()[1])
            data = np.genfromtxt(f, skip_header=6)
    
        # Calculate the grid points using the sampling step
        X = np.arange(xllcorner, xllcorner + ncols * cellsize, cellsize * sampling_step)
        Y = np.arange(yllcorner, yllcorner + nrows * cellsize, cellsize * sampling_step)
        X, Y = np.meshgrid(X, Y)
        Z = data[::sampling_step, ::sampling_step]
    
        # Read Uxm, Uym, and Uzm data from the ASC files with the same sampling step
        Uxo = np.genfromtxt(uxm_file, skip_header=6)[::sampling_step, ::sampling_step]
        Uyo = np.genfromtxt(uym_file, skip_header=6)[::sampling_step, ::sampling_step]
        Uzo = np.genfromtxt(uzm_file, skip_header=6)[::sampling_step, ::sampling_step]
    
        # Flatten the arrays for saving
        x_coords = X.flatten()
        y_coords = Y.flatten()
        z_coords = Z.flatten()
        u100 = Uxo.flatten()
        v100 = Uyo.flatten()
        up100 = Uzo.flatten()
        
        # Calculate the actual number of GPS points that will be generated
        actual_number_of_points = len(x_coords)
    
        # Print the number of points that will be generated
        print(f"With a sampling step of {sampling_step}, you will have a number of points equal to: {actual_number_of_points}")
        
        # Stack the data and save it
        data = np.column_stack(
            (x_coords, y_coords, z_coords, u100, v100, up100, np.full(actual_number_of_points, errx_value), np.full(actual_number_of_points, erry_value), np.full(actual_number_of_points, errz_value)))

        filename_eps = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt")], title="Save GPS Data As")
        if filename_eps:
            
            np.savetxt(filename_eps, data, fmt='%.6f', delimiter='\t')

            print("Equidistant GPS points are created and saved to:", filename_eps)
        else:
            print("File save cancelled.")
            
    # Labels
    label_dem = customtkinter.CTkLabel(center_frame, text="DEM File:")
    label_uxm = customtkinter.CTkLabel(center_frame, text="W-E (x) Displacement File:")
    label_uym = customtkinter.CTkLabel(center_frame, text="N-S (y) Displacement File:")
    label_uzm = customtkinter.CTkLabel(center_frame, text="Vertical (z) Displacement File:")
    label_s = customtkinter.CTkLabel(center_frame, text="Sampling Rate Value:")
    label_errx = customtkinter.CTkLabel(center_frame, text="Error x Value:")
    label_erry = customtkinter.CTkLabel(center_frame, text="Error y Value:")
    label_errz = customtkinter.CTkLabel(center_frame, text="Error z Value:")
    
    label_dem.grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
    label_uxm.grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
    label_uym.grid(row=2, column=0, padx=5, pady=5, sticky=tk.W)
    label_uzm.grid(row=3, column=0, padx=5, pady=5, sticky=tk.W)
    label_s.grid(row=4, column=0, padx=5, pady=5, sticky=tk.W)
    label_errx.grid(row=5, column=0, padx=5, pady=5, sticky=tk.W)
    label_erry.grid(row=6, column=0, padx=5, pady=5, sticky=tk.W)
    label_errz.grid(row=7, column=0, padx=5, pady=5, sticky=tk.W)
    
    # Entry widgets
    entry_dem = customtkinter.CTkEntry(center_frame, width=80)
    entry_uxm = customtkinter.CTkEntry(center_frame, width=80)
    entry_uym = customtkinter.CTkEntry(center_frame, width=80)
    entry_uzm = customtkinter.CTkEntry(center_frame, width=80)
    entry_s = customtkinter.CTkEntry(center_frame, width=80)
    entry_errx = customtkinter.CTkEntry(center_frame, width=80)
    entry_erry = customtkinter.CTkEntry(center_frame, width=80)
    entry_errz = customtkinter.CTkEntry(center_frame, width=80)
    
    entry_dem.grid(row=0, column=1, padx=5, pady=5)
    entry_uxm.grid(row=1, column=1, padx=5, pady=5)
    entry_uym.grid(row=2, column=1, padx=5, pady=5)
    entry_uzm.grid(row=3, column=1, padx=5, pady=5)
    entry_s.grid(row=4, column=1, padx=5, pady=5)
    entry_errx.grid(row=5, column=1, padx=5, pady=5)
    entry_erry.grid(row=6, column=1, padx=5, pady=5)
    entry_errz.grid(row=7, column=1, padx=5, pady=5)
    
    # Buttons to browse files
    browse_dem_button = ctk.CTkButton(center_frame, text="Browse", command=browse_dem_file)
    browse_uxm_button = ctk.CTkButton(center_frame, text="Browse", command=browse_uxm_file)
    browse_uym_button = ctk.CTkButton(center_frame, text="Browse", command=browse_uym_file)
    browse_uzm_button = ctk.CTkButton(center_frame, text="Browse", command=browse_uzm_file)
    
    browse_dem_button.grid(row=0, column=2, padx=5, pady=5)
    browse_uxm_button.grid(row=1, column=2, padx=5, pady=5)
    browse_uym_button.grid(row=2, column=2, padx=5, pady=5)
    browse_uzm_button.grid(row=3, column=2, padx=5, pady=5)
    
    # Add a button to trigger file selection and calculation
    calculate_button = customtkinter.CTkButton(center_frame, text="Generate evenly spaced  GPS points", command=calculate_dem_components)
    calculate_button.grid(row=8, column=0, columnspan=2, padx=5, pady=20)

def gps_random():
    def browse_dem_file():
        file_path = filedialog.askopenfilename(filetypes=[('ESRI ASC files', '*.asc')])
        if file_path:
            entry_dem.delete(0, tk.END)
            entry_dem.insert(0, file_path)

    def browse_uxm_file():
        file_path = filedialog.askopenfilename(filetypes=[('ESRI ASC files', '*.asc')])
        if file_path:
            entry_uxm.delete(0, tk.END)
            entry_uxm.insert(0, file_path)

    def browse_uym_file():
        file_path = filedialog.askopenfilename(filetypes=[('ESRI ASC files', '*.asc')])
        if file_path:
            entry_uym.delete(0, tk.END)
            entry_uym.insert(0, file_path)

    def browse_uzm_file():
        file_path = filedialog.askopenfilename(filetypes=[('ESRI ASC files', '*.asc')])
        if file_path:
            entry_uzm.delete(0, tk.END)
            entry_uzm.insert(0, file_path)

    def calculate_dem_components():
        dem_file = entry_dem.get()
        uxm_file = entry_uxm.get()
        uym_file = entry_uym.get()
        uzm_file = entry_uzm.get()
        s_value = int(entry_s.get())
        errx_value = float(entry_errx.get())
        erry_value = float(entry_erry.get())
        errz_value = float(entry_errz.get())

        # Read DEM data from the ASC file
        with open(dem_file, 'r') as f:
            ncols = int(f.readline().split()[1])
            nrows = int(f.readline().split()[1])
            xllcorner = float(f.readline().split()[1])
            yllcorner = float(f.readline().split()[1])
            cellsize = float(f.readline().split()[1])
            nodata_value = float(f.readline().split()[1])
            data = np.genfromtxt(f, skip_header=6)

        X = np.arange(xllcorner, xllcorner + ncols * cellsize, cellsize)
        Y = np.arange(yllcorner, yllcorner + nrows * cellsize, cellsize)
        X, Y = np.meshgrid(X, Y)
        Z = data

        Uxo = np.genfromtxt(uxm_file, skip_header=6)
        Uyo = np.genfromtxt(uym_file, skip_header=6)
        Uzo = np.genfromtxt(uzm_file, skip_header=6)

        actual_size = Z.flatten().shape[0]
        rand_indices = np.random.choice(np.arange(actual_size), size=s_value, replace=False)
        random_points = np.column_stack((X.flatten()[rand_indices], Y.flatten()[rand_indices], Z.flatten()[rand_indices]))

        disp100 = np.column_stack((Uxo.flatten()[rand_indices], Uyo.flatten()[rand_indices], Uzo.flatten()[rand_indices]))
        u100 = disp100[:, 0]
        v100 = disp100[:, 1]
        up100 = disp100[:, 2]

        data = np.column_stack((random_points, u100, v100, up100, np.full(s_value, errx_value), np.full(s_value, erry_value), np.full(s_value, errz_value)))

        filename_eps = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt")], title="Save GPS Data As")
        if filename_eps:
            np.savetxt(filename_eps, data, fmt='%.6f', delimiter='\t')
            print("Random GPS points are created!")
        else:
            print("File cancelled.")
            
            

        # Labels
    label_dem = customtkinter.CTkLabel(center_frame, text="DEM File:")
    label_uxm = customtkinter.CTkLabel(center_frame, text="W-E (x) Displacement File:")
    label_uym = customtkinter.CTkLabel(center_frame, text="N-S (y) Displacement File:")
    label_uzm = customtkinter.CTkLabel(center_frame, text="Vertical (z) Displacement File:")
    label_s = customtkinter.CTkLabel(center_frame, text="Number of GPS Points:")
    label_errx = customtkinter.CTkLabel(center_frame, text="Error x Value:")
    label_erry = customtkinter.CTkLabel(center_frame, text="Error y Value:")
    label_errz = customtkinter.CTkLabel(center_frame, text="Error z Value:")

    label_dem.grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
    label_uxm.grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
    label_uym.grid(row=2, column=0, padx=5, pady=5, sticky=tk.W)
    label_uzm.grid(row=3, column=0, padx=5, pady=5, sticky=tk.W)
    label_s.grid(row=4, column=0, padx=5, pady=5, sticky=tk.W)
    label_errx.grid(row=5, column=0, padx=5, pady=5, sticky=tk.W)
    label_erry.grid(row=6, column=0, padx=5, pady=5, sticky=tk.W)
    label_errz.grid(row=7, column=0, padx=5, pady=5, sticky=tk.W)

    # Entry widgets
    entry_dem = customtkinter.CTkEntry(center_frame, width=80)
    entry_uxm = customtkinter.CTkEntry(center_frame, width=80)
    entry_uym = customtkinter.CTkEntry(center_frame, width=80)
    entry_uzm = customtkinter.CTkEntry(center_frame, width=80)
    entry_s = customtkinter.CTkEntry(center_frame, width=80)
    entry_errx = customtkinter.CTkEntry(center_frame, width=80)
    entry_erry = customtkinter.CTkEntry(center_frame, width=80)
    entry_errz = customtkinter.CTkEntry(center_frame, width=80)

    entry_dem.grid(row=0, column=1, padx=5, pady=5)
    entry_uxm.grid(row=1, column=1, padx=5, pady=5)
    entry_uym.grid(row=2, column=1, padx=5, pady=5)
    entry_uzm.grid(row=3, column=1, padx=5, pady=5)
    entry_s.grid(row=4, column=1, padx=5, pady=5)
    entry_errx.grid(row=5, column=1, padx=5, pady=5)
    entry_erry.grid(row=6, column=1, padx=5, pady=5)
    entry_errz.grid(row=7, column=1, padx=5, pady=5)

    # Buttons to browse files
    browse_dem_button = customtkinter.CTkButton(center_frame, text="Browse", command=browse_dem_file)
    browse_uxm_button = customtkinter.CTkButton(center_frame, text="Browse", command=browse_uxm_file)
    browse_uym_button = customtkinter.CTkButton(center_frame, text="Browse", command=browse_uym_file)
    browse_uzm_button = customtkinter.CTkButton(center_frame, text="Browse", command=browse_uzm_file)

    browse_dem_button.grid(row=0, column=2, padx=5, pady=5)
    browse_uxm_button.grid(row=1, column=2, padx=5, pady=5)
    browse_uym_button.grid(row=2, column=2, padx=5, pady=5)
    browse_uzm_button.grid(row=3, column=2, padx=5, pady=5)

    # Add a button to trigger file selection and calculation
    calculate_button = customtkinter.CTkButton(center_frame, text="Generate random GPS points", command=calculate_dem_components)
    calculate_button.grid(row=8, column=0, columnspan=2, padx=5, pady=20)


## SISTEM
def RUN_SISTEM():
    
    ############################################################################################################## PARTE 1
    '''
    The script first sets the global variables Snew and S, then proceeds to load and display the DEM data.
    The DEM data is stored in a file located at the path specified by dem_path, which is read into a 2D numpy array called dem
    using np.loadtxt. The shape of the array is then stored in the variables rows and columns.
    The DEM is then plotted.
    
    GPS data is loaded in a similar way, with gps_ON controlling whether or not the GPS data should be loaded.
    If gps_ON is True, the GPS data is loaded from the file specified by gps_path and stored in the array.
    The number of GPS data points is stored in the variable Ngps.
    If gps_ON is False, both the gps variable and Ngps are set to empty arrays.
    
    The same logic applies to loading LEVELING data, where liv_ON controls whether the data should be loaded or not.
    
    LIA data is stored in two arrays, LIA[0,:,:] and LIA[1,:,:].
    
    SAR data is loaded in a similar manner and stored in two arrays, SAR[0,:,:] and SAR[1,:,:], corresponding to "ascending" and "descending" data respectively.
    SAR data plots are created using matplotlib, with colormap and colorbar.
    
    Finally, LIA data is loaded and stored in a similar way to SAR data.
    LIA data plots are also created using matplotlib.
    '''
    import tkinter as tk
    import tkinter as tk
    #from tkinter import *
    from tkinter import filedialog
    import os
    from osgeo import ogr
    from tkinter import ttk
    import os
    from osgeo import gdal
    import numpy as np
    from tkinter.filedialog import askdirectory
    import tkinter.messagebox
    #import gdal
    from osgeo import gdal
    import rasterio
    from rasterio.plot import show
    import matplotlib.pyplot as plt
    import pandas as pd
    import xarray as xr
    import csv
    from tkinter import Toplevel, Message, Scrollbar, Text, messagebox, simpledialog
    import sys
    import subprocess
    import matplotlib
    global colonne,righe,xllcorner,yllcorner,cellsize,Nliv,rows,cols,min_lat,Nsar,max_lat,min_lon,max_lon,step,cellsize,dem,SAR,liv,LIA,rows_entry,cols_entry,min_lat_entry,max_lat_entry, inclination_angle_entry,min_lon_entry,max_lon_entry,step_entry,cellsize,gps,sigmae_entry,sigmal_entry,sigma_liv_entry,sigma_sar_entry,numeric_value,az_angle_max_entry,az_angle_min_entry
    rmse_e_list = []
    rmse_n_list = []
    rmse_up_list = []

    #S
    import numpy as np

    import tkinter as tk
    import tkinter as tk
    #from tkinter import *
    from tkinter import filedialog
    import os

    from tkinter import ttk

    import numpy as np
    from tkinter.filedialog import askdirectory
    import tkinter.messagebox
    #import gdal
    from osgeo import gdal

    import matplotlib.pyplot as plt
    import pandas as pd


    from tkinter import Toplevel, Message, Scrollbar, Text, messagebox, simpledialog

    import subprocess
    import tkinter as tk
    import tkinter as tk
    #from tkinter import *
    from tkinter import filedialog
    import os

    from tkinter import ttk

    import numpy as np
    from tkinter.filedialog import askdirectory
    import tkinter.messagebox
    #import gdal
    from osgeo import gdal

    import matplotlib.pyplot as plt
    import pandas as pd


    from tkinter import Toplevel, Message, Scrollbar, Text, messagebox, simpledialog

    import subprocess

    import numpy as np

    def browse_file(entry):
        filetypes = (("ASC files", "*.asc"), ("Text files", "*.txt"), ("All files", "*.*"))
        filepath = filedialog.askopenfilename(filetypes=filetypes)
        
        entry.delete(0, tk.END)
        entry.insert(tk.END, filepath)

    def save_values():
        dem_file = dem_entry.get()
        gps_file = gps_entry.get()
        liv_file = liv_entry.get()
        sar_file1 = sar1_entry.get()
        sar_file2 = sar2_entry.get()
        lia_file1 = lia1_entry.get()
        lia_file2 = lia2_entry.get()
        step = int(step_entry.get())
        ascending_az_angle = asc_az_entry.get()
        if ascending_az_angle:
            ascending_az_angle = float(ascending_az_angle)
        else:
            descending_az_angle = float('nan')
        descending_az_angle = desc_az_entry.get()
        if descending_az_angle:
            descending_az_angle = float(descending_az_angle)
        else:
            descending_az_angle = float('nan')
        k_value = int(k_entry.get())
        loc_value = loc_entry.get()
        sigmal = sigmal_entry.get()
        sigma_liv = sigma_liv_entry.get()
        sigma_sar = float(sigma_sar_entry.get())
        #inc_ang_val=float(inc_ang_entry.get())
        
        inc_ang_val = inc_ang_entry.get()
        if inc_ang_val:
            inc_ang_val = float(inc_ang_val)
        else:
            inc_ang_val = float('nan')
        inc_ang2_val = inc_ang2_entry.get()
        if inc_ang2_val:
            inc_ang2_val = float(inc_ang2_val)
        else:
            inc_ang2_val = float('nan')   
        #inc_ang2_val=float(inc_ang2_entry.get())

        print("##########################################")
        print("WELCOME ON SISTEM GRAPHICAL USER INTERFACE")
        print("##########################################")
        print("")
        print("__________________________________________")
        print("INPUT PATHS:")
        print("DEM:", dem_file)
        print("GPS:", gps_file)
        print("LEVELLING:", liv_file)
        print("FIRST SAR:", sar_file1)
        print("SECOND SAR:", sar_file2)
        print("FIRST LIA:", lia_file1)
        print("SECOND LIA:", lia_file2)
        print("NUMBER OF STEPS:", step)
        print("FIRST AZIMUTH ANGLE VALUE:", ascending_az_angle)
        print("SECOND AZIMUTH ANGLE VALUE:", descending_az_angle)
        print("K VALUE:", k_value)
        print("LOCALITY DENOMINATOR VALUE:", loc_value)
        print("SIGMA L VALUE:", sigmal)
        print("SIGMA LEVELLING VALUE:", sigma_liv)
        print("SIGMA SAR VALUE:", sigma_sar)
        print("FIRST INCLINATION ANGLE VALUE:", inc_ang_val)
        print("SECOND INCLINATION ANGLE VALUE:", inc_ang2_val)
        print("__________________________________________")



        import os

        folder_name = "SISTEM_OUTPUTS"

        # Get the user's desktop directory
        desktop_dir = os.path.join(os.path.expanduser("~"), "Desktop")

        # Specify the path where you want to create the folder
        folder_path = os.path.join(desktop_dir, folder_name)
        # Check if the folder already exists
        if os.path.exists(folder_path):
            # Find the highest numbered folder with the format "OUTPUTS_X"
            highest_number = 1
            while os.path.exists(os.path.join(desktop_dir, f"{folder_name}_{highest_number}")):
                highest_number += 1

            # Create a new folder with an incremented number
            new_folder_name = f"{folder_name}_{highest_number}"
            folder_path = os.path.join(desktop_dir, new_folder_name)
            os.makedirs(folder_path)
            
            print(f"A save folder '{folder_name}' has been created on your Desktop!")
            print("Folder path:", folder_path)
        else:
            # Create the folder
            os.makedirs(folder_path)

            print("A save folder has been created on your Desktop!")
            print("Folder path:", folder_path)

        # Check if required files are selected
        if not dem_file:
            messagebox.showerror("Error", "DEM is required")
            return

        elif not gps_file:
            messagebox.showerror("Error", "GPS is required")
            return


        elif not liv_file:
            liv = []
            Nliv = 0
            print("No Tiltimetric Data")
            print("__________________________________________")

        

        if dem_file:

            import numpy as np

            with open(dem_file, 'r') as file:
                header_lines = [file.readline().strip() for _ in range(6)]

            # Extract header information
            colonne = int(header_lines[0].split()[1])
            righe = int(header_lines[1].split()[1])
            xllcorner = float(header_lines[2].split()[1])
            yllcorner = float(header_lines[3].split()[1])
            cellsize = float(header_lines[4].split()[1])
            nodata_value = float(header_lines[5].split()[1])

            # Get the dimensions of the data
            width = colonne * cellsize
            height = righe * cellsize

            dem = np.loadtxt(dem_file, skiprows=6)  # Skip the header rows

            # Create a grid of X and Y coordinates
            x = np.linspace(xllcorner, xllcorner + width, colonne)
            y = np.linspace(yllcorner + height,yllcorner , righe)
            # Reverse the y values
            
            X, Y = np.meshgrid(x, y)
            

            # Calculate the elevation values
            elevation = dem

            # Save the DEM as a text file
            plot_path = os.path.join(folder_path, "DEM.txt")
            np.savetxt(plot_path, elevation, delimiter=' ')

            # Display a message while creating dem_xyz and saving it as a text file
            print("Please wait while the image is created...")

            import time
            # Calculate the execution time for creating dem_xyz and saving it as a text file
            start_time = time.time()

            # Create an array with x, y, and elevation values
            dem_xyz = np.column_stack((X.flatten(), Y.flatten(), elevation.flatten()))

            # Save the array as a text file
            plot_path = os.path.join(folder_path, "data_per_locality.txt")
            np.savetxt(plot_path, dem_xyz, delimiter=' ')

            end_time = time.time()
            execution_time = end_time - start_time
            print("Execution time:", execution_time, "seconds")

            # Print the extracted information
            print("__________________________________________")
            print("ESRI INFORMATIONS ABOUT DEM:")
            print("Columns: ", colonne)
            print("Rows: ", righe)
            print("Xllcorner: ", xllcorner)
            print("Yllcorner: ", yllcorner)
            print("Cellsize: ", cellsize)
            print("Nodata_value: ", nodata_value)
            print("__________________________________________")

            # Load the data from the text file
            dem_xyz = np.loadtxt(plot_path)

            # Extract the x, y, and elevation values from the array
            x = dem_xyz[:, 0]
            y = dem_xyz[:, 1]
            elevation = dem_xyz[:, 2]

            # Plot the data
            #plt.scatter(x, y, c=elevation, cmap='jet')
            #plt.colorbar(label='Elevation')
            #plt.xlabel('X')
            #plt.ylabel('Y')
            #plt.title('DEM')

            plt.imshow(dem, cmap='jet')
            plt.colorbar(label='Elevation (m)')
            plt.title('Digital Elevation Model')
            plt.xlabel('Columns')
            plt.ylabel('Rows')
            #plt.show()
            # Save the plot as an image file
            plot_path = os.path.join(folder_path, "DEM.png")
            plt.savefig(plot_path)

            # Close the plot to release memory (optional)
            plt.close()

        if gps_file:
            gps = np.loadtxt(gps_file)
            Ngps = gps.shape[0]
            print("Number of GPS points: ",Ngps)

            # Extract coordinates
            latitude = gps[:, 1]
            longitude = gps[:, 0]

            # Plot GPS data
            plt.quiver(longitude, latitude,gps[:,3],gps[:,4])
            plt.xlabel('Longitude')
            plt.ylabel('Latitude')
            plt.title('GPS Data')
            plt.grid(True)
            #plt.show()
            # Save the plot as an image file
            plot_path = os.path.join(folder_path, "gps.png")
            plt.savefig(plot_path)

            plt.close()
            
            print("__________________________________________")

        if sar_file1 and not sar_file2:

            Nsar=1
            print("Number of SARs: ",Nsar)
            SAR = np.zeros([Nsar, righe, colonne])
            sar_path = sar_file1
            ds = gdal.Open(sar_path)
            sar_image = ds.ReadAsArray()
            SAR[0, :, :] = sar_image

            # Display a message while creating dem_xyz and saving it as a text file
            print("Please wait while the image is created...")
        
            # Calculate the execution time for creating dem_xyz and saving it as a text file
            start_time = time.time()

            fig = plt.figure()
            plt.imshow(sar_image, cmap='jet')
            plt.title("First SAR")
            cbar = plt.colorbar()
            cbar.set_label('Displacement (m)')
            plt.xlabel('Columns')
            plt.ylabel('Rows')
            #plt.show()
            # Save the plot as an image file
            plot_path = os.path.join(folder_path, "First SAR.png")
            plt.savefig(plot_path)

            # Close the plot to release memory (optional)
            plt.close()

            end_time = time.time()
            execution_time = end_time - start_time
            print("Execution time:", execution_time, "seconds")


            print("You have selected 1 SAR")

            print("Processing SAR file 1:", sar_file1)
            print("__________________________________________")


        elif sar_file2 and not sar_file1:
            Nsar=1
            print("Number of SARs: ",Nsar)
            SAR = np.zeros([Nsar, righe, colonne])
            sar_path2 = sar_file2
            ds2 = gdal.Open(sar_path2)
            sar_image2 = ds2.ReadAsArray()
            SAR[0, :, :] = sar_image2

            
            print("Please wait while the image is created...")
        
            
            start_time = time.time()

            fig = plt.figure()
            plt.imshow(sar_image, cmap='jet')
            plt.title("First SAR")
            cbar = plt.colorbar()
            cbar.set_label('Displacement (m)')
            plt.xlabel('Columns')
            plt.ylabel('Rows')
            #plt.show()
            # Save the plot as an image file
            plot_path = os.path.join(folder_path, "First SAR.png")
            plt.savefig(plot_path)

            # Close the plot to release memory (optional)
            plt.close()

            end_time = time.time()
            execution_time = end_time - start_time
            print("Execution time:", execution_time, "seconds")

            
            print("You have selected 1 SAR.")
            print("Processing SAR file 1:", sar_file2)
            print("__________________________________________")


        elif sar_file1 and sar_file2:
            Nsar = 2
            print("Number of SARs: ",Nsar)
            SAR = np.zeros([2, righe, colonne])

            # Asce
            sar_path = sar_file1
            ds = gdal.Open(sar_path)
            sar_image = ds.ReadAsArray()
            SAR[0, :, :] = sar_image

            # Disce
            sar_path2 = sar_file2
            ds2 = gdal.Open(sar_path2)
            sar_image2 = ds2.ReadAsArray()
            SAR[1, :, :] = sar_image2

            # Display a message while creating dem_xyz and saving it as a text file
            print("Please wait while the image is created...")

            # Calculate the execution time for creating dem_xyz and saving it as a text file
            start_time = time.time()

            # Plots
            fig = plt.figure()

            ax1 = fig.add_subplot(1, 2, 1)
            ax1.set_title("First SAR")
            im1 = ax1.imshow(sar_image, cmap='jet')
            colorbar1 = fig.colorbar(im1, ax=ax1, orientation='horizontal')
            colorbar1.set_label("Displacement (m)")
            ax1.set_xlabel('Columns')
            ax1.set_ylabel('Rows')

            ax2 = fig.add_subplot(1, 2, 2)
            ax2.set_title("Second SAR")
            im2 = ax2.imshow(sar_image2, cmap='jet')
            colorbar2 = fig.colorbar(im2, ax=ax2, orientation='horizontal')
            colorbar2.set_label("Displacement (m)")
            ax2.set_xlabel('Columns')
            ax2.set_ylabel('Rows')
            # Save the plot as an image file
            plot_path = os.path.join(folder_path, "First and Second SAR.png")
            plt.savefig(plot_path)

            # Close the plot to release memory (optional)
            plt.close()
            #plt.show()

            end_time = time.time()
            execution_time = end_time - start_time
            print("Execution time:", execution_time, "seconds")
            print("__________________________________________")
            print("You have selected 2 SARs")
            print("__________________________________________")
            # Perform processing for SAR file 2
            print("Processing SAR file 2:", sar_file2)
            print("__________________________________________")

        elif not sar_file1 and not sar_file2:
            messagebox.showerror("Error", "Please select at least one SAR data")
            return

        #if lia_file1 or lia_file2:
        if lia_file1 and not lia_file2:

            Nlia=1
            print("Number of LIAs: ",Nlia)
            LIA = np.zeros([Nlia, righe, colonne])
            lia_path = lia_file1
            ds = gdal.Open(lia_path)
            lia = ds.ReadAsArray()
            LIA[0, :, :] = lia

            
            print("Please wait while the image is created...")
        
            
            start_time = time.time()

            fig = plt.figure()
            plt.imshow(lia, cmap='jet')
            plt.title("First LIA")
            cbar = plt.colorbar()
            #plt.show()
            
            plot_path = os.path.join(folder_path, "First LIA.png")
            plt.savefig(plot_path)

            
            plt.close()

            end_time = time.time()
            execution_time = end_time - start_time
            print("Execution time:", execution_time, "seconds")

            inclination_angle1=np.mean(np.mean(lia))
            print("You have selected 1 LIA. The Inclination angle is: ", inclination_angle1)
            
            inclination_angle1=np.deg2rad(inclination_angle1)
            print("The inclination angle in radiants is : ",inclination_angle1)
            print("__________________________________________")
            LIA[0,:,:]=inclination_angle1
            print("Processing LIA file 1:", lia_file1)
            print("__________________________________________")
            # TODO: 

        elif lia_file2 and not lia_file1:
            Nlia=1
            print("Number of LIAs: ",Nlia)
            LIA = np.zeros([Nlia, righe, colonne])
            lia_path = lia_file2
            ds = gdal.Open(lia_path)
            lia = ds.ReadAsArray()
            LIA[0, :, :] = lia

            
            print("Please wait while the image is created...")
        
            start_time = time.time()

            fig = plt.figure()
            plt.imshow(lia, cmap='jet')
            plt.title("First LIA")
            cbar = plt.colorbar()
            #plt.show()
            
            plot_path = os.path.join(folder_path, "First LIA.png")
            plt.savefig(plot_path)

            
            plt.close()

            end_time = time.time()
            execution_time = end_time - start_time
            print("Execution time:", execution_time, "seconds")

            inclination_angle2=np.mean(np.mean(lia))
            inclination_angle2=np.deg2rad(inclination_angle2)
            print("You have selected 1 LIA. The Inclination angle is: ", inclination_angle2)
            print("The inclination angle in radiants is : ",inclination_angle2)
            print("__________________________________________")

            LIA[0,:,:]=inclination_angle2
            print("Processing LIA file 2:", lia_file2)
            print("__________________________________________")
            # TODO: 

        elif lia_file1 and lia_file2:
            Nlia=2
            print("Number of LIAs: ",Nlia)
            LIA = np.zeros([Nlia, righe, colonne])
            lia_path=lia_file1
            ds = gdal.Open(lia_path)
            lia = ds.ReadAsArray()
            LIA[0, :, :] = lia
            lia_path2=lia_file2
            ds2 = gdal.Open(lia_path2)
            lia_disce = ds2.ReadAsArray()
            LIA[1, :, :] = lia_disce #lia_disce

        
            print("Please wait while the image is created...")
        
            
            start_time = time.time()

            fig = plt.figure()

            ax1 = fig.add_subplot(1, 2, 1)
            ax1.set_title("First LIA")
            im1 = ax1.imshow(lia, cmap='jet')
            fig.colorbar(im1, ax=ax1, orientation='horizontal')

            ax2 = fig.add_subplot(1, 2, 2)
            ax2.set_title("Second LIA")
            im2 = ax2.imshow(lia_disce, cmap='jet')
            fig.colorbar(im2, ax=ax2, orientation='horizontal')

            plot_path = os.path.join(folder_path, "First and Second LIA.png")
            plt.savefig(plot_path)

            
            plt.close()
            #plt.show()

            end_time = time.time()
            execution_time = end_time - start_time
            print("Execution time:", execution_time, "seconds")

            
            inclination_angle1=np.mean(np.mean(lia))
            inclination_angle2=np.mean(np.mean(lia_disce))

            inclination_angle1=np.deg2rad(inclination_angle1)
            inclination_angle2=np.deg2rad(inclination_angle2)

            LIA[0,:,:]=inclination_angle1

            if inclination_angle2 > 0:
                LIA[1,:,:]=inclination_angle2
            else:
                LIA[1,:,:]=[]
            print("You have selected 2 LIAs. The Ascending Inclination angle is (degrees): ", inclination_angle1)
            print("The Descending Inclination angle is (degrees): ", inclination_angle2)
            print("__________________________________________")

        elif not lia_file1 and not lia_file2:
            LIA = np.ones([Nsar, righe, colonne])
            print("__________________________________________")
            print("You have no LIAs")

            if Nsar ==1:    
                inclination_angle1 = float(inc_ang_val)
                print("First Inclination Angle:", inclination_angle1)
                print("First Inclination Angle in radiants:", np.deg2rad(inclination_angle1))

                
                #↨inclination_angle =np.deg2rad(inclination_angle)


                LIA[0,:,:] = np.deg2rad(inclination_angle1)

            elif Nsar > 1:
                inclination_angle1 = float(inc_ang_val)
                print("First Inclination Angle:", inclination_angle1)
                print("First Inclination Angle in radiants:", np.deg2rad(inclination_angle1))

                
                #↨inclination_angle =np.deg2rad(inclination_angle)


                
                inclination_angle2 = float(inc_ang2_val)
                print("Second Inclination Angle:", inclination_angle2)
                print("Second Inclination Angle in radiants:", np.deg2rad(inclination_angle2))

                LIA[0,:,:] = np.deg2rad(inclination_angle1)
                LIA[1,:,:]=np.deg2rad(inclination_angle2)

            

            
        domanda=messagebox.askyesno("Question", "Do you have Locality Data file?")
        if domanda:

            locality_file = filedialog.askopenfilename() # Replace with the actual path or name of your locality file

            average_interdistances = np.loadtxt(locality_file)
            print("Locality values opened from:", locality_file)
            print("__________________________________________")
            Nloc=1
            LOC=np.zeros([Nloc,righe,colonne])
            
            locality=average_interdistances
            #print(locality.shape)
            locality_plot=np.reshape(locality,(righe,colonne))    
            print(locality_plot.shape)


            LOC[0,:,:]=locality_plot

            Nrowloc=locality_plot.shape[0]
            Ncolsloc=locality_plot.shape[1]


            print('Locality shape: ',locality_plot.shape)
            

            fig = plt.figure()
            plt.imshow(locality_plot, cmap='jet')
            plt.title("Distribution Map for locality GPS values")
            cbar = plt.colorbar()
            cbar.set_label('Locality Value (m)', rotation=90)
            plot_path = os.path.join(folder_path, "Locality plots.png")
            plt.savefig(plot_path)

            # Close the plot to release memory (optional)
            plt.close()


            
        else:

            from tqdm import tqdm
            from tqdm import tqdm_gui
            import numpy as np
            from scipy.spatial import distance
            import heapq
            
            import tkinter as tk
            from tkinter import ttk

            import customtkinter

            
            def calculate_average_interdistance(array1, array2, k):
                avg_interdistances = []
                total_points = array1.shape[0]

                # Create a tkinter window
                window = customtkinter.CTk()
                window.title("Please Wait..")
                window.geometry("300x100")

                # Create a progress bar
                progressbar = ttk.Progressbar(basso_dx_frame, length=200, mode="determinate")
                progressbar.pack(pady=20)

                # Create a label for displaying progress information
                progress_label = customtkinter.CTkLabel(basso_dx_frame, text="")
                progress_label.pack()

                try:
                    for i, point1 in enumerate(array1):
                        distances = []
                        for point2 in array2:
                            dist = distance.euclidean(point1[:2], point2[:2])
                            distances.append(dist)
                        sorted_distances = sorted(distances)
                        nearest_distances = sorted_distances[:k]
                        avg_interdist = sum(nearest_distances) / k
                        avg_interdistances.append(avg_interdist)

                        # Update the progress bar
                        progress = int((i + 1) / total_points * 100)
                        progressbar["value"] = progress
                        progress_label.configure(text=f"Calculation of the Locality Matrix: {progress}%")
                        basso_dx_frame.update()

                finally:
                    # Close the window
                    #window.destroy()
                    progressbar.destroy()
                    progress_label.destroy()

                return np.array(avg_interdistances).reshape(-1)





            array1 = dem_xyz
            array2 = gps

            print("__________________________________________")
            print("K value selected is: ",k_value)
            print("__________________________________________")
            average_interdistances = calculate_average_interdistance(array1, array2, k_value)

            plot_path = os.path.join(folder_path, "average_interdistances.txt")
            
            np.savetxt(plot_path, average_interdistances, fmt='%.6f')
            absolute_path = os.path.abspath(plot_path)
            print("Locality values saving in:", absolute_path)
            print("__________________________________________")

            Nloc=1
            LOC=np.zeros([Nloc,righe,colonne])

            locality=np.loadtxt(absolute_path)
            print(locality.shape)
            locality_plot=np.reshape(locality,(righe,colonne))    
            print(locality_plot.shape)


            LOC[0,:,:]=locality_plot

            Nrowloc=locality_plot.shape[0]
            Ncolsloc=locality_plot.shape[1]


            print('Locality shape: ',locality_plot.shape)
            

            fig = plt.figure()
            plt.imshow(locality_plot, cmap='jet')
            plt.title("Distribution Map for locality GPS values")
            cbar = plt.colorbar()
            cbar.set_label('Locality Value (meters)', rotation=270)
            plot_path = os.path.join(folder_path, "Locality plots.png")
            plt.savefig(plot_path)

            # Close the plot to release memory (optional)
            plt.close()


            
        righe = dem.shape[0]
        colonne = dem.shape[1]


        # mi calcolo le coordinate
        max_lon = xllcorner + colonne * cellsize
        min_lon = xllcorner
        min_lat = yllcorner
        max_lat = yllcorner + righe * cellsize

        print("rows:", righe)
        print("cols:", colonne)
        print("Minimum Latitude:", min_lat)
        print("Maximum Latitude:", max_lat)
        print("Minimum Longitude:", min_lon)
        print("Maximum Longitude:", max_lon)

        ###################################################################################################### LOCALITY
        

        width=max_lon-min_lon
        height=max_lat-min_lat

        cellsize_x = width / colonne
        cellsize_y = height / righe

        cellsize=(cellsize_x+cellsize_y)/2

        Nsar = SAR.shape[0]

        minEast = min_lon
        maxNorth = max_lat


        W=np.ones([Nsar,1]) #WEIGHTS

        

        Nr = len(range(0, righe, step)) # number of lines in the solution
        Nc = len(range(0, colonne, step)) # number of columns in the solution

        U = np.zeros((3, Nr, Nc))
        E = np.zeros((3, 3, Nr, Nc))
        O = np.zeros((3, 3, Nr, Nc))
        STDX = np.zeros((12, Nr, Nc))

        pos = np.zeros((3, 1))

        '''
        A GUI is defined to show the user the progress of the pixel calculation
        '''
        import tkinter as tk
        from tkinter import ttk
        import customtkinter
        fin_pix = customtkinter.CTk()
        fin_pix.title("Pixel Transformation")
        fin_pix.geometry("350x100")

        label1 = customtkinter.CTkLabel(basso_dx_frame, text="Resolved Pixels:")
        label1.pack()

        
        progress = ttk.Progressbar(basso_dx_frame, orient="horizontal", length=200, mode="determinate", maximum=101, value=0, style="green.Horizontal.TProgressbar")
        progress.pack()
        label2 = customtkinter.CTkLabel(basso_dx_frame, text="Percentage:")
        label2.pack()

        jj = 0
        for j in range(0, colonne, step):
            
            pos[0] = minEast + cellsize*(j)

            ii = 0
            for i in range(0, righe, step):

            

                progress["value"] = int(round(jj/Nc*100))
                label1.configure(text="Resolved Pixels: {} out of {}".format(Nr*jj, Nr*Nc))
                label2.configure(text="Percentage: {}%".format(round(jj/Nc*100)))
                basso_dx_frame.update()

                pos[1] = maxNorth - cellsize*(i)
                pos[2] = dem[i][j]
                
                sar = SAR[:,i,j]
                lia= LIA[:,i,j]
                locality=LOC[:,i,j]
                loc_value=int(loc_value)
                sigmae=(locality)/loc_value
                sigman = sigmae*1
                sigmau = sigmae*1
                #sigmal = 400
                #sigma_liv = 0.001
                #sigma_sar = 0.001
                Ngps = gps.shape[0]



                '''

                If no levelling data are available, Nliv is set to 0.

                The number of SAR observations, Nsar, is obtained by taking the first dimension (number of rows) of the sar.

                S is set equal to lia.

                az_angle set to an array of two values representing azimuth angles in radians, [190, -10].

                over is set to 0.

                If over is True, the code checks if there are two SAR observations ( Nsar= 2). 
                If there are, it checks if both observations are not missing data, represented by NaN values, 
                using np.isnan.

                If there is no missing data in both SAR observations, the variables sigmae, sigman, and sigmau are divided by 2 
                to reduce the position.

                If only one of the two SAR observations has no missing data, Nsar= 1 
                and the relevant SAR data are assigned to the variables sar, S, W, and az_angle. 
                This is determined by checking which of the two SAR observations has no missing data and then assigning the relevant values.
                '''
                Nliv=None

                if Nliv is not None:

                    Nliv = liv.shape[0]
                else:
                    #Nliv=[]
                    Nliv=0
                    
                Nsar = sar.shape[0]
                S = lia
                ascending_az_angle=int(ascending_az_angle)

                if descending_az_angle:
                    descending_az_angle = float(descending_az_angle) 
                else:
                    descending_az_angle = float('NaN')
                    
                az_angle = np.deg2rad([ascending_az_angle, descending_az_angle])
                over = 0
                if over:
                    if Nsar == 2:
                        viste = np.isnan(sar)
                        if (viste[0] + viste[1]) == 0:
                            
                            sigmae = sigmae/2
                            sigman = sigman/2
                            sigmau = sigmau/2
                    if (viste[0] + viste[1]) == 1:
                        Nsar = 1
                        sarn = Sn = Wn = az_anglen = []
                        if viste[0] == 0:
                            sarn = sar[0]
                            Sn = S[0, :]
                            Wn = W[0]
                            az_anglen = az_angle[0]
                            sar = sarn
                            S = Sn
                            W = Wn
                            az_angle = az_anglen
                        if viste[1] == 0:
                            sarn = sar[1]
                            Sn = S[1, :]
                            Wn = W[1]
                            az_anglen = az_angle[1]
                            sar = sarn
                            S = Sn
                            W = Wn
                            az_angle = az_anglen

                '''
                The code defines a series of matrices that will be used in a subsequent step to calculate deformations.
                The matrices are built based on input data such as GPS measurements, Lia measurements, and SAR measurements.
                
                First, the Agps matrix is created with dimensions (3 * Ngps x 12), where Ngps is the number of GPS measurements.
                For each GPS measurement, a 3 x 12 submatrix is created using values from the gps array (gps[i, 0], gps[i, 1], gps[i, 2]).
                These submatrices are concatenated to create the complete Agps matrix.
                
                Similarly, the Aliv matrix is created with dimensions (Nliv x 12), where Nliv is the number of leveling measurements.
                For each measurement, a 1 x 12 submatrix is created using values from the liv array (liv[i, 0], liv[i, 1], liv[i, 2]).
                These submatrices are concatenated to create the complete Aliv matrix.
                
                The Apix1 matrix is created by repeating the temp matrix (with dimensions 3 x 12).
                The temp matrix is constructed based on the initial position estimate (pos[0,0], pos[1,0], pos[2,0]).
                
                The Apix2 matrix is created by repeating the temp matrix (with dimensions 1 x 12).
                The temp matrix is constructed based on the initial position estimate (pos[0,0], pos[1,0], pos[2,0]).
                
                These two 'temp' matrices are temporary matrices.
                
                The Asar matrix is created with dimensions (Nsar x 12), where Nsar is the number of SAR measurements.
                The Snew matrix is created based on the SAR measurements and the azimuth angle for each SAR measurement.
                The Asar matrix is constructed based on the Snew matrix and contains zeros in the last 9 columns.
                
                Finally, the A matrix is created by concatenating the matrices Agps - Apix1, Aliv - Apix2, and Asar.
                The dimensions of A are (3 * Ngps + Nliv + Nsar) x 12.
                '''
                Agps = np.zeros((3*Ngps, 12)) # (3*Ngps x 12)
                for i in range(Ngps):
                    Agps[3*i:3*(i+1),:] = np.array([[1, 0, 0, gps[i,0], gps[i,1], gps[i,2], 0, 0, 0, 0, gps[i,2], -gps[i,1]],
                                                [0, 1, 0, 0, gps[i,0], 0, gps[i,1], gps[i,2], 0, -gps[i,2], 0, gps[i,0]],
                                                [0, 0, 1, 0, 0, gps[i,0], 0, gps[i,1], gps[i,2], gps[i,1], -gps[i,0], 0]])

                Aliv = np.zeros((Nliv, 12)) # (Nliv x 12)
                for i in range(Nliv):
                    Aliv[i,:] = np.array([0, 0, 1, 0, 0, liv[i,0], 0, liv[i,1], liv[i,2], liv[i,1], -liv[i,0], 0])

                temp = np.array([[0, 0, 0, pos[0,0], pos[1,0], pos[2,0], 0, 0, 0, 0, pos[2,0], -pos[1,0]],
                                [0, 0, 0, 0, pos[0,0], 0, pos[1,0], pos[2,0], 0, -pos[2,0], 0, pos[0,0]],
                                [0, 0, 0, 0, 0, pos[0,0], 0, pos[1,0], pos[2,0], pos[1,0], -pos[0,0], 0]]) # (3 x 12)

                Apix1 = np.tile(temp, (Ngps,1)) # (3*Ngps x 12)
                

                temp = np.array([[0, 0, 0, 0, 0, pos[0,0], 0, pos[1,0], pos[2,0], pos[1,0], -pos[0,0], 0]]) # (1 x 12)

                Apix2 = np.tile(temp, (Nliv,1)) # (Nliv x 12)

                Snew = np.zeros((Nsar, 3))
                for i in range(Nsar):
                    if np.isnan(S[i]):
                        Snew[i,:] = [0, 0, 0]
                    else:
                        Snew[i,:] = [np.cos(az_angle[i])*np.sin(S[i]), np.sin(az_angle[i])*np.sin(S[i]), np.cos(S[i])]


                Asar = np.hstack((Snew, np.zeros((Nsar, 9)))) # (Nsar x 12)

                #A = np.vstack((np.hstack((Agps, -Apix1)), np.hstack((Aliv, -Apix2)), Asar)) # ((3*Ngps + Nliv + Nsar) x 12)
                A = np.concatenate((Agps - Apix1, Aliv - Apix2, Asar))

                # TERMINE NOTO
                '''
                In this part, two arrays bgps and bliv are defined that concatenate information from GPS and leveling sources respectively.
                These arrays will be used to store observations for each measurement.
                The bsar array stores observations from the SAR source.
                Then, the code concatenates all these arrays along the first axis (rows) to form a single array b
                that contains all observations.
                
                Subsequently, the code calculates the weights wgps, wliv, and wsar that will be used to weigh the A and b matrices.
                
                For wgps, the code loops over all GPS observations and calculates the dgps distances
                between each GPS station and the point of interest.
                For each component of the GPS measurement (East, North, Up), the code calculates a weight based on the Gaussian function,
                which models the measurement error.
                The weight is inversely proportional to the measurement error (given by the standard deviations sigmae, sigman, and sigmau)
                and proportional to the inverse of the square of the measurement precision (given by the precisions gps[i,6], gps[i,7], and gps[i,8]).
                
                For wliv, the code loops over all liv observations and calculates the dliv distances between each liv data and the point of interest.
                
                For wsar, the code calculates a single weight based on a Gaussian function with a standard deviation sigma_sar
                that models the measurement error.
                
                Finally, the code concatenates all the weights along the first axis (rows) to form a single array w that contains all the weights.
                '''
                if Ngps:
                    bgps = np.reshape(gps[:,3:6], (3*Ngps, 1))
                else:
                    bgps = np.array([], ndmin=2)
                
                if Nliv:
                    bliv = liv[:,3][:, np.newaxis]
                else:
                    bliv = np.empty((0, bgps.shape[1]), dtype=bgps.dtype)
                
                bsar = sar[:, np.newaxis]
                b = np.concatenate((bgps, bliv, bsar), axis=0)


                # weights

                wgps = np.zeros((3*Ngps,1)) # (3*Ngps x 1)
                for i in range(Ngps+1):
                    transpose=gps[i-1,0:3].T
                    interno_norma=transpose-pos
                    diagonale_interno_norma=np.diag(interno_norma)
                    dgps = np.linalg.norm(diagonale_interno_norma) # distanza tra stazione GPS e pixel
                    dgpsqn = 1 # removed dgpsqn calculation
                    k = 2
                    wgps[3*i-3] = np.exp(-dgps/(sigmae*dgpsqn))/(k*(gps[i-1,5])**2)
                    wgps[3*i-2] = np.exp(-dgps/(sigman*dgpsqn))/(k*(gps[i-1,6])**2)    
                    wgps[3*i-1]   = np.exp(-dgps/(sigmau*dgpsqn))/(k*(gps[i-1,7])**2)


                    
                wliv = np.empty((Nliv,1)) # (Nliv x 1)
                for i in range(Nliv):
                    dliv = np.linalg.norm(liv[i,:3].T - pos) # distanza tra stazione liv e pixel
                    wliv[i] = np.exp(-dliv/sigmal)/(2*sigma_liv**2)
                
                wsar = W/(2*sigma_sar**2) # (Nsar x 1)

                w = np.concatenate((wgps, wliv, wsar)) # matrice dei pesi
                
                '''
                In this part of the code, an attempt is made to solve a linear least squares problem by finding its solution x.
                The problem to be solved is defined as:
                
                A * x = b
                
                where A is a design matrix, and x and b are vectors.
                The goal is to find a solution x that minimizes the residuals || A * x - b ||.
                Thus:
                First, it calculates the weighted least squares solution x of the equation Aw = bw.T using np.linalg.lstsq,
                where Aw and bw are the weighted versions of A and b.
                w is a diagonal weighting matrix.
                The function returns the solution x, the residuals, the rank of the Aw matrix, and the singular values of Aw in x, residuals, rank, s.
                
                Then it calculates the standard deviation stdx of x.
                First, it calculates the variance of x by subtracting the mean of x from each element of x,
                squaring the result, dividing the sum of the squares by 11 (n-1), and then extracting the square root.
                The standard error is then calculated by dividing the variance by the square root of the number of samples.
                
                The first three elements of x are assigned to u.
                The next six elements of x are used to form a 3x3 matrix e and another 3x3 matrix o.
                
                The values of u, e, o, and stdx are stored in the arrays U, E, O, and STDX at the indices ii and jj.
                
                The indices ii and jj are incremented until the end of the loop.
                '''


                def lscov(A, B, w):
                    # Verifica che A abbia rango completo
                    if np.linalg.matrix_rank(A) < min(A.shape):
                        raise ValueError("The matrix A must have complete rank.")
                
                    # Verifica che i pesi siano positivi
                    if np.any(w <= 0):
                        raise ValueError("The weights must be positive real numbers.")
                
                    # Creation of the diagonal weight matrix
                    W = np.sqrt(np.diag(np.array(w).flatten()))

                    AW = A.T @ W
                    x = np.linalg.solve(AW @ A, AW @ B)
                
                    # Calculation of standard error and mean square error (MSE)
                    residuals = B - A @ x
                    mse = (residuals.T @ W @ residuals) / (A.shape[0] - A.shape[1])
                    S = np.linalg.inv(AW @ A) * mse
                    stdx = np.sqrt(np.diag(S))
                
                    return x, stdx, mse
                

                x, stdx, mse = lscov(A, b, w)
                x = np.squeeze(x)
                u = np.array(x[:3])
                e = np.array([[x[3], x[4], x[5]], 
                              [x[4], x[6], x[7]], 
                              [x[5], x[7], x[8]]])
                o = np.array([[0, -x[11], x[10]],
                              [x[11], 0, -x[9]],
                              [-x[10], x[9], 0]])
                
                u = np.squeeze(u)

                stdx = np.squeeze(stdx)
                
                

                u = np.squeeze(u)
                x=np.squeeze(x)
                stdx=np.squeeze(stdx)
                
                
                
                U[:,ii,jj] = u
                E[:,:,ii,jj] = e
                O[:,:,ii,jj] = o
                STDX[:,ii,jj] = stdx #stdx

                ii+=1
            jj+=1

        fin_pix.destroy()  
        progress.destroy()
        label1.destroy()
        label2.destroy()
        

        ############################################################################################ PART 3
        '''
        The variables Ue, Un, and Uu store the displacement maps for east, north, and up, respectively.
        The variables ErrUe, ErrUn, and ErrUu store the error maps for east, north, and up, respectively.
        
        Then, the code calculates and stores the components of the strain tensor in the variables e11, e12, ..., e33.
        The components of the orthogonal tensor are stored in the variables O11, O12, ..., O33.
        
        Finally, the code rounds the GPS positions so that they match the dimensions of the grid and concatenates
        the longitude and latitude values into a single matrix.
        The code then plots the displacement maps using imshow.
        The GPS positions are overlaid on the displacement maps as black stars.
        '''
        Nr = U.shape[1]
        Nc = U.shape[2]

        Ue = np.reshape(U[0,:,:],(Nr,Nc)) # mappa spostamento EAST (Nr x Nc)
        Un = np.reshape(U[1,:,:],(Nr,Nc)) # mappa spostamento NORTH (Nr x Nc)
        Uu = np.reshape(U[2,:,:],(Nr,Nc)) # mappa spostamento UP (Nr x Nc)

        # Construct the full file paths
        file_path_1 = os.path.join(folder_path, "West_East Displacement.asc")
        file_path_2 = os.path.join(folder_path, "North_South Displacement.asc")
        file_path_3 = os.path.join(folder_path, "Vertical Displacement.asc")

        header_lines = []
        header_lines.append(f"ncols {Nc}")
        header_lines.append(f"nrows {Nr}")
        header_lines.append(f"xllcorner {xllcorner}")
        header_lines.append(f"yllcorner {yllcorner}")
        header_lines.append(f"cellsize {cellsize*step}")
        header_lines.append(f"NODATA_value {nodata_value}")

        np.savetxt(file_path_1, Ue, fmt="%.6f", delimiter=" ", header="\n".join(header_lines), comments="")
        np.savetxt(file_path_2, Un, fmt="%.6f", delimiter=" ", header="\n".join(header_lines), comments="")
        np.savetxt(file_path_3, Uu, fmt="%.6f", delimiter=" ", header="\n".join(header_lines), comments="")



        ErrUe = np.reshape(STDX[0,:,:],(Nr,Nc)) # error map EAST (Nr x Nc)
        ErrUn = np.reshape(STDX[1,:,:],(Nr,Nc)) # error map NORTH (Nr x Nc)
        ErrUu = np.reshape(STDX[2,:,:],(Nr,Nc)) # error map UP (Nr x Nc)

        # Construct the full file paths
        file_path_1 = os.path.join(folder_path, "ERROR_West_East Displacement.asc")
        file_path_2 = os.path.join(folder_path, "ERROR_North_South Displacement.asc")
        file_path_3 = os.path.join(folder_path, "ERROR_Vertical Displacement.asc")

        header_lines = []
        header_lines.append(f"ncols {Nc}")
        header_lines.append(f"nrows {Nr}")
        header_lines.append(f"xllcorner {xllcorner}")
        header_lines.append(f"yllcorner {yllcorner}")
        header_lines.append(f"cellsize {cellsize*step}")
        header_lines.append(f"NODATA_value {nodata_value}")

        np.savetxt(file_path_1, ErrUe, fmt="%.6f", delimiter=" ", header="\n".join(header_lines), comments="")
        np.savetxt(file_path_2, ErrUn, fmt="%.6f", delimiter=" ", header="\n".join(header_lines), comments="")
        np.savetxt(file_path_3, ErrUu, fmt="%.6f", delimiter=" ", header="\n".join(header_lines), comments="")
        #strain

        e11 = np.reshape(E[0,0,:,:],(Nr,Nc));
        e12 = np.reshape(E[0,1,:,:],(Nr,Nc))
        e13 = np.reshape(E[0,2,:,:],(Nr,Nc))
        e21 = np.reshape(E[1,0,:,:],(Nr,Nc))
        e22 = np.reshape(E[1,1,:,:],(Nr,Nc))
        e23 = np.reshape(E[1,2,:,:],(Nr,Nc))
        e31 = np.reshape(E[2,0,:,:],(Nr,Nc))
        e32 = np.reshape(E[2,1,:,:],(Nr,Nc))
        e33 = np.reshape(E[2,2,:,:],(Nr,Nc))

        O11 = np.reshape(O[0,0,:,:],(Nr,Nc))
        O12 = np.reshape(O[0,1,:,:],(Nr,Nc))
        O13 = np.reshape(O[0,2,:,:],(Nr,Nc))
        O21 = np.reshape(O[1,0,:,:],(Nr,Nc))
        O22 = np.reshape(O[1,1,:,:],(Nr,Nc))
        O23 = np.reshape(O[1,2,:,:],(Nr,Nc))
        O31 = np.reshape(O[2,0,:,:],(Nr,Nc))
        O32 = np.reshape(O[2,1,:,:],(Nr,Nc))
        O33 = np.reshape(O[2,2,:,:],(Nr,Nc)) 


        gpsn = np.round((( gps[:,0]-minEast ) / (cellsize))/step)
        gpsn = gpsn[:, np.newaxis]
        new_col = np.round((( maxNorth -gps[:,1]) /  (cellsize))/step)
        new_col = new_col[:, np.newaxis]
        gpsn = np.concatenate((gpsn, new_col), axis=1)


        # plot the subplots
        fig, axs = plt.subplots(3, 2, figsize=(15, 12))

        # Subplot 1: West-East Displacement (Ue) and its Error (ErrUe)
        im = axs[0, 0].imshow(Ue, cmap='jet')
        colorbar = plt.colorbar(im, ax=axs[0, 0])
        colorbar.set_label('Displacement (meters)')
        axs[0, 0].set_title('West-East Displacement')
        axs[0, 0].scatter(gpsn[:, 0], gpsn[:, 1], c='k', marker='*')

        im4 = axs[0, 1].imshow(ErrUe, cmap='jet')
        colorbar4 = plt.colorbar(im4, ax=axs[0, 1])
        colorbar4.set_label('Displacement (meters)')
        axs[0, 1].set_title('W-E Displacement Error')
        axs[0, 1].scatter(gpsn[:, 0], gpsn[:, 1], c='k', marker='*')

        # Subplot 2: North-South Displacement (Un) and its Error (ErrUn)
        im2 = axs[1, 0].imshow(Un, cmap='jet')
        colorbar2 = plt.colorbar(im2, ax=axs[1, 0])
        colorbar2.set_label('Displacement (meters)')
        axs[1, 0].set_title('North-South Displacement')
        axs[1, 0].scatter(gpsn[:, 0], gpsn[:, 1], c='k', marker='*')

        im5 = axs[1, 1].imshow(ErrUn, cmap='jet')
        colorbar5 = plt.colorbar(im5, ax=axs[1, 1])
        colorbar5.set_label('Displacement (meters)')
        axs[1, 1].set_title('N-S Displacement Error')
        axs[1, 1].scatter(gpsn[:, 0], gpsn[:, 1], c='k', marker='*')

        # Subplot 3: Vertical Displacement (Uu) and its Error (ErrUu)
        im3 = axs[2, 0].imshow(Uu, cmap='jet')
        colorbar3 = plt.colorbar(im3, ax=axs[2, 0])
        colorbar3.set_label('Displacement (meters)')
        axs[2, 0].set_title('Vertical Displacement')
        axs[2, 0].scatter(gpsn[:, 0], gpsn[:, 1], c='k', marker='*')

        im6 = axs[2, 1].imshow(ErrUu, cmap='jet')
        colorbar6 = plt.colorbar(im6, ax=axs[2, 1])
        colorbar6.set_label('Displacement (meters)')
        axs[2, 1].set_title('Vertical Displacement Error')
        axs[2, 1].scatter(gpsn[:, 0], gpsn[:, 1], c='k', marker='*')

        # Adjust layout and save the plot
        plt.tight_layout()
        plot_path = os.path.join(folder_path, "DISPLACEMENTS.png")
        plt.savefig(plot_path)
        plt.show()
   
        plt.close()




        ###################################################################################################### PART 4
        '''
        In the for loop in this part of the function, initially the number of columns and rows are iterated
        '''

        colonner = Nc
        righer = Nr
        mat = np.zeros((righer, colonner), dtype=[('strain', np.float64, (3,3)), ('rotation', np.float64, (3,3))])
        M = np.zeros((righer, colonner))
        SR = np.zeros((righer, colonner))
        AD = np.zeros((righer, colonner))
        VD = np.zeros((righer, colonner))
        e1 = np.zeros((righer, colonner))
        e2 = np.zeros((righer, colonner))
        e3 = np.zeros((righer, colonner))
        phi = np.zeros((righer, colonner))


        jj = 0
        jjs = 0
        for a in range(colonner):
            ii = 0
            iis = 0
            for b in range(righer):
                if SAR.shape[0] == 1:
                    check_nan = np.isnan(SAR[0, iis, jjs])
                else:
                    check_nan = np.isnan(SAR[0, iis, jjs]) and np.isnan(SAR[1, iis, jjs])
        
                if not check_nan:
                    mat[ii][jj]['strain'] = [[e11[ii][jj], e12[ii][jj], e13[ii][jj]],
                                             [e21[ii][jj], e22[ii][jj], e23[ii][jj]],
                                             [e31[ii][jj], e32[ii][jj], e33[ii][jj]]]
                    mat[ii][jj]['rotation'] = [[O11[ii][jj], O12[ii][jj], O13[ii][jj]],
                                               [O21[ii][jj], O22[ii][jj], O23[ii][jj]],
                                               [O31[ii][jj], O32[ii][jj], O33[ii][jj]]]
        
                    if not (np.isnan(mat['strain'][ii, jj]).any() or np.isinf(mat['strain'][ii, jj]).any()):
                        P = np.linalg.eig(mat['strain'][ii, jj])[0]
                        D = np.sort(P)
        
                        M[ii, jj] = (D[2] - D[0]) * 1000000
                        SR[ii, jj] = (((e11[ii, jj] ** 2) + (e22[ii, jj] ** 2) + 2 * (e12[ii, jj] ** 2)) ** 0.5) * 1000000
                        AD[ii, jj] = (e11[ii, jj] + e22[ii, jj]) * 1000000
                        VD[ii, jj] = (e11[ii, jj] + e22[ii, jj] + e33[ii, jj]) * 1000000
                        phi[ii, jj] = ((3 / 4) + (1 / np.pi) * np.arctan(e22[ii, jj] / e11[ii, jj]))
                    else:
                        M[ii, jj] = np.nan
                        SR[ii, jj] = np.nan
                        AD[ii, jj] = np.nan
                        VD[ii, jj] = np.nan
                else:
                    M[ii, jj] = np.nan
                    SR[ii, jj] = np.nan
                    AD[ii, jj] = np.nan
                    VD[ii, jj] = np.nan
        
                ii += 1
                iis += step
            jj += 1
            jjs += step

        

        # Construct the full file paths
        file_path_1 = os.path.join(folder_path, "2D Area Dilation.asc")
        file_path_2 = os.path.join(folder_path, "Volumetric Dilation.asc")
        file_path_3 = os.path.join(folder_path, "Total Strain Rate 2D.asc")
        file_path_4 = os.path.join(folder_path, "Maximum Shear Strain.asc")

        header_lines = []
        header_lines.append(f"ncols {Nc}")
        header_lines.append(f"nrows {Nr}")
        header_lines.append(f"xllcorner {xllcorner}")
        header_lines.append(f"yllcorner {yllcorner}")
        header_lines.append(f"cellsize {cellsize*step}")
        header_lines.append(f"NODATA_value {nodata_value}")

        np.savetxt(file_path_1, AD, fmt="%.6f", delimiter=" ", header="\n".join(header_lines), comments="")
        np.savetxt(file_path_2, VD, fmt="%.6f", delimiter=" ", header="\n".join(header_lines), comments="")
        np.savetxt(file_path_3, SR, fmt="%.6f", delimiter=" ", header="\n".join(header_lines), comments="")
        np.savetxt(file_path_4, M, fmt="%.6f", delimiter=" ", header="\n".join(header_lines), comments="")



        fig,ax=plt.subplots(2,2,figsize=(10, 8))   

        im1=ax[0,0].imshow(AD,cmap='jet')
        ax[0,0].set_title('2D Area Dilation')   
        colorbar1=plt.colorbar(im1, ax=ax[0,0]) 
        colorbar1.set_label('microstrain (µε)')
        im2=ax[0,1].imshow(VD,cmap='jet')
        ax[0,1].set_title('Volumetric Dilation')
        colorbar2=plt.colorbar(im2, ax=ax[0,1]) 
        colorbar2.set_label('microstrain (µε)')
        im3=ax[1,0].imshow(SR,cmap='jet')
        ax[1,0].set_title('2D Total Strain Rate') 
        colorbar3=plt.colorbar(im3, ax=ax[1,0])  
        colorbar3.set_label('microstrain (µε)')
        im4=ax[1,1].imshow(M,cmap='jet')
        ax[1,1].set_title('Maximum Shear Strain')
        colorbar4=plt.colorbar(im4, ax=ax[1,1])
        colorbar4.set_label('microstrain (µε)')   

        plot_path = os.path.join(folder_path, "STRAINS.png")
        plt.savefig(plot_path)

        plt.show()    
        
        def convert_asc_to_jpeg(asc_file, output_path):
            # Load data from .asc file, skipping the first 6 rows
            data = np.loadtxt(asc_file, skiprows=6)

            # Extract the file name without the extension
            file_name = os.path.splitext(os.path.basename(asc_file))[0]

            # Create a figure and axes
            fig, ax = plt.subplots()

            # Set the colormap to "jet"
            cmap = plt.get_cmap('jet')

            # Create the plot using imshow
            img = ax.imshow(data, cmap=cmap)

            # Set the title using the file name
            ax.set_title(file_name)
            
            # Add a colorbar
            cbar = fig.colorbar(img, ax=ax)

            # Save the plot as a JPEG image
            plt.savefig(output_path, format='jpeg')

            # Close the figure
            plt.close(fig)

        output_folder=folder_path
        # Loop through the .asc files in the folder
        for filename in os.listdir(folder_path):
            if filename.endswith(".asc"):
                asc_file_path = os.path.join(folder_path, filename)

                # Generate the output JPEG file name by replacing the file extension
                output_filename = os.path.splitext(filename)[0] + ".jpeg"

                # Path to save the output JPEG file
                output_file_path = os.path.join(output_folder, output_filename)

                # Convert .asc to .jpeg
                convert_asc_to_jpeg(asc_file_path, output_file_path)
            
        ###


    def validate_number(value):
        if value == "." or value == "-":
            return True
        if value.replace(".", "", 1).replace("-", "", 1).isdigit() or value == "":
            return True
        return False


    # Create labels and entry fields for each input
    dem_label = customtkinter.CTkLabel(center_frame, text="DEM:")
    dem_label.grid(row=0, column=0, sticky="w")
    dem_entry = customtkinter.CTkEntry(center_frame,width=170)
    dem_entry.grid(row=0, column=1, padx=5, pady=5)
    dem_button = customtkinter.CTkButton(center_frame, text="Select..", fg_color="magenta",width=70,command=lambda: browse_file(dem_entry))
    dem_button.grid(row=0, column=2, padx=5, pady=5)

    step_label = customtkinter.CTkLabel(center_frame, text="STEPS:")
    step_label.grid(row=1, column=0, sticky="w")
    step_entry = customtkinter.CTkEntry(center_frame,width=170)
    step_entry.grid(row=1, column=1, padx=5, pady=5)

    gps_label = customtkinter.CTkLabel(center_frame, text="GPS DATA:")
    gps_label.grid(row=2, column=0, sticky="w")
    gps_entry = customtkinter.CTkEntry(center_frame,width=170)
    gps_entry.grid(row=2, column=1, padx=5, pady=5)
    gps_button = customtkinter.CTkButton(center_frame, text="Select..", fg_color="magenta",width=70,command=lambda: browse_file(gps_entry))
    gps_button.grid(row=2, column=2, padx=5, pady=5)

    sar1_label = customtkinter.CTkLabel(center_frame, text="FIRST SAR:")
    sar1_label.grid(row=3, column=0, sticky="w")
    sar1_entry = customtkinter.CTkEntry(center_frame,width=170)
    sar1_entry.grid(row=3, column=1, padx=5, pady=5)
    sar1_button = customtkinter.CTkButton(center_frame, text="Select..", fg_color="magenta",width=70,command=lambda: browse_file(sar1_entry))
    sar1_button.grid(row=3, column=2, padx=5, pady=5)

    lia1_label = customtkinter.CTkLabel(center_frame, text="FIRST LIA:")
    lia1_label.grid(row=4, column=0, sticky="w")
    lia1_entry = customtkinter.CTkEntry(center_frame,width=170)
    lia1_entry.grid(row=4, column=1, padx=5, pady=5)
    lia1_button = customtkinter.CTkButton(center_frame, text="Select..", fg_color="magenta",width=70,command=lambda: browse_file(lia1_entry))
    lia1_button.grid(row=4, column=2, padx=5, pady=5)

    asc_az_label = customtkinter.CTkLabel(center_frame, text="First Azimuth Angle (degrees):")
    asc_az_label.grid(row=5, column=0, sticky="w")
    asc_az_entry = customtkinter.CTkEntry(center_frame,width=170)
    asc_az_entry.grid(row=5, column=1, padx=5, pady=5)

    inc_ang_label = customtkinter.CTkLabel(center_frame, text="First Inclination Angle (degrees):")
    inc_ang_label.grid(row=6, column=0, sticky="w")
    inc_ang_entry = customtkinter.CTkEntry(center_frame,width=170)
    inc_ang_entry.grid(row=6, column=1, padx=5, pady=5)

    sar2_label = customtkinter.CTkLabel(center_frame, text="SECOND SAR:")
    sar2_label.grid(row=7, column=0, sticky="w")
    sar2_entry = customtkinter.CTkEntry(center_frame,width=170)
    sar2_entry.grid(row=7, column=1, padx=5, pady=5)
    sar2_button = customtkinter.CTkButton(center_frame, text="Select..", fg_color="magenta",width=70,command=lambda: browse_file(sar2_entry))
    sar2_button.grid(row=7, column=2, padx=5, pady=5)

    lia2_label = customtkinter.CTkLabel(center_frame, text="SECOND LIA:")
    lia2_label.grid(row=8, column=0, sticky="w")
    lia2_entry = customtkinter.CTkEntry(center_frame,width=170)
    lia2_entry.grid(row=8, column=1, padx=5, pady=5)
    lia2_button = customtkinter.CTkButton(center_frame, text="Select..", fg_color="magenta",width=70, command=lambda: browse_file(lia2_entry))
    lia2_button.grid(row=8, column=2, padx=5, pady=5)

    desc_az_label = customtkinter.CTkLabel(center_frame, text="Second Azimuth Angle (deg):")
    desc_az_label.grid(row=9, column=0, sticky="w")
    desc_az_entry = customtkinter.CTkEntry(center_frame,width=170)
    desc_az_entry.grid(row=9, column=1, padx=5, pady=5)

    inc_ang2_label = customtkinter.CTkLabel(center_frame, text="Second Inclination Angle (deg):")
    inc_ang2_label.grid(row=10, column=0, sticky="w")
    inc_ang2_entry = customtkinter.CTkEntry(center_frame,width=170)
    inc_ang2_entry.grid(row=10, column=1, padx=5, pady=5)

    sigma_sar_label = customtkinter.CTkLabel(center_frame, text="sigma SAR (m):")
    sigma_sar_label.grid(row=11, column=0, sticky="w")
    sigma_sar_entry = customtkinter.CTkEntry(center_frame,width=170)
    sigma_sar_entry.grid(row=11, column=1, padx=5, pady=5)

    sigmal_label = customtkinter.CTkLabel(center_frame, text="locality LEV (m):")
    sigmal_label.grid(row=12, column=0, sticky="w")
    sigmal_entry = customtkinter.CTkEntry(center_frame,width=170)
    sigmal_entry.grid(row=12, column=1, padx=5, pady=5)

    liv_label = customtkinter.CTkLabel(center_frame, text="LEVELLING DATA:")
    liv_label.grid(row=13, column=0, sticky="w")
    liv_entry = customtkinter.CTkEntry(center_frame,width=170)
    liv_entry.grid(row=13, column=1, padx=5, pady=5)
    liv_button = customtkinter.CTkButton(center_frame, text="Select..", fg_color="magenta",width=70,command=lambda: browse_file(liv_entry))
    liv_button.grid(row=13, column=2, padx=5, pady=5)

    sigma_liv_label = customtkinter.CTkLabel(center_frame, text="sigma LEVELLING:")
    sigma_liv_label.grid(row=14, column=0, sticky="w")
    sigma_liv_entry = customtkinter.CTkEntry(center_frame,width=170)
    sigma_liv_entry.grid(row=14, column=1, padx=5, pady=5)

    k_label = customtkinter.CTkLabel(center_frame, text="K LOCALITY VALUE:")
    k_label.grid(row=15, column=0, sticky="w")
    k_entry = customtkinter.CTkEntry(center_frame,width=170)
    k_entry.grid(row=15, column=1, padx=5, pady=5)
    k_entry.insert(0, "9")

    loc_label = customtkinter.CTkLabel(center_frame, text="LOCALITY DENOMINATOR:")
    loc_label.grid(row=16, column=0, sticky="w")
    loc_entry = customtkinter.CTkEntry(center_frame,width=170)
    loc_entry.grid(row=16, column=1, padx=5, pady=5)
    loc_entry.insert(0, "2")



    # Set the validation for numbers only
    validate_cmd = (root.register(validate_number), '%P')
    asc_az_entry.configure(validate='key', validatecommand=validate_cmd)
    step_entry.configure(validate='key', validatecommand=validate_cmd)
    inc_ang_entry.configure(validate='key', validatecommand=validate_cmd)
    inc_ang2_entry.configure(validate='key', validatecommand=validate_cmd)
    loc_entry.configure(validate='key', validatecommand=validate_cmd)
    k_entry.configure(validate='key', validatecommand=validate_cmd)
    sigma_liv_entry.configure(validate='key', validatecommand=validate_cmd)
    desc_az_entry.configure(validate='key', validatecommand=validate_cmd)
    sigmal_entry.configure(validate='key', validatecommand=validate_cmd)
    sigma_sar_entry.configure(validate='key', validatecommand=validate_cmd)



    # Create a button to save the values
    save_button = customtkinter.CTkButton(center_frame, text="Insert Data", fg_color="green",command=save_values)
    save_button.grid(row=17, column=0, columnspan=3, pady=10)


left_button_general = customtkinter.CTkButton(left_frame, text="General", command=display_buttons)
left_button_general.pack(pady=10)
left_button_elaboration = customtkinter.CTkButton(left_frame, text="Spatial Analysis", command=display_buttons_elaboration)
left_button_elaboration.pack(pady=10)
left_button_Visualization = customtkinter.CTkButton(left_frame, text="Visualization", command=display_buttons_visualization)
left_button_Visualization.pack(pady=10)
left_button_synthetic = customtkinter.CTkButton(left_frame, text="Generate Synthetic Data", command=display_buttons_synthetic_model)
left_button_synthetic.pack(pady=10)

left_button_sistem = customtkinter.CTkButton(left_frame, text="SISTEM" , fg_color='Purple',command=RUN_SISTEM)
left_button_sistem.pack(pady=10)

clear_button = customtkinter.CTkButton(left_frame, text="Clear Workspace", fg_color='red', command=clear_all)
clear_button.pack(pady=10)

clear2_button = customtkinter.CTkButton(left_frame, text="Clear Terminal", fg_color='red', command=clear_terminal)
clear2_button.pack(pady=10)

clear3_button = customtkinter.CTkButton(left_frame, text="Clear Tools", fg_color='red', command=clear_all_2)
clear3_button.pack(pady=10)
# Create a button to change the mode
mode_switch = customtkinter.CTkSwitch(left_frame, text="Dark/Light Theme", command=change_mode)
mode_switch.pack(pady=10)


# Start the main event loop
root.mainloop()

