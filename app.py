from database import create_table, insert_product, update_product, get_product
from utils import detect_issues, improve_product

create_table()

product = {
    "name": "T-shirt",
    "description": "Nice shirt",
    "category": "",
    "attributes": {}
}

# Insert original
insert_product(product)

# Detect issues
issues = detect_issues(product)
print("Issues:", issues)

# Improve
improved = improve_product(product)

# Update DB (assuming ID = 1 for now)
update_product(1, improved)

# Fetch and print
data = get_product(1)
print("Stored Data:", data)