from operator import itemgetter
from itertools import groupby
import requests
from bs4 import BeautifulSoup


class DataValidation:
    
    @classmethod
    def check_for_na_space(cls, data, column):
        """
        This methods use to check for any N/A or spaces in the string field
        if so, returns 0 else it returns the field itself

        :param data: bs4.element.Tag
        :param column: int
        :return: int
        """
        if (data.find_all("td")[column].text.replace(",", "") == "N/A" or data.find_all("td")[column].text.isspace()):
            return 0
        else:
            return int(data.find_all("td")[column].text.replace(",", ""))

    @classmethod
    def check_for_zero_division_error(cls, data, *columns):
        """
        This method use `check_for_na_space` and finally check if
        ZeroDivisionError is occuring. If so return 0 else the result

        :param data: bs4.element.Tag
        :param columns: (int, int)
        :result: int
        """
        try:
            result = cls.check_for_na_space(data, columns[0]) / cls.check_for_na_space(data, columns[1])
        except ZeroDivisionError as err:
            return 0
        return result

def index_list_of_countries(_list, value):
    """
    This function helps to index the list of countries in a dictionary 
    by a specific country name
    """
    indexed_dict = {}
    for country_name, items in groupby(_list, key=itemgetter(value)):
        indexed_dict[country_name.lower()] = list(items)[0]
    
    return indexed_dict

def scrapper(country=None):
    url = "https://www.worldometers.info/coronavirus/"
    response = requests.get(url)

    soup = BeautifulSoup(response.content, features="html.parser")

    results = soup.find(id="main_table_countries_today")

    all_tr_styles = [
            tr_styles if (tr_styles.get("style")=="" or tr_styles.get("style")=="background-color:#F0F0F0" or tr_styles.get("style")=="background-color:#EAF7D5") else None for tr_styles in results.find_all("tr")
        ]

    # Filter all None elements
    all_tr_styles_none_filtered = list(filter(None, all_tr_styles))

    countries = [
        {
            "CountryName": data.find_all("td")[1].text,
            "TotalCases": DataValidation.check_for_na_space(data, 2),
            "ActiveCases": DataValidation.check_for_na_space(data, 8),
            "TotalDeaths": DataValidation.check_for_na_space(data, 4),
            "RecoveryRate": DataValidation.check_for_na_space(data, 6) / DataValidation.check_for_na_space(data, 2),
            "PercentageOfPopulationInfected": DataValidation.check_for_zero_division_error(data, 2, 14)
        } for data in all_tr_styles_none_filtered 
    ]




    if country is None:
        return countries
    else:
        return index_list_of_countries(countries, "CountryName").get(country, "Country not found")


class CountryNotFoundError(ValueError):
    pass
