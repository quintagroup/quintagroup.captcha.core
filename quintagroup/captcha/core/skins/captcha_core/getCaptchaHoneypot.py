## Script (Python) "getCaptchaHoneypot"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=
##title=
from quintagroup.captcha.core.utils import getCaptchasCount, getRandIndex, formKey, encrypt, encrypt_token, obfuscate_code

ctype = context.getCaptchaType()
index = getRandIndex(ctype == 'dynamic')
key = formKey(index)
encrypted_key = encrypt(context.captcha_key, key)
token = encrypt_token(context.captcha_key, encrypted_key, index)
token = obfuscate_code(encrypted_key, token)

return {'hashkey': encrypted_key, 'token': token}
