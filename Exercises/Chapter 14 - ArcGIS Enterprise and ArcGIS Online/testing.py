from gis_inventory import Portal, MashUp

# Create a new Portal object

agol = Portal(profile="dyaw_Arch", url="https://www.arcgis.com")

z = agol.search(searching_for = "roles")
x = agol.search(searching_for="users")

ms = MashUp(portals=[agol])

x = ms.search()

x = ms.search()

results = agol.search(limit=124)
print(len(results))
results = agol.search()
print(len(results))
results = agol.search(start=200)
print(len(results))
print(agol.token)
