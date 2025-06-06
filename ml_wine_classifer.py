# -*- coding: utf-8 -*-
"""ML-Wine-Classifer.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1oHYUUBOubvrrjB6klRzgLw0QUW_ZzDgk
"""

# Commented out IPython magic to ensure Python compatibility.
# Enable widgets
from google.colab import output
output.enable_custom_widget_manager()
import ipywidgets as widgets

# Install otter-grader
# %pip install -q otter-grader==6.1.0

# Download the tests directory from the course website (this will be used by otter-grader)
!wget -q https://dtrb.github.io/machinelearning1/assignments/Winter2025/ass7/tests.zip -O tests.zip

# Unzip the tests directory, forcing overwriting of existing files
!unzip -qo tests.zip -d .

# Initialize Otter
import otter
grader = otter.Notebook()

"""# ML Wine Classifer
## Introduction

Welcome to the ML Wine Classifier! In this project, I implement a multi-class classification learner using estimated cross-entropy loss, linear and polynomial decision boundaries and key Python modules like numpy, pandas and scikit-learn.

1. [Dataset Information](#part-1-dataset-information)
1. [Multiclass Classification](#part-2-multiclass-classification)

This project is implemented based on teachings and material from CMPUT 267: Machine Learning I at the University of Alberta.

Let's get started!

# Part 1: Dataset Information

In this project, I use the **UCI Wine dataset**, which is a classic dataset often used for classification tasks.
It contains information about various chemical properties of wines derived from three different cultivars in the same region in Italy.
The features include alcohol content, malic acid, ash, alcalinity of ash, magnesium, total phenols, flavanoids, nonflavanoid phenols, proanthocyanins, color intensity, hue, OD280/OD315 of diluted wines, and proline,
with the labels being the cultivar of the wine (Barolo (0), Grignolino (1), Barbera (2)).
The dataset contains 178 data points. It was introduced by Forina et al. (1991) in their paper on chemical analysis.

Let's begin by loading the dataset and taking a closer look at what it contains.

### Loading the Dataset
"""

# Import necessary libraries
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from ipywidgets import interactive_output
import ipywidgets as widgets
from IPython.display import display, clear_output
from sklearn.preprocessing import PolynomialFeatures
from sklearn.datasets import load_wine
from sklearn.model_selection import train_test_split

# Set a fixed random seed for reproducibility
random_seed = 42

# Load the Wine dataset
wine = load_wine()

# Convert to a DataFrame
df = pd.DataFrame(wine.data, columns=wine.feature_names)
df['Class'] = wine.target

# Display some random rows of the dataset
df.sample(n=5, random_state=random_seed)

"""Now that I have loaded the dataset, I need to prepare it for use in my classification learner.

For better visualization of decision boundaries, I will only use 2 features in this project: alcohol and malic acid. I will store these features in a matrix $\mathbf{X}$ where each row represents a data point and each column represents a feature.
Additionally, I will store the labels (class) in a vector $\mathbf{Y}$.
"""

# Select only the alcohol and malic acid features for simplicity
X = df[['alcohol', 'malic_acid']].values
Y = df['Class'].values

# For binary classification, select class 0 (Barolo) and group the other two classes together to represent 1 (Not-Barolo)
binary_mask = Y == 0
Y_bin = np.where(binary_mask, 0, 1)

"""Next, we will split the data into training and testing sets. We will use 65% of the data for training and 35% for testing."""

# Split the data into training and testing sets
test_size = 0.35
X_train_bin, X_test_bin, Y_train_bin, Y_test_bin = train_test_split(X, Y_bin, test_size=test_size, random_state=random_seed)
X_train_mul, X_test_mul, Y_train_mul, Y_test_mul = train_test_split(X, Y, test_size=test_size, random_state=random_seed)

# Split the data into training and testing sets
test_size = 0.35
X_train_bin, X_test_bin, Y_train_bin, Y_test_bin = train_test_split(X, Y_bin, test_size=test_size, random_state=random_seed)
X_train_mul, X_test_mul, Y_train_mul, Y_test_mul = train_test_split(X, Y, test_size=test_size, random_state=random_seed)

"""### Plotting the Multiclass Dataset

The plot below visualizes the training and test sets for the multiclass classification dataset, which includes the Barolo, Grignolino, and Barbera classes.

In both plots you should see three distinct clusters of points representing the three classes.

# Part 2: Multiclass Classification

In multiclass classification, the set of labels $\mathcal{Y}$ contains more than 2 classes.
In our particular case, the set of labels $\mathcal{Y} = \{0, 1, 2\}$ represents the cultivar of the wine (Barolo, Grignolino, Barbera).
Thus, we will be using all the labels in our dataset from now on, represented as the matrix `Y`.
"""

# @title Plot

# Function to plot the training and testing sets for multiclass classification
def plot_multiclass_train_test(show_plot):
    if show_plot:
        fig, axes = plt.subplots(1, 2, figsize=(15, 6))

        # Plot training data
        axes[0].scatter(X_train_norm_mul[Y_train_mul == 0][:, 1], X_train_norm_mul[Y_train_mul == 0][:, 2], color='red', label='Barolo', s=50)
        axes[0].scatter(X_train_norm_mul[Y_train_mul == 1][:, 1], X_train_norm_mul[Y_train_mul == 1][:, 2], color='blue', label='Grignolino', s=50)
        axes[0].scatter(X_train_norm_mul[Y_train_mul == 2][:, 1], X_train_norm_mul[Y_train_mul == 2][:, 2], color='green', label='Barbera', s=50)
        axes[0].set_xlabel('Alcohol (normalized)')
        axes[0].set_ylabel('Malic Acid (normalized)')
        axes[0].set_title('Training Set')
        axes[0].set_ylim(-2.2, 3.8)
        axes[0].set_xlim(-2.8, 2.8)
        axes[0].legend()

        # Plot testing data
        axes[1].scatter(X_test_norm_mul[Y_test_mul == 0][:, 1], X_test_norm_mul[Y_test_mul == 0][:, 2], color='red', label='Barolo', s=50)
        axes[1].scatter(X_test_norm_mul[Y_test_mul == 1][:, 1], X_test_norm_mul[Y_test_mul == 1][:, 2], color='blue', label='Grignolino', s=50)
        axes[1].scatter(X_test_norm_mul[Y_test_mul == 2][:, 1], X_test_norm_mul[Y_test_mul == 2][:, 2], color='green', label='Barbera', s=50)
        axes[1].set_xlabel('Alcohol (normalized)')
        axes[1].set_ylabel('Malic Acid (normalized)')
        axes[1].set_title('Test Set')
        axes[1].set_ylim(-2.2, 3.8)
        axes[1].set_xlim(-2.8, 2.8)
        axes[1].legend()

        plt.show()
    else:
        clear_output()

# Create a checkbox widget
show_plot_checkbox_multiclass_train_test = widgets.Checkbox(value=False, description='Show Plot')

# Use interactive_output to link the function with the checkbox
interactive_plot_multiclass_train_test = interactive_output(plot_multiclass_train_test, {'show_plot': show_plot_checkbox_multiclass_train_test})

# Display the checkbox and the plot
display(show_plot_checkbox_multiclass_train_test, interactive_plot_multiclass_train_test)

"""For the final step of preprocessing, we will normalize the data and add a column of ones to the feature matrix to account for the bias term."""

# Normalize the features
X_mean_bin = X_train_bin.mean(axis=0)
X_std_bin = X_train_bin.std(axis=0) + 1e-8
X_train_norm_bin = (X_train_bin - X_mean_bin) / X_std_bin
X_test_norm_bin = (X_test_bin - X_mean_bin) / X_std_bin

X_mean_mul = X_train_mul.mean(axis=0)
X_std_mul = X_train_mul.std(axis=0) + 1e-8
X_train_norm_mul = (X_train_mul - X_mean_mul) / X_std_mul
X_test_norm_mul = (X_test_bin - X_mean_mul) / X_std_mul

# Append a column of 1s to the features for the bias term
X_train_norm_bin = np.hstack([np.ones((X_train_norm_bin.shape[0], 1)), X_train_norm_bin])
X_test_norm_bin = np.hstack([np.ones((X_test_norm_bin.shape[0], 1)), X_test_norm_bin])
X_train_norm_mul = np.hstack([np.ones((X_train_norm_mul.shape[0], 1)), X_train_norm_mul])
X_test_norm_mul = np.hstack([np.ones((X_test_norm_mul.shape[0], 1)), X_test_norm_mul])

"""## Implementing SoftMax function"""

def softmax(Z):
    """
    Compute the softmax of each row of the input array.

    Parameters:
    z (numpy array): Input array of shape (n, K) where n is the number of samples and K is the number of classes.

    Returns:
    result (numpy array): Softmax probabilities of shape (n, K).
    """

    result = np.zeros(Z.shape)
    for i in range(Z.shape[0]): #Gives n
        #Updating row by row
        result[i] = (np.exp(Z[i] - np.max(Z[i])))/(np.sum(np.exp(Z[i] - np.max(Z[i]))))


    return result

"""## Implementing BGS Regression Learner"""

def bgd_softmax_regression_learner(X, Y, step_size=0.01, epochs=10, random_seed=42):
    """
    Trains a softmax regression model using batch gradient descent.

    Parameters:
    X (numpy array): Feature matrix of size (n, d+1), where n is the number of samples
                     and d is the number of features. The first column should be all 1s.
    Y (numpy array): Target vector of size (n,) with class labels.
    step_size (float): The step size for gradient descent.
    epochs (int): The number of iterations to run gradient descent.
    random_seed (int, optional): The seed for the random number generator.

    Returns:
    predictor (function): A function that takes a feature vector or matrix and returns predicted probabilities.
    W (numpy array): The final weights after applying gradient descent for the specified epochs.
    """
    np.random.seed(random_seed)
    n, d = X[:, 1:].shape
    K = len(np.unique(Y))  # Number of classes
    W = np.random.randn(d+1, K)  # Initialize the weights randomly

    one_hot_y = np.zeros((n, K)) #Dimensions of one_hot matrix
    for i in range(n):
      one_hot_y[i, Y[i]] = 1

    for i in range(epochs):
      W -= step_size*(1/n)*(X.T @ (softmax(X @ W) - one_hot_y))

    def predictor(x):
        return softmax(x @ W)

    return predictor, W

"""## Implementing Cross Entropy Loss function"""

def multiclass_cross_entropy_loss(Y_pred, Y):
    """
    Compute the cross-entropy loss for multiclass classification.

    Parameters:
    Y_pred (numpy array): Predicted probabilities of shape (n, K) where n is the number of samples and K is the number of classes.
    Y (numpy array): True labels (0, 1, 2) of shape (n,).

    Returns:
    loss (numpy array): Cross-entropy loss of shape (n,).
    """
    # Clip predictions to avoid log(0)
    Y_pred = np.clip(Y_pred, 1e-15, 1 - 1e-15)

    loss = np.zeros(Y.shape)

    #Getting variables for Indicator function
    n = Y_pred.shape[0]
    K = Y_pred.shape[1]

    one_hot_y = np.zeros((n, K)) #Dimensions of one_hot matrix
    for i in range(n):
      one_hot_y[i, Y[i]] = 1

    for i in range(n):
        loss[i] = -(np.sum(one_hot_y[i] * np.log(Y_pred)))/n

    return loss

"""## Plotting the Estimated Zero-One Loss

Similar to the binary classification problem, we would like to evaluate the performance of the multiclass classification learner using the zero-one loss function.

If your implementation of `multiclass_cross_entropy_loss` is correct, you should see the zero-one loss decrease as the number of epochs increases in the plot below.
However, it likely will not decrease as smoothly as the cross-entropy loss, since the `bgd_softmax_regression_learner` is not directly minimizing the zero-one loss.
"""

# @title Plot

# Function to show/hide the plot
def plot_ce_zo_loss_multi(show_plot):
    # Define the number of epochs
    epochs = 200

    # Initialize lists to store the loss values
    cross_entropy_loss_values = []
    zero_one_loss_values = []

    # Train the model and compute the loss for each epoch
    for epoch in range(1, epochs + 1):
        predictor, W = bgd_softmax_regression_learner(X_train_norm_mul, Y_train_mul, step_size=0.1, epochs=epoch, random_seed=random_seed)
        loss = estimated_loss(predictor, X_train_norm_mul, Y_train_mul, multiclass_cross_entropy_loss)
        cross_entropy_loss_values.append(loss)

        # Compute 0-1 loss
        predictor_class, W = multiclass_classification_learner(X_train_norm_mul, Y_train_mul, step_size=0.1, epochs=epoch, random_seed=random_seed)
        zero_one_loss_value = estimated_loss(predictor_class, X_train_norm_mul, Y_train_mul, zero_one_loss)
        zero_one_loss_values.append(zero_one_loss_value)

    if show_plot:
        # Plot the loss values
        plt.figure(figsize=(10, 6))
        plt.plot(range(1, epochs + 1), cross_entropy_loss_values, label='Cross-Entropy Loss', linewidth=3)
        plt.plot(range(1, epochs + 1), zero_one_loss_values, label='Zero-One Loss', linewidth=3)
        plt.xlabel('Epochs')
        plt.ylabel('Estimated Loss')
        plt.legend()
        plt.grid(True)
        plt.show()
    else:
        clear_output()

# Create a checkbox widget
show_plot_checkbox_ce_zo_loss_multi = widgets.Checkbox(value=False, description='Show Plot')

# Use interactive_output to link the function with the checkbox
interactive_plot_ce_zo_loss_multi = interactive_output(plot_ce_zo_loss_multi, {'show_plot': show_plot_checkbox_ce_zo_loss_multi})

# Display the checkbox and the plot
display(show_plot_checkbox_ce_zo_loss_multi, interactive_plot_ce_zo_loss_multi)

"""## Plotting a Linear Decision Boundary

The multiclass classification predictor outputs the class with the highest probability.
Since the probability of a class $y \in \cal{Y}$ is given by $\sigma_y(\mathbf{x}^\top \mathbf{w}_y)$, it implies that the class with the highest probability is the class with the highest value of $\mathbf{x}^\top \mathbf{w}_y$.
If we have two different classes $y, y' \in \cal{Y}$, the decision boundary between these two classes is given by the line $\mathbf{x}^\top (\mathbf{w}_y - \mathbf{w}_{y'}) = 0$.
This line represents when the predicted probability of class $y$ is equal to the predicted probability of class $y'$.
Thus, anything to one side of the line will be predicted as class $y$ and anything to the other side will be predicted as class $y'$.

Below we plot this decision boundary for all possible pairs of classes.
"""

# @title Plot

# Function to show/hide the plot
def plot_db_multi(show_plot):
    # Function to plot the multiclass decision boundary
    def plot_multiclass_decision_boundary(X, Y, f, title, ax):
        # Create a mesh grid
        x_min, x_max = -2.8, 2.8  # Hardcoded x-limits
        y_min, y_max = -2.2, 3.8  # Hardcoded y-limits
        xx, yy = np.meshgrid(np.arange(x_min, x_max, 0.01),
                            np.arange(y_min, y_max, 0.01))

        # Compute the decision boundary
        Z = f(np.c_[np.ones((xx.ravel().shape[0], 1)), xx.ravel(), yy.ravel()])
        Z = Z.reshape(xx.shape)

        # Plot the decision boundary
        ax.contourf(xx, yy, Z, alpha=0.8, levels=[-1, 0, 1, 2], colors=['#FFAAAA', '#AAAAFF', '#AAFFAA'])
        ax.scatter(X[Y == 0][:, 1], X[Y == 0][:, 2], color='red', label='Barolo', s=50)
        ax.scatter(X[Y == 1][:, 1], X[Y == 1][:, 2], color='blue', label='Grignolino', s=50)
        ax.scatter(X[Y == 2][:, 1], X[Y == 2][:, 2], color='green', label='Barbera', s=50)
        ax.set_xlabel('Alcohol (normalized)')
        ax.set_ylabel('Malic Acid (normalized)')
        ax.set_title(title)

        # Hardcoded limits to ensure consistency across both plots
        ax.set_xlim(x_min, x_max)
        ax.set_ylim(y_min, y_max)
        ax.legend()

    epochs = 10000

    if show_plot:
        fig, axes = plt.subplots(1, 2, figsize=(15, 6))

        predictor, W = multiclass_classification_learner(X_train_norm_mul, Y_train_mul, step_size=0.1, epochs=epochs, random_seed=random_seed)
        # Plot the decision boundary on the training set
        plot_multiclass_decision_boundary(X_train_norm_mul, Y_train_mul, predictor, 'Training Set', axes[0])

        # Plot the decision boundary on the test set
        plot_multiclass_decision_boundary(X_test_norm_mul, Y_test_mul, predictor, 'Test Set', axes[1])

        plt.show()
    else:
        clear_output()

# Create a checkbox widget
show_plot_checkbox_db_multi = widgets.Checkbox(value=False, description='Show Plot')

# Use interactive_output to link the function with the checkbox
interactive_plot_db_multi = interactive_output(plot_db_multi, {'show_plot': show_plot_checkbox_db_multi})

# Display the checkbox and the plot
display(show_plot_checkbox_db_multi, interactive_plot_db_multi)

"""## Plotting Polynomial Decision Boundaries

We use polynomial features to allow for more complex decision boundaries in the multiclass classification problem.
Below is a plot of the decision boundary for different polynomial degrees $p$.
You should see that as $p$ increases the decision boundary becomes more complex and can better separate the three classes in the training set.
However, if $p$ is too large, then the decision boundary may become too complex and overfit the training data, leading to poor performance on the test set.
"""

# @title Plot

# Function to show/hide the plots and update the polynomial degree
def plot_db_multi_poly(show_plot, degree):
    # Define the decision boundary function for polynomial features
    def plot_multiclass_decision_boundary_poly(X, Y, f, degree, title, X_poly_mean=None, X_poly_std=None, ax=None):
        # Create a mesh grid
        x_min, x_max = -2.8, 2.8  # Hardcoded x-limits
        y_min, y_max = -2.2, 3.8  # Hardcoded y-limits
        xx, yy = np.meshgrid(np.arange(x_min, x_max, 0.01),
                            np.arange(y_min, y_max, 0.01))

        # Transform the mesh grid to polynomial features
        poly_features = phi_p(np.c_[xx.ravel(), yy.ravel()], degree)

        # Normalize the polynomial features using the same mean and std as the training set
        poly_features = (poly_features - X_poly_mean) / X_poly_std

        # Append a column of 1s to the features for the bias term
        poly_features = np.hstack([np.ones((poly_features.shape[0], 1)), poly_features])

        # Compute the decision boundary
        # Z = poly_features.dot(W)
        # Z = np.argmax(Z, axis=1)
        Z = f(poly_features)
        Z = Z.reshape(xx.shape)

        # Plot the decision boundary
        ax.contourf(xx, yy, Z, alpha=0.8, levels=[-1, 0, 1, 2], colors=['#FFAAAA', '#AAAAFF', '#AAFFAA'])
        ax.scatter(X[Y == 0][:, 1], X[Y == 0][:, 2], color='red', label='Barolo', s=50)
        ax.scatter(X[Y == 1][:, 1], X[Y == 1][:, 2], color='blue', label='Grignolino', s=50)
        ax.scatter(X[Y == 2][:, 1], X[Y == 2][:, 2], color='green', label='Barbera', s=50)
        ax.set_xlabel('Alcohol (normalized)')
        ax.set_ylabel('Malic Acid (normalized)')
        ax.set_ylim(y_min, y_max)
        ax.set_xlim(x_min, x_max)
        ax.set_title(title)
        ax.legend()

    epochs = 10000

    if show_plot:
        # Transform the input features to polynomial features of the selected degree
        X_poly_train = phi_p(X_train_norm_mul[:, 1:], degree)
        X_poly_test = phi_p(X_test_norm_mul[:, 1:], degree)

        # Normalize the polynomial features
        X_poly_mean = X_poly_train.mean(axis=0)
        X_poly_std = X_poly_train.std(axis=0) + 1e-8
        X_poly_train = (X_poly_train - X_poly_mean) / X_poly_std
        X_poly_test = (X_poly_test - X_poly_mean) / X_poly_std

        # Append a column of 1s to the features for the bias term
        X_poly_train = np.hstack([np.ones((X_poly_train.shape[0], 1)), X_poly_train])
        X_poly_test = np.hstack([np.ones((X_poly_test.shape[0], 1)), X_poly_test])

        # Train the model using polynomial features
        predictor_poly, w_poly = multiclass_classification_learner(X_poly_train, Y_train_mul, step_size=0.1, epochs=epochs, random_seed=random_seed)

        fig, axes = plt.subplots(1, 2, figsize=(15, 6))

        # Plot the decision boundary on the training set
        plot_multiclass_decision_boundary_poly(X_poly_train, Y_train_mul, predictor_poly, degree, f'Training Set (Polynomial Degree {degree})', X_poly_mean, X_poly_std, axes[0])

        # Plot the decision boundary on the test set
        plot_multiclass_decision_boundary_poly(X_poly_test, Y_test_mul, predictor_poly, degree, f'Test Set (Polynomial Degree {degree})', X_poly_mean, X_poly_std, axes[1])

        plt.show()
    else:
        clear_output()

# Create a checkbox widget
show_plot_checkbox_db_multi_poly = widgets.Checkbox(value=False, description='Show Plot')

# Create a slider widget for selecting the polynomial degree
degree_slider_db_multi_poly = widgets.IntSlider(value=1, min=1, max=10, step=0.5, description='Degree')

# Use interactive_output to link the function with the checkbox and slider
interactive_plot_db_multi_poly = interactive_output(plot_db_multi_poly, {'show_plot': show_plot_checkbox_db_multi_poly, 'degree': degree_slider_db_multi_poly})

# Display the checkbox, slider, and the plot
display(show_plot_checkbox_db_multi_poly, degree_slider_db_multi_poly, interactive_plot_db_multi_poly)