from flask import request, Response
import jsonpickle
from app import app, embedding_index, PATHS


@app.route('/', methods=['POST'])
def get_closest_vector():
    content = request.get_json(silent=True)
    vector = content['vector']
    closest_celeb_index = embedding_index.get_nns_by_vector(vector, 1)[0]
    closest_celeb_filename = str(PATHS[closest_celeb_index])
    response = {'closest_celeb_filename': closest_celeb_filename}
    response_pickled = jsonpickle.encode(response)
    return Response(response=response_pickled, status=200, mimetype="application/json")
