import os
from datetime import datetime
import pandas as p
import pytz
from dotenv import load_dotenv
import matplotlib.pyplot as plt

from Integration.Co2emis.Co2emisClient import Co2emisClient
from Integration.Eloverblik.Configuration import Configuration
from Integration.Eloverblik.ConsumptionQuantitiesClient import ConsumptionQuantitiesClient
from Integration.Eloverblik.DataAccessTokenClient import DataAccessTokenClient
from Integration.Eloverblik.MeteringPointIdsClient import MeteringPointIdsClient
from Integration.Elspotprices.ElspotpricesClient import ElspotpricesClient

# https://www.regeringen.dk/nyheder/2022/regeringen-saetter-turbo-paa-groen-omstilling-med-ambitioes-groen-skattereform/
DKK_PER_T_CO2 = float(750)
DKK_PER_KG_CO2 = DKK_PER_T_CO2 / float(1000)
DKK_PER_G_CO2 = DKK_PER_KG_CO2 / float(1000)

bidding_zone = 'DK1'
utc_from = datetime(2022, 5, 9, 0, 0, 0, 0, pytz.UTC)
utc_to = datetime(2022, 5, 10, 0, 0, 0, 0, pytz.UTC)
elspotprices_client = ElspotpricesClient()
elspotprices_series = elspotprices_client.find_elspotprices(bidding_zone, utc_from, utc_to)
hourly_elspotprices_DKK_per_kWh = elspotprices_series / float(1000)
hourly_elspotprices_DKK_per_kWh.name = 'Elektricitetsspotpris per kWh, DKK'


co2emis_client = Co2emisClient()
co2emis_series = co2emis_client.find_co2emis(bidding_zone, utc_from, utc_to).resample('H').mean()
hourly_co2tax_prices_DKK_per_kWh = co2emis_series * DKK_PER_G_CO2
hourly_co2tax_prices_DKK_per_kWh.name = 'CO2-emissionsafgift per kWh, DKK'

hourly_prices_including_tax = p.concat([hourly_elspotprices_DKK_per_kWh, hourly_co2tax_prices_DKK_per_kWh], axis=1)

ax = hourly_prices_including_tax.plot(kind='bar', stacked=True, position=1, title='Spotpris + CO2-afgift i ' + bidding_zone)
trimmed_x_labels = [label.get_text()[5:-9] for label in ax.get_xticklabels()]
ax.set_xticklabels(trimmed_x_labels)
plt.tight_layout()
plt.show()

load_dotenv()
configuration = Configuration()
configuration.refresh_token = os.environ.get('ELOVERBLIK_REFRESH_TOKEN')
configuration.customer_key = os.environ.get('ELOVERBLIK_CUSTOMER_KEY')
configuration.data_access_token = DataAccessTokenClient(configuration).get_token()
metering_point_ids = MeteringPointIdsClient(configuration).find_metering_points_ids()
consumption_quantities_series = ConsumptionQuantitiesClient(configuration).find_consumption_quantities(metering_point_ids, utc_from, utc_to)
consumption_quantities_series = consumption_quantities_series.sum(axis='columns')

hourly_prices_including_tax['Elektricitetsspotpris per kWh, DKK'] = hourly_prices_including_tax['Elektricitetsspotpris per kWh, DKK'] * consumption_quantities_series
hourly_prices_including_tax['CO2-emissionsafgift per kWh, DKK'] = hourly_prices_including_tax['CO2-emissionsafgift per kWh, DKK'] * consumption_quantities_series
ax = hourly_prices_including_tax.plot(kind='bar', stacked=True, position=1, title='Udgifter til Spotpris og CO2-afgift for Systemate A/S')
trimmed_x_labels = [label.get_text()[5:-9] for label in ax.get_xticklabels()]
ax.set_xticklabels(trimmed_x_labels)
plt.tight_layout()
plt.show()
