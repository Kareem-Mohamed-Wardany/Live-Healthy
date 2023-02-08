from tkinter import messagebox
import customtkinter as ctk


def MessageBox(parent, type, Text):

    if type == "error":
        messagebox.showerror("Error", Text, icon="error", parent=parent)
    elif type == "info":
        messagebox.showinfo("Info", Text, icon="info", parent=parent)
    elif type == "question":
        messagebox.askyesno("Question", Text, icon="question", parent=parent)
    elif type == "warning":
        messagebox.showwarning("Warning", Text, icon="warning", parent=parent)


# function to let any window be in the center of the screen
def center(win, w, h):
    """
    centers a tkinter window
    :param win: the main window or Toplevel window to center
    """
    ws = win.winfo_screenwidth()
    hs = win.winfo_screenheight()
    x = (ws/2) - (w/2)
    y = (hs/2) - (h/2)

    win.geometry('%dx%d+%d+%d' % (w, h, x, y))
    # win.update_idletasks()
    # width = win.winfo_width()
    # frm_width = win.winfo_rootx() - win.winfo_x()
    # win_width = width + 2 * frm_width
    # height = win.winfo_height()
    # titlebar_height = win.winfo_rooty() - win.winfo_y()
    # win_height = height + titlebar_height + frm_width
    # x = win.winfo_screenwidth() // 2 - win_width // 2
    # y = win.winfo_screenheight() // 2 - win_height // 2
    # win.geometry(f"{width}x{height}+{x}+{y}")
    # win.deiconify()


# Class for scrollabe frame
class ScrollableFrame(ctk.CTkFrame):
    def __init__(
        self, container, bgcolor, height=200, width=200, scrollafter=5, *args, **kwargs
    ):
        self.ScrollAfter = scrollafter
        super().__init__(container, *args, **kwargs)
        self.canvas = ctk.CTkCanvas(
            self, height=height, width=width, background=bgcolor
        )
        self.canvas.bind("<Enter>", self._bound_to_mousewheel)
        self.canvas.bind("<Leave>", self._unbound_to_mousewheel)
        self.scrollbar = ctk.CTkScrollbar(
            self,
            fg_color="transparent",
            bg_color="transparent",
            command=self.canvas.yview,
        )
        self.scrollable_frame = ctk.CTkFrame(
            self.canvas, fg_color="transparent", bg_color="transparent", width=width
        )

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")),
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")

        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.canvas.pack(side="left", fill="both", expand=True)

    def ShowScrollbar(self):
        if (
            len(self.scrollable_frame.winfo_children()) > self.ScrollAfter
        ):  # show scrollbar when needed
            self.scrollbar.pack(side="right", fill="y")

    def _bound_to_mousewheel(self, event):
        self.ShowScrollbar()
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)

    def _unbound_to_mousewheel(self, event):
        self.canvas.unbind_all("<MouseWheel>")

    def _on_mousewheel(self, event):
        if (
            len(self.scrollable_frame.winfo_children()) > self.ScrollAfter
        ):  # disable Scroll Wheel when items is less than ScrollAfter
            self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
