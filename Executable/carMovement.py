print("Python script loading started")

newScene()
loadGeometry("car.osb")

from time import sleep
from math import sin, cos, radians
from threading import Thread, Lock

#nodes
car = findNode("car")
wheelBase_Front = findNode("WheelBase_Front")
wheelBase_Back = findNode("WheelBase_Back")
wheelBase = findNode('Skirt_MultiMaterial')
tireFL = findNode("TireFL_MultiMaterial")
tireRimFL = findNode("TireFL_mat_0")
tireRL = findNode("TireRL_MultiMaterial")
tireRimRL = findNode("TireRL_mat_0")
tireFR = findNode("TireFR_MultiMaterial")
tireRimFR = findNode("TireFR_mat_0")
tireRR = findNode("TireRR_MultiMaterial")
tireRimRR = findNode("TireRR_mat_0")
steeringWheel = findNode("Steering_Transform")
puddles = [findNode('puddleCone1')]

#materials
waterColorMaterial = findMaterial("WaterColor")
tireMaterial = findMaterial("Tire")

#camera
firstPersonCamera = [180.0, 40.0, 35.0]#angle, constant and z axis
thirdPersonCamera = [150.0, 176.0, 50.0]
camera = [[]]

#car
carSpeed = [8]
carTurnSpeed = [3]

#tire
tireAxis = [2.00, 2.00]
tireSpeed = [15.0]
tireTurnSpeed = [.4]

#Steering Wheel
steeringTurnSpeed = [3]

#puddle
puddleAxis = [[0, 400], [400,0], [-400,0], [200,200], [-200,200],[200,-200], [-200,-200]]
lock = Lock()

dryTimeout = [0, 0, 0, 0]

for i, t in enumerate(puddleAxis):
	newPuddle = puddles[0].copy()
	newPuddle.setName("puddleCone" + str(i + 2))
	newPuddle.setTranslation(t[0], t[1], 0)
	puddles.append(newPuddle)

collisionTireFL = vrCollision([tireFL], puddles)
collisionTireFR = vrCollision([tireFR], puddles)
collisionTireRL = vrCollision([tireRL], puddles)
collisionTireRR = vrCollision([tireRR], puddles)


def updateCamera(x, y, rotation):
	aa = x + camera[0][1] * sin(radians(rotation + (camera[0][0])))
	bb = y - camera[0][1] * cos(radians(rotation + (camera[0][0])))
	fromPtr = Pnt3f(aa, bb, camera[0][2])
	firstX = x + sin(radians(rotation + (camera[0][0])))
	firstY = y - cos(radians(rotation + (camera[0][0])))
	toPtr = Pnt3f(firstX, firstY, camera[0][2])
	setFromAtUp(-1, fromPtr, toPtr, getUp(-1))	


def aswd(anglularForce, translateForce):
	rotation = car.getRotation()[2]
	x = car.getTranslation()[0]
	y = car.getTranslation()[1]
	
	if anglularForce != 0:
		rotation += anglularForce * carTurnSpeed[0]
		car.setRotation(0, 0, rotation)
		updateTireAngle(anglularForce)
		updateSteeringAngle(anglularForce)

	if translateForce != 0:
		x += carSpeed[0] * translateForce * sin(radians(rotation))
		y -= carSpeed[0] * translateForce * cos(radians(rotation))		
		car.setTranslation(x, y, 0)
		updateTireRotation(translateForce)
	updateCamera(x, y, rotation)
	isTireOnPuddle()

def updateTireRotation(translateForce):
	leftTires = list(tireFL.getRotation())
	rightTires = list(tireFR.getRotation())
	leftTires[1] += translateForce * tireSpeed[0]
	rightTires[1] -= translateForce * tireSpeed[0]
	
	tireFL.setRotation(1.0, leftTires[1], -90.0)
	tireRL.setRotation(1.0, leftTires[1], -90.0)
	tireFR.setRotation(1.0, rightTires[1], 90.0)
	tireRR.setRotation(1.0, rightTires[1], 90.0)

def updateTireAngle(anglularForce):
	leftRotation = tireFL.getRotation()[2]
	leftRotation += anglularForce * tireTurnSpeed[0]
	tireFL.setRotation(0.0, 0.0, leftRotation)
	tireRL.setRotation(0.0, 0.0, leftRotation)
	
	rightRotation = tireFR.getRotation()[2]
	rightRotation += anglularForce * tireTurnSpeed[0]
	tireFR.setRotation(0.0, 0.0, rightRotation)
	tireRR.setRotation(0.0, 0.0, rightRotation)	


def updateSteeringAngle(anglularForce):
	steeringAngle = list(steeringWheel.getRotation())[0]
	steeringAngle += anglularForce * steeringTurnSpeed[0]
	steeringWheel.setRotation(steeringAngle, 0.0, 90.0)
	
def isTireOnPuddle():
	if collisionTireFL.isColliding() and tireRimFL.getMaterial().getName() != waterColorMaterial.getName():
		tireRimFL.setMaterial(waterColorMaterial)
	elif collisionTireFL.isColliding() == False and tireRimFL.getMaterial().getName() != tireMaterial.getName():
		lock.acquire()
		if dryTimeout[0] == 2:
			tireRimFL.setMaterial(tireMaterial)
			dryTimeout[0] = 0
		elif dryTimeout[0] == 0:
			dryTimeout[0] = 1
		lock.release()
			
		
	if collisionTireFR.isColliding() and tireRimFR.getMaterial().getName() != waterColorMaterial.getName():
		tireRimFR.setMaterial(waterColorMaterial)
	elif collisionTireFR.isColliding() == False and tireRimFR.getMaterial().getName() != tireMaterial.getName():
		lock.acquire()
		if dryTimeout[1] == 2:
			tireRimFR.setMaterial(tireMaterial)
			dryTimeout[1] = 0
		elif dryTimeout[1] == 0:
			dryTimeout[1] = 1
		lock.release()

	if collisionTireRL.isColliding() and tireRimRL.getMaterial().getName() != waterColorMaterial.getName():
		tireRimRL.setMaterial(waterColorMaterial)
	elif collisionTireRL.isColliding() == False and tireRimRL.getMaterial().getName() != tireMaterial.getName():
		lock.acquire()
		if dryTimeout[2] == 2:
			tireRimRL.setMaterial(tireMaterial)
			dryTimeout[2] = 0
		elif dryTimeout[2] == 0:
			dryTimeout[2] = 1
		lock.release()
		
	if collisionTireRR.isColliding() and tireRimRR.getMaterial().getName() != waterColorMaterial.getName():
		tireRimRR.setMaterial(waterColorMaterial)
	elif collisionTireRR.isColliding() == False and tireRimRR.getMaterial().getName() != tireMaterial.getName():
		lock.acquire()
		if dryTimeout[3] == 2:
			tireRimRR.setMaterial(tireMaterial)
			dryTimeout[3] = 0
		elif dryTimeout[3] == 0:
			dryTimeout[3] = 1
		lock.release()


def changeView():
	if camera[0] is thirdPersonCamera:
		camera[0] = firstPersonCamera
		print "First Camera View"
	else:
		camera[0] = thirdPersonCamera
		print "Third Camera View"
	aswd(0.0, 1.0)

def updateWheelBase(sliderChangedValue):
	scale = list(wheelBase.getScale())
	scale[0] +=  sliderChangedValue
	wheelBase.setScale(scale[0], scale[1], scale[2])
	
	front = list(wheelBase_Front.getTranslation())
	front[1] -= (sliderChangedValue / 2)
	wheelBase_Front.setTranslation(front[0], front[1], front[2])
	
	back = list(wheelBase_Back.getTranslation())
	back[1] += (sliderChangedValue / 2)
	wheelBase_Back.setTranslation(back[0], back[1], back[2])
	
w = vrKey(Key_W)
w.connect(aswd, 0.0, 1.0)

s = vrKey(Key_S)
s.connect(aswd, 0.0, -1.0)

d = vrKey(Key_D)
d.connect(aswd, -1.0, 0.0)

a = vrKey(Key_A)
a.connect(aswd, 1.0, 0.0)

keyC = vrKey(Key_C)
keyC.connect(changeView)

changeView()

class DryTiresAfterAWhile(Thread):
	def __init__(self, dryTimeout, lock):
		Thread.__init__(self)
		self.running = True
		self.dryTimeout = dryTimeout
		self.lock = lock

	def run(self):
		while self.running:
			self.lock.acquire()
			if dryTimeout[0] == 1:
				dryTimeout[0] = 2
			if dryTimeout[1] == 1:
				dryTimeout[1] = 2
			if dryTimeout[2] == 1:
				dryTimeout[2] = 2
			if dryTimeout[3] == 1:
				dryTimeout[3] = 2
			self.lock.release()
			sleep(2)

	def terminate(self):
		self.running = False

thread = DryTiresAfterAWhile(dryTimeout, lock)
thread.start()

print("Python script loading completed")
