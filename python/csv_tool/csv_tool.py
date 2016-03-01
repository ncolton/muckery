#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os.path
import string
import csv


def normalize_filepath(filepath):
    return os.path.abspath(os.path.expandvars(os.path.expanduser(filepath)))

def get_first_line(filepath):
    with open(normalize_filepath(filepath)) as f:
        return f.readline()

def map_character_frequency(s):
    character_frequency = {}
    for c in s:
        character = c.lower()
        if character not in character_frequency:
            character_frequency[character] = 0
        character_frequency[character] += 1
    return character_frequency

def discard_letters_and_digits(d):
    new_d = {}
    for k, v in d.iteritems():
        if k in string.letters:
            continue
        if k in string.digits:
            continue
        new_d[k] = v
    # keys_to_keep = itertools.dropwhile(lambda x: x in string.letters or x in string.digits, d.keys())
    return new_d

def suspects_by_occurence(d):
    suspects = {}
    for character, count in d.iteritems():
        if count not in suspects:
            suspects[count] = []
        suspects[count].append(character)
    return suspects

def invert_dictionary(d):
    """inverts single level dictionary, making a list of keys for each of the values"""
    inverted = {}
    for k, v in d.iteritems():
        if v not in inverted:
            inverted[v] = []
        inverted[v].append(k)
    return inverted

def suspects_by_likelyhood(filepath):
    line = get_first_line(normalize_filepath(filepath))
    suspects = discard_letters_and_digits(map_character_frequency(line))
    suspects_by_likelyhood = []
    occurence_to_suspects = invert_dictionary(suspects)
    for key in reversed(occurence_to_suspects.keys()):
        suspects_by_likelyhood.extend(occurence_to_suspects[key])
    return suspects_by_likelyhood

def do_the_thing(filepath):
    print "Suspects in order of likelyhood: %s" % suspects_by_likelyhood(filepath)

def headers_with_sample(filepath, separator):
    with open(normalize_filepath(filepath)) as csvfile:
        reader = csv.DictReader(csvfile, delimiter=separator)
        data = reader.next()

    max_key_width = max(map(len, data.keys()))
    max_value_width = 100
    for key in sorted(data.keys()):
        value = data[key]
        if len(value) > max_value_width:
            value = value[:max_value_width - 1] + '…'
        print '{key:>{key_width}}   {value:<{value_width}}'.format(key=key, value=value, key_width=max_key_width, value_width=max_value_width)

# Will want to be able to select a field and view the full text of it (especially for URL type things)
#   Maybe an option to open in default browser?
# Will want to have the list of headers that need assigning
#   will want to be able to map them in the UI

###
# The stuff actually needed for getting a product in
# or, in some cases, optional but good to map anyways.
#
# # self.header_map['thing in feed'] = 'thing we need'
# self.header_map['productid'] = 'product_id'  # Parent SKU
# self.header_map['Brand'] = 'brand_manufacturer'
# self.header_map['Description'] = 'product_description'
# self.filler['department'] = ''  # Feed provides no department, and can't process w/o this info
# self.header_map['categoryname'] = 'category'  # 'category_mapping'
# self.header_map['mfgsku'] = 'sku'
# self.header_map['modelname'] = 'title'  # 'product_name'
# self.filler['eligible'] = True  # ShopRunner eligible
# self.header_map['link'] = 'product_url'
# # mobile_url
# self.header_map['imagelink'] = 'image_url'  # 'product_image_url_main'
# self.header_map['additionalimagelinks'] = 'product_image_url_additional'
# self.header_map['price'] = 'regular_price'
# self.header_map['saleprice'] = 'sale_price'
# self.header_map['stocklevel'] = 'quantity'
# self.header_map['colorname'] = 'color'  # 'product_color'
# self.header_map['sizename'] = 'size'
# self.filler['attributes'] = ''  # other_attributes
# # self.header_map['upc'] = 'upc'  # no need to map as it works already
# # ean
# # mpn
# # isbn
# # age_range
# self.header_map['condition'] = 'product_condition'
# self.header_map['isadult'] = 'adult'

# filename = '~/repositories/1-JCTR_Shoprunner_Product_201602230220.txt'
filename = '~/repositories/JCTR_Shoprunner_Product_201603010237.txt'
