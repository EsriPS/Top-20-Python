import pathlib

from .models import InventoryDatabase, Portals
from sqlalchemy import create_engine, select, update, delete

from sqlalchemy.orm import sessionmaker


class Database:
    """A class representing a database for GIS inventory explorer."""

    def __init__(
        self,
        path: str = None,
    ):
        """
        Initialize the Database object.

        Args:
            path (str, optional): The path to the database file. If not provided, a default path will be used.
        """
        self.path = path
        self._session = None

        # Create the db on instantiation
        if self.path is None:
            self.path = str(
                pathlib.Path(pathlib.Path.home(), "GIS_Inventory_Explorer_Data.sqlite")
            )
        windows_path = pathlib.Path(self.path)
        if not windows_path.parent.exists():
            windows_path.parent.mkdir(parents=True)

        engine = create_engine(f"sqlite:///{self.path}", echo=False)
        if not pathlib.Path(self.path).exists():
            InventoryDatabase.metadata.create_all(engine)

    def engine(self):
        """
        Get the database engine.

        Returns:
            sqlalchemy.engine.Engine: The database engine.
        """
        return create_engine(f"sqlite:///{self.path}", echo=False)

    @property
    def session(self):
        """
        Get the database session.

        Returns:
            sqlalchemy.orm.Session: The database session.
        """
        session_factory = sessionmaker(bind=self.engine())
        return session_factory()

    def get_portals(self, rows=10, page=1):
        """
        Get a list of portals from the database.

        Args:
            rows (int, optional): The number of rows to retrieve. Defaults to 10.
            page (int, optional): The page number. Defaults to 1.

        Returns:
            list: A list of dictionaries representing the portals.
        """
        stmt = select(Portals)
        results = self.session.scalars(stmt).all()
        return [record.__dict__ for record in results]

    def add_portal(self, url: str):
        """
        Add a portal to the database.

        Args:
            url (str): The URL of the portal.
        """
        session = self.session
        session.add(Portals(url=url))
        session.commit()
        session.close()

    def add_portal_token(self, url: str, token: str, expires: str):
        """
        Add a portal token to the database.

        Args:
            url (str): The URL of the portal.
            token (str): The token to add.
            expires (str): The expiration date of the token.
        """
        session = self.session
        update_stmt = (
            update(Portals)
            .where(Portals.url == url)
            .values(token=token, expires=expires)
        )
        session.execute(update_stmt)
        session.commit()
        session.close()

    def delete_portal(self, url: str):
        """
        Delete a portal from the database.

        Args:
            url (str): The URL of the portal to delete.
        """
        session = self.session
        delete_stmt = delete(Portals).where(Portals.url == url)
        session.execute(delete_stmt)
        session.commit()
        session.close()
