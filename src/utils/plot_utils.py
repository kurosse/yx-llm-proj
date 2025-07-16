import seaborn as sns

def plot_ratings_graph(ratings_df, x, y, save_path=None):

    languages = [
        "zho_Hans",
        "jpn_Jpan",
        "vie_Latn",
        "ind_Latn",
        "tha_Thai",
        "tgl_Latn",
        "amh_Ethi",
        "tso_Latn",
    ]

    resource_colors = {
        "zho_Hans": "green",    # high
        "jpn_Jpan": "green",    # high
        "vie_Latn": "orange",   # medium (amber)
        "ind_Latn": "orange",   # medium
        "tha_Thai": "orange",      # low
        "tgl_Latn": "red",      # low
        "amh_Ethi": "red",      # low
        "tso_Latn": "red",      # low
    }

    sns.set_style("whitegrid")
    graph = sns.catplot(
        data=ratings_df,
        x=x,
        y=y,
        hue="candidate",
        kind="bar",
        height=3.5,
        order=languages,
        aspect=2,
        legend_out=False
    )
    graph.figure.suptitle(
        f"{y} Ratings by Language and Candidate Models",
        y=1.02,            # push it up a little bit
        fontsize=14
    )
    # then make room for it
    graph.figure.subplots_adjust(top=0.9)
    graph.set_xticklabels(rotation=0)
    graph.set_axis_labels("Language", y)
    graph.despine(left=True)
    graph.set(ylim=(0, 100))
    graph.add_legend(
        loc="lower left",
        bbox_to_anchor=(0.01, 0),
    )

    for ax in graph.axes.flat:
        for graph_bar in ax.patches:
            height = graph_bar.get_height()
            if height == 0:
                continue
            ax.text(
                graph_bar.get_x() + graph_bar.get_width() / 2,  # x-position: center of bar
                height + 0.3,                         # y-position: just above bar
                f"{height:.0f}",                      # text label
                ha="center",                          # horizontal alignment
                va="bottom",                           # vertical alignment
                fontsize=11,                       # font size
            )

    for ax in graph.axes.flat:
        for label in ax.get_xticklabels():
            txt = label.get_text()
            if txt in resource_colors:
                label.set_color(resource_colors[txt])

    if save_path:
        graph.savefig(save_path, bbox_inches="tight")
