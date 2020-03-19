# -*- coding: utf-8 -*-

from imap_tools import MailBox, Q
import constants as cs
from bs4 import BeautifulSoup

def mail_connexion():
    mailbox = MailBox(cs.mail_server)
    mailbox.login(cs.mail_address, cs.mail_password, \
                  initial_folder = cs.mail_folder)
    return mailbox

def mail_parse_newswletter_text(msg):
    soup = BeautifulSoup(msg.html, 'html.parser')
    L = soup.find_all("div")
    txt = ""
    for l in L:
        if "border-style: solid" in l.attrs["style"]:
            txt += l.text
    if len(txt) > 0:
        return "```python\n" + txt + "```"
    return ""

def mail_get_newswletter_text(mailbox):
    for msg in mailbox.fetch(Q(seen=False)):
        if "[\U0001f40dPyTricks]" in msg.subject:
            return mail_parse_newswletter_text(msg)
    return ""