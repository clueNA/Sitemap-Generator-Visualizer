import streamlit as st
import requests
import xml.etree.ElementTree as ET
from datetime import datetime
import networkx as nx
import plotly.graph_objects as go
from urllib.parse import urlparse
import pandas as pd
from sitemap_generator import SitemapGenerator

# ... (previous imports remain the same)

def create_network_graph(urls):
    """Create a network graph visualization using plotly"""
    G = nx.DiGraph()
    
    # Add nodes and edges
    for url in urls:
        parsed = urlparse(url)
        path_parts = parsed.path.strip('/').split('/')
        
        current_path = parsed.scheme + '://' + parsed.netloc
        G.add_node(current_path)
        
        for part in path_parts:
            if part:
                next_path = current_path + '/' + part
                G.add_node(next_path)
                G.add_edge(current_path, next_path)
                current_path = next_path
    
    # Create layout
    pos = nx.spring_layout(G)
    
    # Create edges trace
    edge_x = []
    edge_y = []
    for edge in G.edges():
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]
        edge_x.extend([x0, x1, None])
        edge_y.extend([y0, y1, None])

    edge_trace = go.Scatter(
        x=edge_x, y=edge_y,
        line=dict(width=0.5, color='#888'),
        hoverinfo='none',
        mode='lines')

    # Create nodes trace
    node_x = []
    node_y = []
    node_text = []
    for node in G.nodes():
        x, y = pos[node]
        node_x.append(x)
        node_y.append(y)
        node_text.append(node)

    node_trace = go.Scatter(
        x=node_x, y=node_y,
        mode='markers+text',
        hoverinfo='text',
        text=node_text,
        textposition="top center",
        marker=dict(
            showscale=True,
            colorscale='YlGnBu',
            size=10,
            colorbar=dict(
                thickness=15,
                title=dict(
                    text='Node Connections',
                    side='right'
                ),
                xanchor='left'
            )
        )
    )

    # Create the figure
    fig = go.Figure(data=[edge_trace, node_trace],
                   layout=go.Layout(
                       title='Website Structure',
                       showlegend=False,
                       hovermode='closest',
                       margin=dict(b=20, l=5, r=5, t=40),
                       xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                       yaxis=dict(showgrid=False, zeroline=False, showticklabels=False)
                   ))
    
    return fig

def parse_sitemap(xml_content):
    """Parse sitemap XML and return structured data"""
    root = ET.fromstring(xml_content)
    namespace = root.tag.split('}')[0] + '}' if '}' in root.tag else ''
    
    urls = []
    for url in root.findall(f".//{namespace}url"):
        loc = url.find(f"{namespace}loc")
        lastmod = url.find(f"{namespace}lastmod")
        changefreq = url.find(f"{namespace}changefreq")
        priority = url.find(f"{namespace}priority")
        
        url_data = {
            'URL': loc.text if loc is not None else '',
            'Last Modified': lastmod.text if lastmod is not None else '',
            'Change Frequency': changefreq.text if changefreq is not None else '',
            'Priority': priority.text if priority is not None else ''
        }
        urls.append(url_data)
    
    return urls

def main():
    st.set_page_config(page_title="Sitemap Generator & Visualizer", layout="wide")
    
    st.title("Sitemap Generator & Visualizer")
    
    # Create tabs
    tab1, tab2 = st.tabs(["Generate Sitemap", "Visualize Sitemap"])
    
    with tab1:
        st.header("Generate Sitemap")
        
        # Input fields for sitemap generation
        website_url = st.text_input("Enter website URL", "https://example.com")
        max_urls = st.number_input("Maximum URLs to crawl", min_value=10, max_value=50000, value=1000)
        excluded_paths = st.text_area(
            "Excluded paths (one per line)", 
            "admin\nlogin\ncart\n/wp-admin"
        ).split('\n')
        
        if st.button("Generate Sitemap"):
            try:
                with st.spinner("Crawling website and generating sitemap..."):
                    generator = SitemapGenerator(
                        website_url,
                        excluded_paths=[path.strip() for path in excluded_paths if path.strip()],
                        max_urls=max_urls
                    )
                    sitemap_xml = generator.generate()
                    
                    # Display the sitemap
                    st.subheader("Generated Sitemap")
                    st.code(sitemap_xml, language='xml')
                    
                    # Add download button
                    st.download_button(
                        label="Download Sitemap",
                        data=sitemap_xml,
                        file_name="sitemap.xml",
                        mime="application/xml"
                    )
                    
                    # Parse and display structured data
                    urls_data = parse_sitemap(sitemap_xml)
                    df = pd.DataFrame(urls_data)
                    st.subheader("URLs Found")
                    st.dataframe(df)
                    
                    # Display visualization
                    st.subheader("Site Structure Visualization")
                    fig = create_network_graph([url['URL'] for url in urls_data])
                    st.plotly_chart(fig, use_container_width=True)
                    
            except Exception as e:
                st.error(f"Error generating sitemap: {str(e)}")
    
    with tab2:
        st.header("Visualize Existing Sitemap")
        
        # Option to input sitemap URL or upload XML file
        input_method = st.radio("Choose input method", ["URL", "Upload File"])
        
        if input_method == "URL":
            sitemap_url = st.text_input("Enter sitemap URL")
            if st.button("Visualize"):
                try:
                    response = requests.get(sitemap_url)
                    sitemap_content = response.text
                    urls_data = parse_sitemap(sitemap_content)
                    
                    # Display data and visualization
                    df = pd.DataFrame(urls_data)
                    st.dataframe(df)
                    
                    fig = create_network_graph([url['URL'] for url in urls_data])
                    st.plotly_chart(fig, use_container_width=True)
                    
                except Exception as e:
                    st.error(f"Error processing sitemap: {str(e)}")
        
        else:
            uploaded_file = st.file_uploader("Upload sitemap XML file", type=['xml'])
            if uploaded_file is not None:
                try:
                    sitemap_content = uploaded_file.read().decode()
                    urls_data = parse_sitemap(sitemap_content)
                    
                    # Display data and visualization
                    df = pd.DataFrame(urls_data)
                    st.dataframe(df)
                    
                    fig = create_network_graph([url['URL'] for url in urls_data])
                    st.plotly_chart(fig, use_container_width=True)
                    
                except Exception as e:
                    st.error(f"Error processing sitemap: {str(e)}")

if __name__ == "__main__":
    main()