# celebrity_faces
Проект сайта "на какую знаменитость ты похож". 

#### Архитектура.
Состоит из трех сервисов.
1. Веб-морда. Страничка загрузки пользовательской картинки и страничка с результатами. Полученную картинку посылает на сервис эмбеддинга и получает эмбеддинг. Полученный эмбеддинг посылает сервису индекса и получает имя файла с фото самой похожей знаменитости, которое отображается на страничке с результатами. 
2. Сервис эмбеддинга. Принимает картинку через POST-запрос, выделяет лицо и делает необходимую предобработку для [facenet](https://github.com/davidsandberg/facenet) и считает эмбеддинг по предобученной модели facenet. 
3. Сервис индекса. Строит индекс по предварительно подсчитанным эмбеддингам для raw celebrities, принимает POST-запросы с векторами, возвращает имя картинки, соответствующей ближайшему вектору. Пока что в качестве индекса используется [Annoy](https://github.com/spotify/annoy) и поиск проихсходит по урезанному датасету из ~13k картинок из lfw dataset.
4. Все сервисы запускаются в docker'ах через docker-compose.
Все сервисы написаны на Python/Flask.

#### Что изменилось с промежуточного дедлайна и что нужно доделать.
1. Написан на C++ идекс будет основан на [Navigable Small World algorithm](https://publications.hse.ru/mirror/pubs/share/folder/x5p6h7thif/direct/128296059), который подключается через cython. Нужно пофиксить тип выдачи поиска соседей и заменить на него annoy. 
2. Добавлены тесты accuracy для нейросети и индекса. Когда индекс будет пофиксен, будет сравнение accuracy своего индекс и annoy на датасетах, которые использовались для [тестирования annoy](https://github.com/spotify/annoy/blob/master/test/accuracy_test.py).
3. Замена датасета лиц знаменитостей на CelebA в процессе досчитывания векторов для изображений в датасете.
