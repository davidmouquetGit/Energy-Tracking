from gestionbdd.models import ConsoHeureElec, ConsoJourElec, ConsoJourGaz
from sqlalchemy.exc import IntegrityError
import logging
from sqlalchemy.dialects.postgresql import insert
from datetime import datetime
import streamlit as st


def insert_data_conso_horaire(db, records):
    """
    Insère les données horaires dans la base PostgreSQL.
    Si un horodatage existe déjà, la valeur est mise à jour (upsert).
    """
    data_to_insert = []

    # Prépare les données
    for record in records:
        try:
            value_float = float(record["value"])
            ts = datetime.strptime(record["date"], "%Y-%m-%d %H:%M:%S")
            data_to_insert.append({"horodatage": ts, "value": value_float})
        except Exception as e:
            return False

    # Upsert (INSERT or UPDATE)
    try:
        stmt = insert(ConsoHeureElec).values(data_to_insert)
        stmt = stmt.on_conflict_do_update(
            index_elements=["horodatage"],  # correspond à UNIQUE (horodatage)
            set_={"value": stmt.excluded.value}  # met à jour la valeur
        )

        db.execute(stmt)
        db.commit()

    except IntegrityError as e:
        db.rollback()
        return False
    except Exception as e:
        db.rollback()
        return False
    
    return True


def insert_data_conso_jour(db, df):
    data_to_insert = []

    # Prépare les données
    for idx_, row in df.iterrows():
        try:
            data_to_insert.append({"horodatage":row['horodatage'], "value": row['value']})
        except Exception as e:
            return f"Erreur de format sur l'enregistrement journalier données élec"


    # Upsert (INSERT or UPDATE)
    try:
        stmt = insert(ConsoJourElec).values(data_to_insert)
        stmt = stmt.on_conflict_do_update(
            index_elements=["horodatage"],  # correspond à UNIQUE (horodatage)
            set_={"value": stmt.excluded.value}  # met à jour la valeur
        )

        db.execute(stmt)
        db.commit()

    except IntegrityError as e:
        db.rollback()
        return f"Erreur d'intégrité données élec jours: {e}"
    except Exception as e:
        db.rollback()
        return f"Erreur d'insertion données élec jours: {e}"
    return "OK"


    

def insert_data_conso_gaz_jour(db, df):
    import pandas as pd
    

    data_to_insert = []

    # Prépare les données
    for idx_, row in df.iterrows():
        try:
            data_to_insert.append({"horodatage":row['horodatage'], "volume": row['volume'], "energie": row['energie'], "pci": row['pci'], "text": row['text']})
        except Exception as e:
            return f"Erreur de format sur l'enregistrement journalier données gaz"


    # Upsert (INSERT or UPDATE)
    try:
        stmt = insert(ConsoJourGaz).values(data_to_insert)
        stmt = stmt.on_conflict_do_update(
            index_elements=["horodatage"],  # correspond à UNIQUE (horodatage)
            set_={"energie": stmt.excluded.energie}  # met à jour la valeur
        )

        db.execute(stmt)
        db.commit()

    except IntegrityError as e:
        db.rollback()
        return f"Erreur d'intégrité données gaz jours: {e}"
    except Exception as e:
        db.rollback()
        return f"Erreur d'insertion données gaz jours: {e}"
    return "OK"


