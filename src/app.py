import celery.states as celery_states

from flask import Flask, request, jsonify, send_file
from flask.views import MethodView
from celery import Task


from src.upscale.upscale import run_upscaling
from src.mongo_client import save_file, get_file_by_id
from src.celery_app import get_task, celery_app


app = Flask(
    'Upscale_APP'
)


class ContextTask(Task):
    def __call__(self, *args: object, **kwargs: object) -> object:
        with app.app_context():
            return self.run(*args, **kwargs)


celery_app.Task = ContextTask


class UpscalePhotoView(MethodView):
    def get(self, task_id):
        task = get_task(task_id)
        if task.status == celery_states.FAILURE:
            result = None
        else:
            result = task.result

        return jsonify({
            'status': task.status,
            'result': result
        })

    def post(self):
        file = request.files.get('photo')
        if not file:
            return jsonify({
                'error': 'The photo was not attached to the request'
            }), 400

        file_id = save_file(file.stream, file.filename,
                            file.content_type)

        task = run_upscaling.delay(file_id)

        return jsonify({
            'task_id': task.id
        })


@app.get('/processed/<file_uuid>')
def get_file(file_uuid: str):
    print(file_uuid)
    grid = get_file_by_id(file_uuid)

    return send_file(
        grid,
        download_name=grid.filename,
        mimetype=grid.content_type,
        as_attachment=True
    )


upscale_photo_view = UpscalePhotoView.as_view("upscale_photo")
app.add_url_rule(
    '/upscale',
    view_func=upscale_photo_view,
    methods=['POST']
)
app.add_url_rule(
    '/tasks/<task_id>',
    view_func=upscale_photo_view,
    methods=['GET']
)
