import tkinter as tk
from tkinter import ttk
import database
class PrincipalBD():
    def __init__(self, win):
       self.objetoBanco = database.AppBd()