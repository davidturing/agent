---
title: "Theremin"
url: "https://learn.microblocks.fun/en/activities/citilab-course-09-en"
slug: "citilab-course-09-en"
---

This activity is part of the [Citilab Course](../citilab-course-en). Check it out!

### Theremin

#### Theremin

- The [Theremin](https://ca.wikipedia.org/wiki/Theremin) is an electronic musical instrument that is played with the hands but without contact.

- The tone of the instrument varies depending on the distance to the hand. Use the other hand to adjust the volume.

https://www.youtube.com/watch?v=_YYABE0R3uA

#### Theremin without volume control

 Boards: Citilab ED1, micro:bit, micro:STEAMakers, M5Stack-Core, Boardie and others with integrated speaker.

- We will use the touch block play frequency _ for _ ms, adapting the distance values 0-500) to the frequency values 100-5000).

- We will notice that the sound is not continuous, as the sensor takes time to read. To solve it, you need to make two separate programs, one that does the reading and another that reproduces the sound.

##### Challenge 1: Make a Theremin, without volume control, with the distance sensor.

Solution to challenge 1

#### Theremin with volume control

 Boards: Citilab ED1, micro:bit V2, micro:STEAMakers, M5Stack-Core and others with DAC or fast PWM.

- To adjust the volume of the generated tone we can use the Other→System→sound Prims library.

- With the DAC write _ block we can generate a wave of the desired frequency where the volume is affected by the values;

- We can connect a potentiometer to analog pin 1 to control the volume.

This activity is part of the [Citilab Course](../citilab-course-en).

[⬅️ Previous activity](../citilab-course-08-en)
[Next activity ➡️](../citilab-course-10-en)
