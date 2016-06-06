#!/usr/bin/python

"""
    user management for AndreaBot
"""

# dictionary for Telegram chat IDs
address_book = {
    # FOP comm
    'Andrea'    : 113764188,    # FOP director
    'Shane'     : 89686519,     # oweek director
    'Deborah'   : 222836171,    # events director
    'Yantyng'   : 112279032,    # safety/FOP, black OGL

    # USC MC
    'Tham'      : 111665525,    # USC MC member

    # VOGLs
    'Darren'    : 53558212,     # black VOGL, admin
    'Chester'   : 110971462,    # blue VOGL
    'Samantha'  : 106888349,    # red VOGL
    'Khaiqing'  : 118410662,    # purple VOGL
    'Claire'    : 27374797,     # green VOGL
    'Jiahao'    : 68976391,     # orange VOGL

    # COGLs
    'Xinying'   : 104784604,    # black COGL
    'Changming' : 52917741,     # blue COGL
    'Natalya'   : 16335747,     # purple COGL
    'Bryan'     : 117396861,    # green COGL
    'Hongwei'   : 98195170,     # orange COGL
}

rev_book = {v: k for k, v in address_book.items()}

# user groups
global groups
groups = {
	'admins'	: ['Darren'],
	'vogls'	    : ['Darren', 'Jiahao', 'Claire', 'Khaiqing', 'Chester', 'Samantha'],
	'cogls'	    : ['Xinying', 'Changming', 'Natalya', 'Bryan', 'Hongwei'],
	'fopcomm'	: ['Andrea', 'Shane', 'Deborah', 'Yantyng', 'Tham'],
	'safety'	: ['Darren', 'Yantyng'],
}

def getAll():
    return list(set(getGroups(['vogls', 'cogls', 'fopcomm'])))

def getGroups(groupList):
    IDs = []
    for group in groupList:
        if group in groups:
            IDs += getIDs(groups.get(group))
    return IDs

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

##### all mailing_list users are stored here #####
#mailing_list = admins + vogls + cogls + fopcomm + safety + usc
#mailing_list = ['Darren', 'Andrea', 'Tham']
#mailing_list = []
mailing_list = getAll()
