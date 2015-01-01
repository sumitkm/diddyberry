#!/usr/bin/env python

# The Diddyberry Keyboard controller - Adapted from 'Raspberry Snake'
# Original program Written by Gareth Halfacree for the Raspberry Pi User Guide
# Adapted by Sumit Maitra 

import pygame
import os
import sys 
import time
import random #don't need this eventually
import PicoBorgRev

# Re-direct output to standard error
sys.stdout = sys.stderr

# Setup the PicoBorg Reverse
PBR = PicoBorgRev.PicoBorgRev()
#PBR.i2cAddress = 0x44 #Uncomment and change if board address has been changed
PBR.Init()

if not PBR.foundChip:
	boards = PicoBorgRev.ScanForPicoBorgReverse()
	if len(boards) == 0:
		print 'No PicoBorg Reverse found, check if you are connected :-)'
	else:
		print 'No PicoBorg Reverse at address %02X, but we did find boards:' % (PBR.i2cAddress)
		for board in boards:
			print '	%02X (%d)' % (board, board)
		print 'If you need to change the I2C address change the setup line so it points to the correct board, e.g. '
		print 'PBR.i2cAddress = 0x%02X' % (boards[0])
	sys.exit()

#Ensure the communications failsafe has be enabled!
failSafe = False
for i in range(5):
	PBR.SetCommsFailsafe(True)
	failsafe = PBR.GetCommsFailsafe()
	if failsafe:
		break
if not failsafe:
	print 'Board %02X failed to report in failsafe mode!' % (PBR.i2cAddress)
	sys.exit()

PBR.ResetEpo()

# Settings for the joystick
axisUpDown = 1
axisUpDownInverted = False
axisLeftRight = 2
axisLeftRightInverted = False
buttonResetEpo = 3
buttonSlow = 8
slowFactor = 0.5
buttonFastTurn = 9
interval = 0.00

# Power settings
voltageIn = 12.0
voltageOut = 6.0

# Setup the power limits
if voltageOut > voltageIn:
	maxPower = 1.0
else:
	maxPower = voltageOut /float(voltageIn)

#setup pygame
from pygame.locals import *
#os.environ["SDL_VIDEODRIVER"] = "dummy" # Removes the need to have GUI window
pygame.init()

fpsClock = pygame.time.Clock()

playSurface = pygame.display.set_mode((640, 480))
#pygame.display.set_caption('Raspberry Snake')

#redColour = pygame.Color(255, 0, 0)
blackColour = pygame.Color(0, 0, 0)
#whiteColour = pygame.Color(255, 255, 255)
#greyColour = pygame.Color(150, 150, 150)
#snakePosition = [100,100]
#snakeSegments = [[100,100],[80,100],[60,100]]
#raspberryPosition = [300,300]
#raspberrySpawned = 1
#direction = 'right'
#changeDirection = direction
#scoreFont = pygame.font.Font('freesansbold.ttf', 10)
#scoreSurface = scoreFont.render(direction, True, greyColour);
#scoreRectangle = scoreSurface.get_rect()
#scoreRectangle.midtop = (320,0)

def 	gameOver():
	gameOverFont = pygame.font.Font('freesansbold.ttf', 72)
	gameOverSurf = gameOverFont.render('Game Over', True, greyColour)
	gameOverRect = gameOverSurf.get_rect()
	gameOverRect.midtop = (320, 10)
	playSurface.blit(gameOverSurf, gameOverRect)
	pygame.display.flip()
	time.sleep(5)
	pygame.quit()
	sys.exit()

try:
	print 'Press ESC to quit'
	driveLeft = 0.0
	driveRight = 0.0
	running = True
	hadEvent = False
	upDown = 0.0
	leftRight = 0.0

	while running:
		#print 'Running'
		events = pygame.event.get()
		for event in events:
			#print 'HasEvent'
			if event.type == QUIT:
				running = False
			elif event.type == KEYDOWN:
				hadEvent = True			
				if event.key == K_RIGHT or event.key == ord('d'):
					leftRight += 0.2
				if event.key == K_LEFT or event.key == ord('a'):
					leftRight -= 0.2
				if event.key == K_UP or event.key == ord('w'):
					upDown += 0.2
				if event.key == K_DOWN or event.key == ord('x'):
					upDown -= 0.2
				if event.key == K_ESCAPE:
					pygame.event.post(pygame.event.Event(QUIT))

			if hadEvent:
				if leftRight > 0.05: #turning right
					driveRight = 1.0 - (2.0 * leftRight)
				elif leftRight < -0.05: #turning left
					driveLeft =  1.0 + (2.0 * leftRight)
				
				print 'driveRight %f' % (driveRight)
				print 'driveLeft %f' % (driveLeft)
		
				PBR.SetMotor1(driveRight * maxPower)
				PBR.SetMotor2(-driveLeft * maxPower)

		PBR.SetLed(PBR.GetEpo())
		playSurface.fill(blackColour)
		fpsClock.tick(30)

	PBR.MotorsOff()
except KeyboardInterrupt:
	PBR.MotorsOff()
print	
