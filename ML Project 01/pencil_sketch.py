import cv2
import numpy as np
from tkinter import Tk, Label, Button, filedialog
from PIL import Image, ImageTk

class PencilSketchApp:
    def __init__(self, master):
        self.master = master
        master.title("Pencil Sketch from Photo")

        self.label = Label(master, text="Upload an image to convert to pencil sketch with 3D effects.")
        self.label.pack()

        self.upload_button = Button(master, text="Upload Image", command=self.upload_image)
        self.upload_button.pack()

        self.sketch_button = Button(master, text="Convert to Pencil Sketch", command=self.convert_to_sketch, state='disabled')
        self.sketch_button.pack()

        self.image_label = Label(master)
        self.image_label.pack()

    def upload_image(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            self.original_image = cv2.imread(file_path)
            if self.original_image is not None:
                self.resized_image = self.resize_image(self.original_image, width=600)  # Resize the image to a width of 600 pixels
                self.display_image(self.resized_image)
                self.sketch_button.config(state='normal')
            else:
                print("Error: Unable to read image file.")

    def display_image(self, image):
        # Convert the image from OpenCV format to PIL format
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image_pil = Image.fromarray(image_rgb)
        image_tk = ImageTk.PhotoImage(image_pil)

        # Update the label with the image
        self.image_label.configure(image=image_tk)
        self.image_label.image = image_tk

    def resize_image(self, image, width=None, height=None):
        (h, w) = image.shape[:2]
        if width is None and height is None:
            return image
        if width is None:
            r = height / float(h)
            dim = (int(w * r), height)
        else:
            r = width / float(w)
            dim = (width, int(h * r))

        print(f"Resizing image to dimensions: {dim}")
        resized = cv2.resize(image, dim, interpolation=cv2.INTER_AREA)
        return resized

    def convert_to_sketch(self):
        gray_image = cv2.cvtColor(self.resized_image, cv2.COLOR_BGR2GRAY)
        inv_gray_image = 255 - gray_image
        blurred_image = cv2.GaussianBlur(inv_gray_image, (21, 21), 0)
        inv_blur_image = 255 - blurred_image
        sketch_image = cv2.divide(gray_image, inv_blur_image, scale=256.0)

        # Apply a 3D effect using a simple kernel
        kernel = np.array([[0, -1, 0],
                           [-1, 5,-1],
                           [0, -1, 0]])
        sketch_3d_image = cv2.filter2D(sketch_image, -1, kernel)
        
        self.display_image(sketch_3d_image)

if __name__ == "__main__":
    root = Tk()
    app = PencilSketchApp(root)
    root.mainloop()

