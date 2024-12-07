# %%
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


# %%
df1 = pd.DataFrame(
    {
        "Fruit": ["Apples", "Oranges", "Bananas", "Apples", "Oranges", "Bananas"],
        "Contestant": ["Alex", "Alex", "Alex", "Jordan", "Jordan", "Jordan"],
        "Number Eaten": [2, 1, 3, 1, 3, 2],
    }
)

df2 = pd.DataFrame(
    {
        "Fruit": ["Apples", "Oranges", "Bananas", "Apples", "Oranges", "Bananas"],
        "Contestant": ["Peter", "Peter", "Peter", "Anna", "Anna", "Anna"],
        "Number Eaten": [4, 6, 8, 6, 3, 1],
    }
)

# %%

fig1 = px.bar(
    df1,
    x="Fruit",
    y="Number Eaten",
    color="Contestant",
    color_discrete_sequence=px.colors.qualitative.G10,
    barmode="group",
)
# fig2 = px.bar(df2, x="Fruit", y="Number Eaten", color="Contestant", color_discrete_sequence=px.colors.qualitative.G10.reverse(), barmode="group")
fig2 = px.bar(
    df2,
    x="Fruit",
    y="Number Eaten",
    color="Contestant",
    color_discrete_sequence=px.colors.qualitative.G10_r,
    barmode="group",
)
fig = go.Figure(data=fig1.data + fig2.data)
fig.show()

# %%
