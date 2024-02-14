from arcgis.gis import GIS

class Inventory:
    """
    Represents an ArcGIS Portal instance.

    Args:
        url (str, optional): The URL of the ArcGIS Portal. Defaults to "https://www.arcgis.com".
        token (str, optional): The authentication token for the portal. Defaults to None.
        profile (str, optional): The name of the ArcGIS profile to use for authentication. Defaults to None.
        username (str, optional): The username for authentication. Required if `token` and `profile` are not provided. Defaults to None.
        password (str, optional): The password for authentication. Required if `token` and `profile` are not provided. Defaults to None.

    Attributes:
        url (str): The URL of the ArcGIS Portal.
        profile (str): The name of the ArcGIS profile used for authentication.
        username (str): The username used for authentication.
        password (str): The password used for authentication.
        _token (str): The authentication token for the portal.
        _conn (arcgis.gis.GIS): The connection object to the ArcGIS Portal.

    Raises:
        ValueError: If no connection information is provided (either `token`, `profile`, or `username` and `password`).

    """

    def __init__(
        self,
        url: str = "https://www.arcgis.com",
        token: str = None,
        profile: str = None,
        username: str = None,
        password: str = None,
    ):
        self.url = url
        self.profile = profile
        self.username = username
        self.password = password
        self._token = token
        self._conn = None

    @property
    def conn(self):
        """
        Get the connection object to the ArcGIS Portal.

        Returns:
            arcgis.gis.GIS: The connection object.

        Raises:
            ValueError: If no connection information is provided (either `token`, `profile`, or `username` and `password`).

        """
        # If we don't have a connection object, create one
        if not self._conn:
            if self._token:
                self._conn = GIS(url=self.url, token=self._token, verify_cert=False)
            elif self.profile:
                self._conn = GIS(profile=self.profile, verify_cert=False)
            elif self.username and self.password:
                self._conn = GIS(
                    url=self.url,
                    username=self.username,
                    password=self.password,
                    verify_cert=False,
                )
            else:
                raise ValueError(
                    "No connection information provided, must provide either a token, profile, or username and password"
                )
        return self._conn

    def zip_coords(self, zip_code: str):
        """
        Retrieves the coordinates of the boundary for a given zip code.

        Args:
            zip_code (str): The zip code for which to retrieve the boundary coordinates.

        Returns:
            list: The coordinates of the zip code boundary.

        Raises:
            ValueError: If no results are found for the specified zip code.
        """
        # Get the zip code item
        zip_boundaries = self.conn.content.get("91379236cdca4fd88f3682283f63953e")
        # Grab the layer with the zip code boundaries
        zip_boundaries_lyr = zip_boundaries.layers[3]
        # Query the zip code boundaries layer for the specified zip code
        results = zip_boundaries_lyr.query(
            where=f"ZIP_CODE='{zip_code}'", out_fields="*"
        )
        # If we have results, return the coordinates of the zip code boundary
        if len(results) > 0:
            return results.features[0].geometry["rings"][0]
        else:
            raise ValueError(f"No results found for zip code {zip_code}")

    def polygon_intersects_bbox(self, polygon_coords, bbox_coords):
        """Checks if a polygon intersects with a bounding box.

        Args:
            polygon_coords (list): List of coordinates representing the polygon.
            bbox_coords (list): List of coordinates representing the bounding box.

        Returns:
            bool: True if the polygon intersects with the bounding box, False otherwise.
        """
        # Extract the coordinates of the polygon
        polygon_x = [coord[0] for coord in polygon_coords]
        polygon_y = [coord[1] for coord in polygon_coords]

        # Extract the coordinates of the bounding box
        bbox_min_x, bbox_min_y, bbox_max_x, bbox_max_y = (
            bbox_coords[0][0],
            bbox_coords[0][1],
            bbox_coords[1][0],
            bbox_coords[1][1],
        )

        # Check if any of the polygon's vertices are inside the bounding box
        for x, y in zip(polygon_x, polygon_y):
            if bbox_min_x <= x <= bbox_max_x and bbox_min_y <= y <= bbox_max_y:
                return True

        # Check if any of the bounding box's vertices are inside the polygon
        if (
            polygon_x[0] <= bbox_min_x <= polygon_x[1]
            and polygon_y[0] <= bbox_min_y <= polygon_y[3]
        ):
            return True

        return False

    def items_search(
        self,
        append_search_string: str = None,
        return_count: int = 10000,
        start: int = 1,
        sort_field: str = "modified",
        sort_order: str = "desc",
        zip_code: str = None,
    ):
        """Performs an advanced search for items in the ArcGIS Enterprise or ArcGIS Online organization.

        Args:
            append_search_string (str, optional): Additional search string to be appended to the search query. Defaults to None.
            return_count (int, optional): Maximum number of items to return. Defaults to 10000.
            start (int, optional): Starting index of the search results. Defaults to 1.
            sort_field (str, optional): Field to sort the search results by. Defaults to "modified".
            sort_order (str, optional): Sort order of the search results ("asc" or "desc"). Defaults to "desc".
            zip_code (str, optional): Zip code to filter the search results by. Defaults to None.

        Returns:
            list: List of search results as dictionaries.
        """
        # First, building the search string

        search_string = f'(orgid:"{self.conn.properties["id"]}")'

        # If we have an additional search string, we need to add it to the search string
        if append_search_string:
            search_string += f" AND ({append_search_string})"

        # Perform the search
        search_results = self.conn.content.advanced_search(
            query=search_string,
            sort_field=sort_field,
            sort_order=sort_order,
            max_items=return_count,
            start=start,
            as_dict=True,
        )["results"]

        if zip_code:
            zip_coords = self.zip_coords(zip_code)
            search_results = [
                result
                for result in search_results
                if result["extent"]
                and self.polygon_intersects_bbox(zip_coords, result["extent"])
            ]

        return search_results
