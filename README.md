# Multi-Utility Image Analysis App
#### Link: https://huggingface.co/spaces/valleeneutral/multi_utility_image_app

This project provides an advanced image processing and insight extraction tool designed to handle multiple use cases — from calorie estimation in food images, to invoice data extraction, and detailed image insights. By leveraging Gemini AI, Google Generative AI, and deep visual analysis, the app provides intelligent and context-aware responses for diverse image-related tasks.

## Features
1. Calorie Health Tracker – Analyze food images and estimate calorie content.
2. Invoice Insight Extractor – Extract data from invoices and answer user queries.
3. Image Insight Extraction – Identify key elements, objects, or references in an image.
4. Google Gemini AI & Generative AI – Delivers highly accurate and detailed insights.

## Steps to run this Project?

#### Clone the repository
```
git clone https://github.com/fosetorico/multi_utility_image_app.git
```

#### Create a conda environment after opening the repository
```
conda create -n your-chosen-name python=3.10 -y
```

```
conda activate your-chosen-name
```

#### install the requirements
```
pip install -r requirements.txt
```

#### Finally run the following command
```
streamlit run app.py
```