import pathlib

import models
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


class Database:
    def __init__(self, schema: str, path: str = None):
        self.schema = schema
        self._path = None  # Initialize _path attribute
        self.path = path
        self.url = f"sqlite://{self.path}"
        self._session = None

    @property
    def path(self):
        return self._path

    @path.setter
    def path(self, value):
        if value is None:
            value = pathlib.Path(
                pathlib.Path.home(), "GIS_Inventory_Explorer", f"{self.schema}.sqlite"
            )
        else:
            value = pathlib.Path(value)

        self._path = value

    def base(self):
        # Grabbing the base
        return getattr(models, self.schema)

    @property
    def engine(self):
        # If the parent directory does not exist, create it.
        if not self.path.parent.exists():
            self.path.parent.mkdir(parents=True)

        return create_engine(self.url)

    @property
    def session(self):
        """Checks for an open DB session, if not, opens one.

        Returns:
            session(object): DB session
        """
        if self._session:
            return self._session
        session = sessionmaker(bind=self.engine)
        self._session = session()
        return self._session
