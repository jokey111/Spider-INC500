"""Extracting and Appending other company information to the json file"""

import scrapy
import json
from scrapy.selector import Selector
import logging
import time

output_companies = list()


class CompanySchema:
    company_schema = {
         "CompanyID": str()
        ,"Ranking": str()
        ,"CompanyName": str()
        ,"Industry": str()
        ,"Growth": str()
        ,"Revenue": str()
        ,"City": str()
        ,"StateAbbr": str()
        ,"StateName": str()
        ,"YearsOnINCList": str()
        ,"Partner": "None"

        ,"BriefDescription": str()
        ,"Description": str()
        ,"Leadership": str()
        ,"Founded": str()
        ,"ThreeYearGrowth": str()
        ,"Employees": str()
        ,"Website": str()
        ,"Location": str()

        ,"WikipediaPage": str()
        ,"WikipediaURL": str()
    }


class INC500_3:
    global output_companies

    """These xpath are used to extract data from the Company Profile Page"""
    xpath_brief_description = '//html/head/meta[1]/@content'
    xpath_description = '//*[@id="company70866"]/section[2]/div[2]/p/text()'
    xpath_leadership = '//*[@id="company70866"]/section[1]/div[2]/dl[2]/dd/text()'
    xpath_founded = '//*[@id="company70866"]/section[1]/div[3]/dl[5]/dd/text()'
    xpath_3_year_growth = '//*[@id="company70866"]/section[1]/div[3]/dl[2]/dd/text()'
    xpath_employees = '//*[@id="company70866"]/section[1]/div[3]/dl[6]/dd/text()'
    xpath_company_website = '//*[@id="company70866"]/section[5]/dl/dd/a/@href'
    xpath_location = '//html/head/title/text()'

    def __init__(self):
        f = open(file='temp/INC500_1.json', encoding='utf-8', mode='r')
        json_obj = json.loads(f.read())
        f.close()
        self.companies = json_obj

        f = open(file='temp/INC500_2.json', encoding='utf-8', mode='r')
        json_obj = json.loads(f.read())
        f.close()
        self.companies_info = json_obj

        logging.info("Output Companies Initialization Succeed")

    def start_extraction(self):
        """Initialize output companies according to the result of spider 1"""
        for company in self.companies:

            cs = CompanySchema()
            cs.company_schema['CompanyID'] = company['id']
            cs.company_schema['Ranking'] = company['rank']
            cs.company_schema['CompanyName'] = company['company']
            cs.company_schema['Industry'] = company['industry']
            cs.company_schema['Growth'] = company['growth']
            cs.company_schema['Revenue'] = company['revenue']
            cs.company_schema['City'] = company['city']
            cs.company_schema['StateAbbr'] = company['state_s']
            cs.company_schema['StateName'] = company['state_l']
            cs.company_schema['YearsOnINCList'] = company['yrs_on_list']
            for parterner in company['partner_lists']:
                cs.company_schema['Partner'] += parterner + " "

            for wikipedia_detail in self.companies_info['wikipedias']:
                if str(company['id']) == str(wikipedia_detail['company_id']):
                    cs.company_schema['WikipediaPage'] = company['url'] + '.html'
                    cs.company_schema['WikipediaURL'] = wikipedia_detail['wikipedia_url']

            for company_profile in self.companies_info['inc_500_company_details']:
                if str(company['id']) == str(company_profile['company_id']):
                    f = open(file=company_profile['file_path'], encoding='utf-8', mode='r')
                    html = f.read().decode('utf-8')
                    print(html)
                    f.close()

                    cs.company_schema['BriefDescription'] = Selector(text=html).xpath(self.xpath_brief_description).extract()[0]
                    cs.company_schema['Description'] = Selector(text=html).xpath(self.xpath_description).extract()[0]
                    cs.company_schema['Leadership'] = Selector(text=html).xpath(self.xpath_leadership).extract()[0]
                    cs.company_schema['Founded'] = Selector(text=html).xpath(self.xpath_founded).extract()[0]
                    cs.company_schema['ThreeYearGrowth'] = Selector(text=html).xpath(self.xpath_3_year_growth).extract()[0]
                    cs.company_schema['Employees'] = Selector(text=html).xpath(self.xpath_employees).extract()[0]
                    cs.company_schema['Website'] = Selector(text=html).xpath(self.xpath_company_website).extract()[0]
                    cs.company_schema['Location'] = Selector(text=html).xpath(self.xpath_location).extract()[0]

            output_companies.append(cs.company_schema)

            # For Debug purpose
            print(str(cs.company_schema['Ranking']) + "` " + "Finished information collecting stage")



        f = open(file='temp/INC500_3.json', encoding='utf-8', mode='w')
        f.write(json.dumps(output_companies))
        f.close()

if __name__ == '__main__':
    inc_500_3 = INC500_3()
    inc_500_3.start_extraction()