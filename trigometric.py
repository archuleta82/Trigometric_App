# Author: Steven Archuleta
# Date: Jan 2020
# User enters two known measurements of a right triangle and presses enter.
# The application updates remaining angles and side lengths.
# Works with Pythonista app on Apple products for UI.

import ui
from scene import *
import math
from objc_util import *
UIDevice = ObjCClass('UIDevice')


# ---- Add right triangle image to ui ----
view = ui.View()
wid = view.width
high = view.height

iv = ui.ImageView()
iv.image = ui.Image.named('rightT.png')
iv.flex = 'WHTB'
iv.x = wid
iv.y = high + 20
iv.width = 150
iv.height = 120
degreesign = u'\N{DEGREE SIGN}'


# ---- Logic ----
def taptic_popper():
	d = UIDevice.new()
	t = d._tapticEngine()
	t.actuateFeedback_(1002)
	
	
def digits(s):
	try:
		for char in s:
			if char.isdigit() or char.isfloat():
				return True
	except:
		return False
		

def verify(insides):
	count = 0
	results = [0, 0, 0, 0, 0]
	for s in insides:
		if len(s.text) > 0 and digits(s.text):
			results[count] = 1
		count += 1
	return results
		

def pythag(a, b):
	return str(round(math.sqrt((a*a) + (b*b)), 2))

	
def button_tapped(sender):
	'@type sender: ui.Button'
	a = sender.superview['textfield2']
	b = sender.superview['textfield1']
	c = sender.superview['textfield3']
	angle_a = sender.superview['textfield5']
	angle_b = sender.superview['textfield4']
	sides = [a, b, c, angle_a, angle_b]
	taptic_popper()
	
	results = verify(sides)
	print(results)
	
	if results[3:] == [0, 0]:
		if results == [1, 1, 0, 0, 0]:
			a = float(a.text)
			b = float(b.text)
			# c.text = str(round(math.sqrt((a*a + b*b)),2))
			c.text = pythag(a, b)
			c = float(c.text)
			
		elif results == [1, 0, 1, 0, 0]:
			c = float(c.text)
			a = float(a.text)
			b.text = str(round(math.sqrt((c*c - a*a)), 2))
			b = float(b.text)
		
		elif results == [0, 1, 1, 0, 0]:
			b = float(b.text)
			c = float(c.text)
			a.text = str(round(math.sqrt((c*c - b*b)), 2))
			a = float(a.text)
			
		print(str(results))
		#if results[3:] == [0, 0]:
		angle_a.text = str(round(math.degrees(math.atan(a/b)), 1))
		angle_b.text = str(round(90 - (float(angle_a.text)), 1))
		angle_a.text += degreesign
		angle_b.text += degreesign
	
	else:
		if results[3:] == [1, 0]:
			al = float(angle_a.text)
			angle_b.text = str(90 - al)
		elif results[3:] == [0, 1]:
			bo = float(angle_b.text)
			angle_a.text = str(90 - bo)
		
		results = verify(sides)
		print(results)
		if results == [1, 0, 0, 1, 1]:
			a = float(a.text)
			be = a / math.tan(math.radians(float(angle_a.text)))
			c.text = str(pythag(a, be))
			b.text = str(round(be, 1))
			
		elif results == [0, 1, 0, 1, 1]:
			b = float(b.text)
			an = math.tan(math.radians(float(angle_a.text))) * b
			c.text = pythag(an, b)
			a.text = str(round(an, 1))
			
		elif results == [0, 0, 1, 1, 1]:
			c = float(c.text)
			an = math.cos(math.radians(float(angle_b.text))) * c
			b.text = str(round(math.sqrt((c*c) - (an*an)), 1))
			a.text = str(round(an, 1))
		
		angle_a.text += degreesign
		angle_b.text += degreesign	
		label = sender.superview['label1']
		label.text = 'Calculations complete!'
		return
		


def clear(sender):
	'@type sender: ui.Button'
	taptic_popper()
	a.text = ''
	b.text = ''
	c.text = ''
	angle_a.text = ''
	angle_b.text = ''
	label = sender.superview['label1']
	label.text = 'Another one!'

v = ui.load_view()

b = v['textfield1']
a = v['textfield2']
c = v['textfield3']
angle_a = v['textfield5']
angle_b = v['textfield4']

v.add_subview(iv)
v.present('sheet')
