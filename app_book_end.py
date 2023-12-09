#!/usr/bin/env python
# coding: utf-8
import pandas as pd 
import numpy as np 
import pickle 
import streamlit as st 
from PIL import Image 
import datetime
import lightgbm
st.set_page_config(
        page_title="Расчет вероятности отмены бронирования", page_icon = 'favicon.ico'
)
#Display Logo
# import Image from pillow to open images
img = Image.open("logo.png")
day = datetime.datetime.today().strftime('%d.%m.%Y')
today = datetime.datetime.now()
st.write('Сегодня:',day)
# display image using streamlit
# width is used to set the width of an image
st.image(img, width=100)



# loading in the model to predict on the data 
pickle_in = open('model_cat_1.pkl', 'rb') 
classifier = pickle.load(pickle_in) 

# defining the function which will make the prediction using 
# the data which the user inputs 
def prediction_prob(come_from, status, alder, child, days_to_arrive, days_to_stay, room_class): 
	prediction = classifier.predict_proba( 
		[[come_from, status, alder, child, days_to_arrive, days_to_stay, room_class]])[:,1] 
	print(prediction) 
	return prediction 

def prediction(come_from, status, alder, child, days_to_arrive, days_to_stay, room_class): 
	prediction = classifier.predict( 
		[[come_from, status, alder, child, days_to_arrive, days_to_stay, room_class]]) 
	print(prediction) 
	return prediction 


# this is the main function in which we define our webpage 
def main(): 
	# here we define some of the front end elements of the web page like 
	# the font and background color, the padding and the text to be displayed 
	html_temp = """ 
	<div style ="background-color:#e5e5e5;padding:13px;text-align:center;"> 
	<h1 style ="color:#e1ad4f;text-align:center;">Вероятность отмены бронирования: </h1> 
    <h3 style ="color:#e1ad4f;text-align:center;">Модель машинного обучения</h3> 
    <p style="text-align:center;">Модель позволяет на основе накопленных данных прогнозировать вероятность отмены бронирования. Для проведения расчета введите неообходимые данные: </p>
	</div> 
	"""
	st.markdown(html_temp, unsafe_allow_html = True) 
	next_year = today.year + 1
	# the data required to make the prediction 
	booking_date = st.date_input("Дата бронирования", datetime.date(next_year,1,31))
    #
	st.warning("Обязательно выберите две даты!")
	jan_1 = datetime.date(next_year, 1, 1)
	dec_31 = datetime.date(next_year, 12, 31)
	min_date, max_date = st.date_input(
	"Выберите даты на которые забронировал клиент:",
	(jan_1, datetime.date(next_year, 1, 2)),
	jan_1,
	dec_31,
	format="MM.DD.YYYY")
	days_to_stay = max_date-min_date
	days_to_stay = float(days_to_stay.days)
	days_to_arrive = min_date - booking_date
	days_to_arrive = float(days_to_arrive.days)
	#st.write("Клиент выбрал следующие даты:", min_date, max_date, days_to_stay, days_to_arrive )
	
	# Selection box - источник бронирования
	come_from = st.selectbox("Источник бронирования: ",
                     ['Модуль бронирования', 'Прямой', 'Яндекс.Путешествия', 'Ostrovok (Emerging Travel Group)', 'Tvil', 'AllHotelsMarket', 'Алеан', 'Google', 'OneTwoTrip!'])
	come_from = str(come_from)
	# print selected 
	#st.write("Источник бронирования: ", come_from)

	# Selection box - источник бронирования
	room_class = st.selectbox("Класс номера: ",
                     ['Одноместный', 'Стандарт без балкона', 'Стандартный', 'Люкс', 'Супер Люкс'])
	room_class = str(room_class)

	# radio button
	status = st.radio("Тариф: ", ('Завтрак', 'Всё включено'))
	status = str(status) 

	# slider alder
 
	# first argument takes the title of the slider
	# second argument takes the starting of the slider
	# last argument takes the end number
	alder = st.slider("Количество взрослых:", 1, 6)
	alder = str(alder) 
	# print the level
	# format() is used to print value 
	# of a variable at a specific position
	st.text('Количество взрослых: {}'.format(alder))
	# slider child
 
	# first argument takes the title of the slider
	# second argument takes the starting of the slider
	# last argument takes the end number
	child = st.slider("Количество детей:", 0, 3)
	child = str(child) 
	# print the level
	# format() is used to print value 
	# of a variable at a specific position
	st.text('Количество детей: {}'.format(child))
	result ="" 
	predict ="" 
	# the below line ensures that when the button called 'Predict' is clicked, 
	# the prediction function defined above is called to make the prediction 
	# and store it in the variable result 
	if st.button("Узнать вероятность отмены бронирования"): 
		result = prediction_prob(come_from, status, alder, child, days_to_arrive, days_to_stay, room_class) 
		result = int(round(float(result),2)*100)
		predict = prediction(come_from, status, alder, child, days_to_arrive, days_to_stay, room_class) 
		predict = int(round(float(predict),2)*100)
	st.info('Вероятность отмены составляет {} %'.format(result)) 
	if predict == 0:
		st.success("Низкая вероятность отмены")
	else:
		st.error('Высокая вероятность отмены')
if __name__=='__main__': 
	main() 


