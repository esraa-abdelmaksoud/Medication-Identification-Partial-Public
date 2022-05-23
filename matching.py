import pandas as pd
from paddleocr import PaddleOCR
from datetime import datetime
from fuzzywuzzy import fuzz, process
from spellchecker import SpellChecker
import json
import cv2


def load_drug_data(file_path,file_name):
    """load aggregated drug data rows.

    Args:
        file_path: Path to csv file of drug data.
        file_name: Name of the drug data file.

    Returns:
        drug_df: A aggregated version for drug data frame rows. 
    """
    # Read drug data frame
    drug_df = pd.read_csv(r"{}\{} agg.csv".format(file_path,file_name))

    return(drug_df)

def agg_drug_data(file_path,file_name):
    """Create and write to disk a .csv file of aggregated drug data rows.

    Args:
        file_path: Path to csv file of drug data.
        file_name: Name of the drug data file.
    """
    # Read drug data frame
    drug_df = pd.read_csv(r"{}\{}.csv".format(file_path,file_name))

    # Convert `NaNs` to string
    drug_df = drug_df.fillna('')

    # Aggregate rows
    drug_df['All'] = drug_df[['Name','Dose','Type','Size']].agg(' '.join, axis=1)

    # Write dataframe
    drug_df.to_csv(r"{}\{} agg.csv".format(file_path,file_name), header=True, index=False)

    return()

def create_json_dict(file_path,file_name,json_path,json_fname):
    """Create and write to disk JSON dictionary for drug names.
    
    Args:
        file_path: Path to csv file of drug data.
        file_name: Name of the drug data file.
        json_path: Desired path for JSON file.
        json_name: Desired name for JSON file.     
    """
    # Read drug data frame with aggregated data
    drug_df = pd.read_csv(r"{}\{} agg.csv".format(file_path,file_name))

    # Create dictionary from drug names
    drug_dict = {k: v for v,k in enumerate(drug_df['Name'])}

    # Write dictionary to json
    with open(r"{}\{}.json".format(json_path,json_fname), "w") as outfile:
        outfile.write(json.dumps(drug_dict, indent=4))

    return()

def load_json_dict(json_path,json_fname):
    """Create and write to disk JSON dictionary for drug names.
    
    Args:
        json_path: Desired path for JSON file.
        json_name: Desired name for JSON file.
    
    Returns:
        drug_dict: Drug names JSON dictionary.
    """
    # Read json dictionary
    file = open(r"{}\{}".format(json_path,json_fname))
    drug_dict = json.load(file)

    return(drug_dict)

def first_paddle_ocr(img):
    """Apply ocr to image.

    Args:
        img: Image array.

    Return:
        ocr_list: OCR list result.
    """
    # Load OCR engine - need to run only once to download and load model into memory
    ocr = PaddleOCR(use_angle_cls=True, lang='en',use_gpu=False,show_log=False,max_text_length=100) 
    
    # Append OCR output for 4 rotations to list

    ######################################
    ###### Removed until publishing ######
    ######################################

    return (ocr_list)

def use_ocr_on_warped(warp_img,ocr_list):
    """Apply ocr to warped image.

    Args:
        warp_img: Warped image array.
        ocr_list: Previous OCR result list.

    Return:
        ocr_list: OCR list after warping
    """
    # wrap = None
    # Rotate warped image and use OCR twice
    for i in range (2):
        # Using 2 only as Paddle handles extra rotation
        warp_img = cv2.rotate(warp_img, cv2.ROTATE_90_CLOCKWISE)
        # wrap = "yes"

        ocr = PaddleOCR(use_angle_cls=True, lang='en',use_gpu=False,show_log=False,max_text_length=100)
        result = ocr.ocr(warp_img,cls=True)
        ocr_list.extend([line[1][0] for line in result])
    
    return (ocr_list)

def correct_spelling(ocr_list,drug_df,json_path,json_fname):
    """Use spelling correction.

    Args:
        ocr_list: Previous OCR result list.
        drug_df: Drug data frame.
        json_path: Path to json file.
        json_fname: Json file name.

    Return:
        misspelled: Misspelled word.
        correct_word: Corrected word.
    """
    # Initialize variables to avoid NaN errors
    misspelled = None
    correct_word = None

    # Create list of drug names
    drug_list = (drug_df['Name']).tolist()

    # Create dictionary for text matching probabilities
    probab_dict = {}

    for item in ocr_list:
        sort_fuzzy = process.extractOne(item, drug_list,scorer=fuzz.token_set_ratio)
        probab_dict[item] = sort_fuzzy[1]

    # Sort descending by probability and convert to list
    probab_dict = dict(sorted(probab_dict.items(), key=lambda item: item[1],reverse=True))
    probab_list = [*probab_dict.keys()]

    # Get word with highest probability with length > 3
    misspelled = probab_list[0]
    count = 1
    while len(misspelled) < 3:
        misspelled = probab_list[count]
        count+=1

    # Use spelling correction for highest probability text
    spell = SpellChecker(local_dictionary=r'{}\{}'.format(json_path,json_fname))

    correct_word = spell.correction(misspelled)

    return (misspelled,correct_word)

def fuzzy_match(drug_df, ocr_list, ocr_string, json_path,json_fname):
    """Fuzzy match the text result of OCR on drug label to dictionary.

    Args:
        drug_df: Drug data frame.
        ocr_list: Previous OCR result list.
        ocr_string: OCR joined output.
        json_path: Path to json file.
        json_fname: Json file name.

    Return:
        fuzzy_text: Fuzzy matching result.
    """
    # Initalize fuzzy text variable
    fuzzy_text = None

    # Convert lowercase drug names to list
    drug_name_list = drug_df['Name_Lower'].tolist()


    ######################################
    ###### Removed until publishing ######
    ######################################

def get_med_data(fuzzy_text,drug_df):
    """Retrieve drug data.

    Args:
        fuzzy_text: Fuzzy matching result.
        drug_df: Drug data frame.

    Return:
        d_idx: Drug index.
        d_name: Drug name.
        d_dose: Drug dose.
        d_type: Drug type.
        d_size: Drug pack size.
    """
    # Initializing variables
    d_idx, d_name, d_dose, d_type, d_size = None, None, None, None, None

    # Get index of matched fuzzy text
    if fuzzy_text != None:
        filter_idx = drug_df[drug_df['All'] == fuzzy_text[0]]
    else:
        pass
    
    # Get drug details for same index
    try:
        d_idx = filter_idx.index[0]
        d_name = drug_df['Name'][d_idx]
        d_dose = drug_df['Dose'][d_idx]
        d_type = drug_df['Type'][d_idx]
        d_size = drug_df['Size'][d_idx]
    except:
        pass

    return d_idx, d_name, d_dose, d_type, d_size
