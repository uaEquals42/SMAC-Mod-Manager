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
import time


TERRAN_KEY = "terran_Key"
TERRANX_KEY = "terranX_Key"
WF_KEY = "working_folder"
CONFIG = 'settings.ini'
SET = "SETTINGS"
EXCLUDED_FILES = [".tmp", ".dll", ".sys",".Ini"]
EXCLUDED_FOLDERS = ["saves", "Color Blind Palette"]

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
		str_var_inactive_mods = tk.StringVar(value=tuple(self.get_list_of_mods())) #TODO: Have this load from memory
		self.tklist_available_mods = tk.Listbox(frameMods, height=20, listvariable=str_var_inactive_mods)
		self.tklist_available_mods.grid(column=0, row=1, sticky="N,W,E,S")
		scroll_in_mods = ttk.Scrollbar(frameMods, orient="vertical", command=self.tklist_available_mods.yview)
		scroll_in_mods.grid(column=1, row=1, sticky="N,S")
		self.tklist_available_mods['yscrollcommand'] = scroll_in_mods.set
		
		
			
		label_ac_mods = ttk.Label(frameMods, text='Active mods:')
		label_ac_mods.grid(column=4, row=0)
		self.str_var_active_mods = tk.StringVar(value=tuple([])) #TODO: Have this load from memory
		self.tklist_active_mods = tk.Listbox(frameMods, height=20, listvariable=self.str_var_active_mods)
		self.tklist_active_mods.grid(column=4, row=1, sticky="N,W,E,S")
		scroll_ac_mods = ttk.Scrollbar(frameMods, orient="vertical", command=self.tklist_active_mods.yview)
		scroll_ac_mods.grid(column=5, row=1, sticky="N,S")
		self.tklist_active_mods['yscrollcommand'] = scroll_ac_mods.set
		
		
		frame_leftrightbuttons = ttk.Frame(frameMods)
		frame_leftrightbuttons.rowconfigure(3,minsize=20)
		frame_leftrightbuttons.grid(column=3, row=1, padx=10)
		button_left = ttk.Button(frame_leftrightbuttons, text='<', command=lambda: self.move_rightleft(self.tklist_active_mods,self.tklist_available_mods))
		button_right = ttk.Button(frame_leftrightbuttons, text='>', command=lambda: self.move_rightleft(self.tklist_available_mods,self.tklist_active_mods))
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
		
		button_apply = ttk.Button(frameLaunchers, text='Force update', command=lambda: self.apply_mods(True))
		button_SMAC = ttk.Button(frameLaunchers, text='Alpha Centauri', command=lambda: self.start_game(self.str_terran.get()))
		button_SMACX = ttk.Button(frameLaunchers, text='Alien Crossfire', command=lambda: self.start_game(self.str_terranx.get()))
		button_apply.grid(column=0, row=0)
		label_launch.grid(column=1, row=0,pady=5)
		button_SMAC.grid(column=2, row=0,padx=10)
		button_SMACX.grid(column=3, row=0)
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
	
	def move_rightleft(self, list_from, list_to):
		activate = list_from.curselection()
		for modnum in activate:
			modnamelist = list_from.get(modnum)
			list_to.insert('end',modnamelist)
			list_from.selection_clear(modnum)
			list_from.delete(modnum)
		
	def set_terran(self, key, string):
		value = filedialog.askopenfilename()
		self.config[SET][key]=value
		string.set(value)	
		self.save_settings()
		
	def get_list_of_mods(self):
		return os.listdir("./mods/")
	
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

		
		logging.info("Copy to backup folder")
		for dirname, dirnames, files in os.walk(self.config[SET][WF_KEY]):
			#ok remove folders we don't go into
			for rem_f in EXCLUDED_FOLDERS:
				if rem_f in dirnames:
					dirnames.remove(rem_f)
			
			for file in files:
				if path.splitext(file)[1] not in EXCLUDED_FILES:
					file_path = path.join(dirname, file)
					logging.debug(file_path)
					destination = path.join("./backup", path.relpath(path.join(dirname, file), self.config[SET][WF_KEY]))
					self.create_folder(destination)
					shutil.copy2(file_path, destination)
					

	def apply_mods(self, force):
		
		dict_files_to_copy = {} # File relative path : File to copy path
		dict_files_to_copy = self.get_file_dict("./backup", dict_files_to_copy)
		# Get list of mods to apply
		enabledmods = []
		for i in range(0, self.tklist_active_mods.size()):
			enabledmods.append(self.tklist_active_mods.get(i))
		#enabledmods = self.str_var_active_mods.get().translate(test).split(",") #WARNING: WIll leave an empty set in list.
		logging.debug(enabledmods)
		for ap_mods in enabledmods:
			if ap_mods != '':
				dict_files_to_copy = self.get_file_dict(path.join("./mods", ap_mods), dict_files_to_copy)
		
	
		# Then copy files back

		logging.info("Start Copying")
		start_time = time.time()
		

		for key, item in dict_files_to_copy.items():
			destination = path.join(self.config[SET][WF_KEY], key)
			
			
			if force or os.stat(item).st_mtime != os.stat(destination).st_mtime: # not perfect solution, but should be pretty good.
				logging.info(item + " to " + destination)
				shutil.copy2(item, destination)
		elapsed_time = time.time() - start_time
		logging.info("End copying. Time took " +str(elapsed_time))
	
	def get_file_dict(self, directory, dict_files_to_copy):
		for dirname, dirnames, files in os.walk(directory):
			#ok remove folders we don't go into
			for rem_f in EXCLUDED_FOLDERS:
				if rem_f in dirnames:
					dirnames.remove(rem_f)
			
			for file in files:
				if path.splitext(file)[1] not in EXCLUDED_FILES:
					file_path = path.join(dirname, file)
					relative_path = path.relpath(path.join(dirname, file), directory)
					dict_files_to_copy[relative_path] = file_path
					
					logging.debug(relative_path + " : " + file_path)
					
		
		return dict_files_to_copy	
			
	def start_game(self, gamelocation):
		self.apply_mods(False)
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

