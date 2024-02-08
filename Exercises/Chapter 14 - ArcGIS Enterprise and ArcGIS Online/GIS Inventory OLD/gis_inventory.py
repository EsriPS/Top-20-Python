from arcgis.gis import GIS
import requests
from typing import Optional
from operator import itemgetter



def calculate_bounding_box_center(bounding_box):
    # e.g. [[-75.28026781008568, 39.8670120458895], [-74.95576471415357, 40.1380001070083]]
    max_lat, min_lat = bounding_box[0][1], bounding_box[1][1]
    max_lon, min_lon = bounding_box[1][0], bounding_box[0][0]
    center_lat = (max_lat + min_lat) / 2
    center_lon = (max_lon + min_lon) / 2
    return [center_lon, center_lat]


class Portal:
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
    def token(self):
        """
        Get the authentication token for the portal.

        Returns:
            str: The authentication token.

        """
        return self.conn._con.token

    @property
    def conn(self):
        """
        Get the connection object to the ArcGIS Portal.

        Returns:
            arcgis.gis.GIS: The connection object.

        Raises:
            ValueError: If no connection information is provided (either `token`, `profile`, or `username` and `password`).

        """
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

    def search(
        self,
        searching_for: str = "items",
        append_search_string: Optional[str] = None,
        limit: Optional[int] = None,
        start: int = 0,
        pagination_size: int = 100,
    ):
        """
        Perform a search on the ArcGIS Portal.

        Args:
            searching_for (str, optional): The type of search. Defaults to "items".
            append_search_string (str, optional): Additional search string to append to the query. Defaults to None.
            limit (int, optional): The maximum number of results to return. Defaults to None.
            start (int, optional): The starting position of the search results. Defaults to 0.
            pagination_size (int, optional): The number of results to retrieve per request. Defaults to 100.

        Returns:
            dict: The search results, including the list of results, total possible results, and total returned results.

        Raises:
            ValueError: If `searching_for` is not one of 'items', 'groups', 'users', or 'roles'.

        """
        results = []

        search_string = f'(orgid:"{self.conn.properties["id"]}")'

        if append_search_string:
            search_string += f" AND ({append_search_string})"

        if limit and limit < pagination_size:
            pagination_size = limit

        remaining_items = 0

        # The search API is not zero-indexed, so we need to add one to the starting position
        start += 1

        if searching_for == "items":
            url = f"{self.conn.url}/sharing/rest/search"
        elif searching_for == "groups":
            url = f"{self.conn.url}/sharing/rest/community/groups"
        elif searching_for == "users":
            url = f"{self.conn.url}/sharing/rest/community/users"
        elif searching_for == "roles":
            url = f"{self.conn.url}/sharing/rest/portals/self/roles"
        else:
            raise ValueError(
                "searching_for must be one of 'items', 'groups', 'users', or 'roles'"
            )

        while remaining_items is not None:
            # First, setting the pagination size if we have a limit
            if limit and start + pagination_size > limit:
                pagination_size = limit - start + 1

            # Running the search
            params = {
                "q": search_string,
                "sortField": "modified",
                "sortOrder": "desc",
                "num": pagination_size,
                "start": start,
                "f": "json",
                "token": self.token,
            }

            response = requests.get(url, params=params).json()

            # Data for pagination
            total = response["total"]
            results_start = response["start"]

            # Remaining items from search
            if (total - results_start - pagination_size) > 0:
                remaining_items = total - pagination_size
            else:
                remaining_items = None

            # Position of next result for pagination
            start = response["nextStart"]

            # If we have reached the limit, we don't need to continue
            if limit is not None and start >= limit:
                remaining_items = None

            if searching_for == "roles":
                results += response["roles"]
            else:
                results += response["results"]

        for result in results:
            result["portal_url"] = self.url

        return {
            "results": results,
            "total_possible": total,
            "total_returned": len(results),
        }



class CombinedSearch:
    def __init__(
        self,
        portals: list[Portal],
    ):
        self.portals = portals

    def search(
        self,
        searching_for: str = "items",
        append_search_string: Optional[str] = None,
        limit: Optional[int] = None,
        start: int = 0,
        pagination_size: int = 100,
    ):
        all_results = []

        for portal in self.portals:
            # Perform the search
            results = portal.search(
                searching_for=searching_for,
                append_search_string=append_search_string,
                limit=limit,
                pagination_size=pagination_size,
            )
            if results["results"]:
                # Add the results to the list of all results
                all_results += results["results"]

        if all_results:
            # Merge the results and sort them by the modified date
            self._cached_results = sorted(
                all_results,
                key=itemgetter("modified"),
                reverse=True,
            )

        return all_results[start:limit]