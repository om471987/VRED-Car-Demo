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
puddles = findNode('puddleCone1')

#materials
waterColorMaterial = findMaterial("WaterColor")
tireMaterial = findMaterial("Tire")

#camera
firstPersonCamera = [10.0, 30.0, 30.0]
thirdPersonCamera = [80.0,100.0,50.0]
camera = [[], []]

#car
carPosition = [0, 0]
carAngle = [0]
carSpeed = [1]
maxSpeed = [1];
rotSpeed = [1];

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
puddleRadiusSquare = [pow(80.0, 2)]

from time import sleep
from math import sin, cos, fabs, radians, pi, pow

def updateCamera():
	carTra = car.getTranslation()
	fromPtr = Pnt3f(carTra[0] + camera[0][0],carTra[1] + camera[0][1], camera[0][2])
	toPtr = Pnt3f(carTra[0],carTra[1],carTra[2])
	setFromAtUp(-1, fromPtr, toPtr, getUp(-1))
	
	
def aswd(anglularForce, translateForce):
	rotation = car.getRotation()[2]
	x = car.getTranslation()[0]
	y = car.getTranslation()[1]
	
	if anglularForce != 0:
		rotation += anglularForce * rotSpeed[0]
		steetingAngle[0] += anglularForce * 1
		tireAngleLeft[0] += anglularForce * 1
		tireAngleRight[0] += anglularForce * 1
		car.setRotation(0, 0, rotation)
		updateTireAngle()
		updateSteeringAngle()

	if translateForce != 0:
		x += maxSpeed[0] * translateForce * sin(radians(rotation))
		y -= maxSpeed[0] * translateForce * cos(radians(rotation))
		tireAxis[0] -= -1 * translateForce * tireSpeed[0]
		tireAxis[1] += -1 * translateForce * tireSpeed[0]		
		car.setTranslation(x, y, 0)
		updateTireRotation()
	updateCamera()

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
	
def isTireOnPuddle():
	locationFL = getTransformNodeTranslation(tireFL, true)
	locationRL = getTransformNodeTranslation(tireRL, true)
	locationFR = getTransformNodeTranslation(tireFR, true)
	locationRR = getTransformNodeTranslation(tireRR, true)
	
	#for puddle in puddles:
	puddleLocation = getTransformNodeTranslation(puddles, true)
	if (pow((locationFL.x() - puddleLocation.x()), 2) + pow((locationFL.y() - puddleLocation.y()), 2)) <= puddleRadiusSquare[0]:
		soakTireFL()
	else:
		dryUpTireFL()
	if (pow((locationRL.x() - puddleLocation.x()), 2) + pow((locationRL.y() - puddleLocation.y()), 2)) <= puddleRadiusSquare[0]:
		soakTireRL()
	else:
		dryUpTireRL()
	if (pow((locationFR.x() - puddleLocation.x()), 2) + pow((locationFR.y() - puddleLocation.y()), 2)) <= puddleRadiusSquare[0]:
		soakTireFR()
	else:
		dryUpTireFR()
	if (pow((locationRR.x() - puddleLocation.x()), 2) + pow((locationRR.y() - puddleLocation.y()), 2)) <= puddleRadiusSquare[0]:
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
		#camera[1] = [carPosition[0], carPosition[1] - 20, 20]
		print "First Camera View"
	else:
		camera[0] = thirdPersonCamera
		#camera[1] = [carPosition[0], carPosition[1], 0]
		print "Third Camera View"
	updateCamera()

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
	
w = vrKey(Key_W)
w.connect(aswd, 0.0, 1.0)
s = vrKey(Key_S)
s.connect(aswd, 0.0, -1.0)
a = vrKey(Key_A)
a.connect(aswd, -1.0, 0.0)
d = vrKey(Key_D)
d.connect(aswd, 1.0, 0.0)

keyC = vrKey(Key_C)
keyC.connect(changeView)

changeView()

cameraAnglea = [0,0]
def cameraAngle(x, y):
	cameraAnglea[0] += x
	cameraAnglea[1] += y
	setCameraRotation(cameraAnglea[0], cameraAnglea[1])
	cam = getCamNode(-1)
	print "cam angle", cam.getRotation()

key1 = vrKey(Key_1)
key1.connect(cameraAngle, 0.01, 0)

key2 = vrKey(Key_2)
key2.connect(cameraAngle, -0.01, 0)

print("this should come on log")
