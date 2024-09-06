from flask import Blueprint, abort, flash, render_template, request, redirect
from flask_login import current_user, login_required
from ..extensions import db
from ..models.apiary import Apiary
from geopy.distance import geodesic

apiary = Blueprint('apiary', __name__)

@apiary.route('/apiary/all', methods=['POST', 'GET'])
def all():
    notes = Apiary.query.all()
    return render_template('apiary/all.html', notes=notes)

@apiary.route('/apiary/create', methods=['POST', 'GET'])
@login_required
def create():
    if request.method == 'POST':
        beeCount= request.form.get('beeCount')
        breed = request.form.get('breed')
        hiveType = request.form.get('hiveType')
        feed = request.form.get('feed')
        latitude = request.form.get('latitude')
        longitude = request.form.get('longitude')

        all_apiaries = Apiary.query.all()
        for apiary in all_apiaries:
            distance = geodesic((latitude, longitude), (apiary.latitude, apiary.longitude)).meters
            if distance < 1000:  # Пороговое расстояние в метрах
                flash("Пасеки расположены слишком близко!", "danger")
        apiary = Apiary(name=current_user.id, beeCount=beeCount, breed=breed, hiveType=hiveType, feed=feed, latitude=latitude, longitude=longitude)
        
        try:
            db.session.add(apiary)
            db.session.commit()
            flash("Пасека успешно добавлена!", "success")
            return redirect('/')
        except Exception as e:
            print(str(e))
    else:
        return render_template('apiary/create.html')
    
@apiary.route('/apiary/<int:id>/update', methods=['POST', 'GET'])
@login_required
def update(id):
    apiary = Apiary.query.get(id)
    
    if apiary.owner.id == current_user.id:
        if request.method == 'POST':
            apiary.beeCount= request.form.get('beeCount')
            apiary.breed = request.form.get('breed')
            apiary.hiveType = request.form.get('hiveType')
            apiary.feed = request.form.get('feed')        
            try:
                db.session.commit()
                return redirect('/')
            except Exception as e:
                print(str(e))
        else:
            return render_template('apiary/update.html', apiary = apiary)
    else:
        abort(403)
    
@apiary.route('/apiary/<int:id>/delete', methods=['POST', 'GET'])
def delete(id):
    apiary = Apiary.query.get(id)
    try:
        db.session.delete(apiary)
        db.session.commit()
        flash("Пасека успешно удалена!", "success")
        return redirect('/')
    except Exception as e:
        print(str(e))
    