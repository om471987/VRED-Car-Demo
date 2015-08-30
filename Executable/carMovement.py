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
puddles = findNodes('puddleCone',True)

#materials
waterColorMaterial = findMaterial("WaterColor")
tireMaterial = findMaterial("Tire")

updateScene()

from time import sleep
from math import sin, cos, pow

#camera
firstPersonCamera = [10, 30, 30]
thirdPersonCamera = [0,100,50]
camera = [[], []]
upVector = [-0.346251, 0.346252, 0.871906]

#car
carPosition = [0, 0]
carAngle = [0]

#tire
tireAxis = [2.00, 2.00]
tireSpeed = [15.0]
tireAngleLeft = [-90]
tireAngleRight = [90]

#Steering Wheel
steetingAngle = [4.16338e-006, 0.347707, 2.95671]

#Wheelbase
wheelBasePosition = [25.40, 25.40, 25.40]
wheelBaseDelta = [0.0]

#puddle
puddleRadius = [80.0]

def updateCameraPosition():
	setFromAtUp(-1, carPosition[0] + camera[0][0], carPosition[1] + camera[0][1], camera[0][2], camera[1][0], camera[1][1], camera[1][2], upVector[0], upVector[1], upVector[2])
	

def updateCarPosition():
	setTransformNodeTranslation(car, carPosition[0], carPosition[1], 0, True)
	#updateCameraPosition()
	#isTireOnPuddle()
	#print "getPositions", getTransformNodeTranslation(car, true)


def updateCarAngle():
	car.setRotation(0, 0, carAngle[0])
	#updateCameraPosition()
	#print "getRotation", car.getRotation()


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
	setTransformNodeRotation(steeringWheel, steetingAngle[0], 0, 90)
	
def translateFront():
	carPosition[0] -= 1 * sin(carAngle[0])
	carPosition[1] -= 1 * cos(carAngle[0])
	tireAxis[0] += tireSpeed[0]
	tireAxis[1] -= tireSpeed[0]	
	updateCarPosition()
	updateTireRotation()


def translateBack():
	carPosition[0] += 1 * sin(carAngle[0])
	carPosition[1] += 1 * cos(carAngle[0])
	tireAxis[0] -= tireSpeed[0]
	tireAxis[1] += tireSpeed[0]	
	updateCarPosition()
	updateTireRotation()


def rotateLeft():
	carAngle[0] += 1
	steetingAngle[0] += 1
	tireAngleLeft[0] += 1
	tireAngleRight[0] += 1
	updateCarAngle()
	updateTireAngle()
	updateSteeringAngle()


def rotateRight():
	carAngle[0] -= 1
	steetingAngle[0] -= 1
	tireAngleLeft[0] -= 1
	tireAngleRight[0] -= 1	
	updateCarAngle()
	updateTireAngle()
	updateSteeringAngle()

def isTireOnPuddle():
	locationFL = getTransformNodeTranslation(tireFL, true)
	locationRL = getTransformNodeTranslation(tireRL, true)
	locationFR = getTransformNodeTranslation(tireFR, true)
	locationRR = getTransformNodeTranslation(tireRR, true)
	
	for puddle in puddles:
		puddleLocation = getTransformNodeTranslation(puddle, true)
		if (pow((locationFL.x() - puddleLocation.x()), 2) + pow((locationFL.y() - puddleLocation.y()), 2)) <= pow(puddleRadius[0], 2):
			soakTireFL()
		else:
			dryUpTireFL()
		if (pow((locationRL.x() - puddleLocation.x()), 2) + pow((locationRL.y() - puddleLocation.y()), 2)) <= pow(puddleRadius[0], 2):
			soakTireRL()
		else:
			dryUpTireRL()
		if (pow((locationFR.x() - puddleLocation.x()), 2) + pow((locationFR.y() - puddleLocation.y()), 2)) <= pow(puddleRadius[0], 2):
			soakTireFR()
		else:
			dryUpTireFR()
		if (pow((locationRR.x() - puddleLocation.x()), 2) + pow((locationRR.y() - puddleLocation.y()), 2)) <= pow(puddleRadius[0], 2):
			soakTireRR()
		else:
			dryUpTireRR()
			
	
def soakTireFL():
	tireRimFL.setMaterial(waterColorMaterial)
def soakTireFR():
	tireRimFR.setMaterial(waterColorMaterial)
def soakTireRL():	
	tireRimRL.setMaterial(waterColorMaterial)
def soakTireRR():	
	tireRimRR.setMaterial(waterColorMaterial)
	
def dryUpTireFL():
	tireRimFL.setMaterial(tireMaterial)
def dryUpTireFR():	
	tireRimFR.setMaterial(tireMaterial)
def dryUpTireRL():
	tireRimRL.setMaterial(tireMaterial)
def dryUpTireRR():
	tireRimRR.setMaterial(tireMaterial)
	
def changeView():
	if camera[0] is thirdPersonCamera:
		camera[0] = firstPersonCamera
		camera[1] = [carPosition[0], carPosition[1] - 20, 20]
		print "First Camera View"
	else:
		camera[0] = thirdPersonCamera
		camera[1] = [carPosition[0], carPosition[1], 0]
		print "Third Camera View"
	updateCameraPosition()

def updateWheelBase(sliderValue):
	carPosition = [0, 0]
	carAngle = [0]
	
	delta = sliderValue - wheelBaseDelta[0]
	wheelBaseDelta[0] = sliderValue
	
	a = getTransformNodeTranslation(wheelBase_Front, true)
	setTransformNodeTranslation(wheelBase_Front, a.x(), a.y() - (delta / 2), a.z(), True)

	a = getTransformNodeTranslation(wheelBase_Back, true)
	setTransformNodeTranslation(wheelBase_Back, a.x(), a.y() + (delta / 2), a.z(), True)
	
	wheelBase.setScale(wheelBasePosition[0] + wheelBaseDelta[0], wheelBasePosition[1], wheelBasePosition[2])
	print wheelBase.getScale()
	
keyW = vrKey(Key_W)
keyW.connect(translateFront)

keyS = vrKey(Key_S)
keyS.connect(translateBack)

keyA = vrKey(Key_A)
keyA.connect(rotateLeft)

keyD = vrKey(Key_D)
keyD.connect(rotateRight)

keyC = vrKey(Key_C)
keyC.connect(changeView)

changeView()
updateCarPosition()

print("this should come on log")
