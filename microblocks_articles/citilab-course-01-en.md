---
title: "First steps"
url: "https://learn.microblocks.fun/en/activities/citilab-course-01-en"
slug: "citilab-course-01-en"
---

This activity is part of the [Citilab Course](../citilab-course-en). Check it out!

### Introduction

#### What is MicroBlocks

- Microblocks is a free programming environment that allows working with different electronic boards (Citilab ED1, micro:bit, M5Stack-Core, micro:STEAMaker, etc.) and robots (3dBot, CoCube, ED1 Fantàstic, etc).

- The code is visualized on the computer but executed directly on the board. This means that it can be disconnected and continue to function without any additional operation.

- It is available both to install on [different systems](https://microblocks.fun/releases) (Windows, MacOS, Linux) and to use it [online](https://microblocks.fun/run/microblocks.html). There are also versions available to download and run without the need to install (standalone executables).

- The web version has the advantage of always being up to date. The downloadable versions detect boards automatically and are faster.

#### Features ED1 (Front)

#### Features ED1 (Back)

#### Installation and connection with board

- Download the program directly from [here](https://microblocks.fun/download) or go to the web version (a recent version of Chrome or compatible is required).

- With some boards you need to install a driver in case the system does not detect the board automatically. In the case of the ED1, [this driver](https://www.silabs.com/developers/usb-to-uart-bridge-vcp-drivers) is needed.

- If the board is not prepared for microBlocks, it's necessary to install the corresponding firmware with the option update firmware on board on configuration menu .

- Once the computer detects it, the program should automatically connect to the board. In the web version, the connection must be made manually by clicking on the Connect button. In this case a menu appears that requires you to connect via USB via Bluetooth BLE or open Boardie. For now, choose USB, the rest of the options will be explained later.

#### Blocks and libraries

Like many block programming environments, we have a palette of blocks divided into categories.

We also have a number of libraries available, which are collections of blocks with a single purpose. Some of these are made up of other blocks.

By default, the program will load some libraries or others depending on the board connected. If we disable the advanced option auto-load board libraries or load a program that does not include them, they will not appear.

### First steps

#### Let's start programming

- We will start by using the display block of LED Display category by taking it and dragging it to the programming area.

- We will also take the when started block from the Control category and connect it to the previous one.

- Click on the start button or the when started button the to see how it works.

- Unplug the board, connect it to a power source and turning it off and on to check that the program has indeed been saved on it.

##### Challenge 1: Try making other drawings with the screen block

Solution to challenge 1

#### Iterations (I)

- If we want to repeat an action several times, for example making a drawing change to perform an animation, we can use the iteration blocks like forever or repeat _ (among others) that we have in the Control category.

- You will also need to wait a little between the blocks to give time to visualize the changes on the screen, otherwise it will happen too quickly and you won't be able to appreciate it.

##### Challenge 2: Try to make an animation that repeats continuously with the previous blocks

Solution to challenge 2

#### Iterations (II)

- There are other repetition blocks that are also very useful, such as the repeat until _ and the for i in _ block.

- In the first, the repetition is repeated until a condition occurs, for example if we press a button on the board.

- In the case of the second, the value of i will start at 1 and will grow at each iteration until reaching the established value (by default 10). It is also used to iterate through lists, as we will see later.

##### Challenge 3: Try to do an integer count from 5 to 0 with a repeat block.

Solution to challenge 3

And also:

#### Buttons and conditionals

- For this board we have a library available to use the buttons. If it is not loaded automatically, we can add it by clicking on the button(Add Library) and going to Kits and Boards→ED1 Buttons.

- Buttons return a digital value (true or false) represented as a green or red switch. This type of block can be inserted into any other block that has the slot represented in the same way.

- This type of block can be inserted into any other block that has the slot represented with the same shape..

##### Challenge 4: Show a drawing on the screen and clear it using two buttons.

Solution to challenge 4 (when)

Solution to challenge 4 (forever)

### Boardie

- Boardie is a virtual board for MicroBlocks that allows you to test MicroBlocks directly in the browser.

- It is only available in the online version of MicroBlocks.

- It incorporates some common characteristics of real plaques:

5x5 LED display

- Two buttons

- 240x240 graphic screen

- Tons

- Supports HTTP client libray

- Supports Touch Screen library

- File system

- To use Boardie just select the option open Boardie from the connect icon .

- Example of the program Heartbeat

#### More information about Boardie

- [Boardie: A Virtual Board for MicroBlocks](https://microblocks.fun/blog/2022-12-07-boardie-intro/)

- [Making art with MicroBlocks](https://microblocks.fun/blog/2024-08-22-makingart/)

This activity is part of the [Citilab Course](../citilab-course-en).

[Next activity ➡️](../citilab-course-02-en)
