from __future__ import annotations

import datetime
from typing import Any, Dict, List

from sqlalchemy import JSON, TIMESTAMP, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship, composite
from sqlalchemy.schema import ForeignKeyConstraint
from sqlalchemy.types import LargeBinary, String, Integer

type_annotation_map = {
    JSON: JSON,
    bytes: LargeBinary(),
    datetime.datetime: TIMESTAMP(timezone=True),
    Dict[str, Any]: JSON,
    List[Any]: JSON,
}


class InventoryDatabase(DeclarativeBase):
    type_annotation_map = type_annotation_map


class Portals(InventoryDatabase):
    __tablename__ = "portals"

    url: Mapped[str] = mapped_column(String(), primary_key=True)
    token: Mapped[bytes] = mapped_column(String(), nullable=True)
    expires: Mapped[str] = mapped_column(
        Integer, nullable=True
    )
    last_inventoried: Mapped[datetime.datetime] = mapped_column(
        TIMESTAMP(timezone=True), nullable=True
    )



class Items(InventoryDatabase):
    __tablename__ = "items"

    itemId: Mapped[int] = mapped_column(Integer, primary_key=True)
    portal_url: Mapped[str] = mapped_column(String, primary_key=True)
    title: Mapped[str] = mapped_column(String, nullable=True)
    name: Mapped[str] = mapped_column(String, nullable=True)
    type: Mapped[str] = mapped_column(String, nullable=True)
    typeKeywords: Mapped[List[str]] = mapped_column(JSON, nullable=True)
    description: Mapped[str] = mapped_column(String, nullable=True)
    tags: Mapped[List[str]] = mapped_column(JSON, nullable=True)

