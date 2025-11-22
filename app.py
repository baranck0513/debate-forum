from flask import Flask
from flask import render_template
from flask import request, session
from flask import jsonify
import sqlite3
import time

app = Flask(__name__)
# app.secret_key =

# connecting database
def ConnectDatabase():
    con = sqlite3.connect('./debate.sqlite')
    con.row_factory = sqlite3.Row
    return con

# default topics for the home page
def defaultTopics():
    default_topics = ["Sports", "Food", "Computer Science", "Science", "UK"]
    con = ConnectDatabase()
    c = con.cursor()
    currentTime = int(time.time())

    for topic in default_topics:
        # if topic already exists
        c.execute("SELECT topicID FROM topic WHERE topicName = ?", (topic,))
        if not c.fetchone():    
            # insert the topic with a user id and current time
            c.execute("INSERT INTO topic (topicName, postingUser, creationTime, updateTime) VALUES (?, ?, ?, ?)", (topic, "The website added this topic by default", currentTime, currentTime))
    con.commit()
    con.close()

# home page
@app.route("/")
def home(): 
    defaultTopics()
    con = ConnectDatabase()
    c = con.cursor()

    username = session.get('username', None)

    c.execute("SELECT topicName FROM topic")
    allTopics = [row['topicName'] for row in c.fetchall()]

    con.close()

    return render_template("index.html", allTopics=allTopics, username=username)


# add a topic
@app.route('/add_topic', methods=['POST'])
def add_topic():
        con = ConnectDatabase()
        c = con.cursor()
        currentTime = int(time.time())

        topic_name = request.json.get('topic_name')

        username = session.get('username')

        if 'username' not in session:
            return jsonify({'success': False, 'message': 'You have to log in'})

        if not topic_name:
            return jsonify({'success': False, 'message': 'Topic name cannot be empty'})

        c.execute("SELECT topicID FROM topic WHERE topicName = ?", (topic_name,))
        if c.fetchone():
            con.close()
            return jsonify({'success': False, 'message': 'Topic already exists'})

        username = session['username']
        c.execute("SELECT userID FROM user WHERE userName = ?", (username,))
        user = c.fetchone()

        userID = user['userID']
        c.execute("INSERT INTO topic (topicName, postingUser, creationTime, updateTime) VALUES (?, ?, ?, ?)", (topic_name, userID, currentTime, currentTime))
        con.commit()
        con.close()
        return jsonify({'success': True, 'message': 'Topic added'})

# adding claim
@app.route('/add_claim', methods=['POST'])
def add_claim():
    con = ConnectDatabase()
    c = con.cursor()

    topic_name = request.json.get('topic_name')
    claim_text = request.json.get('claim_text')

    username = session.get('username', None)

    if 'username' not in session:
        return jsonify({'success': False, 'message': 'You have to log in'})

    if not claim_text or not topic_name:
        return jsonify({'success': False, 'message': 'Claim text cannot be empty'})

    # topic id
    c.execute("SELECT topicID FROM topic WHERE topicName = ?", (topic_name,))
    topic = c.fetchone()
    topic_id = topic['topicID']

    # user id
    username = session['username']
    c.execute("SELECT userID FROM user WHERE userName = ?", (username,))
    user = c.fetchone()
    if not user:
        con.close()
        return jsonify({'success': False, 'message': 'User not found'})
    user_id = user['userID']
    
    # adding claim into database
    creationTime = int(time.time())

    c.execute("INSERT INTO claim (topic, postingUser, creationTime, updateTime, text) VALUES (?, ?, ?, ?, ?)", (topic_id, user_id, creationTime, creationTime, claim_text))
    con.commit()
    con.close()
    return jsonify({'success': True, 'message': 'Claim added'})

# display claims for a specific topic
@app.route("/topics/claims/<topic_name>")
def claims(topic_name):
    con = ConnectDatabase()
    c = con.cursor()

    username = session.get('username', None)

    # retrieveing topic details
    c.execute("SELECT topic.topicID, topic.creationTime, u.userName AS username FROM topic LEFT JOIN user u ON topic.postingUser = u.userID WHERE topic.topicName = ?", (topic_name,))
    topic_details = c.fetchone()

    topic_id = topic_details['topicID']

    if topic_details['username']:
        topic_creator = topic_details['username']
    else:
        topic_creator = "The website added this topic by default"

    topic_creationTime = time.strftime('%d/%m/%Y - %H.%M', time.localtime(topic_details['creationTime']))

    # retrieveing claims for the topic
    c.execute("""
        SELECT claim.claimID AS id, claim.text, u.userName AS username, claim.creationTime
        FROM claim
        LEFT JOIN user u ON claim.postingUser = u.userID
        WHERE claim.topic = ?
        ORDER BY claim.creationTime DESC""", (topic_id,))
    claims = c.fetchall()

    con.close()
    return render_template("claims.html", topic_name=topic_name, claims=claims, username=username, topic_creator=topic_creator, topic_creationTime=topic_creationTime)



# claim form and retrieveing the replies
@app.route("/claim/<int:claim_id>")
def claim(claim_id):
    con = ConnectDatabase()
    c = con.cursor()

    username = session.get("username", None)

    # retrieveing claim details
    c.execute("""
        SELECT claim.claimID, claim.text, u.userName AS userName, claim.creationTime, topic.topicName
        FROM claim
        LEFT JOIN user u ON claim.postingUser = u.userID
        LEFT JOIN topic ON claim.topic = topic.topicID
        WHERE claim.claimID = ?""", (claim_id,))
    claim = c.fetchone()

    claim_text=claim['text']
    claim_username=claim['username']
    creationTime=claim['creationTime']
    claim_id=claim['claimID']
    topic_name=claim['topicName']
    
    # retrieving replies for the claim
    c.execute("""
        SELECT replyText.text, replyText.creationTime, user.userName AS username, replyToClaim.replyToClaimRelType
        FROM replyToClaim 
        JOIN replyText ON replyToClaim.reply = replyText.replyTextID
        LEFT JOIN user ON replyText.postingUser = user.userID
        WHERE replyToClaim.claim = ? """, (claim_id,))
    replies = c.fetchall()

    con.close()
    return render_template("displayClaim.html", claim_text=claim_text, creationTime=creationTime, claim_id=claim_id, topic_name=topic_name, claim_username=claim_username, replies=replies, username=username)


# submit reply into the database
@app.route('/add_reply', methods=['POST'])
def add_reply():
    con = ConnectDatabase()
    c = con.cursor()

    creationTime = int(time.time())
 
    reply_text = request.json.get('reply_text')
    reply_type = request.json.get('reply_type')
    claim_id = request.json.get('claim_id')

    replyTypeNumber = {
        "Clarification": 1,
        "Supporting Argument": 2,
        "Counter Argument": 3
    }
    replyTypeID = replyTypeNumber.get(reply_type)

    # retrieve user id
    username = session.get('username')
    if not username:
        return jsonify({'success': False, 'message': 'You have to log in'})
    
    c.execute("SELECT userID FROM user WHERE userName = ?", (username,))
    user = c.fetchone()

    if not user:
        return jsonify({'success': False, 'message': 'User not found'})
    
    user_id = user['userID']
    
    # inserting in the replyText
    c.execute("INSERT INTO replyText (postingUser, creationTime, text) VALUES (?, ?, ?) RETURNING replyTextID", (user_id, creationTime, reply_text))
    reply_text_id = c.fetchone()[0] # getting the id of a reply that is inserted

    # inserting in  the replyToClaim
    c.execute("INSERT INTO replyToClaim (reply, claim, replyToClaimRelType) VALUES (?, ?, ?)", (reply_text_id, claim_id, replyTypeID))

    con.commit()
    con.close()

    return jsonify({'success': True, 'message': 'Reply added'})

# add reply to reply
@app.route('/add_reply_to_reply', methods=['POST'])
def add_reply_to_reply():
    con = ConnectDatabase()
    c = con.cursor()

    creationTime = int(time.time())

    reply_to_reply_text = request.json.get('reply_to_reply_text')
    parent_reply_id = request.json.get('parent_reply_id') 
    reply_type = request.json.get('reply_type')

    username = session.get('username')

    #  reply type
    replyToReplyNumber = {
        "Evidence": 1,
        "Support": 2,
        "Rebuttal": 3
    }
    replyToReplyRelTypeID = replyToReplyNumber.get(reply_type)

    if not reply_to_reply_text:
        return jsonify({'success': False, 'message': 'Reply text cannot be empty'})
    
    if replyToReplyRelTypeID is None:
        return jsonify({'success': False, 'message': 'Invalid reply type selected'})

    if not username:
        return jsonify({'success': False, 'message': 'You have to log in'})

    c.execute("SELECT userID FROM user WHERE userName = ?", (username,))
    user = c.fetchone()
    if not user:
        return jsonify({'success': False, 'message': 'User not found'})

    user_id = user['userID']
    
    # inserting in the  replyText 
    c.execute("INSERT INTO replyText (postingUser, creationTime, text) VALUES (?, ?, ?) RETURNING replyTextID", (user_id, creationTime, reply_to_reply_text))
    reply_text_id = c.fetchone()[0] # getting the id of a reply that is inserted

    # insert in the replyToReply
    c.execute("INSERT INTO replyToReply (reply, parent, replyToReplyRelType) VALUES (?, ?, ?)", (reply_text_id, parent_reply_id, replyToReplyRelTypeID))

    con.commit()
    con.close()
    return jsonify({'success': True, 'message': 'Reply to reply added'})

# login
@app.route('/login', methods=['POST'])
def login():
    con = ConnectDatabase()
    c = con.cursor()

    username = request.json.get('username')
    password = request.json.get('password')

    if not username or not password:
        return jsonify({'success': False, 'message': 'You have to enter username and password'})

    c.execute("SELECT * FROM user WHERE userName = ? AND passwordHash = ?", (username, password))
    user = c.fetchone()
    con.close()

    if user:
        session['username'] = username
        session.permanent = True 
        return jsonify({'success': True, 'message': 'Login completed'})
    else:
        return jsonify({'success': False, 'message': 'Username and/or password is wrong'})

# sign up 
@app.route('/signup', methods=['POST'])
def signup():
    con = ConnectDatabase()
    c = con.cursor()

    username = request.json.get('username')
    password = request.json.get('password')

    if not username or not password:
        return jsonify({'success': False, 'message': 'You have to select a username and a password'})

    c.execute("SELECT * FROM user WHERE userName = ?", (username,))
    if c.fetchone():
        con.close()
        return jsonify({'success': False, 'message': 'This username is already used by someone'})

    c.execute("INSERT INTO user (userName, passwordHash, isAdmin, creationTime, lastVisit) VALUES (?, ?, ?, ?, ?)", (username, password, False, int(time.time()), int(time.time())))
    con.commit()
    con.close()
    return jsonify({'success': True, 'message': 'Sign up completed'})

# logout
@app.route('/logout', methods=["POST"])
def logout():
    session.clear()
    return jsonify({'success': True, 'message': 'Logged out'})


# checking user session to display forms(add topic, add claim, add reply) 
@app.route('/checkLogin', methods=['POST'])
def checkLogin():
    if 'username' in session:
        return jsonify({'logged_in': True})
    return jsonify({'logged_in': False})



if __name__ == "__main__":
    app.run(debug=True)