# The idea — verbatim

Source: Mike Shevchenko, Telegram, 2026-09-12 12:18, quoted into the DPC Research group on
2026-09-13 05:57 UTC as message 67 ([chat/67](chat/67-mike-055707.md)). Nothing below is edited.

> идея: USPEX для цифровой эволюции нервных систем. Не «эмулируем муху и называем её слоном»,
> а выращиваем lineage существ из реального connectome-seed.
>
> 1. семя — не все веса, а наследуемая грамматика.
>    Из FlyWire берём модули и мотивы: типы нейронов, excitatory/inhibitory баланс,
>    повторяющиеся graph motifs, сенсорные и моторные контуры. Это первый геном, а не
>    зацементированный мозг на 140k узлов.
>
> 2. тело и мозг растут вместе.
>    Геном описывает: какие сегменты/суставы/сенсоры есть у тела и как нейромодули
>    дублируются, соединяются, специализируются. Не прыжок «муха → слон», а curriculum:
>    fly → жук → шестиногий грузовик → мелкий четвероногий → тяжёлый четвероногий.
>
> 3. операция USPEX, только на живом графе.
>    - heredity: склеиваем рабочие модули мозга и тела двух предков;
>    - softmutation: меняем связи там, где controller нечувствителен/пластичен, а не рубим
>      случайные аксоны;
>    - permutation: меняем роль/тип модулей или сенсорный канал;
>    - random embryos и diversity archive не дают всем превратиться в одного
>      симуляторного таракана.
>
> 4. local relaxation = жизнь потомка.
>    Каждый мутант сначала проходит короткую «юность»: ограниченная plasticity/обучение в
>    нескольких безопасных мирах. Только после этого меряем fitness. Это аналог
>    DFT-relaxation у USPEX: оцениваем не сырой эмбрион, а то, во что он устойчиво
>    складывается.
>
> 5. fitness не один «не упал».
>    multi-objective: энергия, устойчивость, скорость, восстановление после поломки
>    сенсора/сустава, новизна стратегии, перенос на unseen terrain. Отдельный закрытый набор
>    арен — иначе победит тот, кто нашёл дыру в MuJoCo.
>
> Главный артефакт проекта — не один слонячий ролик, а эволюционное древо: какая мутация
> появилась, какой модуль унаследован от мухи, что выросло, где линия сломалась и какие
> навыки пережили смену тела.
>
> Это был бы не biological elephant. Это был бы первый честный connectome-seeded artificial
> organism.

The author's own named next step, from the same message:

> Если будешь развивать дальше — самый интересный следующий шаг, на мой взгляд, это
> формализация представления генома (как именно записывается наследуемая грамматика модулей
> и правил роста). От этого зависит почти всё остальное.

Two claims in the text did not survive the thread and are recorded here so the idea is read
with them: "first" is not true (OpenWorm since 2014, C. elegans whole-body simulators,
whole-fly-brain emulation on Loihi 2, and a connectome-as-controller fly in 2026 — see
[literature.md](literature.md)); and the short "youth" of point 4 is exactly the mechanism
arXiv 2508.17464 measured as the source of mis-ranking. Neither kills the idea; both change
where it starts.
