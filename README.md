# BiLingualLM-Chatbot

This repository contains the implementation of a chatbot that leverages advanced language models, specifically DialogPT and KoGPT. Notably, these models have been optimized for performance by converting them to the ONNX format. The chatbot is designed to seamlessly interact in both **Korean** and **English**, providing a fluent and natural conversational experience in both languages.

## Overview

- **asr.py**: Responsible for Automatic Speech Recognition (ASR) using the Microsoft Azure SDK for Python. It listens to another player's speech and responds based on keyword files located in the data folder.
  
- **config.py**: Sets up various configurations, including API keys, logging settings, and global variables/constants for the chatbot.

- **parse_tree.py**: Parses decision trees and extracts relevant utterances based on the provided input.

- **state_changed.py**: Monitors game updates from a CSV file, processes the data, and executes the decision tree for the virtual avatar.

- **tts.py**: Handles text-to-speech synthesis using the Microsoft Azure TTS SDK. It primarily synthesizes utterances from the `parse_tree.py` and `asr.py` files.

## Key Features

- **Advanced Language Models**: The chatbot utilizes DialogPT and KoGPT, which are state-of-the-art language models known for their capabilities in generating human-like text based on the input provided.

- **ONNX Optimization**: To enhance the performance and reduce the latency of the language models, they have been converted to the ONNX format. This optimization ensures faster response times, making the chatbot more efficient.

- **Integration with Microsoft Azure**: The chatbot integrates with Microsoft Azure's cognitive services for both speech recognition and text-to-speech synthesis, providing a seamless conversational experience.

- **Bilingual Support**: Our chatbot is designed to seamlessly interact in both **Korean** and **English**. Whether you're a native Korean speaker or an English speaker, our chatbot is equipped to understand and respond to you effectively.

## Setup and Usage

1. Clone the repository: git clone https://github.com/byh711/BiLingualLM-Chatbot.git
   
2. Install the required packages: pip install -r requirements.txt
   
3. Ensure you have set up the necessary API keys and configurations in the `config.py` file.
   
4. Run the main script to start the chatbot: python main.py

## Acknowledgements
This work was supported by a grant from the National Research Foundation of Korea (NRF) (Grant number:2021R1G1A1003801). 
We would like to thank our other research collaborators who contributed to this work.
