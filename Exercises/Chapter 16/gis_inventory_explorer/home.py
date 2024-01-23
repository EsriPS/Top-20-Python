import streamlit as st
from data.database import Database
from streamlit_modal import Modal
import arcgis_user_login_streamlit_component
import datetime
import pathlib

import datetime


def convert_esri_time(unix_time):
    """
    Converts a Unix timestamp in milliseconds to a datetime object.

    Args:
        unix_time (int): The Unix timestamp in milliseconds.

    Returns:
        datetime.datetime: The corresponding datetime object.

    """
    if unix_time is None:
        return None
    return datetime.datetime.fromtimestamp(unix_time / 1000)

# Setting up Streamlit multi-page app
st.set_page_config(
    page_title="GIS Inventory Explorer",
    page_icon="☺",
)

# Header content
st.markdown(
    """
    # GIS Inventory Explorer
    Use this app to explore and take inventory of your GIS content!
"""
)

# Allow user to specify or change location of this app's database
# Initalizing value saved to user's session state
if "inventory_path" not in st.session_state:
    st.session_state["inventory_path"] = str(
        pathlib.Path(pathlib.Path.home(), "GIS_Inventory_Explorer_Data.sqlite")
    )

inventory_path_input = st.text_input(
    "Inventory Location", st.session_state.inventory_path, key="inventory-path-input"
)

change_inventory_location = st.button(
    "Change Inventory Location", key="change-inventory-location"
)
if change_inventory_location:
    st.session_state["inventory_path"] = inventory_path_input
    database = Database(st.session_state.inventory_path)
    st.write(f"Inventory path changed to {st.session_state.inventory_path}")

# Initalize Database
database = Database(st.session_state.inventory_path)

# Portal connections
st.header("Portal Connections")

# Add a new Portal connection
portal_modal = Modal(
    "Portal Connection",
    key="portal-modal",
    # Optional
    padding=20,  # default value
    max_width=744,  # default value
)
open_portal_modal = st.button("Add Portal", key="add-portal")
if open_portal_modal:
    portal_modal.open()

if portal_modal.is_open():
    with portal_modal.container():
        container = st.container()
        portal_url = container.text_input("Portal URL")
        if st.button("Add Portal", type="primary"):
            Database().add_portal(portal_url)
            st.write("Portal Added")


# Creating a listing of Portals
portals = database.get_portals()

url_column, token_expire_column, add_token_column = st.columns(3)

url_column.subheader("URL")
token_expire_column.subheader("Token Expires")
add_token_column.subheader("Actions")

for portal in portals:
    url_column.write(portal["url"])

    # Logic for handling token status
    expires = convert_esri_time(portal["expires"])
    token_expire_column.write(expires)
    if portal["expires"] is None:
        open_token_modal = add_token_column.button(
            "Connect", key=f"add-token{portal['url']}"
        )
    else:
        if datetime.datetime.now() > expires:
            open_token_modal = add_token_column.button(
                "Update Connection", key=f"refresh-token{portal['url']}"
            )
        else:
            open_token_modal = add_token_column.button(
                "Refresh Connection", key=f"refresh-token{portal['url']}"
            )

    # Add a new token
    token_modal = Modal(
        "Connect to Portal",
        key=f"token-modal-{portal['url']}",
        # Optional
        padding=20,  # default value
        max_width=744,  # default value
    )

    if open_token_modal:
        token_modal.open()
    if token_modal.is_open():
        with token_modal.container():
            new_token = (
                arcgis_user_login_streamlit_component.arcgis_user_login_streamlit_component()
            )
        if new_token["token"]:
            Database().add_portal_token(
                portal["url"], new_token["token"], new_token["expires"]
            )
