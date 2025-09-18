from peewee import *
import pygame, sys
from pygame.locals import *
from pygame import *
from pygame.font import Font
import random

db = MySQLDatabase(
    'wackamole',
    host='localhost',
    port=3306,
    user='root',
    password='root'
)

class BaseModel(Model):
    class Meta:
        database = db

class Scores(BaseModel):
    #ScoreID = AutoField(). # Peewee automatically handles primary keys
    ScoreName = CharField()
    ScoreVal = IntegerField()

try:
    db.connect()
except:
    print("it didn't connect :)")

#this number is how many it will print later
scores = [None for _ in range(3)]
scoreVals = [None for _ in range(3)]

cursor = db.execute_sql("select scores.scorename, scores.scoreval from scores order by scores.scoreval desc limit 3")

i = 0
for row in cursor.fetchall():
    scores[i] = row[0] + " " + str(row[1])
    scoreVals[i] = row[1]
    print(scores[i])
    i += 1

db.close()
