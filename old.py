#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Dec 14 11:10:01 2019

@author: Denis Moura - github.com/mouradap


Under MIT License

Copyright 2019 Denis Moura

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""

import pygame
import random
import math
from pygame import mixer


#initiatialization of pygame
pygame.init()

#creating a screen

screen = pygame.display.set_mode( (800, 600)) #screen resolution

#Title and Icon
pygame.display.set_caption('Space Invaders')
icon = pygame.image.load('ufo.png')
pygame.display.set_icon(icon)

#Background
background = pygame.image.load('background.png')

#Background song
mixer.music.load('backgroundMusic.wav')
mixer.music.play(-1) #-1 plays on loop



#Player
playerImg = pygame.image.load('spaceship.png')
playerX = 370
playerY = 480
playerXchange = 0
# playerYchange = 0

#One enemy
# enemyImg = pygame.image.load('enemy.png')
# enemyX = random.randint(0,734)
# enemyY = random.randint(0,150)
# enemyXchange = 3
# enemyYchange = 40

#Multiple enemies
enemyImg = []
enemyX = []
enemyY = []
enemyXchange = []
enemyYchange = []
enemyNum = 6

for i in range(enemyNum+1):
	enemyImg.append(pygame.image.load('enemy.png'))
	enemyX.append(random.randint(0,734))
	enemyY.append(random.randint(0,150))
	enemyXchange.append(3)
	enemyYchange.append(40)

#Bullets

bulletImg = pygame.image.load('bullet.png')
bulletX = 0
bulletY = 480
bulletYchange = 10
bulletState = 'ready'

#Score
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)

textX = 10
textY = 10

#GameOver
fontOver = pygame.font.Font('freesansbold.ttf', 64)


def player(x,y):
	screen.blit(playerImg, (x, y))

# #One enemy function
# def enemy(x,y):
# 	screen.blit(enemyImg, (x, y))
#Multiple enemies function	
def enemy(x,y, i):
	screen.blit(enemyImg[i], (x, y))

def fireBullet(x,y):
	global bulletState
	bulletState = 'fire'
	screen.blit(bulletImg, (x + 16,y + 10))

def enemyHit(enemyX, enemyY, bulletX, bulletY):
	distance = math.sqrt( ( math.pow( enemyX - bulletX, 2 ) ) + ( math.pow( enemyY - bulletY , 2 ) ) )
	if distance < 27:
		return True
	else:
		return False

def showScore(x,y):
	score = font.render('Score : ' + str(score_value), True, (255, 255, 255) )
	screen.blit(score, (x, y))

def gameOverText():
	overText = fontOver.render('GAME OVER', True, (255, 255, 255) )
	screen.blit(overText, (200, 250))


#Game loop
running = True

while running:

	screen.fill((0,0,0)) #RGB values
	#background image
	screen.blit(background,(0,0))

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False

		#If keystroke is pressed, check whether if it's right or left.
		if event.type == pygame.KEYDOWN:

			if event.key == pygame.K_LEFT:
				playerXchange = -5
			if event.key == pygame.K_RIGHT:
				playerXchange = 5
			# if event.key == pygame.K_UP:
			# 	playerYchange = -5
			# if event.key == pygame.K_DOWN:
			# 	playerYchange = 5

			if event.key == pygame.K_SPACE:
				if bulletState is 'ready':
					bulletSound = mixer.Sound('shot.wav')
					bulletSound.play()
					bulletX = playerX
					fireBullet(bulletX, bulletY)

		if event.type == pygame.KEYUP:
			if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
				playerXchange = 0
			if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
				playerYchange = 0



	playerX += playerXchange
	if playerX <= 0:
		playerX = 0
	elif playerX >= 736:
		playerX = 736
	# playerY += playerYchange
	# if playerY <= 0:
	# 	playerY = 0
	# elif playerY >= 536:
	# 	playerY = 536

# #Enemy movement	- one enemy
# 	enemyX += enemyXchange
# 	if enemyX <= 0:
# 		enemyXchange = 3
# 		enemyY += enemyYchange
# 	elif enemyX >= 736:
# 		enemyXchange = -3
# 		enemyY += enemyYchange	

#Enemy movement multiple enemies
	for i in range(enemyNum):

		#If gameOver
		if enemyY[i] > 440:
			for j in range(enemyNum):
				enemyY[j] = 2000
			gameOverText()
			break


		enemyX[i] += enemyXchange[i]
		if enemyX[i] <= 0:
			enemyXchange[i] = 3
			enemyY[i] += enemyYchange[i]
		elif enemyX[i] >= 736:
			enemyXchange[i] = -3
			enemyY[i] += enemyYchange[i]


#Collision for multiple enemies
		collision = enemyHit(enemyX[i], enemyY[i], bulletX, bulletY)
		if collision:
			explosionSound = mixer.Sound('explosion.wav')
			explosionSound.play()
			bulletY = 480
			bulletState = 'ready'
			score_value += 10
			enemyX[i] = random.randint(0,734)
			enemyY[i] = random.randint(0,150)

		enemy(enemyX[i],enemyY[i], i)

#Bullet movement
	if bulletState is "fire":
		fireBullet(bulletX,bulletY)
		bulletY -= bulletYchange
		if bulletY <= 0:
			bulletY = 480
			bulletState = 'ready'

# #Collision for one enemy
# 	collision = enemyHit(enemyX, enemyY, bulletX, bulletY)
# 	if collision:
# 		bulletY = 480
# 		bulletState = 'ready'
# 		score += 10
# 		print('Player score increased!')
# 		print('New score: ' + str(score) + ' points.')
# 		enemyX = random.randint(0,734)
# 		enemyY = random.randint(0,150)


	player(playerX,playerY)
	showScore(textX, textY)
# #One enemy
# 	enemy(enemyX,enemyY)
	pygame.display.update()