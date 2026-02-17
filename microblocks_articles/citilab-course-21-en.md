---
title: "Animal sounds game (images and audio)"
url: "https://learn.microblocks.fun/en/activities/citilab-course-21-en"
slug: "citilab-course-21-en"
---

This activity is part of the [Citilab Course](../citilab-course-en). Check it out!

### Playing Audio with MicroBlocks

 Only for boards with sound and a file system, such as ED1, micro:STEAMakers, M5Stack-Core, and others.

- In other activities, we have seen how to generate sounds, for example, using the Tone or Ringtone libraries.

- With MicroBlocks, it is possible to play audio files stored on the board using the WAV library from the Sound category.

- The WAV library allows playing audio files in WAV format. This library does not support compressed files.

- The file must be prepared in advance to reduce its size. Once ready on the computer, it should be uploaded to the board’s file system.

#### Preparing WAV Files

- To minimize storage space or convert another file format to WAV, it is recommended to use the free software [Audacity](https://www.audacityteam.org/) or an [online converter](https://audio.online-convert.com/convert-to-wav).

- Recommended settings to balance audio quality and file size: mono files, a sample rate of 22050 Hz, and 8-bit quantization.

##### Using Audacity

- From the File menu, select the option Export Audio….

- Choose the format WAV (Microsoft) and in the audio options, select Channels: mono, Sample rate: 22050 Hz, and Encoding: Unsigned 8-bit PCM.

- If the file's sample rate is lower than 22050 Hz, increasing it provides no benefit, and the file takes up more space.

##### Using Online-Converter

- On the [Online Converter](https://audio.online-convert.com/convert-to-wav) website or similar, upload the audio file (mp3, ogg, wav, aac, mp4, etc.), select the recommended settings, and save the file to the computer.

- Audio files take up significant filesystem space. A 30-second file at 22050 Hz, stored at 8 bits, takes up approximately 600 KB. Since the total file storage space on an ED1 is 2 MB, this allows for a maximum of 2 minutes of audio.

- For smaller file sizes, use short audio and trim silent sections at the beginning and the end.

#### Uploading the Sound File to the Board

- The easiest way to upload the file is by dragging it directly into MicroBlocks.

- Another method is by enabling MicroBlocks’ advanced options. Click the options icon and select advanced mode. Then, in the file icon , choose put file on board, and select the file from the computer.

#### Playing Audio in MicroBlocks

- Once the library is loaded, it contains a single block, play WAV file _, where you enter the audio file name.

Clicking on the block will play the WAV file through the board’s speaker.

### Displaying Images with MicroBlocks

 Only for boards with a file system and a TFT screen, such as ED1, M5Stack-Core, CoCube, Boardie, and others.

- With MicroBlocks, it is possible to display image files stored on the board using the BMP library from the Graphics and Displays category.

- The BMP library allows displaying BMP (Bitmap) images.

- The file must be prepared beforehand to fit the screen and reduce its size. Once ready on the computer, it should be uploaded to the board’s file system.

#### Preparing BMP Files

- To minimize storage space or convert another file format to BMP, it is recommended to use the free software GIMP or an [online converter](https://image.online-convert.com/convert-to-bmp).

##### Preparing the Image with GIMP

- First, resize the image to fit the screen. If the image is larger, only a portion will be displayed, and it will take up more space. Select Scale Image… from the Image menu and enter the screen dimensions (e.g., for ED1: 128x128).

- If the image proportions do not match the screen, crop it using Canvas Size in the Image menu.

- Finally, save the image as a BMP file. Use File → Export As, choose the location and filename with a BMP extension, then open Advanced Options in the Export BMP Image dialog, and select any 16-bit option.

- If the image is in 8-bit format or less, no options appear in the advanced settings; simply click the Export button.

### Animal Sounds Game

- Before programming the game, we need to load the images and sounds. Simply drag them into MicroBlocks or use put file on board from the File icon . Advanced options must be enabled to use this feature.

- To check that everything is correct, use the file names block from the Others → Files library.

- In the same library, we find the file system data block which shows information about the space used and the total.

#### Displaying the Animals

- To display an animal, use the display BMP file _ at x _ y_ block from the Graphics and Displays → BMP library.

- Create a list with the animals names and a bmp variable to easily switch images.

- Next, use the left and right buttons to switch animals. The bmp variable values must be limited.

#### Playing Animal Sounds

- To play audio files, we’ve already seen that you need to use play WAV file _ block from the Sound → WAV library..\n\n- This time, use the up and down buttons and a wav variable to control the audio file to play.

#### End of the Game

- Finally, ensure that the displayed image and the sound match. Pressing the OK button will check whether the bmp and wav variables are the same.

- If correct, the animal will be removed from the list, and a random one will be displayed and played.

- Voices in WAV format can be added to confirm if the answer is correct or wrong. The voices in the example were generated using [TTSMaker Free Text to Speech](https://ttsmaker.com/).

#### Final Challenge: Complete the Game!

Solution to the Final Challenge

- [Image and sound Files](animals-eng.zip)

- [Source code](animals-eng.ubp)

- Images were sourced from:
[https://en.wikipedia.org/wiki/Template:Emoji/Gallery](https://en.wikipedia.org/wiki/Template:Emoji/Gallery)

- Sounds were sourced from:
[https://en.wikipedia.org/wiki/List_of_animal_sounds](https://en.wikipedia.org/wiki/List_of_animal_sounds)

This activity is part of the [Citilab Course](../citilab-course-en).

[⬅️ Previous activity](../citilab-course-20-en)
[Next activity ➡️](../citilab-course-22-en)
