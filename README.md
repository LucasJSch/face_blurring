# Face Blurring Application

A web application that automatically detects and blurs faces in images and videos using OpenCV.

## Features

- **Face Detection**: Automatically detects faces using OpenCV's Haar Cascade classifier
- **Multiple Effects**: Apply blur or pixelation effects to detected faces
- **Multi-format Support**: Works with images (JPG, PNG, GIF) and videos (MP4, AVI, MOV)
- **Simple Web Interface**: Easy-to-use drag-and-drop upload interface
- **Dockerized**: Ready to run with Docker

## Quick Start

### Using Docker (Recommended)

1. Build the Docker image:
```bash
docker build -t face-blurring-app .
```

2. Run the container:
```bash
docker run -p 5000:5000 face-blurring-app
```

3. Open your browser and go to `http://localhost:5000`

### Local Development

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the application:
```bash
python app.py
```

3. Open your browser and go to `http://localhost:5000`

## Usage

1. Open the application in your web browser
2. Choose an image or video file (drag and drop or click to browse)
3. Select the effect (Blur or Pixelate)
4. Click "Process File" to upload and process
5. View the results and download the processed file

## Supported Formats

- **Images**: JPG, JPEG, PNG, GIF
- **Videos**: MP4, AVI, MOV

## Technical Details

- **Backend**: Python Flask
- **Face Detection**: OpenCV with Haar Cascade classifier
- **Frontend**: HTML, CSS, JavaScript
- **Container**: Docker with Python 3.9 slim base image