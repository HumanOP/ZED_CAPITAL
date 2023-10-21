import tkinter
import customtkinter
import os
from threading import *
import testing_1
import colab_1
import time
from PIL import Image, ImageTk
import sys


customtkinter.set_appearance_mode("dark")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"

def change_appearance_mode_event(new_appearance_mode: str):
    customtkinter.set_appearance_mode(new_appearance_mode)
    
def change_theme_event(new_appearance_mode: str):
    customtkinter.set_default_color_theme(new_appearance_mode)

def change_scaling_event(new_scaling: str):
    new_scaling_float = int(new_scaling.replace("%", "")) / 100
    customtkinter.set_widget_scaling(new_scaling_float)


def select_frame_by_name(name):
    # set button color for selected button
    app.home_button.configure(fg_color=("gray75", "gray25") if name == "home" else "transparent")
    app.frame_2_button.configure(fg_color=("gray75", "gray25") if name == "frame_2" else "transparent")
    app.frame_3_button.configure(fg_color=("gray75", "gray25") if name == "frame_3" else "transparent")
    app.frame_4_button.configure(fg_color=("gray75", "gray25") if name == "frame_4" else "transparent")
    app.frame_5_button.configure(fg_color=("gray75", "gray25") if name == "frame_5" else "transparent")
    
    app.home_frame.grid_forget()
    app.second_frame.grid_forget()
    app.frame1.grid_forget()
    app.checkbox_slider_frame.grid_forget()
    app.third_frame.grid_forget()
    app.backtestoutputframe.grid_forget()
    app.backtestimageframe1.grid_forget()
    app.backtestimageframe2.grid_forget()
    # show selected frame
    if name == "home":
        app.home_frame.grid(row=0, column=1, rowspan=4,columnspan=3, sticky="nsew")
    # if name == "frame_2":
    #     app.second_frame.grid(row=0, column=1, rowspan=4,columnspan=3, sticky="nsew")

    # if name == "frame_3":
    #     app.third_frame.grid(row=0, column=1, rowspan=4,columnspan=3, sticky="nsew")        

def Dashboard():
    select_frame_by_name("home")
    
    # create home frame

def Strategies():
    select_frame_by_name("frame_2")
    print("Strategies clicked")
    customtkinter.set_default_color_theme("green")
    
    # app.main_button_1 = customtkinter.CTkButton(master=app, fg_color="transparent", border_width=2,text="Play", text_color=("gray10", "#DEE4EE"),command=strategy_1)
    # app.main_button_1.grid(row=6, column=4, padx=(20, 10), pady=(10, 20), sticky="nsew")
  
    
    app.frame1 = customtkinter.CTkFrame(app, width=250, height=250)
    app.frame1.grid(row=0, column=1,columnspan=3,rowspan=4 ,padx=(10, 10), pady=(10, 10), sticky="nsew")
    app.frame1.columnconfigure((0,1,2),weight=1)

    app.label = customtkinter.CTkLabel(master=app.frame1, text="Strategies", font=customtkinter.CTkFont(size=15, weight="bold"))
    app.label.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
    app.btn_1 = customtkinter.CTkButton(app.frame1, text="Yash", command=Strategy_1_inputs)
    app.btn_1.grid(row=1, column=1, padx=20, pady=(10, 10))
    app.btn_2 = customtkinter.CTkButton(app.frame1, text="Ashish", command=Strategy_2_inputs)
    app.btn_2.grid(row=2, column=1, padx=20, pady=(10, 10))
    app.btn_3 = customtkinter.CTkButton(app.frame1, text="Divyanshu", command=Strategy_3_inputs)
    app.btn_3.grid(row=3, column=1, padx=20, pady=(10, 10))

  
class OutputStream:
    def __init__(self):
        self.data = ""
    
    def write(self, msg):
        self.data += msg
    
    def flush(self):
        pass  # Just to handle flush calls, if any

    def get_data(self):
        return self.data.strip() 
 
def is_float(s):
    """Check if the input string is a float."""
    try:
        float(s)
        return True
    except ValueError:
        return False

def show_error_message(title, message):
    error_popup = customtkinter.CTkToplevel()
    error_popup.title(title)
    error_popup.geometry("500x200")

    error_label = customtkinter.CTkLabel(error_popup, text=message)
    error_label.pack(pady=20, padx=20)

    def close_popup():
        error_popup.destroy()

    btn_ok = customtkinter.CTkButton(error_popup, text="OK", command=close_popup)
    btn_ok.pack(pady=10)

    error_popup.mainloop()
 
 
def Strategy_1_inputs():
    popup = customtkinter.CTkToplevel()
    popup.title("Inputs")
    popup.geometry("500x500")
    popup.grid_columnconfigure((0,1), weight=1)
    popup.grid_rowconfigure((0,1,2,3), weight=1)

    label1 = customtkinter.CTkLabel(popup, text="Stock symbol\n(NSE)")
    label1.grid(row=0, column=0, pady=5, padx=20, sticky='nswe')
    entry1 = customtkinter.CTkEntry(popup)
    entry1.grid(row=0, column=1, pady=5, padx=20)

    vcmd = popup.register(lambda s: is_float(s) or s == "")
    
    label2 = customtkinter.CTkLabel(popup, text="Time Period\n(as Integer)")
    label2.grid(row=1, column=0, pady=5, padx=20, sticky='nswe')
    entry2 = customtkinter.CTkEntry(popup, validate="key", validatecommand=(vcmd, "%P"))
    entry2.grid(row=1, column=1, pady=5, padx=20)

    label3 = customtkinter.CTkLabel(popup, text="Initial Investment\n(as Integer in rupees)")
    label3.grid(row=2, column=0, pady=5, padx=20, sticky='nswe')
    entry3 = customtkinter.CTkEntry(popup, validate="key", validatecommand=(vcmd, "%P"))
    entry3.grid(row=2, column=1, pady=5, padx=20)

    def run_program():
        # Retrieve the input and run another program or function
        ticker_symbol = entry1.get()
        time_period = float(entry2.get())
        initial_investment = float(entry3.get())
        original_stdout = sys.stdout  # Save the original standard output
        captured_output = OutputStream()
        sys.stdout = captured_output
        
        try:
            # Call the function whose output you want to capture
            testing_1.execute_strategy(ticker_symbol, time_period, initial_investment)
        except Exception as e:
            show_error_message("Error", str(e))
        finally:
            # Always revert stdout, even if the function call raised an error
            sys.stdout = original_stdout

        # Step 3: Update the label
        global output_text
        output_text=""
        output_text = captured_output.get_data()
        print(f"You entered: {ticker_symbol, time_period, initial_investment}")
        Backtesting()
        # popup.destroy()

    btn_run = customtkinter.CTkButton(popup, text="Run Program", command=run_program)
    btn_run.grid(row=3, column=1, pady=10, padx=20, sticky='e')
    btn = customtkinter.CTkButton(popup, text="Cancel", command=popup.destroy)
    btn.grid(row=3, column=0, pady=10, padx=20, sticky='w')

def Strategy_2_inputs():
    popup = customtkinter.CTkToplevel()
    popup.title("Inputs")
    popup.geometry("500x500")
    popup.grid_columnconfigure((0,1), weight=1)
    popup.grid_rowconfigure((0,1,2,3), weight=1)

    label1 = customtkinter.CTkLabel(popup, text="Stock symbol\n(NSE)")
    label1.grid(row=0, column=0, pady=5, padx=20, sticky='nswe')
    entry1 = customtkinter.CTkEntry(popup)
    entry1.grid(row=0, column=1, pady=5, padx=20)

    vcmd = popup.register(lambda s: is_float(s) or s == "")
    
    label2 = customtkinter.CTkLabel(popup, text="Time Period\n(as Integer)")
    label2.grid(row=1, column=0, pady=5, padx=20, sticky='nswe')
    entry2 = customtkinter.CTkEntry(popup, validate="key", validatecommand=(vcmd, "%P"))
    entry2.grid(row=1, column=1, pady=5, padx=20)

    label3 = customtkinter.CTkLabel(popup, text="Initial Investment\n(as Integer in rupees)")
    label3.grid(row=2, column=0, pady=5, padx=20, sticky='nswe')
    entry3 = customtkinter.CTkEntry(popup, validate="key", validatecommand=(vcmd, "%P"))
    entry3.grid(row=2, column=1, pady=5, padx=20)

    def run_program():
        # Retrieve the input and run another program or function
        ticker_symbol = entry1.get()
        time_period = int(entry2.get())
        initial_investment = int(entry3.get())
        
        # Validate inputs
        error_messages = []
        if not ticker_symbol:
            error_messages.append("Please provide a valid Stock symbol in text format.")
        
        if not is_float(time_period):
            error_messages.append("Time Period should be in float format.")
        
        if not is_float(initial_investment):
            error_messages.append("Initial Investment should be in float format.")

        if error_messages:
            show_error_message("Input Error", "\n".join(error_messages))
            return
        original_stdout = sys.stdout  # Save the original standard output
        captured_output = OutputStream()
        sys.stdout = captured_output
        
        try:
            # Call the function whose output you want to capture
            colab_1.execute_strategy(ticker_symbol, time_period, initial_investment)
            
        except Exception as e:
            show_error_message("Error", str(e))
        
        finally:
            # Always revert stdout, even if the function call raised an error
            sys.stdout = original_stdout

        # Step 3: Update the label
        global output_text
        output_text=""
        output_text = captured_output.get_data()
        print(f"You entered: {ticker_symbol, time_period, initial_investment}")
        Backtesting()
        # popup.destroy()

    btn_run = customtkinter.CTkButton(popup, text="Run Program", command=run_program)
    btn_run.grid(row=3, column=1, pady=10, padx=20, sticky='e')
    btn = customtkinter.CTkButton(popup, text="Cancel", command=popup.destroy)
    btn.grid(row=3, column=0, pady=10, padx=20, sticky='w')
  
def Strategy_3_inputs():
    popup = customtkinter.CTkToplevel()
    popup.title("Inputs")
    popup.geometry("500x500")
    popup.grid_columnconfigure((0,1), weight=1)
    popup.grid_rowconfigure((0,1,2,3), weight=1)

    label1 = customtkinter.CTkLabel(popup, text="Stock symbol\n(NSE)")
    label1.grid(row=0, column=0, pady=5, padx=20, sticky='nswe')
    entry1 = customtkinter.CTkEntry(popup)
    entry1.grid(row=0, column=1, pady=5, padx=20)

    vcmd = popup.register(lambda s: is_float(s) or s == "")
    
    label2 = customtkinter.CTkLabel(popup, text="Time Period\n(as Integer)")
    label2.grid(row=1, column=0, pady=5, padx=20, sticky='nswe')
    entry2 = customtkinter.CTkEntry(popup, validate="key", validatecommand=(vcmd, "%P"))
    entry2.grid(row=1, column=1, pady=5, padx=20)

    label3 = customtkinter.CTkLabel(popup, text="Initial Investment\n(as Integer in rupees)")
    label3.grid(row=2, column=0, pady=5, padx=20, sticky='nswe')
    entry3 = customtkinter.CTkEntry(popup, validate="key", validatecommand=(vcmd, "%P"))
    entry3.grid(row=2, column=1, pady=5, padx=20)

    def run_program():
        # Retrieve the input and run another program or function
        ticker_symbol = entry1.get()
        time_period = int(entry2.get())
        initial_investment = int(entry3.get())
        
        # Validate inputs
        error_messages = []
        if not ticker_symbol:
            error_messages.append("Please provide a valid Stock symbol in text format.")
        
        if not is_float(time_period):
            error_messages.append("Time Period should be in float format.")
        
        if not is_float(initial_investment):
            error_messages.append("Initial Investment should be in float format.")

        if error_messages:
            show_error_message("Input Error", "\n".join(error_messages))
            return
        original_stdout = sys.stdout  # Save the original standard output
        captured_output = OutputStream()
        sys.stdout = captured_output
        
        try:
            # Call the function whose output you want to capture
            colab_1.execute_strategy(ticker_symbol, time_period, initial_investment)
            
        except Exception as e:
            show_error_message("Error", str(e))
        
        finally:
            # Always revert stdout, even if the function call raised an error
            sys.stdout = original_stdout

        # Step 3: Update the label
        global output_text
        output_text=""
        output_text = captured_output.get_data()
        print(f"You entered: {ticker_symbol, time_period, initial_investment}")
        Backtesting()
        # popup.destroy()
        
    btn_run = customtkinter.CTkButton(popup, text="Run Program", command=run_program)
    btn_run.grid(row=3, column=1, pady=10, padx=20, sticky='e')
    btn = customtkinter.CTkButton(popup, text="Cancel", command=popup.destroy)
    btn.grid(row=3, column=0, pady=10, padx=20, sticky='w')

   
 
def Data_center():
    select_frame_by_name("frame_3")
    print("Data_center click")
    
    customtkinter.set_default_color_theme("green")
 

    app.main_button_1 = customtkinter.CTkButton(master=app, fg_color="transparent", border_width=2,text="Play", text_color=("gray10", "#DCE4EE"),command=Strategy_1_inputs)
    app.main_button_1.grid(row=6, column=4, padx=(20, 10), pady=(10, 20), sticky="nsew")
  
def Backtesting():
    select_frame_by_name("frame_4")
    print("Data_center click")
    app.geometry("1000x700")
    customtkinter.set_default_color_theme("green")
    
    app.backtestoutputframe = customtkinter.CTkFrame(app)
    app.backtestoutputframe.grid(row=0, column=1, rowspan=4, padx=(10, 10), pady=(10, 10), sticky="nsew")
    app.backtestoutputframe.grid_columnconfigure(0, weight=1)
    app.backtestoutputframe.grid_rowconfigure(0, weight=1)

    app.output_text_widget = customtkinter.CTkTextbox(app.backtestoutputframe)
    app.output_text_widget.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
    app.output_text_widget.insert("0.0", output_text)

    app.prev_size_1 = (0, 0)
    app.prev_size_2 = (0, 0)

    def resize_image_if_changed(frame, original_image, image_label, prev_size_attr):
        current_size = (frame.winfo_width(), frame.winfo_height())
        prev_size = getattr(app, prev_size_attr)
    
        if abs(current_size[0] - prev_size[0]) > 10 or abs(current_size[1] - prev_size[1]) > 10:
            scaled_image = original_image.resize(current_size, Image.LANCZOS)
            photo_image = ImageTk.PhotoImage(scaled_image)
            image_label.configure(image=photo_image)
            image_label.image = photo_image
            setattr(app, prev_size_attr, current_size)

    original_image1 = Image.open(r"C:\Users\bhush\Desktop\CP\zed_capital\test_images\Signals.png")
    original_image2 = Image.open(r"C:\Users\bhush\Desktop\CP\zed_capital\test_images\Portfolio.png")

    app.grid_rowconfigure(0, weight=1)  # For app.backtestimageframe1
    app.grid_rowconfigure(2, weight=1)  # For app.backtestimageframe2

    app.backtestimageframe1 = customtkinter.CTkFrame(app,fg_color=None,bg_color="transparent")
    app.backtestimageframe1.grid(row=0, column=2, rowspan=2, columnspan=2, padx=(10, 10), pady=(10, 10), sticky="nsew")
    app.backtestimageframe1.grid_columnconfigure(0, weight=1)
    app.backtestimageframe1.grid_rowconfigure(0, weight=1)
    photo_image1 = ImageTk.PhotoImage(original_image1)
    app.image_label1 = customtkinter.CTkLabel(app.backtestimageframe1, image=photo_image1, text="")
    app.image_label1.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
    app.backtestimageframe1.bind("<Configure>", lambda event: resize_image_if_changed(app.backtestimageframe1, original_image1, app.image_label1, "prev_size_1"))

    app.backtestimageframe2 = customtkinter.CTkFrame(app)
    app.backtestimageframe2.grid(row=2, column=2, rowspan=2, columnspan=2, padx=(10, 10), pady=(10, 10), sticky="nsew")
    app.backtestimageframe2.grid_columnconfigure(0, weight=1)
    app.backtestimageframe2.grid_rowconfigure(0, weight=1)
    photo_image2 = ImageTk.PhotoImage(original_image2)
    app.image_label2 = customtkinter.CTkLabel(app.backtestimageframe2, image=photo_image2, text="")
    app.image_label2.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
    app.backtestimageframe2.bind("<Configure>", lambda event: resize_image_if_changed(app.backtestimageframe2, original_image2, app.image_label2, "prev_size_2"))


def main():
    #app.geometry("700x700")
    app.state('zoomed')
    app.title("Our APP")
    # current_path = os.path.dirname(os.path.realpath(__file__))
    # app.bg_image = customtkinter.CTkImage(Image.open(current_path + "/test_images/bg_gradient.jpg"),size=(app._current_width, app._current_height))
    # app.bg_image_label = customtkinter.CTkLabel(app, image=app.bg_image)
    # app.bg_image_label.grid(row=0,rowspan=4, column=0,columnspan=4)

    # configure grid layout (4x3)
    app.grid_columnconfigure(1, weight=1)
    app.grid_columnconfigure((2,3), weight=1)
    app.grid_rowconfigure((0, 1, 2), weight=1)

    # load images with light and dark mode image
    image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "test_images")
    app.logo_image = customtkinter.CTkImage(Image.open(os.path.join(image_path, "logo.png")), size=(40, 36))
    app.large_test_image = customtkinter.CTkImage(Image.open(os.path.join(image_path, "large_test_image.png")), size=(500, 150))
    app.image_icon_image = customtkinter.CTkImage(Image.open(os.path.join(image_path, "image_icon_light.png")), size=(20, 20))
    app.home_image = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "home_dark.png")),
                                                dark_image=Image.open(os.path.join(image_path, "home_light.png")), size=(20, 20))
    app.chat_image = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "chat_dark.png")),
                                                dark_image=Image.open(os.path.join(image_path, "chat_light.png")), size=(20, 20))
    app.add_user_image = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "add_user_dark.png")),
                                                    dark_image=Image.open(os.path.join(image_path, "add_user_light.png")), size=(20, 20))



    # create slider and progressbar frame
    app.progressbar_1 = customtkinter.CTkProgressBar(app)
    app.progressbar_1.grid(row=5, column=1, columnspan=4, padx=(10, 10), pady=(10, 0), sticky="nsew")
    # set default values 
    app.progressbar_1.configure(mode="intermidiate")
    app.progressbar_1.start()
    
    
    # create sidebar frame with widgets
    app.sidebar_frame = customtkinter.CTkFrame(app, width=140, corner_radius=0)
    app.sidebar_frame.grid(row=0, column=0, rowspan=7, sticky="nsew")
    app.sidebar_frame.grid_rowconfigure(8, weight=1)

    app.logo_label = customtkinter.CTkLabel(app.sidebar_frame, text="  ZED CAPITAL", image=app.logo_image,compound="left", font=customtkinter.CTkFont(size=20, weight="bold"))
    app.logo_label.grid(row=0, column=0, padx=20, pady=20)
    app.home_button = customtkinter.CTkButton(app.sidebar_frame, corner_radius=0, height=40, border_spacing=10, text="Home", fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("#009FFF"), image=app.home_image, anchor="w", command=Dashboard)
    app.home_button.grid(row=1, column=0, sticky="ew")
    app.frame_2_button = customtkinter.CTkButton(app.sidebar_frame, corner_radius=0, height=40, border_spacing=10, text="Strategies",fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("#009CFF"), image=app.chat_image, anchor="w", command=Strategies)
    app.frame_2_button.grid(row=2, column=0, sticky="ew")
    app.frame_3_button = customtkinter.CTkButton(app.sidebar_frame, corner_radius=0, height=40, border_spacing=10, text="Data Center", fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("#009AFF"), image=app.add_user_image, anchor="w", command=Data_center)
    app.frame_3_button.grid(row=3, column=0, sticky="ew")
    app.frame_4_button = customtkinter.CTkButton(app.sidebar_frame, corner_radius=0, height=40, border_spacing=10, text="Backtesting",fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("#0097FF"), image=app.chat_image, anchor="w", command=Backtesting) # Repots tab + Analytics tab
    app.frame_4_button.grid(row=4, column=0, sticky="ew")
    
    
    
    
    app.frame_5_button = customtkinter.CTkButton(app.sidebar_frame, corner_radius=0, height=40, border_spacing=10, text="Settings", fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("#0093FF"), image=app.add_user_image, anchor="w", command=Data_center)
    app.frame_5_button.grid(row=9, column=0, sticky="ew")




    # create home frame
    app.home_frame = customtkinter.CTkFrame(app, corner_radius=0, fg_color="transparent")
    app.home_frame.grid_columnconfigure(0, weight=1)
    app.home_frame.grid_rowconfigure((0, 1, 2), weight=1)

    app.textbox = customtkinter.CTkTextbox(app.home_frame, width=250, font=customtkinter.CTkFont(family="Courier", size=25))
    app.textbox.grid(row=0, column=0,rowspan=3, columnspan=5, padx=(20, 20), pady=(20, 20), sticky="nsew")
    app.textbox.insert("0.0", "Bihar Innovation Challenge 2023\n\nTEAM NAME: ZED CAPITAL\n\nOur mission is to provide individuals of all experience levels with the tools and knowledge to make informed investment decisions, leveraging the power of algorithmic trading and data-driven strategies.\n\nWe envision a future where anyone, regardless of their financial background, can confidently navigate the complexities of financial markets and achieve their wealth-building goals.\n\nCOLLEGE: Indian Institute OF Technology Roorkee​\nTEAM: YASH KUMAR\n      DIVYANSHU KASHYAP​\n      ASHISH BHARDWAJ​\n")
    
    
    # create second frame
    app.second_frame = customtkinter.CTkFrame(app, corner_radius=0, fg_color="transparent")
    app.second_frame.grid_columnconfigure(0, weight=1)
    app.second_frame.grid_rowconfigure((0, 1, 2), weight=1)
    app.frame1 = customtkinter.CTkFrame(app, corner_radius=0, fg_color="transparent")
    app.frame1.grid_columnconfigure(0, weight=1)
    app.checkbox_slider_frame = customtkinter.CTkFrame(app, width=250, height=250)
    app.checkbox_slider_frame.grid(row=0, column=3,columnspan=2, padx=(20, 20), pady=(20, 0), sticky="nsew")
    
    # create third frame
    app.third_frame = customtkinter.CTkFrame(app, corner_radius=0, fg_color="transparent")
    app.third_frame.grid_columnconfigure(0, weight=1)
    app.third_frame.grid_rowconfigure((0, 1, 2), weight=1)
    
    # create fourth frame
    app.backtestoutputframe = customtkinter.CTkFrame(app)
    app.backtestoutputframe.grid(row=0, column=1,rowspan=4,padx=(10, 10), pady=(10, 10), sticky="nsew")
    app.backtestimageframe1 = customtkinter.CTkFrame(app)
    app.backtestimageframe1.grid(row=0, column=2,rowspan=2 ,padx=(10, 10), pady=(10, 10), sticky="nsew")
    app.backtestimageframe2 = customtkinter.CTkFrame(app)
    app.backtestimageframe2.grid(row=2, column=2,rowspan=2  ,padx=(10, 10), pady=(10, 10), sticky="nsew")
    
    # create fifth frame
    app.fifth_frame = customtkinter.CTkFrame(app, corner_radius=0, fg_color="transparent")
    app.fifth_frame.grid_columnconfigure(0, weight=1)
    app.fifth_frame.grid_rowconfigure((0, 1, 2), weight=1)
    
    # app.scaling_label = customtkinter.CTkLabel(app.fifth_frame, text="UI Scaling:", anchor="w")
    # app.scaling_label.grid(row=7, column=0, padx=20, pady=(10, 0))
    # app.scaling_optionemenu = customtkinter.CTkOptionMenu(app.fifth_frame, values=["80%", "90%", "100%", "110%", "120%"],command=change_scaling_event)
    # app.scaling_optionemenu.grid(row=8, column=0, padx=20, pady=(10, 20))
    # app.scaling_optionemenu.set("100%")
    
    # select default frame
    select_frame_by_name("home")
    app.mainloop()
    
    
if __name__ == "__main__":
    app = customtkinter.CTk()
    main()
