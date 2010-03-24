import re, string
from base import *

class TestConfiglet(ptc.FunctionalTestCase):

    def afterSetUp(self):
        self.sp = self.portal.portal_properties.site_properties
        self.basic_auth = ':'.join((portal_owner,default_password))
        self.loginAsPortalOwner()
        self.addProduct(PRODUCT_NAME)
        
        self.capprops = self.portal.portal_properties[PROPERTY_SHEET]
        self.save_url = self.portal.id + \
            '/prefs_captchas_setup_form?form.submitted=1' + \
            '&form.button.form_submit=Save'

    def layerInSkins(self, layer):
        res = False
        skins = self.portal.portal_skins
        for skin in skins.getSkinSelections():
            path = skins.getSkinPath(skin)
            path = map( string.strip, string.split( path,',' ))
            if not layer in path:
                return False

        return True

    def test_staticOn(self):
        self.publish(self.save_url + '&static_captchas=static',
                     self.basic_auth)
        
        self.assertTrue(self.layerInSkins(LAYER_STATIC_CAPTCHAS),
            "No '%s' skin layer in some skins" % LAYER_STATIC_CAPTCHAS)

    def test_dynamicOn(self):
        res = self.publish(self.save_url + '&static_captchas=dynamic',
                     self.basic_auth).getBody()
        
        open('/tmp/captcha.configlet.html','w').write(res)
        self.assertTrue(self.layerInSkins(LAYER_DYNAMIC_CAPTCHAS),
            "No '%s' skin layer in some skins" % LAYER_DYNAMIC_CAPTCHAS)

    def test_imageSize(self):
        expect = 35
        self.publish(self.save_url + '&image_size=%s' % expect,
             self.basic_auth)

        imsize = self.capprops.getProperty("image_size", 0)
        self.assertTrue(imsize == expect, '"image_size" property ' \
            'contains: "%s", must: "%s"' % (imsize, expect))

    def test_background(self):
        prop, expect = "background", "test-color"
        self.publish(self.save_url + '&%s=%s' % (prop, expect),
             self.basic_auth)

        fact = self.capprops.getProperty(prop, "")
        self.assertTrue(fact == expect, '"%s" property ' \
            'contains: "%s", must: "%s"' % (prop, fact, expect))

    def test_fontColor(self):
        prop, expect = "font_color", "test-font-color"
        self.publish(self.save_url + '&%s=%s' % (prop, expect),
             self.basic_auth)

        fact = self.capprops.getProperty(prop, "")
        self.assertTrue(fact == expect, '"%s" property ' \
            'contains: "%s", must: "%s"' % (prop, fact, expect))

    def test_period(self):
        prop, expect = "period", 22.3
        self.publish(self.save_url + '&%s=%s' % (prop, expect),
             self.basic_auth)

        fact = self.capprops.getProperty(prop, 0)
        self.assertTrue(fact == expect, '"%s" property ' \
            'contains: "%s", must: "%s"' % (prop, fact, expect))

    def test_amplitude(self):
        prop, expect = "amplitude", 11.2
        self.publish(self.save_url + '&%s=%s' % (prop, expect),
             self.basic_auth)

        fact = self.capprops.getProperty(prop, 0)
        self.assertTrue(fact == expect, '"%s" property ' \
            'contains: "%s", must: "%s"' % (prop, fact, expect))

    def test_random(self):
        prop, expect = "random_params", False
        self.publish(self.save_url, self.basic_auth)

        fact = self.capprops.getProperty(prop, None)
        self.assertTrue(fact == expect, '"%s" property ' \
            'contains: "%s", must: "%s"' % (prop, fact, expect))


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestConfiglet))
    return suite