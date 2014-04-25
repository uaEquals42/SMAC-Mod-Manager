'''
Created on Apr 24, 2014

@author: Gregory
'''
import subprocess
import logging
from tkinter import filedialog
import tkinter as tk
from tkinter import ttk

"""
filename = filedialog.askopenfilename()
subprocess.call(filename, shell=True)

"""

class app():
	def __init__(self):
		self.root = tk.Tk()
		self.root.title("SMAC/SMACX Mod Manager")
		self.root.option_add('*tearOff', tk.FALSE)
		self.root.columnconfigure(0, weight=1)
		self.root.rowconfigure(0, weight=1)
		
		noteTabs = ttk.Notebook(self.root)
		frameMods = ttk.Frame(noteTabs); # first page, which would get widgets gridded into it
		frameMods.columnconfigure(0, weight=1)
		frameMods.columnconfigure(4, weight=1)
		frameMods.rowconfigure(1, weight=1)
		
		
		frameOptions = ttk.Frame(noteTabs) 
		frameOptions.columnconfigure(1, weight=1)
		noteTabs.add(frameMods, text='Mods')
		noteTabs.add(frameOptions, text='Options')
		
		noteTabs.grid(column=0, row=0, sticky="N, S, E, W")
		
		
		frameLaunchers = ttk.Frame(self.root)
		label_launch = ttk.Label(frameLaunchers, text='Start:')
		label_launch.grid(column=0, row=0,pady=5)
		button_SMAC = ttk.Button(frameLaunchers, text='Alpha Centauri', command=lambda: print("SMAC!"))
		button_SMACX = ttk.Button(frameLaunchers, text='Alien Crossfire', command=lambda: print("SMACX!"))
		button_SMAC.grid(column=1, row=0,padx=10)
		button_SMACX.grid(column=2, row=0)
		frameLaunchers.grid(column=0, row=1, sticky="S, E")
		
		label_in_mods = ttk.Label(frameMods, text='Inactive mods:')
		label_in_mods.grid(column=0, row=0)
		list_available_mods = tk.Listbox(frameMods, height=20)
		list_available_mods.grid(column=0, row=1, sticky="N,W,E,S")
		scroll_in_mods = ttk.Scrollbar(frameMods, orient="vertical", command=list_available_mods.yview)
		scroll_in_mods.grid(column=1, row=1, sticky="N,S")
		list_available_mods['yscrollcommand'] = scroll_in_mods.set
		for i in range(1,101):
			list_available_mods.insert('end', 'Line %d of 100' % i)
			
		label_ac_mods = ttk.Label(frameMods, text='Active mods:')
		label_ac_mods.grid(column=4, row=0)
		list_active_mods = tk.Listbox(frameMods, height=20)
		list_active_mods.grid(column=4, row=1, sticky="N,W,E,S")
		scroll_ac_mods = ttk.Scrollbar(frameMods, orient="vertical", command=list_active_mods.yview)
		scroll_ac_mods.grid(column=5, row=1, sticky="N,S")
		list_active_mods['yscrollcommand'] = scroll_ac_mods.set
		for i in range(1,101):
			list_active_mods.insert('end', 'Line %d of 100' % i)
		
		frame_leftrightbuttons = ttk.Frame(frameMods)
		frame_leftrightbuttons.rowconfigure(3,minsize=20)
		frame_leftrightbuttons.grid(column=3, row=1, padx=10)
		button_left = ttk.Button(frame_leftrightbuttons, text='<', command=lambda: print("Left!"))
		button_right = ttk.Button(frame_leftrightbuttons, text='>', command=lambda: print("Right!"))
		button_up = ttk.Button(frame_leftrightbuttons, text='/\\', command=lambda: print("Up!"))
		button_down = ttk.Button(frame_leftrightbuttons, text='\\/', command=lambda: print("Down!"))
		button_left.grid(column=0, row=1)
		button_right.grid(column=0, row=2)
		button_up.grid(column=0, row=4)
		button_down.grid(column=0, row=5)
		
		#Options Tab
		label_terran = ttk.Label(frameOptions, text='terran.exe:')
		label_terranx= ttk.Label(frameOptions, text='terranx.exe:')
		label_folder = ttk.Label(frameOptions, text='Alpha Centarui Folder:')
		str_terran = tk.StringVar()
		entry_terran = ttk.Entry(frameOptions, textvariable=str_terran)
		button_get_smac = ttk.Button(frameOptions, text='Find', command=lambda: print("Find SMAC!"))
		
		str_terranx = tk.StringVar()
		entry_terranx = ttk.Entry(frameOptions, textvariable=str_terranx)
		button_get_smacx = ttk.Button(frameOptions, text='Find', command=lambda: print("Find SMACx!"))
		
		label_folder_location = ttk.Label(frameOptions, text='Unknown')
		button_get_folder = ttk.Button(frameOptions, text='Find', command=lambda: print("Find!"))
		
		label_terran.grid(column=0, row=1)
		entry_terran.grid(column=1, row=1,sticky="W,E",padx=10)
		button_get_smac.grid(column=2, row=1)
		label_terranx.grid(column=0, row=2)
		entry_terranx.grid(column=1, row=2,sticky="W,E",padx=10)
		button_get_smacx.grid(column=2, row=2)
		label_folder.grid(column=0, row=3)
		label_folder_location.grid(column=1, row=3,sticky="W,E",padx=10)
		button_get_folder.grid(column=2, row=3)
		# Start the window
		self.root.mainloop()

app()

