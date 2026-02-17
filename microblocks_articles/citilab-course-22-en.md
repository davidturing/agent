---
title: "BLE Telesketch"
url: "https://learn.microblocks.fun/en/activities/citilab-course-22-en"
slug: "citilab-course-22-en"
---

This activity is part of the [Citilab Course](../citilab-course-en). Check it out!

### BLE Telesketch

Only for boards with Bluetooth BLE, a TFT screen, and an accelerometer, such as the ED1, M5Stack-Core, Co-Cube, and others. A simpler version can also be made for boards with an LED display, such as the micro:bit or micro:STEAMakers.

- The Telesketch, or Etch A Sketch, is a toy that became popular in the 1960s. It allowed users to draw on a screen that simulated a television. It had two knobs that controlled the horizontal and vertical movement of the cursor. To erase the drawing, there was a button that cleared the entire screen.

CC BY-SA 3.0, https://commons.wikimedia.org/w/index.php?curid=623459

- In this activity, we'll build a collaborative version of the Telesketch by using the ability to connect multiple boards via BLE (Bluetooth Low Energy).

#### Building the game without connection

- We'll start by building the game without the BLE connection.

- The first step is to define two variables, x and y, to store the coordinates of a circle that we'll randomly position on the TFT screen.

- Using the accelerometer, we'll make the circle move across the screen by tilting the board.

- For example, when the tilt x is below a certain value, we move left by decreasing the x coordinate.

##### Challenge 1: Complete the circle movement

Solution to challenge 1

- Since this will be a collaborative Telesketch, each participant will have their own color. For this reason we define a variable color with a random value.

- To ensure the color isn't too dark and remains visible on the screen, we use the _ with brightness _ % block from the Color library, setting it to 90% brightness.

- To clear the screen, we'll use the accelerometer to detect a shake gesture.

#### BLE Radio

- To communicate between boards, we'll use the BLE Radio library. BLE support must be enabled on the board. If the board has an LCD screen, it will display a three-letter BLE identifier on startup. We can also use the BLE identifier block in the Input category to check this value.

- To enable or disable this functionality, click the options icon and select enable or disable BLE.

- BLE communication is very simple and does not require device pairing. The range is limited to about 10 meters.

- Next, we import the BLE Radio library.

- To send a string, we use the ble send string _ block.

- To receive data, we need two blocks: ble message received? and ble last string, placed inside a loop block.

- The text is received by all boards connected via BLE Radio, except the board that sends the message.

##### Sending and receiving circle coordinates

- To send the coordinates, we construct a text containing all the information using the join _ _ block from the Data category.

- To receive the coordinates, we split the received text using the split _ by _ block and draw the circle with the received coordinates.

#### Final Challenge 1: Complete the collaborative Telesketch!

Solution to final challenge

- The way the circle is shown has been slightly modified to make it blink a bit, helping to distinguish our own drawing.

- BLE data transfer is slow, and messages can occasionally be lost, especially with many devices connected. You can adjust the wait time at the end of the ble send pair _=_ block to make the received drawings more continuous.
ble

- As mentioned, BLE messages are received by all boards. It's possible to send messages to a specific group of boards using the ble set group _ (0–255) block. Only boards in the same group will communicate.

### Communication with OctoStudio

For boards with Bluetooth BLE, LED screen, and accelerometer, such as the ED1, M5Stack-Core, micro:bit, micro:STEAMakers, Co-Cube, and others.

- OctoStudio is a free mobile app for block-based programming, developed by the creators of Scratch at the MIT Media Lab.

- It's specially designed for children aged 7 and up and it's available for Android and iPhone. Unlike App Inventor, it does not generate standalone apps.

- One of OctoStudio's interesting features is that it includes a device-to-device communication method, similar to BLE Radio.

- Only eight different figures can be sent, but this is more than enough for many simple applications. Like BLE Radio, it also supports channels.

#### Figure race in OctoStudio

- To demonstrate communication between OctoStudio and MicroBlocks, we'll create a race for up to 4 players who move their character by shaking their board. Let's see who gets to the finish line first!

- First, place the character at the starting line and adjust its size if necessary.

- Then, wait for a BLE signal corresponding to their figure to move forward a few steps.

- Finally, we'll detect when a character touches the finish line and prevent others from continuing. We'll also emit a circle so boards receive a MicroBlocks signal that the race is over.

#### Figure race in MicroBlocks

- In MicroBlocks, use the OctoStudio library from the Network category.

- To send a beam, use the Octo beam _ to phones block.

- The character is chosen at random from a list of figure names (in English). We use the name to show the character on the screen with the display image _ block from the LED Display library.

- To receive a beam, use the Octo beam received ? and Octo last beam blocks. In this case, we create a variable named finished, which activates when a circle is received from the OctoStudio app.

#### Final Challenge 2: Complete the figure race in both OctoStudio and MicroBlocks

Solution to final challenge

- [Figure race – OctoStudio app](figure-race.octostudio)

This activity is part of the [Citilab Course](../citilab-course-en).

[⬅️ Previous activity](../citilab-course-21-en)
