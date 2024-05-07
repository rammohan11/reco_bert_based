import re

from fastapi import FastAPI

from pydantic import BaseModel
from pydantic import Field

from vector_api import retrieveMatchingQuery

description = """
Retrieves a recommended automation based on specified criteria.\n\nThis endpoints return responses containing various data types to meet diverse application needs. The response payloads may include strings, numbers, dates, times, files, radio options, checkbox options, dropdown options, table schemas, lists of items, and more. These data types enable flexible interaction with the API, catering to a wide range of use cases and allowing clients to handle different types of information seamlessly.\n\n These information will be part of the description 
"""


class Query(BaseModel):
    query : str = Field(description= "query string used to be used for recommendation")

class Variable(BaseModel):
    name: str = Field(description="Name of the Variable")
    description: str

class Automation(BaseModel):
    id : str = Field(description= "reference Id to be passed for Execution of a Automation")
    title : str = Field(description= "Title of the Automation") 
    description : str = Field(description= "Summary of the Automation")
    requiredInputs: list[Variable] | None = None
    optionalInputs: list[Variable] | None = None
    outputs: list[Variable] | None = None


class Recommendations(BaseModel):
    automations : list[Automation] = Field(description="list of Automation Details")
    

def getAuomation(summary: str):
    m = re.search(r'BOT Id: (\d+),', summary)
    actual_summary = summary.removeprefix(m.group())
    m = re.search(r'\d+', m.group())
    id = m.group()
    title = bot_id_to_title[id]
    variables = bot_id_to_variables[id]
    print(id)
    print(title)
    print(variables)
    return Automation(id=id, title=title, description = actual_summary, requiredInputs=variables["requiredInputs"], optionalInputs=variables["optionalInputs"], outputs=variables["outputs"]) 



bot_id_to_variables ={
    "21" : {
        "requiredInputs" : [Variable(name="requisition_id", description="requisition id is used to retrieve details from workday and cancel requisition")], 
        "optionalInputs" : None,
        "outputs" : None,        
    },
    "32" : {
        "requiredInputs" : [Variable(name="name", description="Name of the Service Account Owner"), Variable(name="EMail", description="Mandatory Email Field that Service account will be associated with"), Variable(name="YearOfBirth", description="Select Year of Birth")],
        "optionalInputs" : [Variable(name="Recovery_Email", description="Email Id used for retrieving the service account"), Variable(name="DateOfBirth", description="Date of Birth of User in dd-mm-yyyy format")],
        "outputs" : [Variable(name="access_code", description="Access Code associated with the Service Account")]
    }
}

bot_id_to_title = {
    "21" : "Cancel Requisition related to Finance Procurement",
    "32" : "Service Account"
}

app = FastAPI(
    title = "Get Automation Recommendation",
    description=description)


@app.post("/automations/list")
async def recommend_bots(q: Query) -> Recommendations:
    
    summary = retrieveMatchingQuery(q.query)
    botdts = [getAuomation(summary=summary)]
    return Recommendations(automations=botdts)

    '''
        botdts = [
            Automation(id="21", title="Cancel Requisition Finance Procurement", description="The BOT cancels a requisition related to Finance Procurement", requiredInputs=[Variable(name="requisition id", description="requisition id is used to retrieve details from workday and cancel requisition")]),
            Automation(id="32", title=summary, description="BOT creates a Service Account", requiredInputs=[Variable(name="name", description="Name of the Service Account Owner"), Variable(name="E-Mail", description="Mandatory Email Field that Service account will be associated with"), Variable(name="Year Of Birth", description="Select Year of Birth")], optionalInputs=[Variable(name="Recovery Email", description="Email Id used for retrieving the service account"), Variable(name="Date Of Birth", description="Date of Birth of User in dd-mm-yyyy format")], outputs=[Variable(name="access code", description="Access Code associated with the Service Account")])
        ]
    '''
    