import pandas as pd
from dash import Dash, html, dcc, Input, Output
import plotly.express as px

# ======================================
# Load and Merge Data
# ======================================

performance = pd.read_csv("data/student_performance.csv")
activity = pd.read_csv("data/student_activity.csv")

df = pd.merge(
    performance,
    activity,
    on="Student_ID"
)

# ======================================
# KPI Calculations
# ======================================

total_students = len(df)

avg_marks = round(
    df["Final_Marks"].mean(),
    2
)

avg_attendance = round(
    df["Attendance"].mean(),
    2
)

avg_assignment = round(
    df["Assignment_Completion"].mean(),
    2
)

top_department = (
    df.groupby("Department")["Final_Marks"]
    .mean()
    .idxmax()
)

best_attendance_department = (
    df.groupby("Department")["Attendance"]
    .mean()
    .idxmax()
)

# ======================================
# Dash App
# ======================================

app = Dash(__name__)

card_style = {
    "backgroundColor": "#1E1E1E",
    "borderRadius": "15px",
    "padding": "20px",
    "textAlign": "center",
    "width": "15%",
    "boxShadow": "0px 4px 12px rgba(0,0,0,0.4)"
}

filter_style = {
    "width": "50%",
    "color": "black"
}

app.layout = html.Div([

    # ==================================
    # Title
    # ==================================

    html.H1(
        "Student Performance Dashboard",
        style={
            "textAlign": "center",
            "color": "#00D4FF",
            "marginBottom": "30px"
        }
    ),

    # ==================================
    # KPI Cards
    # ==================================

    html.Div([

        html.Div([
            html.H3("Total Students"),
            html.H2(total_students)
        ], style=card_style),

        html.Div([
            html.H3("Average Marks"),
            html.H2(avg_marks)
        ], style=card_style),

        html.Div([
            html.H3("Attendance"),
            html.H2(f"{avg_attendance}%")
        ], style=card_style),

        html.Div([
            html.H3("Assignments"),
            html.H2(f"{avg_assignment}%")
        ], style=card_style),

        html.Div([
            html.H3("Top Department"),
            html.H2(top_department)
        ], style=card_style),

        html.Div([
            html.H3("Best Attendance"),
            html.H2(best_attendance_department)
        ], style=card_style)

    ],
    style={
        "display": "flex",
        "justifyContent": "space-between",
        "flexWrap": "wrap",
        "gap": "10px"
    }),

    html.Br(),

    # ==================================
    # Filters
    # ==================================

    html.Div([

        html.H3(
            "Select Gender",
            style={"color": "white"}
        ),

        dcc.Dropdown(
            id="gender_filter",
            options=[
                {"label": gender, "value": gender}
                for gender in df["Gender"].unique()
            ],
            value=df["Gender"].unique()[0],
            clearable=False,
            style=filter_style
        ),

        html.Br(),

        html.H3(
            "Select Department",
            style={"color": "white"}
        ),

        dcc.Dropdown(
            id="department_filter",
            options=[
                {"label": dep, "value": dep}
                for dep in df["Department"].unique()
            ],
            value=df["Department"].unique()[0],
            clearable=False,
            style=filter_style
        )

    ]),

    html.Br(),

    # ==================================
    # Top Charts
    # ==================================

    html.Div([

        dcc.Graph(
            id="department_chart",
            style={"width": "50%"}
        ),

        dcc.Graph(
            id="department_pie_chart",
            style={"width": "50%"}
        )

    ],
    style={
        "display": "flex"
    }),

    # ==================================
    # Scatter Plot
    # ==================================

    dcc.Graph(
        id="attendance_marks_chart"
    ),

    # ==================================
    # Study Hours Chart
    # ==================================

    dcc.Graph(
        id="study_hours_chart"
    )

],
style={
    "backgroundColor": "#121212",
    "minHeight": "100vh",
    "padding": "20px",
    "color": "white"
})

# ======================================
# Department Bar Chart
# ======================================

@app.callback(
    Output("department_chart", "figure"),
    Input("department_filter", "value")
)
def update_department_chart(selected_department):

    filtered_df = df[
        df["Department"] == selected_department
    ]

    fig = px.bar(
        filtered_df,
        x="Student_ID",
        y="Final_Marks",
        color="Final_Marks",
        title=f"Student Marks in {selected_department}"
    )

    fig.update_layout(
        template="plotly_dark"
    )

    return fig

# ======================================
# Department Pie Chart
# ======================================

@app.callback(
    Output("department_pie_chart", "figure"),
    Input("department_filter", "value")
)
def update_pie_chart(selected_department):

    department_count = (
        df.groupby("Department")
        .size()
        .reset_index(name="Count")
    )

    fig = px.pie(
        department_count,
        names="Department",
        values="Count",
        title="Department Distribution"
    )

    fig.update_layout(
        template="plotly_dark"
    )

    return fig

# ======================================
# Attendance vs Marks
# ======================================

@app.callback(
    Output("attendance_marks_chart", "figure"),
    Input("gender_filter", "value")
)
def update_attendance_chart(selected_gender):

    filtered_df = df[
        df["Gender"] == selected_gender
    ]

    fig = px.scatter(
        filtered_df,
        x="Attendance",
        y="Final_Marks",
        color="Department",
        size="Study_Hours",
        hover_data=["Student_ID"],
        title=f"Attendance vs Marks ({selected_gender})"
    )

    fig.update_layout(
        template="plotly_dark"
    )

    return fig

# ======================================
# Study Hours vs Marks
# ======================================

@app.callback(
    Output("study_hours_chart", "figure"),
    Input("gender_filter", "value")
)
def update_study_chart(selected_gender):

    filtered_df = df[
        df["Gender"] == selected_gender
    ]

    fig = px.scatter(
        filtered_df,
        x="Study_Hours",
        y="Final_Marks",
        color="Department",
        hover_data=["Student_ID"],
        title=f"Study Hours vs Final Marks ({selected_gender})"
    )

    fig.update_layout(
        template="plotly_dark"
    )

    return fig

# ======================================
# Run App
# ======================================

if __name__ == "__main__":
    app.run(debug=True)