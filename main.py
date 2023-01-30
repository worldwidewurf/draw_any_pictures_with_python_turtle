import os
import os.path
import sys
import time
import turtle as renaissance_painter
from split_image import split_image
from pathlib import Path
from natsort import natsorted
from PIL import Image as image

def get_pixels(image_path,height,width,foldername):
    # split picture to cells
    split_image(image_path, height, width, False, False,output_dir=foldername )


def get_answer(prompt):
    # handle all inputs
    user_input = input(prompt)
    return user_input


def delay_print(d_string):
    
    for letter in d_string:
        sys.stdout.write(letter)
        sys.stdout.flush()
        time.sleep(0.01)

     
def get_height():
    
    while True:
        answer = get_answer('height of your image in millimeters: ')
        if answer.isdigit():
            height = answer
            break
        else:
           print('Height must be a number') 
           continue
    while True:
        answer = get_answer('width of your image in millimeters: ')
        if answer.isdigit():
            width = answer
            break
        else:
           print('width must be a number') 
           continue
    return int(height) , int(width)


def image_path():
    path = get_answer('What is the name of the image(eg monalisa.jpg): ')
    if os.path.isfile(path):
        return path
    else:
        print('File does not exist.')
        image_path()

def rbg(image_p,x,y):
    im = image.open(image_p).convert('RGB')
    r,g,b = im.getpixel((x,y))
    a = (r,g,b)
    return a


def iterate_images_folder(folder,image_extension,height,width):
    lists = []
 
    folder_dir = folder
    if image_extension == '.png':
        images = Path(folder_dir).glob('*.png')
    elif image_extension == '.jpg':
        images = Path(folder_dir).glob('*.jpg')
    images = natsorted(images, key=str)
    rows = []
    k = 0
    for image in images:
        k +=1 
        color = rbg(image,1,1)
        if k != width:
            rows.append(color)
        else:
            rows.append(color)
            lists.append(rows)
            # print(len(rows))
            k = 0
            rows = []
    return lists

def draw(canvas_plain,color_lists):
    renaissance_painter.penup()
    renaissance_painter.goto(-150, 195)
    renaissance_painter.pendown()
    renaissance_painter.speed('fastest')
    renaissance_painter.tracer(1,0)
    x, y = renaissance_painter.xcor(), renaissance_painter.ycor()
    color_row = 0
    for row in canvas_plain:
        color_cell = 0
        for cell in row:
            if cell == '#':
                renaissance_painter.colormode(255)
                renaissance_painter.color(color_lists[color_row][color_cell])
                # renaissance_painter.color("black")
                renaissance_painter.begin_fill()
                renaissance_painter.goto(x, y)
                renaissance_painter.setheading(90)
                for _ in range(4):
                    renaissance_painter.forward(5)
                    renaissance_painter.right(90)
                renaissance_painter.end_fill()

            color_cell+=1
            x += 5
            renaissance_painter.goto(x, y)
        color_row+=1
        x = renaissance_painter.xcor() - 5*len(row)
        y -= 5
        renaissance_painter.goto(x, y)
    renaissance_painter.penup()
    renaissance_painter.tracer(1,0)
    renaissance_painter.goto(0, 0)
    renaissance_painter.done()

def get_folder_name():
    answer = get_answer('folder name: ')
    if os.path.exists(answer):
        return answer
    else:
        get_folder_name()
    
    
def canvas(height,width):
    canva = [['#'] * width] * height
    return canva

def main():
    print('Before continuing with this process get your image height and width.')
    print('''after getting your image specs use those to get the measurements in millimeter. 
          
so basically convert convert pixels to millimeters

a website id suggest is blitzresults.com/en/pixel''')
    while True:
        answer = get_answer('Do you have pictures already split(Y/n)?: ')
        if answer.lower() == 'n':
            height , width = get_height()
            path = image_path()
            image_extension = path[-4:]
            foldername = path[:-4]
            get_pixels(path,height,width,foldername)
            canvas_plain = canvas(height,width)
            color_lists = iterate_images_folder(foldername,image_extension,height,width)
            draw(canvas_plain,color_lists)
        elif answer.lower()=='y':
            height , width = get_height()
            image_extension = get_answer('what is the image extension(eg .png : ')
            foldername = get_folder_name()
            canvas_plain = canvas(height,width)
            color_lists = iterate_images_folder(foldername,image_extension,height,width)
            draw(canvas_plain,color_lists)
    
if __name__ == "__main__":
    main()
