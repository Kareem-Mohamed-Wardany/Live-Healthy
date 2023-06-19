import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import confusion_matrix

def plot_confusion_matrix(y_true, y_pred, classes):
    """
    Plot a confusion matrix for multiclass classification.
    """
    # Compute confusion matrix
    cm = confusion_matrix(y_true, y_pred)
    
    # Normalize the confusion matrix
    cm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]
    
    # Create a figure and axes
    plt.figure(figsize=(8, 6))
    ax = plt.gca()
    
    # Plot the confusion matrix
    sns.heatmap(cm, annot=True, cmap='Blues', fmt='.2f', cbar=False, ax=ax)
    
    # Set the axis labels and title
    ax.set_xlabel('Predicted labels')
    ax.set_ylabel('True labels')
    ax.set_title('Confusion Matrix')
    
    # Set the x-axis and y-axis ticks
    tick_marks = np.arange(len(classes))
    ax.set_xticks(tick_marks + 0.5)
    ax.set_yticks(tick_marks + 0.5)
    ax.set_xticklabels(classes)
    ax.set_yticklabels(classes)
    
    # Show the plot
    plt.tight_layout()
    plt.show()

# Example usage
y_true = [1, 2, 0, 2, 1, 0, 0, 2, 1, 0]
y_pred = [0, 2, 2, 2, 1, 1, 0, 2, 1, 0]
classes = ['Class 0', 'Class 1', 'Class 2']
plot_confusion_matrix(y_true,y_pred,classes)