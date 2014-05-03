'''
Created on Apr 24, 2014
Copyright (C) 2014 Gregory Jordan

This program is free software; you can redistribute it and/or modify it under
the terms of the GNU General Public License as published by the Free Software
Foundation; either version 2 of the License, or (at your option) any later
version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY
WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A
PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with
this program; if not, write to the Free Software Foundation, Inc., 59 Temple
Place, Suite 330, Boston, MA 02111-1307 USA 

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
import sys
import traceback
import winreg


WINE = "WINE"
WF_KEY = "working_folder"
CONFIG = 'settings.ini'
SET = "SETTINGS"
SET2 = "ACTIVE_MODS"
EXCLUDED_FILES = [".tmp", ".dll", ".sys",".Ini"]
EXCLUDED_FOLDERS = ["saves", "Color Blind Palette"]
TERRAN = "terran.exe"
TERRANX = "terranx.exe"

#logging.basicConfig(filename="debug.txt",level=logging.DEBUG)
logging.basicConfig(level=logging.DEBUG)
class app():
	def __init__(self):
		logging.info("start program")
		self.config = configparser.ConfigParser()
		self.config[SET]={}
		self.config[SET2]={}
		self.config.read(CONFIG)

		
		
		self.root = tk.Tk()
		self.root.title("SMAC/SMACX Mod Manager")
		self.root.option_add('*tearOff', tk.FALSE)
		self.root.columnconfigure(0, weight=1)
		self.root.rowconfigure(0, weight=1)
		
		# Create the tabs.
		noteTabs = ttk.Notebook(self.root)
		
		frameMods = ttk.Frame(noteTabs); # first page, which would get widgets gridded into it
		frameMods.columnconfigure(0, weight=1)
		frameMods.columnconfigure(4, weight=1)
		frameMods.rowconfigure(1, weight=1)
		
		# Options tab
		frameOptions = ttk.Frame(noteTabs) 
		frameOptions.columnconfigure(1, weight=1)
		# Display the tabs.
		noteTabs.add(frameMods, text='Mods')
		noteTabs.add(frameOptions, text='Options')
		noteTabs.grid(column=0, row=0, sticky="N, S, E, W")
		
		
		
		
		# In-active mods list gui stuff.
		label_in_mods = ttk.Label(frameMods, text='Inactive mods:')
		str_var_inactive_mods = tk.StringVar(value=self.get_tuple_of_inactivemods()) #TODO: Have this load from memory
		self.tklist_available_mods = tk.Listbox(frameMods, height=20, listvariable=str_var_inactive_mods)
		scroll_in_mods = ttk.Scrollbar(frameMods, orient="vertical", command=self.tklist_available_mods.yview)
		self.tklist_available_mods['yscrollcommand'] = scroll_in_mods.set
		scroll_in_mods.grid(column=1, row=1, sticky="N,S")
		self.tklist_available_mods.grid(column=0, row=1, sticky="N,W,E,S")
		label_in_mods.grid(column=0, row=0)
		
		
		
		
		# Active mods gui stuff.	
		label_ac_mods = ttk.Label(frameMods, text='Active mods:')
		str_var_active_mods = tk.StringVar(value=self.get_tuple_of_mods_used_last()) #TODO: Have this load from memory
		self.tklist_active_mods = tk.Listbox(frameMods, height=20, listvariable=str_var_active_mods)
		scroll_ac_mods = ttk.Scrollbar(frameMods, orient="vertical", command=self.tklist_active_mods.yview)
		self.tklist_active_mods['yscrollcommand'] = scroll_ac_mods.set
		label_ac_mods.grid(column=4, row=0)
		scroll_ac_mods.grid(column=5, row=1, sticky="N,S")
		self.tklist_active_mods.grid(column=4, row=1, sticky="N,W,E,S")
		
		
		# Middle area, up down left right buttons.
		frame_leftrightbuttons = ttk.Frame(frameMods)
		frame_leftrightbuttons.rowconfigure(3,minsize=20)
		frame_leftrightbuttons.grid(column=3, row=1, padx=10)
		button_left = ttk.Button(frame_leftrightbuttons, text='<', command=lambda: self.move_rightleft(self.tklist_active_mods,self.tklist_available_mods))
		button_right = ttk.Button(frame_leftrightbuttons, text='>', command=lambda: self.move_rightleft(self.tklist_available_mods,self.tklist_active_mods))
		button_up = ttk.Button(frame_leftrightbuttons, text='/\\', command=lambda: self.move_up())
		button_down = ttk.Button(frame_leftrightbuttons, text='\\/', command=lambda: self.move_down())
		button_left.grid(column=0, row=1)
		button_right.grid(column=0, row=2)
		button_up.grid(column=0, row=4)
		button_down.grid(column=0, row=5)
		
		#Options Tab
		label_wine = ttk.Label(frameOptions, text='Wine prefix:')
		
		label_folder = ttk.Label(frameOptions, text='Alpha Centarui Folder:')
		
	
		
		label_folder_location = ttk.Label(frameOptions, text=self.config[SET].get(WF_KEY, "Unknown"))
		
		button_get_folder = ttk.Button(frameOptions, text='Find', command=lambda: self.set_directory(label_folder_location))
		
	
		label_folder.grid(column=0, row=3)
		label_folder_location.grid(column=1, row=3,sticky="W,E",padx=10)
		button_get_folder.grid(column=2, row=3)
		
		# Launch Game area
		frameLaunchers = ttk.Frame(self.root)
		label_launch = ttk.Label(frameLaunchers, text='Start:')
		
		button_force = ttk.Button(frameLaunchers, text='Force (slow)', command=lambda: self.apply_mods(True))
		button_apply = ttk.Button(frameLaunchers, text='Apply', command=lambda: self.apply_mods(False))
		button_SMAC = ttk.Button(frameLaunchers, text='Alpha Centauri', command=lambda: self.start_game(TERRAN))
		button_SMACX = ttk.Button(frameLaunchers, text='Alien Crossfire', command=lambda: self.start_game(TERRANX))
		button_force.grid(column=0, row=0)
		button_apply.grid(column=1, row=0)
		label_launch.grid(column=2, row=0,pady=5)
		button_SMAC.grid(column=3, row=0,padx=10)
		button_SMACX.grid(column=4, row=0)
		frameLaunchers.grid(column=0, row=1, sticky="S, E")
		
		# Start the window
		self.root.mainloop()

	def set_directory(self, label):
		#TODO: have it check to see if directory location is valid.
		#TODO: if there is already a directory set, or exe location set... default to their locations.
		tmp = filedialog.askdirectory(initialdir=self.config[SET].get(WF_KEY, path.expanduser("~")))
		if tmp != "":
			# Then check to see if it contains the terran.exe in it.
			if path.exists(path.join(tmp,TERRAN)):
				self.config[SET][WF_KEY] = tmp
				self.save_settings()
				label.configure(text=self.config[SET][WF_KEY])
			
				#TODO: Popup asking to make backup folder.  Y/N
				answer = messagebox.askyesno(message='Copy contents of \n'+tmp+'\n to \n' + path.abspath("./backup")+"\n\n\nIt is required to have an unaltered copy of SMAC/X in the backup folder",icon='question', title='Install')
				
				if answer:
					logging.info("Save to backupfolder")
					self.make_backup_folder()
					logging.info("Finished")
			else:
				messagebox.showerror(title="Executable not found.", message="Could not find terran.exe in folder")
	
	def move_rightleft(self, list_from, list_to):
		activate = list_from.curselection()
		for modnum in activate:
			modnamelist = list_from.get(modnum)
			list_to.insert('end',modnamelist)
			list_from.selection_clear(modnum)
			list_from.delete(modnum)
		
	def get_tuple_of_mods_used_last(self):
		size = self.config[SET2]["Range"];
		tp = []
		modslist = self.get_list_of_mods()
		for i in range(0, int(size)):
			if self.config[SET2][str(i)] in modslist: #This is so that if the user uninstalls a mod we won't have problems.
				tp.append(self.config[SET2][str(i)])
		logging.info(tp)
		return tuple(tp)

	def get_tuple_of_inactivemods(self):
		modslist = self.get_list_of_mods()
		activemods = self.get_tuple_of_mods_used_last()
		for ii in activemods:
			modslist.remove(ii)
		return tuple(modslist)
		
	def get_list_of_mods(self):
		tmp = []
		for ii in os.listdir("./mods/"):
			if path.isdir("./mods/"+ii):
				tmp.append(ii)
		return tmp
	
	def save_settings(self):
		logging.info("Saving settings")
		self.config[SET2]={}
		self.config[SET2]["Range"] = str(self.tklist_active_mods.size())
		for i in range(0, self.tklist_active_mods.size()):
			self.config[SET2][str(i)] = self.tklist_active_mods.get(i)
		
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
		self.save_settings()
		dict_files_to_copy = {} # File relative path : File to copy path
		dict_files_to_copy = self.get_file_dict("./backup", dict_files_to_copy)
		# Get list of mods to apply
		enabledmods = []
		for i in range(0, self.tklist_active_mods.size()):
			enabledmods.append(self.tklist_active_mods.get(i))
		
		logging.debug(enabledmods)
		for ap_mods in enabledmods:	
			dict_files_to_copy = self.get_file_dict(path.join("./mods", ap_mods), dict_files_to_copy)
		
	
		# Then copy files back

		logging.info("Start Copying")
		start_time = time.time()
		

		for key, item in dict_files_to_copy.items():
			destination = path.join(self.config[SET][WF_KEY], key)
			
			# Need to check to see if file exists at destination
			if path.isfile(destination):
				if force or os.stat(item).st_mtime != os.stat(destination).st_mtime: # not perfect solution, but should be pretty good.
					logging.info(item + " to " + destination)
					shutil.copy2(item, destination)
			else: # If there is no file, copy anyway.
				logging.info(item + " to " + destination)
				shutil.copy2(item, destination)
		elapsed_time = time.time() - start_time
		logging.info("End copying. Time took " +str(elapsed_time))
		return dict_files_to_copy
	
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
	
	def move_up(self):
		logging.debug("Move up")
		listsize = self.tklist_active_mods.size()
		if listsize > 1: # If it is less than one, we don't need to do anything.
			location = self.tklist_active_mods.curselection()
			logging.debug(location)
			if location != ():
				num = location[0]
				if  num > 0: # if it is already on top, we don't need to move it up.
					olditem = self.tklist_active_mods.get(num-1)
					self.tklist_active_mods.delete(num-1)
					self.tklist_active_mods.insert(num, olditem)
	
	def move_down(self):
		logging.debug("Move down")
		location = self.tklist_active_mods.curselection()
		logging.debug(location)
		if location != ():
			num = location[0]
			listsize = self.tklist_active_mods.size()
			if num < listsize-1:	
				#if  num > 0: # if it is already on top, we don't need to move it up.
				currentitem = self.tklist_active_mods.get(num)
				self.tklist_active_mods.delete(num)
				self.tklist_active_mods.insert(num+1, currentitem)
				self.tklist_active_mods.select_set(num+1)
			
	def start_game(self, gamekey):
		dict_files_to_copy = self.apply_mods(False)
		logging.info("start the game")
		self.save_settings()	
		# Check to see if folderlocation is valid.
		
		if path.isdir(self.config[SET].get(WF_KEY, "\n\n\n\n\n\n\n\n\n\n\n")):
			# TODO: put in try catch block here.
			try:
				if(sys.platform=='win32'):
					subprocess.Popen(path.join(self.config[SET][WF_KEY],gamekey), cwd=self.config[SET][WF_KEY])
				if(sys.platform=='linux2'):
					subprocess.Popen("wine " + path.join(self.config[SET][WF_KEY],gamekey), cwd=self.config[SET][WF_KEY])
			except OSError:
				# ICK.  User is on windows an the executable is set to run as administrator.
				logging.warning(sys.exc_info()[1])
				for line in traceback.format_list(traceback.extract_tb(sys.exc_info()[2])):
					logging.warning(line)
				
				logging.info("Using workaround.")
				# Use workaround.
				game_location = dict_files_to_copy.get(gamekey)
					
				try:
					subprocess.Popen(game_location, cwd=self.config[SET][WF_KEY])
				except OSError:
					logging.warning("OSError error:", sys.exc_info()[0])
					logging.warning(sys.exc_info()[1])
					for line in traceback.format_list(traceback.extract_tb(sys.exc_info()[2])):
						logging.warning(line)
					messagebox.showerror(message="OSError: Exe is set to run as administrator.  Please uncheck the 'run as admin' in the exe properties.", title='OSError')
				except:
					logging.warning("Unexpected error:", sys.exc_info()[0])
					logging.warning(sys.exc_info()[1])
					for line in traceback.format_list(traceback.extract_tb(sys.exc_info()[2])):
						logging.warning(line)
					messagebox.showerror(message="Unknown Error", title='Error')
				else:
					logging.info("No.")
					
			except:
				logging.warning("Unexpected error:", sys.exc_info()[0])
				logging.warning(sys.exc_info()[1])
				for line in traceback.format_list(traceback.extract_tb(sys.exc_info()[2])):
					logging.warning(line)
				messagebox.showerror(message="Unknown Error", title='Error')

		else:
			logging.warning("Invalid directory location")
app()

