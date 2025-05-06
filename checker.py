import requests
import json 

class LMModel:
    def __init__(self,
                 model="meta-llama/Llama-3.3-70B-Instruct",
                 api_key="ExaqKHHu4kytO20VEsS173nbUJ7EAjT8",
                 api_url="https://api.deepinfra.com/v1/openai/chat/completions",
                 temperature=0.01,
                 max_tokens=70000):
        
        self.model = model
        self.api_key = api_key
        self.api_url = api_url
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }


    def __call__(self, prompt: str):
        
#         system_prompt = (
#             """You are a professional mathematician and are tasked with solving some competition math problems. You will be given a question, and you have to find the correct solution to it. Think step-by-step and give a detailed explanation of your answer. Each step should be technically correct. Your output should be in the following format: 
#             # STEP BY STEP EXPLANATION
#             <detailed explanation of your thought process>
#             # SKILLS and SKILL LEVEL USED
#             <Answer can be ALGEBRA, GEOMETRY, ANALYSIS, TRIGONOMETRY, TOPOLOGY, ALGEBRA+CALCULUS or any combination of skills expected in an advanced highschool or undergraduate or graduate curriculum. Also mention the difficulty level of the question, high school, undergraduate, graduate or research level. This section should not contain anything other than two comma separated values, first being skill and second being level. For multiple skills, separate skills using + and not comma>
#             # Solution
#             SOLUTION: <solution>
#             """
#         )

        # Added prompts for self reflection
#         system_prompt = (
#             """You are a professional mathematician and are tasked with solving some competition math problems. You will be given a question, and you have to find the correct solution to it. Think step-by-step and give a detailed explanation of your answer. Each step should be technically correct. Your output should be in the following format: 
#             # STEP BY STEP EXPLANATION
#             <detailed explanation of your thought process>
#             # SKILLS and SKILL LEVEL USED
#             <Answer can be ALGEBRA, GEOMETRY, ANALYSIS, TRIGONOMETRY, TOPOLOGY, ALGEBRA+CALCULUS or any combination of skills expected in an advanced highschool or undergraduate or graduate curriculum. Also mention the difficulty level of the question, high school, undergraduate, graduate or research level. This section should not contain anything other than two comma separated values, first being skill and second being level. For multiple skills, separate skills using + and not comma>
#             # Initial Solution
#             INITIAL SOLUTION: <initial solution>
            
#             # Final Solution
#             <reflect on your initial solution, try to find logical inconsistencies if any. And write the final solution
#             FINAL SOLUTION: <final solution> 
#             """
            
#         )
        
    
        # Prompts for the ablation study with self reflection, the model has been prompted to know that the problem statement may be wrong, and its soundness has to be found by the model before attempting any further solutions 
        system_prompt = (
            """You are a professional mathematician and are tasked with solving some competition math problems. You will be given a question. The question itself maybe wrong or have minute mistake. First you have to check the soundness of the problem, and if it is correct then you have to find the correct solution to it. If the problem statement is not correct, just say it is not correct and stop at step by step explanation stage. Think step-by-step and give a detailed explanation of your answer. Each step should be technically correct. Your output should be in the following format: 
            # SOUNDNESS OF THE PROBLEM
            <Is the problem correct/sound or not. This should be a YES or NO answer, followed by short explanation>
            # STEP BY STEP EXPLANATION
            <detailed explanation of your thought process>
            # SKILLS and SKILL LEVEL USED
            <Answer can be ALGEBRA, GEOMETRY, ANALYSIS, TRIGONOMETRY, TOPOLOGY, ALGEBRA+CALCULUS or any combination of skills expected in an advanced highschool or undergraduate or graduate curriculum. Also mention the difficulty level of the question, high school, undergraduate, graduate or research level. This section should not contain anything other than two comma separated values, first being skill and second being level. For multiple skills, separate skills using + and not comma>
            # Initial Solution
            INITIAL SOLUTION: <initial solution>
            
            # Final Solution
            <reflect on your initial solution, try to find logical inconsistencies if any. And write the final solution
            FINAL SOLUTION: <final solution> 
            """
            
        )

        payload = {
            "model": self.model,
            "temperature": self.temperature,
            "max_tokens": self.max_tokens,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt}
            ]
        }

        response = requests.post(self.api_url, headers=self.headers, json=payload)

        if response.status_code != 200:
            raise Exception(f"DeepInfra API error: {response.status_code} - {response.text}")

        json_response = response.json()
        return [json_response["choices"][0]["message"]["content"].strip()]
    
    
    #         self.address_prototype = '''
#         {
#                 "address_line1": "",
#                 "address_line2": "",
#                 "city": "",
#                 "state": "",
#                 "country": "",
#                 "zip_code": "",
#                 "email_address": "",
#                 "phone_number": ""
#         }
#         '''

#         self.item_strings = '''
#         "items" = [
#             {
#                 "item_number": "",
#                 "material_number": "",
#                 "material_group": "",
#                 "description": "",
#                 "unit_price": "",
#                 "unit_of_measurement": "",
#                 "quantity": "",
#                 "expense_gl_account": "",
#                 "department": "",
#                 "ship_to": "",
#                 "net_amount": "",
#                 "gross_total": "",
#                 "tax_rate": "",
#                 "tax_amount": ""
#             }
#         ]
#         '''

#         self.description_of_fields = '''
#         purchase_requisition_number, this is the Unique number for the purchase requisition.
#         item_number, this is the Sequential number for each item in the requisition.
#         material_number, Identifier for the material  ( item) or service being requested.
#         description, Brief description of the material or service.
#         quantity, Amount of the material or service required.
#         unit_of_measurement, Measurement unit for the quantity (e.g., pieces, kilograms).
#         delivery_date,Requested date for the delivery of the material or service.
#         plant,Location or facility where the material or service is needed.
#         storage_location,Specific area within the plant for storing the material.
#         purchasing_group,Identifier for the responsible purchasing group or buyer
#         material_group,Category or group to which the material belongs.
#         account_assignment_category,specifies how the cost will be assigned (e.g., to a cost center, project).
#         requisitioner_name,Name of the person requesting the purchase.
#         vendor,Preferred supplier for the material or service, if known.If there are multiple vendors then this may not be filled
#         status,Current status of the requisition (e.g.,Pending,  Draft, In Review, Approved).
#         requisition_date,The date the purchase requisition was created
#         procurement_type,Depending on the ERP the procurement type may differ 
#         charge_account,The GL or other cost objects that the PR/PO should be chareged against
#         deliver_to_location, self evident 
#         need_by_date, self evident
#         promise_date, The date by when the vendor promises to deliver the product or service
#         buyer, self evident
#         requisition_total, Total value of the PR
#         tax, Tax related to the PR
#         '''



# You are a professional mathematician and are tasked with solving some competition math problems. You are will be given a
# question, and you have to find the correct solution to it. Think step-by-step and give a detailed explanation of your answer. Each step should be technically correct. Your output should be in the following format:
# # STEP BY STEP EXPLANATION
# <detailed explanation of your thought process>
# # SKILLS and SKILL LEVEL USED
# <Answer can be ALGEBRA, GEOMETRY, TRIGONOMETRY, TOPLOGY, ALGEBRA+CALCULUS or any combination of skills expected in an advanced highschool or undergraduate curriculum. Also mention the difficulty level of the question, high school, undergraduate, graduate or research level. This section should not contain anything other than two comma separated values, first being skill and second being level. For multiple skills, separate skills using + and not comma>

# Here are the question and solution to the question:
# QUESTION: <question>
# SOLUTION: <solution>

    
    
    

