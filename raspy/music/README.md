# Music Lab - beta v0.2.1

Welcome to Music Lab beta version!

It's simple to start: run startMidi.py. However, you need to pre-install four packages: statistics, numpy, mido, pprint.

The program first requires you to input, following the instructions, the path of your midi file. Putting your file directly on desktop is recommended, so that all you have to do is entering "-/Users/*your-user-name*/Desktop/*your-file-name*.mid". The hyphen at the beginning is vital, otherwise your input will be seen as an internal command in Minecraft, thus blocking the program.

After that, the program will let you choose your own way of configuring the redstone system. That is to say, the configuration will be done based on your choice.

If the midi file is successfully processed, you can then enter your in-game name (or another player's name), so that the redstone music system can be constructed beside the corresponding player.

There are some major defects: the tempo always stays the same, which is planned to be changed in the near future. Also, if you require to process a midi file with moments of more than 15 notes playing, you can do so, but you'll have to manually set the base line after the system is attached, as the default way of doing so cannot bring redstone signal to far-away columns.

You are more than welcome to help us fix bugs and create pull requests. Wish happy redstone-music-ing!