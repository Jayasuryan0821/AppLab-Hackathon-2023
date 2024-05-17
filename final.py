from tkinter import *
from tkinter import filedialog,messagebox,colorchooser 
from PIL import Image, ImageDraw
import PIL 
import numpy as np
import cv2

WIDTH, HEIGHT = 500,500
CENTER = WIDTH // 2
WHITE = (255,255,255)

class Paint:
    
    def __init__(self):
        self.root = Tk()
        self.root.title("Paint App")
        
        self.brush_width = 15
        self.current_color = "#000000"
        
        self.cnv = Canvas(self.root, width = WIDTH - 10, height = HEIGHT - 10,  bg = "white")
        self.cnv.pack()
        self.cnv.bind("<B1-Motion>",self.paint)
        
        self.image = PIL.Image.new("RGB",(WIDTH,HEIGHT),WHITE)
        self.draw = ImageDraw.Draw(self.image) 
        
        self.btn_frame = Frame(self.root)
        self.btn_frame.pack(fill = X)
        
        self.btn_frame.columnconfigure(0,weight = 1)
        self.btn_frame.columnconfigure(1,weight = 1)
        self.btn_frame.columnconfigure(2,weight = 1)
        
        self.clear_btn = Button(self.btn_frame, text = "Clear",command = self.clear)
        self.clear_btn.grid(row = 0,column = 1, sticky = W + E)
        
        self.save_btn = Button(self.btn_frame, text = "Save",command = self.save)
        self.save_btn.grid(row = 1,column = 2, sticky = W + E)
        
        self.bplus_btn = Button(self.btn_frame, text = "B+",command = self.brush_plus)
        self.bplus_btn.grid(row = 0,column = 0, sticky = W + E)
        
        self.bminus_btn = Button(self.btn_frame, text = "B-",command = self.brush_minus)
        self.bminus_btn.grid(row = 1,column = 0, sticky = W + E)
        
        self.color_btn = Button(self.btn_frame, text = "Change Color",command = self.change_color)
        self.color_btn.grid(row = 1,column = 1, sticky = W + E)
        
        self.root.protocol("WM_DELETE_WINDOW",self.on_closing)
        self.root.attributes("-topmost",True)
        self.root.mainloop( )
        
        
    def paint(self,event):
        x1, y1 = (event.x - 1),(event.y - 1)
        x2, y2 = (event.x + 1),(event.y + 1) 
        self.cnv.create_rectangle(x1, y1, x2, y2, outline = self.current_color, fill = self.current_color, width = self.brush_width)
        self.draw.rectangle([x1, y1, x2 + self.brush_width, y2 + self.brush_width],outline = self.current_color, fill = self.current_color, width = self.brush_width)
        
    def clear(self):
        self.cnv.delete("all")
        self.draw.rectangle([0,0,1000,1000],fill = "white")
    
    # def save(self):
    #     filename = filedialog.asksaveasfilename(initialfile = "untitled.png",defaultextension = "png", filetypes = [("PNG",".png"), ("JPG", ".jpg")])
    #     if filename != "":
    #         self.image.save(filename)
    
    # def save(self):
    #     filename = filedialog.asksaveasfilename(initialfile="untitled.png", defaultextension=".png", filetypes=[("PNG", ".png"), ("JPG", ".jpg")])
    #     if filename != "":
    #         # Convert the Pillow image to a numpy array
    #         img_array = np.array(self.image)
            
    #         # Convert from RGB to BGR since OpenCV uses BGR by default
    #         img_array = cv2.cvtColor(img_array, cv2.COLOR_RGB2BGR)
            
    #         # Save the numpy array as an image using OpenCV
    #         cv2.imwrite(filename, img_array)
    #         print(img_array)
        
    def save(self):
        filename = filedialog.asksaveasfilename(initialfile="untitled.png", defaultextension="png", filetypes=[("PNG", ".png"), ("JPG", ".jpg")])
        if filename != "":
            img = np.array(self.image)
            img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
            cv2.imwrite(filename, img)
            self.root.destroy()
            #print(img)
         
            ## colour detection 
            
            # Flatten to one-dimensional array of pixels
            pixel_array = img.reshape(-1, img.shape[-1])

            # Find unique colors
            unique_colors = np.unique(pixel_array, axis=0)

            # Count occurrences of each unique color
            color_counts = np.bincount(
                np.apply_along_axis(
                    lambda x: np.where(np.all(x == unique_colors, axis=1))[0][0],
                    1,
                    pixel_array,
                ),
                minlength=len(unique_colors),
            )

            # Find index of maximum count
            max_count_index = np.argmax(color_counts)

            # Retrieve color associated with index
            most_used_color = unique_colors[max_count_index]

            print(f"The most used color in the image is RGB({most_used_color[0]}, {most_used_color[1]}, {most_used_color[2]})")

            emotion = np.max(most_used_color)
            for i in range(3):
                if emotion == most_used_color[0]:
                    index = 0
                elif emotion == most_used_color[1]:
                    index = 1
                else:
                    index = 2

            #print(index)
            #print(emotion)

            y = None 
            p = None 

            if y == None:
                flag = 1
            elif p == None:
                flag = 1
            else :
                flag = 0
                
            # for yellow
            if most_used_color[0]>most_used_color[1]:
                y = most_used_color[0] - most_used_color[1]
            else:
                y = most_used_color[1] - most_used_color[0]


            if y <= 50:
                color_name = "yellow"
                
                
            # for purple
            if most_used_color[0]>most_used_color[2]:
                p = most_used_color[0] - most_used_color[2]
            else:
                p = most_used_color[2] - most_used_color[0]
                

            if p<= 50:
                color_name = "purple"
                
            # for black 
            if (most_used_color[0] == most_used_color [1] and most_used_color[0] == most_used_color[2]):
                if most_used_color[0] == 0:
                    flag = 2
                    color_name ="black"
                elif most_used_color[0] == 255:
                    flag = 2
                    color_name = "white"
                


            # colour name
            if flag == 1:
                print(color_name)

            elif flag ==2:
                print(color_name)
                
            else:
                if (index == 0):
                    color_name = "red"
                    print(color_name)
                    
                elif (index == 1):
                    color_name = "green"
                    print(color_name)
                    
                elif (index == 2):
                    color_name = "blue"
                    print(color_name)
                    



            ### chatgpt model
            import openai
            #import os

            # Set up your OpenAI API key
            openai.api_key = ""

            # Set up your GPT-3 model parameters
            model_engine = "text-davinci-002"

            # Define the function to generate responses from GPT-3
            def generate_response(prompt):
                response = openai.Completion.create(
                    engine=model_engine,
                    prompt=prompt,
                    max_tokens=100,
                    n=1,
                    stop=None,
                    temperature=0.5
                )
                return response.choices[0].text.strip()

            # Prompt the user with questions
            if color_name == "yellow":
                prompt = input("I noticed you have used the colour yellow a lot in the picture you've painted, do you feel happy or excited?")
            elif color_name == "purple":
                prompt = input("I noticed you have used a lot of purple in the picture you have painted, do you feel creative?")
            elif color_name == "red":
                prompt = input("I noticed you have used a lot of red in the picture you have painted , do you feel like you're in love? or do you feel enraged about anything?")
            elif color_name == "green":
                prompt = input("I noticed you have used a lot of green in the picture you have painted, do you feel relaxed?")
            elif color_name == "blue":
                prompt  = input(" I noticed you have used a lot of blue in the picture you have painted, do you feel calm or sad?")
            elif color_name == "white":
                prompt = input("i noticed you have used a lot of white in the picture you have painted, do you feel peaceful?")
            elif color_name == "black":
                prompt = input("i noticed you used a lot of black in the picture you have painted , are you mourning anything or anyone? do you feel empty?")
            else:
                prompt = input("I'm sorry, I didn't recognize that color. How do you feel about the colors you used in your picture?")
                
            
            user_response = input(prompt)
            print("\nYOU: ")
            chat_response = generate_response(user_response)
            print("\nBOT: ")
            print(chat_response)

            
            while True:    
                # Get the user's response based on the prompt
                
                user_response = input("\nYOU: ")
                print("\nBOT: ")
            
                # Generate a response from GPT-3 based on the user's response
                if(user_response.lower()!="bye"):
                    chat_response = generate_response(user_response)
                    print("\n")
                    # Print the response from GPT-3
                    print(chat_response)
                
                elif(user_response.lower()=="bye"):
                    print("goodbye, have a great day!")
                    break


    
    def brush_plus(self):
        self.brush_width += 1
    
    def brush_minus(self):
        if self.brush_width > 1:
            self.brush_width -= 1
    
    def change_color(self):
        _,self.current_color =  colorchooser.askcolor(title = "Choose a color")
    
    def on_closing(self):
        answer = messagebox.askyesnocancel("Quit", "Would you like to save your work ?", parent = self.root)
        if answer is not None:
            if answer:
                self.save()
            self.root.destroy()
            exit(0)
    
Paint()