# [Простой телеграм-бот](https://t.me/pf_1122_bot)
## Калькулятор:

<img alt="calc1" src="img/calc1.png" width="800"/>

<img alt="calc2" src="img/calc2.png" width="800"/>

## Крестики-нолики:

<img alt="game1.png" src="img/game1.png" width="800"/>
<img alt="game2.png" src="img/game2.png" width="800"/>

## Детектор предметов одежды на фото

[DeepFashion2 json annotations](https://drive.google.com/file/d/1ADv8rePEUis8bp6gfR1l38nE6CSWghVj/view?usp=sharing)
```
mkdir ./DeepFashion2/
gdown --id 1ADv8rePEUis8bp6gfR1l38nE6CSWghVj  -O ./DeepFashion2/json.zip
unzip ./DeepFashion2/json.zip -d ./DeepFashion2/ > /dev/null
rm -f ./DeepFashion2/json.zip
```

[Trained model weights](https://drive.google.com/file/d/1yQLcr73AMfT0baNi0QxwN_A8qx92LzHo/view?usp=sharing)
```
gdown --id 1yQLcr73AMfT0baNi0QxwN_A8qx92LzHo -O ./model/model_0021999.pth
```

Примеры:

<img alt="deep_fashion_1.png" src="img/deep_fashion_1.png" width="1000"/>
<img alt="deep_fashion_2.png" src="img/deep_fashion_2.png" width="1000"/>
<img alt="deep_fashion_3.png" src="img/deep_fashion_3.png" width="1000"/>
