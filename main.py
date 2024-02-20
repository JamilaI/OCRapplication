import pandas as pd
from tabulate import tabulate
import re
import easyocr
import cv2

# preprocess input image by converting the image to grey scale and binarize the images by adjusting the treshold
def img_preprocess(image):
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, binary_image = cv2.threshold(gray_image, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    return binary_image

#extracting the text by OCR
def text_extraction(image):
    reader = easyocr.Reader(['en', 'ar'], gpu=False, download_enabled=True) #OCR reader
    result = reader.readtext(image) #read text from the images
    extracted_text = ' '.join([text[1] for text in result])
    return extracted_text

#Extract the required information from the images like name, father name, id number, gender, etc)

def info_extraction(text):

#use regular expression to detect the needed info
    name_pattern = r'(?:\bالاسم\b|Name)[:؛]?\s*([\s\w\u0600-\u06FF]+)'
    father_name_pattern = r'(?:\bالآب\b|Father)[:؛]?\s*([\s\w\u0600-\u06FF]+)'
    id_number_pattern = r'(?:\bالبطاقة\s*الوطنية\b|ID\s*Number)[:؛]?\s*(\d{12})'
    blood_type_pattern = r'(?:\bفصيلة\s*الدم\b|Blood\s*Type)[:؛]?\s*([\s\w\u0600-\u06FF]+)'


#search in the extracted text for every data.
    name = re.search(name_pattern, text, re.IGNORECASE)
    father_name = re.search(father_name_pattern, text, re.IGNORECASE)
    id_number = re.search(id_number_pattern, text, re.IGNORECASE)
    blood_type = re.search(blood_type_pattern, text, re.IGNORECASE)

    info = { #store the results as info
        'Name': name.group(1).strip() if name else '',
        'Father\'s Name': father_name.group(1).strip() if father_name else '',
        'ID Number': id_number.group(1).strip() if id_number else '',
        'Blood Type': blood_type.group(1).strip() if blood_type else ''
    }

    return info

def img_process(image_path): #processing single image by reading it from image_path
    try:
        print(f"Image Processing: {image_path}")
        image = cv2.imread(image_path)
        preprocessed_image = img_preprocess(image)
        extracted_text = text_extraction(preprocessed_image)
        print("The Extracted text:")
        print(extracted_text)
        extracted_info = info_extraction(extracted_text)
        return extracted_info
    except Exception as e:
        print(f"Error image Processing {image_path}: {e}")
        return None

def multiple_images_process(image_paths): #for processing more than one image.
    data = []
    for image_path in image_paths:
        extracted_info = img_process(image_path)
        if extracted_info:
            data.append(extracted_info)

    df = pd.DataFrame(data)
    df.fillna('', inplace=True)

    print(tabulate(df, tablefmt='grid',  headers='keys', showindex=False))


if __name__ == "__main__":
    image_paths = ["C:\\Users\\gateway\\Downloads\\ID.jpeg","C:\\Users\\gateway\\Downloads\\id2.jpeg","C:\\Users\\gateway\\Downloads\\ID3.jpeg"]
    multiple_images_process(image_paths)
