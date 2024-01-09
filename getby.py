import pymysql
from UDFunctions import choose_genre
from UDFunctions import choose_artist


def get_records_by_genre(conn):
    """returns all the records in the given genre"""
    try:
        genre_id = choose_genre(conn)[0]
        cursor = conn.cursor()
        cursor.callproc('records_by_genre', (genre_id,))
        records = cursor.fetchall()
        if records:
            print("Here are all the records for the chosen genre:")
            for record in records:
                print(record)
        else:
            print("Error retrieving records by genre: ", records)
    except pymysql.Error as err:
        return err


def get_records_by_artist(conn):
    """returns all the records by the given artist"""
    try:
        artist_id = choose_artist(conn)[0]
        cursor = conn.cursor()
        cursor.callproc('records_by_artist', (artist_id,))
        records = cursor.fetchall()
        artist_id = input("Enter the artist ID: ")
        if records:
            print("Here are all the records for the chosen artist:")
            for record in records:
                print(record)
        else:
            print("Error retrieving records by artist: ", records)
    except pymysql.Error as err:
        return err
