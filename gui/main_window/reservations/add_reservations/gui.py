from pathlib import Path
from tkinter import Frame, Canvas, Entry, Button, PhotoImage, messagebox, ttk
from tkcalendar import DateEntry
import controller as db_controller
import datetime

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path("./assets")

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

def get_occupied_rooms():
    """
    Retrieve the list of room numbers that are currently occupied (i.e., where check_out is NULL).
    """
    cmd = "SELECT rooms.room_no FROM rooms JOIN reservations ON rooms.id = reservations.r_id WHERE reservations.check_out IS NULL;"
    db_controller.cursor.execute(cmd)
    
    occupied_rooms = db_controller.cursor.fetchall()
    
    # Return a list of room numbers jo occupied hai
    return [int(room[0]) for room in occupied_rooms]

class AddReservations(Frame):
    def __init__(self, parent, controller=None, *args, **kwargs):
        Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.data = {"g_id": "", "check_in": "", "meal": "", "r_id": "", "booked_rooms": ""}

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
        self.entry_image_1 = PhotoImage(file=relative_to_assets("entry_1.png"))
        entry_bg_1 = self.canvas.create_image(137.5, 153.0, image=self.entry_image_1)

        self.canvas.create_text(
            52.0,
            128.0,
            anchor="nw",
            text="Guest Id",
            fill="#5E95FF",
            font=("Montserrat Bold", 14 * -1),
        )

        self.entry_image_2 = PhotoImage(file=relative_to_assets("entry_2.png"))
        entry_bg_2 = self.canvas.create_image(141.5, 165.0, image=self.entry_image_2)
        entry_2 = Entry(
            self,
            bd=0,
            bg="#EFEFEF",
            highlightthickness=0,
            font=("Montserrat Bold", 18 * -1),
            foreground="#777777",
        )
        entry_2.place(x=52.0, y=153.0, width=179.0, height=22.0)
        self.data["g_id"] = entry_2

        self.entry_image_3 = PhotoImage(file=relative_to_assets("entry_3.png"))
        entry_bg_3 = self.canvas.create_image(137.5, 259.0, image=self.entry_image_3)

        self.canvas.create_text(
            52.0,
            234.0,
            anchor="nw",
            text="Is Taking Meal",
            fill="#5E95FF",
            font=("Montserrat Bold", 14 * -1),
        )

        self.entry_image_4 = PhotoImage(file=relative_to_assets("entry_4.png"))
        entry_bg_4 = self.canvas.create_image(141.5, 271.0, image=self.entry_image_4)
        entry_4 = Entry(
            self,
            bd=0,
            bg="#EFEFEF",
            highlightthickness=0,
            font=("Montserrat Bold", 18 * -1),
            foreground="#777777",
        )
        entry_4.place(x=52.0, y=259.0, width=179.0, height=22.0)
        self.data["r_id"] = entry_4

        self.entry_image_5 = PhotoImage(file=relative_to_assets("entry_5.png"))
        entry_bg_5 = self.canvas.create_image(378.5, 153.0, image=self.entry_image_5)

        self.canvas.create_text(
            293.0,
            128.0,
            anchor="nw",
            text="Room Id",
            fill="#5E95FF",
            font=("Montserrat Bold", 14 * -1),
        )

        self.entry_image_6 = PhotoImage(file=relative_to_assets("entry_6.png"))
        entry_bg_6 = self.canvas.create_image(382.5, 165.0, image=self.entry_image_6)
        entry_6 = Entry(
            self,
            bd=0,
            bg="#EFEFEF",
            highlightthickness=0,
            foreground="#777777",
            font=("Montserrat Bold", 18 * -1),
        )
        entry_6.place(x=293.0, y=153.0, width=179.0, height=22.0)
        self.data["meal"] = entry_6

        self.entry_image_7 = PhotoImage(file=relative_to_assets("entry_7.png"))
        entry_bg_7 = self.canvas.create_image(378.5, 259.0, image=self.entry_image_7)

        self.canvas.create_text(
            293.0,
            234.0,
            anchor="nw",
            text="Check-in Time",
            fill="#5E95FF",
            font=("Montserrat Bold", 14 * -1),
        )

        self.entry_image_8 = PhotoImage(file=relative_to_assets("entry_8.png"))
        entry_bg_8 = self.canvas.create_image(382.5, 271.0, image=self.entry_image_8)

        # Calendar for Date
        self.calendar = DateEntry(
            self,
            bd=0,
            bg="#EFEFEF",
            highlightthickness=0,
            foreground="#777777",
            font=("Montserrat Bold", 14 * -1),
            date_pattern="yyyy-mm-dd",
            mindate=datetime.date.today()
        )
        self.calendar.place(x=280.0, y=259.0, width=120.0, height=22.0)

        # Time Selector (Hours and Minutes)
        self.time_hour = ttk.Combobox(self, width=2, values=[f'{i:02}' for i in range(24)])
        self.time_hour.place(x=400.0, y=259.0, width=40.0, height=22.0)
        self.time_hour.current(0)  # set default value

        self.time_minute = ttk.Combobox(self, width=2, values=[f'{i:02}' for i in range(60)])
        self.time_minute.place(x=438.0, y=259.0, width=40.0, height=22.0)
        self.time_minute.current(0)  # set default value

        # Removed seconds combobox and set seconds as "00" by default
        self.data["check_in"] = (self.calendar, self.time_hour, self.time_minute)

        self.button_image_1 = PhotoImage(file=relative_to_assets("button_1.png"))
        button_1 = Button(
            self,
            image=self.button_image_1,
            borderwidth=0,
            highlightthickness=0,
            command=self.save,
            relief="flat",
        )
        button_1.place(x=164.0, y=322.0, width=190.0, height=48.0)

        self.canvas.create_text(
            139.0,
            59.0,
            anchor="nw",
            text="Add a Reservation",
            fill="#5E95FF",
            font=("Montserrat Bold", 26 * -1),
        )

        self.canvas.create_text(
            549.0,
            59.0,
            anchor="nw",
            text="Operations",
            fill="#5E95FF",
            font=("Montserrat Bold", 26 * -1),
        )

        self.canvas.create_rectangle(
            515.0, 59.0, 517.0, 370.0, fill="#EFEFEF", outline=""
        )

        self.button_image_2 = PhotoImage(file=relative_to_assets("button_2.png"))
        button_2 = Button(
            self,
            image=self.button_image_2,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: self.parent.navigate("view"),
            relief="flat",
        )
        button_2.place(x=547.0, y=116.0, width=209.0, height=74.0)

        self.button_image_3 = PhotoImage(file=relative_to_assets("button_3.png"))
        button_3 = Button(
            self,
            image=self.button_image_3,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: self.parent.navigate("edit"),
            relief="flat",
        )
        button_3.place(x=547.0, y=210.0, width=209.0, height=74.0)

        # Add a dropdown list booked room IDs ka
        self.canvas.create_text(
            550.0,
            310.0,
            anchor="nw",
            text="View Booked Rooms:",
            fill="#5E95FF",
            font=("Montserrat Bold", 14 * -1),
        )

        self.combobox_booked_rooms = ttk.Combobox(
            self,
            values=self.get_booked_rooms()  # This function is called to display the list of booked rooms
        )
        self.combobox_booked_rooms.place(x=550.0, y=335.0, width=179.0, height=22.0)
        self.data["booked_rooms"] = self.combobox_booked_rooms

        # Add a text entry widget to filter the combobox
        self.filter_entry = Entry(self)
        self.filter_entry.place(x=550.0, y=360.0, width=179.0, height=22.0)
        self.filter_entry.bind("<KeyRelease>", self.update_combobox)
        self.filter_entry.bind("<FocusIn>", self.on_focus_in)
        self.filter_entry.bind("<FocusOut>", self.on_focus_out)

        self.placeholder_text = "Or type here to check.."
        self.set_placeholder()

    def set_placeholder(self):
        self.filter_entry.insert(0, self.placeholder_text)
        self.filter_entry.config(fg='grey')

    def on_focus_in(self, event):
        if self.filter_entry.get() == self.placeholder_text:
            self.filter_entry.delete(0, 'end')
            self.filter_entry.config(fg='black')

    def on_focus_out(self, event):
        if not self.filter_entry.get():
            self.set_placeholder()

    def refresh_booked_rooms(self):

        self.combobox_booked_rooms['values'] = self.get_booked_rooms()

    def update_combobox(self, event):
        filter_text = self.filter_entry.get()
        filtered_rooms = [room for room in self.get_booked_rooms() if filter_text in room]
        self.combobox_booked_rooms['values'] = filtered_rooms
        if filter_text in filtered_rooms:
            self.combobox_booked_rooms.set(filter_text)

    def get_datetime(self):
        # Combine date and time components into a single string
        date = self.data["check_in"][0].get_date()
        hour = self.data["check_in"][1].get()
        minute = self.data["check_in"][2].get()

        return f"{date} {hour}:{minute}:00"  # seconds default to "00"

    def get_booked_rooms(self):

        occupied_rooms = get_occupied_rooms()
        return [str(room) for room in occupied_rooms]

    # Save the data to the database
    def save(self):
        # Check if any fields are empty
        for label in ["g_id", "meal", "r_id"]:
            if self.data[label].get() == "":
                messagebox.showinfo("Error", "Please fill in all the fields")
                return

        check_in_time = self.get_datetime()

        # Save the reservation
        result = db_controller.add_reservation(
            self.data["g_id"].get(),
            self.data["meal"].get(),
            self.data["r_id"].get(),
            check_in_time
        )

        if result:
            messagebox.showinfo("Success", "Reservation added successfully")
            self.parent.navigate("view")
            self.parent.refresh_entries()

            # Refresh booked rooms dropdown
            self.refresh_booked_rooms()

            # Clear all fields
            for label in ["g_id", "meal", "r_id"]:
                self.data[label].delete(0, "end")
        else:
            messagebox.showerror(
                "Error",
                "Unable to add reservation. Please make sure the data is validated",
            )
