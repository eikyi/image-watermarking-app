# Importing libraries
import tkinter as tk
from tkinter import Label, messagebox, END
from tkinter.filedialog import askopenfilename
from tkinter.ttk import Entry

from PIL import Image, ImageTk, ImageFont, ImageDraw
FONT = 'fonts/Arial.ttf'
ROTATIONS = ["0","45","90","135"]
img_path = ''
width,height = 900,700
# image uploader function
def image_uploader():
    file_types = [('jpeg files', '*.jpeg'),('png files','*.png'),('jpg files','*.jpg')]
    path = askopenfilename(title="Select An Image",filetypes=file_types)
    global img_path
    img_path = path

    # if file is selected
    if len(path):
        img = Image.open(path)
        img_width, img_height = img.size
        #print(img_width),print(img_height)

        global width,height
        if img_width>width or img_height > height:
            while img_width > width or img_height > height:
                img_width *= 0.99
                img_height *= 0.99

            img = img.resize((int(img_width),int(img_height)))
            messagebox.showinfo(title='Warning',
                                message='The upload image is larger than the canvas. It will ber resized')
        else:
            canvas.config(width=int(img_width), height=int(img_height))
            width= int(img_width)
            height = int(img_height)
        pic = ImageTk.PhotoImage(img)
        canvas.img = pic
        canvas.create_image(width / 2, height / 2, image=pic, anchor=tk.CENTER)

    # if no file is selected, then we are displaying below message
    else:
        print('No file is Choosen !! Please choose a file.')

def add_watermark(image_path):
    font_size = int(watermark_f_size.get())
    tile_selection = int(var.get())
    # get an image
    with Image.open(image_path).convert("RGBA") as base:

        # make a blank image for the text, initialized to transparent text color
        txt = Image.new("RGBA", base.size, (255, 255, 255, 0))

        # get a font
        fnt = ImageFont.truetype(FONT, font_size)

        if logo_path_entry.get():
            try:
                logo = Image.open(logo_path_entry.get())
                logo.thumbnail((int(width/6), int(width/6)))
                logo = logo.convert("RGBA")  # convert to RGBA
                #make the logo transparent
                datas = logo.getdata()
                newData = []
                for item in datas:
                    if item[0] == 0 and item[1] == 0 and item[2] == 0 and item[3] == 255:
                        newData.append((0, 0, 0, 150))
                    else:
                        newData.append(item)

                logo.putdata(newData)
                #rotate the logo
                logo = logo.rotate(int(variable.get()))
                if tile_selection == 1:
                    txt.paste(logo, (50, width - 100))
                else:
                    y = 80
                    for i in range(5):
                        x = 50
                        txt.paste(logo, (x, y))
                        x += 200
                        txt.paste(logo, (x, y))
                        x += 200
                        txt.paste(logo, (x, y))
                        x += 200
                        txt.paste(logo, (x, y))
                        x += 200
                        txt.paste(logo, (x, y))
                        x += 200
                        y += 200

                result = Image.alpha_composite(base, txt)
                if not watermark_entry.get():
                    result.show()
            except FileNotFoundError:
                messagebox.showinfo(title='Invalid Logo Path',
                                    message='The logo path is invalid. Please check and try again Eg: /Users/<username>/Downloads/logo.png')

        if watermark_entry.get():
            # get a drawing context
            d = ImageDraw.Draw(txt)
            if tile_selection == 1:
                d.text((width / 2, height / 2), watermark_entry.get(), font=fnt, fill=(255, 255, 255, 128))
            else:
                #distribute multiple text
                y = 80
                for i in range(8):
                    x = 50
                    # draw text, half opacity
                    d.text((x , y ), watermark_entry.get(), font=fnt, fill=(255, 255, 255, 128))
                    x +=200
                    d.text((x, y), watermark_entry.get(), font=fnt, fill=(255, 255, 255, 128))
                    x += 200
                    d.text((x, y), watermark_entry.get(), font=fnt, fill=(255, 255, 255, 128))
                    x += 200
                    d.text((x, y), watermark_entry.get(), font=fnt, fill=(255, 255, 255, 128))
                    x += 200
                    d.text((x, y), watermark_entry.get(), font=fnt, fill=(255, 255, 255, 128))
                    x += 200
                    y +=120

            txt = txt.rotate(int(variable.get()))
            if logo_path_entry.get():
                out = Image.alpha_composite(result, txt)
            else:
                out = Image.alpha_composite(base, txt)
            out.show()

def sel():
   selection = "You selected the option " + str("")

if __name__ == '__main__':

    # defining tkinter object
    window = tk.Tk()
    window.config(padx=10, pady=10)

    # setting title and basic size to our App
    window.title('Image Watermarking App')
    #window.geometry(f'{WIDTH}x{HEIGHT+100}')

    # adding background color to our upload button
    canvas = tk.Canvas(window, width=width, height=height, background='white')
    #canvas.pack(padx=20,pady=20)
    canvas.grid(column=0, row=0,columnspan=5,padx=5,pady=5)

    # defining our upload buttom
    uploadButton = tk.Button(window, text='Upload', command=image_uploader)
    uploadButton.grid(column=0, row=1)

    #watermark text
    text = Label(text="Watermark Text: ",justify="left")
    text.grid(column=1, row=1)

    # watermark text entry
    watermark_entry = Entry(width=25,justify="left")
    watermark_entry.grid(column=2, row=1)

    #font size label
    f_size_label = Label(text="Font Size:(eg:20): ",justify="left")
    f_size_label.grid(column=3, row=1)

    # font size entry
    watermark_f_size = Entry(width=8,justify="left")
    watermark_f_size.insert(0, '40')
    watermark_f_size.grid(column=4, row=1)

    logo_path_label = Label(text="Logo Path:", justify="left")
    logo_path_label.grid(column=1, row=2)

    logo_path_entry = Entry(width=44, justify="left")
    logo_path_entry.grid(column=2, row=2, columnspan=2)

    single_or_multiple_label = Label(text="Watermark Tile: ")
    single_or_multiple_label.grid(column=1, row=3)

    var = tk.IntVar()
    r_1 = tk.Radiobutton(window, text="Single",  variable=var,value=1)
    r_2 = tk.Radiobutton(window, text="Multiple", variable=var, value=2)
    r_1.grid(column=2,row=3)
    r_2.grid(column=3, row=3)

    rotation_label = Label(text="Rotation: ",width=15)
    rotation_label.grid(column=1, row=4)

    variable = tk.StringVar(window)
    variable.set(ROTATIONS[0])  # default value
    w = tk.OptionMenu(window, variable, *ROTATIONS)
    w.grid(column=2,row=4, columnspan=2)

    add_water_mark_btn = tk.Button(window, text='Add Watermark',command= lambda: add_watermark(img_path))
    add_water_mark_btn.grid(column=1, row=5)

    window.mainloop()

