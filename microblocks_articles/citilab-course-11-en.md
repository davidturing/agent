---
title: "Shutter Controlled with Light"
url: "https://learn.microblocks.fun/en/activities/citilab-course-11-en"
slug: "citilab-course-11-en"
---

This activity is part of the [Citilab Course](../citilab-course-en). Check it out!

### Shutter controlled with Light

 Any board with digital connections for the servos and sensor light (micro:bit, micro:STEAMMakers and others). The TFT screen will be used for the simulation of the shutter (Citilab ED1, M5Stack-Core and others).

#### Defining your own blocks

- Once the control with the buttons is done, it can be changed to any other type of sensor, such as a light sensor, a remote, a control via the Internet or a mobile application.

- Adding an extra control that is compatible with button control requires complicating the program structure.
That's why they recommend defining their own blocks to help simplify the code before starting this process.

#### How tow create blocks

- To create your own blocks, you must use the Add a command block or Add a reporter block buttons from the My Blocks category. If the block must return a value, you must choose the reporter block button and it is necessary to include one or more return _ blocks from the Control category.

- MicroBlocks asks us for the name of the block and will make a new one, shaped like a hat, to which we can attach the blocks that define the action of the new block.

- By clicking with the mouse on the block definition we can add parameters to our block.

- Once defined, the blocks can be thrown away (they are not deleted) and thus we will be left with the new program that is easier to understand, to modify and to expand.

To modify the block definition right click with the mouse over the block and choose show block definition.

#### The sensor reading must be done at intervals

- In this case we will use the light level block that we will find in the Sensors category.

- The reading of the sensor must be done with large time intervals, to give time to fully raise and lower the blind and also avoid minimal changes in lighting.

- It might be interesting to define a block to wait minutes instead of milliseconds.

##### Challenge 1: Complete the shutter project with keyboard control and light sensor. The shutter stops if either button is pressed.

Solution to challenge 1

This activity is part of the [Citilab Course](../citilab-course-en).

[⬅️ Previous activity](../citilab-course-10-en)
[Next activity ➡️](../citilab-course-12-en)
