import numpy as np
from scipy.signal import butter, filtfilt, welch
import cv2
import dlib

# Load Dlib face detector and shape predictor
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("RPPG/shape_predictor_68_face_landmarks.dat")

def get_forehead_roi(frame, face):
    landmarks = predictor(frame, face)

    x1 = landmarks.part(19).x
    x2 = landmarks.part(24).x
    y1 = landmarks.part(19).y
    y2 = landmarks.part(28).y

    # Slightly expand the ROI
    x1 -= 10
    x2 += 10
    y2 = y1 + (y2 - y1) // 2

    # Keep ROI within image bounds
    x1, y1 = max(x1, 0), max(y1, 0)
    x2, y2 = min(x2, frame.shape[1]), min(y2, frame.shape[0])

    roi = frame[y1:y2, x1:x2]
    return roi if roi.size > 0 else None

def extract_signal(roi_frames):
    green_channel = [np.mean(cv2.cvtColor(f, cv2.COLOR_BGR2RGB)[:, :, 1]) for f in roi_frames]
    return np.array(green_channel)

def bandpass_filter(signal, fs=30, low=0.75, high=3.0):
    nyq = 0.5 * fs
    b, a = butter(3, [low / nyq, high / nyq], btype='band')
    return filtfilt(b, a, signal)

def estimate_bpm(filtered_signal, fs=30):
    freqs, psd = welch(filtered_signal, fs=fs)
    peak_freq = freqs[np.argmax(psd)]
    return peak_freq * 60  # Hz to BPM
