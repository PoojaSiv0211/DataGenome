import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.figure_factory as ff

from utils.genome_analyzer import (
    prepare_numeric_features,
    compute_correlation,
    build_3d_feature_embedding,
    cluster_features,
    strongest_relationships,
    generate_dataset_report,
)

st.set_page_config(page_title="DataGenome", layout="wide")

st.title("DataGenome")
st.caption("Visualize the hidden DNA of your dataset")

uploaded = st.file_uploader("Upload a dataset (CSV)", type=["csv"])

if uploaded is not None:
    try:
        df = pd.read_csv(uploaded)

        # Drop common non-analytical columns only after df exists
        df = df.drop(
            columns=["PassengerId", "Name", "Ticket", "Cabin", "id", "ID"],
            errors="ignore"
        )

        st.subheader("Dataset Preview")
        st.dataframe(df.head(), width="stretch")

        numeric_df = prepare_numeric_features(df)

        if numeric_df.shape[1] < 2:
            st.warning("Dataset needs at least 2 numeric columns.")
        else:
            # =========================
            # Correlation heatmap
            # =========================
            st.subheader("Feature Correlation")

            corr = compute_correlation(numeric_df)

            fig_corr = ff.create_annotated_heatmap(
                z=corr.values.round(2),
                x=list(corr.columns),
                y=list(corr.index),
                annotation_text=corr.values.round(2).astype(str),
                colorscale="Viridis",
                showscale=True
            )
            fig_corr.update_layout(height=600)

            st.plotly_chart(fig_corr, width="stretch")

            # =========================
            # 3D genome map
            # =========================
            embedding_df = build_3d_feature_embedding(numeric_df)
            embedding_df, cluster_map = cluster_features(embedding_df)

            if embedding_df is None:
                st.warning("Could not generate genome map.")
            else:
                st.subheader("3D Genome Map")

                fig_3d = px.scatter_3d(
                    embedding_df,
                    x="x",
                    y="y",
                    z="z",
                    text="feature",
                    color=embedding_df["cluster"].astype(str),
                    title="3D Dataset Genome Space",
                )

                fig_3d.update_traces(marker=dict(size=9))
                fig_3d.update_layout(height=750)

                st.plotly_chart(fig_3d, width="stretch")

                # =========================
                # Feature clusters
                # =========================
                st.subheader("Feature Clustering")

                if cluster_map:
                    for cluster_id, features in cluster_map.items():
                        st.write(f"**Cluster {cluster_id + 1}:** {', '.join(features)}")
                else:
                    st.write("Not enough features for clustering.")

                # =========================
                # Strongest relationships
                # =========================
                st.subheader("Feature Insights")
                top_pairs = strongest_relationships(corr, top_n=5)

                if top_pairs:
                    st.markdown("### Strongest Relationships")
                    for col1, col2, value in top_pairs:
                        direction = "positive" if value > 0 else "negative"
                        st.write(
                            f"• **{col1} ↔ {col2}** : {direction} correlation `{value:.2f}`"
                        )

                # =========================
                # Auto dataset report
                # =========================
                st.subheader("Auto Dataset Report")
                report = generate_dataset_report(df, numeric_df, corr)
                st.info(report)

                # =========================
                # Dataset summary
                # =========================
                st.subheader("Dataset Summary")
                c1, c2, c3 = st.columns(3)
                c1.metric("Rows", df.shape[0])
                c2.metric("Columns", df.shape[1])
                c3.metric("Numeric Features", numeric_df.shape[1])

    except Exception as e:
        st.error(f"Error reading dataset: {e}")

else:
    st.info("Upload a CSV file to begin.")