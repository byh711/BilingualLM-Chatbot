# BiLingualLM-Chatbot

This repository contains the implementation of a chatbot designed to operate during the gameplay of "Don't Starve". The chatbot leverages advanced language models, specifically DialoGPT and KoGPT2. Notably, these models have been optimized for performance by converting them to the ONNX format. The chatbot is designed to seamlessly interact in both **Korean** and **English**, providing a fluent and natural conversational experience in both languages.

## Gameplay Interaction: Don't Starve together

During the gameplay of "Don't Starve together", human participants engage in conversations with our developed virtual agent. This setup provides valuable insights into human-agent interaction in a dynamic environment. The agent's responses and interactions are not just limited to the gameplay mechanics but also encompass a broader range of conversational contexts, making the gaming experience more immersive and interactive.

## Overview

- **asr.py**: Responsible for Automatic Speech Recognition (ASR) using the Microsoft Azure SDK for Python. It listens to another player's speech and responds based on keyword files located in the data folder.
  
- **config.py**: Sets up various configurations, including API keys, logging settings, and global variables/constants for the chatbot.

- **parse_tree.py**: Parses decision trees and extracts relevant utterances based on the provided input.

- **state_changed.py**: Monitors game updates from a CSV file, processes the data, and executes the decision tree for the virtual avatar.

- **tts.py**: Handles text-to-speech synthesis using the Microsoft Azure TTS SDK. It primarily synthesizes utterances from the `parse_tree.py` and `asr.py` files.

## Key Features

- **Advanced Language Models**: The chatbot utilizes DialoGPT and KoGPT2, which are state-of-the-art language models known for their capabilities in generating human-like text based on the input provided.

- **ONNX Optimization**: To enhance the performance and reduce the latency of the language models, they have been converted to the ONNX format. This optimization ensures faster response times, making the chatbot more efficient.

- **Integration with Microsoft Azure**: The chatbot integrates with Microsoft Azure's cognitive services for both speech recognition and text-to-speech synthesis, providing a seamless conversational experience.

- **Bilingual Support**: Our chatbot is designed to seamlessly interact in both **Korean** and **English**. Whether you're a native Korean speaker or an English speaker, our chatbot is equipped to understand and respond to you effectively.

## Setup and Usage

1. Clone the repository
   ```sh
   git clone https://github.com/byh711/BiLingualLM-Chatbot.git
   ```
2. Install the required packages
   ```sh
   pip install -r requirements.txt
   ```
4. Ensure you have set up the necessary API keys and configurations in the `config.py` file.
   
5. Run the main script to start the chatbot: python main.py

## Acknowledgements
This work was supported by a grant from the National Research Foundation of Korea (NRF) (Grant number:2021R1G1A1003801). 
We would like to thank our other research collaborators who contributed to this work.
