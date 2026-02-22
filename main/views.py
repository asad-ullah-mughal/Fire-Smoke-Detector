from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from .forms import RegisterForm, LoginForm
import os
from django.conf import settings
from ultralytics import YOLO
from django.core.files.storage import FileSystemStorage
import uuid
import cv2
from django.http import StreamingHttpResponse
from django.views.decorators import gzip
import subprocess
from django.core.mail import send_mail
# Load YOLO model once at startup
model = YOLO(os.path.join(settings.BASE_DIR, "models/best.pt"))

# class VideoCamera:
#     def __init__(self):
#         # 0 = default webcam. Replace with RTSP/HTTP URL for IP cameras
#         self.cap = cv2.VideoCapture(0)

#     def __del__(self):
#         if self.cap.isOpened():
#             self.cap.release()

#     def get_frame(self):
#         success, frame = self.cap.read()
#         if not success:
#             return None

#         # Run YOLO detection
#         results = model.predict(frame, verbose=False)

#         # Annotated frame with detections
#         annotated_frame = results[0].plot()

#         # Encode to JPEG
#         ret, jpeg = cv2.imencode('.jpg', annotated_frame)
#         return jpeg.tobytes()


# def gen(camera):
#     while True:
#         frame = camera.get_frame()
#         if frame:
#             yield (b'--frame\r\n'
#                    b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')


# @gzip.gzip_page
# def live_feed(request):
#     return StreamingHttpResponse(gen(VideoCamera()),
#                                  content_type="multipart/x-mixed-replace;boundary=frame")


# @login_required(login_url='login')
# def camera(request):
#     return render(request, "main/camera.html")
from django.shortcuts import render
from django.http import StreamingHttpResponse
from django.views.decorators import gzip
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.core.mail import send_mail
import cv2
import time

# Load YOLO model once globally
from ultralytics import YOLO
model = YOLO("best.pt")


class VideoCamera:
    def __init__(self, user_email):
        self.cap = cv2.VideoCapture(0)
        self.user_email = user_email
        self.email_sent = False
        self.last_alert_time = 0  # to avoid multiple emails per session

    def __del__(self):
        if self.cap.isOpened():
            self.cap.release()

    def get_frame(self):
        success, frame = self.cap.read()
        if not success:
            return None

        # Run YOLO detection
        results = model.predict(frame, verbose=False)
        annotated_frame = results[0].plot()

        # Extract detected class names
        detected_classes = [model.names[int(c)] for c in results[0].boxes.cls]

        # Check for fire or smoke
        if any(cls.lower() in ["fire", "smoke"] for cls in detected_classes):
            cv2.putText(
                annotated_frame,
                "🔥 ALERT: Fire/Smoke Detected!",
                (20, 50),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (0, 0, 255),
                3,
            )

            # Send email alert once per session
            if not self.email_sent and self.user_email:
                self.send_fire_alert_email()
                self.email_sent = True
                self.last_alert_time = time.time()

        # Encode frame to JPEG
        ret, jpeg = cv2.imencode(".jpg", annotated_frame)
        return jpeg.tobytes()

    def send_fire_alert_email(self):
        try:
            subject = "🔥 Fire/Smoke Detection Alert"
            message = (
                "Dear user,\n\n"
                "Fire or smoke has been detected by your live camera system.\n"
                "Please take immediate action to ensure safety.\n\n"
                "Stay safe,\nFire Detection System 🔥"
            )
            from_email = settings.EMAIL_HOST_USER
            recipient_list = [self.user_email]

            send_mail(subject, message, from_email, recipient_list)
            print(f"✅ Fire alert email sent to {self.user_email}")
        except Exception as e:
            print(f"⚠️ Email sending failed: {e}")


def gen(camera):
    while True:
        frame = camera.get_frame()
        if frame:
            yield (
                b"--frame\r\n"
                b"Content-Type: image/jpeg\r\n\r\n" + frame + b"\r\n\r\n"
            )


@gzip.gzip_page
@login_required(login_url="login")
def live_feed(request):
    """Stream live camera feed and trigger detection alerts."""
    user_email = request.user.email  # use the logged-in user's email
    return StreamingHttpResponse(
        gen(VideoCamera(user_email)),
        content_type="multipart/x-mixed-replace;boundary=frame",
    )


@login_required(login_url="login")
def camera(request):
    return render(request, "main/camera.html")




# Landing page (Login/Register buttons)
def landing(request):
    return render(request, "main/landing.html")

def register_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("index")  # go to homepage
    else:
        form = RegisterForm()
    return render(request, "main/register.html", {"form": form})

def login_view(request):
    if request.method == "POST":
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("index")
    else:
        form = LoginForm()
    return render(request, "main/login.html", {"form": form})

def logout_view(request):
    logout(request)
    return redirect("landing")

@login_required
def index(request):
    return render(request, "main/index.html")


@login_required(login_url='login')
def upload(request):
    context = {}

    if request.method == "POST" and request.FILES.get("file"):
        uploaded_file = request.FILES["file"]

        fs = FileSystemStorage(location=settings.MEDIA_ROOT)
        filename = fs.save(uploaded_file.name, uploaded_file)
        file_path = os.path.join(settings.MEDIA_ROOT, filename)

        is_video = uploaded_file.name.lower().endswith(('.mp4', '.avi', '.mov', '.mkv'))
        unique_run_name = f"result_{uuid.uuid4().hex[:8]}"

        results = model.predict(
            source=file_path,
            save=True,
            project=os.path.join(settings.MEDIA_ROOT, "detections"),
            name=unique_run_name,
            exist_ok=False
        )

        result_dir = results[0].save_dir

        # Find detected output file
        detected_files = [
            f for f in os.listdir(result_dir)
            if f.lower().endswith(('.jpg', '.jpeg', '.png', '.mp4', '.avi', '.mov', '.mkv'))
        ]

        result_file_url = None

        if detected_files:
            result_file = detected_files[0]
            result_path = os.path.join(result_dir, result_file)

            # ✅ Convert .avi to .mp4 for browser playback
            if result_file.lower().endswith(".avi"):
                mp4_name = os.path.splitext(result_file)[0] + ".mp4"
                mp4_path = os.path.join(result_dir, mp4_name)

                try:
                    subprocess.run([
                        "ffmpeg", "-y",
                        "-i", result_path,
                        "-vcodec", "libx264",
                        "-acodec", "aac",
                        "-strict", "-2",
                        mp4_path
                    ], check=True)

                    result_file = mp4_name
                    os.remove(result_path)  # remove old .avi to save space

                except Exception as e:
                    print("FFmpeg conversion failed:", e)

            # Make relative path for template
            result_file_url = os.path.join("detections", unique_run_name, result_file).replace("\\", "/")

        context.update({
            "uploaded_file_url": os.path.join("media", filename).replace("\\", "/"),
            "result_file_url": result_file_url,
            "is_video": is_video,
            "success": True,
        })

    return render(request, "main/upload.html", context)