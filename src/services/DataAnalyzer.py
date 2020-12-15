
from models.Spam import Spam
from models.Users import Users
from models.GlobalDB import GlobalDB
from models import db

def update_spam_likelihood():
    """
        This is function that will execute once a day to analyze the data
        and update spam_likelihood of entries in database
    """
    spams = Spam.query.filter_by().all()
    users = Users.query.filter_by().all()
    user_count = len([user.serialize for user in users])
    
    result = [spam.serialize for spam in spams]
    
    #make set of all spams and maintain their count
    spam_set = { }
    number_set = []
    for spam in result:
        if spam['number'] not in spam_set:
            spam_set[str(spam['number'])] = 1
            number_set.append(str(spam['number']))
        else:
            spam_set[str(spam['number'])] = spam_set[str(spam['number'])] + 1

    #calculate the percentage of being a spam based on total users and update the data
    for number in number_set:
        if spam_set[str(number)] != 0:
            spam_set[str(number)] = float(spam_set[str(number)] / user_count ) * 100
    
    #update values in Globaldb
    for number in number_set:
        globaldb = GlobalDB.query.filter_by(phone_number = number).all()
        if globaldb is not None:
            for i in globaldb:
                i.spam_likelihood = spam_set.get(number)
                db.session.commit()

