#!/usr/bin/python

# Thank you to:
# http://stackoverflow.com/questions/13959750/python-urllib2-cookiejar-with-selenium
# http://www.voidspace.org.uk/python/articles/authentication.shtml
# http://www.voidspace.org.uk/python/articles/urllib2.shtml
# http://stackoverflow.com/questions/2954381/python-form-post-using-urllib2-also-question-on-saving-using-cookies
# http://stackoverflow.com/questions/13404670/getting-or-manipulating-all-cookies-in-selenium-webdriver
# http://stackoverflow.com/questions/7854077/using-a-session-cookie-from-selenium-in-urllib2
# http://stackoverflow.com/questions/15058462/how-to-save-and-load-cookies-using-python-selenium-webdriver
# http://stackoverflow.com/questions/3238925/python-urllib-urllib2-post

import sys
import urllib
import urllib2
import cookielib
import selenium.webdriver

def to_unicode(str_data):
    """
    Tries to decode as utf-8 first, then latin-1.  safe to call on unicode strings
    """
    if isinstance(str_data, str):
        try:
            return str_data.decode('utf-8')
        except Exception as e:
            return str_data.decode('latin-1')
    elif isinstance(str_data, unicode):
        return str_data

def to_unicode_if_string(s):
    if isinstance(s, basestring):
        return to_unicode(s)
    else:
        return s

def cookie_to_dict(cookie):
	'''Translate from a cookielib cookie to a dictionary compatible with
	Selenium WebDriver add_cookie()
	'''
	# As cookielib and Selenium WebDriver use different names for the cookie
	# attribute, need to map between the two. Key is the cookielib name,
	# value is the Selenium name.
	cookie_element_map = {
		'name': 'name',
		'value': 'value',
		'path': 'path',
		'secure': 'secure',
		'expires': 'expiry'
	}
	cookie_dict = dict()

	# Based on observation of the WebDriver cookies, I think this is how the
	# cookielib cookie attributes should me mapped for the domain attribute
	# of a cookie.
	if getattr(cookie, 'domain_initial_dot'):
		cookie_dict[to_unicode('domain')] = to_unicode('.'+getattr(cookie, 'domain'))
	else:
		cookie_dict[to_unicode('domain')] = to_unicode(getattr(cookie, 'domain'))

	for k in cookie_element_map.keys():
		key = to_unicode_if_string(cookie_element_map[k])
		val = to_unicode_if_string(getattr(cookie, k))
		cookie_dict[key] = val

	return cookie_dict

def get_log_in_cookies():
	password_manager = urllib2.HTTPPasswordMgrWithDefaultRealm()
	password_manager.add_password(None, base_url, http_username, http_password)
	auth_handler = urllib2.HTTPBasicAuthHandler(password_manager)

	cookieJar = cookielib.CookieJar()
	opener = urllib2.build_opener(auth_handler, urllib2.HTTPCookieProcessor(cookieJar))

	# Get the initial session cookie
	request = urllib2.Request(base_url)
	response = opener.open(request)

	# send user information through form to log in
	login_data = urllib.urlencode(form_values)
	request = urllib2.Request(base_url + "ajax2/login/", login_data)
	response = opener.open(request)

	return cookieJar

def add_cookies_to_webdriver(driver):
	# WebDriver only allows setting cookies for a domain you are at, so navigate
	# there then set them. This may be a Firefox specific thing, or this may be a
	# Selenium thing, or maybe a settable, per-browser thing.
	driver.get(selenium_url)

	cookieJar = get_log_in_cookies()

	for cookie in cookieJar:
		driver.add_cookie(cookie_to_dict(cookie))
	# At this point, the log in cookies should be attached to the WebDriver
	# instance, and will cause the web server to believe we are logged in as
	# a result.
	driver.get(selenium_url)

selenium_url = ''
base_url = ''
http_username = ''
http_password = ''

form_values = {
	'email': 'test.monkey@sr.test',
	'password': 'abcd1234'
}

driver = selenium.webdriver.Firefox()
add_cookies_to_webdriver(driver)

import time
time.sleep(10)
driver.quit()
