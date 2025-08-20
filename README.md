# Face Blurring Application

A web application that automatically detects and blurs faces in images and videos using OpenCV.

The models available for face detection have some limitations:
- **Haar Cascade (Default)**: Best for frontal faces, may miss some angles.
- **Haar Cascade (Alternative)**: Similar to the default, but may perform better in certain scenarios.
- **Haar Cascade (Alternative 2)**: Another option for frontal faces, with different training data.
- **Haar Cascade (Profile)**: Specifically designed for profile face detection, but may not detect frontal faces.

## Features

- **Face Detection**: Automatically detects faces using multiple OpenCV models:
  - Haar Cascade (Default) - Standard frontal face detection
  - Haar Cascade (Alternative) - Alternative frontal face classifier  
  - Haar Cascade (Alternative 2) - Second alternative classifier
  - Haar Cascade (Profile) - Profile face detection
- **Multiple Effects**: Apply blur or pixelation effects to detected faces
- **Configurable Parameters**: 
  - Adjustable blur strength (5-99)
  - Configurable pixelation size (5-50)
- **Multi-format Support**: Works with images (JPG, PNG, GIF) and videos (MP4, AVI, MOV)
- **Simple Web Interface**: Easy-to-use interface with model selection and parameter controls
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
3. Select the face detection model from the dropdown
4. Adjust blur strength and pixel size using the sliders
5. Select the effect (Blur or Pixelate)
6. Click "Process File" to upload and process
7. View the results and download the processed file

## Supported Formats

- **Images**: JPG, JPEG, PNG, GIF
- **Videos**: MP4, AVI, MOV

## Technical Details

- **Backend**: Python Flask
- **Face Detection**: OpenCV with multiple Haar Cascade classifiers
- **Frontend**: HTML, CSS, JavaScript with responsive design
- **Container**: Docker with Python 3.9 slim base image
- **Configuration**: Real-time parameter adjustment with sliders