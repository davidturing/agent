---
title: "Fantastic Robot with Memory"
url: "https://learn.microblocks.fun/en/activities/citilab-course-15-en"
slug: "citilab-course-15-en"
---

This activity is part of the [Citilab Course](../citilab-course-en). Check it out!

### Fantastic Robot with Memory

#### Lists

- To make the robot able to reproduce a few commands in a row, it is necessary to save them beforehand.

- We have already used variables to store numbers or texts. In this case we will use one to store a list of commands.

- Lists allow us to save a set of data that we can access individually.

- The Data category blocks are used to manipulate the lists.

#### Saving and deleting commands

- The block add _ to list _ allows you to add items to a list, on the other hand with the block delete item _ of list _ you can delete one, the last or all the items from the list .

- Our robot will have to empty the command list when starting or when we press the X button. This can be done by saving an empty list to the variable, or using the delete item _ of list _ block with the all option selected.

- Each movement button will save an identifier of the corresponding order. The wait 500 millisecs block prevents many commands from being added when a button is pressed.

#### Selecting and executing commands

- In the commands list we have the sequence of movements that we want the robot to execute. For example:

- To access a command, use the block item _ of _.

- The control block for i in _ allows iterating through the list. The value of i corresponds to each of the saved items or commands.

- All that remains is to move the engines based on the commands in the list with the OK button.

##### Challenge 1: Program the robot with memory.

Solution to challenge 1

#### Child ED1 robot

- The program used in schools with the Fantastic robot adds sounds and images to the screen to improve interactivity.

- You can download it from [here](https://cloud.citilab.eu/s/Z626GxdFRLQCYyz).

https://www.youtube.com/watch?v=ZGvE_8RV73w

This activity is part of the [Citilab Course](../citilab-course-en).

[⬅️ Previous activity](../citilab-course-14-en)
[Next activity ➡️](../citilab-course-16-en)
