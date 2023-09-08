# -*- coding:utf-8 -*-
'''
This module synthesizes utterances using Microsoft Azure TTS SDK, primarily 
from the 'parse_tree.py' and 'asr.py' files.
'''

# Import libraries
import azure.cognitiveservices.speech as speechsdk
import time
import datetime
import re
import csv
from Working_code import asr
from Working_code import config as cf

# Configuration setup
speech_key, service_region = cf.speech_key, cf.service_region
speech_config = cf.speech_config

# Logger setup
logger = cf.logging.getLogger("__tts__")

def turn_pass_excel():
    """Write turn pass details to an excel file."""
    mode = "w" if cf.turn_counter == 1 else "a"
    with open(cf.turn_pass_path, encoding="utf-8-sig", newline='', mode=mode) as f:
        writer = csv.writer(f)
        if cf.turn_counter == 1:
            writer.writerow(['Speaker', 'Acc', 'Script', 'Time', 'Self_ASR'])
        writer.writerow(cf.list_turn_pass)
        cf.turn_counter += 1

def synthesize_utt(utterance, self_asr_check):
    """Synthesize utterances using Microsoft Azure TTS SDK."""
    if cf.synthesize_utt_check == 0 and utterance:
        cf.synthesize_utt_check = 1
        cf.utt_start_time = round(time.time() - cf.game_start_time, 5)
        logger.info(f"New utterance is: {utterance}")
        
        # MS Azure TTS / Synthesize text and make it to speak
        speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config)
        
        print(f"\n{'*' * 50}\nAvatar: {utterance}\n{'*' * 50}\n")
        
        cf.list_utter.extend(["Avatar", utterance, str(datetime.timedelta(seconds=cf.utt_start_time)).split(".")[0]])
        cf.utt_finish_time = round(time.time() - cf.game_start_time, 5)
        cf.list_utter.append(str(datetime.timedelta(seconds=cf.utt_finish_time)).split(".")[0])
        
        cf.list_utter.append('self' if self_asr_check == 'self' else 'asr')
        asr.asr_tts_excel()
        cf.list_utter = []

        result = speech_synthesizer.speak_text_async(utterance).get()
        
        utterance = re.sub(r'[^a-zA-Z ]', '', utterance).lower() if cf.THIS_LANGUAGE == 'en-US' else re.sub(r'[^ ㄱ-ㅣ가-힣+]', '', utterance)

        if result.reason == speechsdk.ResultReason.Canceled:
            cancellation_details = result.cancellation_details
            logger.info("Speech synthesis canceled: {}".format(cancellation_details.reason))
            if cancellation_details.reason == speechsdk.CancellationReason.Error:
                logger.info("Error details: {}".format(cancellation_details.error_details))
        
        time.sleep(0.2)
        cf.synthesize_utt_check = 0