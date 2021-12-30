from flask import Blueprint, render_template, redirect, request, abort, jsonify, url_for, flash
from src.model import User, LogItem, db
from src.utils import preprocess_img, authUserPhoto
from PIL import Image
import numpy as np
import os

#-- init --#
main = Blueprint('main', __name__, )

#-- endpoints --#


@main.route('/', methods=['GET'])
def getIndex():
    try:
        logItems = [i for i in LogItem.getAll()]
    except:
        return abort(500, 'Record not found')

    return render_template("index.html", table=logItems)


@main.route('/users', methods=['GET'])
def getUsers():
    try:
        users = User.getAll()
    except:
        return abort(500, 'Record not found')
    return render_template('users.html', users=users)


@main.route("/log/<id>",)
def getUserById(id):
    try:
        log = LogItem.get(id)
    except:
        return abort(404, "log Not Found")

    return render_template("log.html", log=log)


@main.route('/users/add')
def getUserPage():
    return render_template('register.html')


@main.route("/users/<int:id>")
def getUserByID(id):
    try:
        user = User.get(id)
        photo_path = f'userPhotos/user-{id}-photo-0.jpg'

    except:
        return abort(404)

    return render_template('user.html', user=user, photo_path=photo_path)


@main.route('/users/add', methods=['POST'])
def postUser():
    try:
        name = request.form.get('name')
        password = request.form.get('password')
        photos = request.files.to_dict(flat=False)

        photos = list(photos.values())[0]

        if password is None or name is None or photos is None or len(photos) != 3:
            abort(400)

        user = User(name=name, password=password)
        db.session.add(user)
        db.session.commit()

        for i in range(len(photos)):
            print('\n\nLOOOP', i, '\n\n')
            file = photos[i]
            path = os.path.join(os.getcwd(), 'static', 'userPhotos')
            if not os.path.exists(path):
                os.mkdir(path)
            print('\n\nFILE', file, '\n\n')

            file.save(os.path.join(path, f'user-{user.id}-photo-{i}.jpg'))

    except:
        return abort(400)

    id = user.id
    return redirect('/users/'+str(id))


@main.route('/auth', methods=['POST'])
def postIndex():
    '''
    This endpoint is responsible to authenticate the id, password, and photo of the user
    The user's id and password is first authenticated
    if passed, the user's photo and the sent photo are compared using a ML model
    '''

    # try:
    print('*****************',request.files)
    print('\n\n-------------',request.form,'\n\n')
    id = request.form.get('id')
    password = request.form.get('password')
    photo = request.files.get('image')
    
    print('---\n\n')
    print(id)
    print(password)
    print(photo)
    print('---\n\n')

    if User.auth(id, password):

        # TODO send two photos to the model
        # image path
        path = os.path.join(os.getcwd(), 'static', 'logPhotos')
        if not os.path.exists(path):
            os.mkdir(path)

        print('\n\nFILE', path, '\n\n')
        logItem = LogItem.insert(id, True)
        photo.save(os.path.join(path,f'log-{logItem.id}.jpg'))

        # model feed
        batch_img = preprocess_img(id)
        photo = Image.open(os.path.join(path,f'log-{logItem.id}.jpg'))
        photo = np.asarray(photo)
        res = authUserPhoto(batch_img,photo)
        if res:  # model successfully identified
            print('-----output-----',res)
            return jsonify({"success":True,})

        # try:
        User.get(id)
        logItem = LogItem.insert(id, False)
        # except:
        logItem = LogItem.insert(None, False)
        print('-----output-----',res)
        return jsonify({"success":False,})
    # except:
    #     return abort(400)


@ main.errorhandler(500)
def handle_500(err):
    return {
        'err', err
    }, 500
