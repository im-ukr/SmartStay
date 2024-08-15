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
            text="Utkarsh",
            fill="#5E95FF",
            font=("Montserrat Bold", 26 * -1),
        )

        self.canvas.create_text(
            418.0,
            138.0,
            anchor="nw",
            text="Kanak",
            fill="#5E95FF",
            font=("Montserrat Bold", 26 * -1),
        )

        self.canvas.create_text(
            56.0,
            170.0,
            anchor="nw",
            text="Roy",
            fill="#5E95FF",
            font=("Montserrat Bold", 18 * -1),
        )

        self.canvas.create_text(
            418.0,
            170.0,
            anchor="nw",
            text="Pandit",
            fill="#5E95FF",
            font=("Montserrat Bold", 18 * -1),
        )

        self.image_image_4 = PhotoImage(file=relative_to_assets("imukr.png"))
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
            text="Dynamic Pricing Straetgies for Hotel Rooms",
            fill="#5E95FF",
            font=("Montserrat Bold", 16 * -1),
        )

        self.canvas.create_text(
            418.0,
            207.0,
            anchor="nw",
            text="B.Tech Undergrad specializing in",
            fill="#777777",
            font=("Montserrat Medium", 13 * -1),
        )

        self.canvas.create_text(
            418.0,
            223.0,
            anchor="nw",
            text="Computer Science. Developed an",
            fill="#777777",
            font=("Montserrat Medium", 13 * -1),
        )

        self.canvas.create_text(
            418.0,
            239.0,
            anchor="nw",
            text="email sending feature that integrates",
            fill="#777777",
            font=("Montserrat Medium", 13 * -1),
        )

        self.canvas.create_text(
            418.0,
            255.0,
            anchor="nw",
            text="seamlessly. Worked on developing",
            fill="#777777",
            font=("Montserrat Medium", 13 * -1),
        )

        self.canvas.create_text(
            418.0,
            271.0,
            anchor="nw",
            text="smart pricing parameters alongside.",
            fill="#777777",
            font=("Montserrat Medium", 13 * -1),
        )

        self.canvas.create_text(
            56.0,
            207.0,
            anchor="nw",
            text="B.Tech Undergrad specializing in",
            fill="#777777",
            font=("Montserrat Medium", 13 * -1),
        )

        self.canvas.create_text(
            56.0,
            223.0,
            anchor="nw",
            text="Artificial Intelligence and Data Science.",
            fill="#777777",
            font=("Montserrat Medium", 13 * -1),
        )

        self.canvas.create_text(
            56.0,
            239.0,
            anchor="nw",
            text="The focus was on designing a robust",
            fill="#777777",
            font=("Montserrat Medium", 13 * -1),
        )

        self.canvas.create_text(
            56.0,
            255.0,
            anchor="nw",
            text="database and implementing Dynamic",
            fill="#777777",
            font=("Montserrat Medium", 13 * -1),
        )

        self.canvas.create_text(
            56.0,
            271.0,
            anchor="nw",
            text="Pricing Engine.",
            fill="#777777",
            font=("Montserrat Medium", 13 * -1),
        )