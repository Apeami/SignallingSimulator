extends Control


func _ready():
	pass 


func _process(delta):
	if pressed==true:
		rect_position = get_viewport().get_mouse_position()+difference


var pressed = false
var difference = null

func _on_DragButton_button_down():
	var mousePos = get_viewport().get_mouse_position()
	var windowPos = rect_position
	difference=windowPos-mousePos
	pressed=true
	print(difference)


func _on_DragButton_button_up():
	pressed=false
