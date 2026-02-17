---
title: "Controlling the Fantastic Robot with Infrared"
url: "https://learn.microblocks.fun/en/activities/citilab-course-16-en"
slug: "citilab-course-16-en"
---

This activity is part of the [Citilab Course](../citilab-course-en). Check it out!

### Controlling the Robot with Infrared

#### Infrared communication

- In this unit we will see how to control the robot wirelessly using infrared technology.

- This technology is based on sending infrared waves between two LEDs (one emitter and one receiver).

- As the ED1 board has an infrared receiver built in, we can use any television remote control or a generic one to send commands to it.

 Other boards need to connect to an infrared receiver. There are many models and they are quite economical.

#### Infrared library

- In order to be able to use the infrared receiver on the board, you need to import the IR Remote library under the Other folder.

- Although there is a block to initialize the receiver in our case it is not needed, since the block to receive codes calculates it automatically. It would only be necessary if you have another board and an external receiver.

- To receive codes you just need to use the corresponding block and press a button on the remote to test if it works.

##### Challenge 1: Make a program that moves the robot with the remote.

Solution to challenge 1

This activity is part of the [Citilab Course](../citilab-course-en).

[⬅️ Previous activity](../citilab-course-15-en)
[Next activity ➡️](../citilab-course-17-en)
