from project.configs.connection import Base
from sqlalchemy import Column, String, Integer, BLOB, DateTime, ForeignKey, func, CheckConstraint


class Characters(Base):
    __tablename__ = "characters"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, unique=True)
    total_xp = Column(Integer, nullable=False)
    character_image = Column(BLOB)

    def __repr__(self):
        return (f"Characters(id={self.id}, name = {self.name}, total_xp = {self.total_xp}, "
                f"character_image = {self.character_image})")
    

class Base_stats(Base):
    __tablename__ = "base_stats"
    character_id = Column(Integer, ForeignKey("characters.id"), primary_key=True)
    hp = Column(Integer, nullable=False)
    stamina = Column(Integer, nullable=False)
    ac = Column(Integer, nullable=False)
    armor = Column(Integer, nullable=False)
    datetime = Column(DateTime, nullable=False, default=func.now())

    def __repr__(self):
        return (f"Base_stats(character_id={self.character_id}, hp={self.hp}, stamina={self.stamina}, ac={self.ac}, "
                f"armor={self.armor}, datetime={self.datetime})")


class Attributes(Base):
    __tablename__ = "attributes"
    character_id = Column(Integer, ForeignKey("characters.id"), primary_key=True)
    str = Column(Integer, CheckConstraint("str >= 0"), nullable=False)
    dex = Column(Integer, nullable=False)
    cons = Column(Integer, nullable=False)
    wis = Column(Integer, nullable=False)
    int = Column(Integer, nullable=False)
    char = Column(Integer, nullable=False)
    datetime = Column(DateTime, nullable=False, default=func.now())


    def __repr__(self):
        return (f"Attributes(character_id={self.character_id}, str={self.str}, dex={self.dex}, cons={self.cons}, "
                f"wis={self.wis}, int={self.int}, char={self.char}, datetime={self.datetime})")


class Attributes_progress_bar(Base):
    __tablename__ = "attributes_progress_bar"
    character_id = Column(Integer, ForeignKey("characters.id"), primary_key=True)
    str_bar = Column(Integer, nullable=False)
    dex_bar = Column(Integer, nullable=False)
    cons_bar = Column(Integer, nullable=False)
    wis_bar = Column(Integer, nullable=False)
    int_bar = Column(Integer, nullable=False)
    char_bar = Column(Integer, nullable=False)
    datetime = Column(DateTime, nullable=False, default=func.now())

    def __repr__(self):
        return (f"Attributes_progress_bar(character_id={self.character_id}, str_bar={self.str_bar}, "
                f"dex_bar={self.dex_bar}, cons_bar={self.cons_bar}, wis_bar={self.wis_bar}, int_bar={self.int_bar}, "
                f"char_bar={self.char_bar}, datetime={self.datetime})")


