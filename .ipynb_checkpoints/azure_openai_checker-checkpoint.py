import os
import json
import requests
import traceback
from llm_checker import LMModel
import time 


# Configuration
INPUT_FOLDER = "input_docs"
OCR_API_URL = "http://52.165.80.198:8831/process_document/v1"

# Initialize LLM
base_summarizer = LMModel()

# Fields and questions
fields_to_extract = {
    "purchase_requisition_number": "What is the purchase requisition number?",
    "delivery_date": "What is the delivery date?",
    "plant": "What is the plant location?",
    "storage_location": "What is the storage location?",
    "purchasing_group": "What is the purchasing group?",
    "account_assignment_category": "What is the account assignment category?",
    "requisitioner_name": "Who is the requisitioner?",
    "vendor": "Who is the vendor?",
    "status": "What is the status of the requisition?",
    "requisition_date": "What is the requisition date?",
    "procurement_type": "What is the procurement type?",
    "charge_account": "What is the charge account?",
    "deliver_to_location": "What is the delivery location?",
    "need_by_date": "What is the need-by date?",
    "promise_date": "What is the promise date?",
    "buyer": "Who is the buyer?",
    "tax": "What is the tax amount or rate?"
}

def upload_file_v2(file_path):
    files = {'file': open(file_path, 'rb')}
    try:
        response = requests.post(OCR_API_URL, files=files)
        response.raise_for_status()
        data_list = response.json().get("data_list", [])
        if data_list:
            return "\n\n".join(data_list)
        else:
            return "OCR failed or no data found"
    except requests.exceptions.RequestException as e:
        return f"OCR failed: {e}"
    finally:
        files['file'].close()

def generate_prompt_for_field(question, extracted_text):
    return f"Here is the given document:\n{extracted_text}.\n\nBased on this document, answer the following question: {question}"


def verify_answer(question, extracted_text, answer):
    url = "https://synthetic-data-test.openai.azure.com/openai/deployments/synthetic-4o/chat/completions?api-version=2023-12-01-preview"
    headers = {
        "Content-Type": "application/json",
        "api-key": "a87f3b6d9af74203b33788a796709638"
    }

    address_prototype = '''
    {
        "address_line1": "",
        "address_line2": "",
        "city": "",
        "state": "",
        "country": "",
        "zip_code": "",
        "email_address": "",
        "phone_number": ""
    }
    '''

    description_of_fields = '''
    purchase_requisition_number, this is the Unique number for the purchase requisition.
    item_number, this is the Sequential number for each item in the requisition.
    material_number, Identifier for the material (item) or service being requested.
    description, Brief description of the material or service.
    quantity, Amount of the material or service required.
    unit_of_measurement, Measurement unit for the quantity (e.g., pieces, kilograms).
    delivery_date, Requested date for the delivery of the material or service.
    plant, Location or facility where the material or service is needed.
    storage_location, Specific area within the plant for storing the material.
    purchasing_group, Identifier for the responsible purchasing group or buyer.
    material_group, Category or group to which the material belongs.
    account_assignment_category, specifies how the cost will be assigned (e.g., to a cost center, project).
    requisitioner_name, Name of the person requesting the purchase.
    vendor, Preferred supplier for the material or service, if known. If there are multiple vendors then this may not be filled.
    status, Current status of the requisition (e.g., Pending, Draft, In Review, Approved).
    requisition_date, The date the purchase requisition was created.
    procurement_type, Depending on the ERP the procurement type may differ.
    charge_account, The GL or other cost objects that the PR/PO should be charged against.
    deliver_to_location, self evident.
    need_by_date, self evident.
    promise_date, The date by when the vendor promises to deliver the product or service.
    buyer, self evident.
    requisition_total, Total value of the PR.
    tax, Tax related to the PR.
    '''
    
    ## let's run a separate experiment 
    data = {
        "messages": [
            {
                "role": "system",
                "content": f"You are an AI assistant that analyzes financial documents like contract. You will be asked to verify the answers of another AI to questions based on contract documents. You will be provided the transcript of the document, the question asked to the AI and the AI's response. You have to respond with just 0 or 1. 0 if the AI's answer is wrong or incorrect, 1 if it is correct or accurate. Do not respond with anything else, just respond 0 or 1. A description of some of the fields or questions to be asked to you can be found here: {description_of_fields}. For the addresses and locations, the answers of the AI are supposed to look like {address_prototype}. If the AI answered NA and the the question can not be answered based on the document, then respond 1. If the question can be answered based on the document and the AI still answered NA, then respond with 0. Anyway, the response should only be 0 or 1, and nothing else"
            },
            {
                "role": "user",
                "content": f"Given the following contract document: {extracted_text}, the following question: {question} was asked to an AI. The AI gave the following answer: {answer}. Based on the document, is the answer of the AI okay or not? Respond with either 0 or 1. Respond with 0 if the answer is incorrect. Respond with 1 if the answer is correct. Do not give any response which is not 0 or 1. If the AI answered NA and the the question can not be answered based on the document, then respond 1. If the question can be answered based on the document and the AI still answered NA, then respond with 0."
            }
        ]
    }

    try:
        response = requests.post(url, headers=headers, json=data)
        if response.status_code == 200:
            response_json = response.json()
            message = response_json['choices'][0]['message']['content'].strip()
            if message == "1":
                return "Yes"
            elif message == "0":
                return "No"
            else:
                return "Verification failed"  # Unexpected response
        else:
            print("Verification Error:", response.status_code)
            return "Verification failed"
    except Exception as e:
        print(f"Verification Exception: {str(e)}")
        return "Verification failed"

# def process_all_documents():
#     results = {}
#     agreement_counter = {field: 0 for field in fields_to_extract.keys()}
#     total_docs = 0

#     for filename in os.listdir(INPUT_FOLDER):
#         file_path = os.path.join(INPUT_FOLDER, filename)
#         if not os.path.isfile(file_path):
#             continue

#         print(f"Processing file: {filename}")
        
#         extracted_text = upload_file_v2(file_path)

#         if not extracted_text.strip():
#             print("OCR failed or empty.")
#             results[filename] = {"error": "OCR failed"}
#             continue

#         doc_result = {}

#         for key, question in fields_to_extract.items():
#             prompt = generate_prompt_for_field(question, extracted_text)
#             llm_response = base_summarizer(prompt)

#             if isinstance(llm_response, list) and len(llm_response) > 0:
#                 answer = llm_response[0].strip()
#             else:
#                 answer = "No response"

#             # Call Azure verifier
#             verification = verify_answer(question, extracted_text, answer)
            
#             ### Response of the verifier
#             print("################################################")
#             print(f"Verifier response from azure openai: {verification}")
#             print("################################################")

#             is_correct = False
#             if verification:
#                 if verification.strip().lower() == "yes":
#                     is_correct = True

#             if is_correct:
#                 agreement_counter[key] += 1

#             doc_result[key] = {
#                 "question": question,
#                 "answer": answer,
#                 "extracted_text": extracted_text,
#                 "is_correct": is_correct
#             }

#         results[filename] = doc_result
#         total_docs += 1

#     # Save detailed results
#     with open("detailed_results_v3.json", "w") as f:
#         json.dump(results, f, indent=4)

#     # Calculate accuracy per field
#     accuracy = {}
#     for key in fields_to_extract.keys():
#         if total_docs > 0:
#             acc = (agreement_counter[key] / total_docs) * 100
#         else:
#             acc = 0.0
#         accuracy[key] = f"{acc:.3f}%"

#     with open("accuracy_results_v3.json", "w") as f:
#         json.dump(accuracy, f, indent=4)

#     print("Processing completed. Results saved to detailed_results.json and accuracy_results.json")

import time

def process_all_documents():
    results = {}
    agreement_counter = {field: 0 for field in fields_to_extract.keys()}
    total_docs = 0

    # New counters for non-NA accuracy
    agreement_counter_non_na = {field: 0 for field in fields_to_extract.keys()}
    total_non_na_counts = {field: 0 for field in fields_to_extract.keys()}

    for filename in os.listdir(INPUT_FOLDER):
        file_path = os.path.join(INPUT_FOLDER, filename)
        if not os.path.isfile(file_path):
            continue

        print(f"Processing file: {filename}")
        
        extracted_text = upload_file_v2(file_path)

        if not extracted_text.strip():
            print("OCR failed or empty.")
            results[filename] = {"error": "OCR failed"}
            continue

        doc_result = {}

        for key, question in fields_to_extract.items():
            prompt = generate_prompt_for_field(question, extracted_text)
            
            ## This is for previous checker
            #llm_response = base_summarizer(prompt)
            
            ## Deepinfra checker 
            llm_response = base_summarizer(prompt)

            if isinstance(llm_response, list) and len(llm_response) > 0:
                answer = llm_response[0].strip()
            else:
                answer = "No response"

            # Retry verification until a valid yes/no is received
            while True:
                try:
                    verification = verify_answer(question, extracted_text, answer)

                    print("################################################")
                    print(f"Verifier response from azure openai: {verification}")
                    print("################################################")

                    if verification and verification.strip().lower() in {"yes", "no"}:
                        break
                    else:
                        print("Invalid verifier response. Retrying in 1 second...")
                        time.sleep(1)
                except Exception as e:
                    print(f"Verifier call failed. Retrying in 1 second...")
                    time.sleep(1)

            is_correct = verification.strip().lower() == "yes"

            if is_correct:
                agreement_counter[key] += 1

            # Non-NA accuracy logic
            if answer.strip().upper() != "NA":
                total_non_na_counts[key] += 1
                if is_correct:
                    agreement_counter_non_na[key] += 1

            doc_result[key] = {
                "question": question,
                "answer": answer,
                "extracted_text": extracted_text,
                "is_correct": is_correct
            }

        results[filename] = doc_result
        total_docs += 1

    # Save detailed results
    with open("detailed_results_v4.json", "w") as f:
        json.dump(results, f, indent=4)

    # Calculate overall accuracy per field
    accuracy = {}
    for key in fields_to_extract.keys():
        if total_docs > 0:
            acc = (agreement_counter[key] / total_docs) * 100
        else:
            acc = 0.0
        accuracy[key] = f"{acc:.3f}%"

    with open("accuracy_results_v4.json", "w") as f:
        json.dump(accuracy, f, indent=4)

    # Calculate accuracy ignoring NA answers
    accuracy_non_na = {}
    for key in fields_to_extract.keys():
        total_non_na = total_non_na_counts[key]
        if total_non_na > 0:
            acc_na = (agreement_counter_non_na[key] / total_non_na) * 100
        else:
            acc_na = 0.0
        accuracy_non_na[key] = f"{acc_na:.3f}%"

    with open("accuracy_results_v4_NA.json", "w") as f:
        json.dump(accuracy_non_na, f, indent=4)

    print("Processing completed. Results saved to detailed_results_v3.json, accuracy_results_v3.json and accuracy_results_v3_NA.json")

if __name__ == "__main__":
    process_all_documents()