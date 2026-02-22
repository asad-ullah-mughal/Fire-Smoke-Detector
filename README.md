# Fire-Smoke-Detector

Fire-Smoke-Detector is a computer vision-based Django web application that utilizes YOLO (You Only Look Once) for real-time smoke and fire detection. This application allows users to upload images or videos for detection or use live camera feeds. In case of smoke or fire detection during live monitoring, the system sends automatic email alerts to the registered user.

## Features

- Real-time fire and smoke detection using YOLO model (`best.pt` stored in the `models/` directory).
- User authentication system with login and registration functionality.
- Upload images or videos for fire and smoke detection.
- Live camera feed monitoring for real-time detection.
- Automatic email alerts to notify users of detected fire or smoke.
- Detection results are saved in the `media/detections/` directory.

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/your-repo/Fire-Smoke-Detector.git
   cd Fire-Smoke-Detector
   ```

2. Create and activate a virtual environment:

   ```bash
   python -m venv venv
   .\venv\Scripts\activate
   ```

3. Install the required dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Apply database migrations:

   ```bash
   python manage.py migrate
   ```

5. Run the development server:

   ```bash
   python manage.py runserver
   ```

6. Access the application at `http://127.0.0.1:8000/` in your web browser.

## Usage

1. Register a new account or log in with an existing account.
2. Navigate to the upload page to upload an image or video for fire/smoke detection.
3. Use the live camera feed feature for real-time monitoring.
4. View detection results in the `media/detections/` directory.
5. Receive email alerts in case of fire or smoke detection during live monitoring.

## Project Structure

```
Fire-Smoke-Detector/
│
├── fire_and_smoke_detection/       # Django project settings and configurations
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── __pycache__/
│
├── main/                           # Main application for fire and smoke detection
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── forms.py
│   ├── models.py
│   ├── tests.py
│   ├── urls.py
│   ├── utils.py                    # Utility functions for detection
│   ├── views.py                    # Application views
│   ├── migrations/                 # Database migrations
│   │   ├── __init__.py
│   │   └── 0001_initial.py
│   ├── static/                     # Static files (CSS, JS, images)
│   │   └── images/
│   └── templates/                  # HTML templates
│       └── main/
│           ├── base.html
│           ├── camera.html
│           ├── index.html
│           ├── landing.html
│           ├── login.html
│           ├── register.html
│           └── upload.html
│
├── media/                          # Media files
│   └── detections/                 # Detection results
│       ├── result_3d8c02cc/
│       └── result_b49a6e82/
│
├── models/                         # Pre-trained YOLO model
│   └── best.pt
│
├── db.sqlite3                      # SQLite database file
├── manage.py                       # Django management script
├── requirements.txt                # Python dependencies
└── README.md                       # Project documentation
```

## Pre-trained Model

The application uses a pre-trained YOLO model (`best.pt`) for fire and smoke detection. The model is stored in the `models/` directory.

## Contributing

Contributions are welcome! If you'd like to contribute, please fork the repository and submit a pull request.

## License

This project is licensed under the MIT License. See the LICENSE file for details.

## Contact

For any inquiries or support, please contact [Your Name] at [your-email@example.com].
