from flask import request, render_template, session, redirect, url_for


def has_session():
    if 'loggedin' in session and session['loggedin'] == True:
        return True
    return False


def controller_authenticate_user():
    if has_session():
        controller_logout()
        return redirect(url_for('view_authenticate_login'))
    # user does not have a session, so continue with authentication process
    msg = ''
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        from User.User_Model import db_get_user_by_username
        account = db_get_user_by_username(str(username))
        if account is None:
            msg = 'Incorrect username / password !'
        elif account.username == username and account.password == password:
            session['loggedin'] = True
            session['id'] = account.id
            session['username'] = account.username
            msg = 'Logged in successfully !'
            return render_template('index.html', msg=msg)
        else:
            msg = 'Something wrong with your information'
    return render_template('login.html', msg=msg)


def controller_logout():
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    return redirect(url_for('view_authenticate_login'))
