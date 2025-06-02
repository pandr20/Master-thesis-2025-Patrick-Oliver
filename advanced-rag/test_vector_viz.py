#!/usr/bin/env python3
"""
Test script to verify vector space visualization is working.
Run this to test if the enhanced RAG system can create the vector space visualization.
"""

import sys
import os
from cj_complex_support_rag import SimpleRAGComparison

def main():
    print("🔬 Testing Vector Space Visualization...")
    print("=" * 50)
    
    try:
        # Initialize the analyzer with the PDF path
        print("📊 Initializing RAG analyzer...")
        analyzer = SimpleRAGComparison("data/Full CJ COMPLEX knowlegdebase.pdf")
        
        # Check if UMAP is working
        if analyzer.umap_model is None:
            print("❌ UMAP model failed to initialize")
            return False
            
        if analyzer.projected_embeddings is None:
            print("❌ Projected embeddings are None")
            return False
            
        print(f"✅ UMAP successfully set up with {len(analyzer.projected_embeddings)} embeddings")
        
        # Test with a few questions
        test_questions = [
            "Hvad laver CJ Complex?",
            "Hvor meget koster jeres tjenester?"
        ]
        
        print("🤖 Running RAG analysis on test questions...")
        results = analyzer.compare_methods(test_questions[:2])  # Just test with 2 questions
        
        # Create visualizations
        print("📊 Creating visualizations...")
        analyzer.create_visualizations(results, "test_vector_viz")
        
        # Check if vector space file was created
        vector_file = "test_vector_viz_vector_space.png"
        if os.path.exists(vector_file):
            print(f"✅ Vector space visualization created: {vector_file}")
            return True
        else:
            print(f"❌ Vector space visualization file not found: {vector_file}")
            return False
            
    except Exception as e:
        print(f"❌ Error during test: {e}")
        import traceback
        print("Traceback:")
        print(traceback.format_exc())
        return False

if __name__ == "__main__":
    success = main()
    if success:
        print("\n🎉 Vector space visualization test PASSED!")
        print("The vector visualization should now be working in your main analysis.")
    else:
        print("\n💥 Vector space visualization test FAILED!")
        print("Check the error messages above to troubleshoot.")
    
    sys.exit(0 if success else 1) 