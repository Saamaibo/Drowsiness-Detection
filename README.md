# Drowsiness Detection

Real-time drowsiness detection from a webcam. [dlib](http://dlib.net) finds the face and its 68 facial landmarks, the **Eye Aspect Ratio (EAR)** is computed from the eye landmarks, and if the eyes stay closed for too long the program shows a **WAKE UP** warning and plays an alarm.

## How it works

EAR compares the eye's height to its width using six landmarks per eye (p1 to p6):

```
EAR = ( |p2 - p6| + |p3 - p5| ) / ( 2 * |p1 - p4| )
```

When the eye is open, EAR is roughly constant. When it closes, EAR drops toward zero. Each frame the notebook:

1. Detects faces with dlib's frontal face detector (on a 420 px wide grayscale copy of the frame).
2. Predicts the 68 landmarks and averages the EAR of both eyes.
3. Counts consecutive frames where EAR is below the threshold. A normal blink is only a few frames, so an alarm only triggers when the count passes the limit.
4. Plays the alarm once per episode, and resets when the eyes open again.

When you quit, the notebook plots EAR over time with the threshold line, which is handy for tuning.

| Setting         | Default | Meaning                                              |
|-----------------|---------|------------------------------------------------------|
| `blink_thresh`  | `0.25`  | EAR below this counts as eyes closed                 |
| `sleep_frames`  | `50`    | Consecutive closed-eye frames before the alarm       |

## Setup

Python 3.10+ and a webcam are required.

```bash
git clone https://github.com/<your-username>/<repo-name>.git
cd <repo-name>
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python download_model.py         # one-time download of the landmark model (~100 MB)
jupyter notebook sleep_detection.ipynb
```

Run the cells in order. A video window opens, and pressing `q` in it quits and shows the EAR plot.

**Notes**
- `requirements.txt` uses `dlib-bin`, which has prebuilt wheels. The regular `dlib` package works too, but needs CMake and a C++ compiler to build.
- On Linux, `playsound` also needs GStreamer and PyGObject installed.
- To use your own alarm, change `ALARM_SOUND` in the settings cell to any `.wav` or `.mp3` file.

## Tuning and limitations

- **Calibrate the threshold.** Resting EAR varies between people, cameras, and angles (and glasses can affect it). If the alarm triggers too easily or never, look at the EAR plot and adjust `blink_thresh`.
- **Time depends on frame rate.** The limit is counted in frames, not seconds, so the same `sleep_frames` means a different delay at different FPS.
- **Frontal faces only.** dlib's HOG detector works best when you face the camera in decent lighting.
- **One shared counter.** If several faces are in view, they all update the same counter.
- This is a hobby project, not a safety system, so don't rely on it to stay safe while driving.

## Credits

- **Landmark model:** `shape_predictor_68_face_landmarks.dat` comes from [dlib-models](https://github.com/davisking/dlib-models) and was trained on the iBUG 300-W dataset, whose license **excludes commercial use**. That's why the file is downloaded rather than included here, and why the model can't be used in a commercial product.
- EAR comes from Soukupová and Čech, *Real-Time Eye Blink Detection using Facial Landmarks* (2016).
- `assets/alarm.wav` was generated for this project.
