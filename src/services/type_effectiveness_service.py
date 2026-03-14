import pokebase
from sqlalchemy.orm import Session
from src.exceptions.entity_not_found_exception import EntityNotFoundException
from src.models.type_effectiveness import TypeEffectiveness
from src.models.type import Type
from src.repository.type_effectiveness_repository import TypeEffectivenessRepository
from src.repository.type_repository import TypeRepository

class TypeEffectivenessService:

    def __init__(self, repository: TypeEffectivenessRepository, type_repository: TypeRepository):
        self.__repository = repository
        self.__type_repository = type_repository

    def populate(self):
        types = pokebase.APIResourceList('type')

        for type in types:
            with self.__type_repository.get_session() as session:
                t_def = self.__type_repository.find_by_name(session, type['name'])

            if t_def is None:
                raise EntityNotFoundException(f"Tipo #{type['name']} não encontrado")

            type_data = pokebase.type_(type['name'])

            with self.__type_repository.get_session() as session:
                self.__build_type_effectiveness(session, type_data.damage_relations.double_damage_from, t_def, 2)
                self.__build_type_effectiveness(session, type_data.damage_relations.half_damage_from, t_def, 0.5)
                self.__build_type_effectiveness(session, type_data.damage_relations.no_damage_from, t_def, 0)
                self.__add_normal_damage_relations(session, t_def)
                session.commit()

    def __build_type_effectiveness(self, session: Session, damage_list: list[str], type_def: Type, multiplier: float):
        for damage in damage_list:            
            t_att = self.__type_repository.find_by_name(session, damage.name)
            if t_att:
                self.__add_relation(session, t_att.id, type_def.id, multiplier)


    def __add_relation(self, session: Session, attack_type_id, defense_type_id, multiplier):
        if not self.__repository.exists_by_primary_key(session, attack_type_id, defense_type_id):
            self.__repository.save(session, TypeEffectiveness(attack_type_id=attack_type_id, defense_type_id=defense_type_id, multiplier=multiplier))

    def __add_normal_damage_relations(self, session: Session, type_def: Type):
        all_types = self.__type_repository.find_all(session)
        existing = self.__repository.find_by_defense_type(session, type_def.id)
        existing_attack_ids = {att_id for (att_id,) in existing}

        for t in all_types:
            if t.id not in existing_attack_ids:
                self.__add_relation(session, t.id, type_def.id, 1)
