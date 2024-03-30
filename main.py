import tkinter
import customtkinter
import cv2
import os
from PIL import Image, ImageTk
import face_recognition
# Define the directory where the photos will be saved
SAVE_DIR = "./photos"
TEXT = ""

class CameraApp:
    def __init__(self, window):
        self.window = window
        self.window.title("Biometry")
        self.window.configure(bg='blue')
        self.cap = cv2.VideoCapture(0)

        # Create the label for displaying the camera image
        self.label =  customtkinter.CTkLabel(self.window, text=TEXT)
        self.label.pack()

        # Create the button for taking photos
        self.button = customtkinter.CTkButton(self.window, fg_color='blue', text="Analyze Face", command=self.take_photo)
        self.button.pack()

        # Set up the main loop to update the camera image
        self.update_camera()

    def update_camera(self):
        ret, frame = self.cap.read()
        if ret:
            # Convert the OpenCV image to a PIL image
            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image = Image.fromarray(image)

            # Convert the PIL image to a Tkinter PhotoImage
            photo = ImageTk.PhotoImage(image=image)

            # Update the label with the new image
            self.label.configure(image=photo)
            self.label.image = photo

        # Schedule the next update in 10 milliseconds
        self.window.after(10, self.update_camera)

    def analyze_user(self):
            print("Analyze the face...")
            baseImg = face_recognition.load_image_file("example.jpg")
            baseImg = cv2.cvtColor(baseImg, cv2.COLOR_BGR2RGB)

            myface = face_recognition.face_locations(baseImg)[0]
            encodemyface = face_recognition.face_encodings(baseImg)[0]
            cv2.rectangle(baseImg, (myface[3], myface[0]), (myface[1], myface[2]), (255, 255, 0), 2)

            # cv2.imshow("Find me",baseImg)
            # cv2.waitKey(0)

            sampleimg = face_recognition.load_image_file(SAVE_DIR+"/photo.jpg")
            sampleimg = cv2.cvtColor(sampleimg, cv2.COLOR_BGR2RGB)

            try:
                samplefacetest = face_recognition.face_locations(sampleimg)[0]
                encodesamplefacetest = face_recognition.face_encodings(sampleimg)[0]
            except IndexError as e:
                #TEXT = "Лицо не найдено"
                print("FAILED AUTHENTICATION")


            result = face_recognition.compare_faces([encodemyface], encodesamplefacetest)
            resultString = str(result)
            print(resultString)

            if resultString == "[True]":
                print("SUCCESSFUL AUTHENTICATION")
                self.open_capybara()
            else:
                print("FAILED AUTHENTICATION")


    def open_capybara(self):
        # Specify the path to the image file
        image_path = "successful_check.png"

        # Load the image using OpenCV
        image = cv2.imread(image_path)

        # Get the screen resolution
        screen_res = (1920, 1080)

        # Resize the image to fit the screen
        image = cv2.resize(image, screen_res)

        # Open a window and display the image in full-screen mode
        cv2.namedWindow("Image", cv2.WINDOW_NORMAL)
        cv2.setWindowProperty("Image", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
        cv2.imshow("Image", image)

        # Wait for a key press to close the window
        cv2.waitKey(0)
        cv2.destroyAllWindows()


    def take_photo(self):
        # Create the save directory if it doesn't exist
        if not os.path.exists(SAVE_DIR):
            os.makedirs(SAVE_DIR)

        # Capture a frame from the camera
        ret, frame = self.cap.read()

        if ret:
            # Save the frame to a file
            filename = os.path.join(SAVE_DIR, "photo.jpg")
            cv2.imwrite(filename, frame)
            print("access to the photo was obtained ", filename)
            self.analyze_user()


if __name__ == "__main__":
    # Create the main window and run the program
    customtkinter.set_appearance_mode("System")  # Modes: system (default), light, dark
    customtkinter.set_default_color_theme("green")  # Themes: blue (default), dark-blue, green

    window = customtkinter.CTk()
    window.configure(bg="green")

    app = CameraApp(window)
    window.mainloop()