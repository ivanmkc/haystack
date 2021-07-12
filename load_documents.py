from typing import List
from haystack import Document
import gspread
import pandas as pd
from haystack.document_store.elasticsearch import ElasticsearchDocumentStore


def pull_sheet_data(spreadsheet_name, worksheet_name):
    scope = [
        "https://spreadsheets.google.com/feeds",
        "https://www.googleapis.com/auth/drive",
    ]

    gc = gspread.service_account()
    wks = gc.open(spreadsheet_name).worksheet(worksheet_name)

    data = wks.get_all_values()
    headers = data.pop(0)

    return pd.DataFrame(data, columns=headers)


def pull_documents(spreadsheet_name, worksheet_name) -> List[Document]:
    # Pulls data from the entire spreadsheet tab.
    df = pull_sheet_data(spreadsheet_name, worksheet_name)

    # Use data to initialize Document objects
    titles = list(df["title"].values)
    texts = list(df["text"].values)
    tags = list(df["tag"].values)
    documents: List[Document] = []
    for title, text, tag in zip(titles, texts, tags):
        documents.append(
            Document(text=text, meta={"name": title or "", "tag": tag or ""})
        )

    return documents


SPREADSHEET_NAME = "QuestionAnswerCorpus"
WORKSHEET_NAME = "Sheet1"

documents = pull_documents(
    spreadsheet_name=SPREADSHEET_NAME, worksheet_name=WORKSHEET_NAME
)

document_store = ElasticsearchDocumentStore(
    host="10.128.0.22", port=9200, username="", password="", index="document"
)

# Delete existing documents in documents store
document_store.delete_documents()

# Write documents to document store
document_store.write_documents(documents)
