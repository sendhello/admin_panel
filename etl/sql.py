BASE_FILM_WORK_SQL = """
    SELECT
        fw.id as id, 
        fw.title as title, 
        fw.description as description, 
        fw.rating as rating, 
        fw.type as type, 
        fw.created as created, 
        fw.modified as modified, 
        pfw.role as role, 
        p.id as person_id, 
        p.full_name as full_name,
        g.name as genre_name
    FROM content.film_work fw
    LEFT JOIN content.person_film_work pfw ON pfw.film_work_id = fw.id
    LEFT JOIN content.person p ON p.id = pfw.person_id
    LEFT JOIN content.genre_film_work gfw ON gfw.film_work_id = fw.id
    LEFT JOIN content.genre g ON g.id = gfw.genre_id
    WHERE {condition}
    ORDER BY fw.modified;
"""
FILM_WORK_BY_LAST_MODIFIED_SQL = BASE_FILM_WORK_SQL.format(condition='fw.modified >= \'{last_modified}\'')
FILM_WORK_BY_IDS_SQL = BASE_FILM_WORK_SQL.format(condition='fw.id IN {film_work_ids}')

GENRE_BY_LAST_MODIFIED_SQL = """
    SELECT id, modified
    FROM content.genre
    WHERE modified >= '{last_modified}'
    ORDER BY modified;
"""

PERSON_BY_LAST_MODIFIED_SQL = """
    SELECT id, modified
    FROM content.person
    WHERE modified >= '{last_modified}'
    ORDER BY modified;
"""

FILM_WORK_IDS_BY_GENRE_IDS_SQL = """
    SELECT fw.id as id, fw.modified as modified
    FROM content.film_work fw
    LEFT JOIN content.genre_film_work gfw ON gfw.film_work_id = fw.id
    WHERE gfw.genre_id IN {record_ids}
    ORDER BY fw.modified; 
"""

FILM_WORK_IDS_BY_PERSON_IDS_SQL = """
    SELECT fw.id as id, fw.modified as modified
    FROM content.film_work fw
    LEFT JOIN content.person_film_work pfw ON pfw.film_work_id = fw.id
    WHERE pfw.person_id IN {record_ids}
    ORDER BY fw.modified; 
"""
