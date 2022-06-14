extends Control

signal requestChange(menuItem)


func _ready():
	print("Main Menu Loaded")


func _on_LoadButton_pressed():
	print("Load Button Pressed")
	emit_signal("requestChange","loadButton")


func _on_EditorButton_pressed():
	print("Editor Button Pressed")
	emit_signal("requestChange","editorButton")


func _on_SettingsButton_pressed():
	print("Settings Button Pressed")
	emit_signal("requestChange","settingsButton")
