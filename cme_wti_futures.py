import requests
import json
import pandas as pd
import csv
import argparse


class PriceCurveExporter():
    def __init__(self):
        self.parser = argparse.ArgumentParser()
        self.parser.add_argument("-d", help="CME WTI futures trade date MM/DD/YYYY", type=str, required=True)
        self.parser.add_argument("-o", help="output file name (without extension)", type=str, required=True)
        self.args = self.parser.parse_args()
        self.json_data = None

    def load_raw_data(self):
        raw_data = "https://www.cmegroup.com/CmeWS/mvc/Settlements/Futures/Settlements/425/FUT?tradeDate=" + self.args.d
        url = raw_data
        response = requests.get(url)
        if response:
            self.json_data = json.loads(response.content)
        else:
            print("Error: No WTI futures data for trade date " + self.args.d)
        return

    def export_to_csv(self):
        if self.json_data:
            settlement_data = pd.DataFrame(self.json_data)
            settlements = [pd.DataFrame(settlement, index=[i]) for (i, settlement) in enumerate(settlement_data['settlements'])]
            monthly_price_data = pd.concat(settlements)
            monthly_price_data.to_csv(self.args.o + ".csv", quoting=csv.QUOTE_NONNUMERIC)
        return


if __name__ == "__main__":
    exporter = PriceCurveExporter()
    exporter.load_raw_data()
    exporter.export_to_csv()
