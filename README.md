# Microphone-Clap
### This is a college project
A simple script that opens a microphone stream using your main microphone and detects a clap
This works by checking your microphone input to check if any noise exceeds a set threshold, you can change this in the constants section at the top of the script.
As of right now, the recording doesn't work; it originally did but then I had an issue that it was saving audios that could be very very long therefore I decided to add a trimmer that would only select the last X amount of seconds on the recording.
It only records one second and the output is essentially static. Will be fixed.
