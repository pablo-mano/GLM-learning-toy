import uuid
import asyncio
from datetime import datetime
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import async_session, Base, engine
from app.models import User, Child, Domain, Word, WordTranslation, WordPrerequisite


# Sample domains data
DOMAINS_DATA = [
    {
        "name": "Animals",
        "description": "Learn animal names from pets to wildlife",
        "icon": "",
        "color": "#4CAF50",
        "words": [
            # BEGINNER
            {
                "id": uuid.uuid5(uuid.NAMESPACE_DNS, "word-dog"),
                "difficulty": "beginner",
                "sort_order": 1,
                "translations": [
                    {"language": "en", "text": "Dog", "phonetic": "/dɔːɡ/", "example": "The dog is playing."},
                    {"language": "pl", "text": "Pies", "phonetic": "/pjɛs/", "example": "Pies biega po trawie."},
                    {"language": "es", "text": "Perro", "phonetic": "/ˈpe.ro/", "example": "El perro está jugando."}
                ],
                "prerequisites": []
            },
            {
                "id": uuid.uuid5(uuid.NAMESPACE_DNS, "word-cat"),
                "difficulty": "beginner",
                "sort_order": 2,
                "translations": [
                    {"language": "en", "text": "Cat", "phonetic": "/kæt/", "example": "The cat sleeps."},
                    {"language": "pl", "text": "Kot", "phonetic": "/kɔt/", "example": "Kot śpi na kanapie."},
                    {"language": "es", "text": "Gato", "phonetic": "/ˈɡa.to/", "example": "El gato está durmiendo."}
                ],
                "prerequisites": []
            },
            {
                "id": uuid.uuid5(uuid.NAMESPACE_DNS, "word-bird"),
                "difficulty": "beginner",
                "sort_order": 3,
                "translations": [
                    {"language": "en", "text": "Bird", "phonetic": "/bɜːrd/", "example": "I see a bird."},
                    {"language": "pl", "text": "Ptak", "phonetic": "/ptak/", "example": "Widzę ptaka."},
                    {"language": "es", "text": "Pájaro", "phonetic": "/ˈpa.ʝa.ɾo/", "example": "Veo un pájaro."}
                ],
                "prerequisites": []
            },
            {
                "id": uuid.uuid5(uuid.NAMESPACE_DNS, "word-fish"),
                "difficulty": "beginner",
                "sort_order": 4,
                "translations": [
                    {"language": "en", "text": "Fish", "phonetic": "/fɪʃ/", "example": "Fish swim in water."},
                    {"language": "pl", "text": "Ryba", "phonetic": "/ˈrɨ.ba/", "example": "Ryby pływają w wodzie."},
                    {"language": "es", "text": "Pez", "phonetic": "/peθ/", "example": "Los peces nadan en el agua."}
                ],
                "prerequisites": []
            },
            # INTERMEDIATE
            {
                "id": uuid.uuid5(uuid.NAMESPACE_DNS, "word-rabbit"),
                "difficulty": "intermediate",
                "sort_order": 5,
                "translations": [
                    {"language": "en", "text": "Rabbit", "phonetic": "/ˈræbɪt/", "example": "The rabbit has long ears."},
                    {"language": "pl", "text": "Królik", "phonetic": "/ˈkrɔ.lik/", "example": "Królik ma długie uszy."},
                    {"language": "es", "text": "Conejo", "phonetic": "/koˈne.xo/", "example": "El conejo tiene orejas largas."}
                ],
                "prerequisites": ["word-cat", "word-fish"]
            },
            {
                "id": uuid.uuid5(uuid.NAMESPACE_DNS, "word-squirrel"),
                "difficulty": "intermediate",
                "sort_order": 6,
                "translations": [
                    {"language": "en", "text": "Squirrel", "phonetic": "/ˈskwɪrəl/", "example": "The squirrel climbs trees."},
                    {"language": "pl", "text": "Wiewiórka", "phonetic": "/vʲɛˈvjuːrka/", "example": "Wiewiórka wspina się na drzewa."},
                    {"language": "es", "text": "Ardilla", "phonetic": "/aɾˈðiʎa/", "example": "La ardilla trepa árboles."}
                ],
                "prerequisites": ["word-bird", "word-cat"]
            },
            {
                "id": uuid.uuid5(uuid.NAMESPACE_DNS, "word-horse"),
                "difficulty": "intermediate",
                "sort_order": 7,
                "translations": [
                    {"language": "en", "text": "Horse", "phonetic": "/hɔːrs/", "example": "Horses run fast."},
                    {"language": "pl", "text": "Koń", "phonetic": "/kɔɲ/", "example": "Konie biegną szybko."},
                    {"language": "es", "text": "Caballo", "phonetic": "/kaˈbaʎo/", "example": "Los caballos corren rápido."}
                ],
                "prerequisites": ["word-dog"]
            },
            {
                "id": uuid.uuid5(uuid.NAMESPACE_DNS, "word-cow"),
                "difficulty": "intermediate",
                "sort_order": 8,
                "translations": [
                    {"language": "en", "text": "Cow", "phonetic": "/kaʊ/", "example": "Cows give milk."},
                    {"language": "pl", "text": "Krowa", "phonetic": "/ˈkrɔ.va/", "example": "Krowy dają mleko."},
                    {"language": "es", "text": "Vaca", "phonetic": "/ˈba.ka/", "example": "Las vacas dan leche."}
                ],
                "prerequisites": ["word-horse"]
            },
            # ADVANCED
            {
                "id": uuid.uuid5(uuid.NAMESPACE_DNS, "word-hedgehog"),
                "difficulty": "advanced",
                "sort_order": 9,
                "translations": [
                    {"language": "en", "text": "Hedgehog", "phonetic": "/ˈhedʒhɒɡ/", "example": "The hedgehog has spines."},
                    {"language": "pl", "text": "Jeż", "phonetic": "/jɛʂ/", "example": "Jeż ma kolce."},
                    {"language": "es", "text": "Erizo", "phonetic": "/eˈɾi.θo/", "example": "El erizo tiene púas."}
                ],
                "prerequisites": ["word-rabbit", "word-squirrel"]
            },
            {
                "id": uuid.uuid5(uuid.NAMESPACE_DNS, "word-fox"),
                "difficulty": "advanced",
                "sort_order": 10,
                "translations": [
                    {"language": "en", "text": "Fox", "phonetic": "/fɒks/", "example": "The fox is clever."},
                    {"language": "pl", "text": "Lis", "phonetic": "/lʲis/", "example": "Lis jest sprytny."},
                    {"language": "es", "text": "Zorro", "phonetic": "/ˈso.ro/", "example": "El zorro es astuto."}
                ],
                "prerequisites": ["word-squirrel", "word-hedgehog"]
            },
        ]
    },
    {
        "name": "Space & NASA",
        "description": "Explore space, planets, rockets, and NASA vocabulary",
        "icon": "",
        "color": "#1E88E5",
        "words": [
            # BEGINNER - Basic space concepts
            {
                "id": uuid.uuid5(uuid.NAMESPACE_DNS, "word-star"),
                "difficulty": "beginner",
                "sort_order": 1,
                "translations": [
                    {"language": "en", "text": "Star", "phonetic": "/stɑːr/", "example": "The star shines at night."},
                    {"language": "pl", "text": "Gwiazda", "phonetic": "/ˈɡvʲa.zda/", "example": "Gwiazda świeci w nocy."},
                    {"language": "es", "text": "Estrella", "phonetic": "/esˈtɾe.ʎa/", "example": "La estrella brilla en la noche."}
                ],
                "prerequisites": []
            },
            {
                "id": uuid.uuid5(uuid.NAMESPACE_DNS, "word-moon"),
                "difficulty": "beginner",
                "sort_order": 2,
                "translations": [
                    {"language": "en", "text": "Moon", "phonetic": "/muːn/", "example": "The moon is full tonight."},
                    {"language": "pl", "text": "Księżyc", "phonetic": "/ˈkʂɛ̃.ʐɨt͡s/", "example": "Księżyc jest w pełni."},
                    {"language": "es", "text": "Luna", "phonetic": "/ˈlu.na/", "example": "La luna está llena esta noche."}
                ],
                "prerequisites": []
            },
            {
                "id": uuid.uuid5(uuid.NAMESPACE_DNS, "word-rocket"),
                "difficulty": "beginner",
                "sort_order": 3,
                "translations": [
                    {"language": "en", "text": "Rocket", "phonetic": "/ˈrɒkɪt/", "example": "The rocket flies to space."},
                    {"language": "pl", "text": "Rakieta", "phonetic": "/raˈkʲɛ.ta/", "example": "Rakieta leci w kosmos."},
                    {"language": "es", "text": "Cohete", "phonetic": "/koˈe.te/", "example": "El cohete vuela al espacio."}
                ],
                "prerequisites": []
            },
            {
                "id": uuid.uuid5(uuid.NAMESPACE_DNS, "word-space"),
                "difficulty": "beginner",
                "sort_order": 4,
                "translations": [
                    {"language": "en", "text": "Space", "phonetic": "/speɪs/", "example": "Earth is in space."},
                    {"language": "pl", "text": "Kosmos", "phonetic": "/ˈkɔs.mɔs/", "example": "Ziemia jest w kosmosie."},
                    {"language": "es", "text": "Espacio", "phonetic": "/esˈpa.θjo/", "example": "La Tierra está en el espacio."}
                ],
                "prerequisites": []
            },
            {
                "id": uuid.uuid5(uuid.NAMESPACE_DNS, "word-sun"),
                "difficulty": "beginner",
                "sort_order": 5,
                "translations": [
                    {"language": "en", "text": "Sun", "phonetic": "/sʌn/", "example": "The sun gives us light."},
                    {"language": "pl", "text": "Słońce", "phonetic": "/ˈswɔɲt͡sɛ/", "example": "Słońce daje nam światło."},
                    {"language": "es", "text": "Sol", "phonetic": "/sol/", "example": "El sol nos da luz."}
                ],
                "prerequisites": []
            },
            {
                "id": uuid.uuid5(uuid.NAMESPACE_DNS, "word-astronaut"),
                "difficulty": "beginner",
                "sort_order": 6,
                "translations": [
                    {"language": "en", "text": "Astronaut", "phonetic": "/ˈæstrənɔːt/", "example": "The astronaut floats in space."},
                    {"language": "pl", "text": "Astronauta", "phonetic": "/as.troˈnaw.ta/", "example": "Astronauta unosi się w kosmosie."},
                    {"language": "es", "text": "Astronauta", "phonetic": "/as.tɾoˈnaw.ta/", "example": "El astronauta flota en el espacio."}
                ],
                "prerequisites": []
            },
            # INTERMEDIATE
            {
                "id": uuid.uuid5(uuid.NAMESPACE_DNS, "word-planet"),
                "difficulty": "intermediate",
                "sort_order": 7,
                "translations": [
                    {"language": "en", "text": "Planet", "phonetic": "/ˈplænɪt/", "example": "Earth is a blue planet."},
                    {"language": "pl", "text": "Planeta", "phonetic": "/plaˈnɛ.ta/", "example": "Ziemia jest niebieską planetą."},
                    {"language": "es", "text": "Planeta", "phonetic": "/plaˈnɛ.ta/", "example": "La Tierra es un planeta azul."}
                ],
                "prerequisites": ["word-star", "word-space"]
            },
            {
                "id": uuid.uuid5(uuid.NAMESPACE_DNS, "word-earth"),
                "difficulty": "intermediate",
                "sort_order": 8,
                "translations": [
                    {"language": "en", "text": "Earth", "phonetic": "/ɜːrθ/", "example": "We live on Earth."},
                    {"language": "pl", "text": "Ziemia", "phonetic": "/ˈʑɛ.mja/", "example": "Mieszkamy na Ziemi."},
                    {"language": "es", "text": "Tierra", "phonetic": "/ˈtjɛ.ɾa/", "example": "Vivimos en la Tierra."}
                ],
                "prerequisites": ["word-planet", "word-sun"]
            },
            {
                "id": uuid.uuid5(uuid.NAMESPACE_DNS, "word-orbit"),
                "difficulty": "intermediate",
                "sort_order": 9,
                "translations": [
                    {"language": "en", "text": "Orbit", "phonetic": "/ˈɔːrbɪt/", "example": "The satellite is in orbit."},
                    {"language": "pl", "text": "Orbita", "phonetic": "/ˈɔr.bi.ta/", "example": "Satelita jest na orbicie."},
                    {"language": "es", "text": "Órbita", "phonetic": "/ˈoɾ.bi.ta/", "example": "El satélite está en órbita."}
                ],
                "prerequisites": ["word-planet", "word-rocket"]
            },
            {
                "id": uuid.uuid5(uuid.NAMESPACE_DNS, "word-mars"),
                "difficulty": "intermediate",
                "sort_order": 10,
                "translations": [
                    {"language": "en", "text": "Mars", "phonetic": "/mɑːrz/", "example": "Mars is the red planet."},
                    {"language": "pl", "text": "Mars", "phonetic": "/mars/", "example": "Mars jest czerwoną planetą."},
                    {"language": "es", "text": "Marte", "phonetic": "/maɾ.te/", "example": "Marte es el planeta rojo."}
                ],
                "prerequisites": ["word-planet", "word-earth"]
            },
            {
                "id": uuid.uuid5(uuid.NAMESPACE_DNS, "word-satellite"),
                "difficulty": "intermediate",
                "sort_order": 11,
                "translations": [
                    {"language": "en", "text": "Satellite", "phonetic": "/ˈsætəlaɪt/", "example": "The satellite orbits Earth."},
                    {"language": "pl", "text": "Satelita", "phonetic": "/sa.tɛˈlita/", "example": "Satelita krąży wokół Ziemi."},
                    {"language": "es", "text": "Satélite", "phonetic": "/saˈtɛ.li.tɛ/", "example": "El satélite orbita la Tierra."}
                ],
                "prerequisites": ["word-orbit", "word-earth"]
            },
            # ADVANCED
            {
                "id": uuid.uuid5(uuid.NAMESPACE_DNS, "word-galaxy"),
                "difficulty": "advanced",
                "sort_order": 12,
                "translations": [
                    {"language": "en", "text": "Galaxy", "phonetic": "/ˈɡæləksi/", "example": "Our galaxy is the Milky Way."},
                    {"language": "pl", "text": "Galaktyka", "phonetic": "/ɡaˈlak.tɨ.ka/", "example": "Nasza galaktyka to Droga Mleczna."},
                    {"language": "es", "text": "Galaxia", "phonetic": "/ɡaˈlak.sja/", "example": "Nuestra galaxia es la Vía Láctea."}
                ],
                "prerequisites": ["word-star", "word-space"]
            },
            {
                "id": uuid.uuid5(uuid.NAMESPACE_DNS, "word-telescope"),
                "difficulty": "advanced",
                "sort_order": 13,
                "translations": [
                    {"language": "en", "text": "Telescope", "phonetic": "/ˈtɛlɪskoʊp/", "example": "The telescope sees far away."},
                    {"language": "pl", "text": "Teleskop", "phonetic": "/tɛˈlɛs.kɔp/", "example": "Teleskop widzi daleko."},
                    {"language": "es", "text": "Telescopio", "phonetic": "/tɛˈlɛs.kɔ.pjo/", "example": "El telescopio ve lejos."}
                ],
                "prerequisites": ["word-star", "word-planet"]
            },
            {
                "id": uuid.uuid5(uuid.NAMESPACE_DNS, "word-meteor"),
                "difficulty": "advanced",
                "sort_order": 14,
                "translations": [
                    {"language": "en", "text": "Meteor", "phonetic": "/ˈmiːtiɔːr/", "example": "A meteor flew across the sky."},
                    {"language": "pl", "text": "Meteor", "phonetic": "/ˈmʲɛ.tɔr/", "example": "Meteor przeleciał po niebie."},
                    {"language": "es", "text": "Meteorito", "phonetic": "/mɛ.tɛ.oˈɾi.to/", "example": "Un meteorito cruzó el cielo."}
                ],
                "prerequisites": ["word-star", "word-space"]
            },
            {
                "id": uuid.uuid5(uuid.NAMESPACE_DNS, "word-gravity"),
                "difficulty": "advanced",
                "sort_order": 15,
                "translations": [
                    {"language": "en", "text": "Gravity", "phonetic": "/ˈɡrævəti/", "example": "Gravity keeps us on the ground."},
                    {"language": "pl", "text": "Grawitacja", "phonetic": "/ɡra.viˈta.ts͡ja/", "example": "Grawitacja trzyma nas na ziemi."},
                    {"language": "es", "text": "Gravedad", "phonetic": "/ɡɾa.βɛˈðað/", "example": "La gravedad nos mantiene en el suelo."}
                ],
                "prerequisites": ["word-earth", "word-orbit"]
            },
            {
                "id": uuid.uuid5(uuid.NAMESPACE_DNS, "word-nebula"),
                "difficulty": "advanced",
                "sort_order": 16,
                "translations": [
                    {"language": "en", "text": "Nebula", "phonetic": "/ˈnɛbjələ/", "example": "A nebula is a cloud in space."},
                    {"language": "pl", "text": "Mgławica", "phonetic": "/mɡwaˈvʲi.t͡sa/", "example": "Mgławica to chmura w kosmosie."},
                    {"language": "es", "text": "Nebulosa", "phonetic": "/nɛ.buˈlɔ.sa/", "example": "Una nebulosa es una nube en el espacio."}
                ],
                "prerequisites": ["word-galaxy", "word-star"]
            },
            {
                "id": uuid.uuid5(uuid.NAMESPACE_DNS, "word-crater"),
                "difficulty": "advanced",
                "sort_order": 17,
                "translations": [
                    {"language": "en", "text": "Crater", "phonetic": "/ˈkreɪtər/", "example": "The moon has many craters."},
                    {"language": "pl", "text": "Kratier", "phonetic": "/ˈkra.t͡ɕɛr/", "example": "Księżyc ma wiele kraterów."},
                    {"language": "es", "text": "Cráter", "phonetic": "/ˈkɾa.tɛɾ/", "example": "La luna tiene muchos cráteres."}
                ],
                "prerequisites": ["word-moon", "word-mars"]
            },
            {
                "id": uuid.uuid5(uuid.NAMESPACE_DNS, "word-launchpad"),
                "difficulty": "advanced",
                "sort_order": 18,
                "translations": [
                    {"language": "en", "text": "Launchpad", "phonetic": "/ˈlɔːntʃpæd/", "example": "The rocket waits on the launchpad."},
                    {"language": "pl", "text": "Platforma startowa", "phonetic": "/platˈfɔr.ma starˈtɔ.va/", "example": "Rakieta czeka na platformie startowej."},
                    {"language": "es", "text": "Plataforma de lanzamiento", "phonetic": "/plaˈtɔr.ma ma lan.θaˈmjen.to/", "example": "El cohete espera en la plataforma de lanzamiento."}
                ],
                "prerequisites": ["word-rocket", "word-astronaut"]
            },
            {
                "id": uuid.uuid5(uuid.NAMESPACE_DNS, "word-mission-control"),
                "difficulty": "advanced",
                "sort_order": 19,
                "translations": [
                    {"language": "en", "text": "Mission Control", "phonetic": "/ˈmɪʃn kənˈtroʊl/", "example": "Mission Control talks to astronauts."},
                    {"language": "pl", "text": "Centrum kontroli", "phonetic": "/ˈt͡sɛn.tɾum kɔnˈtrɔ.lɨ/", "example": "Centrum kontroli rozmawia z astronautami."},
                    {"language": "es", "text": "Control de misión", "phonetic": "/kɔnˈtɾɔl dɛ miˈsjɔn/", "example": "El control de misión habla con los astronautas."}
                ],
                "prerequisites": ["word-astronaut", "word-rocket", "word-satellite"]
            }
        ]
    },
    {
        "name": "Food & Home",
        "description": "Learn about food and household items",
        "icon": "",
        "color": "#FF9800",
        "words": [
            # BEGINNER - Basic food items
            {
                "id": uuid.uuid5(uuid.NAMESPACE_DNS, "word-apple"),
                "difficulty": "beginner",
                "sort_order": 1,
                "translations": [
                    {"language": "en", "text": "Apple", "phonetic": "/ˈæpl/", "example": "I eat an apple."},
                    {"language": "pl", "text": "Jabłko", "phonetic": "/ˈjab.wkɔ/", "example": "Jem jabłko."},
                    {"language": "es", "text": "Manzana", "phonetic": "/manˈθa.na/", "example": "Como una manzana."}
                ],
                "prerequisites": []
            },
            {
                "id": uuid.uuid5(uuid.NAMESPACE_DNS, "word-bread"),
                "difficulty": "beginner",
                "sort_order": 2,
                "translations": [
                    {"language": "en", "text": "Bread", "phonetic": "/bred/", "example": "I like bread."},
                    {"language": "pl", "text": "Chleb", "phonetic": "/xlɛp/", "example": "Lubię chleb."},
                    {"language": "es", "text": "Pan", "phonetic": "/pan/", "example": "Me gusta el pan."}
                ],
                "prerequisites": []
            },
            {
                "id": uuid.uuid5(uuid.NAMESPACE_DNS, "word-milk"),
                "difficulty": "beginner",
                "sort_order": 3,
                "translations": [
                    {"language": "en", "text": "Milk", "phonetic": "/mɪlk/", "example": "I drink milk."},
                    {"language": "pl", "text": "Mleko", "phonetic": "/ˈmlɛ.kɔ/", "example": "Piję mleko."},
                    {"language": "es", "text": "Leche", "phonetic": "/ˈle.tʃe/", "example": "Bebo leche."}
                ],
                "prerequisites": []
            },
            {
                "id": uuid.uuid5(uuid.NAMESPACE_DNS, "word-water"),
                "difficulty": "beginner",
                "sort_order": 4,
                "translations": [
                    {"language": "en", "text": "Water", "phonetic": "/ˈwɔːtər/", "example": "Water is good."},
                    {"language": "pl", "text": "Woda", "phonetic": "/ˈvɔ.da/", "example": "Woda jest dobra."},
                    {"language": "es", "text": "Agua", "phonetic": "/ˈa.ɣwa/", "example": "El agua es buena."}
                ],
                "prerequisites": []
            },
            {
                "id": uuid.uuid5(uuid.NAMESPACE_DNS, "word-chair"),
                "difficulty": "beginner",
                "sort_order": 5,
                "translations": [
                    {"language": "en", "text": "Chair", "phonetic": "/tʃɛr/", "example": "I sit on a chair."},
                    {"language": "pl", "text": "Krzesło", "phonetic": "/ˈkʂɛ.swɔ/", "example": "Siedzę na krześle."},
                    {"language": "es", "text": "Silla", "phonetic": "/ˈsiʎa/", "example": "Me siento en una silla."}
                ],
                "prerequisites": []
            },
            {
                "id": uuid.uuid5(uuid.NAMESPACE_DNS, "word-table"),
                "difficulty": "beginner",
                "sort_order": 6,
                "translations": [
                    {"language": "en", "text": "Table", "phonetic": "/ˈteɪbəl/", "example": "The plate is on the table."},
                    {"language": "pl", "text": "Stół", "phonetic": "/stuw/", "example": "Talerz jest na stole."},
                    {"language": "es", "text": "Mesa", "phonetic": "/ˈme.sa/", "example": "El plato está en la mesa."}
                ],
                "prerequisites": []
            },
            # INTERMEDIATE
            {
                "id": uuid.uuid5(uuid.NAMESPACE_DNS, "word-breakfast"),
                "difficulty": "intermediate",
                "sort_order": 7,
                "translations": [
                    {"language": "en", "text": "Breakfast", "phonetic": "/ˈbrekfəst/", "example": "I eat breakfast in the morning."},
                    {"language": "pl", "text": "Śniadanie", "phonetic": "/ˈɲa.daɲɛ/", "example": "Jem śniadanie rano."},
                    {"language": "es", "text": "Desayuno", "phonetic": "/de.saˈʝu.no/", "example": "Como desayuno por la mañana."}
                ],
                "prerequisites": ["word-bread", "word-milk", "word-apple"]
            },
            {
                "id": uuid.uuid5(uuid.NAMESPACE_DNS, "word-cheese"),
                "difficulty": "intermediate",
                "sort_order": 8,
                "translations": [
                    {"language": "en", "text": "Cheese", "phonetic": "/tʃiːz/", "example": "I like cheese on bread."},
                    {"language": "pl", "text": "Ser", "phonetic": "/sɛr/", "example": "Lubię ser na chlebie."},
                    {"language": "es", "text": "Queso", "phonetic": "/ˈke.so/", "example": "Me gusta el queso en el pan."}
                ],
                "prerequisites": ["word-bread", "word-milk"]
            },
            {
                "id": uuid.uuid5(uuid.NAMESPACE_DNS, "word-kitchen"),
                "difficulty": "intermediate",
                "sort_order": 9,
                "translations": [
                    {"language": "en", "text": "Kitchen", "phonetic": "/ˈkɪtʃən/", "example": "We cook in the kitchen."},
                    {"language": "pl", "text": "Kuchnia", "phonetic": "/ˈkuxɲa/", "example": "Gotujemy w kuchni."},
                    {"language": "es", "text": "Cocina", "phonetic": "/koˈθi.na/", "example": "Cocinamos en la cocina."}
                ],
                "prerequisites": ["word-table", "word-chair"]
            },
            # ADVANCED
            {
                "id": uuid.uuid5(uuid.NAMESPACE_DNS, "word-refrigerator"),
                "difficulty": "advanced",
                "sort_order": 10,
                "translations": [
                    {"language": "en", "text": "Refrigerator", "phonetic": "/rɪˈfrɪdʒəreɪtər/", "example": "The food is cold in the refrigerator."},
                    {"language": "pl", "text": "Lodówka", "phonetic": "/lɔˈdɔf.ka/", "example": "Jedzenie jest zimne w lodówce."},
                    {"language": "es", "text": "Refrigerador", "phonetic": "/ref.ɾi.xe.ɾaˈðoɾ/", "example": "La comida está fría en el refrigerador."}
                ],
                "prerequisites": ["word-kitchen", "word-milk", "word-cheese"]
            },
        ]
    }
]


# Word name to ID mapping for prerequisites
WORD_IDS = {}


async def seed_database(db: AsyncSession) -> None:
    """Seed the database with sample domains and words."""
    print("Seeding database...")

    # Check if already seeded
    result = await db.execute(select(Domain).where(Domain.is_system == True))
    existing = result.scalar_one_or_none()
    if existing:
        print("Database already seeded. Skipping.")
        return

    # Create domains
    for domain_data in DOMAINS_DATA:
        domain = Domain(
            name=domain_data["name"],
            description=domain_data["description"],
            icon=domain_data["icon"],
            color=domain_data["color"],
            is_system=True,
            user_id=None
        )
        db.add(domain)
        await db.flush()

        # Create words for this domain
        for word_data in domain_data["words"]:
            WORD_IDS[f"word-{word_data['translations'][0]['text'].lower()}"] = word_data["id"]

        for word_data in domain_data["words"]:
            word = Word(
                id=word_data["id"],
                domain_id=domain.id,
                difficulty=word_data["difficulty"],
                sort_order=word_data["sort_order"]
            )
            db.add(word)
            await db.flush()

            # Create translations
            for trans_data in word_data["translations"]:
                translation = WordTranslation(
                    word_id=word.id,
                    language=trans_data["language"],
                    text=trans_data["text"],
                    phonetic=trans_data.get("phonetic"),
                    example_sentence=trans_data.get("example_sentence")
                )
                db.add(translation)

            # Create prerequisites
            for prereq_name in word_data["prerequisites"]:
                prereq_id = WORD_IDS.get(prereq_name)
                if prereq_id:
                    prerequisite = WordPrerequisite(
                        word_id=word.id,
                        prerequisite_id=prereq_id
                    )
                    db.add(prerequisite)

        print(f"Created domain: {domain.name} with {len(domain_data['words'])} words")

    await db.commit()
    print("Database seeding complete!")


async def main():
    """Main entry point for seeding."""
    # Create all tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    # Seed data
    async with async_session() as db:
        await seed_database(db)


if __name__ == "__main__":
    asyncio.run(main())
