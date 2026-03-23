import pokebase
from sqlalchemy.orm import Session

from src.exceptions.entity_not_found_exception import EntityNotFoundException
from src.models.base_status import BaseStatus
from src.models.form_ability import FormAbility
from src.models.form_move import FormMove
from src.models.generation import Generation
from src.models.pokemon_form import PokemonForm
from src.models.pokemon_specie import PokemonSpecie
from src.models.pokemon_sprite import PokemonSprite
from src.models.regional_pokedex_number import RegionalPokedexNumber
from src.models.gender import Gender
from src.models.pokemon_gender_ratio import PokemonGenderRatio
from src.models.pokemon_egg_group import PokemonEggGroup
from src.repository.ability_repository import AbilityRepository
from src.repository.base_status_repository import BaseStatusRepository
from src.repository.egg_group_repository import EggGroupRepository
from src.repository.form_ability_repository import FormAbilityRepository
from src.repository.form_move_repository import FormMoveRepository
from src.repository.gender_repository import GenderRepository
from src.repository.generation_repository import GenerationRepository
from src.repository.move_repository import MoveRepository
from src.repository.pokemon_egg_group_repository import PokemonEggGroupRepository
from src.repository.pokemon_form_repository import PokemonFormRepository
from src.repository.pokemon_gender_ratio_repository import PokemonGenderRatioRepository
from src.repository.pokemon_specie_repository import PokemonSpecieRepository
from src.repository.pokemon_sprite_repository import PokemonSpriteRepository
from src.repository.regional_pokedex_number_repository import RegionalPokedexNumberRepository
from src.repository.type_repository import TypeRepository

class PokemonPopulatorService:

    def __init__(self, 
                pokemon_amount: int, 
                repository: PokemonSpecieRepository, 
                regional_pokedex_number_repository :RegionalPokedexNumberRepository, 
                gender_repository: GenderRepository,
                pokemon_gender_ration_repository: PokemonGenderRatioRepository,
                egg_group_repository: EggGroupRepository,
                pokemon_egg_group_repository: PokemonEggGroupRepository,
                generation_repository: GenerationRepository,
                pokemon_form_repository: PokemonFormRepository,
                pokemon_sprite_repository: PokemonSpriteRepository,
                base_status_repository: BaseStatusRepository,
                type_repository: TypeRepository,
                ability_repository: AbilityRepository,
                form_ability_repository: FormAbilityRepository,
                move_repository: MoveRepository,
                form_move_repository: FormMoveRepository
                ):
        self.__pokemon_amount = pokemon_amount
        self.__repository = repository
        self.__regional_pokedex_number_repository = regional_pokedex_number_repository
        self.__gender_repository = gender_repository
        self.__pokemon_gender_ration_repository = pokemon_gender_ration_repository
        self.__egg_group_repository = egg_group_repository
        self.__pokemon_egg_group_repository = pokemon_egg_group_repository
        self.__generation_repository = generation_repository
        self.__pokemon_form_repository = pokemon_form_repository
        self.__pokemon_sprite_repository = pokemon_sprite_repository
        self.__base_status_repository = base_status_repository
        self.__type_repository = type_repository
        self.__ability_repository = ability_repository
        self.__form_ability_repository = form_ability_repository
        self.__move_repository = move_repository
        self.__form_move_repository = form_move_repository

    def populate(self):

        for i in range(1, self.__pokemon_amount + 1):
            print(f"Buscando Pokémon #{i}")
            pokemon = pokebase.pokemon(i)

            with self.__repository.get_session() as session:
                specie = self.__repository.find_by_name(session, pokemon.species.name)
                if specie is None:
                    specie = self.__save_pokemon_specie(session, pokemon.id, pokemon.species.name)

                specie_resource = pokebase.pokemon_species(i)

                self.__save_regional_numbers(session, specie.id, specie_resource.pokedex_numbers)
                self.__save_gender_ratios(session, specie.id, specie_resource.gender_rate)
                self.__save_egg_groups(session, specie.id, specie_resource.egg_groups)

                all_form_names = [variety.pokemon.name for variety in specie_resource.varieties]
                if pokemon.name not in all_form_names:
                    all_form_names.insert(0, pokemon.name)

                
                generations = self.__generation_repository.find_all(session)
                for generation in generations:
                    for form_name in all_form_names:
                        try:
                            form_pokemon = pokebase.pokemon(form_name)
                        except Exception as e:
                            print(f"[WARN] Não foi possível buscar o Pokémon '{form_name}': {e}")
                            continue

                        form = self.__pokemon_form_repository.find_by_specie_id_and_generation_id_and_form_name(session, specie.id, generation.id, form_name)

                        if form is None:
                            form = self.__save_pokemon_form(session, specie.id, form_pokemon, generation.id, form_name)
                            self.__save_base_status(session, form.id, form_pokemon.stats)
                            self.__save_types(session, form, form_pokemon.types)
                            self.__save_abilities(session, form.id, form_pokemon.abilities)
                            self.__save_moves(session, form.id, form_pokemon.moves, generation)
                session.commit()

    def __save_pokemon_specie(self, session: Session, pokedex_number, name) -> PokemonSpecie:
        specie = self.__repository.save(session, PokemonSpecie(pokedex_number=pokedex_number, name=name))
        session.flush()
        return specie

    def __save_regional_numbers(self, session: Session, specie_id: int, pokedex_numbers):
        for entry in pokedex_numbers:
            pokedex_name = entry.pokedex.name
            entry_number = entry.entry_number

            if pokedex_name == "national":
                continue
            
            if not self.__regional_pokedex_number_repository.exists_by_specie_id_and_pokedex_name(session, specie_id, pokedex_name):
                regional_number = RegionalPokedexNumber(
                    specie_id=specie_id,
                    pokedex_name=pokedex_name,
                    entry_number=entry_number,
                )
                self.__regional_pokedex_number_repository.save(session, regional_number)

    def __save_gender_ratios(self, session: Session, specie_id: int, gender_rate):
        if gender_rate == -1:
            gender = self.__get_gender(session, "genderless")
            if not self.__pokemon_gender_ration_repository.exists_by_specie_id_and_gender_id(session, specie_id, gender.id):
                self.__pokemon_gender_ration_repository.save(session, PokemonGenderRatio(specie_id=specie_id, gender_id=gender.id, probability=100))
        else:
            female_prob = (gender_rate / 8) * 100
            male_prob = 100 - female_prob
            female = self.__get_gender(session, "female")
            male = self.__get_gender(session, "male")

            for g, p in [(female, female_prob), (male, male_prob)]:
                if not self.__pokemon_gender_ration_repository.exists_by_specie_id_and_gender_id(session, specie_id, g.id):
                    self.__pokemon_gender_ration_repository.save(session, PokemonGenderRatio(specie_id=specie_id, gender_id=g.id, probability=p))

    def __get_gender(self, session: Session, name: str) -> Gender:
        gender = self.__gender_repository.find_by_name(session, name)
        if gender is None:
            raise EntityNotFoundException(f"Gênero '#{name}' não encontrado")
        return gender

    def __save_egg_groups(self, session: Session, specie_id: int, egg_groups):
        for eg in egg_groups:
            egg_group = self.__egg_group_repository.find_by_name(session, eg.name)
            if egg_group is None:
                raise EntityNotFoundException(f"EggGroup '#{eg.name} não encontrado")

            if not self.__pokemon_egg_group_repository.exists_by_specie_id_and_egg_group_id(session, specie_id, egg_group.id):
                self.__pokemon_egg_group_repository.save(session, PokemonEggGroup(specie_id=specie_id, egg_group_id=egg_group.id))

    def __save_pokemon_form(self, session: Session, specie_id: int, pokemon, generation_id: int, form_name: str) -> PokemonForm:
        form = PokemonForm(
            specie_id = specie_id,
            generation_id = generation_id,
            form_name = form_name,
            height = getattr(pokemon, 'height', None),
            weight = getattr(pokemon, 'weight', None),
            base_experience = pokemon.base_experience,
            is_default = True if form_name == pokemon.name else False,
        )
        self.__pokemon_form_repository.save(session, form)
        session.flush()
        self.__save_sprites(session, form.id, pokemon.sprites)
        return form

    def __save_sprites(self, session: Session, form_id: int, sprites):
        sprite_map = [
            ("front_default", "back_default", "male", False),
            ("front_shiny", "back_shiny", "male", True),
            ("front_female", "back_female", "female", False),
            ("front_shiny_female", "back_shiny_female", "female", True),
            ("front_default", "back_default", "genderless", False),
            ("front_shiny", "back_shiny", "genderless", True),
        ]

        entities = self.__gender_repository.find_all(session)
        genders = {g.name: g for g in entities}

        for front_attr, back_attr, gender_name, is_shiny in sprite_map:
            front_sprite = getattr(sprites, front_attr, None)
            back_sprite = getattr(sprites, back_attr, None)

            if not front_sprite and not back_sprite:
                continue

            gender = genders.get(gender_name)
            if not gender:
                continue

            if not self.__pokemon_sprite_repository.exists_by_specie_id_and_gender_id(session, form_id, gender.id, is_shiny):
                sprite = PokemonSprite(
                    form_id = form_id,
                    gender_id = gender.id,
                    is_shiny = is_shiny,
                    front_sprite = front_sprite,
                    back_sprite = back_sprite
                )
                self.__pokemon_sprite_repository.save(session, sprite)

    def __save_base_status(self, session: Session, form_id: int, pokemon_status):
        stats_dict = {stat.stat.name: stat.base_stat for stat in pokemon_status}

        if "special" in stats_dict and "special-attack" not in stats_dict and "special-defense" not in stats_dict:
            stats_dict["special-attack"] = stats_dict["special"]
            stats_dict["special-defense"] = stats_dict["special"]

        base_status = BaseStatus(
            form_id=form_id,
            hp=stats_dict.get("hp"),
            attack=stats_dict.get("attack"),
            defense=stats_dict.get("defense"),
            special_attack=stats_dict.get("special-attack"),
            special_defense=stats_dict.get("special-defense"),
            speed=stats_dict.get("speed")
        )
        self.__base_status_repository.save(session, base_status)

    def __save_types(self, session: Session, form: PokemonForm, types):
        for type in types:
            type_obj = self.__type_repository.find_by_name(session, type.type.name)
            if type_obj is not None and type_obj not in form.types:
                form.types.append(type_obj)

    def __save_abilities(self, session: Session, form_id: int, abilities):
        for ability in abilities:
            ability_obj = self.__ability_repository.find_by_name(session, ability.ability.name)
            if not self.__form_ability_repository.exists_by_primary_key(session, form_id, ability_obj.id):
                form_ability = FormAbility(
                    form_id = form_id,
                    ability_id = ability_obj.id,
                    is_hidden = ability.is_hidden
                )
                self.__form_ability_repository.save(session, form_ability)

    def __save_moves(self, session: Session, form_id: int, moves, generation: Generation):
        for move in moves:
            move_obj = self.__move_repository.find_by_name(session, move.move.name)
            if move_obj is None:
                continue

            for vg in generation.version_groups:
                vg_detail = next(
                    (d for d in move.version_group_details if d.version_group.name == vg.name),
                    None
                )
                if vg_detail is None:
                    continue

                if not self.__form_move_repository.exists_by_primary_key(session, form_id, move_obj.id, vg.id):
                    form_move = FormMove(
                        form_id=form_id,
                        move_id=move_obj.id,
                        version_group_id=vg.id,
                        move_learn_method=getattr(vg_detail.move_learn_method, 'name', None),
                        level_learned_at=getattr(vg_detail, 'level_learned_at', None)
                    )
                    self.__form_move_repository.save(session, form_move)
