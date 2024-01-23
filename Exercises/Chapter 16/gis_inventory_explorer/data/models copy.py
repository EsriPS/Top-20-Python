from __future__ import annotations

import datetime
from typing import Any, Dict, List

from sqlalchemy import JSON, TIMESTAMP, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy.schema import ForeignKeyConstraint
from sqlalchemy.types import LargeBinary, String

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

    url: Mapped[str] = mapped_column(String(256), primary_key=True)
    token: Mapped[bytes] = mapped_column(LargeBinary(), nullable=False)
    expires: Mapped[datetime.datetime] = mapped_column(
        default=datetime.datetime.now() + datetime.timedelta(minutes=30), nullable=False
    )
