# -*- coding:utf-8 -*-
'''
ASR (Automatic Speech Recognition) with Microsoft Azure SDK for Python.
This script listens to another player's speech and responds based on keyword files located in the data folder.
'''

import sys
import keyboard
import azure.cognitiveservices.speech as speechsdk
import csv
import time
import datetime
import numpy as np
import onnxruntime
from transformers import AutoTokenizer
import warnings
from sentence_transformers import SentenceTransformer, util

from Working_code import config as cf
from Working_code import tts

# Suppress warnings
warnings.filterwarnings('ignore')
onnxruntime.set_default_logger_severity(3)

# Configuration settings
speech_key, service_region = cf.speech_key, cf.service_region
speech_config = cf.speech_config
audio_config = cf.audio_config
logger = cf.logging.getLogger("__asr__")

# Tokenizer and ONNX session based on language
if cf.THIS_LANGUAGE == 'en-US':
    onnx_session = onnxruntime.InferenceSession('Working_code/model/onnx_model/dialoGPT_ENG/decoder_model.onnx')
    tokenizer = AutoTokenizer.from_pretrained('Working_code/model/onnx_model/dialoGPT_ENG')
else:
    onnx_session = onnxruntime.InferenceSession('Working_code/model/onnx_model/kogpt2_KOR/decoder_model.onnx')
    tokenizer = AutoTokenizer.from_pretrained('Working_code/model/onnx_model/kogpt2_KOR', bos_token='</s>', eos_token='</s>', pad_token='<pad>')
    
#Load the model
model = SentenceTransformer('sentence-transformers/multi-qa-mpnet-base-cos-v1')

def asr_tts_excel():
    mode = "w" if cf.script_counter == 1 else "a"
    with open(cf.script_path, encoding="utf-8-sig", newline='', mode=mode) as f:
        writer = csv.writer(f)
        if cf.script_counter == 1:
            writer.writerow(['Speaker', 'Script', 'Start', 'Finish', 'Self_ASR'])
            cf.script_counter += 1
        writer.writerow(cf.list_utter)


class listen_micr:

    def __init__(self):
        self._running = True

    def terminate(self):
        self._running = False

    def run(self):
        speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, language=cf.THIS_LANGUAGE, audio_config=audio_config)

        while self._running:
            try:
                print("Say Something!")
                result = speech_recognizer.recognize_once_async().get()
                user_utt = result.text[:-1].lower()

                if user_utt:
                    self.handle_user_input(user_utt)
                    if ('exit' in user_utt) or ('종료' in user_utt) or (keyboard.is_pressed('esc')):
                        print("Exiting...")
                        sys.exit()

            except Exception as e:
                logger.error(e)

    def handle_user_input(self, user_utt):
        cf.utt_start_time = round(time.time() - cf.game_start_time, 5)
        print("Recognized:", user_utt)
        logger.info(f'user said: {user_utt}')
        self.respond_to_user_utt(user_utt, cf.language)

        cf.list_utter.extend(["Player", user_utt, str(datetime.timedelta(seconds=cf.utt_start_time)).split(".")[0]])
        cf.utt_finish_time = round(time.time() - cf.game_start_time, 5)
        cf.list_utter.append(str(datetime.timedelta(seconds=cf.utt_finish_time)).split(".")[0])
        cf.list_utter.append('None')
        asr_tts_excel()
        cf.list_utter = []

    def respond_to_user_utt(self, user_text, language):
        try:
            decoded_text = self.get_response_text(user_text)
            
            # Encode query and documents
            query_emb = model.encode(user_text, show_progress_bar=False)
            response_emb = model.encode(decoded_text, show_progress_bar=False)
            
            #Compute dot score between query and all document embeddings
            scores = util.dot_score(query_emb, response_emb)[0].tolist()[0]
            
            if scores > cf.threshold:
                tts.synthesize_utt(decoded_text, 'asr')
                print(f"response: {scores}")
            else:
                print(f"No response: {scores}")
                
        except Exception as err:
            logger.error("user input parsing failed", err)

    def get_response_text(self, user_text):
        if cf.THIS_LANGUAGE == 'en-US':
            # Note that we use the user text directly, not wrapped in <usr> or <sys> tags, 
            # as GPT2 doesn't use them. The eos_token is used to mark the end of the question.
            input_ids = tokenizer.encode(user_text + tokenizer.eos_token, return_tensors='np').astype(np.int64)
        
            # Create attention mask
            attention_mask = np.ones_like(input_ids, dtype=np.int64)
        
            decoded_input_ids = top_p_sampling_decode(input_ids, attention_mask)
            decoded_text = tokenizer.decode(decoded_input_ids[0])
        
            # Strip the question text and the eos_token from the response
            decoded_text = decoded_text[len(user_text)+len(tokenizer.eos_token):]
            return decoded_text

        else:
            sent = '<usr>' + user_text + '<sys>'
            input_ids = [tokenizer.bos_token_id] + tokenizer.encode(sent)
            input_ids = np.array([input_ids], dtype=np.int64)
        
            # Create attention mask
            attention_mask = np.ones_like(input_ids, dtype=np.int64)
        
            decoded_input_ids = top_p_sampling_decode(input_ids, attention_mask)
            decoded_text = tokenizer.decode(decoded_input_ids[0])
            decoded_text = decoded_text.split('<sys> ')[1].replace('</s>', '')
            return decoded_text


def softmax(x):
    e_x = np.exp(x - np.max(x))
    return e_x / e_x.sum(axis=-1, keepdims=True)

def top_p_sampling(logits, p=0.9):
    sorted_logits = np.sort(logits)[::-1]
    sorted_indices = np.argsort(logits)[::-1]

    cumulative_probs = np.cumsum(softmax(sorted_logits))

    indices_to_remove = cumulative_probs > p
    indices_to_remove = np.roll(indices_to_remove, 1)  # Shift the indices_to_remove by one to the right to keep the top token
    indices_to_remove[0] = False  # Set the first token as False to always keep it

    logits[sorted_indices[indices_to_remove]] = -np.inf
    probs = softmax(logits)

    token_id = np.random.choice(len(logits), size=1, p=probs)[0]

    return token_id

def top_p_sampling_decode(input_ids, attention_mask, max_length=50, p=0.9):
    current_length = input_ids.shape[1]

    while current_length < max_length:
        outputs = onnx_session.run(output_names=['logits'], input_feed={"input_ids": input_ids, "attention_mask": attention_mask})
        logits = outputs[0][0, -1, :]

        # Apply Top-p sampling
        predicted_token_id = top_p_sampling(logits, p=p)

        # Break if the EOS token is generated
        if predicted_token_id == tokenizer.eos_token_id:
            break

        # Update input_ids and attention_mask
        input_ids = np.concatenate((input_ids, np.array([[predicted_token_id]])), axis=1).astype(np.int64)
        attention_mask = np.concatenate((attention_mask, np.array([[1]])), axis=1).astype(np.int64)

        current_length += 1

    return input_ids