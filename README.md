# Audio Fingerprinting and Song Recognition with Python 🎶

## Introduction

This project demonstrates how to build a Shazam-like application using Python. It leverages the concept of **audio fingerprinting** to identify songs by creating unique digital fingerprints of audio files. These fingerprints are then matched against a database to identify the song being played.

### What is Audio Fingerprinting?

Audio fingerprinting is a technique that converts a piece of audio into a unique identifier, or "fingerprint," based on its frequency patterns. This fingerprint is then used to search a database for a match, allowing applications to quickly identify songs, even in noisy environments.

For more insights into audio fingerprinting, check out these resources:
- [How Shazam Works](https://coding-geek.com/how-shazam-works/)
- [Shazam It! Music Processing, Fingerprinting, and Recognition](https://www.toptal.com/algorithms/shazam-it-music-processing-fingerprinting-and-recognition)
- [Creating Shazam in Java](https://www.royvanrijn.com/blog/2010/06/creating-shazam-in-java/)

## Project Overview

This project is based on an open-source implementation of audio fingerprinting:
- [dejavu](https://github.com/worldveil/dejavu)
- [Fingerprinting and Audio Recognition with Python](https://willdrevo.com/fingerprinting-and-audio-recognition-with-python/)

The project uses Python libraries such as `numpy`, `pyaudio`, `pydub`, and `wave` to generate and compare audio fingerprints.

## Installation

Follow the steps below to set up the project on your local machine.

### Prerequisites

- **Operating System**: Ubuntu 19.04 or later (Other OS may work with slight modifications)
- **Python**: Version 3.x
- **Microphone**: A working microphone is required for real-time audio recognition

### Step 1: Clone the Repository

First, clone the project repository to your local machine:

```bash
git clone https://github.com/JACKSPARROWbts/The_Ear
sudo apt-get install python-tk
sudo apt install ffmpeg
sudo apt-get install portaudio19-dev python-pyaudio
```

### Step 2: Install System Dependencies
Install the necessary system packages for audio processing:

```bash
sudo apt-get install python-tk
sudo apt install ffmpeg
sudo apt-get install portaudio19-dev python-pyaudio
```

### Step 3: Install Python Packages

Install the required Python packages using pip:

```bash
pip install -r requirements.txt
```

- Alternatively, you can manually install the required packages:

```bash
pip install numpy termcolor pyaudio wave pydub
```

### Step 4: Set Up the Database

After installing the dependencies, you need to set up the database where the audio fingerprints will be stored:

``` bash
make clean reset
```

### Step 5: Add Songs to Your Database

Place the MP3 files you want to recognize in the mp3 directory inside the project folder. Create this directory if it doesn't exist:

```bash
mkdir mp3
```

- Copy your MP3 files into this mp3 directory.

### Step 6: Generate Audio Fingerprints

Generate fingerprints for the MP3 files and store them in the database:

```bash
python collect-fingerprints-of-songs.py
```

### Step 7: Recognize Audio from the Microphone

To recognize a song from the microphone, use the following command. Replace -s 5 with the number of seconds you want to listen:

```bash
python recognize-from-microphone.py -s 5
```

The program will listen for the specified duration and try to match the audio against the database.

### Contributing
- Feel free to fork the repository and submit pull requests. Your contributions are welcome!

### License
This project is licensed under the MIT License. See the LICENSE file for more details.

