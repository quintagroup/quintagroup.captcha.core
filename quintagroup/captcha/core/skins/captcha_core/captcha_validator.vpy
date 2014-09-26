from DateTime import DateTime
from Products.CMFCore.utils import getToolByName
from quintagroup.captcha.core import ProductMessageFactory as _
from quintagroup.captcha.core.utils import decrypt, parseKey, validate_key, validate_token

def set_error():
    message = _(u"Please re-enter validation code.")
    context.plone_utils.addPortalMessage(message, 'error')
    state.setError('key', message, 'key_required')
    return state.set(status="failure")

if state.getStatus()=='failure':
    return  state
request = context.REQUEST

test_key = request.get('key', '')
hashkey = request.get('hashkey', '')
tokenkey = request.get('tokenkey', '')
try:
    decrypted_key = decrypt(context.captcha_key, hashkey)
except:
    return set_error()
captcha_tool = getToolByName(context, 'portal_captchas')
if captcha_tool.has_key(decrypted_key):
    return set_error()
parsed_key = parseKey(decrypted_key)

index = parsed_key['key']
date = parsed_key['date']
if (DateTime().timeTime() - float(date)) > 3600:
    return set_error()

ctype = context.getCaptchaType()
try:
    failed = validate_key(context, test_key, index, ctype == 'dynamic')
except AttributeError:
    return set_error()

honeypotEnabled = context.portal_properties.qPloneCaptchas.getProperty('honeypot', False)
if honeypotEnabled and failed and tokenkey:
    try:
        failed = validate_token(context.captcha_key, hashkey, index, tokenkey)
    except ValueError:
        return set_error()

if failed:
    return set_error()

captcha_tool.addExpiredKey(decrypted_key)
return state.set(status="success")
