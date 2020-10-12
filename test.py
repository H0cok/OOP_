import plotly.graph_objects as go
import numpy as np
from IPython.display import Image

np.random.seed(1)
N = 100
x = np.random.rand(N)
y = np.random.rand(N)
colors = np.random.rand(N)
sz = np.random.rand(N) * 30
fig = go.Figure()
fig.add_trace(go.Scatter(
    x=x,
    y=y/5,
    mode="markers",
    marker=go.scatter.Marker(
        size=sz,
        color=colors,
        opacity=0.6,
        colorscale="Viridis"
    )
))

#fig.write_image("C:\Program Files\CryptZ\i8g1.png",width=1110, height=360, scale=1, engine = 'kaleido')