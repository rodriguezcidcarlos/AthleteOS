import plotly.graph_objects as go


ATHLETEOS_TEMPLATE = {
    
    "layout": {

        "paper_bgcolor": "#080808",

        "plot_bgcolor": "#080808",

        "font": {
            "color": "#f8fafc",
            "family": "Arial"
        },

        "title": {
            "font": {
                "size": 20
            }
        },

        "xaxis": {

            "gridcolor": "#222222",

            "zerolinecolor": "#333333"

        },

        "yaxis": {

            "gridcolor": "#222222",

            "zerolinecolor": "#333333"

        },

        "legend": {

            "orientation": "h",

            "y": -0.2

        }

    }
}


def apply_athleteos_style(fig):

    fig.update_layout(

        template="plotly_dark",

        paper_bgcolor="#0f172a",

        plot_bgcolor="#0f172a",

        font=dict(
            color="#e5e7eb"
        ),

        title_font=dict(
            size=20
        ),

        legend=dict(
            bgcolor="rgba(0,0,0,0)"
        )

    )

    fig.update_xaxes(
        gridcolor="rgba(255,255,255,0.08)"
    )

    fig.update_yaxes(
        gridcolor="rgba(255,255,255,0.08)"
    )

    return fig