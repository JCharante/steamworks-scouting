### Potential Modules

* A way to generate who scouts who while still covering at least 3 matches per team.
* A way to keep record data for a team for a certain match
* A way to view the data for a team for all their matches
* (Optional) A way to calculate who would be a good alliance for a given team. 
* Gambling


### Event Setup Service

* Create Events
* Add matches to events (as soon as we get the paper with the match schedule)
* Add teams to matches
* Add teams to Events


#Stuff to Track:

### Per Team

- Notes
- Robot(s)


### Per Robot

- What type of robot (Gear, Defender, Highschol & Lowgoal)
- Notes

### Per Team Per Match

- Low Goal = (-1 = bad | 0 = neutral | 1 = good)
- High Goal = (-1 = bad | 0 = neutral | 1 good)
- Gears = Integer
- Autonomous Gear Placing Position = Left, Middle, Right, or Can't
- Climbing Rating = (1 = They Can't, 2 = They can but are slow/don't really do it, 3 = It takes them 15s or less, 4 = Almost instant climbing (hitting rope and going up))

### Per Match
- Red RP Gain = Int
- Blue RP Gain = Int
- Red Team Members = List[int]
- Blue Team Members = List[int]