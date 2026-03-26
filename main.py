from datetime import datetime
import os, json
from dotenv import load_dotenv
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

from src.repository.ability_repository import AbilityRepository
from src.repository.base_status_repository import BaseStatusRepository
from src.repository.egg_group_repository import EggGroupRepository
from src.repository.evolution_repository import EvolutionRepository
from src.repository.form_ability_repository import FormAbilityRepository
from src.repository.form_move_repository import FormMoveRepository
from src.repository.gender_repository import GenderRepository
from src.repository.generation_repository import GenerationRepository
from src.repository.item_flavor_text_repository import ItemFlavorTextRepository
from src.repository.item_machine_repository import ItemMachineRepository
from src.repository.item_repository import ItemRepository
from src.repository.move_repository import MoveRepository
from src.repository.pokemon_egg_group_repository import PokemonEggGroupRepository
from src.repository.pokemon_form_repository import PokemonFormRepository
from src.repository.pokemon_gender_ratio_repository import PokemonGenderRatioRepository
from src.repository.pokemon_specie_repository import PokemonSpecieRepository
from src.repository.pokemon_sprite_repository import PokemonSpriteRepository
from src.repository.regional_pokedex_number_repository import RegionalPokedexNumberRepository
from src.repository.type_effectiveness_repository import TypeEffectivenessRepository
from src.repository.type_repository import TypeRepository
from src.repository.version_group_repository import VersionGroupRepository
from src.services.ability_populate_service import AbilityPopulationService
from src.services.egg_group_population_service import EggGroupPopulationService
from src.services.evolution_population_service import EvolutionPopulationService
from src.services.gender_populate_service import GenderPopulationService
from src.services.item_flavor_text_population_service import ItemFlavorTextPopulationService
from src.services.item_machine_populate_service import ItemMachinePopulationService
from src.services.item_population_service import ItemPopulationService
from src.services.move_population_service import MovePopulationService
from src.services.pokemon_populator_service import PokemonPopulatorService
from src.services.generation_population_service import GenerationPopulationService
from src.services.type_effectiveness_service import TypeEffectivenessService
from src.services.type_population_service import TypePopulationService
from src.services.version_group_population_service import VersionGroupPopulationService

load_dotenv()

database_url = os.getenv("DATABASE_URL")
POKEMON_AMOUNT = int(os.getenv("POKEMON_AMOUNT"))
GENERATIONS_AMOUNT = int(os.getenv("GENERATIONS_AMOUNT"))
GENERATIONS = json.loads(os.getenv("GENERATIONS"))
EGG_GROUP_AMOUNT = int(os.getenv("EGG_GROUP_AMOUNT"))
POKEMON_TYPES_WHITELIST = os.getenv("POKEMON_TYPES_WHITELIST").split(",")
TYPES_INTRO_MAP = json.loads(os.getenv("TYPES_INTRO_MAP"))

engine = create_engine(database_url)
session_local = sessionmaker(bind=engine)

gender_repository = GenderRepository(session_local)
egg_group_repository = EggGroupRepository(session_local)
type_repository = TypeRepository(session_local)
type_effectiveness_repository = TypeEffectivenessRepository(session_local)
ability_repository = AbilityRepository(session_local)
move_repository = MoveRepository(session_local)
generation_repository = GenerationRepository(session_local)
version_group_repository = VersionGroupRepository(session_local)
pokemon_specie_repository = PokemonSpecieRepository(session_local)
regional_pokedex_number_repository = RegionalPokedexNumberRepository(session_local)
pokemon_gender_ration_repository = PokemonGenderRatioRepository(session_local)
pokemon_egg_group_repository = PokemonEggGroupRepository(session_local)
pokemon_form_repository = PokemonFormRepository(session_local)
pokemon_sprite_repository = PokemonSpriteRepository(session_local)
base_status_repository = BaseStatusRepository(session_local)
form_ability_repository = FormAbilityRepository(session_local)
form_move_repository = FormMoveRepository(session_local)
item_repository = ItemRepository(session_local)
item_flavor_text_repository = ItemFlavorTextRepository(session_local)
item_machine_repository = ItemMachineRepository(session_local)
evolution_repository = EvolutionRepository(session_local)


gender_population_service = GenderPopulationService(gender_repository)
egg_group_population_service = EggGroupPopulationService(egg_group_repository, EGG_GROUP_AMOUNT)
type_population_service = TypePopulationService(type_repository, POKEMON_TYPES_WHITELIST)
type_effectiveness_service = TypeEffectivenessService(
    type_effectiveness_repository, 
    type_repository, 
    generation_repository,
    POKEMON_TYPES_WHITELIST,
    TYPES_INTRO_MAP
)
ability_population_service = AbilityPopulationService(ability_repository)
move_population_service = MovePopulationService(move_repository, type_repository)
generation_population_service = GenerationPopulationService(generation_repository, GENERATIONS, GENERATIONS_AMOUNT)
version_group_population_service = VersionGroupPopulationService(version_group_repository, generation_repository)
pokemon_populator_service = PokemonPopulatorService(
    POKEMON_AMOUNT,
    pokemon_specie_repository,
    regional_pokedex_number_repository,
    gender_repository,
    pokemon_gender_ration_repository,
    egg_group_repository,
    pokemon_egg_group_repository,
    generation_repository,
    pokemon_form_repository,
    pokemon_sprite_repository,
    base_status_repository,
    type_repository,
    ability_repository,
    form_ability_repository,
    move_repository,
    form_move_repository
)
item_population_service = ItemPopulationService(item_repository)
item_flavor_text_population_service = ItemFlavorTextPopulationService(
    item_flavor_text_repository,
    version_group_repository,
    item_repository
)
item_machine_population_service = ItemMachinePopulationService(
    item_machine_repository,
    item_repository,
    move_repository,
    version_group_repository
)
evolution_population_service = EvolutionPopulationService(
    POKEMON_AMOUNT,
    evolution_repository,
    generation_repository,
    item_repository,
    pokemon_form_repository,
    pokemon_specie_repository
)
start_in = datetime.now()
print(f"Populando a base... (#{start_in})")
gender_population_service.populate()
egg_group_population_service.populate()
generation_population_service.populate()
type_population_service.populate()
type_effectiveness_service.populate()
ability_population_service.populate()
move_population_service.populate()
version_group_population_service.populate()
pokemon_populator_service.populate()
item_population_service.populate()
item_flavor_text_population_service.populate()
item_machine_population_service.populate()
evolution_population_service.populate()
end_in = datetime.now()
print(f"Base populada com sucesso! (#{end_in})")
print(f"Tempo total: {end_in - start_in}")