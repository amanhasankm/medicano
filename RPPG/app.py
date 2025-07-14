import streamlit as st
import cv2
import tempfile
import numpy as np
import matplotlib.pyplot as plt
from RPPG import utils  # Ensure utils.py exists in same RPPG folder

def app():
    st.title("💓 rPPG - Heart Rate Estimation")

    mode = st.radio("Select Input Mode", ["Live Webcam", "Upload Video"])

    if mode == "Live Webcam":
        st.info("📸 Click below to capture 5–7 seconds from webcam.")

        if st.button("🎥 Start Live Capture"):
            cap = cv2.VideoCapture(0)
            roi_frames = []
            max_frames = 180  # ~6 seconds at 30 FPS
            frame_count = 0

            stframe = st.empty()

            while frame_count < max_frames:
                ret, frame = cap.read()
                if not ret:
                    st.warning("⚠️ Could not access webcam.")
                    break

                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                faces = utils.detector(gray)

                if faces:
                    face = faces[0]
                    roi = utils.get_forehead_roi(frame, face)
                    if roi is not None:
                        roi_frames.append(roi)
                        frame_count += 1

                stframe.image(frame, channels="BGR", caption=f"Capturing frame {frame_count}/{max_frames}", use_container_width=True)

            cap.release()
            st.success("✅ Webcam capture complete")

            if roi_frames:
                _process_and_plot_signal(roi_frames)

    elif mode == "Upload Video":
        uploaded_file = st.file_uploader("📁 Upload a video file", type=["mp4", "avi", "mov"])
        if uploaded_file:
            temp_file = tempfile.NamedTemporaryFile(delete=False)
            temp_file.write(uploaded_file.read())

            cap = cv2.VideoCapture(temp_file.name)
            roi_frames = []
            frame_count = 0
            max_frames = 180
            stframe = st.empty()

            while cap.isOpened() and frame_count < max_frames:
                ret, frame = cap.read()
                if not ret:
                    break

                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                faces = utils.detector(gray)

                if faces:
                    face = faces[0]
                    roi = utils.get_forehead_roi(frame, face)
                    if roi is not None:
                        roi_frames.append(roi)
                        frame_count += 1

                stframe.image(frame, channels="BGR", caption=f"Processing frame {frame_count}/{max_frames}", use_container_width=True)

            cap.release()
            st.success("✅ Video processed")

            if roi_frames:
                _process_and_plot_signal(roi_frames)

def _process_and_plot_signal(roi_frames):
    st.subheader("📈 Signal Analysis")

    signal = utils.extract_signal(roi_frames)
    st.write("📊 Std Dev of Signal:", np.std(signal))
    st.write("📊 Signal Preview (first 10):", signal[:10])

    if np.std(signal) < 0.1:
        st.error("❌ Signal too weak. Ensure proper lighting and face visibility.")
        return

    filtered = utils.bandpass_filter(signal)
    bpm = utils.estimate_bpm(filtered)

    if bpm < 30 or bpm > 180:
        st.warning("⚠️ BPM out of expected range. Please retry with stable input.")

    st.success(f"💓 Estimated Heart Rate: **{bpm:.2f} BPM**")

    fig, ax = plt.subplots(2, 1, figsize=(10, 6))
    ax[0].plot(signal, color="blue", label="Raw Green Signal")
    ax[0].set_title("Raw Signal")
    ax[0].legend()

    ax[1].plot(filtered, color="green", label="Filtered Signal")
    ax[1].set_title("Bandpass Filtered Signal")
    ax[1].legend()

    st.pyplot(fig)
