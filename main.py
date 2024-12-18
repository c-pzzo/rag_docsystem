import streamlit as st
from src.processing.parser import READMEParser
from src.processing.embeddings import TextEmbeddings
from src.database.operations import MongoDB

def initialize_session_state():
    """Initialize session state variables."""
    if 'db' not in st.session_state:
        st.session_state.db = MongoDB()
    if 'embedder' not in st.session_state:
        st.session_state.embedder = TextEmbeddings()

def search_section():  # Moved up
    """Search Interface"""
    st.header("Search Projects")
    
    query = st.text_input("Enter your search query")
    if query and st.button("Search"):
        try:
            with st.spinner("Searching..."):
                # Generate embedding for query
                query_embedding = st.session_state.embedder.generate_embedding(query)
                
                # Search in MongoDB
                results = st.session_state.db.search_projects(query_embedding)
                
                # Display results
                if results:
                    for idx, result in enumerate(results, 1):
                        with st.expander(f"#{idx} - {result['name']} ({result['project_id']})"):
                            st.markdown("**Overview:**")
                            st.write(result['overview'])
                            st.markdown("---")
                            st.markdown(f"**Relevance Score:** {result['similarity']:.1f}%")
                else:
                    st.info("No matching projects found.")
                
        except Exception as e:
            st.error(f"Error during search: {str(e)}")

def upload_section():  # After search_section
    """README Upload Section"""
    st.header("Upload README")
    uploaded_file = st.file_uploader("Choose a README.md file", type=['md'])
    
    if uploaded_file and st.button("Process README"):
        try:
            # Read and process the file
            content = uploaded_file.read().decode()
            
            # Parse README
            parser = READMEParser(content)
            parsed_data = parser.parse()
            
            # Generate embeddings for sections
            embedded_sections = st.session_state.embedder.generate_section_embeddings(
                parsed_data['sections']
            )
            parsed_data['sections'] = embedded_sections
            
            # Store in MongoDB
            st.session_state.db.insert_project(parsed_data)
            
            st.success(f"Successfully processed README for project: {parsed_data['name']}")
            
        except Exception as e:
            st.error(f"Error processing file: {str(e)}")

def main():  # Main function at the end
    st.title("Project Discovery System")
    
    # Initialize session state
    initialize_session_state()
    
    # Create tabs for different functionalities
    tab1, tab2 = st.tabs(["Upload", "Search"])
    
    with tab1:
        upload_section()
        
    with tab2:
        search_section()

if __name__ == "__main__":
    main()