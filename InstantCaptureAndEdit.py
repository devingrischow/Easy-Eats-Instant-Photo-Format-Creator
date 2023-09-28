import tkinter as tk
from tkinter import filedialog
import customtkinter
from crop_Frame_Function_To_Spec import crop_Image_To_Regular_Spec
from MaskOverGreenWithEEBackground import maskOverGreenWithBackground 
import cv2

import os


customtkinter.set_appearance_mode("blue")
camera = cv2.VideoCapture(0)

#IF AN ERROR OCCURS HERE, ITS BECAUSE THE CONTINUITY CAMERA CANNOT BE FOUND

class InstantCaptureAndEdit:
    def __init__(self):

        #main window (in custom tkinter)
        self.main_window = customtkinter.CTk()
        self.main_window.geometry("719x234")

        self.main_window.title("Easy Easts Ingredient Auto Capture and Edit")


        #new ingredient entry frame 

        self.new_ingredient_entry_frame = customtkinter.CTkFrame(self.main_window, height=200)
        self.new_ingredient_entry_frame.pack(pady=25)


        #status label(ingredients NEED a name), also for any other warnings (like camera not found)
        self.statusLabel = customtkinter.CTkLabel(self.new_ingredient_entry_frame, text="")
        self.statusLabel.pack()
        
        

        self.new_ingredient_label = customtkinter.CTkLabel(self.new_ingredient_entry_frame, text="New Ingredient Name")
        self.new_ingredient_label.pack(side='left', padx=20)

        self.new_ingredient_name_entry_box = customtkinter.CTkEntry(self.new_ingredient_entry_frame,width=200)
        self.new_ingredient_name_entry_box.pack(side='right')

        #choose destination frame 
        # and edit edit button and choose destination frame(s)
        self.choose_destination_frame = customtkinter.CTkFrame(self.main_window, width=900)
        self.choose_destination_frame.pack(pady=4)

        self.open_choose_desination_dialog_box = customtkinter.CTkButton(self.choose_destination_frame, text="Choose Ingredient Photo Destination", command=self.open_and_select_output_location)
        self.open_choose_desination_dialog_box.pack(side='left', padx=20)
        self.placeholderFileNameStringVar = tk.StringVar(self.main_window, "IngredietImageOutput")
        self.destination_entry_box = customtkinter.CTkEntry(self.choose_destination_frame,textvariable=self.placeholderFileNameStringVar,state='disabled', width=300)
        self.destination_entry_box.pack(side='right', pady=10)



        #capture button frame 
        

        self.capture_button_frame = customtkinter.CTkFrame(self.main_window, height=100)
        self.capture_button_frame.pack()

        self.preview_enable = customtkinter.CTkButton(self.capture_button_frame,text="Enable Preview", command=self.enable_preview)
        self.preview_enable.pack(pady=5)

        self.initiate_capture_button = customtkinter.CTkButton(self.capture_button_frame, text="CAPTURE", height=70, width=200, command=self.clicked_Capture)
        self.initiate_capture_button.pack()
        
        
        cv2.waitKey(25)
        self.main_window.mainloop()






    def enable_preview(self):
        ret, frame = camera.read()
        self.frameOriginal = frame
        #Degreen the camera and apply the background 
        degreenedFrame = maskOverGreenWithBackground(frame, size="small")






        self.croppedOutput = crop_Image_To_Regular_Spec(degreenedFrame)

        cv2.imshow("Preview", self.croppedOutput)

        self.preview_enable.after(10, self.enable_preview)

    



    def open_and_select_output_location(self):
        filePath = filedialog.askdirectory(initialdir="IngredietImageOutput", title="Choose New Ingredient Output Location")
        
        self.placeholderFileNameStringVar.set(str(filePath))
        
        return filePath
    


    

    def clicked_Capture(self):
        newIngredientName = self.new_ingredient_name_entry_box.get()
        print(newIngredientName.isalpha())
        if newIngredientName.isalpha() == False:
            print("no name")
            self.statusLabel.configure(text="NO NAME GIVEN, PLEASE ENTER NEW NAME")
        else:
            try:
                print("saving final image")
                filePathString = self.destination_entry_box.get()
                cv2.imwrite(os.path.join(filePathString , f'{newIngredientName}.png'), self.croppedOutput)
                cv2.imwrite(os.path.join(filePathString , f'Og_{newIngredientName}.png'), self.frameOriginal)

                #cv2.imwrite(f"{newIngredientName}.png", self.croppedOutput)
            except AttributeError:
                self.enable_preview()
                self.clicked_Capture()


    

        
        



InstantCaptureAndEdit()





        

