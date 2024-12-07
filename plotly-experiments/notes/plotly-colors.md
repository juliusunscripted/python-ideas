# plotly colors

## basic color stuff

```python
fig1 = px.bar(
    df1,
    x="Fruit",
    y="Number Eaten",
    color="Contestant",
    color_discrete_sequence=px.colors.qualitative.G10,
    # color_discrete_sequence=px.colors.qualitative.G10_r,
    # color_discrete_sequence=px.colors.qualitative.G10.reverse(),
    barmode="group",
)
```

## color palettes

- [plotly discrete colors](https://plotly.com/python/discrete-color/)
