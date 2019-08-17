# Music Lab - beta v0.4.0

Welcome to Music Lab beta version!

It's simple to start: run start_midi.py (when there's a server running and Minecraft 1.12.2 running it). However, you need to pre-install three packages: mido, statistics, numpy.

The program first requires you to input, following the instructions, the path of your midi file. Putting your file directly on desktop is recommended, so that all you have to do is entering "-/Users/*your-user-name*/Desktop/*your-file-name*.mid". The hyphen at the beginning is vital, otherwise your input will be seen as an internal command in Minecraft, thus blocking the program.

After that, the program will let you choose your own way of configuring the redstone system. That is to say, the configuration will be done based on your choice.

If the midi file is successfully processed, you can then enter your in-game name (or another player's name), so that the redstone music system can be constructed beside the corresponding player.

Note that midi files with moments of more than 28 notes playing will not be processed, because for now, the redstone music system, if placed, cannot be initiated with all columns running, due to an algorithm defect of the program.

You are more than welcome to help us fix bugs and create pull requests. Wish happy redstone-music-ing!