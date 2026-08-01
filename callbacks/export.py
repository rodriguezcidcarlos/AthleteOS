from pathlib import Path
import tempfile

import pandas as pd

from dash import (
    Input,
    Output,
    State,
    dcc
)

from exports.pdf_report import generate_pdf_report
from components.exposure_scatter import build_exposure_scatter_figure
from components.executive_gauges import build_executive_gauges_figures
from utils.compensatory import calculate_compensatory

def register_export_callbacks(app):

    @app.callback(
        Output("download-pdf", "data"),
        Input("export-pdf-btn", "n_clicks"),
        State("uploaded-data-store", "data"),
        prevent_initial_call=True
    )
    def export_pdf(_, store):

        if not store:
            return None


        df = pd.DataFrame(
            store["df"]
        )

        squad = pd.DataFrame(
            store["squad"]
        )

        priority = pd.DataFrame(
            store["priority"]
        )

        comp = calculate_compensatory(df)

        print(comp)

        pdf_path = str(
            Path(tempfile.gettempdir())
            / "AthleteOS_Report.pdf"
        )


        # ==========================
        # Figuras para PDF
        # ==========================

        gauges = build_executive_gauges_figures(
            df,
            squad
        )


        exposure = build_exposure_scatter_figure(
            df
        )


        figures = {

            "acwr": gauges["acwr"],

            "availability": gauges["availability"],

            "exposure": gauges["exposure"],

            "scatter": exposure

        }


        generate_pdf_report(
            df=df,
            squad=squad,
            priority=priority,
            figures=figures,
            output_path=pdf_path
        )


        return dcc.send_file(
            pdf_path
        )