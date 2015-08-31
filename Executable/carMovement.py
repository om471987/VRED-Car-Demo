print "Executing find script!"

newScene()
loadGeometry("./car.osb")
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
firstPersonCamera = [10.0, 40.0, 30.0]
thirdPersonCamera = [150.0, 30.0, 50.0]#angle constant and z axis
camera = [[]]

#car
carSpeed = [8]
carTurnSpeed = [3]

#tire
tireAxis = [2.00, 2.00]
tireSpeed = [15.0]
tireAngleLeft = [-90]
tireAngleRight = [90]
tireTurnSpeed = [.6]

#Steering Wheel
steeringAngle = list(steeringWheel.getRotation())
steeringTurnSpeed = [3]

#Wheelbase
wheelBasePosition = [25.40, 25.40, 25.40]
wheelBaseDelta = [0.0]

#puddle
newPuddle = puddles[0].copy()
newPuddle.setName("puddleCone" + str(len(puddles) + 1))
puddles.append(newPuddle)
newPuddle.setTranslation(200, 200, 0)

collisionTireFL = vrCollision([tireFL], puddles)
collisionTireFR = vrCollision([tireFR], puddles)
collisionTireRL = vrCollision([tireRL], puddles)
collisionTireRR = vrCollision([tireRR], puddles)

from time import sleep
from math import sin, cos, radians

'''def updateCamera():
	carTra = car.getTranslation()
	carRot = car.getRotation()
	x = camera[0][0] + carSpeed[0] *  sin(radians(rotation))
	y = camera[0][1] - carSpeed[0] *  cos(radians(rotation))	
	print x, ",", y
	fromPtr = Pnt3f(carTra[0] + x, carTra[1] + y, camera[0][2])
	toPtr = Pnt3f(carTra[0], carTra[1], camera[0][2])
	setFromAtUp(-1, fromPtr, toPtr, getUp(-1))'''


def aswd(anglularForce, translateForce):
	rotation = car.getRotation()[2]
	x = car.getTranslation()[0]
	y = car.getTranslation()[1]
	
	if anglularForce != 0:
		rotation += anglularForce * carTurnSpeed[0]
		steeringAngle[0] += anglularForce * steeringTurnSpeed[0] * 1
		tireAngleLeft[0] += anglularForce * tireTurnSpeed[0] * 1
		tireAngleRight[0] += anglularForce * tireTurnSpeed[0] * 1
		car.setRotation(0, 0, rotation)
		updateTireAngle()
		updateSteeringAngle()

	if translateForce != 0:
		x += carSpeed[0] * translateForce * sin(radians(rotation))
		y -= carSpeed[0] * translateForce * cos(radians(rotation))
		tireAxis[0] -= -1 * translateForce * tireSpeed[0]
		tireAxis[1] += -1 * translateForce * tireSpeed[0]		
		car.setTranslation(x, y, 0)
		updateTireRotation()
		
	aa = x + carSpeed[0] * 1 * camera[0][1] * sin(radians(rotation + (camera[0][0])))
	bb = y - carSpeed[0] * 1 * camera[0][1] * cos(radians(rotation + (camera[0][0])))
	fromPtr = Pnt3f(camera[0][0] + aa, camera[0][1] + bb, camera[0][2])
	toPtr = Pnt3f(x, y, camera[0][2])
	setFromAtUp(-1, fromPtr, toPtr, getUp(-1))	
	isTireOnPuddle()

def updateTireRotation():
	setTransformNodeRotation(tireFL, 1.0, tireAxis[0], -90.0)
	setTransformNodeRotation(tireRL, 1.0, tireAxis[0], -90.0)
	setTransformNodeRotation(tireFR, 1.0, tireAxis[1], 90.0)
	setTransformNodeRotation(tireRR, 1.0, tireAxis[1], 90.0)

def updateTireAngle():
	tireFL.setRotation(1, 1, tireAngleLeft[0])
	tireRL.setRotation(1, 1, tireAngleLeft[0])
	tireFR.setRotation(1, 1, tireAngleRight[0])
	tireRR.setRotation(1, 1, tireAngleRight[0])	


def updateSteeringAngle():
	setTransformNodeRotation(steeringWheel, steeringAngle[0], 0, 90)
	
def isTireOnPuddle():
	if collisionTireFL.isColliding() and tireRimFL.getMaterial() is not waterColorMaterial:
		tireRimFL.setMaterial(waterColorMaterial)
	elif collisionTireFL.isColliding() == False and tireRimFL.getMaterial() is not tireMaterial:
		tireRimFL.setMaterial(tireMaterial)
		
	if collisionTireFR.isColliding() and tireRimFR.getMaterial() is not waterColorMaterial:
		tireRimFR.setMaterial(waterColorMaterial)
	elif collisionTireFR.isColliding() == False and tireRimFR.getMaterial() is not tireMaterial:
		tireRimFR.setMaterial(tireMaterial)

	if collisionTireRL.isColliding() and tireRimRL.getMaterial() is not waterColorMaterial:
		tireRimRL.setMaterial(waterColorMaterial)
	elif collisionTireRL.isColliding() == False and tireRimRL.getMaterial() is not tireMaterial:
		tireRimRL.setMaterial(tireMaterial)
		
	if collisionTireRR.isColliding() and tireRimRR.getMaterial() is not waterColorMaterial:
		tireRimRR.setMaterial(waterColorMaterial)
	elif collisionTireRR.isColliding() == False and tireRimRR.getMaterial() is not tireMaterial:
		tireRimRR.setMaterial(tireMaterial)


def changeView():
	if camera[0] is thirdPersonCamera:
		camera[0] = firstPersonCamera
		print "First Camera View"
	else:
		camera[0] = thirdPersonCamera
		print "Third Camera View"
	aa = camera[0][1] * sin(radians(camera[0][0]))
	bb = camera[0][1] * cos(radians(camera[0][0]))
	fromPtr = Pnt3f(camera[0][0] + aa, camera[0][1] + bb, camera[0][2])
	cc = car.getTranslation()
	toPtr = Pnt3f(cc[0], cc[1], camera[0][2])
	setFromAtUp(-1, fromPtr, toPtr, getUp(-1))

def updateWheelBase(sliderValue):
	delta = sliderValue - wheelBaseDelta[0]
	wheelBaseDelta[0] = sliderValue

	#x = a[0] + sin(radians(carRot[2]))
	#y = a[1] + cos(radians(carRot[2]))
	
	a = getTransformNodeTranslation(wheelBase_Front, true)
	setTransformNodeTranslation(wheelBase_Front, a.x(), a.y() - (delta / 2), a.z(), True)

	a = getTransformNodeTranslation(wheelBase_Back, true)
	setTransformNodeTranslation(wheelBase_Back, a.x(), a.y() + (delta / 2), a.z(), True)

	wheelBase.setScale(wheelBasePosition[0] + wheelBaseDelta[0], wheelBasePosition[1], wheelBasePosition[2])
	
w = vrKey(Key_W)
w.connect(aswd, 0.0, 1.0)
up = vrKey(Key_Up)
up.connect(aswd, 0.0, 1.0)

s = vrKey(Key_S)
s.connect(aswd, 0.0, -1.0)
down = vrKey(Key_Down)
down.connect(aswd, 0.0, -1.0)

d = vrKey(Key_D)
d.connect(aswd, -1.0, 0.0)
left = vrKey(Key_Left)
left.connect(aswd, -1.0, 0.0)

a = vrKey(Key_A)
a.connect(aswd, 1.0, 0.0)
right = vrKey(Key_Right)
right.connect(aswd, 1.0, 0.0)


keyC = vrKey(Key_C)
keyC.connect(changeView)

changeView()

'''def cameraAngle(x):
	camera[0][0] +=  x
	updateCamera()

key1 = vrKey(Key_1)
key1.connect(cameraAngle, 1)

key2 = vrKey(Key_2)
key2.connect(cameraAngle, -1)'''

print("this should come on log")
