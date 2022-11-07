__version__ = '0.1.1'

from emoji_list_discord.Smileys_and_people import *
from emoji_list_discord.Animals_and_nature import *
from emoji_list_discord.Food_and_drink import *
from emoji_list_discord.Travel_and_places import *
from emoji_list_discord.Activities import *
from emoji_list_discord.Objects import *
from emoji_list_discord.Symbols import *

# All emoji

all_Smileys_and_people = list(set(face_positive+face_neutral+face_negative+face_sick+face_role+face_fantasy+face_cat+face_monkey+person+person_role+person_fantasy+person_gesture+person_activity+person_sport+family+body+emotion+clothing))
all_Animals_and_nature = list(set(animals_mammal+animal_bird+animal_amphibian+animal_reptile+animal_marine+animal_bug+plant_flower+plant_other))
all_Food_and_drink = list(set(food_fruit+food_vegetable+food_prepared+food_asian+food_sweet+drink+dishware))
all_Travel_and_places = list(set(place_map+place_geographic+place_building+place_religious+place_other+transport_ground+transport_water+transport_air+hotel))
all_Activities = list(set(event+award_medal+sport+game))
all_Objects = list(set(sound+music+musical_instrument+phone+computer+light_video+book_paper+money+mail+writing+office+lock+tool+medical+other_object))
all_Symbols = list(set(transport_sign+warning+arrow+religion+av_symbol+other_symbol+keycap+alphanum+geometric+flag+country_flag+subdivision_flag))
all_emoji = list(set(face_positive+face_neutral+face_negative+face_sick+face_role+face_fantasy+face_cat+face_monkey+person+person_role+person_fantasy+person_gesture+person_activity+person_sport+family+body+emotion+clothing+animals_mammal+animal_bird+animal_amphibian+animal_reptile+animal_marine+animal_bug+plant_flower+plant_other+food_fruit+food_vegetable+food_prepared+food_asian+food_sweet+drink+dishware+place_map+place_geographic+place_building+place_religious+place_other+transport_ground+transport_water+transport_air+hotel+time+weather+event+award_medal+sport+game+sound+music+musical_instrument+phone+computer+light_video+book_paper+money+mail+writing+office+lock+tool+medical+other_object+transport_sign+warning+arrow+religion+av_symbol+other_symbol+keycap+alphanum+geometric+flag+country_flag+subdivision_flag))
