import pokebase
from sqlalchemy.orm import Session
from src.models.type_effectiveness import TypeEffectiveness
from src.models.type import Type
from src.repository.type_effectiveness_repository import TypeEffectivenessRepository
from src.repository.type_repository import TypeRepository
from src.repository.generation_repository import GenerationRepository

class TypeEffectivenessService:

    def __init__(self, 
                repository: TypeEffectivenessRepository, 
                type_repository: TypeRepository, 
                generation_repository: GenerationRepository,
                allowed_types: list[str],
                types_intro_map: dict[str, str]):
        self.__repository = repository
        self.__type_repository = type_repository
        self.__generation_repository = generation_repository
        self.__allowed_types = [t.lower().strip() for t in allowed_types]
        
        self.__types_intro_ids = {}
        self.__raw_intro_map = types_intro_map

    def __prepare_intro_ids(self, session: Session):
        for t_name, gen_name in self.__raw_intro_map.items():
            gen_entity = self.__generation_repository.find_by_name(session, gen_name)
            if gen_entity:
                self.__types_intro_ids[t_name.lower()] = gen_entity.id

    def populate(self):
        with self.__type_repository.get_session() as session:
            self.__prepare_intro_ids(session)
            
            generations = self.__generation_repository.find_all(session)
            all_api_types = pokebase.APIResourceList('type')

            for t_info in all_api_types:
                type_name = t_info['name'].lower()
                if type_name not in self.__allowed_types:
                    continue
                
                print(f" -> Processing type: {type_name}")
                
                type_data = pokebase.type_(type_name)
                t_def = self.__type_repository.find_by_name(session, type_name)
                
                if t_def is None:
                    print(f" [WARN] Type {type_name} not found in local database. Skipping...")
                    continue

                type_intro_gen_id = self.__types_intro_ids.get(type_name, 1)

                for gen in generations:
                    if gen.id < type_intro_gen_id:
                        continue

                    damage_relations = self.__get_damage_relations_for_gen(type_data, gen.id)

                    self.__build_type_effectiveness(session, damage_relations.double_damage_from, t_def, gen.id, 2.0)
                    self.__build_type_effectiveness(session, damage_relations.half_damage_from, t_def, gen.id, 0.5)
                    self.__build_type_effectiveness(session, damage_relations.no_damage_from, t_def, gen.id, 0.0)
                    self.__add_normal_damage_relations(session, t_def, gen.id)
                
                session.commit()
                print(f" [OK] Type effectiveness for {type_name} saved.")

    def __get_damage_relations_for_gen(self, type_data, current_gen_id: int):
        target_relations = type_data.damage_relations
        
        if hasattr(type_data, 'past_damage_relations') and type_data.past_damage_relations:
            sorted_past = sorted(type_data.past_damage_relations, 
                                key=lambda x: int(x.generation.url.split('/')[-2]))
            
            for past in sorted_past:
                past_gen_id = int(past.generation.url.split('/')[-2])
                if current_gen_id <= past_gen_id:
                    target_relations = past.damage_relations
                    break
        
        return target_relations

    def __build_type_effectiveness(self, session: Session, damage_list, type_def: Type, gen_id: int, multiplier: float):
        for damage in damage_list:
            damage_name = damage.name.lower()
            if damage_name not in self.__allowed_types:
                continue
            
            att_intro_gen_id = self.__types_intro_ids.get(damage_name, 1)
            if gen_id < att_intro_gen_id:
                continue
                
            t_att = self.__type_repository.find_by_name(session, damage_name)
            if t_att:
                self.__add_relation(session, t_att.id, type_def.id, gen_id, multiplier)

    def __add_relation(self, session: Session, attack_id: int, defense_id: int, gen_id: int, multiplier: float):
        if not self.__repository.exists_by_primary_key(session, attack_id, defense_id, gen_id):
            new_relation = TypeEffectiveness(
                attack_type_id=attack_id, 
                defense_type_id=defense_id, 
                generation_id=gen_id, 
                multiplier=multiplier
            )
            self.__repository.save(session, new_relation)
            session.flush()

    def __add_normal_damage_relations(self, session: Session, type_def: Type, gen_id: int):
        all_local_types = self.__type_repository.find_all(session)
        allowed_local_types = [t for t in all_local_types if t.name.lower() in self.__allowed_types]
        
        existing_attack_ids = self.__repository.find_attack_ids_by_defense_and_generation(session, type_def.id, gen_id)
        existing_set = set(existing_attack_ids)

        for t_att in allowed_local_types:
            att_name = t_att.name.lower()
            if t_att.id in existing_set:
                continue
            
            att_intro_gen_id = self.__types_intro_ids.get(att_name, 1)
            if gen_id >= att_intro_gen_id:
                self.__add_relation(session, t_att.id, type_def.id, gen_id, 1.0)