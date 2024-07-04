from pymongo import MongoClient
import webbrowser

# Replace the following with your MongoDB connection details
mongo_uri = "mongodb://localhost:27017/"
database_name = "first-research"
collection_name = "unique_project_documents"

# Connect to MongoDB
client = MongoClient(mongo_uri)
db = client[database_name]
collection = db[collection_name]

# Get all documents from the collection
documents = list(collection.find())


# Function to open URL in web browser
def open_url(url):
    webbrowser.open(url)


# Iterate through each document
for count, document in enumerate(documents, start=1):
    # Extract the URL from the document
    html_url = document.get("html_url")
    if html_url:
        print(f"Opening URL: {html_url} ================== {count}")
        open_url(html_url)
        input("Press Enter to proceed to the next document...")
    else:
        print("No 'html_url' found in document, skipping...")

# Close the connection
client.close()
