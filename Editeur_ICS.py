from datetime import datetime, date, timedelta
from uuid import uuid4
from pathlib import Path


# ============================================================
# PARAMÈTRES GÉNÉRAUX
# ============================================================

DATE_DEBUT = date(2026, 9, 1)
DATE_FIN = date(2027, 4, 16)

# ============================================================
# VACANCES SCOLAIRES - ZONE B / ROUEN
# ============================================================

VACANCES = [
    # Toussaint
    (date(2026, 10, 17), date(2026, 11, 1)),

    # Noël
    (date(2026, 12, 19), date(2027, 1, 3)),

    # Hiver
    (date(2027, 2, 20), date(2027, 3, 7)),

    # Pâques
    (date(2027, 4, 17), date(2027, 4, 30)),
]


# ============================================================
# JOURS FÉRIÉS
# ============================================================

JOURS_FERIES = {
    date(2026, 11, 1),   # Toussaint
    date(2026, 11, 11),  # Armistice

    date(2026, 12, 25),  # Noël

    date(2027, 1, 1),    # Jour de l'An
    date(2027, 3, 29),   # Lundi de Pâques
}


# ============================================================
# EXCEPTION :
# DS DU 11 NOVEMBRE
#
# Le planning indique :
# "11-nov info le 10/11 matin Férié à déplacer"
#
# Tu as demandé de laisser les DS supposés déplacés
# à leur place.
# ============================================================

DS_EXCEPTION_AUTORISE = {
    date(2026, 11, 11)
}


# ============================================================
# LISTE DES ÉVÉNEMENTS
# ============================================================

events = []


def add_event(jour, debut, fin, nom):
    events.append((
        f"{jour.isoformat()} {debut}",
        f"{jour.isoformat()} {fin}",
        nom
    ))


# ============================================================
# DS DU MERCREDI
#
# Créneau : 13h05 → 17h10
# ============================================================

DS_MERCREDI = {

    date(2026, 9, 9):
        "DS Maths",

    date(2026, 9, 16):
        "DS Informatique",

    date(2026, 9, 23):
        "DS Anglais",

    date(2026, 9, 30):
        "DS Maths",

    date(2026, 10, 7):
        "DS Physique",

    date(2026, 10, 14):
        "DS Français",

    date(2026, 11, 4):
        "DS Maths",

    date(2026, 11, 11):
        "DS Informatique",

    date(2026, 11, 18):
        "DS Anglais / Physique",

    date(2026, 11, 25):
        "DS Maths",

    date(2026, 12, 2):
        "DS Physique",

    date(2026, 12, 9):
        "DS Informatique",

    date(2026, 12, 16):
        "DS Maths",

    date(2027, 1, 6):
        "DS Physique",

    date(2027, 1, 13):
        "DS Français",

    date(2027, 1, 20):
        "DS Maths",

    date(2027, 1, 27):
        "DS Informatique",

    date(2027, 2, 3):
        "DS Anglais",

    date(2027, 2, 10):
        "DS Maths",

    date(2027, 2, 17):
        "DS Informatique",

    date(2027, 3, 10):
        "DS Physique",

    date(2027, 3, 17):
        "DS Français",

    date(2027, 3, 24):
        "DS Maths",
}


# ============================================================
# DS PARTICULIERS
# ============================================================

DS_PARTICULIERS = {

    # Jeudi 4 février
    date(2027, 2, 4): (
        "13:05",
        "17:10",
        "DS Physique"
    ),

    # Samedi 27 mars
    date(2027, 3, 27): (
        "07:45",
        "11:45",
        "DS Physique"
    ),
}


# ============================================================
# FONCTION : VACANCES ?
# ============================================================

def est_vacances(jour):

    for debut, fin in VACANCES:

        if debut <= jour <= fin:
            return True

    return False


# ============================================================
# FONCTION : JOUR FÉRIÉ ?
# ============================================================

def est_ferie(jour):

    return jour in JOURS_FERIES


# ============================================================
# GÉNÉRATION DU CALENDRIER
# ============================================================

jour = DATE_DEBUT

while jour <= DATE_FIN:

    # --------------------------------------------------------
    # VACANCES
    # --------------------------------------------------------

    if est_vacances(jour):
        jour += timedelta(days=1)
        continue


    # --------------------------------------------------------
    # JOUR FÉRIÉ
    #
    # Exception : DS du 11 novembre
    # --------------------------------------------------------

    if est_ferie(jour) and jour not in DS_EXCEPTION_AUTORISE:
        jour += timedelta(days=1)
        continue


    weekday = jour.weekday()

    # lundi    = 0
    # mardi    = 1
    # mercredi = 2
    # jeudi    = 3
    # vendredi = 4
    # samedi   = 5


    # ========================================================
    # DS DU MERCREDI
    # ========================================================

    if jour in DS_MERCREDI:

        # On conserve les cours du matin
        # puis le DS prend le créneau de l'après-midi.

        add_event(
            jour,
            "07:45",
            "09:45",
            "Maths — JO 0.21"
        )

        add_event(
            jour,
            "09:55",
            "11:45",
            "Physique — JO 0.21"
        )

        add_event(
            jour,
            "13:05",
            "17:10",
            DS_MERCREDI[jour]
        )

        jour += timedelta(days=1)
        continue


    # ========================================================
    # DS PARTICULIER
    # ========================================================

    if jour in DS_PARTICULIERS:

        debut, fin, nom = DS_PARTICULIERS[jour]

        add_event(
            jour,
            debut,
            fin,
            nom
        )

        # Le samedi 27 mars remplace complètement
        # les cours habituels du samedi.
        jour += timedelta(days=1)
        continue


    # ========================================================
    # LUNDI
    # ========================================================

    if weekday == 0:

        # -------------------------
        # MATIN
        # -------------------------

        add_event(
            jour,
            "07:45",
            "09:45",
            "Maths — JO 2.16"
        )

        add_event(
            jour,
            "09:55",
            "11:45",
            "Physique — TP PC"
        )

        # -------------------------
        # APRÈS-MIDI
        # -------------------------

        add_event(
            jour,
            "13:05",
            "14:00",
            "Physique — JO 0.21"
        )

        add_event(
            jour,
            "14:05",
            "16:10",
            "Maths — JO 0.21"
        )


    # ========================================================
    # MARDI
    # ========================================================

    elif weekday == 1:

        # -------------------------
        # MATIN
        # -------------------------

        add_event(
            jour,
            "07:45",
            "09:45",
            "Informatique — JO 0.21"
        )

        add_event(
            jour,
            "09:55",
            "11:45",
            "Maths — JO 0.21"
        )

        # -------------------------
        # APRÈS-MIDI
        # -------------------------

        add_event(
            jour,
            "14:05",
            "16:10",
            "TIPE"
        )


    # ========================================================
    # MERCREDI NORMAL
    # ========================================================

    elif weekday == 2:

        add_event(
            jour,
            "07:45",
            "09:45",
            "Maths — JO 0.21"
        )

        add_event(
            jour,
            "09:55",
            "11:45",
            "Physique — JO 0.21"
        )

        add_event(
            jour,
            "13:05",
            "17:10",
            "Devoir CPGE — JO 0.09 / Salle des conseils / Salle polyvalente"
        )


    # ========================================================
    # JEUDI
    # ========================================================

    elif weekday == 3:

        add_event(
            jour,
            "07:45",
            "09:45",
            "Maths — JO 0.21"
        )

        add_event(
            jour,
            "09:55",
            "11:45",
            "Anglais LV1 — JO 0.21"
        )


    # ========================================================
    # VENDREDI
    # ========================================================

    elif weekday == 4:

        add_event(
            jour,
            "07:45",
            "09:45",
            "Physique — JO 0.21"
        )

        add_event(
            jour,
            "09:55",
            "11:45",
            "Maths — JO 0.21"
        )


        # ----------------------------------------------------
        # ALTERNANCE A / B
        #
        # SEMAINE A :
        # Info     13h05 → 15h00
        # Physique 15h15 → 16h10
        #
        # SEMAINE B :
        # Physique 14h05 → 15h00
        # Info     15h15 → 17h10
        # ----------------------------------------------------

        lundi = jour - timedelta(days=weekday)

        numero_semaine = (
            lundi - date(2026, 8, 31)
        ).days // 7

        semaine_A = numero_semaine % 2 == 0


        if semaine_A:

            add_event(
                jour,
                "13:05",
                "15:00",
                "Informatique — CPGE 4"
            )

            add_event(
                jour,
                "15:15",
                "16:10",
                "Physique — JO 0.21"
            )

        else:

            add_event(
                jour,
                "14:05",
                "15:00",
                "Physique — JO 0.21"
            )

            add_event(
                jour,
                "15:15",
                "17:10",
                "Informatique — CPGE 4"
            )


    # ========================================================
    # SAMEDI
    # ========================================================

    elif weekday == 5:

        add_event(
            jour,
            "07:45",
            "09:45",
            "Français-Philo — JO 1.26"
        )

        add_event(
            jour,
            "09:55",
            "11:45",
            "Informatique — JO 0.21"
        )


    # Jour suivant
    jour += timedelta(days=1)


# ============================================================
# FORMATAGE ICS
# ============================================================

def fmt(dt_str):

    dt = datetime.strptime(
        dt_str,
        "%Y-%m-%d %H:%M"
    )

    return dt.strftime("%Y%m%dT%H%M%S")


# ============================================================
# EN-TÊTE DU CALENDRIER
# ============================================================

lines = [
    "BEGIN:VCALENDAR",
    "VERSION:2.0",
    "PRODID:-//OpenAI//EDT MPI//FR",
    "CALSCALE:GREGORIAN",
    "X-WR-CALNAME:EDT MPI — Groupe 1 — 2026-2027",
    "X-WR-TIMEZONE:Europe/Paris",
]


timestamp = datetime.utcnow().strftime(
    "%Y%m%dT%H%M%SZ"
)


# ============================================================
# CRÉATION DES VEVENT
# ============================================================

for start, end, summary in events:

    lines.extend([
        "BEGIN:VEVENT",
        f"UID:{uuid4()}",
        f"DTSTAMP:{timestamp}",
        f"DTSTART;TZID=Europe/Paris:{fmt(start)}",
        f"DTEND;TZID=Europe/Paris:{fmt(end)}",
        f"SUMMARY:{summary}",
        "DESCRIPTION:EDT MPI — Groupe 1 — Année 2026-2027",
        "END:VEVENT",
    ])


lines.append("END:VCALENDAR")


# ============================================================
# SAUVEGARDE
# ============================================================

path = Path(
    r"C:\Users\alban\Documents\Prépa\Spé\Autres\ICS Creator\EDT_MPI_Groupe1_2026-2027.ics"
)

path.write_text(
    "\r\n".join(lines),
    encoding="utf-8"
)


# ============================================================
# INFORMATIONS
# ============================================================

print()
print("=" * 60)
print("CALENDRIER MPI G1 GÉNÉRÉ")
print("=" * 60)
print()
print(f"Fichier : {path}")
print(f"Événements : {len(events)}")
print()
print("Période : 01/09/2026 → 16/04/2027")
print("Toussaint : exclue")
print("Noël : exclue")
print("Hiver : exclue")
print("Pâques : arrêt avant le 17/04/2027")
print("LV2 : supprimées")
print("Professeurs : supprimés")
print("DS intégrés")
print()
print("DONE")