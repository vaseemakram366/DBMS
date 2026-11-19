# Durability Simulation


import json

accounts = {
    "Alice": 4000,
    "Bob": 4000
}

with open("accounts.json", "w") as file:
    json.dump(accounts, file)

print("Transaction Committed!")
print("Data Saved Successfully!")

with open("accounts.json", "r") as file:
    saved_accounts = json.load(file)

print("\nRecovered Database:")
print(saved_accounts)
