��          |      �          3   !  >   U  ;   �  "   �  T   �  T   H  �   �  j   %  A   �  v   �  ~  I    �  c   �  u   K  �   �  A   E  �   �  �   	  �   �	  �   F
  �   �
  �   q  E                         
         	                           Enable information about the previous GPO key value Get information about applied policies for the current machine Get information about applied policies for the current user Information about applied policies Information about policy keys and values by guid
* Not applicable with <-l>/<--list> Information about policy keys and values by name
* Not applicable with <-l>/<--list> Output format (DEFAULT): is similar to the common output, in addition, the applied keys, policy values  and preferences are also output Output format: common output including environment information; outputs only the names of applied policies Output format: display of policy keys, values and previous values Output format: output of GPO names and their GUIDs
* Not applicable with <-i>/<--policy_guid> and <-i>/<--policy_name> Set column widths for outputting internal tables (keys and values, preferences, ...)
* If the specified value is less than or equal to 0, the width of the columns
  will be equal to the maximum length of the row
* By default, the column width is equal to the length of the maximum row
* If the length of the maximum string is less than the specified value, the width will not change Project-Id-Version: PACKAGE VERSION
Report-Msgid-Bugs-To: 
PO-Revision-Date: YEAR-MO-DA HO:MI+ZONE
Last-Translator: FULL NAME <EMAIL@ADDRESS>
Language-Team: LANGUAGE <LL@li.org>
Language: Russian
MIME-Version: 1.0
Content-Type: text/plain; charset=UTF-8
Content-Transfer-Encoding: 8bit
 Включение информации о предыдущих значениях ключей GPO Получить информацию о примененных политиках для текущей машины Получить информацию о примененных политиках для текущего пользователя Информация о примененных политиках Информация о ключах и значениях политики по GUID
* Не применяется с <-l>/<--list> Информация о ключах и значениях политики по ее имени
* Не применяется с <-l>/<--list> Формат вывода (ПО УМОЛЧАНИЮ): схож с форматом <common>, отображает дополнительную информацию о GPO Формат вывода: сжатый вывод, включающий информацию о системе; отображаются только имена GPO Формат вывода: отобразить ключи GPO, текущие и предыдущие значения ключей Формат вывода: отображаются имена GPO и их GUID
* Не применяется с <-i>/<--policy_guid> и <-i>/<--policy_name> Задать ширину столбцов для вывода внутренних таблиц (ключи и значения, настройки, ...)
* Если указано значение <= 0, то ширина столбцов
  будет равна максимальной длине строки
* По умолчанию ширина столбцов равна длине максимальной строки
* Если длина максимальной строки меньше заданного значения, то ширина не изменяется 