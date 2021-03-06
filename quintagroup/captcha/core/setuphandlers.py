from random import randint

from Products.CMFCore.utils import getToolByName

from quintagroup.captcha.core.config import CAPTCHA_KEY, CONFIGLET_ID, \
    PROPERTY_SHEET


def generateKey(length):
    key = ''
    for i in range(length):
        key += str(randint(0, 9))
    return key


def setupVarious(context):
    if context.readDataFile('quintagroup.captcha.core_various.txt') is None:
        return

    site = context.getSite()

    # set captcha key
    value = generateKey(8)
    if site.hasProperty(CAPTCHA_KEY):
        site._updateProperty(CAPTCHA_KEY, value)
    else:
        site._setProperty(CAPTCHA_KEY, value, 'string')


def uninstall(context):
    # Only run step if a flag file is present (e.g. not an extension profile)
    if context.readDataFile('quintagroup.captcha.core_uninstall.txt') is None:
        return

    site = context.getSite()

    # remove configlet
    cpt = getToolByName(site, 'portal_controlpanel')
    if CONFIGLET_ID in [o.id for o in cpt.listActions()]:
        cpt.unregisterConfiglet(CONFIGLET_ID)

    # remove property sheet
    pp = getToolByName(site, 'portal_properties')
    if PROPERTY_SHEET in pp.objectIds():
        pp.manage_delObjects(ids=[PROPERTY_SHEET])

    # remove captcha key property
    if site.hasProperty(CAPTCHA_KEY):
        site._delProperty(CAPTCHA_KEY)


def add_honeypot_property(context):
    pp = getToolByName(context, 'portal_properties')
    if PROPERTY_SHEET in pp.objectIds() and not pp[PROPERTY_SHEET].hasProperty("honeypot"):
        pp[PROPERTY_SHEET].manage_addProperty("honeypot", False, 'boolean')
