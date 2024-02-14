from gis_inventory import Inventory

# Create a new Portal object

agol = Inventory(profile="dyaw_Arch", url="https://www.arcgis.com")

x = agol.items_search(zip_code="19046")

print(x)
