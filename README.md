# Atlas Parser
improving accuracy for LLMs.

![image](https://github.com/user-attachments/assets/ffbfa706-f467-4564-98c6-964c6c403919)


## About
Uses Marker to convert PDFs into readable formats that is ready to be used for any LLMs. 
<br>
Coded for the LACC Techbootcamp Team Atlas


## Installation
Install Dependecies *(Recommended to use a virtual environment!)*

Firstly, we install **Marker-PDF**
```
pip install marker-pdf
```

Secondly, since we are using Pytorch, installation differs depending on what operating system you are currently using.<br>
Go to [PyTorch](https://pytorch.org/) and find the **Install PyTorch** section.
![image](https://github.com/user-attachments/assets/b93efc85-168f-4a41-a3ad-31de126cbc55)
<br>
Run the given command and you are good to go.

## Usage
Running the Web Application
```
python main.py
```

## Examples
**MarCO Research Paper**
Converted the PDF Research Paper of MarCO into Markdown with it's images separated.
- https://github.com/Dichill/AtlasParser/blob/main/output/DESCANSO18_MarCO/DESCANSO18_MarCO.md

## Resources
- https://github.com/VikParuchuri/marker | Marker converts PDF to markdown quickly and accurately.
- Gradio                                 | For the Frontend.

