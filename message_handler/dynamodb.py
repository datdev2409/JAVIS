import os
import boto3
from datetime import datetime

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(os.getenv("DYNAMODB_TABLE"))

print("DynamoDB Table: ", table.table_name)


def db_create_transactions(transactions):
    for transaction in transactions:
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        table.put_item(
            Item={
                "PartitionKey": "congdat",
                "SortKey": f"trans#{timestamp}",
                "Name": transaction["name"],
                "Price": transaction["price"],
                "Category": transaction["category"],
            }
        )
        print("Transaction created: ", transaction["name"])
