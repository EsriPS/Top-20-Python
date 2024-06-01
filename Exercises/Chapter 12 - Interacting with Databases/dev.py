import arcpy


file_gdb = r"C:\Users\dav11274\Desktop\github\Top-20-Python\Exercises\Chapter 12 - Interacting with Databases\indoors_test.gdb"

arcpy.env.workspace = file_gdb


arcpy.ListFeatureClasses()

arcpy.ListTables()

arcpy.ListDatasets()

for dataset in arcpy.ListDatasets():
    print(dataset)
    for fc in arcpy.ListFeatureClasses(feature_dataset=dataset):
        print(f"  {fc}")
for fc in arcpy.ListFeatureClasses():
    print(fc)
for table in arcpy.ListTables():
    print(table)



for root, dirs, files in arcpy.da.Walk(file_gdb):
    for file in files:
        print(file)
    for dir in dirs:
        print(dir)









from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class User(Base):
    __tablename__ = "user_account"
    id = Column(Integer, primary_key=True)
    name = Column(String(30))
    fullname = Column(String)
    addresses = relationship(
        "Address", back_populates="user", cascade="all, delete-orphan"
    )
    def __repr__(self):
        return f"User(id={self.id!r}, name={self.name!r}, fullname={self.fullname!r})"

class Address(Base):
    __tablename__ = "address"
    id = Column(Integer, primary_key=True)
    email_address = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey("user_account.id"), nullable=False)
    user = relationship("User", back_populates="addresses")
    def __repr__(self):
        return f"Address(id={self.id!r}, email_address={self.email_address!r})"