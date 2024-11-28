from project.configs.connection import DBConnectionHandler
from project.configs.tables import Characters, Base_stats, Attributes, Attributes_progress_bar


class InitialInsert:

    def insert(self, name, total_xp, character_image, hp, stamina, ac, armor, str, dex, cons, wis, int, char,
               str_bar, dex_bar, cons_bar, wis_bar, int_bar, char_bar):
        with DBConnectionHandler() as db:
            try:
                characters_insert = Characters(name=name, total_xp=total_xp, character_image=character_image)
                db.session.add(characters_insert)
                db.session.flush()
                id = characters_insert.id
                base_stats_insert = Base_stats(character_id=id, hp=hp, stamina=stamina, ac=ac, armor=armor)
                attributes_insert = Attributes(character_id=id, str=str, dex=dex, cons=cons, wis=wis, int=int, char=char)
                attributes_progress_bar_insert = Attributes_progress_bar(character_id=id, str_bar=str_bar,
                                                                         dex_bar=dex_bar, cons_bar=cons_bar,
                                                                         wis_bar=wis_bar, int_bar=int_bar,
                                                                         char_bar=char_bar)
                db.session.add_all([base_stats_insert, attributes_insert, attributes_progress_bar_insert])
                db.session.commit()
            except Exception as exception:
                db.session.rollback()
                raise exception


class CharactersTable:
    def select_name(self, name):
        with DBConnectionHandler() as db:
            query = db.session.query(Characters).filter(Characters.name == name.lower()).all()
            return query


    def select_names(self):
        with DBConnectionHandler() as db:
            query = db.session.query(Characters).all()
            return query


    def select_id(self, name):
        with DBConnectionHandler() as db:
            query = db.session.query(Characters).filter(Characters.name == name.lower()).all()[0].id
            return query


    def select_image(self, id):
        with DBConnectionHandler() as db:
            query = db.session.query(Characters).filter(Characters.id == id).all()[0].character_image
            return query


    def select_total_xp(self, id):
        with DBConnectionHandler() as db:
            query = db.session.query(Characters).filter(Characters.id == id).all()[0].total_xp
            return query


    def update_xp(self, id, new_xp):
        with DBConnectionHandler() as db:
            try:
                db.session.query(Characters).filter(Characters.id == id).update({"total_xp": new_xp})
                db.session.commit()
            except Exception as exception:
                db.session.rollback()
                raise exception



class BaseStatsTable:

    def select_all(self, id):
        with DBConnectionHandler() as db:
            query = db.session.query(Base_stats).filter(Base_stats.character_id == id).all()
            return query


class AttributesTable:

    def select_all(self, id):
        with DBConnectionHandler() as db:
            query = db.session.query(Attributes).filter(Attributes.character_id == id).all()
            return query


    def update(self, attribute, attribute_new_value, id):
        with (DBConnectionHandler() as db):
            try:
                db.session.query(Attributes).filter(Attributes.character_id == id).update({attribute:attribute_new_value})
                db.session.commit()
            except Exception as exception:
                db.session.rollback()
                raise exception

class AttributesProgressBarTable:

    def select_all(self, id):
        with DBConnectionHandler() as db:
            query = db.session.query(Attributes_progress_bar).filter(Attributes_progress_bar.character_id == id).all()
            return query


    def update(self, progress_bar, total_attribute_bar, id):
        with (DBConnectionHandler() as db):
            try:
                db.session.query(Attributes_progress_bar).filter(Attributes_progress_bar.character_id == id).update({progress_bar:total_attribute_bar})
                db.session.commit()
            except Exception as exception:
                db.session.rollback()
                raise exception