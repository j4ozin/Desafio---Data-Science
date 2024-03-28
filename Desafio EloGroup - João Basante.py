# -*- coding: utf-8 -*-

#Automatically generated by Colaboratory.

#Original file is located at

#NOTEBOOK

#Olá, sou João Basante.

#De acordo com os dados fornecidos, importei a biblioteca **pandas** e fui tratando e analisando cada um. Assim, separei a latitude e longitude, deixando-as em um formato mais agradável para comparação. Em seguida, importei outra biblioteca, **plotly**, para verificar os zipcodes e analisar melhor a situação e suas localizações. Dessa forma, pude diferenciar os locais com unidades e aqueles sem unidades.

#Encontrei os locais onde não há unidades e onde há uma grande população, chegando a possíveis locais para novas unidades, como **Houston** e **Nova York**. Houston é um local com moradores de menor poder aquisitivo, enquanto Nova York possui uma população de maior poder aquisitivo. Isso indica ambas como boas opções para abrir novas unidades, sugerindo 2 em Houston e 1 em Nova York. Vale ressaltar que, ao lado de Nova York, encontra-se Filadélfia, que já possui várias unidades.


!pip install openpyxl

import pandas as pd
import plotly.express as px

# Leitura dos arquivos CSV
df_demografico = pd.read_csv('DemographicData_ZCTAs.csv', index_col=0)
df_economico = pd.read_csv('EconomicData_ZCTAs.csv', index_col=0)
df_geocode = pd.read_csv('df_geocode.csv', index_col=0)
df_test_data = pd.read_csv('test_data.csv')
df_transactional_data = pd.read_csv('transactional_data.csv', delimiter=';')

# Visualização dos dados e informações
print("Informações Demográficas:")
print(df_demografico.info())
print(df_demografico.head())

print("\nInformações Econômicas:")
print(df_economico.info())
print(df_economico.head())

print("\nInformações de Geocódigos:")
print(df_geocode.info())
print(df_geocode.head())

print("\nTest Data:")
print(df_test_data.info())
print(df_test_data.head())

print("\nTransactional Data:")
print(df_transactional_data.info())
print(df_transactional_data.head())

# Plotagem dos dados geográficos
df_geocode[['latitude', 'longitude']] = df_geocode['Location'].str.split(',', expand=True)
df_geocode = df_geocode.drop(df_geocode[df_geocode['Address'] == 'Unavailable'].index).reset_index(drop=True)
df_geocode['latitude'] = df_geocode['latitude'].astype(float)
df_geocode['longitude'] = df_geocode['longitude'].astype(float)

fig_mapa = px.scatter_mapbox(df_geocode, lat='latitude', lon='longitude', hover_name='Address', zoom=1, height=800, width=800)
fig_mapa.update_layout(mapbox_style="open-street-map")
fig_mapa.show()

# Manipulação de dados demográficos e identificação de zips sem clínicas
df_demografico['Zip'] = df_demografico['GeographicAreaName'].str.lstrip('ZCTA5 ').astype(float)
zips_sem_clinica = df_demografico[~df_demografico['Zip'].isin(df_geocode['Zipcode'])].reset_index(drop=True)
zips_sem_clinica = zips_sem_clinica.sort_values('TotalPopulation')

# Definição de zips personalizados
meus_zips = pd.DataFrame({'Zip': [77449, 77494, 11368],
                          'Lat': [29.835560000, 29.743300000, 40.749590000],
                          'Lon': [-95.738130000, -95.828620000, -73.852600000]})

fig_mapa_zips = px.scatter_mapbox(meus_zips, lat='Lat', lon='Lon', hover_name='Zip', zoom=3, height=400, width=600)
fig_mapa_zips.update_layout(mapbox_style="open-street-map")
fig_mapa_zips.show()
