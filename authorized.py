#!/usr/bin/python

import re
"""
    user management for AndreaBot
"""

# dictionary for Telegram chat IDs
address_book = {
    # FOP comm
    'Andrea'    : 113764188,    # FOP director
    'Yuchuan'   : 108571854,    # FOP vice-director
    'Cheryl'    : 216847462,    # rag director
    'Shane'     : 89686519,     # oweek director
    'Jileen'    : 120611059,    # ocamp director
    'Deborah'   : 222836171,    # events director
    'Haqeem'    : 176314759,    # logistics director
    'Edwin'     : 70230611,     # finance director
    'Yantyng'   : 112279032,    # safety/FOP, black OGL
    'Dexter'    : 58599435,     # safety IC for ocamp
    'Shao Yang' : 71671678,      # noob developer

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
    'Jingshun'  : 102888885,    # red COGL
}

rev_book = {v: k for k, v in address_book.items()}

# user groups
global groups
groups = {
<<<<<<< HEAD
    'admins'    : ['Darren'],
    'houses'     : ['Darren', 'Jiahao', 'Claire', 'Khaiqing', 'Chester', 'Samantha', 'Xinying', 'Changming', 'Natalya', 'Bryan', 'Hongwei', 'Jingshun'],
    'vogls'     : ['Darren', 'Jiahao', 'Claire', 'Khaiqing', 'Chester', 'Samantha'],
    'cogls'     : ['Xinying', 'Changming', 'Natalya', 'Bryan', 'Hongwei', 'Jingshun'],
    'fopcomm'   : ['Andrea', 'Yuchuan', 'Shane', 'Jileen', 'Deborah', 'Haqeem', 'Edwin', 'Yantyng', 'Tham', 'Dexter', 'Cheryl'],
    'safety'    : ['Darren', 'Yantyng', 'Dexter', 'Khaiqing', 'Jiahao', 'Andrea', 'Yuchuan'],
    'test'      : ['Darren'],
}

"""
    returns a list of chat IDs of all listening to yells
"""
def getMailingList():
    return list(set(getGroups(['vogls', 'cogls', 'fopcomm', 'admins', 'safety'])))
<<<<<<< HEAD
    #return getIDs(['Darren'])
=======
>>>>>>> master

"""
    returns a list of chat IDs from a list of groups
"""
def getGroups(groupList):
    lists = [getIDs(groups.get(group)) for group in groupList if group in groups]
    return [item for sublist in lists for item in sublist]


"""
    get the IDs of a list of people's names
"""
def getIDs(people):
    return [address_book.get(person) for person in people if person in address_book]

"""
    map a chat ID to a name if possible
"""
def whoIs(target_id):
    if target_id in rev_book:
        return rev_book.get(target_id)
    else:
        return target_id

"""
    enumerates all names inside address_book
    for /who command
"""
def enumerateListeners():
    reply = 'The following people are listening to yells:\n'
    i = 1

    # get a list of yell listeners
    for listening_id in getMailingList():
        reply += '%d. %-14s' % (i, whoIs(listening_id))
        i += 1
        if (i+1) % 2 == 0:
            reply += '\n'

    # get group lists
    reply += '\n-------- Group Lists --------\n'
    for group in ['houses', 'fopcomm', 'safety', 'cogls', 'vogls', 'admins']:
        reply += 'Group \'%s\'\n' % group

        # the groups dictionary is maintained in the authorized module
        # we build the reply using the group key-value in the groups dictionary
        # only build up to second last element then append last element to get rid of trailing comma
        for group_member in groups.get(group)[:-1]:
            reply += '%s, ' % group_member
        reply += '%s' % groups.get(group)[-1] # append last member
        reply += '\n\n'

    return reply

def groupIsValid(group_list):
    for group in group_list:
        if group not in groups:
            return False
    return True
