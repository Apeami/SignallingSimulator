extends Node

func set_main_menu():
	for child in get_children():
		child.queue_free()
	add_child(load("res://scenes/MainMenu.tscn").instance())
	get_node("MainMenu").connect("requestChange",self,"_on_Main_Menu_Change")

func _ready():
	print("Begining")
	set_main_menu()

func _on_Main_Menu_Change(menuItem):
	print(menuItem)
	var main_menu= get_node("MainMenu")
	if menuItem == "settingsButton":
		main_menu.queue_free()
		add_child(load("res://scenes/Settings.tscn").instance())
		get_node("Settings").connect("toReturn",self,"set_main_menu")
	
