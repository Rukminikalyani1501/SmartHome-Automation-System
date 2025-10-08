from flask import render_template, redirect, request, url_for
import hardware_routes
import recognition_technology
from model import app, db, Room, Device


@app.route('/')
def index():
    return redirect('login')


@app.route('/home')
def home():
    return render_template('index.html')


@app.route('/add_user', methods=['GET', 'POST'])
def view_add_user():
    from User.User_Controller import controller_add_user
    return controller_add_user()


@app.route('/edit_user', methods=['GET', 'POST'])
def view_edit_user():
    from User.User_Controller import controller_edit_user
    return controller_edit_user()


@app.route('/delete_user', methods=['GET', 'POST'])
def view_delete_user():
    from User.User_Controller import controller_delete_user
    return controller_delete_user()


@app.route('/login', methods=['GET', 'POST'])
def view_authenticate_login():
    from authentication import controller_authenticate_user
    return controller_authenticate_user()


@app.route('/logout', methods=['GET', 'POST'])
def view_authenticate_logout():
    from authentication import controller_logout
    return controller_logout()


# Route for displaying devices
@app.route('/devices')
def show_devices():
    from Devices.Devices_Controller import get_available_devices
    available_devices = get_available_devices()
    if not available_devices:
        return render_template('devices.html', msg='No available devices')
    return render_template('devices.html', devices=available_devices, msg='Detected devices in the house')


@app.route('/add_room', methods=['GET', 'POST'])
def add_room():
    from Rooms.Rooms_Controller import add_room
    return add_room()


@app.route('/rooms')
def show_rooms():
    from Rooms.Rooms_Controller import get_available_rooms
    rooms = get_available_rooms()
    return render_template('rooms.html', rooms=rooms)


@app.route('/show_room_devices/<int:room_id>')
def show_room_devices(room_id):
    room = Room.query.get(room_id)
    if not room.devices:
        return render_template('room.html', devices=[], msg='No devices available in this room.', room=room)
    else:
        from Rooms.Rooms_Controller import get_devices_in_room
        devices = get_devices_in_room(room_id)
        from Devices.Devices_Controller import get_available_devices
        available_devices = get_available_devices()
        for device in devices:
            for available_device in available_devices:
                if device.device_name == available_device.device_name:
                    device.status = True
                else:
                    device.status = False
        return render_template('room.html', devices=devices, room=room)


@app.route('/add_device_to_room/<int:room_id>', methods=['GET', 'POST'])
def add_device_to_room(room_id):
    from Devices.Devices_Controller import get_available_devices
    devices = get_available_devices()
    print(1112, devices)
    if request.method == 'POST':
        device_name = request.form['device_name']
        device_ip = request.form['device_IP']  # Get the selected device_id from the form
        room = Room.query.get(room_id)  # Retrieve the room object by room_id

        if room:
            device = Device(device_name, device_ip, False)  # Retrieve the device object by device_id
            from Devices.Devices_Model import check_device_exists
            boolean = check_device_exists(device_name)
            if not boolean:
                device.save()
            from Rooms.Rooms_Controller import check_device_exists_in_room
            boolean = check_device_exists_in_room(room_id, device_name)
            if not boolean:
                room.devices.append(device)  # Add the device to the room's devices list
                db.session.commit()  # Commit the changes to the database
                return redirect(url_for('show_room_devices', room_id=room_id))

        # If the room or device does not exist, or if there was an error, handle the appropriate response
        msg = 'The chosen device already exists in this room or another room. Please choose another device.'
        print(msg)
        return render_template('available_devices.html', room=room, msg=msg)

    # Handle GET request
    room = Room.query.get(room_id)
    print(room)
    if room:
        return render_template('available_devices.html', room=room, devices=devices)

    # If the room does not exist, handle the appropriate response
    return "Room not found."


@app.route('/available_devices')
def show_available_devices():
    from Devices.Devices_Controller import get_available_devices
    available_devices = get_available_devices()  # Assuming get_available_devices() returns a list of available devices
    if not available_devices:
        return render_template('available_devices.html', msg='No available devices')
    return render_template('available_devices.html', devices=available_devices, msg='Detected devices in the house')


@app.route('/hardware/<device_name>')
def hardware_controller(device_name):
    print(device_name)
    if device_name == 'RGBLight':
        return render_template('control_rgb.html', device_name=device_name, message=None)
    if device_name == 'DoorLock':
        return render_template('control_doorLock.html', device_name=device_name, message=None)


@app.route('/control/<device_name>/turn_on')
def turn_on(device_name):
    if request.method == 'GET':

        if device_name == 'RGBLight':
            message = hardware_routes.turn_on_light()
            return render_template('control_rgb.html', device_name=device_name, message=message)
        elif device_name == 'DoorLock':
            if recognition_technology.check_person_exists_in_database():
                message = hardware_routes.unlock_door()
                return render_template('control_doorLock.html', device_name=device_name, message=message)
            else:
                return render_template('control_doorLock.html', device_name=device_name, message='Not Allowed to enter')
        else:
            return render_template('rooms.html')


@app.route('/control/<device_name>/turn_off')
def turn_off_light(device_name):
    if request.method == 'GET':
        message = ''
        if device_name == 'RGBLight':
            message = hardware_routes.turn_off_light()
            return render_template('control_rgb.html', device_name=device_name, message=message)
        elif device_name == 'DoorLock':
            message = hardware_routes.lock_door()
            return render_template('control_doorLock.html', device_name=device_name, message=message)
        else:
            return render_template('rooms.html', message=message)

@app.route('/control/RGBLight/change_color_blue')
def change_to_blue():
    if request.method == 'GET':
        message = hardware_routes.change_color_blue()
        return render_template('control_rgb.html', device_name='RGBLight', message=message)


@app.route('/control/RGBLight/change_color_red')
def change_to_red():
    if request.method == 'GET':
        message = hardware_routes.change_color_red()
        return render_template('control_rgb.html', device_name='RGBLight', message=message)


@app.route('/control/RGBLight/change_color_purple')
def change_to_putple():
    if request.method == 'GET':
        message = hardware_routes.change_color_purple()
        return render_template('control_rgb.html', device_name='RGBLight', message=message)


@app.route('/control/RGBLight/change_color_pink')
def change_to_pink():
    if request.method == 'GET':
        message = hardware_routes.change_color_pink()
        return render_template('control_rgb.html', device_name='RGBLight', message=message)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
