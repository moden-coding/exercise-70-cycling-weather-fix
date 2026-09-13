#!/usr/bin/env python3

import unittest
from unittest.mock import patch

import pandas as pd

from src.cycling_weather import cycling_weather, main


class TestCyclingWeather(unittest.TestCase):
    """cycling_weather() -> merged cycling-count/weather DataFrame."""

    def setUp(self):
        self.df = cycling_weather()

    def test_shape(self):
        self.assertEqual(
            self.df.shape,
            (8760, 28),
            msg="cycling_weather() should return a DataFrame with shape "
            "(8760, 28) -- one row per hour of 2017 and one column per "
            "weather/cycling-count field. Incorrect shape returned by "
            "cycling_weather function!",
        )

    def test_column_names(self):
        cols = [
            "Year",
            "Precipitation amount (mm)",
            "Snow depth (cm)",
            "Air temperature (degC)",
            "Weekday",
            "Day",
            "Month",
            "Hour",
            "Auroransilta",
            "Eteläesplanadi",
            "Huopalahti (asema)",
            "Kaisaniemi/Eläintarhanlahti",
            "Kaivokatu",
            "Kulosaaren silta et.",
            "Kulosaaren silta po. ",
            "Kuusisaarentie",
            "Käpylä, Pohjoisbaana",
            "Lauttasaaren silta eteläpuoli",
            "Merikannontie",
            "Munkkiniemen silta eteläpuoli",
            "Munkkiniemi silta pohjoispuoli",
            "Heperian puisto/Ooppera",
            "Pitkäsilta itäpuoli",
            "Pitkäsilta länsipuoli",
            "Lauttasaaren silta pohjoispuoli",
            "Ratapihantie",
            "Viikintie",
            "Baana",
        ]
        self.assertCountEqual(
            self.df.columns,
            cols,
            msg="cycling_weather() should return a DataFrame with exactly "
            "these columns (weather fields plus one per counting station). "
            "Incorrect column names!",
        )

    def test_calls(self):
        with patch(
            "src.cycling_weather.cycling_weather", wraps=cycling_weather
        ) as pcw, patch(
            "src.cycling_weather.pd.read_csv", wraps=pd.read_csv
        ) as prc, patch(
            "src.cycling_weather.pd.merge", wraps=pd.merge
        ) as pmerge:
            main()
            pcw.assert_called_once()
            pmerge.assert_called_once()
            self.assertEqual(
                prc.call_count,
                2,
                msg="You should have called pd.read_csv exactly twice: "
                "once for the cycling-count CSV and once for the weather "
                "CSV.",
            )


if __name__ == "__main__":
    unittest.main()
