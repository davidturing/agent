---
title: "Controlling Lights with Hand Claps"
url: "https://learn.microblocks.fun/en/activities/citilab-course-12-en"
slug: "citilab-course-12-en"
---

This activity is part of the [Citilab Course](../citilab-course-en). Check it out!

### Controlling lights with hand claps

 Some boards have a built-in microphone: micro:bit V2, micro:STEAMakers, M5Stack-Core2 and others. For the Citilab ED1 and others you need to connect a microphone.

#### Detecting clap count

- With the Sensing→Microphone library it is possible to detect the number of times one claps their hands.

- This detection allows us to activate any element of the home display, for example the lighting.

- For Citilab ED1 and other borads the microphone is connected to the analog input A1.

The block to use it's clap count. It's important not to have other sounds that might interfere with detection.

#### Activate the lights

- To simulate different lighting levels we can use leds, neopixels or the screen.

- We can use the fill display with _ block that we will find in the Graphics and Displays→Turtle library instead of draw rectangle ... from the TFT library.

##### Challenge 1: Build a program with different lighting levels controlled by clapping your hands.

Solution to challenge 1

 For boards with LED screen that allows color change (Citilab ED1, micro:STEAMakers, M5Stack-Core and others) we can define a new block, using the advanced block set display color _.

This activity is part of the [Citilab Course](../citilab-course-en).

[⬅️ Previous activity](../citilab-course-11-en)
[Next activity ➡️](../citilab-course-13-en)
