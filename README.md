# Синхронный стек
## Работа состоит из двух частей: моделирования в Logisim и описания схемы на SystemVerilog.
* Собрать схему "Синхронный стек". Размер (число ячеек) – 5. Одна ячейка хранит 4 бита. У стека нет состояния “занятости” (занято/свободно). Синхронизация (CLK) должна работать по высокому уровню.
* Схема должна обрабатывать следующие команды (подаются через вход команд COMMAND):
  * 0 – nop (нет операции)
  * 1 – push (положить значение ячейки на вершину стека)
  * 2 – pop (снять значение ячейки с вершины стека)
  * 3 – get (получить значение ячейки по индексу, относительно вершины стека)
* Добавлен отчет
 
# Моделирование кэша
* Необходимо программно смоделировать работу кэша процессора в трёх вариантах: с политикой вытеснения LRU, bit-pLRU и Round-robin.
* Добавлен отчет

# ISA
* Необходимо написать программу-транслятор (дизассемблер), с помощью которой можно преобразовывать машинный код (извлеченный из elf-файла) в текст программы на языке ассемблера. 
* Должен поддерживаться следующий набор команд RISC-V: RV32I, RV32M.
* Кодирование: little endian.
* Вывод регистров: ABI.
* Добавлен отчет
  
# OpenMP
* Необходимо написать программу, проводящую расчет объёма правильного октаэдра методом Монте-Карло.
* Помимо написания программы, необходимо провести замеры времени работы на вашем компьютере и привести графики времени работы программы (некоторые графики из следующих подпунктов можно объединить в один):
  * при различных значениях числа потоков при одинаковом параметре schedule* (без chunk_size);
  * при одинаковом значении числа потоков при различных параметрах schedule* (с chunk_size);
  * с выключенным openmp и с включенным с 1 потоком.
* Добавлены программы строящие графики
* Добавлен отчет
