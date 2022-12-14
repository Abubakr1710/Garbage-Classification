from cgi import test
from secrets import choice
import streamlit as st
import torch
from  torchvision import datasets, transforms, models
import numpy as np
from PIL import Image
import io
st.set_option('deprecation.showfileUploaderEncoding', False)
@st.cache(allow_output_mutation=True)

def load_model():
    model = models.resnext50_32x4d(pretrained=True)
    inputs = model.fc.in_features
    outputs = 6

    model.fc = torch.nn.Linear(inputs, outputs)
    model.load_state_dict(torch.load(
        'model.pth'))

    return model

def load_labels():
    labels_path = 'labels.txt'
    with open(labels_path, "r") as f:
        categories = [s.strip() for s in f.readlines()]
        return categories

def predict(model, categories, image):
    preprocess = transforms.Compose([
        transforms.Resize((120,120)),
        transforms.CenterCrop(100),
        transforms.ToTensor(),
        transforms.Normalize(
            mean=[0.485, 0.456, 0.406],
            std=[0.229, 0.224, 0.225]),
    ])
    input_tensor = preprocess(image)
    input_batch = input_tensor.unsqueeze(0)
    model.eval()
    with torch.no_grad():
        output = model(input_batch)

    probabilities = torch.nn.functional.softmax(output, dim=1)[0] * 100
    st.header("This is a " + categories[np.argmax(probabilities)])



def load_image():
    uploaded_file = st.file_uploader(
        label='Pick an image to test', type=["jpg", "png", 'jpeg'])
    if uploaded_file is not None:
        image_data = uploaded_file.getvalue()
        st.image(image_data, caption="Input Image", width=500)
        return Image.open(io.BytesIO(image_data))

    else:
        st.write('Waiting for upload....')
        return None

st.sidebar.image('images/picture.png', width=300)
st.sidebar.markdown("<h1 style='text-align: center; color: black;'><a href= 'https://abubakr1710-my-website-app-kx4y2h.streamlit.app/'>Abubakr Mamajonov</a></h1>", unsafe_allow_html=True)
#st.title('Garbage Classification')
menu = ['Home', 'Test']
choice = st.sidebar.selectbox('Menu', menu)
if choice == 'Home':
    st.markdown("<h1 style='text-align: center; color: black;'>Garbage Classifier</h1>", unsafe_allow_html=True)
    image = 'images/box.jpeg'
    st.image(image, width=700, caption='Waste management-Global problem')
    st.write('Humans produce millions of tons of garbage everyday. Garbage needs to be segregated before it is taken out of houses. Sometimes people are so lazy to do like that. It is time to automate it')
    st.subheader('Some informations about the data:')
    st.write('Dataset contains 6 type of garbage such as:')
    st.write('1.Cardboard')
    st.write('2.Glass')
    st.write('3.Metal')
    st.write('4.Paper')
    st.write('5.Plastic')
    st.write('6.Trash')
    image = 'images/type.png'
    st.image(image, width=700)

    



elif choice == 'Test':
    st.subheader("Let's test the model")
    def main():

        model = load_model()
        categories = load_labels()
        image = load_image()
        result = st.button('Run on image')

        if result:
            predict(model, categories, image)

    if __name__ == '__main__':
        main()


