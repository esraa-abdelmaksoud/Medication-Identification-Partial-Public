from preprocessing import *
from matching import *
import re

img_name = r'IMG_20210831_154439.jpg' #Multi-relax
img_path = r'D:\drug captures\test'
# img_path = r'D:\drug captures\huawei y5II'
json_fname = r'drug dictionary.json'
json_path = r'D:\drug captures'
file_name = r'drug list'
file_path = r'D:\drug captures'
res = 1000

# Loading data frame of drug data
drug_df = load_drug_data(file_path,file_name)

# Resizing image
img = resize_image(res,img_path,img_name)

# Use OCR for first time
ocr_list = first_paddle_ocr(img)

# Apply image pre-processing techniques and re-use OCR if length of OCR output list is less than 8
try:
    if len(ocr_list) <= 8:
        # Canny and Contour
        contours = get_contours(img)

        # Rectangle contour 
        points = draw_rectangle(img,contours)

        # Warping to remove background
        warped = warp(img,points)

        # OCR on warped image
        ocr_list = use_ocr_on_warped(warped,ocr_list)
except:
    print("Getting contours failed.")

# Add space before numbers if after a 3-chars word or before unit such as mg/gm
if len(ocr_list) != 0:
    ocr_list = [re.sub(r"(\d*\d)([m,g])",r"\1 \2", elem) for elem in ocr_list]
    ocr_list = [re.sub(r"(\S{3})(\d)", r"\1 \2", elem) for elem in ocr_list]
    ocr_list = [elem.replace('0 0','00') for elem in ocr_list]
    ocr_list = [val.replace('?','') if '?' in val else val for val in ocr_list]
    ocr_string = ' '.join(ocr_list)

    # Fuzzy matching and spelling correction
    fuzzy_text = fuzzy_match(drug_df, ocr_list, ocr_string, json_path,json_fname)

    # Retrieve medication/drug data from data frame
    d_idx, d_name, d_dose, d_type, d_size = get_med_data(fuzzy_text,drug_df)

    print('Index: ', d_idx,'\n Name: ', d_name, '\n Dose: ', d_dose, '\n Type: ', d_type, '\n Dose: ', d_size)
