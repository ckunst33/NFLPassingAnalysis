import streamlit as st
import plotly.express as px
import pandas as pd
import nfl_data_py as nfl
import requests
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt
from random import randint

st.set_page_config(page_title="NFL Passing Analyzer",page_icon='data:image/jpeg;base64,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',layout='wide')
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
    f'<p style="text-align: center; font-size: 30px;">{caption2}</p>'  # Adjust font-size as needed
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


# Example NFL coordinates (x, y, z)
nfl_coordinates = [
    (10, 20, 0),
    (50, 25, 0),
    (90, 30, 0),
    (100, 40, 0),
]
# Plot the coordinates on the field
df = pd.read_csv('nfl_data.csv')
df['name'] = df['name'].replace('Rayne Prescott', 'Dak Prescott')
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
selected_week = st.multiselect('Select a week', weeks,)
df = df[df['week'].isin(selected_week)]
passes = df['pass_type'].unique()
filter = st.multiselect('Filter by:', passes,default=passes)
df = df[df['pass_type'].isin(filter)]
df['team1'] = 'home'
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
colortype = st.selectbox('Color Scheme',['Completion/Incompletion','Week','Team Colors'])
fieldtype = st.selectbox('Field Type',['NextGen','Grass'])
if fieldtype == 'Grass':
    fieldcol = 'green'
    linecol = 'white'
else:
    fieldcol = '#2C2C2C'
    linecol = 'grey'


def draw_football_field():
    # Define the field dimensions
    field_length = 120  # 100 yards + 2 end zones of 10 yards each
    field_width = 53.33  # 53.33 yards wide (160 feet)
    
    # Create the field as a filled rectangle
    field_x = [0, field_length, field_length, 0, 0]
    field_y = [0, 0, field_width, field_width, 0]
    field_z = [0, 0, 0, 0, 0]


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
            z=[0],  # Z position for the annotation, slightly above the field
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
            z=[0],  # Z position for the annotation, slightly above the field
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
            line=dict(color=linecol, width=1.5, dash='solid'),
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
            line=dict(color=linecol, width=4, dash='solid'),
            showlegend=False,
            hoverinfo='none'
        ))
    # Add annotations for vertical hash marks
    for j in range(-15, 60, 1):
        fig.add_trace(go.Scatter3d(
            x=[-3.1, 3.1],
            y=[j, j],
            z=[0, 0],
            mode='text',
            marker=dict(size=0, color=linecol),
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
            z=[0, 0],
            mode='text',
            marker=dict(size=0, color=linecol),
            text=['-', '-'],
            # textposition='top center',
            showlegend=False,
            hoverinfo='text',
            hovertext=sign + str(j)
        ))
    fig.add_trace(go.Scatter3d(
        x=[x_coordinate, x_coordinate],
        y=[y_coordinate, y_coordinate],
        z=[3, 3],
        mode='markers',
        marker=dict(size=12, color='#4E3A2A',symbol='star'),
        hoverinfo='text',
        hovertext='QB'


    ))
   
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

df2 = df



# df2 = df2.head(50)
# dfg = dfg.head(50)
df2['z'] = 0
# dfg['z'] = 0
x_values = []
y_values = []
z_values = []
# Loop through each row in the 'location' column
# for loc_list in df2['location']:
#     for coord in loc_list:
#         x = loc_list[0]
#         y=loc_list[1]
#         x_values.append(x)
#         y_values.append(y)
#         z_values.append(0)
for index, row in df2.iterrows():
    # Append the value from column 'x' to the list
    x_values.append(row['x'])
    y_values.append(row['y'])
    z_values.append(0)



x_values2 = []
y_values2 = []
z_values2 = []
x_coordinate = st.number_input(
    'Enter QB x coordinate',
    value=0.0,
    min_value=-25.0,  # Minimum value for x coordinate
    max_value=25.0    # Maximum value for x coordinate
)

y_coordinate = st.number_input(
    'Enter QB y coordinate',
    value=-8.0,
    min_value=-10.0,  # Minimum value for y coordinate
    max_value=0.0     # Maximum value for y coordinate
)
for index, row in df2.iterrows():
    # Append the value from column 'x' to the list
    x_values2.append(x_coordinate)
    y_values2.append(y_coordinate)
    z_values2.append(0)
# # Loop through each row in the 'location' column

import numpy as np
import plotly.graph_objects as go
import streamlit as st
import math
def calculate_distance(x1, y1, x2, y2):
    """Calculate the distance between two points (x1, y1) and (x2, y2)."""
    return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)

def generate_arc_points(p1, p2, apex, num_points=100):
    """Generate points on a quadratic Bezier curve (arc) between p1 and p2 with an apex."""
    t = np.linspace(0, 1, num_points)
    x = (1 - t)**2 * p1[0] + 2 * (1 - t) * t * apex[0] + t**2 * p2[0]
    y = (1 - t)**2 * p1[1] + 2 * (1 - t) * t * apex[1] + t**2 * p2[1]
    z = (1 - t)**2 * p1[2] + 2 * (1 - t) * t * apex[2] + t**2 * p2[2]
    return x, y, z

# Example lists of x and y coordinates
x_coords = x_values
y_coords = y_values
z_value = 0  # Fixed z value
x_coords2 = x_values2
y_coords2 = y_values2

# Create figure
fig = go.Figure()
# fig = draw_football_field()

# Loop through pairs of points to create arcs
colors = df['pass_type'].apply(
        lambda pt: 'blue' if pt == 'TOUCHDOWN' else (
            '#39FF14' if pt == 'COMPLETE' else (
                'red' if pt == 'INTERCEPTION' else 'white'
            )
        )
    ).tolist() 
color_dict = {
    "ARI": ["#97233F", "#000000"],  # Arizona Cardinals
    "ATL": ["#A71930", "#000000", "#A5ACAF"],  # Atlanta Falcons
    "BAL": ["#241773", "#000000", "#9E7C0C"],  # Baltimore Ravens
    "BUF": ["#00338D", "#C60C30"],  # Buffalo Bills
    "CAR": ["#0085CA", "#101820", "#A5ACAF", "#BFC0BF"],  # Carolina Panthers
    "CHI": ["#0B162A", "#C83803", "#DD4814", "#FFFFFF"],  # Chicago Bears
    "CIN": ["#FB4F14", "#000000", "#FFFFFF"],  # Cincinnati Bengals
    "CLE": ["#311D00", "#FF3C00", "#FFFFFF"],  # Cleveland Browns
    "DAL": ["#041E42", "#869397", "#FFFFFF"],  # Dallas Cowboys
    "DEN": ["#FB4F14", "#002244", "#FFFFFF"],  # Denver Broncos
    "DET": ["#0076B6", "#B0B7BC", "#FFFFFF"],  # Detroit Lions
    "GB": ["#203731", "#FFB81C"],  # Green Bay Packers
    "HOU": ["#03202F", "#A71930", "#FFFFFF"],  # Houston Texans
    "IND": ["#002C5F", "#A5ACAF", "#FFFFFF"],  # Indianapolis Colts
    "JAC": ["#101820", "#006778", "#D7A22A", "#9F792C", "#FFFFFF"],  # Jacksonville Jaguars
    "KC": ["#E31837", "#FFB81C"],  # Kansas City Chiefs
    "LV": ["#000000", "#A5ACAF", "#FFFFFF"],  # Las Vegas Raiders
    "LAC": ["#0072CE", "#FFB81C", "#002244", "#FFFFFF"],  # Los Angeles Chargers
    "LAR": ["#002244", "#FFFFFF", "#B3995D"],  # Los Angeles Rams
    "MIA": ["#008E97", "#F58220", "#FFFFFF", "#005778"],  # Miami Dolphins
    "MIN": ["#4F2683", "#FFC62F", "#FFFFFF"],  # Minnesota Vikings
    "NE": ["#002244", "#C60C30", "#B0B7BC", "#FFFFFF"],  # New England Patriots
    "NO": ["#D3BC8D", "#000000"],  # New Orleans Saints
    "NYJ": ["#203731", "#FFFFFF"],  # New York Jets
    "PHI": ["#004C54", "#A5ACAF", "#FFFFFF"],  # Philadelphia Eagles
    "PIT": ["#FFB81C", "#101820"],  # Pittsburgh Steelers
    "SF": ["#AA0000", "#B3995D", "#FFFFFF"],  # San Francisco 49ers
    "SEA": ["#002244", "#69BE28", "#A5ACAF", "#FFFFFF"],  # Seattle Seahawks
    "TB": ["#D50A0A", "#34302B", "#FF7900", "#FFFFFF"],  # Tampa Bay Buccaneers
    "TEN": ["#0C2340", "#4B92DB", "#FFFFFF"],  # Tennessee Titans
    "WAS": ["#773141", "#FFB612", "#FFFFFF"]  # Washington Commanders
}

def get_color2(pass_type, colors):
    if pass_type == 'TOUCHDOWN':
        return colors[0]  # First color
    elif pass_type in ['INTERCEPTION', 'INCOMPLETE']:
        return colors[1]  # Second color
    else:
        return colors[0]  # Default to first colo   
import random

# Function to generate a random color in hex format
def random_color():
    return "#{:06x}".format(random.randint(0, 0xFFFFFF))
unique_weeks = df2['week'].unique()
week_to_color = {week: random_color() for week in unique_weeks}
def get_color(row):
    week_color = week_to_color[week]
    return week_color 
passes = df2['pass_type'].tolist()
ys = df2['y'].tolist()
weeks = df2['week'].tolist()
hovertext = [f'Week: {week}: {round(y_value, 2)} Air Yards - {pt}\n' for pt, y_value, week in zip(passes, ys,weeks)]
for i in range(len(df2)):
    if df2['pass_type'].iloc[i] == 'TOUCHDOWN':
        col = 'blue'
    elif df2['pass_type'].iloc[i] == 'INTECEPTION':
        col = 'red'
    elif df2['pass_type'].iloc[i] == 'INCOMPLETE':
        col = 'white'
    else: 
        col = '#39FF14'
    week = df2['week'].iloc[i]
    week = df2['week'].iloc[i]
    col3 = get_color(week)
    col2 = get_color2(df2['pass_type'].iloc[i], color_dict[df2['team'].iloc[i]])
    x1 = x_coords[i]
    y1 = y_coords[i]
    x2 = x_coords2[i]
    y2 = y_coords2[i]
    z_value2 = 3
    # Define the start and end points
    p2 = np.array([x1, y1, z_value])
    p1 = np.array([x2, y2, z_value2])
    
    # Apex will be above the line connecting p1 and p2
    distance = calculate_distance(x1, y1, x2, y2)
    if distance > 50:
        h = randint(28,33)
    elif distance > 40:
        h = randint(24,27)
    elif distance > 30:
        h = randint(21,22)
    elif distance > 20:
        h = randint(14, 15)
    elif distance > 10:
        h = 12
    else: 
        h = 11.5
    if distance < 10:
        h = distance
    apex = np.array([0.5 * (x1 + x2), 0.5 * (y1 + y2), h])  # Adjust apex height as needed
    
    # Generate arc points
    x, y, z = generate_arc_points(p1, p2, apex)
    
    # Add arc trace
    if colortype == 'Completion/Incompletion':
        realcol = col
    elif colortype == 'Team Colors':
        realcol = col2
    else:
        realcol = col3
    fig.add_trace(go.Scatter3d(
        x=x, y=y, z=z,
        mode='lines',
        line=dict(width=8,color=realcol),
        name=f'Arc {i + 1}',
        hoverinfo='text',
        hovertext=hovertext[i]  # Provide hovertext as a list
    ))
    
    # Add start and end points
    fig.add_trace(go.Scatter3d(
        x=[p1[0], p2[0]],
        y=[p1[1], p2[1]],
        z=[p1[2], p2[2]],
        mode='markers',
        marker=dict(size=8, symbol='circle-open',color=col),
        name=f'Endpoints {i + 1}',
        hoverinfo='text',
        hovertext=hovertext[i]  # Provide hovertext as a list
    ))
    fig.add_trace(go.Scatter3d(
        x=[p1[0], p2[0]],
        y=[p1[1], p2[1]],
        z=[p1[2], p2[2]],
        mode='markers',
        marker=dict(size=4, symbol='circle',color=col),
        name=f'Endpoints {i + 1}',
        hoverinfo='text',
        hovertext=hovertext[i]  # Provide hovertext as a list
    ))

# Update layout
fig.update_layout(
    title='3D Arcs Plot',
    scene=dict(
        xaxis_title='X',
        yaxis_title='Y',
        zaxis_title='Z'
    )
)
fig = draw_football_field()
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
            range=(-53.3333/2, 53.3333/2),
            showticklabels=False,
            showgrid=False,

 # Set the range for the x-axis
        ),
        yaxis=dict(
            title='',
            range=[-15,60] ,
            showticklabels=False,
            showgrid=False,
 # Set the range for the y-axis
        ),
        zaxis=dict(
            title='',
            range=[0, 18],
              showbackground=True,
                backgroundcolor=fieldcol,
                showticklabels=False,
                showgrid=False,
 # Set the range for the z-axis
        )
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


# Show plot
# st.write(df2)

# st.plotly_chart(fig,use_container_width=True)




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
    


                            
# List of metrics
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

# Create histogram plot with Seaborn and Matplotlib
plt.style.use('dark_background')
fig, ax = plt.subplots()
sns.histplot(df['y'], kde=False, ax=ax)

# Add labels and title if needed
ax.set_xlabel('Air Yards')
ax.set_ylabel('Frequency')
ax.set_title('Distribution of Air Yards')

col1, col2 = st.columns(2)
with col1:
    st.pyplot(fig)  # Use st.pyplot for Matplotlib figures

# Create field plot
fig, (ax1, ax2) = plt.subplots(1, 2)

qb = df

sns.kdeplot(x=qb.x, y=qb.y, ax=ax1, cmap='gist_heat', shade=True, shade_lowest=False, n_levels=10)
ax1.set_xlabel('')
ax1.set_xticks([])
ax1.set_yticks([])
ax1.set_ylabel('')
ax1.set_xlim(-53.3333/2, 53.3333/2)
ax1.set_ylim(-15,60)

for j in range(-15, 60-1, 1):
    ax1.annotate('--', (-3.1, j-0.5), ha='center', fontsize=10)
    ax1.annotate('--', (3.1, j-0.5), ha='center', fontsize=10)

for i in range(-10, 60, 5):
    ax1.axhline(i, c='w', ls='-', alpha=0.7, lw=1.5)

for i in range(-10, 60, 10):
    ax1.axhline(i, c='w', ls='-', alpha=1, lw=1.5)

for i in range(10, 60-1, 10):
    ax1.annotate(str(i), (-12.88, i-1.15), ha='center', fontsize=15, rotation=270)
    ax1.annotate(str(i), (12.88, i-0.65), ha='center', fontsize=15, rotation=90)

sns.scatterplot(x=qb.x, y=qb.y, ax=ax2)
ax2.set_xlabel('')
ax2.set_ylabel('')
ax2.set_xticks([])
ax2.set_yticks([])
ax2.set_xlim(-53.3333/2, 53.3333/2)
ax2.set_ylim(-15,60)

for j in range(-15, 60, 1):
    ax2.annotate('--', (-3.1, j-0.5), ha='center', fontsize=10)
    ax2.annotate('--', (3.1, j-0.5), ha='center', fontsize=10)

for i in range(-10, 60, 5):
    ax2.axhline(i, c='w', ls='-', alpha=0.7, lw=1.5)

for i in range(-10, 60, 10):
    ax2.axhline(i, c='w', ls='-', alpha=1, lw=1.5)

for i in range(10, 60-1, 10):
    ax2.annotate(str(i), (-12.88, i-1.15), ha='center', fontsize=15, rotation=270)
    ax2.annotate(str(i), (12.88, i-0.65), ha='center', fontsize=15, rotation=90)

with col2:
    st.pyplot(fig)  # Use st.pyplot for Matplotlib figures

# Display season totals
coli1, coli2 = st.columns(2)
with coli1:
    st.subheader('Season Totals')
    st.subheader(f'Completions/Attempts: {complete_count}/{total_passes}')
    st.subheader(f'Completion Percentage: {round((complete_count/total_passes)*100,2)}%')
    st.subheader(f'Touchdowns: {touchdown_count}')
    st.subheader(f'Interceptions: {interception_count}')
    st.subheader(f'Passing Yards: {int(yards)}')

# Plotly bar graph
with coli2:
    selected_metric = st.selectbox('Select Metric', metrics)
    fig2 = px.bar(
        nfl2,
        x='week',
        y=selected_metric,
        title=f'Weekly Statistics for {selected_metric.replace("_", " ").title()}',
        labels={'week': 'Week', selected_metric: selected_metric.replace("_", " ").title()},
        template='plotly_dark'
    )
    st.plotly_chart(fig2)  # Use st.plotly_chart for Plotly figures
