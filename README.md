# celebrity_faces
Проект сайта "на какую знаменитость ты похож". 


#### Отчет.
Состоит из трех сервисов.
1. Веб-морда. Страничка загрузки пользовательской картинки и страничка с результатами. Полученную картинку посылает на сервис эмбеддинга и получает эмбеддинг. Полученный эмбеддинг посылает сервису индекса и получает имя файла с фото самой похожей знаменитости, которое отображается на страничке с результатами. 
2. Сервис эмбеддинга. Принимает картинку через POST-запрос, выделяет лицо и делает необходимую предобработку для [facenet](https://github.com/davidsandberg/facenet) и считает эмбеддинг по предобученной модели facenet. Используются фото знаменитостей датасета [CelebA](http://mmlab.ie.cuhk.edu.hk/projects/CelebA.html). [Тест accuracy на датасете LFW](https://github.com/YuliaNikonova/celebrity_faces/blob/master/nn_embeddings/test_nn_lfw.ipynb). [Примеры наиболее похожих фото на датасете CelebA](https://github.com/YuliaNikonova/celebrity_faces/blob/master/examples_nn_celeba.ipynb).
3. Сервис индекса. Строит индекс по предварительно подсчитанным эмбеддингам для raw celebrities, принимает POST-запросы с векторами, возвращает имя картинки, соответствующей ближайшему вектору. Пока что в качестве индекса используется [Annoy](https://github.com/spotify/annoy). Написан на C++ идекс [Navigable Small World algorithm](https://publications.hse.ru/mirror/pubs/share/folder/x5p6h7thif/direct/128296059), который подключается через cython, но возникает проблема при отдаче результата работы плюсового кода в питон. Предполагалось тестить его accuracy на 1000 посчитанных facenet эмбеддингов датасета CelebA https://github.com/YuliaNikonova/celebrity_faces/blob/nsw_index_to_work/index/accuracy_test.py.
4. Все сервисы запускаются в docker'ах через docker-compose.
Все сервисы написаны на Python/Flask.


