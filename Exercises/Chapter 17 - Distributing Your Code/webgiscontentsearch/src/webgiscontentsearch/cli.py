import argparse
from datetime import datetime
from arcgis.gis import GIS
from . import items_search
import tabulate

def main():
    # Create the argument parser
    parser = argparse.ArgumentParser(
        description="Search for items in ArcGIS Online organization or Portal for ArcGIS"
    )

    # Add the command-line arguments
    parser.add_argument(
        "--url",
        required=True,
        help="URL of the ArcGIS Online organization or Portal for ArcGIS",
    )
    parser.add_argument("--username", required=True, help="Username for authentication")
    parser.add_argument("--password", required=True, help="Password for authentication")
    parser.add_argument(
        "--append_search_string",
        help="Additional search string to be appended to the main search string",
    )
    parser.add_argument("--owner", help="Username of the item owner")
    parser.add_argument(
        "--group", help="Name of the group to filter the search results by"
    )
    parser.add_argument("--tag", help="Tag to filter the search results by")
    parser.add_argument(
        "--content_status",
        choices=["deprecated", "org_authoritative", "public_authoritative"],
        help="Content status to filter the search results by",
    )
    parser.add_argument(
        "--created_from",
        type=datetime.fromisoformat,
        help="Start date of the item creation range (YYYY-MM-DD)",
    )
    parser.add_argument(
        "--created_to",
        type=datetime.fromisoformat,
        help="End date of the item creation range (YYYY-MM-DD)",
    )
    parser.add_argument(
        "--modified_from",
        type=datetime.fromisoformat,
        help="Start date of the item modification range (YYYY-MM-DD)",
    )
    parser.add_argument(
        "--modified_to",
        type=datetime.fromisoformat,
        help="End date of the item modification range (YYYY-MM-DD)",
    )
    parser.add_argument(
        "--output_path", help="Path to save the search results as an Excel file"
    )

    # Parse the command-line arguments
    args = parser.parse_args()

    # Create a GIS object
    gis = GIS(args.url, args.username, args.password)

    # Call the items_search function with the provided arguments
    results = items_search(
        gis=gis,
        append_search_string=args.append_search_string,
        owner=args.owner,
        group=args.group,
        tag=args.tag,
        content_status=args.content_status,
        created_from=args.created_from,
        created_to=args.created_to,
        modified_from=args.modified_from,
        modified_to=args.modified_to,
        output_path=args.output_path,
    )["results"]

    print("Search completed successfully!")

    # Convert the list of dictionaries to a list of lists
    table_data = [[item["title"], item["owner"], item["created"], item["modified"]] for item in results]

    # Print the table
    print(tabulate.tabulate(table_data, headers=["Title", "Owner", "Created", "Modified"], tablefmt="grid"))


if __name__ == "__main__":
    main()
