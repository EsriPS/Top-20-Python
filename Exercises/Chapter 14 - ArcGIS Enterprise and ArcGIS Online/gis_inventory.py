from arcgis.gis import GIS
import requests
from typing import Optional
from operator import itemgetter
import datetime

ESRI_BUILTIN_USERS = [
    "esri",
    "esri_apps",
    "esri_ar",
    "esri_boundaries",
    "esri_bs",
    "esri_ca",
    "esri_cs",
    "esri_da",
    "esri_de",
    "esri_demographics",
    "esri_el",
    "esri_en",
    "esri_es",
    "esri_et",
    "esri_fi",
    "esri_fr",
    "esri_he",
    "esri_hi",
    "esri_hk",
    "esri_hr",
    "esri_hu",
    "esri_id",
    "esri_ind",
    "esri_it",
    "esri_ja",
    "esri_ko",
    "esri_livingatlas",
    "esri_lt",
    "esri_lv",
    "esri_nav",
    "esri_nav",
    "esri_nb",
    "esri_nl",
    "esri_pl",
    "esri_po",
    "esri_pt",
    "esri_ro",
    "esri_ru",
    "esri_sl",
    "esri_sr",
    "esri_sv",
    "esri_th",
    "esri_tr",
    "esri_tw",
    "esri_vi",
    "esri_zh",
]


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

    @property
    def org_id(self):
        """
        Get the organization ID of the portal.

        Returns:
            str: The organization ID.

        """
        return self.conn.properties["id"]

    def total_possible_results(self, searching_for: str = "items"):
        """
        Get the total possible results for a search.

        Args:
            searching_for (str, optional): The type of search. Defaults to "items".

        Returns:
            int: The total possible results.

        """
        return self.search(searching_for=searching_for, limit=1)["total_possible"]

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

        search_string = f'(orgid:"{self.org_id}")'

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


class MashUp:
    """
    Represents a mashup of search results from multiple ArcGIS Portals.

    Args:
        portals (list[Portal]): A list of Portal instances to search.
        searching_for (str, optional): The type of search. Defaults to "items".
        append_search_string (str, optional): Additional search string to append to the query. Defaults to None.
        limit (int, optional): The maximum number of results to return. Defaults to None.
        pagination_size (int, optional): The number of results to retrieve per request. Defaults to 100.

    Attributes:
        portals (list[Portal]): A list of Portal instances to search.
        searching_for (str): The type of search.
        append_search_string (str): Additional search string to append to the query.
        limit (int): The maximum number of results to return.
        pagination_size (int): The number of results to retrieve per request.
        _last_result_date (dict): A dictionary to store the last modified date for each portal.
        _cached_results (list[dict]): A list to cache the merged search results.

    """

    def __init__(
        self,
        portals: list[Portal],
        searching_for: str = "items",
        append_search_string: Optional[str] = None,
        limit: Optional[int] = None,
        pagination_size: int = 100,
    ):
        self.portals = portals
        self.searching_for = searching_for
        self.append_search_string = append_search_string
        self.limit = limit
        self.pagination_size = pagination_size
        self._last_result_date = {}
        self._cached_results = []

    def clear_cached_results(self):
        """
        Clear the cached search results.

        """
        self._cached_results = []

    def merge_results(self, lists_of_dicts: list[list[dict]]):
        """
        Merge multiple lists of dictionaries into a single list of unique dictionaries.

        Args:
            lists_of_dicts (list[list[dict]]): The lists of dictionaries to merge.

        Returns:
            list[dict]: The merged list of unique dictionaries.

        """
        merged_lists = []
        for list_of_dicts in lists_of_dicts:
            if list_of_dicts != []:
                merged_lists += list_of_dicts
        unique_dicts = {}
        for dictionary in merged_lists:
            key = (dictionary["id"], dictionary["portal_url"])
            if (
                key not in unique_dicts
                or dictionary["modified"] > unique_dicts[key]["modified"]
            ):
                unique_dicts[key] = dictionary
        return list(unique_dicts.values())

    def search(self, start=0, limit=None):
        """
        Perform a search across multiple ArcGIS Portals. This method will cache the
        search results and only perform new searches if the last modified date of the
        search results is greater than the last modified date of the cached results.

        Args:
            start (int, optional): The starting position of the search results. Defaults to 0.
            limit (int, optional): The maximum number of results to return. Defaults to None.

        Returns:
            list[dict]: The search results.

        """
        all_results = []
        for portal in self.portals:
            if portal.url in self._last_result_date:
                modified_string = f"modified: [{self._last_result_date[portal.url]+.001} TO {datetime.datetime.now().timestamp()*1000}]"
            else:
                modified_string = None

            if modified_string and self.append_search_string:
                search_string = (
                    f"({modified_string}) AND ({self.append_search_string}))"
                )
            elif modified_string:
                search_string = modified_string
            elif self.append_search_string:
                search_string = self.append_search_string
            else:
                search_string = None

            results = portal.search(
                searching_for=self.searching_for,
                append_search_string=search_string,
                limit=limit,
                pagination_size=self.pagination_size,
            )
            if results["results"]:
                self._last_result_date[portal.url] = max(
                    results["results"], key=lambda x: x["modified"]
                )["modified"]
                all_results += results["results"]

        if all_results:
            self._cached_results = sorted(
                self.merge_results([self._cached_results, all_results]),
                key=itemgetter("modified"),
                reverse=True,
            )
        return self._cached_results[start:limit]
