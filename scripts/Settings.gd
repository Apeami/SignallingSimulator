extends Control

signal toReturn

func fillContributerList():
	var file = File.new()
	file.open("res://contributerList.txt", File.READ)
	get_node("ContributerBox").text = file.get_as_text()


func _ready():
	fillContributerList()



func _on_ReturnButton_pressed():
	emit_signal("toReturn")
