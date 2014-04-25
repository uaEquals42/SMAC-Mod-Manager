'''
Created on Apr 24, 2014

@author: Gregory
'''
import subprocess
import logging
from tkinter import filedialog, messagebox
import tkinter as tk
from tkinter import ttk
from os import path
import configparser
import os
import shutil


"""
filename = filedialog.askopenfilename()
subprocess.Popen(r'c:\mytool\tool.exe', cwd=r'd:\test\local')

"""

TERRAN_KEY = "terran_Key"
TERRANX_KEY = "terranX_Key"
WF_KEY = "working_folder"
CONFIG = 'settings.ini'
SET = "SETTINGS"

logging.basicConfig(level=logging.DEBUG)
class app():
	def __init__(self):
		logging.info("start program")
		self.config = configparser.ConfigParser()
		self.config[SET]={}

		self.config.read(CONFIG)
		
	
		
		
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
		
		self.str_terran = tk.StringVar()
		self.str_terran.set(self.config[SET].get(TERRAN_KEY, " "))
		entry_terran = ttk.Entry(frameOptions, textvariable=self.str_terran)
		button_get_smac = ttk.Button(frameOptions, text='Find', command=lambda: self.set_terran(TERRAN_KEY, self.str_terran) )
		
		self.str_terranx = tk.StringVar()
		self.str_terranx.set(self.config[SET].get(TERRANX_KEY, " "))
		entry_terranx = ttk.Entry(frameOptions, textvariable=self.str_terranx)
		button_get_smacx = ttk.Button(frameOptions, text='Find', command=lambda: self.set_terran(TERRANX_KEY,self.str_terranx))
		
		
		label_folder_location = ttk.Label(frameOptions, text=self.config[SET].get(WF_KEY, "Unknown"))
		
		button_get_folder = ttk.Button(frameOptions, text='Find', command=lambda: self.set_directory(label_folder_location))
		
		label_terran.grid(column=0, row=1)
		entry_terran.grid(column=1, row=1,sticky="W,E",padx=10)
		button_get_smac.grid(column=2, row=1)
		label_terranx.grid(column=0, row=2)
		entry_terranx.grid(column=1, row=2,sticky="W,E",padx=10)
		button_get_smacx.grid(column=2, row=2)
		label_folder.grid(column=0, row=3)
		label_folder_location.grid(column=1, row=3,sticky="W,E",padx=10)
		button_get_folder.grid(column=2, row=3)
		
		# Launch Game area
		frameLaunchers = ttk.Frame(self.root)
		label_launch = ttk.Label(frameLaunchers, text='Start:')
		label_launch.grid(column=0, row=0,pady=5)
		button_SMAC = ttk.Button(frameLaunchers, text='Alpha Centauri', command=lambda: self.start_game(self.str_terran.get()))
		button_SMACX = ttk.Button(frameLaunchers, text='Alien Crossfire', command=lambda: self.start_game(self.str_terranx.get()))
		button_SMAC.grid(column=1, row=0,padx=10)
		button_SMACX.grid(column=2, row=0)
		frameLaunchers.grid(column=0, row=1, sticky="S, E")
		
		# Start the window
		self.root.mainloop()

	def set_directory(self, label):
		#TODO: have it check to see if directory location is valid.
		#TODO: if there is already a directory set, or exe location set... default to their locations.
		tmp = filedialog.askdirectory(initialdir=self.config[SET].get(WF_KEY, path.expanduser("~")))
		if tmp != "":
			self.config[SET][WF_KEY] = tmp
			self.save_settings()
			label.configure(text=self.config[SET][WF_KEY])
		
			#TODO: Popup asking to make backup folder.  Y/N
			answer = messagebox.askyesno(message='Copy contents of \n'+tmp+'\n to \n' + path.abspath("./backup")+"\n\n\nIt is required to have an unaltered copy of SMAC/X in the backup folder",icon='question', title='Install')
			
			if answer:
				logging.info("Save to backupfolder")
				self.make_backup_folder()
				logging.info("Finished")
	
	def set_terran(self, key, string):
		value = filedialog.askopenfilename()
		self.config[SET][key]=value
		string.set(value)	
		self.save_settings()
		
	
	def save_settings(self):
		logging.info("Saving settings")
		self.config[SET][TERRAN_KEY] = self.str_terran.get()
		self.config[SET][TERRANX_KEY] = self.str_terranx.get()
		
		
		with open(CONFIG, 'w') as configfile:
			self.config.write(configfile)
	
	
	def create_folder(self, location):
		direct = path.dirname(location)
		if not path.exists(direct):
			logging.debug("Create backup folder")
			os.makedirs(direct)
	
	def make_backup_folder(self):
		# See if backupfolder exists, if not, make it and copy all the modable filetypes.
		
		# Ignore .tmp, .dll /saves /Color Blind Palette for backup folder.
		# Autoconvert color blind into a mod.
		fileexcludes = [".tmp", ".dll", ".sys"]
		folders_skip = ["saves", "Color Blind Palette"]
		
		logging.info("Copy to backup folder")
		for dirname, dirnames, files in os.walk(self.config[SET][WF_KEY]):
			#ok remove folders we don't go into
			for rem_f in folders_skip:
				if rem_f in dirnames:
					dirnames.remove(rem_f)
			
			for file in files:
				if path.splitext(file)[1] not in fileexcludes:
					file_path = path.join(dirname, file)
					logging.debug(file_path)
					destination = path.join("./backup", path.relpath(path.join(dirname, file), self.config[SET][WF_KEY]))
					self.create_folder(destination)
					shutil.copyfile(file_path, destination)
					

		
		
		
			
	def start_game(self, gamelocation):
		print("start the game")
		self.save_settings()	
		# Check to see if folderlocation is valid.
		print()
		if path.isdir(self.config[SET].get(WF_KEY, "\n\n\n\n\n\n\n\n\n\n\n")):
			# TODO: put in try catch block here.
			subprocess.Popen(gamelocation, cwd=self.config[SET][WF_KEY])
		else:
			logging.warning("Invalid directory location")
app()

