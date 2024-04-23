import os
from dataclasses import dataclass

import arcpy

SHAPEFILE_EXTS = [
    ".shp",
    ".shx",
    ".dbf",
    ".sbn",
    ".sbx",
    ".fbn",
    ".fbx",
    ".ain",
    ".aih",
    ".atx",
    ".ixs",
    ".mxs",
    ".prj",
    ".xml",
    ".cpg",
    ".shp.xml",
    ".shp.ea.iso.xml",
    ".shp.iso.xml",
]


@dataclass
class File:
    """A class for storing data about a file."""

    name: str
    path: str
    size: str
    created: int
    modified: str
    extension: str
    parent_directory: str
    accessed: str


@dataclass
class Directory:
    name: str
    path: str
    size: str
    created: int
    modified: str
    parent_directory: str


@dataclass
class APRXLayer:
    name: str
    source: str = None
    connection: dict = None


@dataclass
class APRXMap:
    name: str
    layers: list[APRXLayer]

@dataclass
class GeodatabaseData:
    name: str
    type: str
    features: int
    fields: list[str]


@dataclass
class Dataset:
    name: str
    data: list[GeodatabaseData]

@dataclass
class APRX(File):
    name: str
    maps: list[APRXMap]

@dataclass
class FileGeodatabase(File):
    datasets: list[Dataset]
    data: list[GeodatabaseData]


@dataclass
class Shapefile(File):
    features: int
    fields: list[str]


class DirectoryScanner:
    """A class for scanning directories and processing files and directories.

        Args:
        path (str): The path to the directory to be scanned.
        recursive (bool, optional): Flag indicating whether to scan subdirectories recursively. Defaults to True.

    """
    
    def __init__(self, path: str, recursive: bool = True):
        self.path = path
        self.recursive = recursive

    @property
    def path(self):
        """
        str: The path to the directory to be scanned.
        """
        return self._path

    @path.setter
    def path(self, value):
        """
        Setter for the path property.

        Args:
            value (str): The path to be set.

        Raises:
            FileNotFoundError: If the specified path does not exist.
            ValueError: If the specified path is not a directory.
        """
        if not os.path.exists(value):
            raise FileNotFoundError("Path does not exist")
        if not os.path.isdir(value):
            raise ValueError("Path must be a directory")
        self._path = value

    def scan(
        self,
        path: str = None,
        recursive: bool = None,
        _results: list = None,
        _scanned_paths: list = None,
    ):
        """
        Scans the specified directory and its subdirectories for files and directories.

        Args:
            path (str, optional): The path of the directory to scan. If not provided, the default path will be used.
            _results (list, optional): A list to store the scan results. If not provided, a new list will be created.
            _scanned_paths (list, optional): A list to keep track of the scanned paths. If not provided, a new list will be created.
            recursive (bool, optional): Flag indicating whether to scan subdirectories recursively. If not provided, the value specified during object initialization will be used.

        Returns:
            list: A list of scan results.

        Raises:
            FileNotFoundError: If the specified directory is not found.
            PermissionError: If the user does not have permission to access the directory.
        """
        if _results is None:
            _results = []

        if _scanned_paths is None:
            _scanned_paths = []

        if path is None:
            path = self.path

        if recursive is None:
            recursive = self.recursive

        try:
            print(f"Scanning {path}")
            for entry in os.scandir(path):
                if entry.path not in _scanned_paths:
                    _scanned_paths.append(entry.path)
                    if entry.is_file():
                        _results.append(self.parse_result(entry))
                    # If the entry is a directory, scan it.
                    elif entry.is_dir():
                        # If the entry is not a special directory, scan it.
                        if "$" in entry.name:
                            pass
                        if self.recursive:
                            _results.append(self.parse_result(entry))
                            self.scan(
                                path=entry.path,
                                _results=_results,
                                _scanned_paths=_scanned_paths,
                            )

        except FileNotFoundError:
            print("The specified directory was not found.")
        except PermissionError:
            print("You do not have permission to access this directory.")

        return _results

    def parse_result(self, entry: os.DirEntry):
        """
        Parses the given `entry` and returns a `File` or `Directory` object based on the type of entry.

        Args:
            entry (os.DirEntry): The directory entry to parse.

        Returns:
            File or Directory: The parsed object representing the entry.

        Raises:
            ValueError: If the entry is neither a file nor a directory.
        """
        if entry.is_file():
            return File(
                name=entry.name,
                path=entry.path,
                parent_directory=entry.path.split(entry.name)[0],
                extension=entry.name.split(".")[-1],
                size=round(entry.stat().st_size / 1024000, 2),
                created=entry.stat().st_ctime,
                modified=entry.stat().st_mtime,
                accessed=entry.stat().st_atime,
            )
        elif entry.is_dir():
            return Directory(
                name=entry.name,
                path=entry.path,
                parent_directory=entry.path.split(entry.name)[0],
                size=round(entry.stat().st_size / 1024000, 2),
                created=entry.stat().st_ctime,
                modified=entry.stat().st_mtime,
            )
        else:
            raise ValueError("Entry must be a file or directory")


class GeoScanner(DirectoryScanner):
    """Derived class that processes files.

    Args:
        path (str): The path to the directory to be scanned.
        recursive (bool, optional): Flag indicating whether to scan subdirectories recursively. Defaults to True.

    """

    def __init__(self, path: str, recursive: bool = True):
        super().__init__(path, recursive)

    def geoscan(self):
        """Scans the directory for geospatial files and processes them.

        Returns:
            list: A list of processed geospatial files.

        """
        scan_results = self.scan(self.path, self.recursive)
        geoscan_results = []
        for result in scan_results:
            if isinstance(result, File):
                if result.extension == "shp":
                    geoscan_results.append(self.process_shapefile(result))
                elif result.extension == "aprx":
                    geoscan_results.append(self.process_aprx(result))
            elif isinstance(result, Directory):
                if result.name.endswith(".gdb"):
                    geoscan_results.append(self.process_file_geodatabase(result))
        return geoscan_results

    def process_shapefile(self, file: File):
        """Processes a shapefile.

        Args:
            file (File): The shapefile to be processed.

        Returns:
            Shapefile: The processed shapefile.

        Raises:
            ValueError: If the file is not a shapefile.

        """
        if file.extension != "shp":
            raise ValueError("File must be a shapefile")

        # Finding the basename
        basename = file.name.split(".shp")[0]
        # Finding related shapefile parts
        parent_scan = DirectoryScanner(file.parent_directory).scan(
            recursive=False, _results=[]
        )
        related_files = [
            file
            for file in parent_scan
            if isinstance(file, File)
            and basename in file.name
            and any([file.name.endswith(ext) for ext in SHAPEFILE_EXTS])
        ]

        size = sum([file.size for file in related_files])
        features = int(str(arcpy.management.GetCount(file.path)))
        fields = [field.name for field in arcpy.ListFields(file.path)]

        info = file.__dict__ | {
            "size": size,
            "features": features,
            "fields": fields,
        }

        return Shapefile(**info)

    def process_aprx(self, file: File):
        """Processes an ArcGIS Pro project file.

        Args:
            file (File): The ArcGIS Pro project file to be processed.

        Returns:
            APRX: The processed ArcGIS Pro project.

        Raises:
            ValueError: If the file is not an ArcGIS Pro project.

        """
        if file.extension != "aprx":
            raise ValueError("File must be an ArcGIS Pro project")

        aprx = arcpy.mp.ArcGISProject(file.path)

        maps = []

        for aprx_map in aprx.listMaps():
            map_layers = []
            for map_layer in aprx_map.listLayers():
                if map_layer.isFeatureLayer:
                    source = map_layer.dataSource
                    connection = map_layer.connectionProperties
                else:
                    source = None
                    connection = None
                map_layers.append(
                    APRXLayer(
                        name=map_layer.name,
                        source=source,
                        connection=connection,
                    )
                )
            maps.append(
                APRXMap(
                    name=aprx_map.name,
                    layers=map_layers,
                )
            )

        return APRX(
            **file.__dict__,
            maps=maps,
        )

    def process_file_geodatabase(self, directory: Directory):
        """Processes a file geodatabase.

        Args:
            directory (Directory): The file geodatabase directory to be processed.

        Returns:
            FileGeodatabase: The processed file geodatabase.

        Raises:
            ValueError: If the directory is not a file geodatabase.

        """
        if not directory.name.endswith(".gdb"):
            raise ValueError("File must be a file geodatabase")

        root_data = self.process_datasets(
            path=directory.path,
        )

        arcpy.env.workspace = directory.path

        datasets = arcpy.ListDatasets("*", "All")

        for table in arcpy.ListTables("*", "All"):
            root_data.append(
                GeodatabaseData(
                    name=table,
                    type="Table",
                    features=int(str(arcpy.management.GetCount(table))),
                    fields=[field.name for field in arcpy.ListFields(table)],
                )
            )
        datasets = []

        # https://pylint.readthedocs.io/en/latest/user_guide/messages/warning/modified-iterating-list.html
        for dataset in datasets.copy():
            datasets.append(
                Dataset(
                    name=dataset,
                    data=self.process_datasets(
                        path=directory.path,
                        dataset=dataset,
                    ),
                )
            )

        return FileGeodatabase(
            **directory.__dict__,
            datasets=datasets,
            data=root_data,
            extension=None,
            accessed=None,
        )

    def process_datasets(self, path: str, dataset: str = None):
        """Processes datasets within a file geodatabase.

        Args:
            path (str): The path to the file geodatabase.
            dataset (str, optional): The name of the dataset within the file geodatabase. Defaults to None.

        Returns:
            list: A list of processed datasets.

        """
        data_in_dataset = []
        arcpy.env.workspace = path

        for feature_class in arcpy.ListFeatureClasses("*", "All", dataset):
            data_in_dataset.append(
                GeodatabaseData(
                    name=feature_class,
                    type="Feature Class",
                    features=int(str(arcpy.management.GetCount(feature_class))),
                    fields=[field.name for field in arcpy.ListFields(feature_class)],
                )
            )

        return data_in_dataset


if __name__ == "__main__":
    scanner = GeoScanner(r"C:\Users\dan11332\Documents\ArcGIS\Projects\MTK Testing")
    results = scanner.geoscan()
    print(results)
