#!/usr/bin/env python3
"""
Minimal test for vector space visualization to isolate segmentation fault issues.
"""

import matplotlib
matplotlib.use('Agg')  # Set backend before importing pyplot
import matplotlib.pyplot as plt
import numpy as np
import sys
import os

def test_basic_plot():
    """Test basic matplotlib functionality."""
    try:
        print("📊 Testing basic matplotlib...")
        fig, ax = plt.subplots(1, 1, figsize=(8, 6))
        
        # Create some dummy data
        x = np.random.randn(50)
        y = np.random.randn(50)
        
        ax.scatter(x, y, alpha=0.6)
        ax.set_title('Basic Test Plot')
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        
        plt.savefig('basic_test.png', dpi=150, bbox_inches='tight')
        plt.close()
        plt.clf()
        
        if os.path.exists('basic_test.png'):
            print("✅ Basic matplotlib test PASSED")
            return True
        else:
            print("❌ Basic matplotlib test FAILED")
            return False
            
    except Exception as e:
        print(f"❌ Basic matplotlib test ERROR: {e}")
        return False

def test_umap_visualization():
    """Test UMAP-like visualization without the actual RAG system."""
    try:
        print("🔬 Testing UMAP-like visualization...")
        
        # Create dummy embeddings and projections
        n_docs = 73
        embedding_dim = 384
        
        # Simulate embeddings
        embeddings = np.random.randn(n_docs, embedding_dim)
        
        # Simulate UMAP projection (just use first 2 dimensions for simplicity)
        projected = embeddings[:, :2]
        
        # Create visualization
        fig, axes = plt.subplots(2, 2, figsize=(12, 10))
        
        # Plot 1: All documents
        ax = axes[0, 0]
        ax.scatter(projected[:, 0], projected[:, 1], 
                  c='lightgray', alpha=0.5, s=10)
        ax.set_title('All Documents')
        ax.grid(True, alpha=0.3)
        
        # Plot 2: Query points
        ax = axes[0, 1]
        ax.scatter(projected[:, 0], projected[:, 1], 
                  c='lightgray', alpha=0.3, s=10)
        # Add some query points
        query_points = np.random.randn(3, 2)
        colors = ['red', 'blue', 'green']
        for i, (point, color) in enumerate(zip(query_points, colors)):
            ax.scatter(point[0], point[1], c=color, s=80, marker='X', 
                      label=f'Query {i+1}')
        ax.set_title('Queries')
        ax.legend()
        ax.grid(True, alpha=0.3)
        
        # Plot 3: Retrieved documents
        ax = axes[1, 0]
        ax.scatter(projected[:, 0], projected[:, 1], 
                  c='lightgray', alpha=0.3, s=10)
        # Simulate retrieved documents
        naive_indices = np.random.choice(n_docs, 5, replace=False)
        advanced_indices = np.random.choice(n_docs, 10, replace=False)
        
        ax.scatter(projected[naive_indices, 0], projected[naive_indices, 1], 
                  c='lightcoral', s=30, alpha=0.7, label='Naive RAG')
        ax.scatter(projected[advanced_indices, 0], projected[advanced_indices, 1], 
                  c='lightblue', s=30, alpha=0.7, label='Advanced RAG')
        ax.set_title('Retrieved Documents')
        ax.legend()
        ax.grid(True, alpha=0.3)
        
        # Plot 4: Detailed view
        ax = axes[1, 1]
        ax.scatter(projected[:, 0], projected[:, 1], 
                  c='lightgray', alpha=0.3, s=10)
        ax.scatter(query_points[0][0], query_points[0][1], 
                  c='red', s=120, marker='X', label='Query')
        ax.scatter(projected[naive_indices[:3], 0], projected[naive_indices[:3], 1], 
                  c='lightcoral', s=50, alpha=0.8, label='Naive')
        ax.scatter(projected[advanced_indices[:3], 0], projected[advanced_indices[:3], 1], 
                  c='lightblue', s=50, alpha=0.8, label='Advanced')
        ax.set_title('Detailed View')
        ax.legend()
        ax.grid(True, alpha=0.3)
        
        plt.suptitle('Vector Space Analysis Test', fontsize=14)
        plt.tight_layout()
        
        plt.savefig('vector_space_test.png', dpi=150, bbox_inches='tight')
        plt.close()
        plt.clf()
        
        if os.path.exists('vector_space_test.png'):
            print("✅ Vector space visualization test PASSED")
            return True
        else:
            print("❌ Vector space visualization test FAILED")
            return False
            
    except Exception as e:
        print(f"❌ Vector space test ERROR: {e}")
        import traceback
        print(traceback.format_exc())
        return False

def main():
    print("🧪 Running Minimal Vector Space Tests...")
    print("=" * 50)
    
    # Test 1: Basic matplotlib
    basic_success = test_basic_plot()
    
    if not basic_success:
        print("\n💥 Basic matplotlib failed - cannot proceed")
        return False
    
    # Test 2: Vector space visualization
    vector_success = test_umap_visualization()
    
    if vector_success:
        print("\n🎉 All tests PASSED!")
        print("The issue might be specific to the RAG system integration.")
        print("Vector space visualization should work in principle.")
        return True
    else:
        print("\n💥 Vector space test FAILED!")
        print("There's a fundamental issue with the visualization.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 