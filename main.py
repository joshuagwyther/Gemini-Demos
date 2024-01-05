#Google Gemini Vision Simple Demo

from dotenv import load_dotenv

load_dotenv()

import streamlit as st
from PIL import Image
import io
import base64
import requests
import os

os.getenv["GOOGLE_API_KEY"]

#function to convert the image to bytes for download
def convert_image_to_bytes(image):
    buffered = io.BytesIO()
    image.save(buffered, format="JPEG")
    return buffered.getvalue()

#function to resize image
def resize_image(image):
    return image.resize((512, int(image.height * 512 / image.width)))

#function to convert the image to base64
def convert_image_to_base64(image):
    buffered = io.BytesIO()
    image.save(buffered, format="JPEG")
    return base64.b64encode(buffered.getvalue()).decode()

#function to all the Gemini API with image
def call_gemini_api(image_base64, api_key):
    headers = {
      'Content-Type': 'application/json',
    }
    data = {
      "contents": [
      {
        "parts": [
          {"text": "What is this picture?"},
          {
              "inline_data": {
                  "mime_type": "image/jpeg",
                  "data": image_base64
              }
          }
        ]
      }
    ]
  }
    response = requests.post(
      f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro-vision:generateContent${api_key}",
      headers=headers,
      json=data
  )
    return response.json()

#streamlit UI components
def main():
  st.title("Gemini Vision")

#button to grab a picture from webcam
  image = st.camera_input("Take a Picture")

  if image is not None:
  #display the picture that was taken from webcam
    st.image(image, caption='Captured Image.', use_column_width=True)

# convert the image to PIL
    pil_image = Image.open(image)
    resized_image = resize_image(pil_image)

#convert image to base64
    image_base64 = convert_image_to_base64(resized_image)

#API Key
    api_key = os.getenv['GOOGLE_API_KEY']    

    if api_key:
      #make API call
      response = call_gemini_api(image_base64, api_key)

      #dispay the response
      if response['candidates'][0]['content']['parts'][0]['text']:
          text_from_response = response['candidates'][0]['content']['parts'][0]['text']
          st.write(text_from_response)
      else:
          st.write("No respose frm API.")
    else:
      st.write("Please add your API Key.")

if __name__ == "__main__":
  main()