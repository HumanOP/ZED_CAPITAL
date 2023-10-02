import customtkinter
import os
import subprocess
from threading import *
import cv2
import mediapipe as mp
import pydirectinput as pd
import pyautogui as pag
import time




customtkinter.set_appearance_mode("dark")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"


app = customtkinter.CTk()
app.geometry("1100x1100")
app.title("ZED CAPITAL")

# configure grid layout (4x3)
app.grid_columnconfigure(1, weight=1)
app.grid_columnconfigure((2,3), weight=0)
app.grid_rowconfigure((0, 1, 2), weight=1)

def change_appearance_mode_event(new_appearance_mode: str):
    customtkinter.set_appearance_mode(new_appearance_mode)
    
def change_theme_event(new_appearance_mode: str):
    customtkinter.set_default_color_theme(new_appearance_mode)

def change_scaling_event(new_scaling: str):
    new_scaling_float = int(new_scaling.replace("%", "")) / 100
    customtkinter.set_widget_scaling(new_scaling_float)


def Strategies():
    print("Strategies clicked")
    customtkinter.set_default_color_theme("green")
    
    app.textbox.destroy()
    # create main entry and button
 

    app.main_button_1 = customtkinter.CTkButton(master=app, fg_color="transparent", border_width=2,text="Play", text_color=("gray10", "#DCE4EE"),command=strategy_1)
    app.main_button_1.grid(row=6, column=4, padx=(20, 10), pady=(10, 20), sticky="nsew")

    app.key_frame = customtkinter.CTkFrame(app)
    app.key_frame.grid(row=0, column=1,columnspan=4, sticky="nsew")
    app.logo_label = customtkinter.CTkLabel(master=app.key_frame, text="Key Binds", font=customtkinter.CTkFont(size=20, weight="bold"))
    app.logo_label.grid(row=0, column=1 , padx=40, pady=(0, 0))
  
    

    # create tabview
    app.frame2 = customtkinter.CTkFrame(app, width=250, height=250)
    app.frame2.grid(row=1, column=1,columnspan=2, padx=(20, 0), pady=(20, 0), sticky="nsew")

    app.label1 = customtkinter.CTkLabel(master=app.frame2, text="GESTUREs")
    app.label1.grid(row=0, column=0,  padx=10, pady=10, sticky="")
    app.label2 = customtkinter.CTkLabel(master=app.frame2, text="Moving left")
    app.label2.grid(row=1, column=0, padx=10, pady=10, sticky="")
    app.label3 = customtkinter.CTkLabel(master=app.frame2, text="Moving right")
    app.label3.grid(row=2, column=0, padx=10, pady=10, sticky="")
    app.label4 = customtkinter.CTkLabel(master=app.frame2, text="Jumping")
    app.label4.grid(row=3, column=0, padx=10, pady=10, sticky="")
    app.label5 = customtkinter.CTkLabel(master=app.frame2, text="Crouching")
    app.label5.grid(row=4, column=0, padx=10, pady=10, sticky="")




    # create checkbox and switch frame
    app.checkbox_slider_frame = customtkinter.CTkFrame(app, width=250, height=250)
    app.checkbox_slider_frame.grid(row=1, column=3,columnspan=2, padx=(20, 20), pady=(20, 0), sticky="nsew")
    app.label_radio_group = customtkinter.CTkLabel(master=app.checkbox_slider_frame, text="Triggering key")
    app.label_radio_group.grid(row=0, column=0, columnspan=2, padx=10, pady=10, sticky="")
    app.seg_button_1= customtkinter.CTkSegmentedButton(app.checkbox_slider_frame)
    app.seg_button_1.grid(row=1, column=0, padx=(20, 10), pady=(10, 10), sticky="ew")

    app.seg_button_2 = customtkinter.CTkSegmentedButton(app.checkbox_slider_frame)
    app.seg_button_2.grid(row=2, column=0, padx=(20, 10), pady=(10, 10), sticky="ew")
    
    app.seg_button_3 = customtkinter.CTkSegmentedButton(app.checkbox_slider_frame)
    app.seg_button_3.grid(row=3, column=0, padx=(20, 10), pady=(10, 10), sticky="ew")
    
    app.seg_button_4 = customtkinter.CTkSegmentedButton(app.checkbox_slider_frame)
    app.seg_button_4.grid(row=4, column=0, padx=(20, 10), pady=(10, 10), sticky="ew")
    


    # create slider and progressbar frame

    app.progressbar_1 = customtkinter.CTkProgressBar(app)
    app.progressbar_1.grid(row=5, column=1, columnspan=4, padx=(10, 10), pady=(10, 0), sticky="nsew")

    # set default values
    
    
    app.progressbar_1.configure(mode="intermidiate")
    app.progressbar_1.start()

    app.seg_button_1.configure(values=['left', 'right','up','down'])
    app.seg_button_1.set('left')
    app.seg_button_2.configure(values=['left', 'right','up','down'])
    app.seg_button_2.set('right')
    app.seg_button_3.configure(values=['left', 'right','up','down'])
    app.seg_button_3.set('up')
    app.seg_button_4.configure(values=['left', 'right','up','down'])
    app.seg_button_4.set('down')


def Data_center():
    print("Data_center click")
    
    customtkinter.set_default_color_theme("green")
    
    app.textbox.destroy()
    # create main entry and button
 

    app.main_button_1 = customtkinter.CTkButton(master=app, fg_color="transparent", border_width=2,text="Play", text_color=("gray10", "#DCE4EE"),command=minecraft)
    app.main_button_1.grid(row=6, column=4, padx=(20, 10), pady=(10, 20), sticky="nsew")

    app.key_frame = customtkinter.CTkFrame(app)
    app.key_frame.grid(row=0, column=1,columnspan=4, sticky="nsew")
    app.logo_label = customtkinter.CTkLabel(master=app.key_frame, text="Key Binds", font=customtkinter.CTkFont(size=20, weight="bold"))
    app.logo_label.grid(row=0, column=1 , padx=40, pady=(0, 0))
  
    

    # create tabview
    app.frame2 = customtkinter.CTkFrame(app, width=250, height=250)
    app.frame2.grid(row=1, column=1,columnspan=2, padx=(20, 0), pady=(20, 0), sticky="nsew")

    app.label1 = customtkinter.CTkLabel(master=app.frame2, text="GESTUREs")
    app.label1.grid(row=0, column=0,  padx=10, pady=10, sticky="")
    app.label2 = customtkinter.CTkLabel(master=app.frame2, text="Left palm open")
    app.label2.grid(row=1, column=0, padx=10, pady=10, sticky="")
    app.label3 = customtkinter.CTkLabel(master=app.frame2, text="Moving left")
    app.label3.grid(row=2, column=0, padx=10, pady=10, sticky="")
    app.label4 = customtkinter.CTkLabel(master=app.frame2, text="Moving right")
    app.label4.grid(row=3, column=0, padx=10, pady=10, sticky="")
    app.label5 = customtkinter.CTkLabel(master=app.frame2, text="Jumping")
    app.label5.grid(row=4, column=0, padx=10, pady=10, sticky="")
    app.label6 = customtkinter.CTkLabel(master=app.frame2, text="Crouching")
    app.label6.grid(row=5, column=0, padx=10, pady=10, sticky="")
    app.label7 = customtkinter.CTkLabel(master=app.frame2, text="Right hand thumb closed")
    app.label7.grid(row=6, column=0, padx=10, pady=10, sticky="")
    app.label8 = customtkinter.CTkLabel(master=app.frame2, text="Right hand midle finger down")
    app.label8.grid(row=7, column=0,  padx=10, pady=10, sticky="")
    app.label9 = customtkinter.CTkLabel(master=app.frame2, text="Wankanda symbol")
    app.label9.grid(row=8, column=0, padx=10, pady=10, sticky="")
    app.label10 = customtkinter.CTkLabel(master=app.frame2, text="left hand palm movement")
    app.label10.grid(row=9, column=0, padx=10, pady=10, sticky="")
    app.label11 = customtkinter.CTkLabel(master=app.frame2, text="release keys")
    app.label11.grid(row=10, column=0, padx=10, pady=10, sticky="")



    # create checkbox and switch frame
    app.checkbox_slider_frame = customtkinter.CTkFrame(app, width=250, height=250)
    app.checkbox_slider_frame.grid(row=1, column=3,columnspan=2, padx=(20, 20), pady=(20, 0), sticky="nsew")
    app.label_radio_group = customtkinter.CTkLabel(master=app.checkbox_slider_frame, text="Triggering key")
    app.label_radio_group.grid(row=0, column=0, columnspan=2, padx=10, pady=10, sticky="")
    app.seg_button_1= customtkinter.CTkSegmentedButton(app.checkbox_slider_frame)
    app.seg_button_1.grid(row=1, column=0, padx=(20, 10), pady=(10, 10), sticky="ew")
    app.combobox_1 = customtkinter.CTkComboBox(app.checkbox_slider_frame,
                                                values=["left click","right click","Arrow up", "Arrow down", "Arrow left","Arrow right","shift","space",'e',"scroll"])
    app.combobox_1.grid(row=5, column=0, padx=20, pady=(10, 10))

    app.seg_button_2 = customtkinter.CTkSegmentedButton(app.checkbox_slider_frame)
    app.seg_button_2.grid(row=2, column=0, padx=(20, 10), pady=(10, 10), sticky="ew")
    app.combobox_2 = customtkinter.CTkComboBox(app.checkbox_slider_frame,
                                                values=["left click","right click","Arrow up", "Arrow down", "Arrow left","Arrow right","shift","space",'e',"scroll"])
    app.combobox_2.grid(row=6, column=0, padx=20, pady=(10, 10))
    app.seg_button_3 = customtkinter.CTkSegmentedButton(app.checkbox_slider_frame)
    app.seg_button_3.grid(row=3, column=0, padx=(20, 10), pady=(10, 10), sticky="ew")
    app.combobox_3 = customtkinter.CTkComboBox(app.checkbox_slider_frame,
                                                values=["right click"])
    app.combobox_3.grid(row=7, column=0, padx=20, pady=(10, 10))
    app.combobox_4 = customtkinter.CTkComboBox(app.checkbox_slider_frame,
                                                values=["left click"])
    app.combobox_4.grid(row=8, column=0, padx=20, pady=(10, 10))
    app.combobox_5 = customtkinter.CTkComboBox(app.checkbox_slider_frame,
                                                values=["left click","right click","Arrow up", "Arrow down", "Arrow left","Arrow right","shift","space",'e',"scroll"])
    app.combobox_5.grid(row=9, column=0, padx=20, pady=(10, 10))
    app.combobox_6 = customtkinter.CTkComboBox(app.checkbox_slider_frame,
                                                values=["left click","right click","Arrow up", "Arrow down", "Arrow left","Arrow right","shift","space",'e',"scroll"])
    app.combobox_6.grid(row=10, column=0, padx=20, pady=(10, 10))


    # create slider and progressbar frame

    app.progressbar_1 = customtkinter.CTkProgressBar(app)
    app.progressbar_1.grid(row=5, column=1, columnspan=4, padx=(10, 10), pady=(10, 0), sticky="nsew")

    # set default values
    app.combobox_1.set("space")
    app.combobox_2.set("shift")
    app.combobox_3.set("right click")
    app.combobox_4.set("left click")
    app.combobox_5.set('e')
    app.combobox_6.set("scroll")
    
    app.progressbar_1.configure(mode="intermidiate")
    app.progressbar_1.start()

    app.seg_button_1.configure(values=['w', 'a','d'])
    app.seg_button_1.set('w')
    app.seg_button_2.configure(values=['w', 'a','d'])
    app.seg_button_2.set('a')
    app.seg_button_3.configure(values=['w', 'a','d'])
    app.seg_button_3.set('d')
           
       
def subway():

    class App1(Thread):
        def run(self):
            os.startfile(r"C:\Users\Prajwal Sastry\OneDrive\Desktop\SubwaySurf.lnk")
                
    class App2(Thread):
        def run(self):
            subwaygame()
                
    app1 = App1()
    app2 = App2()

    app2.start()
    app1.start()

def subwaygame():
    cap = cv2.VideoCapture(0)
    # Initiate holistic model
    with mp_holistic.Holistic(min_detection_confidence=0.5, min_tracking_confidence=0.5) as holistic:
        
        while cap.isOpened():
            success, frame = cap.read()
            # Recolor Feed
            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            # Make Detections
            results = holistic.process(image)
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
            # Right hand
            mp_drawing.draw_landmarks(image, results.right_hand_landmarks, mp_holistic.HAND_CONNECTIONS)

            # Left Hand
            mp_drawing.draw_landmarks(image, results.left_hand_landmarks, mp_holistic.HAND_CONNECTIONS)

            # Pose Detections
            mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_holistic.POSE_CONNECTIONS)
            cv2.line(image, pt1=(0, 150), pt2=(640, 150), color=(0, 0, 0), thickness=2, lineType=8, shift=0)
            cv2.line(image, pt1=(465, 0), pt2=(465, 480), color=(0, 0, 0), thickness=2, lineType=8, shift=0) 
            cv2.line(image, pt1=(175, 0), pt2=(175, 480), color=(0, 0, 0), thickness=2, lineType=8, shift=0)           
            cv2.line(image, pt1=(0, 280), pt2=(640, 280), color=(0, 0, 0), thickness=2, lineType=8, shift=0)
            cv2.imshow('Raw Webcam Feed',cv2.flip(image,1))
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            
            try:
                image_height, image_width, _ = image.shape
            

                l_sh_x=results.pose_landmarks.landmark[mp_holistic.PoseLandmark.LEFT_SHOULDER].x*image_width
                l_sh_y=results.pose_landmarks.landmark[mp_holistic.PoseLandmark.LEFT_SHOULDER].y*image_height
                
                l_wr_x=results.pose_landmarks.landmark[mp_holistic.PoseLandmark.LEFT_WRIST].x*image_width
                l_wr_y=results.pose_landmarks.landmark[mp_holistic.PoseLandmark.LEFT_WRIST].y*image_height
                
                
                screen_width,screen_height=pd.size()
                
                r_sh_x=results.pose_landmarks.landmark[mp_holistic.PoseLandmark.RIGHT_SHOULDER].x*image_width
                r_sh_y=results.pose_landmarks.landmark[mp_holistic.PoseLandmark.RIGHT_SHOULDER].y*image_height
            
                r_wr_x=results.pose_landmarks.landmark[mp_holistic.PoseLandmark.RIGHT_WRIST].x*image_width
                r_wr_y=results.pose_landmarks.landmark[mp_holistic.PoseLandmark.RIGHT_WRIST].y*image_height
            
                
                #for move to right side of screen...moving right
                if l_wr_x>465.0:
                    pd.press(app.seg_button_1.get()) 
                
                #for move to left side of screen...moving right
                if r_wr_x<175.0:
                    pd.press(app.seg_button_2.get())
                #for jump...jumping
                if r_sh_y<160 and l_sh_y<160:
                    pd.press('app.seg_button_3.get()')
                #for crouch...crouching
                if r_sh_y>270 and l_sh_y>270:
                    pd.press('app.seg_button_4.get()')
            except:
                pass
    cap.release()
    cv2.destroyAllWindows()

def strategy_1():  
    python_interpreter = r"C:\Users\bhush\AppData\Local\Microsoft\WindowsApps\python.exe"
    script_path = r"C:\Users\bhush\Desktop\CP\zed_capital\testing-1.py"
    
    command = [python_interpreter, script_path]
    subprocess.run(command, shell=True)

def minecraft():

    class App1(Thread):
        def run(self):
            os.startfile("C:\XboxGames\Minecraft Launcher\Content\gamelaunchhelper.exe")
                
    class App2(Thread):
        def run(self):
            minecraftgame()
                
    app1 = App1()
    app2 = App2()

    app2.start()
    app1.start()
   
def minecraftgame():
    cap = cv2.VideoCapture(0)
    # Initiate holistic model
    with mp_holistic.Holistic(min_detection_confidence=0.5, min_tracking_confidence=0.5) as holistic:
 
        while cap.isOpened():

            success, frame = cap.read()
            # Recolor Feed
            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            # Make Detections
            results = holistic.process(image)
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
            # Right hand
            mp_drawing.draw_landmarks(image, results.right_hand_landmarks, mp_holistic.HAND_CONNECTIONS)

            # Left Hand
            mp_drawing.draw_landmarks(image, results.left_hand_landmarks, mp_holistic.HAND_CONNECTIONS)

            # Pose Detections
            mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_holistic.POSE_CONNECTIONS)
            cv2.line(image, pt1=(0, 150), pt2=(640, 150), color=(0, 0, 0), thickness=2, lineType=8, shift=0)
            cv2.line(image, pt1=(465, 0), pt2=(465, 480), color=(0, 0, 0), thickness=2, lineType=8, shift=0) 
            cv2.line(image, pt1=(175, 0), pt2=(175, 480), color=(0, 0, 0), thickness=2, lineType=8, shift=0)           
            cv2.line(image, pt1=(0, 300), pt2=(640, 300), color=(0, 0, 0), thickness=2, lineType=8, shift=0)
            cv2.imshow('Raw Webcam Feed',cv2.flip(image,1))
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            
            try:
                image_height, image_width, _ = image.shape
                w_x = results.left_hand_landmarks.landmark[0].x*image_width
                w_y = results.left_hand_landmarks.landmark[0].y*image_height
                
                #l_mid_tip_x = results.left_hand_landmarks.landmark[mp_holistic.HandLandmark.MIDDLE_FINGER_TIP].x*image_width
                l_mid_tip_y = results.left_hand_landmarks.landmark[mp_holistic.HandLandmark.MIDDLE_FINGER_TIP].y*image_height
                l_mid_mcp_y=image_height*results.left_hand_landmarks.landmark[mp_holistic.HandLandmark.MIDDLE_FINGER_MCP].y
                

                l_sh_x=results.pose_landmarks.landmark[mp_holistic.PoseLandmark.LEFT_SHOULDER].x*image_width
                l_sh_y=results.pose_landmarks.landmark[mp_holistic.PoseLandmark.LEFT_SHOULDER].y*image_height
                
                l_palm_x=results.pose_landmarks.landmark[mp_holistic.PoseLandmark.LEFT_WRIST].x*image_width
                r_palm_x=results.pose_landmarks.landmark[mp_holistic.PoseLandmark.RIGHT_WRIST].x*image_width
                
                screen_width,screen_height=pd.size()
                
                index_x=1920-(screen_width*results.right_hand_landmarks.landmark[mp_holistic.HandLandmark.INDEX_FINGER_TIP].x)*2
                index_y=screen_height*results.right_hand_landmarks.landmark[mp_holistic.HandLandmark.INDEX_FINGER_TIP].y
                
                r_sh_x=results.pose_landmarks.landmark[mp_holistic.PoseLandmark.RIGHT_SHOULDER].x*image_width
                r_sh_y=results.pose_landmarks.landmark[mp_holistic.PoseLandmark.RIGHT_SHOULDER].y*image_height
                
                r_ring_tip_y=image_height*results.right_hand_landmarks.landmark[mp_holistic.HandLandmark.RING_FINGER_TIP].y
                
                r_thumb_tip_x=image_width*results.right_hand_landmarks.landmark[mp_holistic.HandLandmark.THUMB_TIP].x
                r_index_mcp_x=image_width*results.right_hand_landmarks.landmark[mp_holistic.HandLandmark.INDEX_FINGER_MCP].x
                
                r_mid_tip_y=image_height*results.right_hand_landmarks.landmark[mp_holistic.HandLandmark.MIDDLE_FINGER_TIP].y
                r_mid_mcp_y=image_height*results.right_hand_landmarks.landmark[mp_holistic.HandLandmark.MIDDLE_FINGER_MCP].y
                
                l_mid_tip_y=image_height*results.left_hand_landmarks.landmark[mp_holistic.HandLandmark.MIDDLE_FINGER_TIP].y
                l_mid_mcp_y=image_height*results.left_hand_landmarks.landmark[mp_holistic.HandLandmark.MIDDLE_FINGER_MCP].y
                
                #camera rotation when right ring finger up
                if r_ring_tip_y<r_mid_mcp_y:
                    pag.moveTo(index_x,index_y,0.7)
                
                            
                if l_mid_tip_y<l_mid_mcp_y:#palm forward  ...left palm open
                    pd.keyDown('app.seg_button_1.get()')
                    
                #for opening inventory...wankanda symbol
                if l_palm_x<r_palm_x:
                    pd.press(app.combobox_5.get())
                    time.sleep(0.5)
                
                #left click...right hand midle finger down
                if r_mid_tip_y>r_mid_mcp_y:
                    pag.click()
                    time.sleep(0.25)
                
                #right click...right hand thumb closed
                if r_thumb_tip_x<r_index_mcp_x:
                    pag.click(button='right')
                
                #for move to right side of screen...moving right
                if l_sh_x<320.0:
                    pd.keyDown(app.seg_button_3.get()) 
                
                #Navigate through hotbar....left hand palm movement
                if l_mid_tip_y<150:
                    pag.scroll(100)
                
                #Navigate through hotbar    
                if l_mid_mcp_y>300:
                    pag.scroll(-100)
                
                #for move to left side of screen...moving left
                if r_sh_x>320.0:
                    pd.keyDown(app.seg_button_2.get())
                    
                #for jump...jumping
                if r_sh_y<150 and l_sh_y<150:
                    pd.press(app.combobox_1.get())
                    
                #for crouch...crouching
                if r_sh_y>300 and l_sh_y>300:
                    pd.press(app.combobox_2.get())
                    
                if l_mid_tip_y>l_mid_mcp_y:#un-pressing keys...left hand fist
                    pd.keyUp('w')
                    pd.keyUp('a')
                    pd.keyUp('d')

            except:
                pass
    cap.release()
    cv2.destroyAllWindows()

# create sidebar frame with widgets
app.sidebar_frame = customtkinter.CTkFrame(app, width=140, corner_radius=0)
app.sidebar_frame.grid(row=0, column=0, rowspan=7, sticky="nsew")
app.sidebar_frame.grid_rowconfigure(4, weight=1)
app.logo_label = customtkinter.CTkLabel(app.sidebar_frame, text="PANEL 1\n", font=customtkinter.CTkFont(size=20, weight="bold"))
app.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))
app.sidebar_button_1 = customtkinter.CTkButton(app.sidebar_frame, text= "Strategies", command=Strategies)
app.sidebar_button_1.grid(row=1, column=0, padx=20, pady=10)
app.sidebar_button_2 = customtkinter.CTkButton(app.sidebar_frame, text= "Data Center", command=Data_center)
app.sidebar_button_2.grid(row=2, column=0, padx=20, pady=10)


app.scaling_label = customtkinter.CTkLabel(app.sidebar_frame, text="UI Scaling:", anchor="w")
app.scaling_label.grid(row=7, column=0, padx=20, pady=(10, 0))
app.scaling_optionemenu = customtkinter.CTkOptionMenu(app.sidebar_frame, values=["80%", "90%", "100%", "110%", "120%"],
                                                    command=change_scaling_event)
app.scaling_optionemenu.grid(row=8, column=0, padx=20, pady=(10, 20))
app.scaling_optionemenu.set("100%")

# create textbox
app.textbox = customtkinter.CTkTextbox(app, width=250, font=customtkinter.CTkFont(family="Courier", size=200))
app.textbox.grid(row=0, column=1,rowspan=3, padx=(20, 20), pady=(20, 20), sticky="nsew")
app.textbox.insert("0.0", "\n  BIC\n")
   



app.mainloop()