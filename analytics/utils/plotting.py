import plotly.graph_objects as go

def get_empty_plotly_chart(margin = None):
    fig = go.Figure()

    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        autosize=True,
        margin=margin or {"l": 60, "r": 60, "b": 60, "t": 60},
        showlegend=False,
        yaxis={"showticklabels": False},
        xaxis={"showticklabels": False},
    )

    return fig.to_json()