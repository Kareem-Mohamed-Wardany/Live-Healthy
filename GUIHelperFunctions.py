from tkinter import messagebox
import tkinter as tk
import customtkinter as ctk

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
    win.iconbitmap(default="asset\TitleImage.ico",)