# Use the official Anaconda base image
FROM continuumio/anaconda3:latest

# Set environment variables
ENV PYSPARK_VERSION=3.3.2
ENV CONDA_ENV=lasagna

# Update conda and create a new environment
RUN conda update -n base -c defaults conda && \
    conda create -n $CONDA_ENV python=3.11 anaconda && \
    echo "conda activate $CONDA_ENV" >> ~/.bashrc

# Activate the environment
SHELL ["/bin/bash", "--login", "-c"]
RUN source activate $CONDA_ENV && \
    conda install -c conda-forge pyspark=$PYSPARK_VERSION findspark jupyterlab && \
    conda install -c conda-forge nodejs

# Set the default command to launch Jupyter Lab
CMD ["jupyter", "lab", "--ip=0.0.0.0", "--port=8888", "--no-browser", "--allow-root"]