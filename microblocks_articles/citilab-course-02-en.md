---
title: "Sensors"
url: "https://learn.microblocks.fun/en/activities/citilab-course-02-en"
slug: "citilab-course-02-en"
---

This activity is part of the [Citilab Course](../citilab-course-en). Check it out!

### Sensors

 Boards: Citilab ED1, micro:bit, micro:STEAMakers, M5Stack-Core.

#### Sensors and relational operators

- In addition to the buttons, the ED1 board incorporates different sensors: light, temperature, tilt, etc.

- Given that these sensors give an analog value (that is, numerical) we will have to use relational blocks if we want to execute actions related to it.

- These blocks also return a true or false value, so they can be used with the conditional blocks we saw earlier.

##### Challenge 1: Show two different patterns on the screen by covering and uncovering the light sensor

Solution to challenge 1

#### Temperature sensor

- Another sensor integrated into the board is the temperature sensor.

- A very simple example that can be done is to add to the graph the value that the sensor gives us every X time (for example 1 second) to visualize it comfortably.

- We can even export the data in .csv format and open it with a spreadsheet program (MSOffice, LibreOffice, etc.)

#### Experiment on Weightlessness

- We can use the acceleration sensor to conduct an experiment on weightlessness, which occurs when an object enters free fall.

- The acceleration due to gravity is 9.8 m/s². When at rest, the acceleration block returns approximately 98 (it is multiplied by 10 since MicroBlocks does not use decimals).

- If we throw an object upwards, just before it starts falling, it will experience a moment of apparent gravity equal to 0. This is what happens during parabolic training flights or what astronauts experience due to their constant state of free fall.

- In our experiment, we will throw the board upwards so it can record the acceleration value during its motion.

- If we try the experiment, we will see that a wired connection can be an issue. However, using boards with Bluetooth BLE, we can connect and program with MicroBlocks wirelessly.

- To do this, we need to use the online version of MicroBlocks, which only works with Chrome or compatible browsers.

- The Bluetooth name of the board is "MicroBlocks" followed by three uppercase letters.

- Once the connection is established, we can work with MicroBlocks just as we would with a wired connection and carry out our experiment!.

- In the graph, we can observe a brief moment where the apparent gravity is close to 0, meaning a condition of weightlessness occurs.

- For Bluetooth BLE connection on Linux, the [Web Bluetooth option](chrome://flags/#enable-web-bluetooth) must be enabled in the browser.

This activity is part of the [Citilab Course](../citilab-course-en).

[⬅️ Previous activity](../citilab-course-01-en)
[Next activity ➡️](../citilab-course-03-en)
