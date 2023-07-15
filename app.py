from flask import *
from flask_mysqldb import MySQL
from wtforms import Form, StringField, TextAreaField, PasswordField, validators, SelectField
import random
from wtforms import Form, StringField, TextAreaField, PasswordField, validators, SelectField
import random
from functools import wraps
from datetime import datetime, timedelta
from key import secret_key,salt
from itsdangerous import URLSafeTimedSerializer
from stoken import token
from cmail import sendmail
from key import *
app = Flask(__name__)
app.secret_key=secret_key

app.config['SESSION_TYPE']='filesystem'
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'root'
app.config['MYSQL_DB'] = 'bloodbank'
mysql = MySQL(app)

@app.route('/')
def index():
    return render_template('home.html')


@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        bgroup = request.form["bgroup"]
        bpackets = request.form["bpackets"]
        fname = request.form["fname"]
        address = request.form["adress"]

        cur = mysql.connection.cursor()

        cur.execute("INSERT INTO CONTACT(B_GROUP, C_PACKETS, F_NAME, ADRESS) VALUES (%s, %s, %s, %s)",(bgroup, bpackets, fname, address))

        mysql.connection.commit()

        contact_id = cur.lastrowid  # Get the last inserted contact ID

        cur.execute("INSERT INTO NOTIFICATIONS(CONTACT_ID, NB_GROUP, N_PACKETS, NF_NAME, NADRESS) VALUES (%s, %s, %s, %s, %s)",
                    (contact_id, bgroup, bpackets, fname, address))

        mysql.connection.commit()

        cur.close()

        flash('Your request has been successfully sent to the Blood Bank', 'success')
        return redirect(url_for('index'))

    return render_template('contact.html')



class RegisterForm(Form):
    name = StringField('Name', [validators.DataRequired(),validators.Length(min=1,max=25)])
    email = StringField('Email',[validators.DataRequired(),validators.Length(min=10,max=50)])
    password = PasswordField('Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm',message='Password do not match')
    ])
    confirm = PasswordField('Confirm Password')

@app.route('/register', methods=['GET','POST'])
def register():
    # form = RegisterForm(request.form)
    if request.method  == 'POST':
        name = request.form['name']
        email = request.form['email']
        #pwd = request.form['password']
        password = request.form['password']
        #e_id = name+str(random.randint(1111,9999))
        e_id=request.form['e_id']
        cursor = mysql.connection.cursor()
        cursor.execute('select count(*) from RECEPTION where name=%s',[name])
        count=cursor.fetchone()[0]
        cursor.execute('select count(*) from RECEPTION where email=%s',[email])
        count1=cursor.fetchone()[0]
        cursor.close()
        if count==1:
            flash('username already in use')
            return render_template('register.html')
        elif count1==1:
            flash('Email already in use')
            return render_template('register.html')
        data={'name':name,'password':password,'email':email,'e_id':e_id}
        subject='Email Confirmation'
        body=f"Thanks for signing up\n\nfollow this link for further steps-{url_for('confirm',token=token(data,salt),_external=True)}"
        sendmail(to=email,subject=subject,body=body)
        flash('Confirmation link sent to mail')
        return redirect(url_for('login'))
    return render_template('register.html')
    '''cur.execute("INSERT INTO RECEPTION(E_ID,NAME,EMAIL,PASSWORD) VALUES(%s, %s, %s, %s)",(e_id, name, email, password))
    mysql.connection.commit()
    cur.close()
    flashing_message = "Success! You can log in with Employee ID " + str(e_id)
    flash( flashing_message,"success")

    return redirect(url_for('login'))

return render_template('register.html',form = form)'''

@app.route('/confirm/<token>')
def confirm(token):
    try:
        serializer=URLSafeTimedSerializer(secret_key)
        data=serializer.loads(token,salt=salt,max_age=180)
    except Exception as e:
        #print(e)
        return 'Link Expired register again'
    else:
        cursor=mysql.connection.cursor()
        name=data['name']
        cursor.execute('select count(*) from RECEPTION where name=%s',[name])
        count=cursor.fetchone()[0]
        if count==1:
            cursor.close()
            flash('You are already registerterd!')
            return redirect(url_for('login'))
        else:
            cursor.execute('insert into RECEPTION(E_ID,NAME,EMAIL,PASSWORD) values(%s,%s,%s,%s)',[data['e_id'],data['name'],data['email'],data['password']])
            mysql.connection.commit()
            cursor.close()
            flash('Details registered!')
            return redirect(url_for('login'))
        
@app.route('/forgot',methods=['GET','POST'])
def forgot():
    if request.method=='POST':
        email=request.form['email']
        cursor=mysql.connection.cursor()
        cursor.execute('select count(*) from reception where email=%s',[email])
        count=cursor.fetchone()
        cursor.close()
        count = count[0]
        if count==1:
            cursor=mysql.connection.cursor()
            cursor.execute('SELECT email from reception where email=%s',[email])
            status=cursor.fetchone()
            cursor.close()
            subject='Forget Password'
            confirm_link=url_for('reset',token=token(email,salt=salt2),_external=True)
            body=f"Use this link to reset your password-\n\n{confirm_link}"
            sendmail(to=email,body=body,subject=subject)
            flash('Reset link sent check your email')
            return redirect(url_for('login'))
        else:
            flash('Invalid email id')
            return render_template('forgot.html')
    return render_template('forgot.html')


@app.route('/reset/<token>',methods=['GET','POST'])
def reset(token):
    try:
        serializer=URLSafeTimedSerializer(secret_key)
        email=serializer.loads(token,salt=salt2,max_age=180)
    except:
        abort(404,'Link Expired')
    else:
        if request.method=='POST':
            newpassword=request.form['npassword']
            confirmpassword=request.form['cpassword']
            if newpassword==confirmpassword:
                cursor=mysql.connection.cursor()
                cursor.execute('update reception set password=%s where email=%s',[newpassword,email])
                mysql.connection.commit()
                flash('Reset Successful')
                return redirect(url_for('login'))
            else:
                flash('Passwords mismatched')
                return render_template('newpassword.html')
        return render_template('newpassword.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        e_id = request.form["e_id"]
        password = request.form["password"]

        cur = mysql.connection.cursor()

        result=cur.execute("SELECT * FROM RECEPTION WHERE E_ID = %s ", [e_id])
    
        if result > 0:
            data = cur.fetchone()
            print(data)
            password1 = data[3]

        if(password, password1):
            session['logged_in'] = True
            session['e_id'] = e_id

            flash('You are now logged in', 'success')
            return redirect(url_for('dashboard'))
        else:
            error = 'Invalid login'
            return render_template('login.html', error=error)
        cur.close()
    else:
        error = 'Employee ID not found'
        return render_template('login.html', error=error)

    return render_template('login.html')

def is_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('Unauthorized, Please login!', 'danger')
            return redirect(url_for('login'))
    return wrap

@app.route('/logout')
@is_logged_in
def logout():
    session.clear()
    flash('You are now logged out', 'success')
    return redirect(url_for('index'))
@app.route('/dashboard')
@is_logged_in
def dashboard():
    cur = mysql.connection.cursor()

    cur.execute("SELECT B_GROUP, SUM(TOTAL_PACKETS) AS TOTAL_PACKETS FROM BLOODBANK GROUP BY B_GROUP")
    result = cur.fetchall()
    cur.close()

    integer_values = [int(value) for _, value in result]
    print(integer_values)

    if all(value == 0 for value in integer_values):
        flash('Insufficient blood')

    if 0 < len(result) > 0:
        return render_template('dashboard.html', details=result)
    else:
        msg = 'Blood Bank is Empty'
        return render_template('dashboard.html', msg=msg)


@app.route('/bloodrequest', methods=['POST'])
@is_logged_in
def bloodrequest():
    blood_group = request.form['blood_group']
    packets = int(request.form['packets'])

    cur = mysql.connection.cursor()

    cur.execute("SELECT TOTAL_PACKETS FROM BLOODBANK WHERE B_GROUP = %s", (blood_group,))
    blood_group_packets = cur.fetchone()

    if blood_group_packets and blood_group_packets['TOTAL_PACKETS'] > 0:
        if packets <= blood_group_packets['TOTAL_PACKETS']:
            cur.execute("UPDATE BLOODBANK SET TOTAL_PACKETS = TOTAL_PACKETS - %s WHERE B_GROUP = %s",
                        (packets, blood_group))
            mysql.connection.commit()
            cur.close()
            flash('Blood request accepted.', 'success')
        else:
            flash('Insufficient blood packets available for the requested blood group.', 'danger')
    else:
        flash('Blood packets not available for the requested blood group.', 'danger')

    return redirect(url_for('dashboard'))




from datetime import datetime, timedelta

@app.route('/donate', methods=['GET', 'POST'])
@is_logged_in
def donate():
    if request.method == 'POST':
        dname = request.form["dname"]
        sex = request.form["sex"]
        age = request.form["age"]
        weight = request.form["weight"]
        address = request.form["address"]
        disease = request.form["disease"]
        demail = request.form["demail"]
        mobile=request.form["mobile"]

        if disease == 'No':
            cur = mysql.connection.cursor()
            
            six_months_ago = datetime.now() - timedelta(days=180)
            cur.execute("SELECT DONOR_DATE FROM DONOR WHERE DNAME = %s ORDER BY DONOR_DATE DESC LIMIT 1", (dname,))
            last_donation_date = cur.fetchone()

            if last_donation_date and last_donation_date['DONOR_DATE'] >= six_months_ago:
                flash('This donor has already donated blood within the last 6 months.', 'danger')
                cur.close()
                return redirect(url_for('donate'))

            cur.execute(
                "INSERT INTO DONOR(DNAME, SEX, AGE, WEIGHT, ADDRESS, DISEASE, DEMAIL,mobile_no) VALUES(%s, %s, %s, %s, %s, %s, %s,%s)",
                (dname, sex, age, weight, address, disease, demail, mobile))

            mysql.connection.commit()
            cur.close()

            flash('Success! Donor details added.', 'success')
            return redirect(url_for('donorlogs'))
        else:
            flash('Donors with diseases are not eligible to donate.', 'danger')
            return redirect(url_for('donate'))

    return render_template('donate.html')


@app.route('/donorlogs')
@is_logged_in
def donorlogs():
    cur = mysql.connection.cursor()
    result = cur.execute("SELECT * FROM DONOR")
    logs = cur.fetchall()

    if result>0:
        return render_template('donorlogs.html',logs=logs)
    else:
        msg = ' No logs found '
        return render_template('donorlogs.html',msg=msg)
    
    cur.close()


@app.route('/bloodform', methods=['GET', 'POST'])
@is_logged_in
def bloodform():
    if request.method == 'POST':
        d_id = request.form["d_id"]
        blood_group = request.form["blood_group"]
        packets = request.form["packets"]

        cur = mysql.connection.cursor()

        cur.execute("SELECT * FROM BLOODBANK WHERE B_GROUP = %s", (blood_group,))
        bloodbank_record = cur.fetchone()

        if bloodbank_record:
            cur.execute("INSERT INTO BLOOD(D_ID, B_GROUP, PACKETS) VALUES(%s, %s, %s)", (d_id, blood_group, packets))

            cur.execute("UPDATE BLOODBANK SET TOTAL_PACKETS = TOTAL_PACKETS + %s WHERE B_GROUP = %s", (packets, blood_group))

            mysql.connection.commit()

            cur.close()

            flash('Success! Donor Blood details added.', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Blood group does not exist in the blood bank.', 'danger')

    return render_template('bloodform.html')


@app.route('/notifications', methods=['GET', 'POST'])
@is_logged_in
def notifications():
    cur = mysql.connection.cursor()
    result = cur.execute("SELECT N.N_ID, N.NB_GROUP, N.N_PACKETS, C.CONTACT_ID, C.F_NAME, C.ADRESS FROM NOTIFICATIONS N JOIN CONTACT C ON N.NF_NAME = C.F_NAME AND N.NADRESS = C.ADRESS")
    requests = cur.fetchall()
    #print(requests[0])

    if result > 0:
        return render_template('notification.html', requests=requests)
    else:
        msg = 'No requests found'
        return render_template('notification.html', msg=msg)

    cur.close()




@app.route('/notifications/accept/<int:notification_id>')
@is_logged_in
def accept(notification_id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT NB_GROUP, N_PACKETS, N_ID FROM NOTIFICATIONS WHERE N_ID = %s", [notification_id])
    notification = cur.fetchone()
    if notification:
        blood_group = notification[0]
        packets = notification[1]
        status = 'Accepted'

        cur.execute("SELECT TOTAL_PACKETS FROM BLOODBANK WHERE B_GROUP = %s", [blood_group])
        total_packets = cur.fetchone()[0]

        if packets <= total_packets:
            cur.execute("UPDATE BLOODBANK SET TOTAL_PACKETS = TOTAL_PACKETS - %s WHERE B_GROUP = %s",(packets, blood_group))
            cur.execute("DELETE FROM notifications WHERE N_ID = %s", [notification_id])
            mysql.connection.commit()
            flash('Request Accepted', 'success')
        else:
            flash('Insufficient blood', 'danger')

    cur.close()
    return redirect(url_for('notifications'))

@app.route('/notifications/decline/<int:notification_id>')
@is_logged_in
def decline(notification_id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT NB_GROUP, N_PACKETS FROM NOTIFICATIONS WHERE N_ID = %s", (notification_id,))
    notification = cur.fetchone()
    print(notification)
    if notification:
        blood_group = notification[0]
        packets = notification[1]
        status = 'Declined'

        cur.execute("UPDATE BLOODBANK SET TOTAL_PACKETS = TOTAL_PACKETS WHERE B_GROUP = %s",
                    (packets, blood_group))

        cur.execute("DELETE FROM NOTIFICATIONS WHERE N_ID = %s", (notification_id,))

        mysql.connection.commit()

        flash('Request Declined', 'danger')
    else:
        flash('Notification not found', 'danger')

    cur.close()

    return redirect(url_for('notifications'))

if __name__ == '__main__':
    app.run(debug=True)
