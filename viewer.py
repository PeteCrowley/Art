from abc import abstractmethod, ABC
from tkinter import *
from PIL import ImageTk, Image


class ImageViewer(ABC):
    def __init__(self):
        self.window = Tk()
        self.img_list = []
        self.populate_image_list()
        self.num = 0
        self.image_label = Label(self.window, text="Image 0", image=self.img_list[0], compound="bottom")
        self.image_label.grid()
        self.window.bind('<Right>', lambda e: self.next_img())
        self.window.bind('<Left>', lambda e: self.last_img())

    def next_img(self):
        self.num = (self.num + 1) % len(self.img_list)
        self.update_image()

    def last_img(self):
        self.num = (self.num - 1) % len(self.img_list)
        self.update_image()

    def update_image(self):
        self.image_label.config(text=self.image_caption(), image=self.img_list[self.num])
        self.image_label.grid(row=0, column=0)

    def image_caption(self) -> str:
        return "Image " + str(self.num)

    @abstractmethod
    def populate_image_list(self):
        pass

    def run(self):
        self.window.mainloop()


class SnowflakeImageViewer(ImageViewer):
    def __init__(self):
        super().__init__()
        self.window.title("Koch's Snowflakes")
        self.update_image()

    def image_caption(self) -> str:
        return "Koch's " + str(self.num + 3) + " Sided Polygon (Depth " + str(self.get_depth()) + ")"

    def populate_image_list(self):
        for i in range(3, 21):
            img = Image.open("Images/Koch_" + str(i) + "-gon.jpg")
            img.thumbnail((1000, 700))
            img = ImageTk.PhotoImage(img)
            self.img_list.append(img)

    def get_depth(self) -> int:
        n = self.num + 3
        if n == 3:
            return 5
        if n <= 14:
            return 4
        return 3


class StarViewer(ImageViewer):
    def __init__(self):
        super().__init__()
        self.window.title("Star Viewer")
        self.captions = ["Zoomed in Star", "Star Inside Circle", "Circumscribed Star"]
        self.update_image()

    def populate_image_list(self):
        for file_name in ["Images/cool_star.jpg", "Images/inside_star.jpg", "Images/outside_star.jpg"]:
            img = Image.open(file_name)
            img.thumbnail((1000, 700))
            img = ImageTk.PhotoImage(img)
            self.img_list.append(img)

    def image_caption(self) -> str:
        return self.captions[self.num]


if __name__ == "__main__":
    viewer = StarViewer()
    viewer.run()
