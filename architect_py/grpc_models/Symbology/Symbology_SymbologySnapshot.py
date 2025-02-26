# generated by datamodel-codegen:
#   filename:  Symbology_SymbologySnapshot.json

from __future__ import annotations

from enum import Enum
from typing import Annotated, Dict, List, Optional, Union

from msgspec import Meta, Struct

Decimal = str


class DerivativeKind1(Enum):
    Linear = 'Linear'


class DerivativeKind2(Enum):
    Inverse = 'Inverse'


class DerivativeKind3(Enum):
    Quanto = 'Quanto'


DerivativeKind = Union[DerivativeKind1, DerivativeKind2, DerivativeKind3]


class OptionLike(Struct):
    strike: Decimal
    expiration: Optional[str] = None


class EventContractSeriesInstance2(Struct):
    OptionLike: OptionLike


class Unit(Enum):
    base = 'base'


class MinOrderQuantityUnit1(Struct):
    unit: Unit


class Unit1(Enum):
    quote = 'quote'


class MinOrderQuantityUnit2(Struct):
    unit: Unit1


MinOrderQuantityUnit = Union[MinOrderQuantityUnit1, MinOrderQuantityUnit2]


class OptionsExerciseType(Enum):
    american = 'american'
    european = 'european'
    unknown = 'unknown'


class Outcome(Struct):
    name: str


PriceDisplayFormat = str


class ProductType2(Enum):
    Fiat = 'Fiat'


class ProductType1(Struct):
    product_type: ProductType2


class ProductType4(Enum):
    Commodity = 'Commodity'


class ProductType3(Struct):
    product_type: ProductType4


class ProductType6(Enum):
    Crypto = 'Crypto'


class ProductType5(Struct):
    product_type: ProductType6


class ProductType8(Enum):
    Equity = 'Equity'


class ProductType7(Struct):
    product_type: ProductType8


class ProductType10(Enum):
    Index = 'Index'


class ProductType9(Struct):
    product_type: ProductType10


class ProductType12(Enum):
    Future = 'Future'


class ProductType11(Struct):
    derivative_kind: DerivativeKind
    expiration: str
    multiplier: Decimal
    product_type: ProductType12
    first_notice_date: Optional[str] = None
    series: Optional[str] = None
    underlying: Optional[str] = None


class ProductType14(Enum):
    FutureSpread = 'FutureSpread'


class ProductType16(Enum):
    Perpetual = 'Perpetual'


class ProductType15(Struct):
    derivative_kind: DerivativeKind
    multiplier: Decimal
    product_type: ProductType16
    underlying: Optional[str] = None


class ProductType18(Enum):
    Option = 'Option'


class ProductType20(Enum):
    EventContract = 'EventContract'


class ProductType22(Enum):
    Unknown = 'Unknown'


class ProductType21(Struct):
    product_type: ProductType22


class PutOrCall(Enum):
    P = 'P'
    C = 'C'


class SpreadLeg(Struct):
    product: str
    quantity: Annotated[
        Decimal,
        Meta(
            description='Some spreads have different ratios for their legs, like buy 1 A, sell 2 B, buy 1 C; We would represent that with quantities in the legs: 1, -2, 1'
        ),
    ]
    """
    Some spreads have different ratios for their legs, like buy 1 A, sell 2 B, buy 1 C; We would represent that with quantities in the legs: 1, -2, 1
    """


class TickSize1(Struct):
    simple: Decimal


Threshold = List[Decimal]


class Varying(Struct):
    thresholds: List[Threshold]


class TickSize2(Struct):
    varying: Varying


TickSize = Union[TickSize1, TickSize2]


class TimeZone(Enum):
    Africa_Abidjan = 'Africa/Abidjan'
    Africa_Accra = 'Africa/Accra'
    Africa_Addis_Ababa = 'Africa/Addis_Ababa'
    Africa_Algiers = 'Africa/Algiers'
    Africa_Asmara = 'Africa/Asmara'
    Africa_Asmera = 'Africa/Asmera'
    Africa_Bamako = 'Africa/Bamako'
    Africa_Bangui = 'Africa/Bangui'
    Africa_Banjul = 'Africa/Banjul'
    Africa_Bissau = 'Africa/Bissau'
    Africa_Blantyre = 'Africa/Blantyre'
    Africa_Brazzaville = 'Africa/Brazzaville'
    Africa_Bujumbura = 'Africa/Bujumbura'
    Africa_Cairo = 'Africa/Cairo'
    Africa_Casablanca = 'Africa/Casablanca'
    Africa_Ceuta = 'Africa/Ceuta'
    Africa_Conakry = 'Africa/Conakry'
    Africa_Dakar = 'Africa/Dakar'
    Africa_Dar_es_Salaam = 'Africa/Dar_es_Salaam'
    Africa_Djibouti = 'Africa/Djibouti'
    Africa_Douala = 'Africa/Douala'
    Africa_El_Aaiun = 'Africa/El_Aaiun'
    Africa_Freetown = 'Africa/Freetown'
    Africa_Gaborone = 'Africa/Gaborone'
    Africa_Harare = 'Africa/Harare'
    Africa_Johannesburg = 'Africa/Johannesburg'
    Africa_Juba = 'Africa/Juba'
    Africa_Kampala = 'Africa/Kampala'
    Africa_Khartoum = 'Africa/Khartoum'
    Africa_Kigali = 'Africa/Kigali'
    Africa_Kinshasa = 'Africa/Kinshasa'
    Africa_Lagos = 'Africa/Lagos'
    Africa_Libreville = 'Africa/Libreville'
    Africa_Lome = 'Africa/Lome'
    Africa_Luanda = 'Africa/Luanda'
    Africa_Lubumbashi = 'Africa/Lubumbashi'
    Africa_Lusaka = 'Africa/Lusaka'
    Africa_Malabo = 'Africa/Malabo'
    Africa_Maputo = 'Africa/Maputo'
    Africa_Maseru = 'Africa/Maseru'
    Africa_Mbabane = 'Africa/Mbabane'
    Africa_Mogadishu = 'Africa/Mogadishu'
    Africa_Monrovia = 'Africa/Monrovia'
    Africa_Nairobi = 'Africa/Nairobi'
    Africa_Ndjamena = 'Africa/Ndjamena'
    Africa_Niamey = 'Africa/Niamey'
    Africa_Nouakchott = 'Africa/Nouakchott'
    Africa_Ouagadougou = 'Africa/Ouagadougou'
    Africa_Porto_Novo = 'Africa/Porto-Novo'
    Africa_Sao_Tome = 'Africa/Sao_Tome'
    Africa_Timbuktu = 'Africa/Timbuktu'
    Africa_Tripoli = 'Africa/Tripoli'
    Africa_Tunis = 'Africa/Tunis'
    Africa_Windhoek = 'Africa/Windhoek'
    America_Adak = 'America/Adak'
    America_Anchorage = 'America/Anchorage'
    America_Anguilla = 'America/Anguilla'
    America_Antigua = 'America/Antigua'
    America_Araguaina = 'America/Araguaina'
    America_Argentina_Buenos_Aires = 'America/Argentina/Buenos_Aires'
    America_Argentina_Catamarca = 'America/Argentina/Catamarca'
    America_Argentina_ComodRivadavia = 'America/Argentina/ComodRivadavia'
    America_Argentina_Cordoba = 'America/Argentina/Cordoba'
    America_Argentina_Jujuy = 'America/Argentina/Jujuy'
    America_Argentina_La_Rioja = 'America/Argentina/La_Rioja'
    America_Argentina_Mendoza = 'America/Argentina/Mendoza'
    America_Argentina_Rio_Gallegos = 'America/Argentina/Rio_Gallegos'
    America_Argentina_Salta = 'America/Argentina/Salta'
    America_Argentina_San_Juan = 'America/Argentina/San_Juan'
    America_Argentina_San_Luis = 'America/Argentina/San_Luis'
    America_Argentina_Tucuman = 'America/Argentina/Tucuman'
    America_Argentina_Ushuaia = 'America/Argentina/Ushuaia'
    America_Aruba = 'America/Aruba'
    America_Asuncion = 'America/Asuncion'
    America_Atikokan = 'America/Atikokan'
    America_Atka = 'America/Atka'
    America_Bahia = 'America/Bahia'
    America_Bahia_Banderas = 'America/Bahia_Banderas'
    America_Barbados = 'America/Barbados'
    America_Belem = 'America/Belem'
    America_Belize = 'America/Belize'
    America_Blanc_Sablon = 'America/Blanc-Sablon'
    America_Boa_Vista = 'America/Boa_Vista'
    America_Bogota = 'America/Bogota'
    America_Boise = 'America/Boise'
    America_Buenos_Aires = 'America/Buenos_Aires'
    America_Cambridge_Bay = 'America/Cambridge_Bay'
    America_Campo_Grande = 'America/Campo_Grande'
    America_Cancun = 'America/Cancun'
    America_Caracas = 'America/Caracas'
    America_Catamarca = 'America/Catamarca'
    America_Cayenne = 'America/Cayenne'
    America_Cayman = 'America/Cayman'
    America_Chicago = 'America/Chicago'
    America_Chihuahua = 'America/Chihuahua'
    America_Ciudad_Juarez = 'America/Ciudad_Juarez'
    America_Coral_Harbour = 'America/Coral_Harbour'
    America_Cordoba = 'America/Cordoba'
    America_Costa_Rica = 'America/Costa_Rica'
    America_Creston = 'America/Creston'
    America_Cuiaba = 'America/Cuiaba'
    America_Curacao = 'America/Curacao'
    America_Danmarkshavn = 'America/Danmarkshavn'
    America_Dawson = 'America/Dawson'
    America_Dawson_Creek = 'America/Dawson_Creek'
    America_Denver = 'America/Denver'
    America_Detroit = 'America/Detroit'
    America_Dominica = 'America/Dominica'
    America_Edmonton = 'America/Edmonton'
    America_Eirunepe = 'America/Eirunepe'
    America_El_Salvador = 'America/El_Salvador'
    America_Ensenada = 'America/Ensenada'
    America_Fort_Nelson = 'America/Fort_Nelson'
    America_Fort_Wayne = 'America/Fort_Wayne'
    America_Fortaleza = 'America/Fortaleza'
    America_Glace_Bay = 'America/Glace_Bay'
    America_Godthab = 'America/Godthab'
    America_Goose_Bay = 'America/Goose_Bay'
    America_Grand_Turk = 'America/Grand_Turk'
    America_Grenada = 'America/Grenada'
    America_Guadeloupe = 'America/Guadeloupe'
    America_Guatemala = 'America/Guatemala'
    America_Guayaquil = 'America/Guayaquil'
    America_Guyana = 'America/Guyana'
    America_Halifax = 'America/Halifax'
    America_Havana = 'America/Havana'
    America_Hermosillo = 'America/Hermosillo'
    America_Indiana_Indianapolis = 'America/Indiana/Indianapolis'
    America_Indiana_Knox = 'America/Indiana/Knox'
    America_Indiana_Marengo = 'America/Indiana/Marengo'
    America_Indiana_Petersburg = 'America/Indiana/Petersburg'
    America_Indiana_Tell_City = 'America/Indiana/Tell_City'
    America_Indiana_Vevay = 'America/Indiana/Vevay'
    America_Indiana_Vincennes = 'America/Indiana/Vincennes'
    America_Indiana_Winamac = 'America/Indiana/Winamac'
    America_Indianapolis = 'America/Indianapolis'
    America_Inuvik = 'America/Inuvik'
    America_Iqaluit = 'America/Iqaluit'
    America_Jamaica = 'America/Jamaica'
    America_Jujuy = 'America/Jujuy'
    America_Juneau = 'America/Juneau'
    America_Kentucky_Louisville = 'America/Kentucky/Louisville'
    America_Kentucky_Monticello = 'America/Kentucky/Monticello'
    America_Knox_IN = 'America/Knox_IN'
    America_Kralendijk = 'America/Kralendijk'
    America_La_Paz = 'America/La_Paz'
    America_Lima = 'America/Lima'
    America_Los_Angeles = 'America/Los_Angeles'
    America_Louisville = 'America/Louisville'
    America_Lower_Princes = 'America/Lower_Princes'
    America_Maceio = 'America/Maceio'
    America_Managua = 'America/Managua'
    America_Manaus = 'America/Manaus'
    America_Marigot = 'America/Marigot'
    America_Martinique = 'America/Martinique'
    America_Matamoros = 'America/Matamoros'
    America_Mazatlan = 'America/Mazatlan'
    America_Mendoza = 'America/Mendoza'
    America_Menominee = 'America/Menominee'
    America_Merida = 'America/Merida'
    America_Metlakatla = 'America/Metlakatla'
    America_Mexico_City = 'America/Mexico_City'
    America_Miquelon = 'America/Miquelon'
    America_Moncton = 'America/Moncton'
    America_Monterrey = 'America/Monterrey'
    America_Montevideo = 'America/Montevideo'
    America_Montreal = 'America/Montreal'
    America_Montserrat = 'America/Montserrat'
    America_Nassau = 'America/Nassau'
    America_New_York = 'America/New_York'
    America_Nipigon = 'America/Nipigon'
    America_Nome = 'America/Nome'
    America_Noronha = 'America/Noronha'
    America_North_Dakota_Beulah = 'America/North_Dakota/Beulah'
    America_North_Dakota_Center = 'America/North_Dakota/Center'
    America_North_Dakota_New_Salem = 'America/North_Dakota/New_Salem'
    America_Nuuk = 'America/Nuuk'
    America_Ojinaga = 'America/Ojinaga'
    America_Panama = 'America/Panama'
    America_Pangnirtung = 'America/Pangnirtung'
    America_Paramaribo = 'America/Paramaribo'
    America_Phoenix = 'America/Phoenix'
    America_Port_au_Prince = 'America/Port-au-Prince'
    America_Port_of_Spain = 'America/Port_of_Spain'
    America_Porto_Acre = 'America/Porto_Acre'
    America_Porto_Velho = 'America/Porto_Velho'
    America_Puerto_Rico = 'America/Puerto_Rico'
    America_Punta_Arenas = 'America/Punta_Arenas'
    America_Rainy_River = 'America/Rainy_River'
    America_Rankin_Inlet = 'America/Rankin_Inlet'
    America_Recife = 'America/Recife'
    America_Regina = 'America/Regina'
    America_Resolute = 'America/Resolute'
    America_Rio_Branco = 'America/Rio_Branco'
    America_Rosario = 'America/Rosario'
    America_Santa_Isabel = 'America/Santa_Isabel'
    America_Santarem = 'America/Santarem'
    America_Santiago = 'America/Santiago'
    America_Santo_Domingo = 'America/Santo_Domingo'
    America_Sao_Paulo = 'America/Sao_Paulo'
    America_Scoresbysund = 'America/Scoresbysund'
    America_Shiprock = 'America/Shiprock'
    America_Sitka = 'America/Sitka'
    America_St_Barthelemy = 'America/St_Barthelemy'
    America_St_Johns = 'America/St_Johns'
    America_St_Kitts = 'America/St_Kitts'
    America_St_Lucia = 'America/St_Lucia'
    America_St_Thomas = 'America/St_Thomas'
    America_St_Vincent = 'America/St_Vincent'
    America_Swift_Current = 'America/Swift_Current'
    America_Tegucigalpa = 'America/Tegucigalpa'
    America_Thule = 'America/Thule'
    America_Thunder_Bay = 'America/Thunder_Bay'
    America_Tijuana = 'America/Tijuana'
    America_Toronto = 'America/Toronto'
    America_Tortola = 'America/Tortola'
    America_Vancouver = 'America/Vancouver'
    America_Virgin = 'America/Virgin'
    America_Whitehorse = 'America/Whitehorse'
    America_Winnipeg = 'America/Winnipeg'
    America_Yakutat = 'America/Yakutat'
    America_Yellowknife = 'America/Yellowknife'
    Antarctica_Casey = 'Antarctica/Casey'
    Antarctica_Davis = 'Antarctica/Davis'
    Antarctica_DumontDUrville = 'Antarctica/DumontDUrville'
    Antarctica_Macquarie = 'Antarctica/Macquarie'
    Antarctica_Mawson = 'Antarctica/Mawson'
    Antarctica_McMurdo = 'Antarctica/McMurdo'
    Antarctica_Palmer = 'Antarctica/Palmer'
    Antarctica_Rothera = 'Antarctica/Rothera'
    Antarctica_South_Pole = 'Antarctica/South_Pole'
    Antarctica_Syowa = 'Antarctica/Syowa'
    Antarctica_Troll = 'Antarctica/Troll'
    Antarctica_Vostok = 'Antarctica/Vostok'
    Arctic_Longyearbyen = 'Arctic/Longyearbyen'
    Asia_Aden = 'Asia/Aden'
    Asia_Almaty = 'Asia/Almaty'
    Asia_Amman = 'Asia/Amman'
    Asia_Anadyr = 'Asia/Anadyr'
    Asia_Aqtau = 'Asia/Aqtau'
    Asia_Aqtobe = 'Asia/Aqtobe'
    Asia_Ashgabat = 'Asia/Ashgabat'
    Asia_Ashkhabad = 'Asia/Ashkhabad'
    Asia_Atyrau = 'Asia/Atyrau'
    Asia_Baghdad = 'Asia/Baghdad'
    Asia_Bahrain = 'Asia/Bahrain'
    Asia_Baku = 'Asia/Baku'
    Asia_Bangkok = 'Asia/Bangkok'
    Asia_Barnaul = 'Asia/Barnaul'
    Asia_Beirut = 'Asia/Beirut'
    Asia_Bishkek = 'Asia/Bishkek'
    Asia_Brunei = 'Asia/Brunei'
    Asia_Calcutta = 'Asia/Calcutta'
    Asia_Chita = 'Asia/Chita'
    Asia_Choibalsan = 'Asia/Choibalsan'
    Asia_Chongqing = 'Asia/Chongqing'
    Asia_Chungking = 'Asia/Chungking'
    Asia_Colombo = 'Asia/Colombo'
    Asia_Dacca = 'Asia/Dacca'
    Asia_Damascus = 'Asia/Damascus'
    Asia_Dhaka = 'Asia/Dhaka'
    Asia_Dili = 'Asia/Dili'
    Asia_Dubai = 'Asia/Dubai'
    Asia_Dushanbe = 'Asia/Dushanbe'
    Asia_Famagusta = 'Asia/Famagusta'
    Asia_Gaza = 'Asia/Gaza'
    Asia_Harbin = 'Asia/Harbin'
    Asia_Hebron = 'Asia/Hebron'
    Asia_Ho_Chi_Minh = 'Asia/Ho_Chi_Minh'
    Asia_Hong_Kong = 'Asia/Hong_Kong'
    Asia_Hovd = 'Asia/Hovd'
    Asia_Irkutsk = 'Asia/Irkutsk'
    Asia_Istanbul = 'Asia/Istanbul'
    Asia_Jakarta = 'Asia/Jakarta'
    Asia_Jayapura = 'Asia/Jayapura'
    Asia_Jerusalem = 'Asia/Jerusalem'
    Asia_Kabul = 'Asia/Kabul'
    Asia_Kamchatka = 'Asia/Kamchatka'
    Asia_Karachi = 'Asia/Karachi'
    Asia_Kashgar = 'Asia/Kashgar'
    Asia_Kathmandu = 'Asia/Kathmandu'
    Asia_Katmandu = 'Asia/Katmandu'
    Asia_Khandyga = 'Asia/Khandyga'
    Asia_Kolkata = 'Asia/Kolkata'
    Asia_Krasnoyarsk = 'Asia/Krasnoyarsk'
    Asia_Kuala_Lumpur = 'Asia/Kuala_Lumpur'
    Asia_Kuching = 'Asia/Kuching'
    Asia_Kuwait = 'Asia/Kuwait'
    Asia_Macao = 'Asia/Macao'
    Asia_Macau = 'Asia/Macau'
    Asia_Magadan = 'Asia/Magadan'
    Asia_Makassar = 'Asia/Makassar'
    Asia_Manila = 'Asia/Manila'
    Asia_Muscat = 'Asia/Muscat'
    Asia_Nicosia = 'Asia/Nicosia'
    Asia_Novokuznetsk = 'Asia/Novokuznetsk'
    Asia_Novosibirsk = 'Asia/Novosibirsk'
    Asia_Omsk = 'Asia/Omsk'
    Asia_Oral = 'Asia/Oral'
    Asia_Phnom_Penh = 'Asia/Phnom_Penh'
    Asia_Pontianak = 'Asia/Pontianak'
    Asia_Pyongyang = 'Asia/Pyongyang'
    Asia_Qatar = 'Asia/Qatar'
    Asia_Qostanay = 'Asia/Qostanay'
    Asia_Qyzylorda = 'Asia/Qyzylorda'
    Asia_Rangoon = 'Asia/Rangoon'
    Asia_Riyadh = 'Asia/Riyadh'
    Asia_Saigon = 'Asia/Saigon'
    Asia_Sakhalin = 'Asia/Sakhalin'
    Asia_Samarkand = 'Asia/Samarkand'
    Asia_Seoul = 'Asia/Seoul'
    Asia_Shanghai = 'Asia/Shanghai'
    Asia_Singapore = 'Asia/Singapore'
    Asia_Srednekolymsk = 'Asia/Srednekolymsk'
    Asia_Taipei = 'Asia/Taipei'
    Asia_Tashkent = 'Asia/Tashkent'
    Asia_Tbilisi = 'Asia/Tbilisi'
    Asia_Tehran = 'Asia/Tehran'
    Asia_Tel_Aviv = 'Asia/Tel_Aviv'
    Asia_Thimbu = 'Asia/Thimbu'
    Asia_Thimphu = 'Asia/Thimphu'
    Asia_Tokyo = 'Asia/Tokyo'
    Asia_Tomsk = 'Asia/Tomsk'
    Asia_Ujung_Pandang = 'Asia/Ujung_Pandang'
    Asia_Ulaanbaatar = 'Asia/Ulaanbaatar'
    Asia_Ulan_Bator = 'Asia/Ulan_Bator'
    Asia_Urumqi = 'Asia/Urumqi'
    Asia_Ust_Nera = 'Asia/Ust-Nera'
    Asia_Vientiane = 'Asia/Vientiane'
    Asia_Vladivostok = 'Asia/Vladivostok'
    Asia_Yakutsk = 'Asia/Yakutsk'
    Asia_Yangon = 'Asia/Yangon'
    Asia_Yekaterinburg = 'Asia/Yekaterinburg'
    Asia_Yerevan = 'Asia/Yerevan'
    Atlantic_Azores = 'Atlantic/Azores'
    Atlantic_Bermuda = 'Atlantic/Bermuda'
    Atlantic_Canary = 'Atlantic/Canary'
    Atlantic_Cape_Verde = 'Atlantic/Cape_Verde'
    Atlantic_Faeroe = 'Atlantic/Faeroe'
    Atlantic_Faroe = 'Atlantic/Faroe'
    Atlantic_Jan_Mayen = 'Atlantic/Jan_Mayen'
    Atlantic_Madeira = 'Atlantic/Madeira'
    Atlantic_Reykjavik = 'Atlantic/Reykjavik'
    Atlantic_South_Georgia = 'Atlantic/South_Georgia'
    Atlantic_St_Helena = 'Atlantic/St_Helena'
    Atlantic_Stanley = 'Atlantic/Stanley'
    Australia_ACT = 'Australia/ACT'
    Australia_Adelaide = 'Australia/Adelaide'
    Australia_Brisbane = 'Australia/Brisbane'
    Australia_Broken_Hill = 'Australia/Broken_Hill'
    Australia_Canberra = 'Australia/Canberra'
    Australia_Currie = 'Australia/Currie'
    Australia_Darwin = 'Australia/Darwin'
    Australia_Eucla = 'Australia/Eucla'
    Australia_Hobart = 'Australia/Hobart'
    Australia_LHI = 'Australia/LHI'
    Australia_Lindeman = 'Australia/Lindeman'
    Australia_Lord_Howe = 'Australia/Lord_Howe'
    Australia_Melbourne = 'Australia/Melbourne'
    Australia_NSW = 'Australia/NSW'
    Australia_North = 'Australia/North'
    Australia_Perth = 'Australia/Perth'
    Australia_Queensland = 'Australia/Queensland'
    Australia_South = 'Australia/South'
    Australia_Sydney = 'Australia/Sydney'
    Australia_Tasmania = 'Australia/Tasmania'
    Australia_Victoria = 'Australia/Victoria'
    Australia_West = 'Australia/West'
    Australia_Yancowinna = 'Australia/Yancowinna'
    Brazil_Acre = 'Brazil/Acre'
    Brazil_DeNoronha = 'Brazil/DeNoronha'
    Brazil_East = 'Brazil/East'
    Brazil_West = 'Brazil/West'
    CET = 'CET'
    CST6CDT = 'CST6CDT'
    Canada_Atlantic = 'Canada/Atlantic'
    Canada_Central = 'Canada/Central'
    Canada_Eastern = 'Canada/Eastern'
    Canada_Mountain = 'Canada/Mountain'
    Canada_Newfoundland = 'Canada/Newfoundland'
    Canada_Pacific = 'Canada/Pacific'
    Canada_Saskatchewan = 'Canada/Saskatchewan'
    Canada_Yukon = 'Canada/Yukon'
    Chile_Continental = 'Chile/Continental'
    Chile_EasterIsland = 'Chile/EasterIsland'
    Cuba = 'Cuba'
    EET = 'EET'
    EST = 'EST'
    EST5EDT = 'EST5EDT'
    Egypt = 'Egypt'
    Eire = 'Eire'
    Etc_GMT = 'Etc/GMT'
    Etc_GMT_0 = 'Etc/GMT+0'
    Etc_GMT_1 = 'Etc/GMT+1'
    Etc_GMT_10 = 'Etc/GMT+10'
    Etc_GMT_11 = 'Etc/GMT+11'
    Etc_GMT_12 = 'Etc/GMT+12'
    Etc_GMT_2 = 'Etc/GMT+2'
    Etc_GMT_3 = 'Etc/GMT+3'
    Etc_GMT_4 = 'Etc/GMT+4'
    Etc_GMT_5 = 'Etc/GMT+5'
    Etc_GMT_6 = 'Etc/GMT+6'
    Etc_GMT_7 = 'Etc/GMT+7'
    Etc_GMT_8 = 'Etc/GMT+8'
    Etc_GMT_9 = 'Etc/GMT+9'
    Etc_GMT_0_1 = 'Etc/GMT-0'
    Etc_GMT_1_1 = 'Etc/GMT-1'
    Etc_GMT_10_1 = 'Etc/GMT-10'
    Etc_GMT_11_1 = 'Etc/GMT-11'
    Etc_GMT_12_1 = 'Etc/GMT-12'
    Etc_GMT_13 = 'Etc/GMT-13'
    Etc_GMT_14 = 'Etc/GMT-14'
    Etc_GMT_2_1 = 'Etc/GMT-2'
    Etc_GMT_3_1 = 'Etc/GMT-3'
    Etc_GMT_4_1 = 'Etc/GMT-4'
    Etc_GMT_5_1 = 'Etc/GMT-5'
    Etc_GMT_6_1 = 'Etc/GMT-6'
    Etc_GMT_7_1 = 'Etc/GMT-7'
    Etc_GMT_8_1 = 'Etc/GMT-8'
    Etc_GMT_9_1 = 'Etc/GMT-9'
    Etc_GMT0 = 'Etc/GMT0'
    Etc_Greenwich = 'Etc/Greenwich'
    Etc_UCT = 'Etc/UCT'
    Etc_UTC = 'Etc/UTC'
    Etc_Universal = 'Etc/Universal'
    Etc_Zulu = 'Etc/Zulu'
    Europe_Amsterdam = 'Europe/Amsterdam'
    Europe_Andorra = 'Europe/Andorra'
    Europe_Astrakhan = 'Europe/Astrakhan'
    Europe_Athens = 'Europe/Athens'
    Europe_Belfast = 'Europe/Belfast'
    Europe_Belgrade = 'Europe/Belgrade'
    Europe_Berlin = 'Europe/Berlin'
    Europe_Bratislava = 'Europe/Bratislava'
    Europe_Brussels = 'Europe/Brussels'
    Europe_Bucharest = 'Europe/Bucharest'
    Europe_Budapest = 'Europe/Budapest'
    Europe_Busingen = 'Europe/Busingen'
    Europe_Chisinau = 'Europe/Chisinau'
    Europe_Copenhagen = 'Europe/Copenhagen'
    Europe_Dublin = 'Europe/Dublin'
    Europe_Gibraltar = 'Europe/Gibraltar'
    Europe_Guernsey = 'Europe/Guernsey'
    Europe_Helsinki = 'Europe/Helsinki'
    Europe_Isle_of_Man = 'Europe/Isle_of_Man'
    Europe_Istanbul = 'Europe/Istanbul'
    Europe_Jersey = 'Europe/Jersey'
    Europe_Kaliningrad = 'Europe/Kaliningrad'
    Europe_Kiev = 'Europe/Kiev'
    Europe_Kirov = 'Europe/Kirov'
    Europe_Kyiv = 'Europe/Kyiv'
    Europe_Lisbon = 'Europe/Lisbon'
    Europe_Ljubljana = 'Europe/Ljubljana'
    Europe_London = 'Europe/London'
    Europe_Luxembourg = 'Europe/Luxembourg'
    Europe_Madrid = 'Europe/Madrid'
    Europe_Malta = 'Europe/Malta'
    Europe_Mariehamn = 'Europe/Mariehamn'
    Europe_Minsk = 'Europe/Minsk'
    Europe_Monaco = 'Europe/Monaco'
    Europe_Moscow = 'Europe/Moscow'
    Europe_Nicosia = 'Europe/Nicosia'
    Europe_Oslo = 'Europe/Oslo'
    Europe_Paris = 'Europe/Paris'
    Europe_Podgorica = 'Europe/Podgorica'
    Europe_Prague = 'Europe/Prague'
    Europe_Riga = 'Europe/Riga'
    Europe_Rome = 'Europe/Rome'
    Europe_Samara = 'Europe/Samara'
    Europe_San_Marino = 'Europe/San_Marino'
    Europe_Sarajevo = 'Europe/Sarajevo'
    Europe_Saratov = 'Europe/Saratov'
    Europe_Simferopol = 'Europe/Simferopol'
    Europe_Skopje = 'Europe/Skopje'
    Europe_Sofia = 'Europe/Sofia'
    Europe_Stockholm = 'Europe/Stockholm'
    Europe_Tallinn = 'Europe/Tallinn'
    Europe_Tirane = 'Europe/Tirane'
    Europe_Tiraspol = 'Europe/Tiraspol'
    Europe_Ulyanovsk = 'Europe/Ulyanovsk'
    Europe_Uzhgorod = 'Europe/Uzhgorod'
    Europe_Vaduz = 'Europe/Vaduz'
    Europe_Vatican = 'Europe/Vatican'
    Europe_Vienna = 'Europe/Vienna'
    Europe_Vilnius = 'Europe/Vilnius'
    Europe_Volgograd = 'Europe/Volgograd'
    Europe_Warsaw = 'Europe/Warsaw'
    Europe_Zagreb = 'Europe/Zagreb'
    Europe_Zaporozhye = 'Europe/Zaporozhye'
    Europe_Zurich = 'Europe/Zurich'
    GB = 'GB'
    GB_Eire = 'GB-Eire'
    GMT = 'GMT'
    GMT_0 = 'GMT+0'
    GMT_0_1 = 'GMT-0'
    GMT0 = 'GMT0'
    Greenwich = 'Greenwich'
    HST = 'HST'
    Hongkong = 'Hongkong'
    Iceland = 'Iceland'
    Indian_Antananarivo = 'Indian/Antananarivo'
    Indian_Chagos = 'Indian/Chagos'
    Indian_Christmas = 'Indian/Christmas'
    Indian_Cocos = 'Indian/Cocos'
    Indian_Comoro = 'Indian/Comoro'
    Indian_Kerguelen = 'Indian/Kerguelen'
    Indian_Mahe = 'Indian/Mahe'
    Indian_Maldives = 'Indian/Maldives'
    Indian_Mauritius = 'Indian/Mauritius'
    Indian_Mayotte = 'Indian/Mayotte'
    Indian_Reunion = 'Indian/Reunion'
    Iran = 'Iran'
    Israel = 'Israel'
    Jamaica = 'Jamaica'
    Japan = 'Japan'
    Kwajalein = 'Kwajalein'
    Libya = 'Libya'
    MET = 'MET'
    MST = 'MST'
    MST7MDT = 'MST7MDT'
    Mexico_BajaNorte = 'Mexico/BajaNorte'
    Mexico_BajaSur = 'Mexico/BajaSur'
    Mexico_General = 'Mexico/General'
    NZ = 'NZ'
    NZ_CHAT = 'NZ-CHAT'
    Navajo = 'Navajo'
    PRC = 'PRC'
    PST8PDT = 'PST8PDT'
    Pacific_Apia = 'Pacific/Apia'
    Pacific_Auckland = 'Pacific/Auckland'
    Pacific_Bougainville = 'Pacific/Bougainville'
    Pacific_Chatham = 'Pacific/Chatham'
    Pacific_Chuuk = 'Pacific/Chuuk'
    Pacific_Easter = 'Pacific/Easter'
    Pacific_Efate = 'Pacific/Efate'
    Pacific_Enderbury = 'Pacific/Enderbury'
    Pacific_Fakaofo = 'Pacific/Fakaofo'
    Pacific_Fiji = 'Pacific/Fiji'
    Pacific_Funafuti = 'Pacific/Funafuti'
    Pacific_Galapagos = 'Pacific/Galapagos'
    Pacific_Gambier = 'Pacific/Gambier'
    Pacific_Guadalcanal = 'Pacific/Guadalcanal'
    Pacific_Guam = 'Pacific/Guam'
    Pacific_Honolulu = 'Pacific/Honolulu'
    Pacific_Johnston = 'Pacific/Johnston'
    Pacific_Kanton = 'Pacific/Kanton'
    Pacific_Kiritimati = 'Pacific/Kiritimati'
    Pacific_Kosrae = 'Pacific/Kosrae'
    Pacific_Kwajalein = 'Pacific/Kwajalein'
    Pacific_Majuro = 'Pacific/Majuro'
    Pacific_Marquesas = 'Pacific/Marquesas'
    Pacific_Midway = 'Pacific/Midway'
    Pacific_Nauru = 'Pacific/Nauru'
    Pacific_Niue = 'Pacific/Niue'
    Pacific_Norfolk = 'Pacific/Norfolk'
    Pacific_Noumea = 'Pacific/Noumea'
    Pacific_Pago_Pago = 'Pacific/Pago_Pago'
    Pacific_Palau = 'Pacific/Palau'
    Pacific_Pitcairn = 'Pacific/Pitcairn'
    Pacific_Pohnpei = 'Pacific/Pohnpei'
    Pacific_Ponape = 'Pacific/Ponape'
    Pacific_Port_Moresby = 'Pacific/Port_Moresby'
    Pacific_Rarotonga = 'Pacific/Rarotonga'
    Pacific_Saipan = 'Pacific/Saipan'
    Pacific_Samoa = 'Pacific/Samoa'
    Pacific_Tahiti = 'Pacific/Tahiti'
    Pacific_Tarawa = 'Pacific/Tarawa'
    Pacific_Tongatapu = 'Pacific/Tongatapu'
    Pacific_Truk = 'Pacific/Truk'
    Pacific_Wake = 'Pacific/Wake'
    Pacific_Wallis = 'Pacific/Wallis'
    Pacific_Yap = 'Pacific/Yap'
    Poland = 'Poland'
    Portugal = 'Portugal'
    ROC = 'ROC'
    ROK = 'ROK'
    Singapore = 'Singapore'
    Turkey = 'Turkey'
    UCT = 'UCT'
    US_Alaska = 'US/Alaska'
    US_Aleutian = 'US/Aleutian'
    US_Arizona = 'US/Arizona'
    US_Central = 'US/Central'
    US_East_Indiana = 'US/East-Indiana'
    US_Eastern = 'US/Eastern'
    US_Hawaii = 'US/Hawaii'
    US_Indiana_Starke = 'US/Indiana-Starke'
    US_Michigan = 'US/Michigan'
    US_Mountain = 'US/Mountain'
    US_Pacific = 'US/Pacific'
    US_Samoa = 'US/Samoa'
    UTC = 'UTC'
    Universal = 'Universal'
    W_SU = 'W-SU'
    WET = 'WET'
    Zulu = 'Zulu'


class Enumerated(Struct):
    outcome: Outcome


class EventContractSeriesInstance1(Struct):
    Enumerated: Enumerated


EventContractSeriesInstance = Union[
    EventContractSeriesInstance1, EventContractSeriesInstance2
]


class ExecutionInfo(Struct):
    execution_venue: str
    is_delisted: bool
    min_order_quantity: Decimal
    min_order_quantity_unit: MinOrderQuantityUnit
    step_size: Decimal
    tick_size: TickSize
    initial_margin: Optional[Decimal] = None
    maintenance_margin: Optional[Decimal] = None


class OptionsSeriesInfo(Struct):
    derivative_kind: DerivativeKind
    exercise_type: OptionsExerciseType
    expiration_time_of_day: str
    expiration_time_zone: TimeZone
    is_cash_settled: bool
    multiplier: Decimal
    options_series: str
    quote_symbol: str
    strikes_by_expiration: Dict[str, List[Decimal]]
    underlying: str
    venue_discriminant: Optional[str] = None


class OptionsSeriesInstance(Struct):
    expiration: str
    put_or_call: PutOrCall
    strike: Decimal


class ProductType13(Struct):
    legs: List[SpreadLeg]
    product_type: ProductType14


class ProductType17(Struct):
    instance: OptionsSeriesInstance
    product_type: ProductType18
    series: str


class ProductType19(Struct):
    instance: EventContractSeriesInstance
    product_type: ProductType20
    series: str


ProductType = Union[
    ProductType1,
    ProductType3,
    ProductType5,
    ProductType7,
    ProductType9,
    ProductType11,
    ProductType13,
    ProductType15,
    ProductType17,
    ProductType19,
    ProductType21,
]


class ProductInfo(Struct):
    product_type: ProductType
    price_display_format: Optional[PriceDisplayFormat] = None
    primary_venue: Optional[str] = None


class SymbologySnapshot(Struct):
    execution_info: Dict[str, Dict[str, ExecutionInfo]]
    options_series: Dict[str, OptionsSeriesInfo]
    products: Dict[str, ProductInfo]
    sid: Annotated[int, Meta(ge=0, title='sequence_id')]
    sn: Annotated[int, Meta(ge=0, title='sequence_number')]
    product_aliases: Optional[Dict[str, Dict[str, str]]] = {}
