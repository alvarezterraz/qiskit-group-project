# Variational Quantum Image Classifier

A hybrid quantum-classical machine learning approach for classifying geometric patterns in images using a quantum neural network implemented with Qiskit.

Made by the Team 5 in the Road To Practitioner Program from IBM and BasQ.

May 2025.

## Team (5) members

1. Iñigo Vilaseco Extramiana
2. Ignacio Fernández Losa
3. Pedro José Álvarez Terraz
4. Diego Mallada Conte
5. Adrián Gustavo del Pozo Martín 
6. Arturo Juárez Carrillo

## Project Overview

This project implements a Variational Quantum Image Classifier that can identify different geometric patterns (horizontal, vertical, and diagonal lines) in N×N pixel images. The classifier leverages quantum computing principles to potentially offer advantages over classical machine learning approaches for specific pattern recognition tasks.

The implementation uses a hybrid quantum-classical approach where:
- Image data is encoded into quantum states using parameterized quantum circuits 
- A custom ansatz with entangling gates captures spatial relationships between pixels
- A classical optimizer tunes the quantum circuit parameters to minimize classification error
- Quantum simulation is supported, and the final model can be executed on real quantum hardware

This work is part of the IBM Quantum Road to Practitioners (R2P) Program, exploring practical applications of quantum computing in machine learning and pattern recognition domains.

## Key Features

- **Quantum Data Encoding**: Each image pixel is encoded into a quantum state using ZFeatureMap, creating a one-to-one mapping between pixels and qubits
- **Spatially-Aware Quantum Circuit**: Custom ansatz design with entangling connections that preserve and leverage the 2D spatial structure of image data
- **Multi-Class Classification**: Classifies patterns into three categories (horizontal, vertical, and diagonal lines) using a single observable measurement
- **Optimized Circuit Design**: Implementation of circuit optimization techniques to reduce gate depth and improve execution efficiency on real quantum hardware
- **Hardware Execution**: Support for running on both quantum simulators and real IBM Quantum hardware with resilience options
- **Batch Processing**: Mini-batch gradient descent implementation to handle larger datasets efficiently
- **Circuit Transpilation**: Advanced transpilation techniques to find optimal circuit representations for specific quantum hardware architectures

## Dataset

The project uses a synthetic dataset of n×n pixel images (default 3×3) containing three pattern classes:
- Horizontal lines (class -1)
- Vertical lines (class +1)
- Diagonal lines (class 0)

Each image is generated with carefully positioned lines (of specified length) and random noise applied to non-line pixels to create a challenging classification task. The dataset generation process allows for customizing:
- Image dimensions
- Line length
- Noise characteristics 
- Dataset size

The synthetic nature of the dataset provides a controlled environment for evaluating the quantum classifier's performance and enables exploring how quantum machine learning approaches handle spatial pattern recognition tasks.

## Project Structure

The project is organized in a Jupyter notebook (`VariationalQuantumClassifier.ipynb`) with the following sections:

1. **Database Creation**: Code for generating synthetic image datasets with different line patterns
2. **Qubit Mapping**: Implementation of feature encoding using ZFeatureMap to convert classical image data into quantum states
3. **Ansatz Construction**: Design of a custom variational quantum circuit with spatial connectivity matching the 2D structure of the image data
4. **Observable Definition**: Creation of a measurement observable using Pauli Z operators
5. **Forward Pass and Loss Functions**: Implementation of the quantum network forward pass and MSE loss function
6. **Circuit Optimization**: Techniques for optimizing circuit execution on quantum hardware
7. **Training Process**: Mini-batch training approach using classical optimization (COBYLA)
8. **Post-processing and Evaluation**: Analysis of classifier performance and visualization of results
9. **Hardware Execution**: Circuit optimization and execution on real quantum hardware

## Technologies Used

- **Qiskit**: Core quantum computing framework for circuit design, simulation, and hardware execution
- **NumPy**: For numerical operations and dataset manipulation
- **Matplotlib**: For visualization of images and results
- **scikit-learn**: For dataset splitting, evaluation metrics, and classical ML components
- **SciPy**: For optimization algorithms (COBYLA)
- **IBM Quantum Platform**: For access to real quantum hardware
- **Jupyter Notebooks**: For interactive development and documentation

## Installation and Usage

### Prerequisites
- Python 3.8+
- An IBM Quantum account (free)

### Installation
```bash
# Clone the repository
git clone https://github.com/yourusername/qiskit-group-project.git
cd qiskit-group-project

# Create a virtual environment (optional but recommended)
python -m venv venv
source venv/bin/activate  # On Windows, use: venv\Scripts\activate

# Install required packages
pip install qiskit qiskit-ibm-runtime numpy matplotlib scikit-learn scipy jupyter
```

### Configuration for IBM Quantum Hardware
To run on real quantum hardware:
1. Set up your IBM Quantum account credentials
2. Ensure you have the qiskit-ibm-runtime package installed
3. Modify the backend selection in the hardware execution section

## License

This project is licensed under CC0 1.0 Universal - see the LICENSE file for details.

## Acknowledgments

Special thanks to IBM Quantum for providing the Road to Practitioners (R2P) Program and the quantum computing resources necessary for this project. We also acknowledge the contributions of the broader quantum computing community and the educational resources that made this work possible.

