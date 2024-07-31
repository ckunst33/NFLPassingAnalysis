import streamlit as st
import plotly.express as px
import pandas as pd
from courtCoordinates2 import CourtCoordinates
from basketballShot2 import BasketballShot
import nfl_data_py as nfl
import requests
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt
st.set_page_config(layout='wide')
def display_player_image(player_id, width2, caption2):
    # Construct the URL for the player image using the player ID
    image_url = f"https://a.espncdn.com/combiner/i?img=/i/headshots/nfl/players/full/{player_id}.png&w=350&h=254"
    
    # Check if the image URL returns a successful response
    response = requests.head(image_url)
    
    if response.status_code == 200:
        # If image is available, display it
        st.markdown(
        f'<div style="display: flex; flex-direction: column; align-items: center;">'
        f'<img src="{image_url}" style="width: {width2}px;">'
        f'<p style="text-align: center;">{caption2}</p>'
        f'</div>',
        unsafe_allow_html=True
    )
    
        # st.image(image_url, width=width2, caption=caption2)
    else:
        image_url = "https://cdn.nba.com/headshots/nba/latest/1040x760/fallback.png"
        st.markdown(
        f'<div style="display: flex; flex-direction: column; align-items: center;">'
        f'<img src="{image_url}" style="width: {width2}px;">'
        f'<p style="text-align: center;">{"Image Unavailable"}</p>'
        f'</div>',
        unsafe_allow_html=True
    )
        # If image is not available, display a message


st.markdown("""
    <style>
    .big-font {
        font-size: 100px !important;
        text-align: center;
    }
    </style>
    <p class="big-font">NFL Passing Analyzer</p>
    """, unsafe_allow_html=True)
ids = nfl.import_ids()

import plotly.graph_objects as go
import numpy as np

def draw_football_field():
    # Define the field dimensions
    field_length = 120  # 100 yards + 2 end zones of 10 yards each
    field_width = 53.33  # 53.33 yards wide (160 feet)
    
    # Create the field as a filled rectangle
    field_x = [0, field_length, field_length, 0, 0]
    field_y = [0, 0, field_width, field_width, 0]
    field_z = [0, 0, 0, 0, 0]

    court = CourtCoordinates()
    court_lines_df = court.get_court_lines()

    # fig = px.line_3d(
    #     data_frame=court_lines_df,
    #     x='x',
    #     y='y',
    #     z='z',
    #     line_group='line_group',
    #     color='color',
    #     color_discrete_map={
    #         'court': 'rgba(0,0,0,0)',
    #         'hoop': '#e47041'
    #     }
    # )
        # Add horizontal lines
    for i in range(10,70,10):
        fig.add_trace(go.Scatter3d(
            x=[25],  # X position for the annotation
            y=[i],  # Y position for the annotation
            z=[-1],  # Z position for the annotation, slightly above the field
            mode='text',
            text=[f'+{i}'],  # Text for the annotation
            textposition='top center',  # Adjusted position for better visibility
            textfont=dict(size=20, color='gold'),  # Font size and color
            showlegend=False,
            hoverinfo='none'
        ))
        fig.add_trace(go.Scatter3d(
            x=[-25],  # X position for the annotation
            y=[i],  # Y position for the annotation
            z=[-1],  # Z position for the annotation, slightly above the field
            mode='text',
            text=[f'+{i}'],  # Text for the annotation
            textposition='top center',  # Adjusted position for better visibility
            textfont=dict(size=20, color='gold'),  # Font size and color
            showlegend=False,
            hoverinfo='none'
        ))
    for i in range(-10, 60, 5):

        fig.add_trace(go.Scatter3d(
            x=[-field_width/2, field_width/2],
            y=[i, i],
            z=[0, 0],
            mode='lines',
            line=dict(color='grey', width=1.5, dash='solid'),
            showlegend=False,
            hoverinfo='none'
        ))
    
    # # Add thicker horizontal lines

    for i in range(-10, 60, 10):

        fig.add_trace(go.Scatter3d(
            x=[-field_width/2, field_width/2],
            y=[i, i],
            z=[0, 0],
            mode='lines',
            line=dict(color='grey', width=4, dash='solid'),
            showlegend=False,
            hoverinfo='none'
        ))
    # Add annotations for vertical hash marks
    for j in range(-15, 60, 1):
        fig.add_trace(go.Scatter3d(
            x=[-3.1, 3.1],
            y=[j, j],
            z=[-1, -1],
            mode='text',
            marker=dict(size=0, color='grey'),
            text=['-', '-'],
            textposition='top center',
            showlegend=False,
            hoverinfo='none'
        ))
        if j <= 0:
            sign = ''
        else:
            sign = '+'
        fig.add_trace(go.Scatter3d(
            x=[-26.5, 26.5],
            y=[j,j],
            z=[-1, -1],
            mode='text',
            marker=dict(size=0, color='grey'),
            text=['-', '-'],
            # textposition='top center',
            showlegend=False,
            hoverinfo='text',
            hovertext=sign + str(j)
        ))
    fig.update_layout(    
        margin=dict(l=20, r=20, t=20, b=20),
        scene_aspectmode="data",
        height=800,
        scene_camera=dict(
            eye=dict(x=1.3, y=0, z=0.7)
        ),
        scene=dict(
            xaxis=dict(
                title='',
                showticklabels=False,
                showgrid=False,
                range=[-field_width / 2, field_width / 2]  # Set x-axis boundaries
            ),
            yaxis=dict(
                title='',
                showticklabels=False,
                showgrid=False,
                range=[-15, 60]  # Set y-axis boundaries
            ),
            zaxis=dict(
                title='',
                showticklabels=False,
                showgrid=False,
                range=[0, 0],  # Adjust if needed
                showbackground=True,
                backgroundcolor='#2C2C2C'
            ),
        ),
        legend=dict(
            yanchor='bottom',
            y=0.05,
            x=0.2,
            xanchor='left',
            orientation='h',
            font=dict(size=15, color='black'),
            bgcolor='white',
            title='',
            itemsizing='constant'
        ),
        legend_traceorder="reversed",
        showlegend=False
    )
    fig.add_trace(go.Scatter3d(
        x=[-field_width/2, field_width/2],
            y=[0, 0],
            z=[0, 0],
            mode='lines',
            line=dict(color='gold', width=4, dash='solid'),
            showlegend=False,
            hoverinfo='text',
            hovertext='Line of Scrimmage'
    ))



    return fig

def plot_coordinates(fig, df):
    x = df['x'].tolist()  # Convert x column to a list
    y = df['y'].tolist()  # Convert y column to a list
    z = [0] * len(df)  # Create a list of zeros for z values
    
    # Map pass_type to colors
    colors = df['pass_type'].apply(
        lambda pt: 'blue' if pt == 'TOUCHDOWN' else (
            '#39FF14' if pt == 'COMPLETE' else (
                'red' if pt == 'INTERCEPTION' else 'white'
            )
        )
    ).tolist()    
    # Generate hover text
    passes = df['pass_type'].tolist()
    ys = df['y'].tolist()
    weeks = df['week'].tolist()
    hovertext = [f'Week: {week}: {round(y_value, 2)} Air Yards - {pt}\n' for pt, y_value, week in zip(passes, ys,weeks)]
    
    
    fig.add_trace(go.Scatter3d(
        x=x,
        y=y,
        z=z,
        mode='markers',
        marker=dict(size=8, color=colors,symbol='circle-open'),
        hoverinfo='text',
        hovertext=hovertext  # Provide hovertext as a list
    ))
    fig.add_trace(go.Scatter3d(
        x=x,
        y=y,
        z=z,
        mode='markers',
        marker=dict(size=5, color=colors,symbol='circle'),
        hoverinfo='text',
        hovertext=hovertext  # Provide hovertext as a list
    ))

# Create the football field figure
fig = go.Figure()
fig = draw_football_field()

# Example NFL coordinates (x, y, z)
nfl_coordinates = [
    (10, 20, 0),
    (50, 25, 0),
    (90, 30, 0),
    (100, 40, 0),
]
# Plot the coordinates on the field
df = pd.read_csv('https://raw.githubusercontent.com/ArrowheadAnalytics/next-gen-scrapy-2.0/master/all_pass_locations.csv')
qbs = df['name'].unique()
qb_name = st.selectbox('Select a quarterback', qbs)
ids = ids[ids['name'] == qb_name]
ids = ids[ids['position'] == 'QB']
df = df.loc[(df['name'].str.contains(qb_name))]
seasons = df['season'].unique()
seasons.sort()
selected_season = st.selectbox('Select a season',seasons)
df = df[df['season']==selected_season]
weeks = df['week'].unique()
weeks.sort()
selected_week = st.multiselect('Select a week', weeks,default=weeks)
df = df[df['week'].isin(selected_week)]
passes = df['pass_type'].unique()
filter = st.multiselect('Filter by:', passes,default=passes)
df = df[df['pass_type'].isin(filter)]
df['team1'] = 'home'
plot_coordinates(fig, df)
game_shots_df = df
nfl2 = nfl.import_ngs_data(stat_type='passing',years=range(selected_season,selected_season+1))
nfl2 = nfl2[nfl2['player_display_name'] == qb_name]
nfl2 = nfl2[nfl2['season'] == selected_season]
nfl2 = nfl2[nfl2['week'].isin(selected_week)]
complete_count = nfl2['completions'].sum()
interception_count = nfl2['interceptions'].sum()
touchdown_count = nfl2['pass_touchdowns'].sum()
total_passes = nfl2['attempts'].sum()
yards = nfl2['pass_yards'].sum()



# game_coords_df = pd.DataFrame()
# # generate coordinates for shot paths
# for index, row in game_shots_df.iterrows():
#     x = row.x,
#     y = row.y,
#     shot = BasketballShot(
#         shot_start_x=x,
#         shot_start_y=y,
#         shot_id=row.season,
#         shot_made=row.pass_type,
#         )
#     shot_df = shot.get_shot_path_coordinates()
#     game_coords_df = pd.concat([game_coords_df, shot_df])


# shot_path_fig = px.line_3d(
#     data_frame=game_coords_df,
#     x='x',
#     y='y',
#     z='z',
#     line_group='line_id',
# )

# for i in range(len(shot_path_fig.data)):
#     fig.add_trace(shot_path_fig.data[i])




# # Show the plot
weekstr = ''
for week in selected_week:
    weekstr += str(week) + ', '
weekstr = weekstr[:-2]
if len(selected_week) > 1:
    typeweek = 'Weeks:'
else:
    typeweek = 'Week:'
st.subheader(f'{qb_name} Passing Chart')
id = int(ids['espn_id'])
if id:
    display_player_image(id,500,f'{qb_name}')
st.subheader(f'Season: {selected_season}')
st.subheader(f'{typeweek} {weekstr}')

st.plotly_chart(fig,use_container_width=True)
# Create a list of metrics
metrics = [
    'avg_time_to_throw',
    'avg_completed_air_yards',
    'avg_intended_air_yards',
    'avg_air_yards_differential',
    'aggressiveness',
    'max_completed_air_distance',
    'avg_air_yards_to_sticks',
    'attempts',
    'pass_yards',
    'pass_touchdowns',
    'interceptions',
    'passer_rating',
    'completions',
    'completion_percentage',
    'expected_completion_percentage',
    'completion_percentage_above_expectation',
    'avg_air_distance',
    'max_air_distance'
]

# Dropdown for selecting metric

# Show plot in Streamlit
# Create the histogram plot
fig, ax = plt.subplots()
sns.histplot(df['y'], kde=False, ax=ax)

# Add labels and title if needed
ax.set_xlabel('Air Yards')
ax.set_ylabel('Frequency')
ax.set_title('Distribution of Air Yards')
col1, col2 = st.columns(2)
# Show the plot in Streamlit
with col1:
    st.plotly_chart(fig)
coli1, coli2 = st.columns(2)
with coli1:
    st.subheader('Season Totals')
    st.subheader(f'Completions/Attempts: {complete_count}/{total_passes}')
    st.subheader(f'Completion Percentage: {round((complete_count/total_passes)*100,2)}%')
    st.subheader(f'Touchdowns: {touchdown_count}')
    st.subheader(f'Interceptions: {interception_count}')
    st.subheader(f'Passing Yards: {int(yards)}')

plt.style.use('dark_background')

#Set up our subplots
fig, (ax1, ax2) =plt.subplots(1,2)


qb = df

#What we've added here is shading for the densities, but leaving the lowest density area unshaded.
#I've also added the *n_level* parameter, which allows us to choose how many levels we want to have in our contour. The higher the number here, the smoother the plot will look.
sns.kdeplot(x=qb.x, y=qb.y, ax=ax1, cmap='gist_heat', shade=True, shade_lowest=False, n_levels=10)

#Set title, remove ticks and labels
ax1.set_xlabel('')
ax1.set_xticks([])

ax1.set_yticks([])

ax1.set_ylabel('')

#Remove any part of the plot that is out of bounds
ax1.set_xlim(-53.3333/2, 53.3333/2)

ax1.set_ylim(-15,60)
#This makes our scales (x and y) equal (1 pixel in the x direction is the same 'distance' in coordinates as 1 pixel in the y direction)




#Plot all of the field markings (line of scrimmage, hash marks, etc.)

for j in range(-15,60-1,1):
    ax1.annotate('--', (-3.1,j-0.5),
                 ha='center',fontsize =10)
    ax1.annotate('--', (3.1,j-0.5),
                 ha='center',fontsize =10)
    
for i in range(-10,60,5):
    ax1.axhline(i,c='w',ls='-',alpha=0.7, lw=1.5)
    
for i in range(-10,60,10):
    ax1.axhline(i,c='w',ls='-',alpha=1, lw=1.5)
    
for i in range(10,60-1,10):
    ax1.annotate(str(i), (-12.88,i-1.15),
            ha='center',fontsize =15,
                rotation=270)
    
    ax1.annotate(str(i), (12.88,i-0.65),
            ha='center',fontsize =15,
                rotation=90)
sns.scatterplot(x=qb.x, y=qb.y, ax=ax2)

ax2.set_xlabel('')
ax2.set_ylabel('')
ax2.set_xticks([])

ax2.set_yticks([])

ax2.set_xlim(-53.3333/2, 53.3333/2)

ax2.set_ylim(-15,60)

for j in range(-15,60,1):
    ax2.annotate('--', (-3.1,j-0.5),
                 ha='center',fontsize =10)
    ax2.annotate('--', (3.1,j-0.5),
                 ha='center',fontsize =10)
    
for i in range(-10,60,5):
    ax2.axhline(i,c='w',ls='-',alpha=0.7, lw=1.5)
    
for i in range(-10,60,10):
    ax2.axhline(i,c='w',ls='-',alpha=1, lw=1.5)
    
for i in range(10,60-1,10):
    ax2.annotate(str(i), (-12.88,i-1.15),
            ha='center',fontsize =15,
                rotation=270)
    
    ax2.annotate(str(i), (12.88,i-0.65),
            ha='center',fontsize =15,
                rotation=90)

with col2:
    st.pyplot(fig)
with coli2:
    selected_metric = st.selectbox('Select Metric', metrics)

# Plotly bar graph
    fig2 = px.bar(
    nfl2,
    x='week',
    y=selected_metric,
    title=f'Weekly Statistics for {selected_metric.replace("_", " ").title()}',
    labels={'week': 'Week', selected_metric: selected_metric.replace("_", " ").title()},
    template='plotly_dark'
    )

    st.plotly_chart(fig2)


