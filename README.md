# Quantum Neural Network Image Classifier

This repository contains the capstone project developed as part of the IBM Road to Practitioner (R2P) Program. Our team of 6 members has created a quantum-enhanced image classification system using IBM's Qiskit framework.

## Team members

1. Iñigo Vilaseco
2. Ignacio Fernández
3. Pedro Álvarez
4. Diego Mallada Conte
5. Adrián Gustavo del Pozo Martín 
6. Arturo Juárez

## Project Overview

The project demonstrates the application of quantum computing in machine learning by implementing a Quantum Neural Network (QNN) for image classification. Specifically, we've developed a system that can distinguish between simple geometric shapes (circles and crosses) using quantum kernel estimation techniques.

## Key Features

- Custom 8x8 pixel image dataset creation tool
- Quantum kernel-based classification system
- Integration with IBM Qiskit for quantum computations
- Comparative analysis between classical and quantum approaches

## Dataset

The project uses a custom dataset consisting of:
- 60 total images (circles and crosses)
- 40 training images (20 circles, 20 crosses)
- 20 testing images (10 circles, 10 crosses)

The dataset was created using our custom `symbols_maker.py` tool, which allows for:
- Manual drawing on an 8x8 pixel grid
- Export to both CSV and PNG formats
- Automatic labeling and vectorization of images

## Project Structure

- `NeuralNetworkClassifier.ipynb`: Main implementation of the quantum neural network classifier
- `symbols_maker.py`: Tool for creating and saving custom image patterns
- `circles.csv` & `crosses.csv`: Dataset files containing the vectorized images
- `Pruebas.ipynb`: Notebook containing experimental tests and validations

## Technologies Used

- IBM Qiskit: Quantum computing framework
- Python: Programming language
- Pandas: Data manipulation and analysis
- NumPy: Numerical computing
- Matplotlib: Data visualization

## Installation and Usage

1. Clone this repository
2. Install required dependencies:
   ```bash
   pip install qiskit pandas numpy matplotlib
   ```
3. Run the Jupyter notebooks to see the implementation and results
4. Use `symbols_maker.py` to create new training data if desired


## License

This project is licensed under the terms included in the LICENSE file.

## Acknowledgments

Special thanks to IBM Quantum for providing the R2P Program and the quantum computing resources necessary for this project.

