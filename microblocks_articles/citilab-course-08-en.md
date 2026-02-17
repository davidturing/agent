---
title: "Parking Alarm"
url: "https://learn.microblocks.fun/en/activities/citilab-course-08-en"
slug: "citilab-course-08-en"
---

This activity is part of the [Citilab Course](../citilab-course-en). Check it out!

### Parking alarm

#### Distance sensor VL53L1X

- In this activity we will work with a distance sensor, with a measurement range between 4 and 400 cm.

- This is a sensor that measures the time it takes for a laser to bounce off the surface to be measured (Time of Flight TOF).

- It is a digital sensor, and it is connected via the I²C serial bus. The I²C connection needs 4 cables, two for power and two for sending and receiving signals.

#### Distance sensor connection (I²C)

 Boards:
Citilab ED1 (before 2.2 version), micro:bit i micro:STEAMakers with adapter.
Citilab ED1 (version 2.2 and higher), M5Stack-Core direct connexion.

- The sensor has a Groove connector and an adapter is needed for the ED1.

- Black corresponds to GND (Ground).

- The red corresponds to the 5V (it is important not to cross the GND and the 5V as the sensor or the board can be damaged).

- The other connections are represented with white and yellow colors. In the case of the adapters indicated, the white goes to the SDA connector of the ED1 and the yellow to the SDL connector (they are crossed in relation to the colors drawn on the sensor).

- Starting with version 2.2 of the ED1 board and other boards with the Groove connector, the sensor can be connected directly.

#### VL53L1X library

- The library for this sensor is in the Sensing category with the name Distance (VL53L1X).

- Just add 2 blocks one that returns the distance in millimeters and another that tells us if the sensor is connected.

##### Challenge 1: Make a program that displays the distance in mm per screen

Solution to challenge 1

#### Tone Library

 Boards: Citilab ED1, micro:bit V2, micro:STEAMakers, M5Stack-Core, Boardie i altres amb altaveu incoprorat.

- Microblocks incorporates a library for cards that support the generation of sounds. This is the Tone library. In the case of the ED1, it is loaded automatically.

- The basic block is play frequency _ for _ ms which plays for the specified time, a tone at the specified frequency.

- The values ​​that the ED1 mini speaker can reproduce are between 100 and 10,000 Hz. The maximums perceptible by the human ear are between 20 and 20,000 Hz.

#### Play notes

- The block play note _ octave _ for _ ms allows you to play musical notes in both Anglo-Saxon and European notation.

- In the Music folder of the examples, that can be opened using the Open option under the file menú , you can find several projects that play melodies.

- The Ringtone library allows you to play melodies in RTTTL format from Nokia. Exemples [1](http://microblocks.fun/mbtest/NokringTunes.txt) [2](http://www.fodor.sk/spectrum/rttl.htm).

#### Parking sensor

- The reverse parking sensors measure the distance and generate visual and acoustic signals to warn of the proximity of an obstacle.

- Our sensor does not detect very short or very long distances (2-100 cm) and therefore we will have to take this into account in our code.

- We can define multiple conditions with _ and _ and _ or _ operators.

##### Challenge 2: Make a visual and audible parking sensor

Solution to challenge 2

This activity is part of the [Citilab Course](../citilab-course-en).

[⬅️ Previous activity](../citilab-course-07-en)
[Next activity ➡️](../citilab-course-09-en)
