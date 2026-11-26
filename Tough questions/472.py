# Shadow Paging Simulation

shadow_pages = {"Page1": 100, "Page2": 200}
current_pages = shadow_pages.copy()

print("Shadow Page Table:", shadow_pages)

# Transaction modifies a page
current_pages["Page1"] = 150

print("Updated Current Page Table:", current_pages)

# Commit: switch to the new page table
shadow_pages = current_pages.copy()

print("After Commit:", shadow_pages)