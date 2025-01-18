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

        self.configure(bg="#F7F9FB")

        self.canvas = Canvas(
            self,
            bg="#F7F9FB",
            height=600,
            width=800,
            bd=0,
            highlightthickness=0,
            relief="ridge",
        )

        self.canvas.place(x=0, y=0)
        self.image_image_1 = PhotoImage(file=relative_to_assets("image_1.png"))
        self.canvas.create_image(400, 50, image=self.image_image_1)

        # Add method to Canvas to draw rounded rectangles
        Canvas.create_rounded_rectangle = self._create_rounded_rectangle

        # Curved boxes for founders
        self.create_founder_box(50, 50, "Utkarsh Roy", "BT/AI&DS-30", "Final year Student at AI&DS Batch of 2025.")
        self.create_founder_box(430, 50, "Saanvi Sadani", "BT/AI&DS-31", "Final year Student at AI&DS Batch of 2025.")
        self.create_founder_box(50, 230, "Vrushali Sandam", "BT/AI&DS-33", "Final year Student at AI&DS Batch of 2025.")
        self.create_founder_box(430, 230, "Prathna Shah", "BT/AI&DS-34", "Final year Student at AI&DS Batch of 2025.")

        # Bold part of the text
        self.canvas.create_text(
            85.0,
            15.0,
            anchor="nw",
            text="DAEEH Project Sem VII 2024",
            fill="#5E95FF",
            font=("Montserrat Bold", 16 * -1),
        )

        # Rest of the text
        self.canvas.create_text(
            85.0 + 240,  # Adjust the x position to place it right after the bold text
            15.0,
            anchor="nw",
            text=" ● Dynamic Pricing Strategies for Hotel Rooms 🏠",
            fill="#5E95FF",
            font=("Montserrat Bold", 16 * -1),
        )

    def create_founder_box(self, x, y, name, roll, description):
        box = self.canvas.create_rounded_rectangle(
            x, y, x + 320, y + 160, radius=20, fill="#FFFFFF", outline="#D1D1D1"
        )

        name_text = self.canvas.create_text(
            x + 20,
            y + 20,
            anchor="nw",
            text=name,
            fill="#5E95FF",
            font=("Montserrat Bold", 26 * -1),
        )

        roll_text = self.canvas.create_text(
            x + 20,
            y + 60,
            anchor="nw",
            text=roll,
            fill="#5E95FF",
            font=("Montserrat Bold", 18 * -1),
        )

        desc_text = self.canvas.create_text(
            x + 20,
            y + 90,
            anchor="nw",
            text=description,
            fill="#777777",
            font=("Montserrat Medium", 13 * -1),
        )

        self.canvas.tag_bind(box, "<Enter>", lambda event: self.on_hover(box, name_text, roll_text, desc_text))
        self.canvas.tag_bind(name_text, "<Enter>", lambda event: self.on_hover(box, name_text, roll_text, desc_text))
        self.canvas.tag_bind(roll_text, "<Enter>", lambda event: self.on_hover(box, name_text, roll_text, desc_text))
        self.canvas.tag_bind(desc_text, "<Enter>", lambda event: self.on_hover(box, name_text, roll_text, desc_text))

        self.canvas.tag_bind(box, "<Leave>", lambda event: self.on_leave(box, name_text, roll_text, desc_text))
        self.canvas.tag_bind(name_text, "<Leave>", lambda event: self.on_leave(box, name_text, roll_text, desc_text))
        self.canvas.tag_bind(roll_text, "<Leave>", lambda event: self.on_leave(box, name_text, roll_text, desc_text))
        self.canvas.tag_bind(desc_text, "<Leave>", lambda event: self.on_leave(box, name_text, roll_text, desc_text))

    def on_hover(self, box, name_text, roll_text, desc_text):
        self.canvas.itemconfig(box, fill="#E0E0E0")
        self.canvas.itemconfig(name_text, fill="#0000FF")
        self.canvas.itemconfig(roll_text, fill="#0000FF")
        self.canvas.itemconfig(desc_text, fill="#0000FF")

    def on_leave(self, box, name_text, roll_text, desc_text):
        self.canvas.itemconfig(box, fill="#FFFFFF")
        self.canvas.itemconfig(name_text, fill="#5E95FF")
        self.canvas.itemconfig(roll_text, fill="#5E95FF")
        self.canvas.itemconfig(desc_text, fill="#777777")

    def _create_rounded_rectangle(self, x1, y1, x2, y2, radius=25, **kwargs):
        points = [
            x1 + radius, y1,
            x1 + radius, y1,
            x2 - radius, y1,
            x2 - radius, y1,
            x2, y1,
            x2, y1 + radius,
            x2, y1 + radius,
            x2, y2 - radius,
            x2, y2 - radius,
            x2, y2,
            x2 - radius, y2,
            x2 - radius, y2,
            x1 + radius, y2,
            x1 + radius, y2,
            x1, y2,
            x1, y2 - radius,
            x1, y2 - radius,
            x1, y1 + radius,
            x1, y1 + radius,
            x1, y1
        ]

        return self.canvas.create_polygon(points, **kwargs, smooth=True)


Canvas.create_rounded_rectangle = About._create_rounded_rectangle