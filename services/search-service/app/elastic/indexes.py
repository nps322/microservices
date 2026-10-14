MOVIE_MAPPING = {
    "properties": {
        "id": {
            "type": "long"
        },
        "title": {
            "type": "text"
        },
        "director_id": {
            "type": "long"
        },
        "director_name": {
            "type": "text"
        },
    }
}

INDEX_SETTINGS = {
    "number_of_shards": 1,
    "number_of_replicas": 0,
}