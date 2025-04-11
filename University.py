import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import statsmodels

st.set_page_config(layout="wide", page_title="📊 University Dashboard")

df = pd.read_csv("https://raw.githubusercontent.com/Youssef-FahmyEG/Student-Grades/main/content/Students_Grading_Cleaned.csv")

st.sidebar.image("https://raw.githubusercontent.com/Youssef-FahmyEG/Student-Grades/main/content/Logo.png")


gender = st.sidebar.selectbox("Gender", df["gender"].unique())
department = st.sidebar.multiselect("Department", df["department"].unique())
age_group = st.sidebar.multiselect("Age Group", df["age_group"].unique())

filtered_df = df[df["gender"] == gender]
if department:
    filtered_df = filtered_df[filtered_df["department"].isin(department)]
if age_group:
    filtered_df = filtered_df[filtered_df["age_group"].isin(age_group)]

numerical = filtered_df.describe()
categorical = filtered_df.describe(include="O")

st.markdown(
    """
    <style>
        .stApp {
            background-color: black !important;
        }

        .sidebar .sidebar-content {
            background-color: #FFFFFF !important;
        }

        .stTabs [data-baseweb="tab-list"] {
            display: flex;
            justify-content: center;
            flex-wrap: wrap;
            overflow: visible !important;
            padding-right: 0 !important;
        }

        .stTabs [data-baseweb="tab"] {
            flex: 1;
            min-width: 250px;
            text-align: center;
            font-size: 20px !important;
            padding: 15px 30px !important;
            background: linear-gradient(to right, #7b8aff, #4825ff);
            color: white !important;
            border-radius: 10px;
            white-space: nowrap;
        }

        .stTabs [aria-selected="true"] {
            background: linear-gradient(to right, #ff7b8a, #ff4825) !important;
            font-weight: bold !important;
        }

        .custom-title {
            text-align: center;
            color: white !important;
            font-size: 28px !important;
            font-weight: bold;
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 10px;
        }
    </style>
    """,
    unsafe_allow_html=True
)

tab1, tab2 , tab3 , tab4 = st.tabs([
    "📊 DataFrame & Basic Stats",
    "🏛️ Department Overview" ,
    "🏆 Performance Insights" ,
    "🧮 Score Correlation"
])

with tab1:
    total_students = len(filtered_df)
    st.markdown(f'<div class="custom-title">🎓 Total Students: {total_students}</div>', unsafe_allow_html=True)

    st.markdown('<h2 class="custom-title">📋 DataFrame</h2>', unsafe_allow_html=True)
    st.dataframe(filtered_df)

    st.markdown('<h2 class="custom-title">📊 Numerical Statistics</h2>', unsafe_allow_html=True)
    st.dataframe(numerical)

    st.markdown('<h2 class="custom-title">🗂️ Categorical Statistics</h2>', unsafe_allow_html=True)
    st.dataframe(categorical)

with tab2:
    averages = {
        "📅 Attendance": filtered_df["attendance"].mean(),
        "📝 Midterm": filtered_df["midterm_score"].mean(),
        "📚 Quizzes": filtered_df["quizzes_avg"].mean(),
        "💻 Project": filtered_df["projects_score"].mean(),
        "🙋 Participation": filtered_df["participation_score"].mean(),
        "🎯 Final Exam": filtered_df["final_score"].mean(),
        "🏁 Total Score": filtered_df["total_score"].mean()
    }

    st.markdown("<h2 class='custom-title'>📊 Averages Summary</h2>", unsafe_allow_html=True)

    colors = [
        "linear-gradient(135deg, #007cf0, #00dfd8)",
        "linear-gradient(135deg, #7928ca, #ff0080)",
        "linear-gradient(135deg, #f7971e, #ffd200)",
        "linear-gradient(135deg, #00c9ff, #92fe9d)",
        "linear-gradient(135deg, #f953c6, #b91d73)",
        "linear-gradient(135deg, #43cea2, #185a9d)",
        "linear-gradient(135deg, #fc5c7d, #6a82fb)"
    ]


    cards = list(averages.items())
    total_card = cards.pop(-1)

    cols = st.columns(3)
    for i, (label, value) in enumerate(cards):
        with cols[i % 3]:
            st.markdown(f"""
                <div style="
                    background: {colors[i]};
                    padding: 1.5rem;
                    border-radius: 1rem;
                    text-align: center;
                    color: white;
                    margin-bottom: 1.5rem;
                    box-shadow: 0 4px 15px rgba(0,0,0,0.15);
                    height: 180px;
                    display: flex;
                    flex-direction: column;
                    justify-content: center;
                ">
                    <h4 style="margin-bottom: 0.5rem; font-size: 1.4rem; font-weight: 900;">{label}</h4>
                    <h2 style="font-size: 2.8rem; font-weight: bold;">{value:.2f}</h2>
                </div>
            """, unsafe_allow_html=True)

    label, value = total_card
    st.markdown(f"""
        <div style="
            background: {colors[-1]};
            padding: 2rem;
            border-radius: 1rem;
            text-align: center;
            color: white;
            margin: 2rem 0;
            box-shadow: 0 4px 15px rgba(0,0,0,0.15);
            height: 220px;
            display: flex;
            flex-direction: column;
            justify-content: center;
        ">
            <h2 style="margin-bottom: 0.5rem; font-size: 1.8rem; font-weight: 900;">{label}</h2>
            <h1 style="font-size: 4rem; font-weight: bold;">{value:.2f}</h1>
        </div>
    """, unsafe_allow_html=True)

    department_counts = filtered_df["department"].value_counts().reset_index()
    department_counts.columns = ["Department", "Count"]

    colors_map = {
        "CS": "#00008B",
        "Engineering": "#4B0082",
        "Business": "#8000B0",
        "Mathematics": "#C71585"
    }

    bar_colors = [colors_map.get(dept, "#00008B") for dept in department_counts["Department"]]

    fig = go.Figure()

    for i in range(len(department_counts)):
        fig.add_trace(go.Bar(
            x=[department_counts["Department"][i]],
            y=[department_counts["Count"][i]],
            name=department_counts["Department"][i],
            text=[department_counts["Count"][i]],
            textposition='inside',
            textfont=dict(size=16, family="Arial", color="white", weight="bold"),
            marker=dict(color=bar_colors[i]),
            width=0.7
        ))

    fig.update_layout(
        title={
            "text": "Number of Students in each Department",
            "x": 0.5,
            "y": 0.9,
            "xanchor": "center",
            "yanchor": "top",
        },
        title_font=dict(size=24, family="Arial", color="black"),
        yaxis=dict(showticklabels=False, title=None, showgrid=False),
        xaxis=dict(
            tickfont=dict(size=14, family="Arial", color="black", weight="bold"),
            showgrid=False,
            tickangle=0
        ),
        plot_bgcolor="white",
        showlegend=True,
        legend_title=dict(text="Department"),
        legend=dict(font=dict(size=14, family="Arial", color="black", weight="bold")),
        width=900,
        height=500,
        margin=dict(l=50, r=50, t=100, b=50),
        bargap=0.15
    )

    for i, dept in enumerate(department_counts["Department"]):
        fig.add_shape(
            type="line",
            x0=i-0.35,
            x1=i+0.35,
            y0=0,
            y1=0,
            line=dict(color="gray", width=1)
        )

    st.plotly_chart(fig, use_container_width=True)

    grade_counts = filtered_df['grade'].value_counts().reset_index()
    grade_counts.columns = ["Grade", "Count"]

    colors_map = {
        "A": "#00008B",
        "B": "#4B0082",
        "C": "#8000B0",
        "D": "#C71585"
    }

    pie_colors = [colors_map.get(grade, "#00008B") for grade in grade_counts["Grade"]]

    fig2 = px.pie(grade_counts, names="Grade", values="Count", title="Grade Distribution",
                  hole=0.5, color="Grade", labels={"Grade": "Grade", "Count": "Number of Students"})

    fig2.update_traces(marker=dict(colors=pie_colors))

    fig2.update_layout(
        title={
            "text": "Grade Distribution",
            "x": 0.5,
            "xanchor": "center",
            "yanchor": "top"
        },
        title_font=dict(size=24, family="Arial", color="black"),
        legend=dict(
            font=dict(size=17, family="Arial", color="black", weight="bold")
        ),
        annotations=[
            dict(
                font=dict(size=20, family="Arial", color="black", weight="bold"),
                showarrow=False,
                text="Number of Students",
                x=0.5,
                y=-0.1
            )
        ]
    )

    st.plotly_chart(fig2, use_container_width=True)

    attendance_per_dept = filtered_df.groupby("department")["attendance"].mean().reset_index()

    colors_map = {
        "CS": "#00008B",
        "Engineering": "#4B0082",
        "Business": "#8000B0",
        "Mathematics": "#C71585"
    }

    bar_colors = [colors_map.get(dept, "#00008B") for dept in attendance_per_dept["department"]]

    fig = go.Figure()

    for i, row in attendance_per_dept.iterrows():
        dept = row["department"]
        attendance = row["attendance"]
        color = colors_map.get(dept, "#00008B")

        fig.add_trace(go.Bar(
            x=[dept],
            y=[attendance],
            name=dept,
            marker=dict(color=color),
            text=[round(attendance, 1)],
            textposition='inside',
            textfont=dict(size=16, family="Arial", color="white", weight="bold"),
            width=0.7,
            showlegend=True,
            legendgroup=dept
        ))

    fig.update_layout(
        title={
            "text": "Average Attendance by Department",
            "x": 0.5,
            "y": 0.9,
            "xanchor": "center",
            "yanchor": "top",
        },
        title_font=dict(size=24, family="Arial", color="black"),
        yaxis=dict(showticklabels=False, title=None, showgrid=False),
        xaxis=dict(
            tickfont=dict(size=14, family="Arial", color="black", weight="bold"),
            showgrid=False,
            tickangle=0
        ),
        plot_bgcolor="white",
        showlegend=True,
        legend_title_text="Department",
        legend=dict(font=dict(size=14, family="Arial", color="black", weight="bold")),  # ✅ bold legend
        width=900,
        height=500,
        margin=dict(l=50, r=50, t=100, b=50),
        bargap=0.15
    )

    for i in range(len(attendance_per_dept)):
        fig.add_shape(
            type="line",
            x0=i - 0.35,
            x1=i + 0.35,
            y0=0,
            y1=0,
            line=dict(color="gray", width=1)
        )

    st.plotly_chart(fig, use_container_width=True)

with tab3:
    averages = {
        "📅 Attendance": filtered_df["attendance"].mean(),
        "📝 Midterm": filtered_df["midterm_score"].mean(),
        "📚 Quizzes": filtered_df["quizzes_avg"].mean(),
        "💻 Project": filtered_df["projects_score"].mean(),
        "🙋 Participation": filtered_df["participation_score"].mean(),
        "🎯 Final Exam": filtered_df["final_score"].mean(),
        "🏁 Total Score": filtered_df["total_score"].mean()
    }

    st.markdown("<h2 class='custom-title'>📊 Averages Summary</h2>", unsafe_allow_html=True)

    colors = [
        "linear-gradient(135deg, #007cf0, #00dfd8)",
        "linear-gradient(135deg, #7928ca, #ff0080)",
        "linear-gradient(135deg, #f7971e, #ffd200)",
        "linear-gradient(135deg, #00c9ff, #92fe9d)",
        "linear-gradient(135deg, #f953c6, #b91d73)",
        "linear-gradient(135deg, #43cea2, #185a9d)",
        "linear-gradient(135deg, #fc5c7d, #6a82fb)"
    ]


    cards = list(averages.items())
    total_card = cards.pop(-1)

    cols = st.columns(3)
    for i, (label, value) in enumerate(cards):
        with cols[i % 3]:
            st.markdown(f"""
                <div style="
                    background: {colors[i]};
                    padding: 1.5rem;
                    border-radius: 1rem;
                    text-align: center;
                    color: white;
                    margin-bottom: 1.5rem;
                    box-shadow: 0 4px 15px rgba(0,0,0,0.15);
                    height: 180px;
                    display: flex;
                    flex-direction: column;
                    justify-content: center;
                ">
                    <h4 style="margin-bottom: 0.5rem; font-size: 1.4rem; font-weight: 900;">{label}</h4>
                    <h2 style="font-size: 2.8rem; font-weight: bold;">{value:.2f}</h2>
                </div>
            """, unsafe_allow_html=True)

    label, value = total_card
    st.markdown(f"""
        <div style="
            background: {colors[-1]};
            padding: 2rem;
            border-radius: 1rem;
            text-align: center;
            color: white;
            margin: 2rem 0;
            box-shadow: 0 4px 15px rgba(0,0,0,0.15);
            height: 220px;
            display: flex;
            flex-direction: column;
            justify-content: center;
        ">
            <h2 style="margin-bottom: 0.5rem; font-size: 1.8rem; font-weight: 900;">{label}</h2>
            <h1 style="font-size: 4rem; font-weight: bold;">{value:.2f}</h1>
        </div>
    """, unsafe_allow_html=True)

        # === Top 5 Students by Total Score (Enhanced) ===
    top_students = filtered_df.nlargest(5, "total_score")[["full_name", "total_score"]]

    fig = px.bar(
    top_students,
    x="total_score",
    y="full_name",
    title="Top 5 Students by Total Score",
    labels={"full_name": "Student Name", "total_score": "Total Score"},
    text_auto=True,
    color="full_name",
    color_discrete_sequence=px.colors.sequential.Aggrnyl
)

    fig.update_traces(marker=dict(line=dict(width=0)), width=0.6) 

    fig.update_layout(
    title=dict(
        text="Top 5 Students by Total Score",
        x=0.5,
        xanchor="center",
        font=dict(size=24, family="Arial", color="black")
    ),
    legend=dict(
        font=dict(size=14, family="Arial", color="black")
    ),
    yaxis=dict(
        tickfont=dict(size=14, family="Arial", color="black", weight="bold")
    )
)

    st.plotly_chart(fig, use_container_width=True)

    Lowest_students = filtered_df.nsmallest(5, "total_score")[["full_name", "total_score"]]

    fig = px.bar(
    Lowest_students,
    x="total_score",
    y="full_name",
    title="Lowest 5 Students by Total Score",
    labels={"full_name": "Student Name", "total_score": "Total Score"},
    text_auto=True,
    color="full_name",
    color_discrete_sequence=px.colors.sequential.Blues_r
)

    fig.update_traces(marker=dict(line=dict(width=0)), width=0.6)

    fig.update_layout(
    title=dict(
        text="Lowest 5 Students by Total Score",
        x=0.5,
        xanchor="center",
        font=dict(size=24, family="Arial", color="black")
    ),
    legend=dict(
        font=dict(size=14, family="Arial", color="black")
    ),
    yaxis=dict(
        tickfont=dict(size=14, family="Arial", color="black", weight="bold")
    )
)

    st.plotly_chart(fig, use_container_width=True)

    activity_percentages = (filtered_df['extracurricular_activities'].value_counts(normalize=True).round(1)) * 100

    fig = px.pie(
    names=activity_percentages.index,
    values=activity_percentages.values,
    title="Participation in Extracurricular Activities",
    color_discrete_sequence=["#2ca25f", "#a1d99b"],
)

    fig.update_layout(
    title=dict(
        text="Participation in Extracurricular Activities",
        x=0.5,
        xanchor="center",
        font=dict(size=24, color="black", family="Arial")
    ),
    legend=dict(
        font=dict(size=17, color="black", family="Arial", weight="bold")
    )
)

    fig.update_traces(
    textfont=dict(size=14, family="Arial", color="black", weight="bold")
)

    st.plotly_chart(fig, use_container_width=True)

    grade_distribution = filtered_df.groupby('parent_education_level')['grade'].value_counts().unstack().fillna(0).reset_index()

    color_palette = ["#004e64", "#00a5cf", "#7209b7", "#25a18e", "#7ae582"]

    fig = px.bar(
    grade_distribution,
    x="parent_education_level",
    y=grade_distribution.columns[1:],
    labels={
        "parent_education_level": "Parent Education Level",
        "value": "Number of Students"
    },
    barmode="group",
    color_discrete_sequence=color_palette,
    text_auto=True)

    fig.update_layout(
        title={
            "text": "Grade Distribution by Parent Education Level",
            "x": 0.5,
            "y": 0.9,
            "xanchor": "center",
            "yanchor": "top",
        },
        title_font=dict(size=24, family="Arial", color="black"),
        yaxis=dict(showticklabels=False, title=None, showgrid=False),
        xaxis=dict(
            tickfont=dict(size=14, family="Arial", color="black", weight="bold"),
            showgrid=False,
            tickangle=0
        ),
        plot_bgcolor="white",
        showlegend=True,
        legend_title=dict(text="Grade"),
        legend=dict(font=dict(size=17, family="Arial", color="black", weight="bold")),
        width=900,
        height=500,
        margin=dict(l=50, r=50, t=100, b=50),
        bargap=0.15
    )

    st.plotly_chart(fig, use_container_width=True)

    internet_access_counts = filtered_df['internet_access_at_home'].value_counts()

    fig = px.pie(
    names=internet_access_counts.index,
    values=internet_access_counts.values,
    color_discrete_sequence=px.colors.qualitative.Alphabet,
    hole=0.5
)

    fig.update_traces(
    textfont=dict(size=16, family="Arial", color="white"),
    textfont_weight="bold",
    textinfo='label+percent'
)

    fig.update_layout(
    title=dict(
        text="Internet Access at Home",
        x=0.5,
        xanchor='center',
        y=0.95,
        font=dict(size=24, color="black", family="Arial")
    ),
    legend=dict(
        font=dict(size=17, color="black", family="Arial", weight="bold"
        ),
        bgcolor="rgba(0,0,0,0)"
    )
)

    st.plotly_chart(fig, use_container_width=True)

with tab4:
    averages = {
        "📅 Attendance": filtered_df["attendance"].mean(),
        "📝 Midterm": filtered_df["midterm_score"].mean(),
        "📚 Quizzes": filtered_df["quizzes_avg"].mean(),
        "💻 Project": filtered_df["projects_score"].mean(),
        "🙋 Participation": filtered_df["participation_score"].mean(),
        "🎯 Final Exam": filtered_df["final_score"].mean(),
        "🏁 Total Score": filtered_df["total_score"].mean()
    }

    st.markdown("<h2 class='custom-title'>📊 Averages Summary</h2>", unsafe_allow_html=True)

    colors = [
        "linear-gradient(135deg, #007cf0, #00dfd8)",
        "linear-gradient(135deg, #7928ca, #ff0080)",
        "linear-gradient(135deg, #f7971e, #ffd200)",
        "linear-gradient(135deg, #00c9ff, #92fe9d)",
        "linear-gradient(135deg, #f953c6, #b91d73)",
        "linear-gradient(135deg, #43cea2, #185a9d)",
        "linear-gradient(135deg, #fc5c7d, #6a82fb)"
    ]


    cards = list(averages.items())
    total_card = cards.pop(-1)

    cols = st.columns(3)
    for i, (label, value) in enumerate(cards):
        with cols[i % 3]:
            st.markdown(f"""
                <div style="
                    background: {colors[i]};
                    padding: 1.5rem;
                    border-radius: 1rem;
                    text-align: center;
                    color: white;
                    margin-bottom: 1.5rem;
                    box-shadow: 0 4px 15px rgba(0,0,0,0.15);
                    height: 180px;
                    display: flex;
                    flex-direction: column;
                    justify-content: center;
                ">
                    <h4 style="margin-bottom: 0.5rem; font-size: 1.4rem; font-weight: 900;">{label}</h4>
                    <h2 style="font-size: 2.8rem; font-weight: bold;">{value:.2f}</h2>
                </div>
            """, unsafe_allow_html=True)

    label, value = total_card
    st.markdown(f"""
        <div style="
            background: {colors[-1]};
            padding: 2rem;
            border-radius: 1rem;
            text-align: center;
            color: white;
            margin: 2rem 0;
            box-shadow: 0 4px 15px rgba(0,0,0,0.15);
            height: 220px;
            display: flex;
            flex-direction: column;
            justify-content: center;
        ">
            <h2 style="margin-bottom: 0.5rem; font-size: 1.8rem; font-weight: 900;">{label}</h2>
            <h1 style="font-size: 4rem; font-weight: bold;">{value:.2f}</h1>
        </div>
    """, unsafe_allow_html=True)

    numerical_data = filtered_df.select_dtypes(include="number").corr().round(2)


    fig = px.imshow(
    numerical_data, 
    title="Correlation Matrix of Numerical Data",
    text_auto=True  
)

    fig.update_traces(
    textfont=dict(
        size=10,  
        color="black",  
        family="Arial",  
        weight="bold"  
    ),
    texttemplate="%{z}",
)

    fig.update_layout(
    title_font=dict(size=24, family="Arial", color="black"),
    title_x=0.5, 
    title_xanchor="center", 
    xaxis=dict(title="Features", tickfont=dict(size=12, family="Arial", color="black")),
    yaxis=dict(title="Features", tickfont=dict(size=12, family="Arial", color="black")),
    plot_bgcolor="white",
    width=800,
    height=600,
)

    st.plotly_chart(fig)

    fig1 = px.scatter(filtered_df, x="study_hours_per_week", y="total_score", color="gender", trendline="ols", title="Effect of Study Hours on Final Scores")
    fig1.update_layout(
    title=dict(
        text="Effect of Study Hours on Final Scores",
        x=0.5, 
        xanchor='center',
        y=0.95,  
        yanchor='bottom'
    ),
    title_font=dict(size=24, color="black", family="Arial"),
    xaxis_title_font=dict(size=17),
    yaxis_title_font=dict(size=17),
    xaxis=dict(showgrid=False),
    yaxis=dict(showgrid=False),
    legend=dict(
        font=dict(size=17, family="Arial Black")
    )
)
    st.plotly_chart(fig1)

    fig2 = px.scatter(filtered_df, x="final_score", y="quizzes_avg", size="study_hours_per_week", color_discrete_sequence= ["red" , "blue"], title="Correlation between Final Score and Quizzes based on Study Hours")
    fig2.update_traces(marker=dict(
    color=df["gender"].apply(lambda x: 'purple' if x == 'M' else 'blue'),
    showscale=False
))
    fig2.update_layout(
    title=dict(
        text="Correlation between Final Score and Quizzes based on Study Hours",
        x=0.5, 
        xanchor='center',
        y=0.95,  
        yanchor='bottom'
    ),
    title_font=dict(size=24, color="black", family="Arial"),
    xaxis_title_font=dict(size=17),
    yaxis_title_font=dict(size=17),
    xaxis=dict(showgrid=False),
    yaxis=dict(showgrid=False),
    legend=dict(
        font=dict(size=17, family="Arial Black")
    )
)
    st.plotly_chart(fig2)

    fig3 = px.box(filtered_df, x="parent_education_level", y="total_score", color="gender", title="Total Score by Parent Education Level")
    fig3.update_layout(
    title=dict(
        text="Total Score by Parent Education Level",
        x=0.5, 
        xanchor='center',
        y=0.95,  
        yanchor='bottom'
    ),
    title_font=dict(size=24, color="black", family="Arial"),
    xaxis_title_font=dict(size=17),
    yaxis_title_font=dict(size=17),
    xaxis=dict(showgrid=False),
    yaxis=dict(showgrid=False),
    legend=dict(
        font=dict(size=17, family="Arial Black")
    )
)
    st.plotly_chart(fig3)

