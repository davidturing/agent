---
title: "Controlling the Fantastic Robot with WiFi"
url: "https://learn.microblocks.fun/en/activities/citilab-course-17-en"
slug: "citilab-course-17-en"
---

This activity is part of the [Citilab Course](../citilab-course-en). Check it out!

### Controlling the Robot with WiFi

#### WiFi connection

- To connect the board to a WiFi network or create one of your own, you need to import the WiFi library that is inside the Network folder.

- Once the library is open, we will use the corresponding block to connect to a Wi-Fi network by entering both the name of this network and the password.

- If we want to see the IP address assigned by the network to the board, we can use the IP address block.

##### Challenge 1: Make a program that displays the IP address on the screen

Solution to challenge 1

#### Web server

- To start a web server, you need to import the HTTP Server library which is also in the Network folder.

- The basic blocks to be able to manage requests to the server and to send responses are those of HTTP server request, path of request _ and respond _ to HTTP request.

#### Receiving requests

- When a client connects to the HTTP server, its request is recorded in the HTTP server request block.

- As they are actually text strings, one way to see if there is a request or not is to check that this block returns an empty result.

- If you also want to respond with a text, click on the arrow in the respond _ to HTTP request block and then change the text of the content.

##### Challenge 2: Run a web server on the board that responds with text to any request

Solution to challenge 2

#### Application path

- For a web server to perform different actions according to the request received, routes or paths are used.

- The path of a web request is the text that we put after the name of an IP address or web domain in the browser bar, including the slash (/).

- It is important to know that the HTTP server request block is emptied every time it is used, so you need to save its result to be able to work with it (for example with a variable).

##### Challenge 3: Make a web server that acts as an "echo", answering the same path text

Solution to challenge 3

#### Manage requests

- Now that we know how to identify the path used in the request we can make the board do things besides respond via web.

- For example we can turn on or off the integrated LED of the sending board by specifying the "on" and "off" commands through the path to the request.

- It's important to add a block that responds with something by default if you don't use any of the established paths, otherwise the browser will hang waiting for a response.

##### Challenge 4: Make the robot move by sending commands through the browser

Solution to challenge 4

- For more advanced web server examples, including graphs and even data export, please refer to the [BME680 Demo](https://bitbucket.org/john_maloney/smallvm/src/stable/gp/Examples/Network/BME680%20Demo.ubp) and [Databot Data Logger](https://bitbucket.org/john_maloney/smallvm/src/stable/gp/Examples/Network/Databot%20Data%20Logger.ubp) examples in the Network folder.

This activity is part of the [Citilab Course](../citilab-course-en).

[⬅️ Previous activity](../citilab-course-16-en)
[Next activity ➡️](../citilab-course-18-en)
