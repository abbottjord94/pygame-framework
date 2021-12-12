import os
import sys
import json
import shutil
import random
from PyQt5 import QtCore, QtWidgets, QtGui
from mainwindow import Ui_MainWindow
from new_project import Ui_Dialog as Ui_NewProject
from new_scene import Ui_Dialog as Ui_NewScene
from about_dialog import Ui_Dialog as Ui_AboutDialog
from new_gameobject import Ui_Dialog as Ui_NewGameobject
from editor_settings import Ui_Dialog as Ui_EditorSettings

class PygameEditor(Ui_MainWindow):
	
	_has_active_project = False
	_has_active_scene = False
	_can_save = False
	_has_active_scene = False
	_has_active_object = False
	_current_project = ""
	_current_working_directory = ""
	_current_active_scene = ""
	_active_scene_state = {}
	_active_object = {}
	_selected_object = {}
	_heirarchy_objects = {}
	_project_state = {}
	_editor_settings = {}
	_preview_scene = None
	
	def __init__(self, dialog):
		Ui_MainWindow.__init__(self)
		self.setupUi(dialog)
		
		self.load_editor_settings()
		
		#Other stuff
		self.scene_list.clicked.connect(self.scenelist_clicked)
		self.object_list.clicked.connect(self.objectlist_clicked)
		self.object_heirarchy.clicked.connect(self.objectheirarchy_clicked)
		
		#Lower button group
		self.newscene_button.clicked.connect(self.new_scene)
		self.newgameobject_button.clicked.connect(self.new_gameobject)
		self.editgameobject_button.clicked.connect(self.edit_gameobject)
		self.deletegameobject_button.clicked.connect(self.delete_gameobject)
		self.deleteallgameobjects_button.clicked.connect(self.deleteall_gameobjects)
		self.editscenesettings_button.clicked.connect(self.edit_scene_settings)
		
		#File Menu
		self.actionNew_Project.triggered.connect(self.new_project)
		self.actionNew_Scene.triggered.connect(self.new_scene)
		self.actionOpen_Project.triggered.connect(self.open_project)
		self.actionNew_GameObject.triggered.connect(self.new_gameobject)
		self.actionSave_Scene.triggered.connect(self.save_scene)
		self.actionSave_Project.triggered.connect(self.save_project)
		self.actionExit.triggered.connect(self.exit_program)
		
		#Edit Menu
		self.actionScene_Settings.triggered.connect(self.edit_scene_settings)
		self.actionProject_Settings.triggered.connect(self.edit_project_settings)
		self.actionEditor_Settings.triggered.connect(self.edit_editor_settings)
		
		#Build Menu
		self.actionBuild.triggered.connect(self.build_project)
		self.actionBuild_Settings.triggered.connect(self.edit_build_settings)
		
		#View Menu
		
		
		#Tools Menu
		
		
		#Help Menu
		self.actionAbout.triggered.connect(self.show_about)
	
	
	#Help Menu functions
	def show_about(self):
		Dialog = QtWidgets.QDialog()
		ui = Ui_AboutDialog()
		ui.setupUi(Dialog)
		Dialog.show()
		Dialog.exec_()
	
	
	#Build Menu functions
	def build_project(self):
		self.save_project()
		
		template_files_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), "template_files")
		scenemanager_template_dir = os.path.join(template_files_dir, "scene_manager.temp.py")
		scenemanager_template = open(scenemanager_template_dir, "r").read()
		
		import_list = ""
		object_types_dict = "_object_types = {"
		first_scene = "\"" + self._current_active_scene + ".json\""
		
		for object in self._project_state["object_types"]:
			import_list += "from " + object + " import " + object + "\n"
			object_types_dict += "\"" + object + "\"" + ": " + object + ", "
		
		object_types_dict = object_types_dict[:-2]
		object_types_dict += "}"
		
		scenemanager_template = scenemanager_template.replace("($IMPORT_LIST)", import_list)
		scenemanager_template = scenemanager_template.replace("($OBJECT_TYPE_DICT)", object_types_dict)
		scenemanager_template = scenemanager_template.replace("($FIRST_SCENE_NAME)", first_scene)
		
		scenemanager_output = open(os.path.join(self._project_state["project_directory"], "scene_manager.py"), "w+")
		scenemanager_output.write(scenemanager_template)
		scenemanager_output.close()
		
		settingsfile_output = open(os.path.join(self._project_state["project_directory"], "settings.json"), "w+")
		settingsfile_output.write("{\"game\":{\"title\": \"" + self._project_state["project_settings"]["game_title"] + "\" ,\"window_x\": " + str(self._project_state["project_settings"]["window_x"]) + ",\"window_y\": " + str(self._project_state["project_settings"]["window_y"]) + ",\"max_framerate\": " + str(self._project_state["project_settings"]["tps"]) + "}}")
		
		settingsfile_output.close()
	
	def edit_build_settings(self):
		pass
	
	
	#Edit menu functions
	def edit_project_settings(self):
		pass
	
	def edit_editor_settings(self):
		Dialog = QtWidgets.QDialog()
		ui = Ui_EditorSettings()
		ui.setupUi(Dialog)
		Dialog.show()
		result = Dialog.exec_()
			
		if(result == QtWidgets.QDialog.Accepted):
			editor_path = ui.editor_path.text()
			self._editor_settings["code_editor"] = editor_path
			self.save_editor_settings()
	
	#File Menu functions
	def new_project(self):
	
		#Ask the user if they want to save before starting a new project
		if self._has_active_project:
			self.prompt_save()
		
		#If no project is active, no need to ask the user to save
		
		Dialog = QtWidgets.QDialog()
		ui = Ui_NewProject()
		ui.setupUi(Dialog)
		Dialog.show()
		result = Dialog.exec_()
			
		if(result == QtWidgets.QDialog.Accepted):
			
			try:
				#Clear the object and scene list
				self.object_list.clear()
				self.scene_list.clear()
				self.scene_preview.setScene(None)
			
				#Grab the form data
				_project_name = ui.project_name.text()
				_project_dir = ui.project_directory.text()
				_project_settings = {
					"window_x": int(ui.window_x.text()),
					"window_y": int(ui.window_y.text()),
					"tps": int(ui.ticks_per_second.text()),
					"game_title": ui.game_title.text()
				}
				
				#Set the new project state
				self._current_project = _project_name
				self._project_state["project_name"] = _project_name
				self._project_state["scenes"] = []
				self._project_state["object_types"] = {}
				self._project_state["project_settings"] = _project_settings
				
				#Create the project directories, project file, and copy template files
				rootdir = os.path.join(_project_dir, _project_name)
				os.mkdir(rootdir)
				os.mkdir(os.path.join(rootdir, "scenes"))
				os.mkdir(os.path.join(rootdir, "assets"))
				self._project_state["project_directory"] = rootdir
				
				project_file = open(os.path.join(rootdir, _project_name + ".json"), "w+")
				project_file.write(json.dumps(self._project_state))
				project_file.close()
				
				template_files_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), "template_files")
				shutil.copyfile(os.path.join(template_files_dir, "game.py"), os.path.join(rootdir, "game.py"))
				shutil.copyfile(os.path.join(template_files_dir, "app.py"), os.path.join(rootdir, "app.py"))
				shutil.copyfile(os.path.join(template_files_dir, "game_object.py"), os.path.join(rootdir, "game_object.py"))
				
				#Set the active project flag and enable the window components
				self._has_active_project = True
				self.unlock_components()
				self.scene_preview.setSceneRect(QtCore.QRectF(0.0, 0.0, _project_settings["window_x"], _project_settings["window_y"]))
				self.actionNew_Scene.setEnabled(True)
				self.newscene_button.setEnabled(True)
				self.actionSave_Project.setEnabled(True)
					
			except:
				print(sys.exc_info())
	
	def open_project(self):
	
		#Ask the user if they want to save before starting a new project
		if self._has_active_project:
			self.prompt_save()
	
		#Create the file dialog
		file = QtWidgets.QFileDialog()
		fn = file.exec()
		if(fn):
			try:
				
				#Clear the scene and object lists
				self.object_list.clear()
				self.scene_list.clear()
				self.object_heirarchy.clear()
				self.scene_preview.setScene(None)
				
				self._has_active_object = False
				self._has_active_scene = False
				
				#Try to open the file and extract the project data from it
				with open(file.selectedFiles()[0]) as project_file:
					file_obj = json.loads(project_file.read())
					project_file.close()
					self._project_state = file_obj
					self._current_project = self._project_state["project_name"]
					self._current_working_directory = self._project_state["project_directory"]
					
					for scene in self._project_state["scenes"]:
						self.scene_list.addItem(scene)
						
					for object in self._project_state["object_types"]:
						self.object_list.addItem(object)
					
					self._has_active_project = True
					self.unlock_components()
					self.scene_preview.setSceneRect(QtCore.QRectF(0.0, 0.0, self._project_state["project_settings"]["window_x"], self._project_state["project_settings"]["window_y"]))
					self.actionNew_Scene.setEnabled(True)
					self.newscene_button.setEnabled(True)
					self.actionSave_Project.setEnabled(True)
					
					if(self.scene_list.count() > 0):
						self.actionSave_Scene.setEnabled(True)
						self.actionNew_GameObject.setEnabled(True)
						self.newgameobject_button.setEnabled(True)

			except:
				print(sys.exc_info())
				
	def import_gameobject(self):
		pass
		
	def import_scene(self):
		pass
	
	def save_scene(self):
		try:
			scenes_dir = os.path.join(self._project_state["project_directory"], "scenes")
			file = open(os.path.join(scenes_dir, self._current_active_scene + ".json"), "w+")
			file.write(json.dumps(self._active_scene_state))
			file.close()
		except:
			print(sys.exc_info())
	
	def save_project(self):
		try:
			file = open(os.path.join(self._project_state["project_directory"], self._current_project + ".json"), "w+")
			file.write(json.dumps(self._project_state))
			file.close()
			self.save_scene()
			self.save_editor_settings()
		except:
			print(sys.exc_info())
	
	def exit_program(self):
		if(self._can_save):
			self.prompt_save()
		sys.exit()
	
	
	#Lower button group functions
	def new_scene(self):
		Dialog = QtWidgets.QDialog()
		ui = Ui_NewScene()
		ui.setupUi(Dialog)
		Dialog.show()
		result = Dialog.exec_()
			
		if(result == QtWidgets.QDialog.Accepted):
			scene_name = ui.scene_name.text()
			background_image = ui.background_image_dir.text()
			scene_obj = {}
			scene_obj["scene_name"] = scene_name
			scene_obj["background"] = background_image
			scene_obj["objects"] = []	
			
			self._current_active_scene = scene_name
			self._active_scene_state = scene_obj
			self._project_state["scenes"].append(scene_name)
			
			scene_dir = os.path.join(self._project_state["project_directory"], "scenes")
			scene_file = open(os.path.join(scene_dir, scene_name + ".json"), "w+")
			scene_file.write(json.dumps(scene_obj))
			scene_file.close()
			
			self.scene_list.addItem(scene_name)
			self.actionSave_Scene.setEnabled(True)
			self.actionNew_GameObject.setEnabled(True)
			self.newgameobject_button.setEnabled(True)
			self.save_project()
	
	def new_gameobject(self):
		Dialog = QtWidgets.QDialog()
		ui = Ui_NewGameobject()
		ui.setupUi(Dialog)
		Dialog.show()
		result = Dialog.exec_()
		
		if result:
			#Get the form data
			gameobject_type_name = ui.gameobject_type_name.text()
			gameobject_image_dir = ui.gameobject_image_directory.text()
			
			#Get all the necessary directories
			rootdir = self._project_state["project_directory"]
			template_files_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), "template_files")
			assets_dir = os.path.join(rootdir, "assets")
			new_image_path = os.path.join(assets_dir, os.path.basename(gameobject_image_dir))
			
			#Copy template files and assets into their appropriate locations
			try:
				shutil.copyfile(os.path.join(template_files_dir, "gameObject.temp.py"), os.path.join(rootdir, gameobject_type_name + ".py"))
			except:
				print(sys.exc_info())
				
			try:
				shutil.copyfile(gameobject_image_dir, new_image_path)
			except:
				print(sys.exc_info())
				
			try:
				temp_file_r = open(os.path.join(rootdir, gameobject_type_name + ".py"), "r")
				ts = temp_file_r.read()
				temp_file_r.close()
				ts = ts.replace("($GAMEOBJECT_NAME)", gameobject_type_name)
			except:
				print(sys.exc_info())
			
			try:
				temp_file_w = open(os.path.join(rootdir, gameobject_type_name + ".py"), "w+")
				temp_file_w.write(ts)
				temp_file_w.close()
			except:
				print(sys.exc_info())
			
			#Add the object to the object list
			self.object_list.addItem(gameobject_type_name)
			self._project_state["object_types"][gameobject_type_name] = {"image": new_image_path}
			
			self.save_project()
	
	def edit_gameobject(self):
		if self._has_active_object:
			editor = self._editor_settings["code_editor"]
			cmd_str = '"' + editor + "\" " + os.path.join(self._project_state["project_directory"], self.object_list.item(self.object_list.currentRow()).text() + ".py")
			os.system(cmd_str)
	
	def delete_gameobject(self):
		if self._has_selected_object:
			graphics_item = self._heirarchy_objects[self._selected_object["id"]]["graphics_item"]
			self._preview_scene.removeItem(graphics_item)
			self.object_heirarchy.takeItem(self.object_heirarchy.currentRow())
			self._active_scene_state["objects"].remove(self._selected_object)
			self._selected_object = {}
			self.deletegameobject_button.setEnabled(False)
			self._has_selected_object = False
			self.save_project()
	
	def deleteall_gameobjects(self):
		pass
	
	def edit_scene_settings(self):
		pass

	#Utility functions
	def prompt_save(self):
		message_box = QtWidgets.QMessageBox()
		message_box.setWindowTitle("Save Project?")
		message_box.setIcon(QtWidgets.QMessageBox.Question)
		message_box.setText("Would you like to save the changes to your project?")
		message_box.setStandardButtons(QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
		result = message_box.exec_()
		
		#For some reason this is the return value
		if(result == 16384):
			self.save_project()			
		
	def unlock_components(self):
		self.object_heirarchy.setEnabled(True)
		self.object_list.setEnabled(True)
		self.scene_list.setEnabled(True)
		
	def scenelist_clicked(self):
		#Save the scene since the changes will be cleared by changing the active scene
		if self._has_active_scene:
			self.save_scene()
		
		#Grab the scene file and convert it into a JSON object
		scene_dir = os.path.join(self._project_state["project_directory"], "scenes")
		file = open(os.path.join(scene_dir, self.scene_list.item(self.scene_list.currentRow()).text() + ".json"), "r")
		scene_obj = json.loads(file.read())
		
		#Set the states and flags
		self._current_active_scene = self.scene_list.item(self.scene_list.currentRow()).text()
		self._active_scene_state = scene_obj
		self.scene_name_label.setText("Scene Name: " + self._current_active_scene)
		self._has_active_scene = True
		
		#Clear the scene preview and heirarchy, draw the background and objects
		self.scene_preview.setEnabled(True)
		self._preview_scene = QtWidgets.QGraphicsScene()
		background = QtWidgets.QGraphicsPixmapItem(QtGui.QPixmap(self._active_scene_state["background"]))
		background.setPos(0,0)
		self._preview_scene.addItem(background)
		self.scene_preview.setScene(self._preview_scene)
		self.object_heirarchy.clear()
		self._heirarchy_objects = {}
		for object in self._active_scene_state["objects"]:
			new_object = QtWidgets.QGraphicsPixmapItem(QtGui.QPixmap(object["image"]))
			new_object.setPos(object["x"], object["y"])
			self._heirarchy_objects[object["id"]] = {"image": object["image"], "graphics_item": new_object}
			self._preview_scene.addItem(new_object)
			self.object_heirarchy.addItem(object["obj_name"] + "(" + object["type"] + "), ID: " + object["id"])
			
		#Set the mouse click event (redundant most of the time but I don't know where else to put this)
		self._preview_scene.mousePressEvent = self.scenepreview_clicked
		
	def objectlist_clicked(self):
		selected_item = self.object_list.item(self.object_list.currentRow()).text()
		self._active_object = self._project_state["object_types"][selected_item]
		self._has_active_object = True
		self.editgameobject_button.setEnabled(True)
		
	def scenepreview_clicked(self, event):
		if self._has_active_object and self._has_active_scene:
			x = event.scenePos().x()
			y = event.scenePos().y()
			
			#Create the new graphics item
			new_object = QtWidgets.QGraphicsPixmapItem(QtGui.QPixmap(self._active_object["image"]))
			new_object.setPos(x,y)
			self._preview_scene.addItem(new_object)
			
			#Guarantee a unique ID
			random_id = str(random.randint(100000, 999999))
			while self.find_object_by_id(random_id) is not None:
				random_id = str(random.randint(100000, 999999))
			
			self._active_scene_state["objects"].append({"id": random_id, "obj_name": "none", "type": self.object_list.item(self.object_list.currentRow()).text(), "x": x, "y": y, "image": self._active_object["image"], "custom_properties": {}})
			self._heirarchy_objects[random_id] = {"image": self._active_object["image"], "graphics_item": new_object}
			self.object_heirarchy.addItem("none (" + self.object_list.item(self.object_list.currentRow()).text() + "), ID: " + random_id)
			
			self._can_save = True
			
	def objectheirarchy_clicked(self):
		selected_item = self.object_heirarchy.item(self.object_heirarchy.currentRow()).text()
		selected_item_id = selected_item[-6:]
		self._selected_object = self.find_object_by_id(selected_item_id)
		
		self._has_selected_object = True
		self.deletegameobject_button.setEnabled(True)
			
	def load_editor_settings(self):
		try:
			path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "editor_settings.json")
			file = open(path, "r")
			self._editor_settings = json.loads(file.read())
			file.close()
		except:
			self._editor_settings["code_editor"] = "notepad"
			print(sys.exc_info())
			
	def save_editor_settings(self):
		try:
			path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "editor_settings.json")
			file = open(path, "w+")
			file.write(json.dumps(self._editor_settings))
			file.close()
		except:
			self._editor_settings["code_editor"] = "notepad"
			print(sys.exc_info())
			
	def find_object_by_id(self, id):
		for obj in self._active_scene_state["objects"]:
			if(obj["id"] == id):
				return obj
		return None
	
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = PygameEditor(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())