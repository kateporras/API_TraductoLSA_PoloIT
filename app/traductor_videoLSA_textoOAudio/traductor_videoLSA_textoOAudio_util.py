import json
import os
import cv2
import numpy as np
import mediapipe as mp
from tensorflow.keras.preprocessing.sequence import pad_sequences # type: ignore
mp_hands = mp.solutions.hands




def extraer_frames(video_path):

    cap = cv2.VideoCapture(video_path)
    frames = []
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        frames.append(frame)
    cap.release()
    return frames

def extraer_frames_modelo(dataset_videos):

    #lee todos los .mp4 del dataset y devuelve:
    # - diccionario {nombre : [frames]}
    # - max_frames= maximo de frames de todos los videos

    dic_videos_frames = {}
    max_frames = 0

    for video_arch in os.listdir(dataset_videos):
        if video_arch.endswith('.mp4'):
            video_path = os.path.join(dataset_videos, video_arch)
            palabra=os.path.splitext(video_arch)[0]
            frames = extraer_frames(video_path)
            dic_videos_frames[palabra] = frames
            max_frames = max(max_frames, len(frames))

    return dic_videos_frames, max_frames

#-----------------Para generar los Keypoints de los frames-----------------

def extraer_keypoints_por_frame(frame):
    with mp_hands.Hands(static_image_mode=True, max_num_hands=2, min_detection_confidence=0.5) as hands:
        results = hands.process(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        if results.multi_hand_landmarks:
            landmarks = results.multi_hand_landmarks[0]
            return np.array([[landmark.x, landmark.y, landmark.z] for landmark in landmarks.landmark]).flatten()
        else:
            return np.zeros((21, 3))

def extraer_keypoints_de_frames(frames,max_frames):
    secuencia= [extraer_keypoints_por_frame(frame) for frame in frames]
    secuencia_padding = pad_sequences(secuencia, maxlen=max_frames, padding='post', truncating='post', dtype='float32')[0]
    return np.array([secuencia_padding])

def cargar_max_frames(path):
    with open(path, 'r') as file:
        data=json.load(file)
    return data['max_frames']