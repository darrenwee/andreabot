#!/usr/bin/python

"""
    user management for AndreaBot
"""

# dictionary for Telegram chat IDs
address_book = {
    'Darren'    : 53558212,     # black VOGL, admin
    'Yantyng'   : 112279032,    # safety/FOP, black OGL
    'Chester'   : 110971462,    # blue VOGL
    'Samantha'  : 106888349,    # red VOGL
    'Khaiqing'  : 118410662,    # purple VOGL
    'Claire'    : 27374797,     # green VOGL
    'Jiahao'    : 68976391,     # orange VOGL
}

rev_book = {v: k for k, v in address_book.items()}

# user groups
admins = ['Darren']
vogls = ['Darren', 'Jiahao', 'Claire', 'Khaiqing', 'Chester', 'Samantha']
cogls = []
fopcomm = ['Yantyng']
safety = ['Darren', 'Yantyng']

##### all mailing_list users are stored here #####
#mailing_list = admins + vogls + cogls + fopcomm + safety
mailing_list = ['Darren']
#mailing_list = []
mailing_list = list(set(mailing_list)) # get rid of duplicates

def getIDs(group):
    IDs = []
    for person in group:
        if person in address_book:
            IDs.append(address_book.get(person))
    return IDs

def whoIs(target_id):
    if target_id in rev_book:
        return rev_book.get(target_id)
    else:
        return target_id
