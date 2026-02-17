---
title: "Shutter Controlled with Buttons"
url: "https://learn.microblocks.fun/en/activities/citilab-course-10-en"
slug: "citilab-course-10-en"
---

This activity is part of the [Citilab Course](../citilab-course-en). Check it out!

### Shutter controlled with buttons

 Any board with digital connections for the servos (micro:bit, micro:STEAMMakers and others). The TFT screen will be used for the simulation of the shutter (Citilab ED1, M5Stack-Core and others).

#### DC motors

- Motors are devices that transform electrical energy into mechanical rotational motion.

- DC motors do use direct current to operate.

- Motors that use alternating current to operate, are called AC motors.

#### Servo motors

- A servomotor is a direct current (DC) motor whose behavior can be controlled thanks to a small electronic board and a set of gears.

- Although there are different types of servomotors, the way to control them is the same: by means of an electric pulse with a specific duration.

- Depending on the duration of this pulse, the servomotor will turn to a certain angle (standard) or it will turn continuously to one side or the other (continuous rotation).

- These servomotors consume about 100-200 mA and can reach 500mA at the time of start-up or change of direction. You must avoid giving commands to the engines while they are turning.

- The servomotor can be connected to any of the digital outputs, although D1 and D2 give 3.3V and therefore the servomotor works with less power, while D3 and D4 work at 5V. The D4 output is connected internally to the speaker and small noises may occur.

- Important! If using outputs 3 and 4 on an ED1 prior to version 2.3 it is recommended to do so with battery and the switch in "ON".

#### Angular servomotors

- Standard or angular servomotors move a specific angle between 2 values. The most typical is SG90 which moves between 0 and 180º, taking about 150ms to make this angle. This engine does not spin!

- It comes with a series of accessories that allow you to connect with gears or attach to other elements.

- The angular servomotors we will use are the SG90, a small and very affordable model.

#### Angle control by pulse width

- To set the angle, a pulse is sent every 20 ms. According to the duration of the pulse, the servo changes the angle. It is a pulse width modulation (PWM).

- If the duration is approximately 1ms the servo is placed at an angle of 0º and if it is 2ms at 180º.

- Once the angle is set, the servomotor does not move even if we send more pulses.

##### Challenge 1: Make a program that makes the servo move from one angle to another, alternately

 Hint: you need to use the advanced block wait _ microseconds from the Control category.

Solution to challenge 1

#### Servo library

- To work with servomotors it is more practical to use the Servo library.

- The set servo _ to _ degrees (-90 to 90) block is used with the angle motors, whereas the set servo _ to speed _ (-100 to 100) is used with continuous rotation motors.

##### Challenge 2: Control a continuous rotation motor with the up and down button

Solution to challenge 2

#### Home automation

- It's the application of different technologies to improve housing, especially to improve energy efficiency.

- It can also be applied to the improvement of schools, public buildings or even cities.

- As an example, we will make a shutter that is controlled by the level of light and a lighting system that can be set in motion with the snap of a hand.

#### Shutter simulation

- We will use a simple drawing on the screen to simulate a shutter, whose height will vary according to the value of the y variable.

- In a real case we should use limit switches that indicate that the shutter has reached the upper and lower limits. Here we will do this control by program using the value of the variable (0 = upper, 127 = lower).

##### Challenge 3: Simulate a shutter (with screen and servo motor) controlled by the up and down buttons.

Solution to challenge 3

This activity is part of the [Citilab Course](../citilab-course-en).

[⬅️ Previous activity](../citilab-course-09-en)
[Next activity ➡️](../citilab-course-11-en)
