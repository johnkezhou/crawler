#xpath
xpath={
'shop_list': '//*[@id:"shop-all-list"]/ul//li',
'ding': '',
'shop_level': '//div[2]/div[2]/span/@title',
'city_id': '',
'main_category_name': '//div[2]/div[3]/a[1]/span/text()',
'address': '//div[2]/div[3]/span/text()',
'avgcost': '//div[2]/div[2]/a[2]/b/text()',
'shop_id': '',
'shop_power': '',
'shop_group_id': '',
'full_name': '',
'food_type': '//div[2]/div[3]/a[1]/span/text()',
'cu': '',
'taste_score': '//div[2]/span/span[1]/b/text()',
'shop_url': '//div[2]/div[1]/a[1]/@href',
'comment_number': '//div[2]/div[2]/a[1]/b/text()',
'main_category_id': '',
'shop_name': '//div[2]/div[1]/a[1]/h4/text()',
'shop_glat': '',
'location': '//div[2]/div[3]/a[2]/span/text()',
'power': '',
'shop_glng': '',
'huo': '',
'phone': '',
'shop_type': '',
'service_score': '//div[2]/span/span[3]/b/text()',
'city_name': '',
'shop_logo': '//div[1]/a/img/@data-src',
'tuan': '',
'wai': '',
'environment_score': '//div[2]/span/span[2]/b/text()'}
from xml.etree.ElementTree import Element, tostring, parse
def dict_to_xml(tag, dt):
    element = Element(tag)
    for key, value in dt.items():
        child = Element(key)
        child.text = str(value)
        element.append(child)
    return element

e = dict_to_xml('xpath', xpath)
print tostring(e)
import xmltodict

tree = parse('../xpath.xml')
print tree
string = tostring(tree.getroot())
edt = xmltodict.parse(string)
print edt['shop_item'].keys()
