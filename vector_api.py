from vec_cache import VecCache
from sentence_transformers import SentenceTransformer

summaries=[
    "BOT Id: 21, FinanceProcurement Bot utilises the provided URI to retrieve a custom report from Workday's API. The report is titled BP Requisitions Transactions of Type Awaiting Action for 30 Days and is being requested in JSON format. This URI is likely used in a RESTful GET request to retrieve the report data from the Workday API.  The data provided is a Workday API request to cancel a requisition. The request includes the ID of the requisition to be canceled, which is passed as a $vRequisitionID$ parameter. In summary, the request is to cancel a specific requisition with the ID provided. Finance Procurement.",
    "BOT Id: 32, GCPServiceAccountDeletion bot, relies on a REST Delete request to delete a service account in Google Identity and Access Management (IAM). The `$projectId` and `$sEmail` variables are replaced with the actual project ID and service account email address, respectively. The Delete request sends a request to the IAM API to delete the specified service account.",
    "BOT Id: 43, DHCPMacFiltering bot, generates report related to missing MAC Address. lists device MAC address from Crowd Strike. From the Mac address list got from Crowd strike, compare is with the MAC address list from DHCP server and add the missing MAC address to DHCP server."       
]

model = SentenceTransformer("all-MiniLM-L6-v2")

cache = VecCache(ttl=36000, vector_size=384)

for summary in summaries:
    vector_summary = model.encode(summary)
    
    cache.store_with_vector(summary, vector_summary)


def retrieveMatchingQuery(query: str) -> str:
    vector_query = model.encode(query)
    summary = cache.search_with_vector(vector_query)
    print("summary is : ", summary)
    return summary


if __name__ == "__main__":
    summary = retrieveMatchingQuery("Delete Google Service Account")
