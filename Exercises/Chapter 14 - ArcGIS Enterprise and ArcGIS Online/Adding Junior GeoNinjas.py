from arcgis.gis import GIS
import pandas as pd
import random
import string


def random_password(length: int = 32) -> str:
    """Generates a random password

    Returns
        str Random password
    """
    new_password = "".join(
        random.choice(string.ascii_letters + string.digits) for _ in range(length - 2)
    )
    return f"{random.choice(string.ascii_letters)}{new_password}{random.choice(string.ascii_letters)}"


agol = GIS(profile="my_profile")

agol.users.roles.all()

junior_geoninja_role_privliges = agol.users.roles.all()[3].privileges.copy()

junior_geoninja_role_privliges.append("portal:user:shareToGroup")

new_role = agol.users.roles.create(
    name="Junior GeoNinja",
    description="Junior GeoNinja's role",
    privileges=junior_geoninja_role_privliges,
)

new_group = agol.groups.create(
    title="Junior GeoNinjas Group",
    tags="Junior GeoNinja",
    description="This is a group for Junior GeoNinjas",
)

new_role_id = new_role.role_id

junior_geoninjas = pd.read_excel("Junior GeoNinjas.xlsx")

junior_geoninjas

for ninja in junior_geoninjas.iterrows():
    # Make a username
    username = f"{ninja[1]['First Name'][0]}{ninja[1]['Last Name']}_GeoNinja"
    # Temporary password
    temp_password = random_password()
    # Create the user
    new_user = agol.users.create(
        username=username,
        password=temp_password,
        firstname=ninja[1]["First Name"],
        lastname=ninja[1]["Last Name"],
        email=ninja[1]["Email"],
        role=new_role.role_id,
        description="I'm a Junior Geoninja!",
    )
    # Add thumbnail
    new_user.update(thumbnail=f"{ninja[1]['Favorite Esri Product']}.jpg")
    # Add to group
    new_group.add_users([username])
    print(f"User {username} created with password {temp_password}")
