
import folium
from folium.plugins import HeatMap
import os


def create_map(scores_df: list, bar_df: list, city_centroid: tuple, city: str):
    max_amount = float(scores_df['Score_scaled'].max())

    hmap = folium.Map(location=list(city_centroid), zoom_start=12, )

    for index, row in bar_df.iterrows():
        popup = '''<div class="row">
                        <div class="column">
                            <p>Name: {}</p>
                            <p>Rating: {}</p>
                        </div>
                    </div>'''.format(row['name'], row['score'])

        folium.Marker([row['lat'], row['lon']], popup=popup).add_to(hmap)

    hm_wide = HeatMap(list(zip(scores_df.latitude.values, scores_df.longitude.values, scores_df.Score_scaled.values)),
                       min_opacity=0.0,
                       max_val=max_amount,
                       radius=25,
                       blur=15,
                       max_zoom=8,)

    hmap.add_child(hm_wide)
    heatmap_name = city + '_heatmap.html'
    hmap.save(os.path.join('results', heatmap_name))
