# Paint App in Python

from tkinter import *
from tkinter import colorchooser,filedialog,messagebox
from PIL import ImageGrab,ImageTk,Image

import tkinter.ttk as ttk
import os

root = Tk()
root.title("Paint App")
root.iconbitmap("icon.ico")
root.geometry("1000x700")

# Brush Color
brush_color = "black"

# Saved = False
saved = False

# Change Color
def change_color(color):
    global brush_color
    brush_color = color

# Change the size of the brush
def change_brush_size(e):
    brush_slider_label.config(text=str(int(brush_slider.get())))

# Draw on the canvas
def draw(e):
    # e is to do something

    # Brush Parameters
    brush_width = int(brush_slider.get())

    # Brush Types: BUTT, ROUND, PROJECTING
    brush_type = brush_style_type.get()

    # Starting Position
    x1 = e.x - 1
    y1 = e.y - 1

    # Ending Position
    x2 = e.x + 1
    y2 = e.y + 1

    # Draw The Line
    canvas.create_line(x1,y1,x2,y2,fill=brush_color,smooth=True,width=brush_width,capstyle=brush_type)

# Change Brush Color
def change_brush_color(something_about_which_I_dont_care=None):
    global brush_color
    brush_color = "black"
    brush_color = colorchooser.askcolor(color=brush_color)[1]

# Change Canvas Color
def change_canvas_color():
    global canvas_background_color
    canvas_background_color = "black"
    canvas_background_color = colorchooser.askcolor(color=canvas_background_color)[1]

    canvas.config(bg=canvas_background_color)

# Clear Canvas
def clear_canvas(extra_thing_about_which_nobody_cares=None):
    canvas.config(bg="white")
    canvas.delete(ALL)

# Save image to PNG
def save_to_png(extra_thing_about_which_nobody_cares=None):
    
    file_path = filedialog.asksaveasfilename(initialdir=os.curdir,filetypes=(
        ("PNG Files","*.png"),
        ("All Files","*.*"),
    ))

    if not file_path.endswith(".png"):
        file_path += ".png"

    if file_path:
        x=(root.winfo_rootx()*1.25+canvas.winfo_x()*1.25)
        y=(root.winfo_rooty()*1.25+canvas.winfo_y()*1.25)
        x1=x+canvas.winfo_width()*1.25
        y1=y+canvas.winfo_height()*1.25
        ImageGrab.grab().crop((x,y,x1,y1)).save(file_path)

        # Pop up message box
        messagebox.showinfo("Image Saved!","Your Image has been saved successfully.")

        global saved
        saved = True

# Create New File
def new_file():
    if saved:
        clear_canvas()
    else:
        ok = messagebox.askyesno("File Not Saved!","The file on which you are working is not saved, if you continue all progress will be lost.\nDo you want to continue?")

        if ok:
            clear_canvas()

# Open a file
def open_file():
    global img
    path = filedialog.askopenfilename(filetypes=[("PNG Files","*.png")])
    if path:
        img = ImageTk.PhotoImage(Image.open(path))  
        canvas.create_image(20, 20, anchor=NW, image=img)   

# Help
def about():
    top = Toplevel(root)
    top.geometry("600x300")
    top.iconbitmap("about.ico")
    Label(top,text="Paint App: About",font=('Calibri',18)).pack(anchor=CENTER)
    Label(top,text="This app has been created by Jenil in the udemy course by 'John Elder'.\nI have made this app using Python and Tkinter.",font=("Calbiri",12)).pack()

    global img
    img = ImageTk.PhotoImage(Image.open("python.png"))  
    Label(top,image=img).pack()
    canvas.pack() 

# Key Board Shortcuts
def help_keyboard_shortcuts():
    top = Toplevel(root)
    top.geometry("400x400")
    top.iconbitmap("keyboard.ico")
    Label(top,text="Paint App: Key Board Shortcuts",font=('Calibri',18)).pack(anchor=CENTER)
    Label(top,text="e: Erase\nh: Change Color\nc: Clear Canvas\nShift + R: Chnage Brush Type To Round\nShift + S: Chnage Brush Type To Slash\nShift + D: Chnage Brush Type To Diamond\nCtrl + N: New File\nCtrl + O Open File\nCtrl + S: Save File",font=("Calbiri",14)).pack()

# Eraser
def eraser(blah=None):
    global brush_color
    brush_color = "white"

# Create Menu Bar
menu = Menu(root)
root.config(menu=menu)

# Create a file menu item
file_menu = Menu(menu)
file_menu.add_command(label="New File",command=new_file)
file_menu.add_command(label="Open File",command=open_file)
file_menu.add_command(label="Save",command=save_to_png)
file_menu.add_separator()
file_menu.add_command(label="Exit",command=root.quit)
menu.add_cascade(label="File",menu=file_menu)

# Create a help menu item
help_menu = Menu(menu)
help_menu.add_command(label="About",command=about)
help_menu.add_command(label="Key Board Shrtcuts",command=help_keyboard_shortcuts)
menu.add_cascade(label="Help",menu=help_menu)

# Width and Height
w = 600
h = 400

# Create Canvas
canvas = Canvas(root,width=w,height=h,bg="white")
canvas.bind("<B1-Motion>",draw)
canvas.pack(pady=20)

# Create Brush Options Frames
brush_options_frame = Frame(root)
brush_options_frame.pack(pady=10)

# Brush Size : Brush Options
brush_size_frame = LabelFrame(brush_options_frame,text="Brush Size")
brush_size_frame.grid(row=0,column=0,padx=30)

# Brush Slider
brush_slider = ttk.Scale(brush_size_frame,from_ = 100,to = 1,orient=VERTICAL,value=20,command=change_brush_size)
brush_slider.pack(pady=10,padx=10)

# Brush Slider Labelk
brush_slider_label  = Label(brush_size_frame,text=brush_slider.get())
brush_slider_label.pack()

# Brush Type : Brush Options
brush_type_frame = LabelFrame(brush_options_frame,text="Brush Type")
brush_type_frame.grid(row=0,column=1,padx=30)

# Create Tkinter String Variable to store Brush Type
brush_style_type = StringVar()
brush_style_type.set(ROUND)

# Create Radio Buttons
brush_type_radio_btn_1 = Radiobutton(brush_type_frame,text="Round",variable=brush_style_type,value=ROUND)
brush_type_radio_btn_1.pack(anchor=W)

brush_type_radio_btn_2 = Radiobutton(brush_type_frame,text="Slash",variable=brush_style_type,value=BUTT)
brush_type_radio_btn_2.pack(anchor=W)

brush_type_radio_btn_3 = Radiobutton(brush_type_frame,text="Diamond",variable=brush_style_type,value=PROJECTING)
brush_type_radio_btn_3.pack(anchor=W)

# Change Colors
change_color_frame = LabelFrame(brush_options_frame,text="Change Colors")
change_color_frame.grid(row=0,column=2,padx=30)

# Change Brush Color Button
change_brush_color_btn = Button(change_color_frame,text="Brush Color",command=change_brush_color)
change_brush_color_btn.pack(pady=10,padx=10)

# Change Canvas Color Button
change_canvas_color = Button(change_color_frame,text="Canvas Color",command=change_canvas_color)
change_canvas_color.pack(pady=10,padx=10)

# Program Options Frame
options_frame = LabelFrame(brush_options_frame,text="Options")
options_frame.grid(row=0,column=3,padx=30)

# Clear Button
clear_btn = Button(options_frame,text="Clear Canvas",command=clear_canvas)
clear_btn.pack(padx=10,pady=10)

# Save Button
save_to_png_btn = Button(options_frame,text="Save to PNG",command=save_to_png)
save_to_png_btn.pack(padx=10,pady=10)

# Eraser
eraser_btn = Button(options_frame,text="Eraser Tool",command=eraser)
eraser_btn.pack(padx=10,pady=10)

# Change Colors
pen_colors_frame = LabelFrame(brush_options_frame,text="Pen Colors")
pen_colors_frame.grid(row=0,column=4,padx=30)

# Black
black_color_btn = Button(pen_colors_frame,bg="black",command=lambda: change_color("black"))
black_color_btn.grid(row=0,column=0,padx=5,pady=5)

# White
white_color_btn = Button(pen_colors_frame,bg="white",command=lambda: change_color("white"))
white_color_btn.grid(row=1,column=0,padx=5,pady=5)

# Red
red_color_btn = Button(pen_colors_frame,bg="red",command=lambda: change_color("red"))
red_color_btn.grid(row=0,column=1,padx=5,pady=5)

# Pink
pink_color_btn = Button(pen_colors_frame,bg="Pink",command=lambda: change_color("Pink"))
pink_color_btn.grid(row=1,column=1,padx=5,pady=5)

# Blue
blue_color_btn = Button(pen_colors_frame,bg="blue",command=lambda: change_color("blue"))
blue_color_btn.grid(row=0,column=2,padx=5,pady=5)

# Light Blue
light_blue_color_btn = Button(pen_colors_frame,bg="light blue",command=lambda: change_color("light blue"))
light_blue_color_btn.grid(row=1,column=2,padx=5,pady=5)

# Orange
orange_color_btn = Button(pen_colors_frame,bg="orange",command=lambda: change_color("orange"))
orange_color_btn.grid(row=0,column=5,padx=5,pady=5)

# Yellow
yellow_color_btn = Button(pen_colors_frame,bg="yellow",command=lambda: change_color("yellow"))
yellow_color_btn.grid(row=1,column=5,padx=5,pady=5)

# Green
green_color_btn = Button(pen_colors_frame,bg="green",command=lambda: change_color("green"))
green_color_btn.grid(row=0,column=4,padx=5,pady=5)

# Light green
light_green_color_btn = Button(pen_colors_frame,bg="light green",command=lambda: change_color("light green"))
light_green_color_btn.grid(row=1,column=4,padx=5,pady=5)

# Key Board Shortucts
root.bind("<e>",eraser)
root.bind("<h>",change_brush_color)
root.bind("<c>",clear_canvas)

root.bind("<Shift_L><R>",lambda e: brush_style_type.set(ROUND))
root.bind("<Shift_L><S>",lambda e: brush_style_type.set(BUTT))
root.bind("<Shift_L><D>",lambda e: brush_style_type.set(PROJECTING))

root.bind("<Control_L><s>",lambda e: save_to_png())
root.bind("<Control_L><n>",lambda e: new_file())
root.bind("<Control_L><o>",lambda e: open_file())

root.bind("<F1>",lambda e: about())
root.bind("<F2>",lambda e: help_keyboard_shortcuts())

root.mainloop()

# -Jenil Chudgar
