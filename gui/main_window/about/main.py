from pathlib import Path

from tkinter import Frame, Canvas, PhotoImage
from controller import *

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path("./assets")


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)


def about():
    About()


class About(Frame):
    def __init__(self, parent, controller=None, *args, **kwargs):
        Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent

        self.configure(bg="#FFFFFF")

        self.canvas = Canvas(
            self,
            bg="#FFFFFF",
            height=432,
            width=797,
            bd=0,
            highlightthickness=0,
            relief="ridge",
        )

        self.canvas.place(x=0, y=0)
        self.canvas.create_text(
            36.0,
            43.0,
            anchor="nw",
            text="SmartStay was created by",
            fill="#5E95FF",
            font=("Montserrat Bold", 26 * -1),
        )

        self.image_image_1 = PhotoImage(file=relative_to_assets("image_1.png"))
        image_1 = self.canvas.create_image(191.0, 26.0, image=self.image_image_1)

        self.image_image_2 = PhotoImage(file=relative_to_assets("image_2.png"))
        image_2 = self.canvas.create_image(203.0, 205.0, image=self.image_image_2)

        self.image_image_3 = PhotoImage(file=relative_to_assets("image_3.png"))
        image_3 = self.canvas.create_image(565.0, 205.0, image=self.image_image_3)

        self.canvas.create_text(
            56.0,
            121.0,
            anchor="nw",
            text="Tinkerer",
            fill="#777777",
            font=("Montserrat Medium", 15 * -1),
        )

        self.canvas.create_text(
            418.0,
            121.0,
            anchor="nw",
            text="Coder",
            fill="#777777",
            font=("Montserrat Medium", 15 * -1),
        )

        self.canvas.create_text(
            56.0,
            138.0,
            anchor="nw",
            text="Person",
            fill="#5E95FF",
            font=("Montserrat Bold", 26 * -1),
        )

        self.canvas.create_text(
            418.0,
            138.0,
            anchor="nw",
            text="Person",
            fill="#5E95FF",
            font=("Montserrat Bold", 26 * -1),
        )

        self.canvas.create_text(
            56.0,
            170.0,
            anchor="nw",
            text="1",
            fill="#5E95FF",
            font=("Montserrat Bold", 18 * -1),
        )

        self.canvas.create_text(
            418.0,
            170.0,
            anchor="nw",
            text="2",
            fill="#5E95FF",
            font=("Montserrat Bold", 18 * -1),
        )

        self.image_image_4 = PhotoImage(file=relative_to_assets("image_4.png"))
        image_4 = self.canvas.create_image(308.0, 150.0, image=self.image_image_4)

        self.canvas.create_rectangle(
            56.0, 197.0, 169.0, 199.0, fill="#FFFFFF", outline=""
        )

        self.canvas.create_rectangle(
            418.0, 197.0, 531.0, 199.0, fill="#FFFFFF", outline=""
        )

        self.image_image_5 = PhotoImage(file=relative_to_assets("image_5.png"))
        image_5 = self.canvas.create_image(669.0, 151.0, image=self.image_image_5)

        self.canvas.create_text(
            197.0,
            352.0,
            anchor="nw",
            text="DAEEH Project Sem VII 2024",
            fill="#5E95FF",
            font=("Montserrat Bold", 16 * -1),
        )

        self.canvas.create_text(
            418.0,
            207.0,
            anchor="nw",
            text="Lorem ipsum dolor sit amet,",
            fill="#777777",
            font=("Montserrat Medium", 13 * -1),
        )

        self.canvas.create_text(
            418.0,
            223.0,
            anchor="nw",
            text="consectetur adipiscing elit.",
            fill="#777777",
            font=("Montserrat Medium", 13 * -1),
        )

        self.canvas.create_text(
            418.0,
            239.0,
            anchor="nw",
            text="Sed do eiusmod tempor",
            fill="#777777",
            font=("Montserrat Medium", 13 * -1),
        )

        self.canvas.create_text(
            418.0,
            255.0,
            anchor="nw",
            text="incididunt ut labore et dolore",
            fill="#777777",
            font=("Montserrat Medium", 13 * -1),
        )

        self.canvas.create_text(
            418.0,
            271.0,
            anchor="nw",
            text="magna aliqua.",
            fill="#777777",
            font=("Montserrat Medium", 13 * -1),
        )

        self.canvas.create_text(
            56.0,
            207.0,
            anchor="nw",
            text="Lorem ipsum dolor sit amet,",
            fill="#777777",
            font=("Montserrat Medium", 13 * -1),
        )

        self.canvas.create_text(
            56.0,
            223.0,
            anchor="nw",
            text="consectetur adipiscing elit.",
            fill="#777777",
            font=("Montserrat Medium", 13 * -1),
        )

        self.canvas.create_text(
            56.0,
            239.0,
            anchor="nw",
            text="Sed do eiusmod tempor",
            fill="#777777",
            font=("Montserrat Medium", 13 * -1),
        )

        self.canvas.create_text(
            56.0,
            255.0,
            anchor="nw",
            text="incididunt ut labore et dolore",
            fill="#777777",
            font=("Montserrat Medium", 13 * -1),
        )

        self.canvas.create_text(
            56.0,
            271.0,
            anchor="nw",
            text="magna aliqua.",
            fill="#777777",
            font=("Montserrat Medium", 13 * -1),
        )
