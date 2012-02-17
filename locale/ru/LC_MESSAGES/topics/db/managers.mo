��    ;      �  O   �        N   	  �   X  d     c   l     �    �  �       �  �  �	  K  /  �  {  #        C  %   S  �   y     �  ?   �  �  <  �     �   �     i  �  w  �   ;  *  �    �  �   
  I  �  ~   ;  �   �     J     b     p  �  y  �  *  #   �  �   �    �   8   �!    �!  �   �#    �$  �   �%  �   �&  �   ''  �  (  �   �)  �   )*  �  +  �   �,  (   �-  �   �-  �   j.  �   /  �   �/  ?   G0  R  �0  �   �1  �   �2  �  .3  T   �4  �   5  �   �5  �   �6  7   97  �  q7  �   ?9  `  #:  n  �;    �=  �  �?  M   �B  )   C  T   @C    �C  �  �D  `   HF  �  �F  �   �I  J  RJ     �K  )  �K    �N  s  �O  �  hQ  �  S  C  �T  �   X    �X  %    Z     &Z     @Z  �  SZ    �\  @   _  �   \_  ,  M`  Z   za    �a  -  �d  >  f  �   Qh    &i  �  @j  �  �k  �   �m  �  �n  
  Rp  �  ]r  m   ;t  �   �t  �   |u  �   'v  �   �v  r   �w    8x  �   Hz  �   D{     6      ;   0      /                "              1       :   7       '          2   $   .   &                    %         4                       !   -            #                       ,       *   (             9       +   8      	   3       5      
   )                           ...the statement ``Book.objects.all()`` will return all books in the database. A ``Manager`` is the interface through which database query operations are provided to Django models. At least one ``Manager`` exists for every model in a Django application. A ``Manager``'s base ``QuerySet`` returns all objects in the system. For example, using this model:: A custom ``Manager`` method can return anything you want. It doesn't have to return a ``QuerySet``. Adding extra Manager methods Adding extra ``Manager`` methods is the preferred way to add "table-level" functionality to your models. (For "row-level" functionality -- i.e., functions that act on a single instance of a model object -- use :ref:`Model methods <model-methods>`, not custom ``Manager`` methods.) Another thing to note about this example is that ``Manager`` methods can access ``self.model`` to get the model class to which they're attached. As already suggested by the `django.contrib.gis` example, above, the ``use_for_related_fields`` feature is primarily for managers that need to return a custom ``QuerySet`` subclass. In providing this functionality in your manager, there are a couple of things to remember. By default, Django adds a ``Manager`` with the name ``objects`` to every Django model class. However, if you want to use ``objects`` as a field name, or if you want to use a name other than ``objects`` for the ``Manager``, you can rename it on a per-model basis. To rename the ``Manager`` for a given class, define a class attribute of type ``models.Manager()`` on that model. For example:: By default, Django uses an instance of a "plain" manager class when accessing related objects (i.e. ``choice.poll``), not the default manager on the related object. This is because Django needs to be able to retrieve the related object, even if it would otherwise be filtered out (and hence be inaccessible) by the default manager. Class inheritance and model managers aren't quite a perfect match for each other. Managers are often specific to the classes they are defined on and inheriting them in subclasses isn't necessarily a good idea. Also, because the first manager declared is the *default manager*, it is important to allow that to be controlled. So here's how Django handles custom managers and :ref:`model inheritance <model-inheritance>`: Controlling automatic Manager types Custom Managers Custom managers and model inheritance Django makes shallow copies of manager objects during certain queries; if your Manager cannot be copied, those queries will fail. Django provides a way for custom manager developers to say that their manager class should be used for automatic managers whenever it is the default manager on a model. This is done by setting the ``use_for_related_fields`` attribute on the manager class:: Do not filter away any results in this type of manager subclass Finally for this example, suppose you want to add extra managers to the child class, but still use the default from ``AbstractBase``. You can't add the new manager directly in the child class, as that would override the default and you would have to also explicitly include all the managers from the abstract base class. The solution is to put the extra managers in another base class and introduce it into the inheritance hierarchy *after* the defaults:: For example, the following model has *two* ``Manager``\s -- one that returns all objects, and one that returns only the books by Roald Dahl:: For example, this custom ``Manager`` offers a method ``with_counts()``, which returns a list of all ``OpinionPoll`` objects, each with an extra ``num_responses`` attribute that is the result of an aggregate query:: For example:: Given the purpose for which it's used, the name of this attribute (``use_for_related_fields``) might seem a little odd. Originally, the attribute only controlled the type of manager used for related field access, which is where the name came from. As it became clear the concept was more broadly useful, the name hasn't been changed. This is primarily so that existing code will :doc:`continue to work </misc/api-stability>` in future Django versions. Here, ``default_manager`` is the default. The ``objects`` manager is still available, since it's inherited. It just isn't used as the default. If the normal plain manager class (:class:`django.db.models.Manager`) is not appropriate for your circumstances, you can force Django to use the same class as the default manager for your model by setting the `use_for_related_fields` attribute on the manager class. This is documented fully below_. If this attribute is set on the *default* manager for a model (only the default manager is considered in these situations), Django will use that class whenever it needs to automatically create a manager for the class.  Otherwise, it will use :class:`django.db.models.Manager`. If you override the ``get_query_set()`` method and filter out any rows, Django will return incorrect results. Don't do that. A manager that filters results in ``get_query_set()`` is not appropriate for use as an automatic manager. If you use custom ``Manager`` objects, take note that the first ``Manager`` Django encounters (in the order in which they're defined in the model) has a special status. Django interprets the first ``Manager`` defined in a class as the "default" ``Manager``, and several parts of Django (including :djadmin:`dumpdata`) will use that ``Manager`` exclusively for that model. As a result, it's a good idea to be careful in your choice of default manager in order to avoid a situation where overriding ``get_query_set()`` results in an inability to retrieve objects you'd like to work with. If you use this directly in a subclass, ``objects`` will be the default manager if you declare no managers in the base class:: If you want to inherit from ``AbstractBase``, but provide a different default manager, you can provide the default manager on the child class:: Implementation concerns Manager names Managers Managers defined on non-abstract base classes are *not* inherited by child classes. If you want to reuse a manager from a non-abstract base, redeclare it explicitly on the child class. These sorts of managers are likely to be fairly specific to the class they are defined on, so inheriting them can often lead to unexpected results (particularly as far as the default manager goes). Therefore, they aren't passed onto child classes. Managers from abstract base classes are always inherited by the child class, using Python's normal name resolution order (names on the child class override all others; then come names on the first parent class, and so on). Abstract base classes are designed to capture information and behavior that is common to their child classes. Defining common managers is an appropriate part of this common information. Modifying initial Manager QuerySets Of course, because ``get_query_set()`` returns a ``QuerySet`` object, you can use ``filter()``, ``exclude()`` and all the other ``QuerySet`` methods on it. So these statements are all legal:: One reason an automatic manager is used is to access objects that are related to from some other model. In those situations, Django has to be able to see all the objects for the model it is fetching, so that *anything* which is referred to can be retrieved. Set ``use_for_related_fields`` when you define the class Sometimes this default class won't be the right choice. One example is in the :mod:`django.contrib.gis` application that ships with Django itself. All ``gis`` models must use a special manager class (:class:`~django.contrib.gis.db.models.GeoManager`) because they need a special queryset (:class:`~django.contrib.gis.db.models.GeoQuerySet`) to be used for interacting with the database.  It turns out that models which require a special manager like this need to use the same manager class wherever an automatic manager is created. The ``use_for_related_fields`` attribute must be set on the manager *class*, not on an *instance* of the class. The earlier example shows the correct way to set it, whereas the following will not work:: The default manager on a class is either the first manager declared on the class, if that exists, or the default manager of the first abstract base class in the parent hierarchy, if that exists. If no default manager is explicitly declared, Django's normal default manager is used. The way ``Manager`` classes work is documented in :doc:`/topics/db/queries`; this document specifically touches on model options that customize ``Manager`` behavior. There are two reasons you might want to customize a ``Manager``: to add extra ``Manager`` methods, and/or to modify the initial ``QuerySet`` the ``Manager`` returns. These rules provide the necessary flexibility if you want to install a collection of custom managers on a group of models, via an abstract base class, but still customize the default manager. For example, suppose you have this base class:: This document has already mentioned a couple of places where Django creates a manager class for you: `default managers`_ and the "plain" manager used to `access related objects`_. There are other places in the implementation of Django where temporary plain managers are needed. Those automatically created managers will normally be instances of the :class:`django.db.models.Manager` class. This example allows you to request ``Person.men.all()``, ``Person.women.all()``, and ``Person.people.all()``, yielding predictable results. This example also pointed out another interesting technique: using multiple managers on the same model. You can attach as many ``Manager()`` instances to a model as you'd like. This is an easy way to define common "filters" for your models. This won't be an issue for most custom managers. If you are just adding simple methods to your ``Manager``, it is unlikely that you will inadvertently make instances of your ``Manager`` uncopyable. However, if you're overriding ``__getattr__`` or some other private method of your ``Manager`` object that controls object state, you should ensure that you don't affect the ability of your ``Manager`` to be copied. Throughout this section, we will use the term "automatic manager" to mean a manager that Django creates for you -- either as a default manager on a model with no managers, or to use temporarily when accessing related objects. Using managers for related object access Using this example model, ``Person.objects`` will generate an ``AttributeError`` exception, but ``Person.people.all()`` will provide a list of all ``Person`` objects. Whatever features you add to your custom ``Manager``, it must be possible to make a shallow copy of a ``Manager`` instance; i.e., the following code must work:: With this example, you'd use ``OpinionPoll.objects.with_counts()`` to return that list of ``OpinionPoll`` objects with ``num_responses`` attributes. With this sample model, ``Book.objects.all()`` will return all books in the database, but ``Book.dahl_objects.all()`` will only return the ones written by Roald Dahl. Writing correct Managers for use in automatic Manager instances You also shouldn't change the attribute on the class object after it has been used in a model, since the attribute's value is processed when the model class is created and not subsequently reread. Set the attribute on the manager class when it is first defined, as in the initial example of this section and everything will work smoothly. You can override a ``Manager``\'s base ``QuerySet`` by overriding the ``Manager.get_query_set()`` method. ``get_query_set()`` should return a ``QuerySet`` with the properties you require. You can use a custom ``Manager`` in a particular model by extending the base ``Manager`` class and instantiating your custom ``Manager`` in your model. Project-Id-Version: Django 1.4
Report-Msgid-Bugs-To: 
POT-Creation-Date: 2012-02-15 15:13
PO-Revision-Date: 2012-02-17 19:07+0200
Last-Translator: Automatically generated
Language-Team: none
MIME-Version: 1.0
Content-Type: text/plain; charset=UTF-8
Content-Transfer-Encoding: 8bit
Language: ru
Plural-Forms: nplurals=3; plural=(n%10==1 && n%100!=11 ? 0 : n%10>=2 && n%10<=4 && (n%100<10 || n%100>=20) ? 1 : 2);
 ...``Book.objects.all()`` вернет все книги из базы данных. Менеджер(``Manager``) - это интерфейс, через который создаются запросы к моделям Django. Каждая модель имеет хотя бы один менеджер. Базовый ``QuerySet`` менеджера возвращает все объекты модели. Возьмем для примера эту модель:: Методы ``Manager`` могут возвращать что угодно. И это не обязательно должен быть ``QuerySet``. Добавление методов в менеджер Добавление дополнительных методов в ``Manager`` - лучший способ добавить "table-level" функционал в вашу модель. (Для "row-level" функционала -- то есть функции, которые работают с одним экземпляром модели -- используйте :ref:`методы модели <model-methods>`, а не методы менеджера.) Стоит отметить, что методы ``Manager`` могут обращаться к ``self.model`` что бы получить класс модели, которая использует этот менеджер. Как уже упоминалось в примере о `django.contrib.gis`, ``use_for_related_fields`` используется для возвращения специального подкласса ``QuerySet``. Реализуя подобный функционал необходимо помнить о нескольких правилах. По-умолчанию Django добавляет ``Manager`` с именем ``objects`` для каждого класса модели. Однако, если вы хотите использовать ``objects``, как имя поля, или хотите использовать название отличное от ``objects`` для ``Manager``, вы можете переименовать его для модели. Что бы переименовать ``Manager`` добавьте в класс атрибут, значение которого экземпляр ``models.Manager()``. Например:: По-умолчанию, Django использует "обычный" класс менеджера для получения связанных объектов (например, ``choice.poll``), а не менеджер по-умолчанию связанной модели. Это связано с тем, что Django необходимо получить все связанные объекты, без каких либо фильтров применяемых менеджером по-умолчанию. Наследование моделей и менеджеры взаимодействуют не совсем просто. Обычно менеджеры предназначены для работы с моделью, к которой принадлежат, по этому наследовать их в дочерних моделях - не всегда хорошая идея. К тому же первый менеджер в модели будет *менеджером по-умолчанию*, и очень важно что бы это так и работало. Вот как Django решает эти проблемы при :ref:`наследовании моделей <model-inheritance>`: Тип автоматически создаваемого менеджера Собственные менеджеры Собственные менеджеры и наследование моделей Django выполняет копирование экземпляра менеджера при определенных запросах. Если ваш менеджер нельзя скопировать, эти запросы перестанут работать. Django позволяет указать, что созданный вам менеджер должен использоваться как "автоматически созданный менеджер", каждый раз когда он добавлен в модель как менеджер по-умолчанию. Это можно сделать используя атрибут ``use_for_related_fields``:: Не фильтруйте результаты запроса в таких менеджерах Еще один пример... Например, мы хотим добавить еще один менеджер и в то же время оставить менеджер по-умолчанию из ``AbstractBase``. Вы не можете просто добавить новый менеджер в дочернюю модель, т.к. вам нужно будет так же добавить менеджер из абстрактной модели перед ним, что бы он был менеджером по-умолчанию. Мы можем добавить дополнительный менеджер в другую модель, и добавить в наследование *после* базовой:: Например, следующая модель содержит *два* менеджера -- один возвращает все книги, второй - только книги Roald Dahl:: Например, этот ``Manager`` имеет метод ``with_counts()``, который возвращает список всех объектов ``OpinionPoll``, каждый из которых содержит дополнительный атрибут ``num_responses`` с результатом агрегации:: Например:: С учетом целей, для которых он используется, имя этого атрибута (``use_for_related_fields``) может звучать немного странно. Изначально этот атрибут использовался для определения менеджера для доступа к связанным объектам, вот откуда это название. В то время, когда стало понятно на сколько это широко можно использовать эту концепцию, имя не изменилось. Это было сделано, что бы существующий код :doc:`продолжал работать </misc/api-stability>` в следующих версиях Django. ``default_manager`` - менеджер по-умолчанию. Менеджер ``objects`` так же можно использовать, т.к. он был унаследован. Он просто не используется как менеджер по-умолчанию. Если стандартный менеджер(:class:`django.db.models.Manager`) вас не устраивает, вы можете указать Django  использовать менеджер по-умолчанию используя аргумент ``use_for_related_fields`` в классе менеджера. Все это описано в manager-types_. Если этот атрибут используется для менеджера *по-умолчанию* (это работает только для менеджера по-умолчанию), Django будет использовать его каждый раз при автоматическом создании менеджера, иначе будет использован :class:`django.db.models.Manager`. Если вы переопределите метод ``get_query_set()`` и отфильтруете часть результата, Django вернет неверный результат. Не делайте этого. Менеджер, который фильтрует результат запроса в ``get_query_set()`` не подходит на роль автоматически создаваемого менеджера. При использовании собственного объекта ``Manager``,помните что первый ``Manager``, который заметит Django (в том порядке, в котором они определяются в модели) имеет особый статус. Для Django первый ``Manager`` будет ``Manager`` "по-умолчанию", и некоторые компоненты Django (включая :djadmin:`dumpdata`) будут использовать этот ``Manager``. По-этому нужно быть осторожным при выборе менеджера по-умолчанию, что бы переопределив ``get_query_set()`` не попасть в ситуацию, когда вы не можете получить нужный объект. Унаследовав от него модель, ``objects`` станет менеджером по-умолчанию, если мы не определим другой менеджер в дочерней модели :: Если вы хотите унаследоваться от ``AbstractBase``, но использовать другой менеджер по-умолчанию, вы можете определить менеджер по-умолчанию таким способом:: Проблемы реализации Имя менеджера Менеджеры Менеджеры из не абстрактной базовой модели *не* наследуются дочерними. Если вы хотите унаследовать менеджер из не абстрактной родительской модели, добавьте его в дочернюю модель. Такие менеджеры обычно тесно связаны с моделью, по этому их наследование может привести к проблемам (по крайней мере менеджер по-умолчанию). Таким образом, они не передаются на дочерние классы. Менеджеры абстрактного класса наследуются дочерним классом, используя правила именования Python (имена дочернего класса переопределяют имена родительского).Абстрактные классы созданы для работы с общими данными дочерних классов. Определение общих менеджеров - важная часть абстрактных моделей. Изменение базового QuerySets менеджера Конечно же, т.к. ``get_query_set()`` возвращает экземпляр ``QuerySet``, вы можете использовать ``filter()``, ``exclude()`` и остальные методы ``QuerySet``. Например:: Одно из назначений автоматически создаваемого менеджера - доступ к связанным объектам. В этом случае Django должен иметь возможность получить *все* связанные объекты. Добавляйте ``use_for_related_fields`` при определении класса Для некоторых случаев обычный класс не подойдет. Один из примеров это приложение :mod:`django.contrib.gis` которое включено в Django. Все ``gis`` модели должны использовать специальный менеджер (:class:`~django.contrib.gis.db.models.GeoManager`), т.к. они должны использовать особый ``QuerySet`` класс (:class:`~django.contrib.gis.db.models.GeoQuerySet`) для работы с базой данных.  Получается что они должны использовать специальный менеджер каждый раз, когда Django должен автоматически создать его. Атрибут ``use_for_related_fields`` должен быть добавлен в *класс* менеджера, не в *экземпляр* класса. Пример выше показывает верный вариант, в то время как этот не будет работать:: Менеджером по-умолчанию  становится первый менеджер определенный в модели. Если он отсутствует, используется менеджер по-умолчанию первого абстрактного класса среди родительских моделей, если он существует. Если таким образом не удалось определить менеджер по-умолчанию, используется стандартный менеджер Django. Как работает ``Manager`` описано в разделе :doc:`/topics/db/queries`; этот раздел описывает как изменить поведение менеджера модели. Есть две причины почему вам может понадобиться изменить ``Manager``: добавить дополнительные методы, и/или изменить базовый ``QuerySet``, который возвращает ``Manager``. Эти правила позволяют достаточно гибко добавить собственные менеджеры в модель через абстрактные модели, в то же время имея возможность переопределить менеджер по-умолчанию. Например, у нас есть такой базовый класс:: Этот раздел уже упоминался несколько раз там, где говорилось что Django создает менеджер для тебя: `default managers`_ и "стандартный" менеджер используемые для `access related objects`_.  Есть и другие ситуация, когда Django создает временные менеджеры. Обычно это экземпляры класса :class:`django.db.models.Manager`. Этот пример позволяет выполнить ``Person.men.all()``, ``Person.women.all()``, и ``Person.people.all()``для получения соответствующего результата. Этот пример так же показывает как мы можем использовать несколько менеджеров в одной модели. Вы можете добавить столько экземпляров ``Manager()``, сколько вы пожелаете. Это позволяет легко добавить набор "стандартных" фильтров для вашей модели. Для большинства менеджеров это не будет проблемой. Если вы просто добавить метод в ``Manager``, вряд ли он станет не копируемый. Однако, если вы измените ``__getattr__`` или какой-либо другой приватный метод, который контролирует состояние объекта, вы должны убедиться что объект можно скопировать. В этом разделе мы будем использовать термит "автоматически созданный менеджер" подразумевая менеджер, который Django создает для вас  -- будь то менеджер по-умолчанию для модели без определенных менеджеров, или временный менеджер для доступа к связанным объектам. Использования менеджеров для получения связанных объектов Обращение к ``Person.objects`` вызовет исключение ``AttributeError``, в то время как ``Person.people.all()`` вернет список всех объектов ``Person``. Всегда должно работать копирование экземпляра менеджера, то есть должен работать такой код:: Вы можете использовать ``OpinionPoll.objects.with_counts()`` что бы получить список объектов ``OpinionPoll`` с атрибутом ``num_responses``. Для этой простой модели, ``Book.objects.all()`` вернет все книги из базы данных, в то время как ``Book.dahl_objects.all()`` вернет книги Roald Dahl. Каким должен быть класс автоматически создаваемого менеджера Вы так же не должны изменять атрибут экземпляра класса менеджера, т.к. значение атрибута класса обрабатывается в момент объявления класса и в дальнейшем не переопределяется. Устанавливайте атрибут в классе менеджера при его объявлении, как в примере выше, и все будет работать правильно. Вы можете изменить базовый ``QuerySet`` переопределив метод ``Manager.get_query_set()``. Метод ``get_query_set()`` возвращает ``QuerySet`` с необходимыми вам свойствами. Вы можете использовать собственный менеджер создав его через наследование от основного класса ``Manager`` и добавив его в модель. 